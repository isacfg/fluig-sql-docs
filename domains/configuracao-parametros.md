# Domínio: configuracao-parametros

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_PARAMGERAL

Parâmetros gerais de configuração em pares chave/valor, por tenant (ou globais quando TENANT_ID é nulo).

**Ciclo de vida:** Gravada/atualizada por administração e pelo sistema; baixo volume.

**Atenção:** TENANT_ID anulável. Unique (provável) TENANT_ID + DATA_KEY. A relação inferida com FLUIG_RUNTIMEDATA_PROCESS_MNGR é falsa.

**PK:** PARAMGERAL_ID · **Unique:** (TENANT_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PARAMGERAL_ID` | bigint(20) | N | Chave primária. |  |  |
| `DATA_KEY` | varchar(255) | N | Chave do parâmetro de configuração. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor do parâmetro (até 4000 caracteres). |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant do parâmetro; nulo indica global. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant (também FK física).

**Dicas de consulta:** DATA_VALUE pode conter segredos/configuração sensível dependendo da chave.
