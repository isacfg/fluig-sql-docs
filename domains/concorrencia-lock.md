# Domínio: concorrencia-lock

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_LOCK

Locks distribuídos de recursos: indica que um item de uma funcionalidade está bloqueado por uma instância/sessão (UUID).

**Ciclo de vida:** Linha criada ao adquirir o lock e removida ao liberar; transitória, poucas linhas.

**Atenção:** PK composta (TENANT_ID, FEATURE_TYPE, ITEM_ID). Locks órfãos podem ficar se o servidor cair. Java tem FDNLock com id composto (por isso campos repetidos).

**PK:** TENANT_ID, FEATURE_TYPE, ITEM_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TENANT_ID` | bigint | N | Tenant do lock; parte da PK composta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `FEATURE_TYPE` | bigint | N | Tipo da funcionalidade bloqueada (inteiro); parte da PK. Valores definidos por quem solicita o lock. |  |  |
| 🔑 `ITEM_ID` | bigint | N | Identificador do item bloqueado dentro da funcionalidade; parte da PK. |  |  |
| `UUID` | varchar(36) | N | UUID do dono do lock (sessão/instância que o adquiriu). |  |  |

**Dicas de consulta:** Consultar pela PK completa.
