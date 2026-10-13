# Domínio: audit

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FLUIG_AUDIT

Trilha de auditoria de ações de usuários sobre recursos do Fluig (criar, editar, remover etc.).

**Ciclo de vida:** Uma linha por evento auditado; cresce continuamente e é expurgada conforme EXPIRATION_DAYS de FLUIG_AUDIT_CONFIG; volume alto.

**Atenção:** Sempre filtrar por TENANT_ID (índice fluig_audit_idx1: TENANT_ID, USER_TENANT_ID, RESOURCE_NAME, RESOURCE_KEY). RESOURCE_KEY é texto, não FK.

**PK:** AUDIT_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `AUDIT_ID` | bigint(20) | N | PK surrogate do evento de auditoria. |  |  |
| `DETAIL` | varchar(255) | S | Descrição curta/chave do detalhe do evento. |  |  |
| `DETAIL_PARAMS` | longtext | S | Parâmetros do detalhe (LOB longtext), provavelmente JSON/texto serializado. |  |  |
| `USER_IP` | varchar(50) | S | Endereço IP do usuário que executou a ação (dado pessoal). |  |  |
| `RESOURCE_NAME` | varchar(255) | N | Nome do tipo de recurso auditado (ex.: tabela/entidade). |  |  |
| `RESOURCE_KEY` | varchar(255) | N | Chave/identificador do registro do recurso auditado, como texto. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant em que o evento ocorreu. |  | FDN_TENANT.TENANT_ID |
| `AUDIT_TIMESTAMP` | datetime | N | Data e hora do evento. |  |  |
| `TYPE` | int(11) | N | Tipo do evento auditado (enum FluigAuditEventType). | 0=CREATE; 1=EDIT; 2=REMOVE; 3=RESTORE; 4=DOWNLOAD; 5=INACTIVE; 6=EXECUTE |  |
| `USER_TENANT_ID` | bigint(20) | N | Usuário (vínculo usuário-tenant) que executou a ação. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · logical-probable/probable — Usuário executor; sem FK física, nome/semântica coincidem.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant do evento.

**Dicas de consulta:** Contém IP do usuário (dado pessoal) e possivelmente dados em DETAIL_PARAMS (LOB). Filtre por TENANT_ID e AUDIT_TIMESTAMP.

## FLUIG_AUDIT_CONFIG

Configuração de auditoria por tenant: habilita/desabilita e define retenção em dias.

**Ciclo de vida:** Uma linha por tenant (unique em TENANT_ID).

**Atenção:** Unique fluig_audit_config_idx1 em TENANT_ID.

**PK:** AUDIT_CONFIG_ID · **Unique:** (TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `AUDIT_CONFIG_ID` | bigint | N | PK surrogate da configuração. |  |  |
| `ENABLED` | bit | N | Indica se a auditoria está ativa no tenant. | 1=ativa; 0=inativa |  |
| `EXPIRATION_DAYS` | integer | S | Dias de retenção dos registros de FLUIG_AUDIT antes do expurgo; NULL provavelmente sem expiração. |  |  |
| `TENANT_ID` | bigint | N | Tenant configurado (único). |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · 1:1 · logical-probable/probable — Tenant da configuração.

**Dicas de consulta:** Máximo 1 linha por tenant.
