# Domínio: privacy-lgpd

6 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_PDATATRACE

Rastro de acesso/alteração de dados pessoais (LGPD): quem, quando, qual recurso e campos.

**Ciclo de vida:** Uma linha por evento rastreado; expurgo por EXPIRATION_DAYS em FDN_PDATATRACE_CONFIG; volume alto.

**Atenção:** Filtrar por TENANT_ID e USER_TENANT_ID (índice fdn_pdatatrace__idx1). RESOURCE_* são textos.

**PK:** PDATATRACE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PDATATRACE_ID` | bigint(20) | N | PK surrogate do rastro. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant do evento. |  | FDN_TENANT.TENANT_ID |
| `USER_TENANT_ID` | bigint(20) | N | Usuário (vínculo usuário-tenant) relacionado ao evento. |  | FDN_USERTENANT.USER_TENANT_ID |
| `TYPE` | int(11) | N | Tipo do evento (enum DatatraceEventType). | 0=CREATE; 1=EDIT; 2=VIEW |  |
| `SOURCE` | int(11) | N | Origem do evento (enum DatatraceEventSource). | 0=USER_REST; 1=CARD_REST; 2=WORKFLOW_WEBSERVICE |  |
| `RESOURCE_TABLE` | varchar(255) | N | Tabela/entidade do recurso com dado pessoal acessado. |  | FDN_PERSONALDATA.TABLE_ID |
| `RESOURCE_KEY` | varchar(255) | N | Nome da chave do recurso (campo identificador). |  |  |
| `RESOURCE_ID` | varchar(255) | N | Valor do identificador do registro acessado, como texto. |  |  |
| `FIELDS` | varchar(255) | N | Campos de dados pessoais envolvidos (lista em texto). |  | FDN_PERSONALDATA.FIELD_ID |
| `USER_IP` | varchar(50) | S | IP de origem da requisição (dado pessoal). |  |  |
| `DATATRACE_TIMESTAMP` | datetime | N | Data e hora do evento. |  |  |

**Relacionamentos (saem desta tabela):**

- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · logical-probable/probable — Usuário associado ao evento.
- `(RESOURCE_TABLE, FIELDS)` → **FDN_PERSONALDATA** `(TABLE_ID, FIELD_ID)` · N:1 · logical-probable/probable — Catálogo de dados pessoais correspondente à tabela/campos rastreados.

**Dicas de consulta:** Contém IP e identifica acessos a dados pessoais; tratar como sensível.

## FDN_PDATATRACE_CONFIG

Configuração do rastreamento de dados pessoais por tenant: ativo e retenção em dias.

**Ciclo de vida:** Uma linha por tenant (unique).

**Atenção:** Unique fdn_datatrace_config_idx1 em TENANT_ID.

**PK:** PDATATRACE_CONFIG_ID · **Unique:** (TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PDATATRACE_CONFIG_ID` | bigint | N | PK surrogate. |  |  |
| `ENABLED` | bit | N | Indica se o rastreamento está ativo no tenant. | 1=ativo; 0=inativo |  |
| `EXPIRATION_DAYS` | integer | S | Dias de retenção dos registros de FDN_PDATATRACE; NULL provavelmente sem expiração. |  |  |
| `TENANT_ID` | bigint | N | Tenant configurado (único). |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · 1:1 · logical-probable/probable — Tenant da configuração.

**Dicas de consulta:** 1 linha por tenant.

## FDN_PDATA_CLASSIFICATION

Catálogo de classificações de dados pessoais (base legal/categoria) usado nas justificativas LGPD.

**Ciclo de vida:** Dados de referência; poucas linhas.

**Atenção:** Sem tenant.

**PK:** PDATA_CLASSIFICATION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PDATA_CLASSIFICATION_ID` | bigint | N | PK da classificação. |  |  |
| `PDATA_CLASSIFICATION` | varchar(255) | N | Texto/chave da classificação de dado pessoal. |  |  |

**Relacionamentos (saem desta tabela):**

- `(PDATA_CLASSIFICATION_ID)` → **FDN_PDATA_JUSTIFICATION** `(PDATA_CLASSIFICATION_ID)` · 1:N · physical-fk/confirmed — Justificativas que usam a classificação.

**Dicas de consulta:** Tabela de domínio.

## FDN_PDATA_INFOTYPE

Catálogo de tipos de informação de dados pessoais (ex.: identificação, contato) usados em FDN_PERSONALDATA.

**Ciclo de vida:** Dados de referência; poucas linhas.

**Atenção:** Sem tenant.

**PK:** INFORMATION_TYPE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `INFORMATION_TYPE_ID` | bigint | N | PK do tipo de informação. |  |  |
| `INFORMATION_TYPE` | varchar(255) | N | Texto/chave do tipo de informação. |  |  |

**Relacionamentos (saem desta tabela):**

- `(INFORMATION_TYPE_ID)` → **FDN_PERSONALDATA** `(INFORMATION_TYPE_ID)` · 1:N · physical-fk/confirmed — Dados pessoais deste tipo.

**Dicas de consulta:** Tabela de domínio.

## FDN_PDATA_JUSTIFICATION

Justificativa de tratamento de um dado pessoal cadastrado, associada a uma classificação.

**Ciclo de vida:** Criada ao justificar um registro de FDN_PERSONALDATA.

**Atenção:** Sem tenant direto; herdado de FDN_PERSONALDATA.

**PK:** PDATA_JUSTIFICATION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PDATA_JUSTIFICATION_ID` | BIGINT | N | PK da justificativa. |  |  |
| `PDATA_JUSTIFICATION` | VARCHAR(500) | N | Texto livre da justificativa (até 500 caracteres). |  |  |
| `PERSONALDATA_ID` | BIGINT | N | Dado pessoal justificado. |  | FDN_PERSONALDATA.PERSONALDATA_ID |
| `PDATA_CLASSIFICATION_ID` | BIGINT | N | Classificação aplicada. |  | FDN_PDATA_CLASSIFICATION.PDATA_CLASSIFICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(PERSONALDATA_ID)` → **FDN_PERSONALDATA** `(PERSONALDATA_ID)` · N:1 · physical-fk/confirmed — Dado pessoal (FK FK_FDNPDATAJUSTIFICATION001; JPA personalData).
- `(PDATA_CLASSIFICATION_ID)` → **FDN_PDATA_CLASSIFICATION** `(PDATA_CLASSIFICATION_ID)` · N:1 · physical-fk/confirmed — Classificação (FK FK_FDNPDATAJUSTIFICATION002; JPA classification).

**Dicas de consulta:** Join com FDN_PERSONALDATA e FDN_PDATA_CLASSIFICATION.

## FDN_PERSONALDATA

Catálogo de dados pessoais por tenant: tabela e campo que contêm dado pessoal, sensibilidade e se permitem anonimização.

**Ciclo de vida:** Cadastrado por usuário; removido logicamente (REMOVED=1 e REMOVAL_DATE).

**Atenção:** Soft-delete via REMOVED/REMOVAL_DATE. Unique key (artefato UNIQUE) provavelmente em tenant+tabela+campo.

**PK:** PERSONALDATA_ID · **Unique:** (TENANT_ID, TABLE_ID, FIELD_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PERSONALDATA_ID` | BIGINT | N | PK do dado pessoal cadastrado. |  |  |
| `TENANT_ID` | bigint | N | Tenant do cadastro. |  | FDN_TENANT.TENANT_ID |
| `TABLE_ID` | varchar(255) | N | Identificador/nome da tabela que contém o dado pessoal. |  |  |
| `FIELD_ID` | varchar(255) | N | Identificador/nome do campo com dado pessoal. |  |  |
| `ALLOWS_ANONYMIZATION` | bit | N | Indica se o dado pode ser anonimizado. | 1=permite; 0=não |  |
| `CREATION_DATE` | datetime | N | Data e hora do cadastro. |  |  |
| `REMOVED` | bit | S | Marca de remoção lógica. | 1=removido; 0/NULL=ativo |  |
| `REMOVAL_DATE` | datetime | S | Data e hora da remoção lógica. |  |  |
| `SENSITIVE_DATA` | bit | N | Indica dado pessoal sensível (LGPD). | 1=sensível; 0=comum |  |
| `TABLE_DESCRIPTION` | varchar(255) | N | Descrição legível da tabela. |  |  |
| `FIELD_DESCRIPTION` | varchar(255) | N | Descrição legível do campo. |  |  |
| `USER_TENANT_ID` | bigint | N | Usuário que cadastrou o dado pessoal. |  | FDN_USERTENANT.USER_TENANT_ID |
| `REMOVED_BY_USER_TENANT_ID` | bigint | S | Usuário que removeu o cadastro. |  | FDN_USERTENANT.USER_TENANT_ID |
| `INFORMATION_TYPE_ID` | bigint | N | Tipo de informação do dado pessoal. |  | FDN_PDATA_INFOTYPE.INFORMATION_TYPE_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.
- `(INFORMATION_TYPE_ID)` → **FDN_PDATA_INFOTYPE** `(INFORMATION_TYPE_ID)` · N:1 · physical-fk/confirmed — Tipo de informação.
- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Usuário que cadastrou.
- `(REMOVED_BY_USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Usuário que removeu.
- `(PERSONALDATA_ID)` → **FDN_PDATA_JUSTIFICATION** `(PERSONALDATA_ID)` · 1:N · physical-fk/confirmed — Justificativas do dado.

**Dicas de consulta:** Filtrar por TENANT_ID e REMOVED (NULL ou 0) para ativos. Descreve metadados, não contém os dados pessoais em si.
