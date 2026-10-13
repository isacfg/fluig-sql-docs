# Domínio: wcm-resources

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## WCM_RESOURCECOMPONENT

Catálogo de componentes de recursos estáticos (bibliotecas JS/CSS) identificados por código, que temas/widgets podem referenciar.

**Ciclo de vida:** Carga de catálogo, poucas linhas, raramente alterada.

**Atenção:** Código único global (sem tenant).

**PK:** RESOURCE_COMPONENT_ID · **Unique:** (RESOURCE_COMPONENT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_COMPONENT_ID` | bigint | N | PK surrogate do componente de recurso. |  |  |
| `RESOURCE_COMPONENT_CODE` | varchar(25) | N | Código único do componente (até 25 caracteres), usado para buscar via findByCode. |  |  |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_COMPONENT_ID)` → **WCM_RESOURCECOMPONENTFILE** `(RESOURCE_COMPONENT_ID)` · 1:N · physical-fk/confirmed — Arquivos que compõem o componente.

**Dicas de consulta:** Buscar por RESOURCE_COMPONENT_CODE; arquivos em WCM_RESOURCECOMPONENTFILE.

## WCM_RESOURCECOMPONENTFILE

Arquivos (JS/CSS etc.) pertencentes a um componente de recurso, com tipo, caminho e ordem de carga.

**Ciclo de vida:** Carga de catálogo junto com o componente; poucas linhas.

**Atenção:** Unique (RESOURCE_COMPONENT_ID, RESOURCE_TYPE, RESOURCE_PATH).

**PK:** RESOURCE_COMPONENT_FILE_ID · **Unique:** (RESOURCE_COMPONENT_ID, RESOURCE_TYPE, RESOURCE_PATH)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_COMPONENT_FILE_ID` | bigint | N | PK surrogate do arquivo. |  |  |
| `RESOURCE_ORDER` | integer | N | Ordem de carga do arquivo dentro do componente. |  |  |
| `RESOURCE_PATH` | varchar(255) | N | Caminho/URL do arquivo do recurso. |  |  |
| `RESOURCE_TYPE` | varchar(16) | N | Tipo do recurso (String livre até 16 caracteres, ex.: tipo de arquivo JS/CSS). |  |  |
| `RESOURCE_COMPONENT_ID` | bigint | N | Componente dono do arquivo. |  | WCM_RESOURCECOMPONENT.RESOURCE_COMPONENT_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_COMPONENT_ID)` → **WCM_RESOURCECOMPONENT** `(RESOURCE_COMPONENT_ID)` · N:1 · physical-fk/confirmed — Componente dono do arquivo.

**Dicas de consulta:** Named query findByComponent. Ordenar por RESOURCE_ORDER para carga.

## WCM_RESOURCEKIT

Catálogo de kits de recursos estáticos (conjuntos de arquivos) identificados por código.

**Ciclo de vida:** Carga de catálogo, poucas linhas.

**Atenção:** Código único global (sem tenant).

**PK:** RESOURCE_KIT_ID · **Unique:** (RESOURCE_KIT_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_KIT_ID` | bigint | N | PK surrogate do kit. |  |  |
| `RESOURCE_KIT_CODE` | varchar(16) | N | Código único do kit (até 16 caracteres). |  |  |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_KIT_ID)` → **WCM_RESOURCEKITFILE** `(RESOURCE_KIT_ID)` · 1:N · physical-fk/confirmed — Arquivos do kit.

**Dicas de consulta:** Buscar por RESOURCE_KIT_CODE.

## WCM_RESOURCEKITFILE

Arquivos que compõem um kit de recursos, com tipo, caminho e ordem.

**Ciclo de vida:** Carga de catálogo; poucas linhas.

**Atenção:** Unique (RESOURCE_KIT_ID, RESOURCE_TYPE, RESOURCE_PATH).

**PK:** RESOURCE_KIT_FILE_ID · **Unique:** (RESOURCE_KIT_ID, RESOURCE_TYPE, RESOURCE_PATH)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_KIT_FILE_ID` | bigint | N | PK surrogate do arquivo do kit. |  |  |
| `RESOURCE_ORDER` | integer | N | Ordem de carga do arquivo no kit. |  |  |
| `RESOURCE_PATH` | varchar(255) | N | Caminho/URL do arquivo do recurso. |  |  |
| `RESOURCE_TYPE` | varchar(16) | N | Tipo do recurso (String livre até 16 caracteres, ex.: JS/CSS). |  |  |
| `RESOURCE_KIT_ID` | bigint | N | Kit dono do arquivo. |  | WCM_RESOURCEKIT.RESOURCE_KIT_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_KIT_ID)` → **WCM_RESOURCEKIT** `(RESOURCE_KIT_ID)` · N:1 · physical-fk/confirmed — Kit dono do arquivo.

**Dicas de consulta:** Named query findByKit.
