# Domínio: ecm-forms

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FICHA

Valores dos campos das fichas (registros de formulário/fichário): uma linha por campo de cada ficha, versão e tabela do formulário.

**Ciclo de vida:** Linhas criadas ao salvar uma ficha (documento TP_DOCUMENTO=5) e atualizadas/removidas conforme a ficha muda. Volume muito alto (campos x fichas).

**Atenção:** PK (COD_EMPRESA, NR_FICHA, NR_VERSAO, COD_TABELA, COD_CAMPO). NR_FICHA corresponde a NR_DOCUMENTO da ficha em DOCUMENTO. Estrutura EAV; COD_TABELA distingue tabela pai/filha (pai-e-filho).

**PK:** COD_EMPRESA, NR_FICHA, NR_VERSAO, COD_TABELA, COD_CAMPO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NR_FICHA` | integer | N | Número da ficha = NR_DOCUMENTO do documento ficha. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_CAMPO` | varchar(70) | N | Identificador do campo do formulário (nome do input). |  | FICHARIO_CAMPO.COD_CAMPO |
| 🔑 `COD_TABELA` | varchar(50) | N | Tabela do formulário (principal ou filha pai-e-filho) à qual o campo pertence. |  | FICHARIO.COD_TABELA |
| 🔑 `NR_VERSAO` | integer | N | Versão da ficha. |  | DOCUMENTO.NR_VERSAO |
| `NR_FICHARIO` | integer | S | Número do fichário (formulário) ao qual a ficha pertence. |  | FICHARIO.NR_FICHARIO |
| `COD_VALOR` | longtext | S | Valor gravado no campo (texto longo). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_FICHA, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Ficha é um documento tipo 5.
- `(COD_EMPRESA, COD_CAMPO, NR_FICHARIO, COD_TABELA)` → **FICHARIO_CAMPO** `(COD_EMPRESA, COD_CAMPO, NR_FICHARIO, COD_TABELA)` · N:1 · logical-probable/probable — Definição do campo; a versão da ficha (NR_VERSAO) não é necessariamente a versão do fichário, por isso a heurística de PK completa é parcial.

**Dicas de consulta:** COD_VALOR é longtext: pode conter dados pessoais digitados em formulários. Para dados de formulário de processo prefira também as tabelas ML{N}* dinâmicas.

## FICHARIO

Definição das tabelas de um fichário (formulário): cada fichário tem uma tabela principal e, opcionalmente, tabelas filhas (pai-e-filho).

**Ciclo de vida:** Criada ao publicar/atualizar um formulário; uma linha por tabela por versão.

**Atenção:** PK (COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA). NR_FICHARIO = NR_DOCUMENTO do fichário (TP_DOCUMENTO=4).

**PK:** COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `NR_FICHARIO` | integer | N | Número do fichário (formulário), igual a NR_DOCUMENTO do documento fichário. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `COD_TABELA` | varchar(50) | N | Identificador da tabela do formulário (principal ou filha). |  |  |
| 🔑 `NR_VERSAO` | integer | N | Versão do fichário. |  | DOCUMENTO.NR_VERSAO |
| `COD_TABELA_PAI` | varchar(50) | S | COD_TABELA da tabela pai quando esta é filha (pai-e-filho); NULL para a principal. |  | FICHARIO.COD_TABELA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_FICHARIO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento fichário (tipo 4).
- `(COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA)` → **FICHARIO_CAMPO** `(COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA)` · 1:N · logical-probable/probable — Campos da tabela do fichário.

**Dicas de consulta:** Juntar com FICHARIO_CAMPO por (COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA).

## FICHARIO_CAMPO

Definição dos campos de cada tabela de um fichário (formulário): nome e tipo do campo.

**Ciclo de vida:** Criada na publicação do formulário; uma linha por campo por versão.

**Atenção:** PK (COD_EMPRESA, COD_CAMPO, NR_FICHARIO, COD_TABELA, NR_VERSAO).

**PK:** COD_EMPRESA, COD_CAMPO, NR_FICHARIO, COD_TABELA, NR_VERSAO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_CAMPO` | varchar(70) | N | Identificador/nome do campo do formulário. |  |  |
| 🔑 `NR_FICHARIO` | integer | N | Número do fichário (formulário). |  | FICHARIO.NR_FICHARIO |
| 🔑 `COD_TABELA` | varchar(50) | N | Tabela do formulário à qual o campo pertence. |  | FICHARIO.COD_TABELA |
| 🔑 `NR_VERSAO` | integer | N | Versão do fichário. |  | FICHARIO.NR_VERSAO |
| `TIPO_CAMPO` | varchar(50) | S | Tipo de dado/componente do campo (texto, número etc.); valores não confirmados. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA)` → **FICHARIO** `(COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA)` · N:1 · logical-confirmed/confirmed — Tabela do fichário a que o campo pertence (chave coincide integralmente).

**Dicas de consulta:** Descritor dos valores guardados em FICHA.
