# Domínio: ecm-lists-filters

14 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FAVORITOS

Documentos marcados como favoritos por usuário.

**Ciclo de vida:** Linha criada ao favoritar, removida ao desfavoritar.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, CD_MATRICULA, NR_DOCUMENTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que favoritou o documento. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Número do documento favoritado. |  | DOCUMENTO.NR_DOCUMENTO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento favoritado (qualquer versão).

**Dicas de consulta:** Contém referência a usuário (matrícula/id); dado pessoal indireto.

## FAVORITOS_PROCES

Processos (definições) marcados como favoritos por usuário.

**Ciclo de vida:** Linha criada/removida ao favoritar.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, CD_MATRICULA, COD_DEF_PROCES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que favoritou o processo. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DEF_PROCES` | varchar(255) | N | Código da definição de processo favoritada. |  | DEF_PROCES.COD_DEF_PROCES |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA)` → **VERS_DEF_PROCES** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — Join usado em ProcessDefinitionVersion.searchFavoritesProcess.
- `(COD_DEF_PROCES)` → **VERS_DEF_PROCES** `(COD_DEF_PROCES)` · N:1 · hql-join/confirmed — Join usado em ProcessDefinitionVersion.searchFavoritesProcess.
- `(COD_EMPRESA, COD_DEF_PROCES)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.

**Dicas de consulta:** Contém referência a usuário (matrícula/id); dado pessoal indireto.

## FILTERS

Filtros salvos pelos usuários nas listas de documentos ou de processos (tarefas), com tipo DOCUMENT ou PROCESS.

**Ciclo de vida:** Criado pelo usuário; POSITION reordenada por queries.

**Atenção:** Multi-tenant por TENANT_ID.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador do filtro salvo. |  |  |
| `IS_PUBLIC` | bit | S | Indica se o filtro é público (visível a outros usuários). | 1=público; 0/null=privado (inferido) |  |
| `NAME` | varchar(255) | N | Nome do filtro. |  |  |
| `POSITION` | integer | N | Posição do filtro na lista do usuário/tenant/tipo (Filter.nextPosition, updatePositions). |  |  |
| `TENANT_ID` | bigint | N | Tenant do filtro. |  | FDN_TENANT.TENANT_ID |
| `TYPE` | integer | N | Tipo do filtro (enum FilterType, ordinal). | 0=DOCUMENT; 1=PROCESS |  |
| `USER_ID` | bigint | N | Usuário dono do filtro (id numérico). |  | FDN_USER.USER_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_ID)` → **FDN_USER** `(USER_ID)` · N:1 · logical-probable/probable — Dono do filtro.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant do filtro.

**Dicas de consulta:** Contém referência a usuário (matrícula/id); dado pessoal indireto.  Filtrar por FILTERS.TENANT_ID e USER_ID; TYPE 0=DOCUMENT, 1=PROCESS.

## FILTER_FIELDS

Campos/critérios e opções de exibição (cor, fonte, largura, visibilidade) de um filtro salvo.

**Ciclo de vida:** Removidos em bloco ao editar/excluir o filtro (removeAllFieldsFromFilter).

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador do campo do filtro. |  |  |
| `FKEY` | varchar(255) | N | Chave do campo do filtro (nome do campo/atributo filtrado); coluna FKEY pois KEY é reservada. |  |  |
| `PROCESS_ID` | varchar(255) | S | Código da definição de processo associada ao campo do filtro (cópia de VALUE no construtor). |  | DEF_PROCES.COD_DEF_PROCES |
| `SLOT_ID` | integer | S | Slot/posição do campo na visão do filtro de processo. |  |  |
| `TYPE` | varchar(255) | S | Tipo do campo do filtro (texto livre definido pela aplicação). |  |  |
| `VALUE` | varchar(255) | S | Valor do critério do filtro para a chave FKEY. |  |  |
| `VISIBLE` | bit | S | Indica se o campo é exibido como coluna na lista. |  |  |
| `FILTER_ID` | bigint | S | Filtro ao qual o campo pertence. |  | FILTERS.ID |
| `COLOR_FIELD` | varchar(255) | S | Cor aplicada ao campo na exibição. |  |  |
| `FONT_STYLE` | varchar(255) | S | Estilo da fonte do campo (ex.: itálico). |  |  |
| `ORDER_POSITION` | integer | S | Posição de ordenação da coluna. |  |  |
| `SIZE_FIELD` | integer | S | Tamanho/largura da coluna do campo. |  |  |
| `SENSITIVE_DATA` | bit | S | Marca o campo como dado sensível. |  |  |
| `FONT_WEIGHT` | varchar(255) | S | Peso da fonte (ex.: bold). |  |  |
| `TEXT_DECORATION` | varchar(255) | S | Decoração do texto (ex.: underline). |  |  |
| `LABEL` | varchar(255) | S | Rótulo exibido do campo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(FILTER_ID)` → **FILTERS** `(ID)` · N:1 · physical-fk/confirmed — FK ['FILTER_ID'] referencia FILTERS.

## FILTER_GROUP

Compartilhamento de um filtro com grupo, papel ou usuário, com permissão.

**Ciclo de vida:** Uma linha por destinatário; apenas um de GROUP_ID/ROLE_ID/USER_TENANT_ID deve estar preenchido (inferido).

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador da concessão de acesso ao filtro. |  |  |
| `FILTER_ID` | bigint | S | Filtro compartilhado. |  | FILTERS.ID |
| `GROUP_ID` | bigint | S | Grupo que recebe acesso (alternativa a usuário/papel). |  | FDN_GROUP.GROUP_ID |
| `ROLE_ID` | bigint | S | Papel que recebe acesso. |  | FDN_ROLE.ROLE_ID |
| `USER_TENANT_ID` | bigint | S | Usuário (vínculo usuário-tenant) que recebe acesso. |  | FDN_USERTENANT.USER_TENANT_ID |
| `PERMISSION` | bigint | S | Nível de permissão concedido ao filtro (inteiro; significado não encontrado). |  |  |

**Relacionamentos (saem desta tabela):**

- `(FILTER_ID)` → **FILTERS** `(ID)` · N:1 · physical-fk/confirmed — FK ['FILTER_ID'] referencia FILTERS.
- `(GROUP_ID)` → **FDN_GROUP** `(GROUP_ID)` · N:1 · physical-fk/confirmed — FK ['GROUP_ID'] referencia FDN_GROUP.
- `(ROLE_ID)` → **FDN_ROLE** `(ROLE_ID)` · N:1 · physical-fk/confirmed — FK ['ROLE_ID'] referencia FDN_ROLE.
- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — FK ['USER_TENANT_ID'] referencia FDN_USERTENANT.

**Dicas de consulta:** Contém referência a usuário (matrícula/id); dado pessoal indireto.

## FILTER_ORDER

Critérios de ordenação de um filtro salvo, apontando para um FILTER_FIELDS.

**Ciclo de vida:** Removidos junto com o filtro (removeOrderFromFilter).

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador do critério de ordenação. |  |  |
| `TYPE` | varchar(255) | S | Direção/tipo da ordenação (string livre; ex. ASC/DESC provável). |  |  |
| `FILTER_ID` | bigint | S | Filtro ao qual a ordenação pertence. |  | FILTERS.ID |
| `FIELD_ID` | bigint | S | Campo do filtro usado como chave de ordenação. |  | FILTER_FIELDS.ID |

**Relacionamentos (saem desta tabela):**

- `(FILTER_ID)` → **FILTERS** `(ID)` · N:1 · physical-fk/confirmed — FK ['FILTER_ID'] referencia FILTERS.
- `(FIELD_ID)` → **FILTER_FIELDS** `(ID)` · N:1 · physical-fk/confirmed — FK ['FIELD_ID'] referencia FILTER_FIELDS.

## META_LISTA

Cabeçalho de meta-lista: lista dinâmica de dados definida pelo usuário (tabelas customizadas de metadados do ECM).

**Ciclo de vida:** Exclusão lógica por LOG_DELETE.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_LISTA` | integer | N | Código da meta-lista (lista dinâmica/dataset de metadados) dentro da empresa. |  |  |
| `LOG_DELETE` | bit | S | Exclusão lógica da lista. | 1=excluída; 0/null=ativa |  |
| `DSL_LISTA` | varchar(255) | S | Descrição da lista. |  |  |
| `NOM_LISTA` | varchar(50) | S | Nome da lista. |  |  |
| `TP_LISTA` | integer | S | Tipo da lista; queries findAll filtram TP_LISTA=0 ou nulo como listas comuns. | 0/null=lista comum; outros valores não confirmados |  |

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LISTA_CAMPO

Campos (colunas) de uma meta-lista, com título, tipo, obrigatoriedade e lista estrangeira.

**Ciclo de vida:** Exclusão lógica por LOG_DELETE.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA, NUM_SEQ_CAMPO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_CAMPO` | integer | N | Sequencial do campo dentro da meta-lista. |  |  |
| 🔑 `COD_LISTA` | integer | N | Meta-lista dona do campo. |  | META_LISTA.COD_LISTA |
| `LOG_DELETE` | bit | N | Exclusão lógica do campo. | 1=excluído; 0=ativo |  |
| `NOM_CAMPO` | varchar(70) | S | Nome técnico do campo. |  |  |
| `COD_LISTA_ESTRAN` | integer | S | Meta-lista estrangeira referenciada quando o campo é chave estrangeira para outra lista. |  | META_LISTA.COD_LISTA |
| `LOG_ROTULO` | bit | N | Indica se o campo é o rótulo (label) exibido do registro. |  |  |
| `LOG_REQUER` | bit | N | Indica se o campo é obrigatório. |  |  |
| `NOM_TITULO` | varchar(50) | S | Título exibido do campo. |  |  |
| `TP_CAMPO` | integer | S | Tipo de dado do campo (código inteiro; mapeamento não confirmado). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.
- `(COD_EMPRESA, COD_LISTA_ESTRAN)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Lista estrangeira referenciada pelo campo.

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LISTA_PERSPECT

Perspectivas (visões salvas) de uma meta-lista.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA, COD_PERSPECT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_LISTA` | integer | N | Meta-lista da perspectiva. |  | META_LISTA.COD_LISTA |
| 🔑 `COD_PERSPECT` | integer | N | Código da perspectiva (visão salva) dentro da lista. |  |  |
| `DES_PERSPECT` | varchar(255) | S | Descrição da perspectiva. |  |  |
| `NOM_PERSPECT` | varchar(50) | S | Nome da perspectiva. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LISTA_PERSPECT_CAMPO

Campos incluídos em uma perspectiva da meta-lista, com ordem e indicação de agrupador.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA, COD_PERSPECT, NUM_SEQ_CAMPO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_CAMPO` | integer | N | Sequencial do campo da meta-lista incluído na perspectiva. |  | META_LISTA_CAMPO.NUM_SEQ_CAMPO |
| 🔑 `COD_LISTA` | integer | N | Meta-lista. |  | META_LISTA.COD_LISTA |
| 🔑 `COD_PERSPECT` | integer | N | Perspectiva. |  | META_LISTA_PERSPECT.COD_PERSPECT |
| `NOM_CAMPO` | varchar(70) | S | Nome do campo na perspectiva. |  |  |
| `LOG_AGRUPADOR` | bit | S | Indica se o campo é usado como agrupador na perspectiva. |  |  |
| `NUM_ORDEM` | integer | S | Ordem do campo na perspectiva. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA, NUM_SEQ_CAMPO)` → **META_LISTA_CAMPO** `(COD_EMPRESA, COD_LISTA, NUM_SEQ_CAMPO)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.
- `(COD_EMPRESA, COD_LISTA, COD_PERSPECT)` → **META_LISTA_PERSPECT** `(COD_EMPRESA, COD_LISTA, COD_PERSPECT)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LISTA_PERSPECT_FILTRO

Filtros (campo, condição, valor) aplicados a uma perspectiva de meta-lista.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA, COD_PERSPECT, COD_FILTRO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_FILTRO` | integer | N | Sequencial do filtro dentro da perspectiva. |  |  |
| 🔑 `COD_LISTA` | integer | N | Meta-lista. |  | META_LISTA.COD_LISTA |
| 🔑 `COD_PERSPECT` | integer | N | Perspectiva. |  | META_LISTA_PERSPECT.COD_PERSPECT |
| `COD_CONDICAO` | varchar(255) | S | Operador da condição do filtro (string; ex. igual, maior). |  |  |
| `NOM_CAMPO` | varchar(70) | S | Campo filtrado. |  |  |
| `COD_VALOR` | varchar(255) | S | Valor de comparação do filtro. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA, COD_PERSPECT)` → **META_LISTA_PERSPECT** `(COD_EMPRESA, COD_LISTA, COD_PERSPECT)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LISTA_REL

Relacionamentos mestre-detalhe entre meta-listas.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA_PAI, COD_LISTA_FILHO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_LISTA_FILHO` | integer | N | Meta-lista detalhe (filha) do relacionamento mestre-detalhe. |  | META_LISTA.COD_LISTA |
| 🔑 `COD_LISTA_PAI` | integer | N | Meta-lista mestre (pai). |  | META_LISTA.COD_LISTA |
| `COD_TABELA` | varchar(50) | S | Identificador da tabela/dataset do relacionamento. |  |  |

**Dicas de consulta:** Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## META_LIST_EVENT

Scripts de evento (JavaScript) associados a uma meta-lista.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, COD_LISTA, COD_EVENT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_EVENT` | varchar(255) | N | Identificador do evento (ex. nome de evento de lista) com script associado. |  | EVENT_GERAL.COD_EVENT |
| 🔑 `COD_LISTA` | integer | N | Meta-lista dona do evento. |  | META_LISTA.COD_LISTA |
| `DSL_EVENT` | longtext | N | Código-fonte JavaScript do evento (LOB). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_LISTA)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Chaves compostas coincidem com a PK do alvo; sem FK física.

**Dicas de consulta:** DSL_EVENT é LOB com script; evitar SELECT *. Sempre filtrar COD_EMPRESA e, nas filhas, COD_LISTA; ignore LOG_DELETE=1 em META_LISTA/CAMPO.

## PREFER_PASTA

Preferência de classificação (ordenação) de conteúdo de uma pasta por usuário.

**Ciclo de vida:** Uma linha por usuário/pasta/versão.

**Atenção:** Multi-tenant por COD_EMPRESA (parte da PK).

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(255) | N | Matrícula do usuário dono da preferência. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Número da pasta (documento tipo pasta). |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Versão do documento/pasta. |  | DOCUMENTO.NR_VERSAO |
| `IDI_CLASSIF_PASTA` | integer | N | Índice/critério de classificação (ordenação) escolhido pelo usuário para o conteúdo da pasta. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Pasta cuja preferência de classificação foi salva.

**Dicas de consulta:** Contém referência a usuário (matrícula/id); dado pessoal indireto.
