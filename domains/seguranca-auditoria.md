# Domínio: seguranca-auditoria

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_ACCESSLOG

Log de acessos (login/logout) à plataforma Fluig por usuário, com IP do cliente, IP do servidor e agente. Recebe uma linha por evento de acesso.

**Ciclo de vida:** Insert-only a cada autenticação; cresce continuamente (alto volume), sujeito a expurgo por rotina de manutenção.

**Atenção:** Sem FK: LOGIN guarda o login textual, não o ID do usuário. LOG_TYPE=0 é contado como acesso (login) nas consultas de usuários ativos no período. Índice IDX_FDNCCESSLOG001 (TENANT_ID, LOG_TYPE, ACCESS_DATE).

**PK:** ACCESSLOG_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ACCESSLOG_ID` | bigint | N | Chave primária do registro de acesso. |  |  |
| `ACCESS_DATE` | datetime | N | Data e hora do evento de acesso. |  |  |
| `CLIENT_ADDRESS` | varchar(50) | N | Endereço IP do cliente que acessou (dado pessoal). |  |  |
| `LOG_TYPE` | integer | N | Tipo do evento de acesso; 0 é usado como "acesso/login" nas contagens de usuários do período. | 0=acesso (login) contado nos relatórios; demais valores não confirmados |  |
| `LOGIN` | varchar(150) | N | Login (código textual) do usuário que acessou. |  | FDN_USERTENANT.USER_CODE |
| `SERVER_ADDRESS` | varchar(50) | N | Endereço IP do servidor Fluig que atendeu o acesso. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) do acesso. |  | FDN_TENANT.TENANT_ID |
| `CATEGORY` | varchar(20) | S | Categoria/agente do cliente (navegador ou app); mapeado ao campo Java "agent". |  |  |
| `OS` | varchar(20) | S | Sistema operacional do cliente (máx. 20 caracteres). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant do acesso, sem FK física.

**Dicas de consulta:** Contém IPs e login (dados pessoais). Filtrar sempre por TENANT_ID e intervalo de ACCESS_DATE para usar o índice.
