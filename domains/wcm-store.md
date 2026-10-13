# Domínio: wcm-store

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_STOREITEM_METRIC

Métricas de uso (downloads e visualizações) de itens da loja de componentes WCM, por tenant.

**Ciclo de vida:** Linha criada no primeiro acesso/download do item por tenant; contadores incrementados.

**Atenção:** Unique (TENANT_ID, COMPONENT_CODE). DOWNLOADS/VIEWS são bigint no banco, mas Integer na entidade.

**PK:** STOREITEM_METRIC_ID · **Unique:** (TENANT_ID, COMPONENT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `STOREITEM_METRIC_ID` | bigint | N | PK surrogate da métrica. |  |  |
| `COMPONENT_CODE` | varchar(40) | N | Código do componente/item na loja (até 40). |  |  |
| `NAME` | varchar(255) | N | Nome do item da loja. |  |  |
| `DEVELOPER_CODE` | varchar(80) | N | Código do desenvolvedor do item. |  |  |
| `DEVELOPER_NAME` | varchar(80) | N | Nome do desenvolvedor do item. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) dono da métrica. |  | FDN_TENANT.TENANT_ID |
| `DOWNLOADS` | bigint | S | Contagem de downloads do item pelo tenant. |  |  |
| `VIEWS` | bigint | S | Contagem de visualizações do item pelo tenant. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant da métrica.

**Dicas de consulta:** Filtrar sempre por TENANT_ID. Índice por COMPONENT_CODE.
