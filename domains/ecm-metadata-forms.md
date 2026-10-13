# Domínio: ecm-metadata-forms

29 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## ECM_ABSTRACT_FORM_ITEM

Tabela base (@Inheritance TABLE_PER_CLASS) dos itens do formulário de metadados do ECM; contém os atributos comuns a todos os tipos de item.

**Ciclo de vida:** Em TABLE_PER_CLASS as linhas dos itens ficam nas tabelas concretas ECM_*_FORM_ITEM; esta base pode estar vazia.

**PK:** ID · **Unique:** (METADATAFORM_ID, HTML_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador sintético do item (tabela base TABLE_PER_CLASS; chave natural é METADATAFORM_ID+HTML_ID). |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID` | varchar(255) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `PARENT_ITEM` | bigint | S | Item pai (hierarquia). |  | ECM_ABSTRACT_FORM_ITEM.ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(PARENT_ITEM)` → **ECM_ABSTRACT_FORM_ITEM** `(ID)` · N:1 · physical-fk/confirmed — FK ['PARENT_ITEM'] referencia ECM_ABSTRACT_FORM_ITEM.

**Dicas de consulta:** Filtrar por METADATAFORM_ID.

## ECM_BUTTON_FORM_ITEM

Itens do tipo button dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** HTML_ID, METADATAFORM_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `BUTTON_BACKGROUND_COLOR` | varchar(50) | S | Cor de fundo do botão (valor CSS). |  |  |
| `BUTTON_BORDER_COLOR` | varchar(50) | S | Cor da borda do botão (valor CSS). |  |  |
| `BUTTON_TYPE` | varchar(50) | N | Ação do botão (enum ButtonItemTypeEnum como string). | SAVE_AND_CLOSE=salvar e fechar; SAVE_AND_CONTINUE=salvar e continuar; CANCEL=cancelar |  |
| `BUTTON_LABEL` | varchar(200) | S | Texto do botão. |  |  |
| `BUTTON_LABEL_COLOR` | varchar(50) | S | Cor do texto do botão. |  |  |
| `BUTTON_TOOLTIP` | longtext | S | Tooltip do botão (LOB). |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_DATE_FIELD_FORM_ITEM

Itens do tipo date field dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `USE_ANALYTICS` | bit | S | Indica se o campo é usado em analytics/indexação analítica. |  |  |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor (usado como indexador/identificação do documento). |  |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário para o campo. |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo. |  |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. |  |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_DIVIDER_FORM_ITEM

Itens do tipo divider dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `COLOR` | varchar(255) | S | Cor do divisor. |  |  |
| `DIVIDER_TYPE` | varchar(255) | N | Estilo do divisor (enum DividerTypeEnum como string). | LINE=linha; POINTS=pontilhado; TRACE=traço |  |
| `SPACING` | integer | S | Espaçamento do divisor. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_DOCTO_LANGUAGE

Idiomas disponíveis para documentos por tenant (ECM).

**Ciclo de vida:** Poucas linhas por tenant.

**Atenção:** Multi-tenant por TENANT_ID.

**PK:** ID · **Unique:** (TENANT_ID, LANGUAGE_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador do idioma de documento. |  |  |
| `DESCRIPTION` | varchar(255) | N | Descrição do idioma. |  |  |
| `LANGUAGE_CODE` | varchar(255) | N | Código do idioma (ex. pt_BR); único por tenant. |  |  |
| `TENANT_ID` | bigint | N | Tenant do idioma. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant.

## ECM_DYNAMIC_TABLE_FORM_ITEM

Itens do tipo dynamic table dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `DELETE_RECORD_BTN_TEXT` | varchar(255) | S | Texto do botão de excluir registro da tabela dinâmica. |  |  |
| `HAS_ADD_BUTTON` | bit | S | Indica se a tabela dinâmica exibe botão de adicionar registro. |  |  |
| `HAS_DELETE_BUTTON` | bit | S | Indica se a tabela dinâmica exibe botão de excluir registro. |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo. |  |  |
| `NEW_RECORD_BTN_TEXT` | varchar(255) | S | Texto do botão de novo registro. |  |  |
| `TITLE_BACKGROUND_COLOR` | varchar(255) | S | Cor de fundo do título da tabela. |  |  |
| `TITLE_COLOR` | varchar(255) | S | Cor do texto do título da tabela. |  |  |
| `ALIGN_ITEMS_ON_TOP` | bit | S | Alinha os itens da tabela ao topo. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_EVALUATION_FIELD_FORM_ITEM

Itens do tipo evaluation field dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor (usado como indexador/identificação do documento). |  |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário para o campo. |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo. |  |  |
| `MAX_VALUE` | integer | S | Valor máximo da avaliação (ex.: número de estrelas). |  |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. |  |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_EXTERNAL_LINK_FORM_ITEM

Itens do tipo external link dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai.

**Ciclo de vida:** Criada ao salvar o formulário de metadados no editor; chave natural (METADATAFORM_ID, HTML_ID).

**Atenção:** Herança TABLE_PER_CLASS: colunas comuns repetidas; para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM. Sem COD_EMPRESA: o tenant vem via ECM_METADATA_FORM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário; junto com METADATAFORM_ID forma a chave. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário de metadados, em unidades do editor visual. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba ou tabela) que contém este item; nulo se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome/identificador do campo no formulário de metadados, usado como nome do campo de indexação. |  |  |
| `ORDER_ITEM` | integer | S | Posição de ordenação do item dentro do formulário ou do pai. |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do editor. |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do editor. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item (enum MetadataFormItemTypeEnum gravado como string). | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem |  |
| `VALUE_ITEM` | bit | S | Indica se o item guarda valor de metadado (campo de dado) em vez de ser apenas elemento visual. | 1=guarda valor; 0=apenas visual (inferido do nome) |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do editor. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual o item pertence. |  | ECM_METADATA_FORM.ID |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário para o campo. |  |  |
| `LINK` | longtext | S | URL do link externo (LOB). |  |  |
| `VALID_FOR_RELEASE` | bit | S | Indica se o item está válido para publicação (release) do formulário; padrão TRUE na entidade. | 1=válido; 0=inválido (inferido) |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID'] referencia ECM_METADATA_FORM.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · logical-confirmed/probable — Subtipo JPA TABLE_PER_CLASS: tabela repete as colunas do pai abstrato; mesmo item aparece (METADATAFORM_ID,HTML_ID) na tabela base apenas se a base for populada (em TABLE_PER_CLASS as linhas ficam só na tabela concreta).

**Dicas de consulta:** Filtrar por METADATAFORM_ID; junte a ECM_METADATA_FORM.ID. Colunas HELP_TEXT/LINK/BUTTON_TOOLTIP são longtext.

## ECM_FIXED_TABLE_COLUMN

Colunas de um item tabela fixa do formulário de metadados.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador da coluna. |  |  |
| `HTML_ID` | varchar(10) | N | HTML_ID da coluna. |  |  |
| `COLUMN_ORDER` | integer | S | Ordem da coluna na tabela fixa. |  |  |
| `TITLE` | varchar(255) | S | Título da coluna. |  |  |
| `HTML_ID_FIXEDTABLE_ITEM` | varchar(10) | S | HTML_ID do item tabela fixa dono da coluna. |  | ECM_FIXED_TABLE_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | Formulário de metadados da tabela fixa. |  | ECM_METADATA_FORM.ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_FIXEDTABLE_ITEM)` → **ECM_FIXED_TABLE_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · physical-fk/confirmed — FK ['METADATAFORM_ID', 'HTML_ID_FIXEDTABLE_ITEM'] referencia ECM_FIXED_TABLE_FORM_ITEM.

## ECM_FIXED_TABLE_FORM_ITEM

Itens do tipo tabela fixa (grid de colunas e linhas pré-definidas) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe FixedTableMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo no formulário. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_3yruo4t5v7r6t254saa49omac).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_FIXED_TABLE_ROW** `(METADATAFORM_ID, HTML_ID_FIXEDTABLE_ITEM)` · 1:N · jpa-join/confirmed — Valores de células/linhas da tabela fixa (rowsValues, EAGER).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_FIXED_TABLE_COLUMN** `(METADATAFORM_ID, HTML_ID_FIXEDTABLE_ITEM)` · 1:N · jpa-join/probable — Definição das colunas da tabela fixa (FixedTableColumn.fixedTable, mappedBy; nomes exatos das colunas da tabela filha não verificados).

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'. Definições de coluna em ECM_FIXED_TABLE_COLUMN e valores em ECM_FIXED_TABLE_ROW.

## ECM_FIXED_TABLE_ROW

Valores (células) das linhas de um item de tabela fixa de formulário de metadados: cada linha guarda o valor de uma coluna (COLUMN_HTML_ID) em uma linha (ROW_ID).

**Ciclo de vida:** Criada/atualizada ao salvar o formulário; removida em cascata (CascadeType.REMOVE) com o item de tabela fixa.

**Atenção:** PK própria ID; vínculo ao item via (METADATAFORM_ID, HTML_ID_FIXEDTABLE_ITEM). Sem COD_EMPRESA. Uma linha lógica da tabela = várias linhas aqui com mesmo ROW_ID.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | PK sintética (bigint gerado) da célula/linha de valor da tabela fixa. |  |  |
| `COLUMN_HTML_ID` | varchar(10) | N | HTML_ID da coluna (ECM_FIXED_TABLE_COLUMN) à qual o valor pertence. |  | ECM_FIXED_TABLE_COLUMN.HTML_ID |
| `ROW_ID` | varchar(50) | N | Identificador da linha da tabela fixa (até 50 chars); agrupa as células da mesma linha. |  |  |
| `ROW_ORDER` | integer | S | Ordem da linha dentro da tabela fixa. |  |  |
| `COLUMN_VALUE` | varchar(255) | S | Valor de texto da célula (linha x coluna). |  |  |
| `HTML_ID_FIXEDTABLE_ITEM` | varchar(10) | S | HTML_ID do item de tabela fixa dono da linha; FK composta com METADATAFORM_ID. |  | ECM_FIXED_TABLE_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | ID do formulário dono; FK composta com HTML_ID_FIXEDTABLE_ITEM. |  | ECM_FIXED_TABLE_FORM_ITEM.METADATAFORM_ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_FIXEDTABLE_ITEM)` → **ECM_FIXED_TABLE_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · physical-fk/confirmed — Tabela fixa dona da célula (FK_ID_FX_TB_ITM_IN_ROW).
- `(METADATAFORM_ID, COLUMN_HTML_ID)` → **ECM_FIXED_TABLE_COLUMN** `(METADATAFORM_ID, HTML_ID)` · N:1 · logical-probable/probable — COLUMN_HTML_ID identifica a coluna da tabela fixa; sem FK física, nomes das colunas de ECM_FIXED_TABLE_COLUMN não verificados.

**Dicas de consulta:** Reconstruir a tabela: filtrar por METADATAFORM_ID + HTML_ID_FIXEDTABLE_ITEM, agrupar por ROW_ID, ordenar por ROW_ORDER, colunas por COLUMN_HTML_ID.

## ECM_IMAGE_FORM_ITEM

Itens do tipo imagem dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe ImageMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `DOCUMENT_ID` | integer | S | Número do documento ECM da imagem quando IMG_TYPE=ECM_DOCUMENT; NULL nos demais tipos. |  | DOCUMENTO.NR_DOCUMENTO |
| `IMG_HEIGHT` | integer | S | Altura da imagem exibida, em pixels. |  |  |
| `IMAGE_POSITION` | varchar(255) | S | Alinhamento horizontal da imagem no formulário (enum ImagePositionEnum, string). | LEFT=esquerda; RIGHT=direita; CENTER=centro |  |
| `IMG_TYPE` | varchar(255) | N | Origem da imagem (enum ImageFormItemTypeEnum, string). | LINK=URL externa em IMG_LINK; UPLOADED_IMG=imagem enviada (nome em IMG_ATTACH_NAME); ECM_DOCUMENT=documento do ECM (DOCUMENT_ID/DOCUMENT_VERSION) |  |
| `IMG_WIDTH` | integer | S | Largura da imagem exibida, em pixels. |  |  |
| `IMG_ATTACH_NAME` | varchar(255) | S | Nome do arquivo da imagem enviada (IMG_TYPE=UPLOADED_IMG). |  |  |
| `IMG_LINK` | varchar(255) | S | URL da imagem quando IMG_TYPE=LINK. |  |  |
| `DOCUMENT_VERSION` | integer | S | Versão do documento ECM da imagem (junto com DOCUMENT_ID). |  | DOCUMENTO.NR_VERSAO |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_ju7jvsx0u3kdxx2r471680kce).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.
- `(DOCUMENT_ID, DOCUMENT_VERSION)` → **DOCUMENTO** `(NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento ECM da imagem quando IMG_TYPE=ECM_DOCUMENT; sem FK; COD_EMPRESA vem do tenant do formulário.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'. IMG_LINK pode conter URL externa.

## ECM_LABEL_FORM_ITEM

Itens do tipo rótulo de texto estático dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe LabelMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `LABEL_TEXT` | longtext | S | Texto do rótulo estático exibido no formulário (LOB, pode conter HTML). |  |  |
| `LABEL_POSITION` | varchar(255) | N | Alinhamento do texto do rótulo (enum TitlePositionEnum, string). | LEFT=esquerda; RIGHT=direita; CENTER=centro |  |
| `LABEL_COLOR` | varchar(255) | S | Cor do texto do rótulo (valor CSS, ex.: hexadecimal). |  |  |
| `TEXT_FONT_SIZE` | varchar(255) | S | Tamanho da fonte do rótulo (enum LabelSizeEnum, string). | EXTRA_SMALL; SMALL; MEDIUM; LARGE; EXTRA_LARGE |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_daoh4fooy8ely3rvkqtttt7ps).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'. LABEL_TEXT é LOB.

## ECM_LIST_FIELD_FORM_ITEM

Itens do tipo campo de lista/seleção (combo, lista, checkbox, radio) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe ListMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor do registro (usado para identificar/descrever o registro). | 1=é descritor; 0=não |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário junto ao campo (LOB). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo no formulário. |  |  |
| `LIST_TYPE` | varchar(255) | N | Tipo de controle de seleção (enum ListItemTypeEnum, string). | LIST=lista; COMBO=lista suspensa; CHECKBOX=seleção múltipla; RADIO_BUTTON=escolha única |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. | 1=múltiplos valores; 0=valor único |  |
| `OPTIONS` | longtext | S | Opções disponíveis do campo de lista (LOB, texto serializado definido pelo editor do formulário). |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. | 1=obrigatório; 0=opcional |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único entre os registros do formulário. | 1=único; 0=não |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_e32sbu3u7jobm7ebqcci4i4i3).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'. OPTIONS é LOB.

## ECM_METADATA_FORM

Cabeçalho de um formulário de metadados do ECM Fluig (tipo de documento com campos configuráveis, 'metadata form'). Uma linha por versão do formulário, ligada a um documento ECM.

**Ciclo de vida:** Criada ao criar/editar o formulário (status EDITING), vira CURRENT ao publicar e DEPRECATED quando outra versão assume (UPDATE em lote por documento). Volume baixo (um por versão de formulário).

**Atenção:** Multi-tenant via TENANT_ID (= DOCUMENTO.COD_EMPRESA). Unique (TENANT_ID, DOCUMENT_ID, DCMNT_VRSN_NMBER). Versionamento por VERSION_STATUS; consultas de formulário ativo devem filtrar VERSION_STATUS='CURRENT'. Raiz da hierarquia: todas as tabelas ECM_*_FORM_ITEM, ECM_TAB_ITEM, ECM_FIXED_TABLE_ROW e ECM_METADATA_FORM_TRANSLATE apontam para ID.

**PK:** ID · **Unique:** (TENANT_ID, DOCUMENT_ID, DCMNT_VRSN_NMBER)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | PK sintética do formulário de metadados (uma linha por versão do formulário). |  |  |
| `TITLE` | varchar(255) | S | Título do formulário de metadados. |  |  |
| `FORM_UUID` | varchar(255) | S | UUID gerado do formulário (UUID.randomUUID() na criação). |  |  |
| `VERSION_STATUS` | varchar(255) | N | Estado da versão do formulário (enum MetadataFormVersionStatusEnum, string). | EDITING=em edição; CURRENT=versão vigente; DEPRECATED=versão antiga substituída (setada em lote pela query UPDATE_SET_OLD_FORMS_DEPRECATED) |  |
| `TENANT_ID` | bigint | S | Empresa/tenant do documento associado; parte do FK composto para DOCUMENTO.COD_EMPRESA. |  | DOCUMENTO.COD_EMPRESA |
| `DOCUMENT_ID` | integer | S | Número do documento ECM (tipo formulário) ao qual esta versão está ligada. |  | DOCUMENTO.NR_DOCUMENTO |
| `DCMNT_VRSN_NMBER` | integer | S | Versão do documento ECM ligado ao formulário. |  | DOCUMENTO.NR_VERSAO |
| `ALIGN_ITEMS_ON_TOP` | bit | S | Se 1, alinha ao topo os itens do formulário; default TRUE na entidade. | 1=alinha ao topo; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, DOCUMENT_ID, DCMNT_VRSN_NMBER)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · jpa-join/confirmed — Documento ECM (formulário) associado a esta versão (FK_METDTFORM_DCMNT, @ManyToOne Document).
- `(ID)` → **ECM_METADATA_FORM_TRANSLATE** `(METADATAFORM_ID)` · 1:N · jpa-join/confirmed — Traduções dos textos do formulário.
- `(ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID)` · 1:N · jpa-join/confirmed — Itens (children) do formulário; existem em uma tabela ECM_*_FORM_ITEM por tipo.

**Dicas de consulta:** Join com DOCUMENTO por (TENANT_ID=COD_EMPRESA, DOCUMENT_ID=NR_DOCUMENTO, DCMNT_VRSN_NMBER=NR_VERSAO). Named queries: filtro por título UPPER(TITLE) LIKE e VERSION_STATUS=CURRENT.

## ECM_METADATA_FORM_TRANSLATE

Traduções (pt, en, es) de textos de um formulário de metadados, indexadas por chave de string.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário com tradução de rótulos; removida com o formulário.

**Atenção:** Unique (METADATAFORM_ID, STRING_KEY). Sem COD_EMPRESA; tenant via ECM_METADATA_FORM.

**PK:** ID · **Unique:** (METADATAFORM_ID, STRING_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | PK sintética da tradução. |  |  |
| `STRING_KEY` | varchar(255) | S | Chave do texto traduzível (ex.: rótulos do formulário); única por METADATAFORM_ID. |  |  |
| `STRING_EN` | longtext | S | Texto traduzido em inglês (LOB). |  |  |
| `STRING_ES` | longtext | S | Texto traduzido em espanhol (LOB). |  |  |
| `STRING_PT` | longtext | S | Texto traduzido em português (LOB). |  |  |
| `METADATAFORM_ID` | bigint | N | Formulário de metadados ao qual a tradução pertence. |  | ECM_METADATA_FORM.ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário traduzido (FK_TRASLTE_MTDT).

**Dicas de consulta:** Buscar por METADATAFORM_ID; colunas STRING_* são LOB.

## ECM_NUMBER_FIELD_FORM_ITEM

Itens do tipo campo numérico dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe NumberFieldMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `USE_ANALYTICS` | bit | S | Indica se o campo é usado em analytics/análises dos dados do formulário. | 1=usa analytics; 0=não |  |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor do registro (usado para identificar/descrever o registro). | 1=é descritor; 0=não |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário junto ao campo (LOB). |  |  |
| `INITIAL_VALUE_NUMBER_FIELD` | decimal(19,2) | S | Valor numérico inicial padrão do campo (decimal 19,2). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo no formulário. |  |  |
| `MASK` | varchar(255) | S | Máscara de formatação do campo numérico (texto livre). |  |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. | 1=múltiplos valores; 0=valor único |  |
| `PLACEHOLDER` | varchar(255) | S | Texto de dica (placeholder) mostrado no campo vazio. |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. | 1=obrigatório; 0=opcional |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único entre os registros do formulário. | 1=único; 0=não |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_quoq3hgs6rdki35roty3pd9v3).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'.

## ECM_SECTION_FORM_ITEM

Itens do tipo seção (agrupador visual com título) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe SectionMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `SECTION_TITLE` | varchar(255) | S | Título exibido no cabeçalho da seção. |  |  |
| `TITLE_BACKGROUND_COLOR` | varchar(255) | S | Cor de fundo do cabeçalho da seção (valor CSS). |  |  |
| `TITLE_COLOR` | varchar(255) | S | Cor do texto do título da seção (valor CSS). |  |  |
| `SECTION_ALIGN_ITEMS_ON_TOP` | bit | S | Se 1, alinha os itens filhos da seção ao topo. | 1=alinha ao topo; 0=não |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_plmdugi58s91o665j4be98257).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'.

## ECM_TAB_FORM_ITEM

Itens do tipo contêiner de abas dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe TabMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `TAB_BORDER_COLOR` | varchar(255) | S | Cor da borda das abas (valor CSS). |  |  |
| `TAB_TEXT_COLOR` | varchar(255) | S | Cor do texto das abas (valor CSS). |  |  |
| `TAB_ALIGN_ITEMS_ON_TOP` | bit | S | Se 1, alinha ao topo os itens dentro das abas. | 1=alinha ao topo; 0=não |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_het7mr1dwm017q4o0y3a9uvwp).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_TAB_ITEM** `(METADATAFORM_ID, HTML_ID_TABFORM_ITEM)` · 1:N · jpa-join/confirmed — Abas do item (TabMetadataFormItem.tabs).

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'.

## ECM_TAB_ITEM

Abas individuais de um item de abas (TabMetadataFormItem) em formulário de metadados: título e ordem de cada aba.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário; removida em cascata com o item de abas.

**Atenção:** PK própria ID; vínculo ao item de abas via (METADATAFORM_ID, HTML_ID_TABFORM_ITEM). HTML_ID aqui é o id da aba, não do item pai. Os candidatos inferidos do extrator para outras tabelas *_FORM_ITEM são falsos positivos.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | PK sintética de uma aba individual. |  |  |
| `HTML_ID` | varchar(10) | N | HTML_ID da aba (até 10 chars), identificador da aba dentro do formulário. |  |  |
| `ORDER_ECM_TAB_ITEM` | integer | S | Ordem de exibição da aba dentro do item de abas. |  |  |
| `TAB_TITLE` | varchar(255) | S | Título exibido na aba. |  |  |
| `HTML_ID_TABFORM_ITEM` | varchar(10) | S | HTML_ID do item de abas (ECM_TAB_FORM_ITEM) dono desta aba; FK composta com METADATAFORM_ID. |  | ECM_TAB_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | ID do formulário dono; FK composta com HTML_ID_TABFORM_ITEM. |  | ECM_TAB_FORM_ITEM.METADATAFORM_ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_TABFORM_ITEM)` → **ECM_TAB_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · physical-fk/confirmed — Item de abas dono da aba (FK_ID_TB_FRM_ITM).

**Dicas de consulta:** Listar abas: WHERE METADATAFORM_ID=? AND HTML_ID_TABFORM_ITEM=? ORDER BY ORDER_ECM_TAB_ITEM. Itens filhos de uma aba referenciam HTML_ID_PARENT (provável o HTML_ID da aba/item).

## ECM_TEXT_AREA_FIELD_FORM_ITEM

Itens do tipo campo de texto longo (textarea) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe TextAreaMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor do registro (usado para identificar/descrever o registro). | 1=é descritor; 0=não |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário junto ao campo (LOB). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo no formulário. |  |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. | 1=múltiplos valores; 0=valor único |  |
| `PLACEHOLDER` | varchar(255) | S | Texto de dica (placeholder) mostrado no campo vazio. |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. | 1=obrigatório; 0=opcional |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único entre os registros do formulário. | 1=único; 0=não |  |
| `RICH_TEXT` | bit | S | Indica se o campo de texto longo usa editor de texto rico (HTML). | 1=rich text; 0=texto simples |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_7kpt9c7q015du5gsrllyb6qwo).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'.

## ECM_TEXT_FIELD_FORM_ITEM

Itens do tipo campo de texto curto com máscara dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe TextFieldMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `USE_ANALYTICS` | bit | S | Indica se o campo é usado em analytics/análises dos dados do formulário. | 1=usa analytics; 0=não |  |
| `DESCRIPTOR` | bit | S | Indica se o campo é descritor do registro (usado para identificar/descrever o registro). | 1=é descritor; 0=não |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao usuário junto ao campo (LOB). |  |  |
| `INITIAL_VALUE` | varchar(255) | S | Valor inicial padrão do campo de texto. |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rótulo exibido do campo no formulário. |  |  |
| `TEXT_FIELD_TYPE` | varchar(255) | N | Máscara/tipo do campo de texto (enum TextFieldMaskEnum, string). | NONE; CPF; CEP; PERCENT; EMAIL; CNPJ; DATETIME; PHONE; CELLPHONE; CARPLATE; CURRENCY; IP |  |
| `MULTIPLE_VALUES` | bit | S | Indica se o campo aceita múltiplos valores. | 1=múltiplos valores; 0=valor único |  |
| `PLACEHOLDER` | varchar(255) | S | Texto de dica (placeholder) mostrado no campo vazio. |  |  |
| `REQUIRED` | bit | S | Indica se o preenchimento do campo é obrigatório. | 1=obrigatório; 0=opcional |  |
| `IS_UNIQUE` | bit | S | Indica se o valor do campo deve ser único entre os registros do formulário. | 1=único; 0=não |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_b785lqy7bporxtif7cjej1oqn).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'. Campos com máscara CPF/CNPJ/EMAIL/IP podem guardar dados pessoais no valor do registro (não nesta tabela).

## ECM_TITLE_FORM_ITEM

Itens do tipo título dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário.

**Ciclo de vida:** Criada/atualizada ao salvar o formulário no editor de formulários de metadados; removida em cascata com o formulário/versão. Volume proporcional à quantidade de formulários e campos.

**Atenção:** Subclasse JPA (TABLE_PER_CLASS) de AbstractMetadataFormItem (classe TitleMetadataFormItem): não há tabela concreta ECM_ABSTRACT_FORM_ITEM garantida; as colunas comuns (HTML_ID, ITEM_*, NAME, ORDER_ITEM, FORM_ITEM_TYPE...) se repetem em cada tabela de item. PK composta (METADATAFORM_ID, HTML_ID). Sem COD_EMPRESA: tenant só via ECM_METADATA_FORM.TENANT_ID.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulário (até 10 chars); com METADATAFORM_ID forma a PK do item. |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout do formulário (grade), inteiro; 0 quando não definido. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (seção, aba, etc.) que contém este item; NULL se estiver na raiz do formulário. |  | ECM_*_FORM_ITEM.HTML_ID (mesmo METADATAFORM_ID) |
| `NAME` | varchar(255) | S | Nome técnico do campo, usado como chave do valor ao gravar os dados do registro do formulário. |  |  |
| `ORDER_ITEM` | integer | S | Ordem de exibição do item entre os filhos do formulário (ORDER BY order). |  |  |
| `ITEM_POS_X` | integer | S | Posição horizontal do item no layout do formulário (inteiro). |  |  |
| `ITEM_POS_Y` | integer | S | Posição vertical do item no layout do formulário (inteiro). |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum gravado como string; identifica a subclasse/tabela do item. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (nome da classe JPA do item; o valor igual ao da tabela) |  |
| `VALUE_ITEM` | bit | S | Indica se o item armazena valor do usuário (campo de dado) em oposição a item apenas visual. | 1=campo que guarda valor; 0=elemento visual |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout do formulário (inteiro). |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | ID do formulário de metadados dono do item; parte da PK. |  | ECM_METADATA_FORM.ID |
| `COLOR` | varchar(255) | S | Cor do texto do título (valor CSS). |  |  |
| `TITLE` | varchar(255) | S | Texto do título exibido no formulário. |  |  |
| `TITLE_HEIGHT_TYPE` | varchar(255) | S | Nível/tamanho do título (enum TitleItemHeightEnum, string). | H1; H2; H3 |  |
| `TITLE_POSITION` | varchar(255) | S | Alinhamento do título (enum TitlePositionEnum, string). | LEFT=esquerda; RIGHT=direita; CENTER=centro |  |
| `VALID_FOR_RELEASE` | bit | S | Flag de validade do item para publicação (release) do formulário; default Boolean.TRUE na entidade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulário de metadados dono do item (FK FK_fwj76d347n8wtusdetk0u0enl).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Herança JPA TABLE_PER_CLASS: ECM_ABSTRACT_FORM_ITEM é a superclasse abstrata; esta tabela repete as colunas comuns. Sem FK física.

**Dicas de consulta:** Para listar todos os itens de um formulário é preciso UNION das tabelas ECM_*_FORM_ITEM filtradas por METADATAFORM_ID. Filtre tenant via JOIN ECM_METADATA_FORM (TENANT_ID). Preferir a versão VERSION_STATUS='CURRENT'.

## ECM_UPLOAD_FILE_FORM_ITEM

Subclasse (JPA TABLE_PER_CLASS) de ECM_ABSTRACT_FORM_ITEM para itens de upload de arquivo em formularios de metadados do ECM. Cada linha e um campo de anexo de um formulario.

**Ciclo de vida:** Criada/atualizada quando o designer salva o formulario de metadados; copiada ao versionar o formulario; removida com o formulario. Volume baixo.

**Atenção:** PK composta (METADATAFORM_ID,HTML_ID). Colunas comuns repetidas de ECM_ABSTRACT_FORM_ITEM (TABLE_PER_CLASS): o HTML_ID e unico por formulario entre todas as tabelas *_FORM_ITEM.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulario de metadados; junto com METADATAFORM_ID forma a PK composta (varchar 10). |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout (grade) do formulario de metadados. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (secao/aba) que contem este item no layout; NULL se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome tecnico do campo/item, usado como nome do campo no formulario. |  |  |
| `ORDER_ITEM` | integer | S | Posicao de ordenacao do item no formulario. |  |  |
| `ITEM_POS_X` | integer | S | Posicao horizontal (coluna) do item no layout do formulario. |  |  |
| `ITEM_POS_Y` | integer | S | Posicao vertical (linha) do item no layout do formulario. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum (ex.: UploadFileMetadataFormItem), igual ao nome da classe da entidade. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (armazenado como string) |  |
| `VALUE_ITEM` | bit | S | Flag: o item guarda valor preenchido pelo usuario (campo de dados) em vez de ser elemento decorativo/estrutural. | 1=item de valor; 0=estrutural |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout (grade) do formulario. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulario de metadados dono do item; parte da PK composta. |  | ECM_METADATA_FORM.ID |
| `ALLOWED_EXTENSIONS` | varchar(255) | S | Lista de extensoes de arquivo permitidas no upload. |  |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao preencher o campo (LOB). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rotulo exibido do campo no formulario. |  |  |
| `REQUIRED` | bit | S | Flag: preenchimento obrigatorio do campo. | 1=obrigatorio; 0=opcional |  |
| `UPLOAD_ITEM_MULTIPLE_VALUES` | bit | S | Flag: permite enviar multiplos arquivos neste campo. |  |  |
| `UPLOAD_ITEM_ALLOW_MANY_ITEMS` | bit | S | Flag: permite varios itens/linhas de upload no campo. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Flag: item validado/consistente para a publicacao (release) do formulario. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulario de metadados dono do item.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Heranca TABLE_PER_CLASS: superclasse abstrata; sem FK fisica, repete as colunas comuns.

**Dicas de consulta:** Filtrar por METADATAFORM_ID. Para ler todos os itens do formulario e preciso unir (UNION) todas as tabelas *_FORM_ITEM.

## ECM_ZOOM_DISPLAY_FIELD

Campos do dataset exibidos na janela de pesquisa de um item Zoom de formulario de metadados (colunas de exibicao/pesquisa).

**Ciclo de vida:** Criada ao configurar o item zoom no designer; removida/recriada ao salvar o formulario. Volume baixo.

**Atenção:** Unique (METADATAFORM_ID,HTML_ID_ZOOM_ITEM,DATASET_FIELD). Filha de ECM_ZOOM_FIELD_FORM_ITEM via FK composta FK_ID_ZM_FLD_DSPLY.

**PK:** ID · **Unique:** (METADATAFORM_ID, HTML_ID_ZOOM_ITEM, DATASET_FIELD)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador sequencial da linha (PK). |  |  |
| `DATASET_FIELD` | varchar(255) | S | Nome do campo do dataset a exibir na pesquisa do zoom. |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rotulo exibido para o campo do dataset. |  |  |
| `SEARCH` | bit | S | Flag: campo e pesquisavel na janela do zoom. | 1=usado na pesquisa; 0=so exibicao |  |
| `STANDARD` | bit | S | Flag: campo e exibido por padrao na lista do zoom. |  |  |
| `HTML_ID_ZOOM_ITEM` | varchar(10) | S | HTML_ID do item zoom pai; parte da FK composta. |  | ECM_ZOOM_FIELD_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | Formulario de metadados do item zoom pai; parte da FK composta. |  | ECM_ZOOM_FIELD_FORM_ITEM.METADATAFORM_ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` → **ECM_ZOOM_FIELD_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · physical-fk/confirmed — Item zoom ao qual o campo de exibicao pertence.

**Dicas de consulta:** Join sempre pelo par (METADATAFORM_ID, HTML_ID_ZOOM_ITEM).

## ECM_ZOOM_FIELD_FORM_ITEM

Subclasse de ECM_ABSTRACT_FORM_ITEM para itens Zoom (selecao de registro de um dataset) em formularios de metadados do ECM.

**Ciclo de vida:** Gravada ao salvar o formulario no designer; copiada na versao; removida com o formulario. Volume baixo.

**Atenção:** PK composta (METADATAFORM_ID,HTML_ID). TABLE_PER_CLASS: repete colunas da superclasse. Pai de ECM_ZOOM_DISPLAY_FIELD, ECM_ZOOM_FILTER_FIELD e ECM_ZOOM_OUTPUT_FIELD.

**PK:** METADATAFORM_ID, HTML_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulario de metadados; junto com METADATAFORM_ID forma a PK composta (varchar 10). |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout (grade) do formulario de metadados. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (secao/aba) que contem este item no layout; NULL se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome tecnico do campo/item, usado como nome do campo no formulario. |  |  |
| `ORDER_ITEM` | integer | S | Posicao de ordenacao do item no formulario. |  |  |
| `ITEM_POS_X` | integer | S | Posicao horizontal (coluna) do item no layout do formulario. |  |  |
| `ITEM_POS_Y` | integer | S | Posicao vertical (linha) do item no layout do formulario. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum (ex.: UploadFileMetadataFormItem), igual ao nome da classe da entidade. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (armazenado como string) |  |
| `VALUE_ITEM` | bit | S | Flag: o item guarda valor preenchido pelo usuario (campo de dados) em vez de ser elemento decorativo/estrutural. | 1=item de valor; 0=estrutural |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout (grade) do formulario. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulario de metadados dono do item; parte da PK composta. |  | ECM_METADATA_FORM.ID |
| `USE_ANALYTICS` | bit | S | Flag: campo participa de analise/indexacao analitica dos dados do formulario. |  |  |
| `CARD_DATASET_ID` | integer | S | Identificador numerico do dataset de fichas (cartao) usado como fonte; alternativa a DATASET_ID. |  |  |
| `DATASET_ID` | varchar(255) | S | Nome (codigo) do dataset que alimenta o zoom. |  | DATASET.NOME |
| `DESCRIPTOR` | bit | S | Flag: campo usado como descritor (identificacao resumida) do registro do formulario. |  |  |
| `DISPLAY_KEY` | varchar(255) | S | Campo do dataset usado como chave/texto principal de exibicao do valor selecionado. |  |  |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao preencher o campo (LOB). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rotulo exibido do campo no formulario. |  |  |
| `MAX_SELECTION` | integer | S | Numero maximo de itens selecionaveis quando ha multiplos valores. |  |  |
| `MULTIPLE_VALUES` | bit | S | Flag: permite selecionar multiplos valores. | 1=multiplos; 0=unico |  |
| `PLACEHOLDER` | varchar(255) | S | Texto de placeholder exibido no campo vazio. |  |  |
| `REQUIRED` | bit | S | Flag: preenchimento obrigatorio do campo. | 1=obrigatorio; 0=opcional |  |
| `RESULT_LIMIT` | integer | S | Limite de resultados retornados na busca/pesquisa do zoom. |  |  |
| `IS_UNIQUE` | bit | S | Flag: valor do campo deve ser unico entre os registros do formulario. |  |  |
| `VALID_FOR_RELEASE` | bit | S | Flag: item validado/consistente para a publicacao (release) do formulario. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulario dono do item.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Heranca TABLE_PER_CLASS; sem FK fisica.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ZOOM_DISPLAY_FIELD** `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` · 1:N · physical-fk/confirmed — Campos de exibicao do zoom.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ZOOM_FILTER_FIELD** `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` · 1:N · physical-fk/confirmed — Filtros fixos do zoom.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ZOOM_OUTPUT_FIELD** `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` · 1:N · jpa-join/confirmed — Campos de saida (preenchimento de outros itens).

**Dicas de consulta:** DATASET_ID e referencia logica por nome ao dataset (nao validada: confidence medium).

## ECM_ZOOM_FILTER_FIELD

Filtros fixos (campo=valor) aplicados ao dataset consultado por um item Zoom de formulario de metadados.

**Ciclo de vida:** Criada ao configurar filtros do zoom no designer; recriada ao salvar. Volume baixo.

**Atenção:** Unique (METADATAFORM_ID,HTML_ID_ZOOM_ITEM,FILTER_FIELD). FK composta FK_ID_ZM_FLD_FLTR para ECM_ZOOM_FIELD_FORM_ITEM.

**PK:** ID · **Unique:** (METADATAFORM_ID, HTML_ID_ZOOM_ITEM, FILTER_FIELD)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador sequencial da linha (PK). |  |  |
| `FILTER_FIELD` | varchar(255) | S | Nome do campo do dataset sobre o qual o filtro e aplicado. |  |  |
| `FILTER_VALUE` | varchar(255) | S | Valor constante usado no filtro do campo. |  |  |
| `HTML_ID_ZOOM_ITEM` | varchar(10) | S | HTML_ID do item zoom pai; parte da FK composta. |  | ECM_ZOOM_FIELD_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | Formulario do item zoom pai; parte da FK composta. |  | ECM_ZOOM_FIELD_FORM_ITEM.METADATAFORM_ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` → **ECM_ZOOM_FIELD_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · physical-fk/confirmed — Item zoom ao qual o filtro pertence.

**Dicas de consulta:** Join pelo par (METADATAFORM_ID, HTML_ID_ZOOM_ITEM).

## ECM_ZOOM_OUTPUT_FIELD

Mapeia um campo (DISPLAY_KEY) do dataset do zoom para outro item do formulario (HTML_ID) que sera preenchido quando um registro e selecionado.

**Ciclo de vida:** Criada ao configurar saidas do zoom; recriada ao salvar o formulario. Volume baixo.

**Atenção:** Sem FK fisica visivel no input; JPA @JoinColumns (FK_ID_ZM_OUT_DSPLY) para ECM_ZOOM_FIELD_FORM_ITEM via (METADATAFORM_ID,HTML_ID_ZOOM_ITEM). HTML_ID e varchar(255) aqui (mas 10 nas tabelas de item) e NAO e FK; as relacoes inferidas para as tabelas *_FORM_ITEM sao heuristicas erradas.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Identificador sequencial da linha (PK). |  |  |
| `HTML_ID` | varchar(255) | S | HTML_ID do item do formulario de destino que recebe o valor do campo de saida (referencia logica, sem FK). |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `DISPLAY_KEY` | varchar(255) | S | Campo do dataset cujo valor e copiado para o item de destino. |  |  |
| `HTML_ID_ZOOM_ITEM` | varchar(10) | S | HTML_ID do item zoom pai; parte da FK composta. |  | ECM_ZOOM_FIELD_FORM_ITEM.HTML_ID |
| `METADATAFORM_ID` | bigint | S | Formulario do item zoom pai (e do item de destino). |  | ECM_ZOOM_FIELD_FORM_ITEM.METADATAFORM_ID |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID, HTML_ID_ZOOM_ITEM)` → **ECM_ZOOM_FIELD_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · jpa-join/confirmed — Item zoom dono do mapeamento de saida (@JoinColumns, FK_ID_ZM_OUT_DSPLY).
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · N:1 · logical-probable/probable — Item de destino preenchido; polimorfico entre as tabelas *_FORM_ITEM, sem FK.

**Dicas de consulta:** Para achar o item de destino faca lookup por (METADATAFORM_ID, HTML_ID) em todas as tabelas *_FORM_ITEM.

## ECM_ZOOM_USER_FORM_ITEM

Subclasse de ECM_ABSTRACT_FORM_ITEM para itens Zoom de usuario (selecao de usuarios) em formularios de metadados do ECM.

**Ciclo de vida:** Gravada ao salvar o formulario no designer; copiada na versao; removida com o formulario. Volume baixo.

**Atenção:** PK composta (HTML_ID,METADATAFORM_ID). TABLE_PER_CLASS: repete colunas da superclasse.

**PK:** HTML_ID, METADATAFORM_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `HTML_ID` | varchar(10) | N | Identificador HTML do item dentro do formulario de metadados; junto com METADATAFORM_ID forma a PK composta (varchar 10). |  |  |
| `ITEM_POS_HEIGHT` | integer | S | Altura do item no layout (grade) do formulario de metadados. |  |  |
| `HTML_ID_PARENT` | varchar(10) | S | HTML_ID do item pai (secao/aba) que contem este item no layout; NULL se estiver na raiz. |  | ECM_ABSTRACT_FORM_ITEM.HTML_ID |
| `NAME` | varchar(255) | S | Nome tecnico do campo/item, usado como nome do campo no formulario. |  |  |
| `ORDER_ITEM` | integer | S | Posicao de ordenacao do item no formulario. |  |  |
| `ITEM_POS_X` | integer | S | Posicao horizontal (coluna) do item no layout do formulario. |  |  |
| `ITEM_POS_Y` | integer | S | Posicao vertical (linha) do item no layout do formulario. |  |  |
| `FORM_ITEM_TYPE` | varchar(255) | N | Tipo do item: nome do enum MetadataFormItemTypeEnum (ex.: UploadFileMetadataFormItem), igual ao nome da classe da entidade. | TextFieldMetadataFormItem; TextAreaMetadataFormItem; ExternalLinkMetadataFormItem; ListMetadataFormItem; UploadFileMetadataFormItem; NumberFieldMetadataFormItem; EvaluationMetadataFormItem; DateFieldMetadataFormItem; ZoomFieldMetadataFormItem; TitleMetadataFormItem; DividerMetadataFormItem; SectionMetadataFormItem; TabMetadataFormItem; ImageMetadataFormItem; DynamicTableMetadataFormItem; FixedTableMetadataFormItem; LabelMetadataFormItem; ZoomUserMetadataFormItem; ButtonMetadataFormItem (armazenado como string) |  |
| `VALUE_ITEM` | bit | S | Flag: o item guarda valor preenchido pelo usuario (campo de dados) em vez de ser elemento decorativo/estrutural. | 1=item de valor; 0=estrutural |  |
| `ITEM_WIDTH` | integer | S | Largura do item no layout (grade) do formulario. |  |  |
| 🔑 `METADATAFORM_ID` | bigint | N | Formulario de metadados dono do item; parte da PK composta. |  | ECM_METADATA_FORM.ID |
| `USE_ANALYTICS` | bit | S | Flag: campo participa de analise/indexacao analitica dos dados do formulario. |  |  |
| `DESCRIPTOR` | bit | S | Flag: campo usado como descritor (identificacao resumida) do registro do formulario. |  |  |
| `ZOOM_USER_FILTER_GROUP` | varchar(255) | S | Codigo do grupo usado para filtrar usuarios quando ZOOM_USR_FILTER_TYPE=GROUP_FILTER. |  | FDN_GROUP.GROUP_CODE |
| `HELP_TEXT` | longtext | S | Texto de ajuda exibido ao preencher o campo (LOB). |  |  |
| `FIELD_LABEL` | varchar(255) | S | Rotulo exibido do campo no formulario. |  |  |
| `MAX_SELECTION` | integer | S | Numero maximo de itens selecionaveis quando ha multiplos valores. |  |  |
| `MULTIPLE_VALUES` | bit | S | Flag: permite selecionar multiplos valores. | 1=multiplos; 0=unico |  |
| `PLACEHOLDER` | varchar(255) | S | Texto de placeholder exibido no campo vazio. |  |  |
| `REQUIRED` | bit | S | Flag: preenchimento obrigatorio do campo. | 1=obrigatorio; 0=opcional |  |
| `RESULT_LIMIT` | integer | S | Limite de resultados retornados na busca/pesquisa do zoom. |  |  |
| `ZOOM_USER_FILTER_ROLE` | varchar(255) | S | Codigo do papel usado para filtrar usuarios quando ZOOM_USR_FILTER_TYPE=ROLE_FILTER. |  |  |
| `IS_UNIQUE` | bit | S | Flag: valor do campo deve ser unico entre os registros do formulario. |  |  |
| `ZOOM_USR_TYPE_VALUE_SAVE` | varchar(255) | N | Que atributo do usuario e gravado como valor do campo (enum por nome). | SAVE_EMAIL=grava e-mail; SAVE_LOGIN=grava login |  |
| `ZOOM_USR_FILTER_TYPE` | varchar(255) | N | Tipo de filtro aplicado na lista de usuarios (enum por nome). | NONE=sem filtro; GROUP_FILTER=filtra por grupo; ROLE_FILTER=filtra por papel |  |
| `VALID_FOR_RELEASE` | bit | S | Flag: item validado/consistente para a publicacao (release) do formulario. |  |  |

**Relacionamentos (saem desta tabela):**

- `(METADATAFORM_ID)` → **ECM_METADATA_FORM** `(ID)` · N:1 · physical-fk/confirmed — Formulario dono do item.
- `(METADATAFORM_ID, HTML_ID)` → **ECM_ABSTRACT_FORM_ITEM** `(METADATAFORM_ID, HTML_ID)` · 1:1 · jpa-join/confirmed — Heranca TABLE_PER_CLASS; sem FK fisica.

**Dicas de consulta:** Valor gravado pode ser e-mail ou login do usuario (dado pessoal) conforme ZOOM_USR_TYPE_VALUE_SAVE.
