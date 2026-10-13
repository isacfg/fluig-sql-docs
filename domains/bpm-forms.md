# Domínio: bpm-forms

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FICHARIO_CAMPO_PROCES

Mapeia campos do formulário a um processo: descrição e posição (slot) de campos exibidos/indexados para a definição de processo.

**Ciclo de vida:** Gravada ao configurar o formulário associado a um processo; poucas linhas por processo.

**Atenção:** PK (COD_EMPRESA, COD_CAMPO, COD_DEF_PROCES).

**PK:** COD_EMPRESA, COD_CAMPO, COD_DEF_PROCES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_CAMPO` | varchar(50) | N | Nome do campo do formulário mapeado. |  | FICHARIO_CAMPO.COD_CAMPO |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo à qual o campo é associado. |  | DEF_PROCES.COD_DEF_PROCES |
| `DS_CAMPO` | varchar(200) | S | Descrição/rótulo do campo no processo. |  |  |
| `NUM_SEQ` | integer | S | Posição (slot) numérica do campo na lista do processo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-confirmed/probable — Definição do processo.

**Dicas de consulta:** Filtrar por COD_EMPRESA e COD_DEF_PROCES.

## TEMA_FORMULARIO

Temas visuais (arquivos de tema) aplicáveis a formulários.

**Ciclo de vida:** Cadastrada pelo administrador; baixo volume.

**Atenção:** PK (COD_EMPRESA, NUM_TEMA_FORM). Apenas um tema deve estar como padrão (FormTheme.findStandard).

**PK:** COD_EMPRESA, NUM_TEMA_FORM

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `NUM_TEMA_FORM` | integer | N | Identificador do tema de formulário. |  |  |
| `ATIVO` | bit | S | Indica se o tema está ativo. | 1=ativo |  |
| `NOM_ARQUIVO_TEMA` | varchar(255) | S | Nome do arquivo do tema (CSS/pacote). |  |  |
| `NOM_TEMA_FORM` | varchar(255) | S | Nome exibido do tema. |  |  |
| `TEMA_PADRAO` | bit | S | Indica o tema padrão. | 1=tema padrão |  |

**Dicas de consulta:** Consulta do padrão: TEMA_PADRAO=1.
