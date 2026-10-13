# Domínio: infraestrutura-sequencias

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## SEQ_ECM

Tabela de sequências (próximo ID) por empresa e por tabela lógica, usada pelo ECM/workflow para gerar chaves numéricas sem auto-increment.

**Ciclo de vida:** Uma linha por (empresa, tabela); COD_PROX_ID é incrementado a cada geração de ID. Volume muito baixo, altíssima atualização.

**Atenção:** Contador manual: leitura+update concorrentes exigem lock; não alterar manualmente.

**PK:** COD_EMPRESA, CD_TABELA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `CD_TABELA` | varchar(50) | N | Nome/identificador lógico da tabela cujo ID é sequenciado. |  |  |
| `COD_PROX_ID` | integer | N | Próximo valor de ID a ser entregue para a tabela CD_TABELA. |  |  |

**Dicas de consulta:** Não fazer join; é apenas gerador de sequência. Não editar fora do aplicativo.
