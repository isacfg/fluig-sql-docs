# Domínio: seguranca-api

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_API_BLOCKER

Padrões de URL/API bloqueados pelo filtro bloqueador de APIs do Fluig, com exceções. Cada linha é um padrão de bloqueio.

**Ciclo de vida:** Configuração; poucas linhas, alterada raramente por administração.

**Atenção:** Sem coluna de tenant: configuração global do servidor.

**PK:** API_BLOCKER_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `API_BLOCKER_ID` | bigint(20) | N | Chave primária do padrão de bloqueio. |  |  |
| `PATTERN` | varchar(500) | S | Padrão (expressão/caminho) de requisições a bloquear; campo Java blockPattern. |  |  |
| `EXCEPTIONS` | varchar(600) | S | Lista de exceções ao padrão (caminhos permitidos), em texto livre. |  |  |

**Dicas de consulta:** Tabela pequena e global; ler inteira (FDNAPIBlockerPattern.findAll).
