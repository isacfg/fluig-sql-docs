# Domínio: wcm-portal

16 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_APPLICATION

Catálogo de aplicações do portal WCM em herança single-table: temas, layouts, widgets, componentes (páginas) e aplicações; APPLICATION_TYPE discrimina o tipo.

**Ciclo de vida:** Registrada ao instalar/publicar pacotes (EAR) de widget/tema/layout; poucas centenas de linhas; sem tenant.

**Atenção:** Herança JPA SINGLE_TABLE por APPLICATION_TYPE (theme/layout/widget/component/application). Colunas específicas (PAGE_DESCRIPTOR, WIDGET_EDIT_FILE, MOBILEAPP_WIDGET) ficam NULL nos outros tipos; APPLICATION_FILE mapeia themeFile/pageFile/viewFile/layoutFile conforme o tipo. Único por APPLICATION_CODE.

**PK:** APPLICATION_ID · **Unique:** (APPLICATION_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `APPLICATION_TYPE` | varchar(31) | N | Discriminador da herança: tipo da aplicação WCM. | theme=tema; layout=layout; widget=widget (RESOURCE_TYPE_WIDGET); demais (component/application) não confirmados |  |
| 🔑 `APPLICATION_ID` | bigint(20) | N | Chave primária da aplicação WCM (referenciada por páginas, temas, layouts, widgets). |  |  |
| `ACTIVATION_CLASS` | varchar(255) | S | Classe Java de ativação invocada ao instalar/ativar a aplicação. |  |  |
| `APPLICATION_EXTENSIBLE` | bit(1) | N | Indica se a aplicação pode ser estendida por outras. | 1=extensível; 0=não |  |
| `APPLICATION_PUBLIC` | bit(1) | N | Indica se a aplicação é pública (disponível a todos/sem autenticação). | 1=pública; 0=não |  |
| `APPLICATION_VERSION` | varchar(80) | N | Versão do pacote da aplicação (texto). |  |  |
| `APPLICATION_CODE` | varchar(40) | N | Código único da aplicação, usado em URLs e referências. |  |  |
| `APPLICATION_CONTEXT` | varchar(60) | N | Contexto web (context root) onde a aplicação é servida. |  |  |
| `DESCRIPTION` | varchar(4000) | N | Descrição da aplicação (até 4000). |  |  |
| `DEVELOPER_CODE` | varchar(80) | N | Código do desenvolvedor/fabricante da aplicação. |  |  |
| `DEVELOPER_NAME` | varchar(80) | N | Nome do desenvolvedor/fabricante. |  |  |
| `DEVELOPER_URL` | varchar(120) | N | URL do desenvolvedor/fabricante. |  |  |
| `EXTENDED_DATA` | longtext | S | Dados estendidos da aplicação em texto longo (LOB). |  |  |
| `FILE_NAME` | varchar(255) | S | Nome do arquivo de origem da aplicação. |  |  |
| `EAR_FILE_NAME` | varchar(255) | S | Nome do arquivo EAR implantado da aplicação. |  |  |
| `APPLICATION_ICON` | varchar(80) | S | Ícone da aplicação (nome/classe). |  |  |
| `INTERNAL` | bit(1) | N | Indica aplicação interna da plataforma (fornecida pelo Fluig). | 1=interna; 0=externa |  |
| `IS_EXTENSION` | bit(1) | N | Indica se a aplicação estende outra aplicação. | 1=extensão; 0=não |  |
| `LOCALE_FILE` | varchar(40) | S | Nome-base do arquivo de internacionalização (localeFileBaseName). |  |  |
| `MAX_HEIGHT` | int(11) | S | Altura máxima (px) do widget/componente. |  |  |
| `MAX_WIDTH` | int(11) | S | Largura máxima (px). |  |  |
| `MIN_HEIGHT` | int(11) | S | Altura mínima (px). |  |  |
| `MIN_WIDTH` | int(11) | S | Largura mínima (px). |  |  |
| `PRODUCT` | varchar(255) | S | Produto associado à aplicação (texto livre). |  |  |
| `APPLICATION_RENDERER` | varchar(40) | N | Renderizador usado para exibir a aplicação. |  |  |
| `APPLICATION_TITLE` | varchar(60) | N | Título exibido da aplicação. |  |  |
| `APPLICATION_FILE` | varchar(40) | N | Arquivo principal: themeFile (tema), pageFile (componente), viewFile (widget) ou layoutFile (layout). |  |  |
| `PAGE_DESCRIPTOR` | longtext | S | Descritor de página (LOB) apenas para componentes. |  |  |
| `WIDGET_EDIT_FILE` | varchar(40) | S | Arquivo de edição do widget (editFile); só widgets. |  |  |
| `MOBILEAPP_WIDGET` | bit(1) | S | Indica widget para app mobile; só widgets. | 1=sim; 0/NULL=não |  |
| `UI_WIDGET` | bit(1) | S | Indica widget de UI (uiWidget) ou layout de UI (uiLayout), conforme tipo. | 1=sim; 0/NULL=não |  |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATIONCATEGORY** `(APPLICATION_ID)` · 1:N · physical-fk/confirmed — Categorias.
- `(APPLICATION_ID)` → **WCM_LAYOUTSLOT** `(APPLICATION_ID)` · 1:N · physical-fk/confirmed — Slots de layout.
- `(APPLICATION_ID)` → **WCM_PAGE** `(THEME_ID)` · 1:N · physical-fk/confirmed — Páginas que usam este tema.
- `(APPLICATION_ID)` → **WCM_APPLICATION_APP_DEPENDENCY** `(ID)` · N:1 · hql-join/confirmed — Dataset.findComponentByDatasetDependency

**Dicas de consulta:** Sempre filtre por APPLICATION_TYPE ao buscar temas/widgets/layouts. Sem COD_EMPRESA/tenant. Colunas LOB: EXTENDED_DATA, PAGE_DESCRIPTOR.

## WCM_APPLICATIONCATEGORY

Categoria atribuída a uma aplicação WCM (agrupamento no catálogo de widgets).

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_CATEGORY_ID · **Unique:** (APPLICATION_ID, APPLICATION_CATEGORY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_CATEGORY_ID` | bigint | N | Chave primária. |  |  |
| `APPLICATION_CATEGORY` | varchar(60) | N | Nome/código da categoria. |  |  |
| `APPLICATION_ID` | bigint | N | Aplicação categorizada. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.
- `(APPLICATION_CATEGORY_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · hql-join/confirmed — findGroupedEnabledWidgetsCategoriesByTenant

**Dicas de consulta:** Único por APPLICATION_ID+APPLICATION_CATEGORY.

## WCM_APPLICATIONDATA

Par chave/valor de configuração de uma instância de widget em página (por PAGE_WIDGET_ID), compartilhado entre usuários.

**Ciclo de vida:** Gravada ao salvar preferências do widget.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_DATA_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_DATA_ID` | bigint | N | Chave primária. |  |  |
| `DATA_KEY` | varchar(255) | N | Chave da preferência/configuração. |  |  |
| `DATA_VALUE` | longtext | S | Valor da configuração (LOB). |  |  |
| `PAGE_WIDGET_ID` | bigint | N | Instância de widget na página. |  | WCM_PAGEWIDGET.PAGE_WIDGET_ID |

**Relacionamentos (saem desta tabela):**

- `(PAGE_WIDGET_ID)` → **WCM_PAGEWIDGET** `(PAGE_WIDGET_ID)` · N:1 · physical-fk/confirmed — Instância de widget dona do dado.

**Dicas de consulta:** Versão por usuário em WCM_APPLICATIONUSERDATA.

## WCM_APPLICATIONLOCALE

Locale (idioma) suportado por uma aplicação WCM.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_LOCALE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_LOCALE_ID` | bigint | N | Chave primária. |  |  |
| `APPLICATION_LOCALE_CODE` | varchar(16) | S | Código do locale (ex.: pt_BR), até 16. |  |  |
| `APPLICATION_ID` | bigint | N | Aplicação. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.

## WCM_APPLICATIONPRODUCT

Produto TOTVS ao qual a aplicação WCM está associada (um registro por produto).

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_PRODUCT_ID · **Unique:** (APPLICATION_ID, PRODUCT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_PRODUCT_ID` | bigint | N | Chave primária. |  |  |
| `PRODUCT_CODE` | varchar(32) | N | Código do produto. |  |  |
| `APPLICATION_ID` | bigint | N | Aplicação. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.

**Dicas de consulta:** Único por APPLICATION_ID+PRODUCT_CODE.

## WCM_APPLICATIONRESOURCE

Recurso estático (ex.: CSS/JS) declarado por uma aplicação WCM, com ordem de carga.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_RESOURCE_ID · **Unique:** (APPLICATION_ID, APPLICATION_RESOURCE_TYPE, APPLICATION_RESOURCE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_RESOURCE_ID` | bigint | N | Chave primária. |  |  |
| `RESOURCE_ORDER` | integer | N | Ordem de carga do recurso. |  |  |
| `APPLICATION_RESOURCE` | varchar(255) | N | Caminho/nome do recurso. |  |  |
| `APPLICATION_RESOURCE_TYPE` | varchar(16) | N | Tipo do recurso (ex.: css/js). | não confirmado no código |  |
| `APPLICATION_ID` | bigint | N | Aplicação. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.

**Dicas de consulta:** Único por APPLICATION_ID+TYPE+RESOURCE.

## WCM_APPLICATIONSERVICE

Serviço (EJB/JNDI) exposto à aplicação WCM por nome de variável.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_SERVICE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_SERVICE_ID` | bigint | N | Chave primária. |  |  |
| `APPLICATION_JNDI_NAME` | varchar(255) | N | Nome JNDI do serviço. |  |  |
| `APPLICATION_VAR_NAME` | varchar(16) | N | Nome da variável pela qual o serviço é injetado. |  |  |
| `APPLICATION_ID` | bigint | N | Aplicação. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.

## WCM_APPLICATIONUSERDATA

Par chave/valor de preferência de widget por usuário (LOGIN) e instância (PAGE_WIDGET_ID).

**Ciclo de vida:** Gravada ao usuário personalizar widget.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** APPLICATION_DATA_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `APPLICATION_DATA_ID` | bigint | N | Chave primária. |  |  |
| `DATA_KEY` | varchar(255) | N | Chave da preferência. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor (até 4000). |  |  |
| `LOGIN` | varchar(150) | N | Login do usuário dono da preferência. |  | FDN_USERTENANT.LOGIN |
| `PAGE_WIDGET_ID` | bigint | N | Instância do widget. |  | WCM_PAGEWIDGET.PAGE_WIDGET_ID |

**Relacionamentos (saem desta tabela):**

- `(PAGE_WIDGET_ID)` → **WCM_PAGEWIDGET** `(PAGE_WIDGET_ID)` · N:1 · physical-fk/confirmed — Instância de widget.

**Dicas de consulta:** Dado por usuário: LOGIN.

## WCM_APPLICATION_APP_DEPENDENCY

Vínculo entre aplicação WCM e uma dependência (WCM_APPLICATION_DEPENDENCY), com flag de ativo.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Chave primária. |  |  |
| `APPLICATION_ID` | bigint | N | Aplicação que declara a dependência (jpa: component). |  | WCM_APPLICATION.APPLICATION_ID |
| `DEPENDENCY_ID` | bigint | N | Dependência declarada. |  | WCM_APPLICATION_DEPENDENCY.ID |
| `CREATED_AT` | datetime | N | Data/hora de criação. |  |  |
| `UPDATED_AT` | datetime | S | Data/hora da última atualização. |  |  |
| `ACTIVE` | bit(1) | N | Vínculo ativo. | 1=ativo (default); 0=inativo |  |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · jpa-join/confirmed — Aplicação dona.
- `(DEPENDENCY_ID)` → **WCM_APPLICATION_DEPENDENCY** `(ID)` · N:1 · physical-fk/confirmed — Dependência.
- `(ID)` → **WCM_APPLICATION_DEPENDENCY** `(ID)` · N:1 · hql-join/confirmed — WCMApplicationAppDependency.listByDependencyCode

## WCM_APPLICATION_DEPENDENCY

Dependência (biblioteca/recurso por código e tipo) que aplicações WCM podem declarar, por tenant.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Chave primária. |  |  |
| `CODE` | varchar(255) | N | Código da dependência. |  |  |
| `RESOURCE_TYPE` | varchar(31) | N | Tipo do recurso da dependência. | não confirmado |  |
| `TENANT_ID` | bigint | N | Tenant. |  | FDN_TENANT.TENANT_ID |
| `CREATED_AT` | datetime | N | Criação. |  |  |
| `UPDATED_AT` | datetime | S | Atualização. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.
- `(ID)` → **WCM_APPLICATION_APP_DEPENDENCY** `(ID)` · N:1 · hql-join/confirmed — WCMApplicationDependency.findByTenantIdAndComponentId

**Dicas de consulta:** Filtre por TENANT_ID.

## WCM_COMPONENTPAGE

Associa um componente (aplicação WCM) a uma versão de página.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** COMPONENTPAGE_ID · **Unique:** (APPLICATION_ID, PAGEVERSION_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPONENTPAGE_ID` | bigint | N | Chave primária. |  |  |
| `APPLICATION_ID` | bigint | N | Componente WCM. |  | WCM_APPLICATION.APPLICATION_ID |
| `PAGEVERSION_ID` | bigint | N | Versão de página. |  | WCM_PAGEVERSION.ID |
| `TENANT_ID` | bigint | N | Tenant. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.
- `(PAGEVERSION_ID)` → **WCM_PAGEVERSION** `(ID)` · N:1 · physical-fk/confirmed — Versão de página.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.

**Dicas de consulta:** Único por APPLICATION_ID+PAGEVERSION_ID.

## WCM_CONFIGURATION

Configuração global do portal WCM (layout/tema padrão, URL do servidor, permissões de perfil/espaço).

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** CONFIGURATION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CONFIGURATION_ID` | bigint | N | Chave primária. |  |  |
| `ALLOW_MULTIPLE_ORGANIZATION` | bit | N | Permite múltiplas organizações. | 1=sim; 0=não |  |
| `ALLOW_PERFIL` | bit | N | Permite perfil de usuário. | 1=sim; 0=não |  |
| `ALLOW_SPACE` | bit | N | Permite espaços (comunidades). | 1=sim; 0=não |  |
| `SERVER_URL` | varchar(255) | N | URL base do servidor. |  |  |
| `DEFAULT_LAYOUT_ID` | bigint | S | Layout padrão. |  | WCM_APPLICATION.APPLICATION_ID |
| `DEFAULT_THEME_ID` | bigint | S | Tema padrão. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(DEFAULT_LAYOUT_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Layout padrão.
- `(DEFAULT_THEME_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Tema padrão.

**Dicas de consulta:** Sem coluna de tenant.

## WCM_LAYOUTSLOT

Slot (região) de um layout WCM onde widgets podem ser colocados.

**Ciclo de vida:** Povoada na instalação/publicação da aplicação.

**Atenção:** Filha de WCM_APPLICATION; sem tenant.

**PK:** LAYOUT_SLOT_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `LAYOUT_SLOT_ID` | bigint | N | Chave primária. |  |  |
| `LAYOUT_DECORATOR` | bit | N | Slot é decorador. | 1=sim; 0=não |  |
| `EDITABLE_SLOT` | bit | N | Slot editável. | 1=sim; 0=não |  |
| `LAYOUT_SLOT` | varchar(50) | N | Nome do slot. |  |  |
| `APPLICATION_ID` | bigint | N | Layout (WCM_APPLICATION tipo layout). |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(APPLICATION_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação WCM dona do registro.

## WCM_MENUITEM

Item de menu do portal, hierárquico, que aponta para página ou link externo.

**Ciclo de vida:** Criado/editado pelo administrador do portal.

**Atenção:** Hierarquia por PARENT_MENUITEM_ID.

**PK:** MENUITEM_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `MENUITEM_ID` | bigint | N | Chave primária. |  |  |
| `MENUITEM_AUTH` | integer | N | Autorização de visibilidade (enum MenuAuth). | 0=PUBLIC; 1=AUTHENTICATED; 2=PRIVATE |  |
| `DESCRIPTION` | varchar(120) | S | Descrição. |  |  |
| `DISPLAY_ORDER` | integer | N | Ordem entre irmãos. |  |  |
| `HIDDEN` | bit | N | Oculto. | 1=oculto |  |
| `ICON` | varchar(80) | S | Ícone. |  |  |
| `MENUITEM_LEVEL` | integer | N | Nível na hierarquia. |  |  |
| `OPEN_TARGET` | varchar(80) | N | Target de abertura (ex.: _self). |  |  |
| `OPEN_URL` | varchar(255) | N | URL aberta. |  |  |
| `TITLE` | varchar(60) | N | Título. |  |  |
| `MENUITEM_TYPE` | integer | N | Tipo do item. | 1=PAGE; 2=LINK (WCMMenuItemType) |  |
| `PARENT_MENUITEM_ID` | bigint | S | Item pai. |  | WCM_MENUITEM.MENUITEM_ID |
| `RESOURCE_ID` | bigint | S | Recurso de segurança. |  | FDN_RESOURCE.RESOURCE_ID |

**Relacionamentos (saem desta tabela):**

- `(PARENT_MENUITEM_ID)` → **WCM_MENUITEM** `(MENUITEM_ID)` · N:1 · physical-fk/confirmed — Pai.
- `(RESOURCE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · physical-fk/confirmed — Recurso de segurança.

**Dicas de consulta:** Sem TENANT_ID na tabela (a named query findAllByTenant filtra via recurso).

## WCM_PAGE

Página do portal WCM (hierárquica), com tema, URL amigável e flags de exibição.

**Ciclo de vida:** Criada ao publicar/criar páginas; versões em WCM_PAGEVERSION.

**Atenção:** Único por PAGE_CODE+TENANT_ID.

**PK:** PAGE_ID · **Unique:** (PAGE_CODE, TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PAGE_ID` | bigint | N | Chave primária. |  |  |
| `DEFAULT_LOCALE` | varchar(12) | S | Locale padrão. |  |  |
| `DISABLE_CHILD_LEVEL` | bit | S | Desabilita subníveis. | 1=sim |  |
| `DISPLAY_ORDER` | integer | N | Ordem de exibição. |  |  |
| `EDITABLE` | bit | N | Editável. |  |  |
| `ENABLED` | bit | N | Habilitada. |  |  |
| `FRIENDLY_URL` | varchar(255) | S | URL amigável. |  |  |
| `HIDDEN` | bit | N | Oculta do menu. |  |  |
| `PAGE_LEVEL` | integer | N | Nível hierárquico. |  |  |
| `MENU_GROUP` | bit | S | Funciona como grupo de menu. |  |  |
| `PAGE_CODE` | varchar(40) | N | Código da página. |  |  |
| `PARENT_PAGE_ID` | bigint | S | Página pai. |  | WCM_PAGE.PAGE_ID |
| `RESOURCE_ID` | bigint | S | Recurso de segurança. |  | FDN_RESOURCE.RESOURCE_ID |
| `TENANT_ID` | bigint | N | Tenant. |  | FDN_TENANT.TENANT_ID |
| `THEME_ID` | bigint | S | Tema (WCM_APPLICATION tipo theme). |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(PARENT_PAGE_ID)` → **WCM_PAGE** `(PAGE_ID)` · N:1 · physical-fk/confirmed — Pai.
- `(RESOURCE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · physical-fk/confirmed — Recurso.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.
- `(THEME_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Tema.
- `(PAGE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · hql-join/confirmed — FDNResource.findAllResourcesByFilterWithExcludeListWithoutForbiddenCodes

**Dicas de consulta:** Filtre por TENANT_ID.

## WCM_PAGEDATA

Par chave/valor de dados de uma versão de página.

**Ciclo de vida:** Gravada ao salvar a página.

**Atenção:** Único por PAGEVERSION_ID+DATA_KEY.

**PK:** PAGE_DATA_ID · **Unique:** (PAGEVERSION_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PAGE_DATA_ID` | bigint | N | Chave primária. |  |  |
| `DATA_KEY` | varchar(255) | N | Chave. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor (até 4000). |  |  |
| `PAGEVERSION_ID` | bigint | N | Versão de página. |  | WCM_PAGEVERSION.ID |

**Relacionamentos (saem desta tabela):**

- `(PAGEVERSION_ID)` → **WCM_PAGEVERSION** `(ID)` · N:1 · physical-fk/confirmed — Versão de página.
