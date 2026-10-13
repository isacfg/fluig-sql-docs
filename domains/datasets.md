# Domínio: datasets

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_DATASETHISTORY

Histórico de versões de datasets customizados (implementação JavaScript). Cada linha é uma versão de um dataset.

**Ciclo de vida:** Nova linha a cada salvamento/publicação de dataset; versões antigas permanecem. Volume moderado.

**Atenção:** Unicidade (TENANT_ID, DATASET_ID, VERSION). VERSION_STATUS é enum ordinal. DATASET_IMPL é LOB (longtext) com o código.

**PK:** DATASET_HISTORY_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DATASET_HISTORY_ID` | bigint | N | Chave primária da versão do dataset. |  |  |
| `DATASET_DESCRIPTION` | varchar(100) | S | Descrição do dataset. |  |  |
| `DATASET_ID` | varchar(100) | N | Identificador (nome) do dataset, ex. usado em consultas de dataset. |  |  |
| `DATASET_IMPL` | longtext | S | Código-fonte (JavaScript) da implementação do dataset; LOB longtext. |  |  |
| `TYPE` | varchar(20) | S | Tipo do dataset (ex.: customizado/builtin); texto de até 20 caracteres. |  |  |
| `BUILDER` | varchar(200) | S | Nome do builder/classe construtora do dataset, quando não é implementação JS. |  |  |
| `VERSION` | bigint | N | Número sequencial da versão do dataset dentro do tenant. |  |  |
| `VERSION_STATUS` | integer | N | Status da versão (enum DatasetHistoryStatus, ordinal). | 0=DRAFT; 1=PUBLISHED; 2=INACTIVE (ordinal do enum; assumindo EnumType.ORDINAL) |  |
| `TENANT_ID` | bigint | N | Tenant dono do dataset. |  | FDN_TENANT.TENANT_ID |
| `UPDATE_TIME` | datetime | N | Data/hora da gravação desta versão. |  |  |
| `USER_TENANT_ID` | bigint | S | Usuário (FDN_USERTENANT) que gravou a versão. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant (FK_DATASETHISTORYTENANT).
- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Autor da versão (FK_DATASETHISTORYUSERTENANT).

**Dicas de consulta:** Para o dataset vigente, filtrar VERSION_STATUS pelo publicado e maior VERSION. Não selecionar DATASET_IMPL em listagens.
