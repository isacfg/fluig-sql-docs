# Domínio: volumes-sites

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_DOWNLOADNOTIFY

Usuários a notificar quando um item da fila de download de site (FDN_SITEDOWNLOADQUEUE) concluir. Liga item da fila a usuário.

**Ciclo de vida:** Criada ao solicitar download; removida após a notificação ou fim da fila.

**Atenção:** Sem tenant direto.

**PK:** DOWNLOADNOTIFY_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DOWNLOADNOTIFY_ID` | bigint(20) | N | Chave primária. |  |  |
| `QUEUE_ID` | bigint(20) | N | Item da fila de download a ser notificado. |  | FDN_SITEDOWNLOADQUEUE.QUEUE_ID |
| `USERTENANT_ID` | bigint(20) | N | Usuário a notificar (FDN_USERTENANT). |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(QUEUE_ID)` → **FDN_SITEDOWNLOADQUEUE** `(QUEUE_ID)` · N:1 · physical-fk/confirmed — Item da fila.
- `(USERTENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · jpa-join/confirmed — Usuário a notificar.

**Dicas de consulta:** Consulta típica: findByQueueAndUser.

## FDN_SITE

Sites (servidores/sites de volume) usados na replicação e download de arquivos, com URL, limites de cópia e stream e tentativas máximas.

**Ciclo de vida:** Cadastro administrativo; baixo volume.

**Atenção:** findLocalSite obtém o site local. Pode ser vinculado a FDN_LOCAL. SITE_CODE é usado em buscas.

**PK:** SITE_ID · **Unique:** (TENANT_ID, SITE_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `SITE_ID` | bigint(20) | N | Chave primária do site. |  |  |
| `ACTIVE` | bit(1) | S | Indica site ativo (inactivate o desativa). | 1=ativo; 0=inativo |  |
| `COPY_LIMIT` | int(11) | S | Limite de cópias simultâneas. |  |  |
| `MAXIMUM_RETRIES` | int(11) | S | Número máximo de tentativas em caso de falha. |  |  |
| `SITE_CODE` | varchar(150) | N | Código único do site. |  |  |
| `SITE_URL` | varchar(400) | N | URL do site (até 400 caracteres). |  |  |
| `STREAM_LIMIT` | int(11) | S | Limite de streams simultâneos. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant dono do site. |  | FDN_TENANT.TENANT_ID |
| `LOCAL_ID` | bigint(20) | S | Local (FDN_LOCAL) associado ao site; anulável. |  | FDN_LOCAL.ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant do site.
- `(LOCAL_ID)` → **FDN_LOCAL** `(ID)` · N:1 · jpa-join/confirmed — Local do site (FK_SITELOCAL).

**Dicas de consulta:** Filtrar por TENANT_ID.

## FDN_SITEDOWNLOADQUEUE

Fila de downloads de arquivos de documentos entre sites. Cada linha é uma transferência de uma versão de documento para o site do usuário.

**Ciclo de vida:** Inserida ao agendar o download; atualizada com progresso, status e fim; itens concluídos/erros podem permanecer.

**Atenção:** QUEUE_STATUS = enum FDNDownloadQueueStatus: 1=SCHEDULED; 2=PAUSED; 3=DOWNLOADING; 4=FORCE_DOWNLOADING; 5=ERROR; 6=COMPLETED. Sem TENANT_ID; o tenant vem de USER_SITE_ID -> FDN_SITE.

**PK:** QUEUE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `QUEUE_ID` | bigint(20) | N | Chave primária do item da fila. |  |  |
| `DOCUMENT_ID` | bigint(20) | N | Id do documento a baixar. |  | DOCUMENTO.NR_DOCUMENTO |
| `END_DATE` | datetime | S | Data/hora do fim do download. |  |  |
| `ERROR_LOG` | varchar(255) | S | Mensagem de erro do último fracasso (até 255 caracteres). |  |  |
| `FILE_SITE_ID` | bigint(20) | N | Site de origem onde o arquivo está. |  | FDN_SITE.SITE_ID |
| `FILE_SIZE` | float | S | Tamanho do arquivo (unidade não confirmada). |  |  |
| `FILE_STREAM` | varchar(1024) | N | Caminho/identificador do stream de origem do arquivo. |  |  |
| `OUTPUT_FILE` | varchar(1024) | N | Caminho do arquivo de destino. |  |  |
| `QUEU_PRIORITY` | int(11) | N | Prioridade na fila; menor valor primeiro (ordenado ASC). |  |  |
| `PROGRESS` | float | S | Progresso do download (percentual ou fração, unidade não confirmada). |  |  |
| `SCHEDELED_TIME` | bigint(20) | S | Instante agendado em milissegundos epoch (nome com grafia original). |  |  |
| `STARTED_TIME` | bigint(20) | S | Instante de início em milissegundos epoch. |  |  |
| `QUEUE_STATUS` | int(11) | N | Status do item (enum FDNDownloadQueueStatus). | 1=SCHEDULED; 2=PAUSED; 3=DOWNLOADING; 4=FORCE_DOWNLOADING; 5=ERROR; 6=COMPLETED |  |
| `USER_ID` | varchar(255) | S | Identificador do usuário solicitante, em texto. |  | FDN_USERTENANT.USER_CODE |
| `USER_SITE_ID` | bigint(20) | N | Site do usuário (destino do download). |  | FDN_SITE.SITE_ID |
| `DOCUMENT_VERSION` | bigint(20) | N | Versão do documento a baixar. |  |  |

**Relacionamentos (saem desta tabela):**

- `(USER_SITE_ID)` → **FDN_SITE** `(SITE_ID)` · N:1 · physical-fk/confirmed — Site de destino do usuário.
- `(FILE_SITE_ID)` → **FDN_SITE** `(SITE_ID)` · N:1 · jpa-join/confirmed — Site de origem do arquivo.
- `(QUEUE_ID)` → **FDN_DOWNLOADNOTIFY** `(QUEUE_ID)` · 1:N · physical-fk/confirmed — Notificações do item.

**Dicas de consulta:** Para ativos: QUEUE_STATUS != 6 (COMPLETED).
