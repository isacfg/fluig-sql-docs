# Domínio: wcm-portal-pages

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_PAGEVERSION

Versão de uma página do portal WCM (título, ícone, layout, autorização, publicação). Cada edição/publicação gera nova versão ligada a WCM_PAGE.

**Ciclo de vida:** Linha criada a cada nova versão de página; PUBLISHED marca a versão ativa. Cresce com o histórico de edições.

**Atenção:** Sem coluna de tenant: o tenant vem via WCM_PAGE. Versionamento por VERSION (sequencial por página). A versão corrente é a com PUBLISHED=1.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | PK surrogate da versão da página (gerada, GenerationType.AUTO). |  |  |
| `AUTH` | integer | N | Nível de autorização de acesso à página (enum PageAuth gravado como ordinal). | 0=PUBLIC; 1=AUTHENTICATED; 2=PRIVATE (ordem do enum PageAuth, EnumType.ORDINAL) |  |
| `DESCRIPTION` | varchar(255) | S | Descrição curta da página nesta versão. |  |  |
| `ENABLED_CHILDREN` | bit | N | Indica se a página aceita páginas filhas (hierarquia). | 1=habilitado; 0=não |  |
| `ENABLED_MOBILEAPP` | bit | N | Indica se a página é exibida no aplicativo mobile. | 1=habilitado; 0=não |  |
| `ENABLED_PATHPARAM` | bit | N | Indica se a página aceita parâmetros no path da URL. | 1=habilitado; 0=não |  |
| `ICON` | varchar(80) | S | Nome/caminho do ícone da página (até 80 caracteres). |  |  |
| `ICONFONT` | varchar(255) | S | Classe de ícone de fonte (icon font) da página. |  |  |
| `DATE_MODIFIED` | datetime | N | Data/hora da última modificação desta versão. |  |  |
| `PUBLISHED` | bit | N | Indica se esta é a versão publicada (ativa) da página. | 1=publicada; 0=rascunho/antiga |  |
| `TITLE` | varchar(255) | N | Título da página exibido no portal. |  |  |
| `VERSION` | bigint | N | Número sequencial da versão dentro da página (imutável, updatable=false). |  |  |
| `VERSION_DESCRIPTION` | varchar(4000) | S | Texto livre descrevendo as mudanças desta versão (até 4000). |  |  |
| `LAST_EDIT_USER` | bigint | S | Usuário que fez a última edição (FK para FDN_USERTENANT). |  | FDN_USERTENANT.USER_TENANT_ID |
| `LAYOUT_ID` | bigint | N | Layout da página: aplicação WCM do tipo layout. |  | WCM_APPLICATION.APPLICATION_ID |
| `PAGE_ID` | bigint | N | Página pai a que a versão pertence. |  | WCM_PAGE.PAGE_ID |

**Relacionamentos (saem desta tabela):**

- `(LAST_EDIT_USER)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Último usuário que editou a versão.
- `(LAYOUT_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Layout (aplicação WCM) usado pela página.
- `(PAGE_ID)` → **WCM_PAGE** `(PAGE_ID)` · N:1 · physical-fk/confirmed — Página a que a versão pertence (também mapeada como jpa-join WCMPageVersion.page).
- `(ID)` → **WCM_PAGEWIDGET** `(PAGEVERSION_ID)` · 1:N · jpa-join/confirmed — Widgets posicionados nesta versão (OneToMany mappedBy pageVersion).

**Dicas de consulta:** Para a versão vigente de uma página: WHERE PAGE_ID=? AND PUBLISHED=1. Índice WCMPAGEVERSION001 (ID,PAGE_ID,PUBLISHED). Filtrar tenant via WCM_PAGE.

## WCM_PAGEWIDGET

Posicionamento de um widget (aplicação WCM) em um slot de uma versão de página.

**Ciclo de vida:** Linhas criadas ao salvar a composição de uma versão de página; novas versões copiam os widgets.

**Atenção:** Unique (PAGEVERSION_ID, SLOT, WIDGET_ORDER) garante ordem única por slot.

**PK:** PAGE_WIDGET_ID · **Unique:** (PAGEVERSION_ID, SLOT, WIDGET_ORDER)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PAGE_WIDGET_ID` | bigint | N | PK surrogate do widget na página. |  |  |
| `ENABLED_MOBILEAPP` | bit | N | Indica se o widget aparece no app mobile. | 1=sim; 0=não |  |
| `SHOW_TITLEBAR` | bit | N | Indica se a barra de título do widget é exibida. | 1=exibe; 0=oculta |  |
| `SLOT` | varchar(60) | N | Nome do slot (área) do layout onde o widget é renderizado. |  |  |
| `SYSTEM_WIDGET` | bit | N | Indica widget de sistema (fixo, não removível pelo usuário). | 1=sistema; 0=comum |  |
| `WIDGET_ORDER` | bigint | N | Ordem de exibição do widget dentro do slot. |  |  |
| `PAGEVERSION_ID` | bigint | N | Versão de página que contém o widget. |  | WCM_PAGEVERSION.ID |
| `WIDGET_ID` | bigint | N | Aplicação WCM (widget) instanciada. |  | WCM_APPLICATION.APPLICATION_ID |

**Relacionamentos (saem desta tabela):**

- `(PAGEVERSION_ID)` → **WCM_PAGEVERSION** `(ID)` · N:1 · physical-fk/confirmed — Versão da página dona do widget.
- `(WIDGET_ID)` → **WCM_APPLICATION** `(APPLICATION_ID)` · N:1 · physical-fk/confirmed — Aplicação/widget colocado no slot.

**Dicas de consulta:** Named queries: findAll, findPagesByWidget (páginas que usam um widget), findById. Join típico: PAGEVERSION_ID -> WCM_PAGEVERSION.ID -> PAGE_ID.
