# Domínio: use-policy

5 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## POLICYDOCUMENT

Documento de política de uso (termos) em um idioma, com versão de documento, flag de padrão e exigência de consentimento.

**Ciclo de vida:** Criado ao cadastrar documentos na política de uso de um tenant; poucas linhas.

**Atenção:** DOCUMENTID é o ID lógico do documento (ECM), não PK desta tabela.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | integer | N | Chave primária do documento de política (AUTO). |  |  |
| `DOCUMENTDEFAULT` | bit | S | Marca o documento como padrão da política. | 1=padrão; 0/NULL=não |  |
| `CONSENTREQUIRED` | bit | N | Se o aceite explícito do usuário é obrigatório. | 1=obrigatório; 0=não |  |
| `DOCUMENTID` | integer | N | ID do documento (ECM) que contém o texto da política. |  | DOCUMENTO.NR_DOCUMENTO |
| `LANGUAGE` | varchar(255) | N | Idioma do documento (ex.: pt_BR). |  |  |

**Relacionamentos (saem desta tabela):**

- `(ID)` → **POLICYUSER** `(POLICYDOCUMENTID)` · 1:N · jpa-join/confirmed — Aceites de usuários deste documento.

**Dicas de consulta:** Pertence a USEPOLICY via USEPOLICY_POLICYDOCUMENT (tenant vem de USEPOLICY).

## POLICYDOCUMENT_POLICYUSER

Tabela de junção JPA (@OneToMany usersAccepted) entre documento de política e aceites de usuário.

**Ciclo de vida:** Linha criada junto com cada POLICYUSER registrado.

**Atenção:** USERSACCEPTED_ID é único: cada aceite pertence a um só documento. Redundante com POLICYUSER.POLICYDOCUMENTID.

**PK:** POLICYDOCUMENT_ID, USERSACCEPTED_ID · **Unique:** (USERSACCEPTED_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `POLICYDOCUMENT_ID` | integer | N | Documento de política. |  | POLICYDOCUMENT.ID |
| 🔑 `USERSACCEPTED_ID` | integer | N | Aceite de usuário. |  | POLICYUSER.ID |

**Relacionamentos (saem desta tabela):**

- `(USERSACCEPTED_ID)` → **POLICYUSER** `(ID)` · N:1 · physical-fk/confirmed — Aceite do usuário.
- `(POLICYDOCUMENT_ID)` → **POLICYDOCUMENT** `(ID)` · N:1 · physical-fk/confirmed — Documento aceito.

**Dicas de consulta:** Prefira POLICYUSER.POLICYDOCUMENTID para joins diretos.

## POLICYUSER

Registro de aceite/resposta de um usuário a uma versão de documento de política de uso.

**Ciclo de vida:** Criado quando o usuário responde à política; imutável (colunas updatable=false); cresce com usuários.

**Atenção:** Único por (POLICYDOCUMENTID, ALIAS, DOCUMENTVERSION). Contém identificação de usuário.

**PK:** id · **Unique:** (policyDocumentId, alias, documentVersion)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | integer | N | Chave primária do aceite. |  |  |
| `ALIAS` | varchar(255) | N | Alias/identificador do usuário que respondeu. |  | FDN_USERTENANT.USER_CODE |
| `DOCUMENTVERSION` | integer | N | Versão do documento aceita pelo usuário. |  |  |
| `RESPONSEDATE` | datetime | S | Data/hora da resposta do usuário (default now na criação). |  |  |
| `USERNAME` | varchar(255) | N | Login/nome do usuário que aceitou (indexado). |  | FDN_USERTENANT.LOGIN |
| `POLICYDOCUMENTID` | integer | N | Documento de política respondido. |  | POLICYDOCUMENT.ID |

**Relacionamentos (saem desta tabela):**

- `(POLICYDOCUMENTID)` → **POLICYDOCUMENT** `(ID)` · N:1 · physical-fk/confirmed — Documento de política respondido (jpa-join PolicyUser.policyDocument).

**Dicas de consulta:** Dados pessoais: USERNAME, ALIAS. Não há coluna de tenant: chegue via POLICYDOCUMENT -> USEPOLICY.TENANTID.

## USEPOLICY

Política de uso de um tenant; agrega os documentos de política via USEPOLICY_POLICYDOCUMENT.

**Ciclo de vida:** Uma linha por tenant.

**Atenção:** TENANTID é único: uma política por tenant.

**PK:** id · **Unique:** (tenantId)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | integer | N | Chave primária. |  |  |
| `TENANTID` | bigint | N | Tenant dono da política (único). |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANTID)` → **FDN_TENANT** `(TENANT_ID)` · 1:1 · logical-probable/probable — Tenant da política (sem FK física).
- `(ID)` → **POLICYDOCUMENT** `(ID)` · N:M-via-this-table · jpa-join/confirmed — Documentos via USEPOLICY_POLICYDOCUMENT.

**Dicas de consulta:** Consulta típica: WHERE TENANTID=:tenant.

## USEPOLICY_POLICYDOCUMENT

Tabela de junção JPA entre USEPOLICY e seus POLICYDOCUMENT (@OneToMany documents).

**Ciclo de vida:** Linhas criadas ao salvar a política com seus documentos.

**Atenção:** DOCUMENTS_ID único (um documento pertence a uma só política).

**PK:** USEPOLICY_ID, DOCUMENTS_ID · **Unique:** (DOCUMENTS_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USEPOLICY_ID` | integer | N | Política de uso. |  | USEPOLICY.ID |
| 🔑 `DOCUMENTS_ID` | integer | N | Documento de política. |  | POLICYDOCUMENT.ID |

**Relacionamentos (saem desta tabela):**

- `(DOCUMENTS_ID)` → **POLICYDOCUMENT** `(ID)` · N:1 · physical-fk/confirmed — Documento da política.
- `(USEPOLICY_ID)` → **USEPOLICY** `(ID)` · N:1 · physical-fk/confirmed — Política dona.
