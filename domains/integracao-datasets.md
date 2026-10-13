# Domínio: integracao-datasets

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## SERV_DATASET

Cadastro de datasets (fontes de dados consultáveis por formulários/scripts), com implementação JS, builder e configuração de cache/offline.

**Ciclo de vida:** Criado/alterado no editor de datasets; datasets nativos são carregados na inicialização. Volume baixo a médio.

**Atenção:** Entidade Dataset; PK (COD_EMPRESA, COD_DATASET). Datasets customizados têm código-fonte em DSL_DATASET.

**PK:** COD_EMPRESA, COD_DATASET

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DATASET` | varchar(100) | N | Nome/código do dataset, usado nas consultas (datasetId). |  |  |
| `DSL_BUILDER` | varchar(200) | S | Classe/builder Java que implementa o dataset (datasets nativos). |  |  |
| `DES_DATASET` | varchar(100) | S | Descrição do dataset. |  |  |
| `DSL_DATASET` | longtext | S | Código-fonte JavaScript do dataset customizado. |  |  |
| `IS_ACTIVE` | bit | N | Indica se o dataset está ativo e consultável. | 1=ativo; 0=inativo |  |
| `IS_DRAFT` | bit | N | Indica se o dataset é rascunho (não publicado). | 1=rascunho; 0=publicado |  |
| `JOURN_ADHERENCE` | integer | S | Nível de aderência ao journaling (rastreio de alterações) do dataset. |  |  |
| `LAST_REMOTE_SYNC` | bigint | S | Timestamp (epoch ms) da última sincronização remota. |  |  |
| `LAST_RESET` | bigint | S | Timestamp (epoch ms) do último reset do cache do dataset. |  |  |
| `COD_LISTA` | integer | S | Código da lista de metadados (metalist) associada ao armazenamento do dataset. |  | META_LISTA.COD_LISTA |
| `MOBILE_OFFLINE` | bit | S | Indica se o dataset é disponibilizado em cache offline para mobile. | 1=sim; 0=não |  |
| `FORCE_MOBILE_OFFLINE` | bit | S | Força cache offline mobile mesmo sem solicitação do dataset. | 1=sim; 0=não |  |
| `RESET_TYPE` | integer | S | Tipo de política de reset do cache do dataset. |  |  |
| `SERVER_OFFLINE` | bit | S | Indica se o dataset é mantido em cache no servidor (offline). | 1=sim; 0=não |  |
| `SYNC_DETAILS` | longtext | S | Detalhes (texto longo) da última sincronização ou do erro de sincronização. |  |  |
| `SYNC_STATUS` | integer | S | Status da última sincronização do dataset. |  |  |
| `TYPE` | varchar(255) | S | Tipo do dataset (ex.: builder, customizado, avançado). |  |  |
| `UPDATE_INTERVAL` | bigint | S | Intervalo, em milissegundos, para atualização do cache offline. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Lista de metadados que guarda os dados em cache do dataset.

**Dicas de consulta:** Consultar sempre por COD_EMPRESA. DSL_DATASET e SYNC_DETAILS são longtext.
