# Domínio: acesso-recente

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_RECENTLY_VIEWED

Itens vistos recentemente por usuário (documento, instância de processo ou página), para o atalho de recentes.

**Ciclo de vida:** Upsert a cada visualização; truncada por rotina de limpeza. Volume médio.

**Atenção:** OBJECT_TYPE define qual coluna é preenchida (NUM_DOCUMENT, NUM_PROCESS_INSTANCE ou PAGE_CODE). LOGIN é textual.

**PK:** RECENTLY_VIEWED_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RECENTLY_VIEWED_ID` | bigint | N | Chave primária. |  |  |
| `TENANT_ID` | bigint | N | Tenant do usuário. |  | FDN_TENANT.TENANT_ID |
| `LOGIN` | varchar(150) | N | Login do usuário que visualizou. |  | FDN_USERTENANT.USER_CODE |
| `OBJECT_TYPE` | varchar(16) | N | Tipo do objeto visto (enum TypeAccessEnum, gravado como string). | PAGE; PROCESS_INSTANCE; DOCUMENT |  |
| `NUM_DOCUMENT` | int | S | Número do documento visto quando OBJECT_TYPE=DOCUMENT. |  | DOCUMENT.NR_DOCUMENTO |
| `NUM_PROCESS_INSTANCE` | int | S | Número da instância de processo quando OBJECT_TYPE=PROCESS_INSTANCE. |  | PROCES_WORKFLOW.NUM_PROCES |
| `PAGE_CODE` | varchar(128) | S | Código da página quando OBJECT_TYPE=PAGE. |  |  |
| `DAT_ACCESS` | datetime | N | Data/hora do último acesso ao item. |  |  |
| `DESCRIPTION` | varchar(254) | S | Descrição/título do item exibido. |  |  |

**Relacionamentos (saem desta tabela):**

- `(NUM_DOCUMENT)` → **DOCUMENTO** `(NR_DOCUMENTO)` · N:1 · logical-probable/probable — Quando OBJECT_TYPE=DOCUMENT; nome da tabela alvo não confirmado.
- `(NUM_PROCESS_INSTANCE)` → **PROCES_WORKFLOW** `(NUM_PROCES)` · N:1 · logical-probable/probable — Quando OBJECT_TYPE=PROCESS_INSTANCE.

**Dicas de consulta:** Filtrar por TENANT_ID e LOGIN; ordenar por DAT_ACCESS desc.
