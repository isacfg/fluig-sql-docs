# Domínio: foundation-tenancy

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_PRODUCT

Catálogo de produtos TOTVS/Fluig que podem ser habilitados para um tenant.

**Ciclo de vida:** Populada na instalação/atualização; poucas linhas.

**Atenção:** PRODUCT_CODE é a chave de negócio usada por FDN_TENANTPRODUCT.PRODUCT_CODE.

**PK:** PRODUCT_ID · **Unique:** (PRODUCT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PRODUCT_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `PRODUCT_CODE` | varchar(32) | N | Código do produto (chave de negócio, único). |  |  |
| `PRODUCT_NAME` | varchar(132) | N | Nome exibido do produto. |  |  |

**Relacionamentos (saem desta tabela):**

- `(PRODUCT_CODE)` → **FDN_TENANTPRODUCT** `(PRODUCT_CODE)` · 1:N · logical-probable/probable — Produtos habilitados por tenant referenciam este código (FDNTenantProduct.product é String sem FK).

**Dicas de consulta:** Tabela de domínio pequena.

## FDN_TENANT

Tenant (empresa/organização) do Fluig; raiz da multi-tenancy, referenciada por quase todas as tabelas.

**Ciclo de vida:** Criado na instalação ou provisionamento; poucas linhas.

**Atenção:** TENANT_CODE é a chave de negócio. Unique key provável em TENANT_CODE. Quase toda tabela do Fluig filtra por TENANT_ID.

**PK:** TENANT_ID · **Unique:** (TENANT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TENANT_ID` | bigint(20) | N | Chave primária do tenant, usada como TENANT_ID em todo o sistema. |  |  |
| `TENANT_UUID` | varchar(36) | S | UUID do tenant. |  |  |
| `TENANT_CODE` | varchar(32) | N | Código curto do tenant (chave de negócio). |  |  |
| `DESCRIPTION` | varchar(255) | N | Nome/descrição da organização. |  |  |
| `FEDERAL_ID` | varchar(50) | N | Identificador federal (ex.: CNPJ) da organização. |  |  |
| `IDP_ID` | varchar(255) | S | Identificador do provedor de identidade (IdP) externo associado. |  |  |
| `IDP_LOGOFF` | bit(1) | S | Indica se o logoff deve ser propagado ao IdP. | 1=propaga logoff ao IdP; 0=não |  |
| `ORGANIZATION_URL` | varchar(255) | N | URL da organização/instância do tenant. |  |  |
| `REMOVE_VOLUME` | bit(1) | N | Indica remoção do volume de arquivos ao remover o tenant. | 1=remover volume; 0=manter |  |
| `TENANT_ACTIVE` | bit(1) | N | Indica tenant ativo. | 1=ativo; 0=inativo |  |
| `THUMBNAIL_ENABLED` | bit(1) | N | Habilita geração de thumbnails para o tenant. | 1=habilitado; 0=desabilitado |  |
| `USE_WIZARD` | bit(1) | S | Indica uso do wizard inicial de configuração. | 1=usa wizard; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANTDATA** `(TENANT_ID)` · 1:N · jpa-join/confirmed — Propriedades do tenant.
- `(TENANT_ID)` → **FDN_TENANTPRODUCT** `(TENANT_ID)` · 1:N · jpa-join/confirmed — Produtos habilitados.
- `(TENANT_ID)` → **FDN_USERTENANT** `(TENANT_ID)` · 1:N · jpa-join/confirmed — Usuários do tenant.

**Dicas de consulta:** Tabela raiz de tenancy. Contém FEDERAL_ID (CNPJ), dado de identificação da organização.

## FDN_TENANTDATA

Parâmetros/propriedades chave/valor de configuração do tenant.

**Ciclo de vida:** Criadas na configuração do tenant e alteradas por administração; volume médio.

**Atenção:** Padrão EAV; HIDE marca valores ocultos na UI (potencialmente sensíveis).

**PK:** TENANTDATA_ID · **Unique:** (TENANT_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TENANTDATA_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DATA_KEY` | varchar(255) | N | Nome do parâmetro de configuração do tenant. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor do parâmetro (até 4000 chars); pode conter segredos quando HIDE=1. |  |  |
| `HIDE` | bit(1) | S | Indica valor oculto (não exibido na interface). | 1=oculto; 0=visível |  |
| `TENANT_ID` | bigint(20) | N | Tenant dono do parâmetro. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.

**Dicas de consulta:** Filtre por TENANT_ID e DATA_KEY. Linhas com HIDE=1 podem conter segredos.

## FDN_TENANTPRODUCT

Associação tenant-produto: quais produtos (FDN_PRODUCT) estão habilitados em cada tenant.

**Ciclo de vida:** Criada no provisionamento/licenciamento; poucas linhas por tenant.

**Atenção:** Associa por PRODUCT_CODE (string) sem FK para FDN_PRODUCT.

**PK:** TENANTPRODUCT_ID · **Unique:** (TENANT_ID, PRODUCT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TENANTPRODUCT_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `PRODUCT_CODE` | varchar(32) | N | Código do produto habilitado. |  | FDN_PRODUCT.PRODUCT_CODE |
| `TENANT_ID` | bigint(20) | N | Tenant que possui o produto. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.
- `(PRODUCT_CODE)` → **FDN_PRODUCT** `(PRODUCT_CODE)` · N:1 · logical-probable/probable — Produto referenciado por código.
