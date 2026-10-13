# Domínio: document-management

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## LOCK_RESOURCE

Trava (lock) de recurso por usuário/sessão para edição exclusiva (LockResource).

**Ciclo de vida:** Criada ao bloquear um recurso; removida ao liberar.

**Atenção:** Linhas órfãs podem ficar se a sessão cair.

**PK:** COD_EMPRESA, TOKEN_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `TOKEN_ID` | varchar(255) | N | Token único da trava. |  |  |
| `CD_MATRICULA` | varchar(255) | S | Matrícula do usuário que detém a trava. |  | FDN_USER.COLLEAGUE_ID |
| `ID_RESOURCE` | varchar(255) | N | Identificador do recurso travado (ex.: documento). |  |  |
| `DATA_LOCK` | date | S | Data da trava. |  |  |
| `HRA_LOCK` | varchar(255) | S | Hora da trava (texto). |  |  |
| `DES_ID_SESSAO` | varchar(2000) | S | Descrição/id da sessão que travou. |  |  |

**Dicas de consulta:** Contém ids de sessão (sensível).
