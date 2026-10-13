# Domínio: rating

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## RATING

Avaliação (nota) que um usuário deu a um app mobile do Fluig (MY_FLUIG ou MY_APPROVAL), uma linha por usuário e app.

**Ciclo de vida:** Criada na primeira avaliação e atualizada (LAST_RATING_DATE, RATING_NOTE) nas seguintes; volume baixo.

**Atenção:** Multi-tenant por TENANT_ID. Único por (USER_CODE, APP_IDENTIFIER).

**PK:** ID · **Unique:** (USER_CODE, APP_IDENTIFIER)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador surrogate da avaliação do app (PK). |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa Fluig) do usuário que avaliou. |  | FDN_TENANT.TENANT_ID |
| `USER_CODE` | varchar(150) | N | Código (login) do usuário que avaliou o app; único junto com APP_IDENTIFIER. |  | FDN_USERTENANT.USER_CODE |
| `FIRST_RATING_DATE` | datetime | N | Data/hora da primeira avaliação do usuário para o app. |  |  |
| `LAST_RATING_DATE` | datetime | N | Data/hora da avaliação mais recente do usuário para o app. |  |  |
| `RATING_NOTE` | tinyint | N | Nota atribuída pelo usuário (inteiro pequeno, tipicamente estrelas); escala exata não confirmada no código. |  |  |
| `RATED_BY_STORE` | bit | N | Indica se a avaliação foi feita via loja de apps (true) ou dentro do próprio app (false). | true=avaliado pela loja; false=avaliado no app (default) |  |
| `APP_IDENTIFIER` | varchar(30) | N | Aplicativo mobile avaliado; enum AppIdentifier gravado como STRING (nome da constante Java). | MY_FLUIG=app Fluig mobile (appName MYFLUIG); MY_APPROVAL=app de aprovações mobile (appName MYAPPROVAL) |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant do avaliador.

**Dicas de consulta:** Filtrar por TENANT_ID. USER_CODE é dado pessoal indireto.
