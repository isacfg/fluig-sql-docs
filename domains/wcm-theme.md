# Domínio: wcm-theme

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_THEME_HISTORY

Histórico de trocas de tema do portal por tenant (tema anterior e novo) com flags sobre tema responsivo.

**Ciclo de vida:** Linha inserida a cada troca de tema; só cresce.

**Atenção:** TENANT_CODE e TENANT_DESCRIPTION são cópias desnormalizadas do tenant no momento da troca.

**PK:** THEME_HISTORY_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `THEME_HISTORY_ID` | bigint | N | PK surrogate do registro. |  |  |
| `OLD_THEME` | varchar(40) | N | Código do tema anterior. |  |  |
| `NEW_THEME` | varchar(40) | N | Código do novo tema. |  |  |
| `CHANGE_DATE` | datetime | N | Data/hora da troca de tema. |  |  |
| `TENANT_ID` | bigint | N | Tenant que trocou o tema. |  | FDN_TENANT.TENANT_ID |
| `TENANT_CODE` | varchar(40) | N | Código do tenant (cópia desnormalizada). |  |  |
| `TENANT_DESCRIPTION` | varchar(255) | N | Descrição do tenant (cópia desnormalizada). |  |  |
| `REFUSED_RESPONSIVE` | bit | N | Indica que o tenant recusou migrar para tema responsivo. | 1=recusou; 0=não |  |
| `ALREADY_USED_RESPONSIVE_THEME` | bit | N | Indica que o tenant já usou tema responsivo antes. | 1=já usou; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant que trocou o tema.

**Dicas de consulta:** Filtrar por TENANT_ID; ordenar por CHANGE_DATE.
