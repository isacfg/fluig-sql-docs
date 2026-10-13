# Domínio: permissoes-categorias

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_CATEGORY

Categorias hierárquicas usadas para agrupar recursos (FDN_RESOURCE) no modelo de permissões. Cada linha é uma categoria, possivelmente filha de outra.

**Ciclo de vida:** Criadas por módulos/administração; baixo volume.

**Atenção:** Hierarquia por PARENT_CATEGORY_ID (auto-relação). IS_INTERNAL e IS_HIDDEN controlam visibilidade (findByTenantAndIdIncludeHidden inclui ocultas). TENANT_ID é anulável.

**PK:** CATEGORY_ID · **Unique:** (TENANT_ID, CATEGORY_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CATEGORY_ID` | bigint(20) | N | Chave primária da categoria. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant dono da categoria. |  | FDN_TENANT.TENANT_ID |
| `PARENT_CATEGORY_ID` | bigint(20) | S | Categoria pai na hierarquia; nulo para categoria raiz. |  | FDN_CATEGORY.CATEGORY_ID |
| `CATEGORY_CODE` | varchar(128) | N | Código único da categoria, usado em findByCode. |  |  |
| `CATEGORY_NAME` | varchar(128) | N | Nome de exibição da categoria. |  |  |
| `DESCRIPTION` | varchar(255) | S | Descrição livre da categoria. |  |  |
| `ICON_URL` | varchar(255) | S | URL/caminho do ícone da categoria. |  |  |
| `IS_INTERNAL` | bit(1) | N | Indica categoria interna do sistema (não criada pelo usuário). | 1=interna; 0=não interna |  |
| `IS_HIDDEN` | bit(1) | N | Indica categoria oculta nas listagens padrão. | 1=oculta; 0=visível |  |

**Relacionamentos (saem desta tabela):**

- `(PARENT_CATEGORY_ID)` → **FDN_CATEGORY** `(CATEGORY_ID)` · N:1 · jpa-join/probable — Categoria pai (auto-relação hierárquica); inferida por nome da coluna e query findByParent.
- `(CATEGORY_ID)` → **FDN_CATEGORY_RESOURCE** `(CATEGORY_ID)` · 1:N · physical-fk/confirmed — Recursos vinculados à categoria.

**Dicas de consulta:** Filtrar por TENANT_ID; use IS_HIDDEN=0 para listagens de usuário.

## FDN_CATEGORY_RESOURCE

Tabela de associação entre categorias (FDN_CATEGORY) e recursos (FDN_RESOURCE). Cada linha vincula um recurso a uma categoria.

**Ciclo de vida:** Criada ao categorizar recursos; remoção ao descategorizar.

**Atenção:** Associação N:M com id próprio. RESOURCE_ID não tem FK física, apenas join JPA.

**PK:** CATEGORY_RESOURCE_ID · **Unique:** (CATEGORY_ID, RESOURCE_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CATEGORY_RESOURCE_ID` | bigint(20) | N | Chave primária da associação. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant da associação. |  | FDN_TENANT.TENANT_ID |
| `RESOURCE_ID` | bigint(20) | S | Recurso categorizado. |  | FDN_RESOURCE.RESOURCE_ID |
| `CATEGORY_ID` | bigint(20) | S | Categoria à qual o recurso pertence. |  | FDN_CATEGORY.CATEGORY_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · jpa-join/confirmed — Recurso categorizado.
- `(CATEGORY_ID)` → **FDN_CATEGORY** `(CATEGORY_ID)` · N:1 · physical-fk/confirmed — Categoria do recurso (FK_CATEGORYOFRESOURCE).

**Dicas de consulta:** Filtrar por TENANT_ID; join com FDN_CATEGORY e FDN_RESOURCE.
