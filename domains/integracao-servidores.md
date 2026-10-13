# Domínio: integracao-servidores

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_FLUIG_SERVER

Servidores Fluig cadastrados (outras instâncias Fluig conectadas), cada um com credenciais OAuth em FDN_AUTHORIZECLIENTDATA.

**Ciclo de vida:** Cadastro administrativo; poucas linhas.

**Atenção:** Credenciais ficam na tabela referenciada, não aqui.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | BIGINT(20) | N | Chave primária do servidor Fluig cadastrado. |  |  |
| `NAME` | VARCHAR(255) | N | Nome do servidor Fluig. |  |  |
| `AUTHORIZECLIENTDATA_ID` | BIGINT(20) | N | Dados de cliente OAuth usados para autenticar neste servidor. |  | FDN_AUTHORIZECLIENTDATA.AUTHORIZECLIENTDATA_ID |

**Relacionamentos (saem desta tabela):**

- `(AUTHORIZECLIENTDATA_ID)` → **FDN_AUTHORIZECLIENTDATA** `(AUTHORIZECLIENTDATA_ID)` · N:1 · jpa-join/confirmed — Credenciais OAuth do servidor (também FK física).

**Dicas de consulta:** Dados sensíveis (consumer key/secret) em FDN_AUTHORIZECLIENTDATA.
