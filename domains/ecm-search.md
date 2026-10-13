# Domínio: ecm-search

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## SINONIMO

Sinônimos de termos do dicionário de busca, por idioma.

**Ciclo de vida:** Mantida pelo administrador de busca/dicionário; baixo volume.

**Atenção:** PK (COD_EMPRESA, IND_IDIOMA, COD_TERMO, COD_TERMO_SINONIMO).

**PK:** COD_EMPRESA, IND_IDIOMA, COD_TERMO, COD_TERMO_SINONIMO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `IND_IDIOMA` | varchar(12) | N | Código do idioma do termo (ex.: pt). |  | TERMO.IND_IDIOMA |
| 🔑 `COD_TERMO` | varchar(100) | N | Termo principal. |  | TERMO.COD_TERMO |
| 🔑 `COD_TERMO_SINONIMO` | varchar(100) | N | Termo sinônimo do termo principal. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, IND_IDIOMA, COD_TERMO)` → **TERMO** `(COD_EMPRESA, IND_IDIOMA, COD_TERMO)` · N:1 · logical-confirmed/confirmed — Termo ao qual o sinônimo pertence.

**Dicas de consulta:** Sem dados sensíveis.

## TAG

Cadastro de tags (etiquetas) usadas para classificar conteúdo.

**Ciclo de vida:** Uma linha por tag distinta; criada ao primeiro uso.

**Atenção:** PK (COD_EMPRESA, COD_TAG). Associações com documentos/conteúdos ficam em outras tabelas.

**PK:** COD_EMPRESA, COD_TAG

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_TAG` | varchar(100) | N | Texto da tag (identificador). |  |  |

**Dicas de consulta:** Tabela mínima; ligações a conteúdo em tabelas de associação.

## TERMO

Dicionário de termos de busca por idioma, com marcação de termos irrelevantes (stop words).

**Ciclo de vida:** Mantida pela indexação/administração; volume baixo a médio.

**Atenção:** PK (COD_EMPRESA, IND_IDIOMA, COD_TERMO).

**PK:** COD_EMPRESA, IND_IDIOMA, COD_TERMO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `IND_IDIOMA` | varchar(2) | N | Código do idioma de 2 letras do termo. |  |  |
| 🔑 `COD_TERMO` | varchar(100) | N | Texto do termo. |  |  |
| `LOG_IRRELEV` | bit | S | Termo irrelevante (ignorado na busca). | 1=irrelevante |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, IND_IDIOMA, COD_TERMO)` → **SINONIMO** `(COD_EMPRESA, IND_IDIOMA, COD_TERMO)` · 1:N · logical-confirmed/confirmed — Sinônimos do termo.

**Dicas de consulta:** Nota: IND_IDIOMA é varchar(2) aqui e varchar(12) em SINONIMO.
