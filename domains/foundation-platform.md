# Domínio: foundation-platform

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_SITESCHEDULER

Janelas de agendamento (início/fim) associadas a um site do Fluig; usada por consulta FDNSiteScheduler.findBySite.

**Ciclo de vida:** Linhas criadas ao agendar um período para um site; volume baixo.

**Atenção:** Sem coluna de tenant: o tenant vem via FDN_SITE.

**PK:** SITESCHEDULER_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `SITESCHEDULER_ID` | bigint(20) | N | PK surrogate do agendamento do site. |  |  |
| `END_TIME` | bigint(20) | N | Fim do agendamento, epoch em milissegundos (Long). |  |  |
| `SITE_ID` | bigint(20) | N | Site ao qual o agendamento pertence. |  | FDN_SITE.SITE_ID |
| `START_TIME` | bigint(20) | N | Início do agendamento, epoch em milissegundos (Long). |  |  |

**Relacionamentos (saem desta tabela):**

- `(SITE_ID)` → **FDN_SITE** `(SITE_ID)` · N:1 · physical-fk/confirmed — Site dono do agendamento (FK FK_9314CU0VGYY7PXECBECEIJPM8; JPA FDNSiteScheduler.site).

**Dicas de consulta:** Filtrar por SITE_ID; para tenant fazer join com FDN_SITE.

## FDN_UPDATE_HOTFIX

Registro de updates/hotfixes aplicados à instalação do Fluig, com código, data de criação e usuário que aplicou.

**Ciclo de vida:** Uma linha por update/hotfix aplicado; volume muito baixo.

**Atenção:** Sem tenant; é global da instalação.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | PK surrogate do registro de hotfix. |  |  |
| `COD_UPDATE` | varchar(255) | N | Código/identificador do update ou hotfix aplicado. |  |  |
| `UPDATE_CREATION_DATE` | date | S | Data de criação do update/hotfix (somente data). |  |  |
| `USER_UPDATE` | varchar(255) | N | Usuário que aplicou/registrou o update (texto livre, não FK). |  |  |

**Dicas de consulta:** Tabela global; consulta via UpdateHotfixEntity.findUpdateHotfix.

## FDN_VOLUME

Volumes de armazenamento de arquivos (GED/documentos) por tenant, com capacidade máxima e espaço usado.

**Ciclo de vida:** Criados na configuração do tenant; USED_SPACE é atualizado via UPDATE (addUsedSpace/removeDeletedSpace) a cada upload/remoção.

**Atenção:** VOLUME_TYPE=0 casa com qualquer tipo (findByType usa volumeType = :type OR volumeType = 0). Há unique key (artefato UNIQUE) provavelmente sobre tenant+código.

**PK:** VOLUME_ID · **Unique:** (TENANT_ID, VOLUME_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `VOLUME_ID` | bigint(20) | N | PK surrogate do volume. |  |  |
| `DOCUMENT_ID` | int(11) | S | Documento do GED associado ao volume (opcional). |  | DOCUMENT.DOCUMENT_ID |
| `MAX_SIZE` | float | N | Capacidade máxima do volume (float; unidade provavelmente bytes ou MB). |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant dono do volume. |  | FDN_TENANT.TENANT_ID |
| `USED_SPACE` | float | N | Espaço já utilizado no volume (float, mesma unidade de MAX_SIZE); incrementado/decrementado por UPDATE. |  |  |
| `VOLUME_CODE` | varchar(150) | N | Código textual do volume, único por tenant; usado para localizar o volume. |  |  |
| `VOLUME_TYPE` | int(11) | N | Tipo do volume; 0 serve como curinga para qualquer tipo. | 0=curinga (qualquer tipo); demais valores não confirmados |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant dono do volume.
- `(VOLUME_ID)` → **FDN_VOLUMESITE** `(VOLUME_ID)` · 1:N · jpa-join/confirmed — Mapeamentos do volume para sites com caminho de storage.

**Dicas de consulta:** Sempre filtrar por TENANT_ID. Atualizar USED_SPACE só via mecanismo da aplicação.

## FDN_VOLUMESITE

Associa um volume de armazenamento a um site, informando o caminho físico (STORAGE) usado por esse site naquele volume.

**Ciclo de vida:** Criada ao vincular site a volume; volume baixo.

**Atenção:** Unique key (artefato UNIQUE), provavelmente VOLUME_ID+SITE_ID. Sem coluna de tenant: use FDN_SITE/FDN_VOLUME.

**PK:** VOLUMESITE_ID · **Unique:** (VOLUME_ID, SITE_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `VOLUMESITE_ID` | bigint(20) | N | PK surrogate do vínculo volume-site. |  |  |
| `SITE_ID` | bigint(20) | N | Site vinculado ao volume. |  | FDN_SITE.SITE_ID |
| `STORAGE` | varchar(400) | N | Caminho de armazenamento (path) do site dentro do volume. |  |  |
| `VOLUME_ID` | bigint(20) | N | Volume vinculado ao site. |  | FDN_VOLUME.VOLUME_ID |

**Relacionamentos (saem desta tabela):**

- `(VOLUME_ID)` → **FDN_VOLUME** `(VOLUME_ID)` · N:1 · jpa-join/confirmed — Volume vinculado (FDNVolumeSite.volume).
- `(SITE_ID)` → **FDN_SITE** `(SITE_ID)` · N:1 · physical-fk/confirmed — Site vinculado.

**Dicas de consulta:** Join típico: FDN_VOLUMESITE -> FDN_VOLUME para obter TENANT_ID e VOLUME_CODE.
