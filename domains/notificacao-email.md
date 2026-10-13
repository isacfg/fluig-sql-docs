# Domínio: notificacao-email

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## TEMPLATE_EMAIL

Cadastro de templates de e-mail do Fluig por empresa e idioma (dialeto), apontando o arquivo físico do template; inclui padrão e customizados.

**Ciclo de vida:** Carregada com os templates padrão e acrescida quando o admin cria templates customizados. Volume baixo.

**Atenção:** PK inclui COD_DIALETO: um mesmo template tem uma linha por idioma. Entidade EmailTemplate.

**PK:** COD_EMPRESA, COD_TEMPLATE_EMAIL, COD_DIALETO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DIALETO` | varchar(10) | N | Idioma/dialeto do template (ex.: pt_BR, en_US). |  |  |
| 🔑 `COD_TEMPLATE_EMAIL` | varchar(50) | N | Identificador do template de e-mail. |  |  |
| `LOG_TEMPLATE_PADR` | bit | S | Indica se é template padrão do produto (não customizado). | 1=padrão; 0=customizado |  |
| `NOM_ARQ_FISIC` | varchar(510) | S | Nome do arquivo físico (ex.: .html/.ftl) que contém o corpo do template. |  |  |
| `NM_ARQUIVOS_RELACIONADOS` | varchar(1020) | S | Lista de arquivos relacionados (anexos/imagens) ao template. |  |  |
| `DES_TEMPLATE_EMAIL` | varchar(510) | S | Descrição do template de e-mail. |  |  |

**Dicas de consulta:** Named queries: findByDialectId, findDefaultTemplate, findAllCustom, findByFileName, findByTemplateId.
