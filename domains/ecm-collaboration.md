# Domínio: ecm-collaboration

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## ECM_COLLABORATION

Sessão de colaboração externa (edição online em app de terceiros, ex. Office365/Google) vinculada a uma versão de documento do ECM. Criada ao iniciar a colaboração.

**Ciclo de vida:** Uma linha por colaboração iniciada; IS_ACTIVE=false ao encerrar (END_DATE preenchido). Cascade REMOVE remove os convidados.

**Atenção:** Multi-tenant por TENANT_ID (não COD_EMPRESA). SOURCE_DOC_* é o documento original; DOCUMENT_* é o documento/versão colaborado (cópia/versão de trabalho).

**PK:** COLLABORATION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COLLABORATION_ID` | bigint | N | Identificador gerado (GenerationType.AUTO) da colaboração. |  |  |
| `IS_ACTIVE` | bit | N | Indica se a colaboração está em andamento. | 1=ativa; 0=encerrada |  |
| `DOCUMENT_ID` | integer | N | Documento ECM em colaboração. |  | DOCUMENTO.NR_DOCUMENTO |
| `DOCUMENT_VERSION` | integer | N | Versão do documento em colaboração. |  | DOCUMENTO.NR_VERSAO |
| `END_DATE` | datetime | S | Data/hora de término da colaboração. |  |  |
| `EXTENSION` | varchar(255) | S | Extensão do arquivo colaborado (ex. docx, xlsx). |  |  |
| `EXTERNAL_FILE_ID` | varchar(255) | S | ID do arquivo no serviço externo de colaboração; usado em lookup (findByExternalFileId). |  |  |
| `EXTERNAL_URL` | varchar(255) | S | URL do arquivo no serviço externo para abrir a edição. |  |  |
| `SOURCE_DOC_ID` | integer | N | Documento ECM de origem a partir do qual a colaboração foi iniciada (imutável). |  | DOCUMENTO.NR_DOCUMENTO |
| `SOURCE_DOC_VERSION` | integer | N | Versão do documento de origem (imutável). |  | DOCUMENTO.NR_VERSAO |
| `START_DATE` | datetime | S | Data/hora de início da colaboração. |  |  |
| `TENANT_ID` | bigint | N | Tenant/empresa dona da colaboração (imutável após insert). |  | FDN_TENANT.TENANT_ID |
| `UPLOADER_LOGIN` | varchar(255) | N | Login do usuário que iniciou/enviou o arquivo à colaboração. |  | FDN_USERTENANT.LOGIN |
| `COLLABORATION_APP_ID` | bigint | N | FK para o app de colaboração utilizado. |  | ECM_COLLABORATION_APP.ID |

**Relacionamentos (saem desta tabela):**

- `(COLLABORATION_APP_ID)` → **ECM_COLLABORATION_APP** `(ID)` · N:1 · physical-fk/confirmed — App de colaboração usado.
- `(TENANT_ID, DOCUMENT_ID, DOCUMENT_VERSION)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão do documento colaborada (sem FK).
- `(COLLABORATION_ID)` → **ECM_COLLABORATION_GUEST** `(COLLABORATION_ID)` · 1:N · jpa-join/confirmed — Convidados da colaboração (OneToMany guests).
- `(COLLABORATION_ID)` → **ECM_COLLABORATION_APP** `(ID)` · N:1 · hql-join/confirmed — CollaborationApp.findAppByCollaborationId

**Dicas de consulta:** Filtrar por TENANT_ID. Ativa: IS_ACTIVE=1 por (DOCUMENT_ID, DOCUMENT_VERSION). Linha tem URLs/IDs externos; sem dado pessoal direto além de UPLOADER_LOGIN.

## ECM_COLLABORATION_APP

Cadastro dos aplicativos externos de colaboração (provedores de edição online) habilitados por tenant.

**Ciclo de vida:** Poucas linhas por tenant, configuradas por administração/instalação; raramente alteradas.

**Atenção:** UNIQUE (TENANT_ID, APP_CODE, APP_JNDI_NAME). TENANT_ID e APP_JNDI_NAME não são atualizáveis. CLIENT_SECRET é credencial.

**PK:** ID · **Unique:** (TENANT_ID, APP_CODE, APP_JNDI_NAME)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador gerado da app de colaboração. |  |  |
| `CLIENT_ID` | varchar(255) | S | Client ID OAuth da integração com o provedor externo. |  |  |
| `CLIENT_SECRET` | varchar(255) | S | Client secret OAuth da integração (credencial sensível). |  |  |
| `APP_CODE` | varchar(255) | N | Código identificador da app de colaboração (usado em findByAppCode). |  |  |
| `ENABLED` | varchar(255) | N | Indicador de app habilitada, armazenado como string. |  |  |
| `APP_JNDI_NAME` | varchar(255) | S | Nome JNDI do componente/EJB que implementa a integração com a app. |  |  |
| `APP_NAME` | varchar(255) | N | Nome de exibição da app de colaboração. |  |  |
| `TENANT_ID` | bigint | N | Tenant dono do registro (imutável). |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(ID)` → **ECM_COLLABORATION** `(COLLABORATION_APP_ID)` · 1:N · physical-fk/confirmed — Colaborações que usam esta app.

**Dicas de consulta:** SENSÍVEL: CLIENT_SECRET e CLIENT_ID são credenciais; não expor. Filtrar por TENANT_ID.

## ECM_COLLABORATION_GUEST

Participantes (convidados) de uma colaboração externa, com permissão no serviço externo.

**Ciclo de vida:** Uma linha por usuário convidado por colaboração; removidas em cascata com a colaboração.

**Atenção:** UNIQUE (COLLABORATION_ID, LOGIN). Sem TENANT_ID; o tenant vem de ECM_COLLABORATION.

**PK:** COLLABORATION_GUEST_ID · **Unique:** (COLLABORATION_ID, LOGIN)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COLLABORATION_GUEST_ID` | bigint | N | Identificador gerado do convidado. |  |  |
| `IS_ACTIVE` | bit | N | Indica se o convidado ainda tem acesso à colaboração. | 1=ativo; 0=inativo |  |
| `END_DATE` | datetime | S | Data/hora de fim do acesso do convidado. |  |  |
| `EXTERNAL_EMAIL` | varchar(255) | S | E-mail do convidado no serviço externo (dado pessoal). |  |  |
| `EXTERNAL_ID` | varchar(255) | S | ID do convidado/permissão no serviço externo. |  |  |
| `EXTERNAL_PERMISSION` | varchar(255) | S | Papel/permissão concedido no serviço externo (ex. leitura/escrita). |  |  |
| `INVITATION_DATE` | datetime | S | Data/hora em que o convite foi enviado. |  |  |
| `LOGIN` | varchar(255) | N | Login do usuário Fluig convidado. |  | FDN_USERTENANT.LOGIN |
| `IS_OWNER` | bit | N | Indica se o convidado é o dono (iniciador) da colaboração. | 1=dono; 0=convidado |  |
| `START_DATE` | datetime | S | Data/hora de início do acesso do convidado. |  |  |
| `COLLABORATION_ID` | bigint | N | FK para a colaboração. |  | ECM_COLLABORATION.COLLABORATION_ID |

**Relacionamentos (saem desta tabela):**

- `(COLLABORATION_ID)` → **ECM_COLLABORATION** `(COLLABORATION_ID)` · N:1 · physical-fk/confirmed — Colaboração à qual pertence.

**Dicas de consulta:** PII: EXTERNAL_EMAIL e LOGIN. Join: GUEST.COLLABORATION_ID = ECM_COLLABORATION.COLLABORATION_ID.
