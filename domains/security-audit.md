# Domínio: security-audit

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## LOG_ACESSO

Log de acessos (login/logout/timeout/erro) de usuários, com IPs de cliente e servidor (LogAccess).

**Ciclo de vida:** Uma linha por evento de acesso; cresce continuamente.

**PK:** COD_EMPRESA, CD_MATRICULA, DAT_CLIEN_SERVID, DES_CLIEN_IP

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(255) | N | Matrícula do usuário que acessou. |  | FDN_USER.COLLEAGUE_ID |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `DAT_CLIEN_SERVID` | datetime | N | Data/hora do evento de acesso. |  |  |
| 🔑 `DES_CLIEN_IP` | varchar(255) | N | Endereço IP do cliente. |  |  |
| `IDI_TIP_ACESSO` | integer | S | Tipo do acesso (LogAccessTypes). | 0=login;1=logout;2=timeout;3=login com usuário não encontrado;4=erro de login |  |
| `DES_SERVID_IP` | varchar(255) | S | Endereço IP do servidor que atendeu. |  |  |

**Dicas de consulta:** Dado pessoal: IPs e matrículas. Último logout/timeout: ORDER BY DAT_CLIEN_SERVID DESC.
