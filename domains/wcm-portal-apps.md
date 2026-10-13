# Domínio: wcm-portal-apps

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_TENANTAPPLICATION

Habilitação de uma aplicação WCM (widget/tema/layout) para um tenant, com código externo opcional.

**Ciclo de vida:** Criada ao instalar/habilitar uma aplicação no tenant; ENABLED_APP alterna a habilitação.

**Atenção:** Unique (TENANT_ID, APPLICATION_ID). Filtrar por TENANT_ID.

**PK:** TENANT_APPLICATION_ID · **Unique:** (TENANT_ID, APPLICATION_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TENANT_APPLICATION_ID` | bigint | N | PK surrogate. |  |  |
| `APP_CODE_EXT` | varchar(40) | S | Código estendido/customizado da aplicação no tenant (findByTenantExtendedAppCode). |  |  |
| `ENABLED_APP` | bit | N | Indica se a aplicação está habilitada no tenant. | 1=habilitada; 0=desabilitada |  |
| `APPLICATION_ID` | bigint | N | Aplicação WCM habilitada. |  | WCM_APPLICATION.APPLICATION_ID |
| `TENANT_ID` | bigint | N | Tenant dono da habilitação. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação habilitada.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.

**Dicas de consulta:** Named queries: findByTenant, findByApplication, findByTenantApplication, findByTenantExtendedAppCode, findByApplicationCode.
