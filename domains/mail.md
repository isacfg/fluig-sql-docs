# Domínio: mail

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## MAILEVENTTEMPLATE

Mapeia eventos de e-mail do Fluig a templates por tenant, dialeto (idioma) e nome de template, com assunto.

**Ciclo de vida:** Configuração; volume baixo.

**Atenção:** Unique UK_MAILEVTTPL001 em (tenantId, eventKey, dialect, templateName). Colunas sem coluna Java mapeada no extrator (nomes TENANTID, EVENTKEY sem underscore).

**PK:** id · **Unique:** (tenantId, eventKey, dialect, templateName)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | PK surrogate. |  |  |
| `DIALECT` | varchar(255) | N | Dialeto/idioma do template (ex.: pt_BR). |  |  |
| `EVENTKEY` | varchar(255) | N | Chave do evento de e-mail que dispara o template. |  |  |
| `SUBJECT` | varchar(255) | N | Assunto do e-mail para este evento. |  |  |
| `TEMPLATENAME` | varchar(255) | N | Nome do arquivo/template de e-mail utilizado. |  |  |
| `TENANTID` | bigint | N | Tenant dono da configuração. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANTID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant da configuração; sem FK física.

**Dicas de consulta:** Filtrar por TENANTID + EVENTKEY + DIALECT.
