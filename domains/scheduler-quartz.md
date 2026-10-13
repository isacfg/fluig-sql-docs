# Domínio: scheduler-quartz

12 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## QRTZ_BLOB_TRIGGERS

Tabela padrão do Quartz para triggers de tipo customizado serializados em BLOB.

**Ciclo de vida:** Normalmente vazia (Fluig usa cron/simple).

**Atenção:** Sem FK física para QRTZ_TRIGGERS neste schema.

**PK:** TRIGGER_GROUP, TRIGGER_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Nome do grupo do trigger Quartz; compõe a PK (TRIGGER_GROUP, TRIGGER_NAME) e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| 🔑 `TRIGGER_NAME` | varchar(255) | N | Nome do trigger Quartz dentro do grupo; compõe a PK e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_NAME |
| `BLOB_DATA` | longblob | S | Dados serializados (BLOB) de triggers customizados que o Quartz não persiste em tabela própria. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TRIGGER_GROUP, TRIGGER_NAME)` → **QRTZ_TRIGGERS** `(TRIGGER_GROUP, TRIGGER_NAME)` · 1:1 · logical-confirmed/probable — Detalhe do trigger tipo BLOB; mesma PK de QRTZ_TRIGGERS (sem FK física no schema).

**Dicas de consulta:** Tabela de infraestrutura do Quartz; não alterar manualmente.

## QRTZ_CALENDARS

Calendários Quartz serializados que excluem períodos de disparo de triggers.

**Ciclo de vida:** Poucas linhas; geralmente vazia.

**PK:** CALENDAR_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CALENDAR_NAME` | varchar(255) | N | Nome do calendário Quartz (PK); referenciado por QRTZ_TRIGGERS.CALENDAR_NAME. |  |  |
| `CALENDAR` | longblob | N | Objeto Calendar do Quartz serializado (binário Java). |  |  |

**Dicas de consulta:** Infraestrutura Quartz; CALENDAR é binário Java.

## QRTZ_CRON_TRIGGERS

Detalhe de triggers do Quartz baseados em expressão cron, 1:1 com QRTZ_TRIGGERS.

**Ciclo de vida:** Criada junto com o trigger cron ao agendar job.

**Atenção:** Sem tenant: scheduler é global ao cluster (tenant fica no nome/grupo/JobDataMap).

**PK:** TRIGGER_GROUP, TRIGGER_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Nome do grupo do trigger Quartz; compõe a PK (TRIGGER_GROUP, TRIGGER_NAME) e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| 🔑 `TRIGGER_NAME` | varchar(255) | N | Nome do trigger Quartz dentro do grupo; compõe a PK e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_NAME |
| `CRON_EXPRESSION` | varchar(255) | N | Expressão cron do Quartz (formato com segundos) que define a recorrência do trigger. |  |  |
| `TIME_ZONE_ID` | varchar(255) | S | ID do fuso horário (ex.: America/Sao_Paulo) usado para avaliar a expressão cron; pode ser nulo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TRIGGER_GROUP, TRIGGER_NAME)` → **QRTZ_TRIGGERS** `(TRIGGER_GROUP, TRIGGER_NAME)` · 1:1 · logical-confirmed/probable — Detalhe cron do trigger; mesma PK de QRTZ_TRIGGERS.

**Dicas de consulta:** JOIN com QRTZ_TRIGGERS por (TRIGGER_GROUP, TRIGGER_NAME).

## QRTZ_FIRED_TRIGGERS

Registro transitório de triggers em execução/adquiridos pelos nós do scheduler.

**Ciclo de vida:** Inserida ao adquirir o trigger e removida ao concluir; poucas linhas.

**Atenção:** Linhas órfãs podem ficar após queda de nó; Quartz limpa na recuperação.

**PK:** ENTRY_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ENTRY_ID` | varchar(255) | N | Identificador único da execução em andamento (instância + contador); PK. |  |  |
| `FIRED_TIME` | decimal(19,2) | N | Instante em que o trigger disparou, em milissegundos desde epoch. |  |  |
| `INSTANCE_NAME` | varchar(255) | N | Nome da instância do scheduler (nó do cluster) que está executando o disparo. |  | QRTZ_SCHEDULER_STATE.INSTANCE_NAME |
| `IS_STATEFUL` | bit | S | Legado Quartz 1.x: job stateful (não concorrente). Nulo em linhas novas. |  |  |
| `IS_VOLATILE` | bit | N | Legado Quartz 1.x: trigger volátil (não persistido entre reinícios). |  |  |
| `JOB_GROUP` | varchar(255) | S | Grupo do job disparado; nulo se o job não exige não-concorrência. |  | QRTZ_JOB_DETAILS.JOB_GROUP |
| `JOB_NAME` | varchar(255) | S | Nome do job disparado; nulo se o job não exige não-concorrência. |  | QRTZ_JOB_DETAILS.JOB_NAME |
| `PRIORITY` | integer | S | Prioridade do trigger no momento do disparo (inteiro; maior executa primeiro). |  |  |
| `REQUESTS_RECOVERY` | bit | S | Indica se o job deve ser reexecutado se a instância cair durante a execução. |  |  |
| `STATE` | varchar(255) | N | Estado da execução no Quartz (ex.: EXECUTING, ACQUIRED, BLOCKED); valores não enumerados no código do Fluig. |  |  |
| `TRIGGER_GROUP` | varchar(255) | N | Grupo do trigger disparado. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| `TRIGGER_NAME` | varchar(255) | N | Nome do trigger disparado. |  | QRTZ_TRIGGERS.TRIGGER_NAME |

**Relacionamentos (saem desta tabela):**

- `(TRIGGER_GROUP, TRIGGER_NAME)` → **QRTZ_TRIGGERS** `(TRIGGER_GROUP, TRIGGER_NAME)` · N:1 · logical-probable/probable — Execução em andamento de um trigger (join lógico Quartz).
- `(JOB_GROUP, JOB_NAME)` → **QRTZ_JOB_DETAILS** `(JOB_GROUP, JOB_NAME)` · N:1 · logical-probable/probable — Job em execução (campos nulos se job concorrente).
- `(INSTANCE_NAME)` → **QRTZ_SCHEDULER_STATE** `(INSTANCE_NAME)` · N:1 · logical-probable/probable — Nó do cluster que executa o disparo.

**Dicas de consulta:** Útil para ver jobs rodando agora por INSTANCE_NAME.

## QRTZ_JOB_DETAILS

Definição dos jobs agendados no Quartz (classe, grupo, nome, dados). Entidade com named queries usadas pelo painel de agendamentos do Fluig.

**Ciclo de vida:** Criada ao registrar um job; removida ao desagendar.

**Atenção:** Sem tenant; JOB_GROUP/JOB_NAME identificam o job.

**PK:** JOB_GROUP, JOB_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `JOB_GROUP` | varchar(255) | N | Grupo do job Quartz; parte da chave do job em QRTZ_JOB_DETAILS. |  | QRTZ_JOB_DETAILS.JOB_GROUP |
| 🔑 `JOB_NAME` | varchar(255) | N | Nome do job Quartz dentro do grupo; parte da chave do job em QRTZ_JOB_DETAILS. |  | QRTZ_JOB_DETAILS.JOB_NAME |
| `DESCRIPTION` | varchar(255) | S | Descrição textual do job, usada em buscas por filtro (named query findJobDetailsByFilterSearch). |  |  |
| `IS_DURABLE` | bit | N | Se true, o job permanece armazenado mesmo sem triggers associados. |  |  |
| `IS_STATEFUL` | bit | N | Legado Quartz: job stateful (execução não concorrente, persiste JobDataMap). |  |  |
| `IS_VOLATILE` | bit | N | Legado Quartz: job volátil (não sobrevive a reinício). |  |  |
| `JOB_CLASS_NAME` | varchar(255) | N | Nome completo da classe Java que implementa o job executado pelo scheduler. |  |  |
| `JOB_DATA` | longblob | S | JobDataMap serializado (binário) com parâmetros passados ao job. |  |  |
| `REQUESTS_RECOVERY` | bit | N | Se true, o job é reexecutado quando a instância que o rodava falha. |  |  |

**Dicas de consulta:** JOB_DATA é BLOB serializado. Join com QRTZ_TRIGGERS por (JOB_GROUP, JOB_NAME).

## QRTZ_JOB_LISTENERS

Listeners de job registrados por job.

**Ciclo de vida:** Normalmente vazia.

**PK:** JOB_GROUP, JOB_LISTENER, JOB_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `JOB_GROUP` | varchar(255) | N | Grupo do job Quartz; parte da chave do job em QRTZ_JOB_DETAILS. |  | QRTZ_JOB_DETAILS.JOB_GROUP |
| 🔑 `JOB_LISTENER` | varchar(255) | N | Nome do JobListener registrado para o job; parte da PK. |  |  |
| 🔑 `JOB_NAME` | varchar(255) | N | Nome do job Quartz dentro do grupo; parte da chave do job em QRTZ_JOB_DETAILS. |  | QRTZ_JOB_DETAILS.JOB_NAME |

**Relacionamentos (saem desta tabela):**

- `(JOB_GROUP, JOB_NAME)` → **QRTZ_JOB_DETAILS** `(JOB_GROUP, JOB_NAME)` · N:1 · physical-fk/confirmed — Listener registrado para o job.

**Dicas de consulta:** FK física para QRTZ_JOB_DETAILS.

## QRTZ_LOCKS

Linhas de lock usadas pelo Quartz em modo cluster (SELECT FOR UPDATE) para sincronizar nós.

**Ciclo de vida:** Poucas linhas fixas; semeadas na instalação.

**PK:** LOCK_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `LOCK_NAME` | varchar(255) | N | Nome do lock global do Quartz (ex.: TRIGGER_ACCESS, JOB_ACCESS, STATE_ACCESS) usado em SELECT FOR UPDATE para sincronizar nós. |  |  |

**Dicas de consulta:** Não consultar para negócio.

## QRTZ_PAUSED_TRIGGER_GRPS

Grupos de triggers pausados.

**Ciclo de vida:** Normalmente vazia.

**Atenção:** Não é pai de triggers; só lista grupos.

**PK:** TRIGGER_GROUP

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Grupo de triggers atualmente pausado; PK. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |

**Dicas de consulta:** Infraestrutura Quartz.

## QRTZ_SCHEDULER_STATE

Estado/heartbeat de cada instância (nó) do scheduler no cluster.

**Ciclo de vida:** Uma linha por nó; atualizada a cada check-in.

**PK:** INSTANCE_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `INSTANCE_NAME` | varchar(255) | N | Nome único da instância (nó) do scheduler no cluster; PK. |  |  |
| `CHECKIN_INTERVAL` | decimal(19,2) | N | Intervalo de check-in da instância, em milissegundos. |  |  |
| `LAST_CHECKIN_TIME` | decimal(19,2) | N | Último check-in da instância (heartbeat), ms desde epoch; usado para detectar nós mortos. |  |  |
| `RECOVERER` | varchar(255) | S | Instância que está recuperando jobs desta instância falha; nulo se nenhuma. |  |  |

**Dicas de consulta:** Detectar nós mortos via LAST_CHECKIN_TIME + CHECKIN_INTERVAL.

## QRTZ_SIMPLE_TRIGGERS

Detalhe de triggers Quartz de repetição simples (contagem e intervalo), 1:1 com QRTZ_TRIGGERS.

**Ciclo de vida:** Criada junto com o trigger simples.

**PK:** TRIGGER_GROUP, TRIGGER_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Nome do grupo do trigger Quartz; compõe a PK (TRIGGER_GROUP, TRIGGER_NAME) e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| 🔑 `TRIGGER_NAME` | varchar(255) | N | Nome do trigger Quartz dentro do grupo; compõe a PK e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_NAME |
| `REPEAT_COUNT` | decimal(19,2) | N | Número de repetições após o primeiro disparo (-1 = indefinido). |  |  |
| `REPEAT_INTERVAL` | decimal(19,2) | N | Intervalo entre repetições, em milissegundos. |  |  |
| `TIMES_TRIGGERED` | decimal(19,2) | N | Quantidade de vezes que o trigger já disparou. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TRIGGER_GROUP, TRIGGER_NAME)` → **QRTZ_TRIGGERS** `(TRIGGER_GROUP, TRIGGER_NAME)` · 1:1 · logical-confirmed/probable — Detalhe simples (repetição) do trigger; mesma PK de QRTZ_TRIGGERS.

**Dicas de consulta:** JOIN com QRTZ_TRIGGERS por (TRIGGER_GROUP, TRIGGER_NAME).

## QRTZ_TRIGGERS

Triggers do Quartz: quando e qual job disparar, estado e próximos/últimos disparos.

**Ciclo de vida:** Criada ao agendar; NEXT_FIRE_TIME/TRIGGER_STATE atualizados a cada disparo.

**Atenção:** Tempos em milissegundos desde epoch (decimal). Named query findTriggersFromJob.

**PK:** TRIGGER_GROUP, TRIGGER_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Nome do grupo do trigger Quartz; compõe a PK (TRIGGER_GROUP, TRIGGER_NAME) e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| 🔑 `TRIGGER_NAME` | varchar(255) | N | Nome do trigger Quartz dentro do grupo; compõe a PK e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_NAME |
| `CALENDAR_NAME` | varchar(255) | S | Calendário Quartz opcional que exclui períodos do disparo. |  | QRTZ_CALENDARS.CALENDAR_NAME |
| `DESCRIPTION` | varchar(255) | S | Descrição textual do trigger. |  |  |
| `END_TIME` | decimal(19,2) | S | Fim da validade do trigger, ms desde epoch; nulo = sem fim. |  |  |
| `IS_VOLATILE` | bit | N | Legado Quartz: trigger volátil. |  |  |
| `JOB_DATA` | longblob | S | JobDataMap do trigger serializado (binário). |  |  |
| `JOB_GROUP` | varchar(255) | N | Grupo do job que o trigger dispara. |  | QRTZ_JOB_DETAILS.JOB_GROUP |
| `JOB_NAME` | varchar(255) | N | Nome do job que o trigger dispara. |  | QRTZ_JOB_DETAILS.JOB_NAME |
| `MISFIRE_INSTR` | smallint | S | Código da instrução de misfire do Quartz (política quando o disparo é perdido). |  |  |
| `NEXT_FIRE_TIME` | decimal(19,2) | S | Próximo disparo previsto, ms desde epoch; nulo se não há mais. |  |  |
| `PREV_FIRE_TIME` | decimal(19,2) | S | Último disparo ocorrido, ms desde epoch. |  |  |
| `PRIORITY` | integer | S | Prioridade do trigger (maior = primeiro em empate de horário). |  |  |
| `START_TIME` | decimal(19,2) | N | Início da validade do trigger, ms desde epoch. |  |  |
| `TRIGGER_STATE` | varchar(255) | N | Estado do trigger no Quartz (ex.: WAITING, ACQUIRED, PAUSED, BLOCKED, COMPLETE, ERROR); não enumerado no código do Fluig. |  |  |
| `TRIGGER_TYPE` | varchar(255) | N | Tipo do trigger que define a tabela de detalhe (ex.: CRON, SIMPLE, BLOB). | CRON=QRTZ_CRON_TRIGGERS; SIMPLE=QRTZ_SIMPLE_TRIGGERS; BLOB=QRTZ_BLOB_TRIGGERS (convenção Quartz, não confirmada no código) |  |

**Relacionamentos (saem desta tabela):**

- `(JOB_GROUP, JOB_NAME)` → **QRTZ_JOB_DETAILS** `(JOB_GROUP, JOB_NAME)` · N:1 · physical-fk/confirmed — Job disparado pelo trigger.
- `(CALENDAR_NAME)` → **QRTZ_CALENDARS** `(CALENDAR_NAME)` · N:1 · logical-probable/probable — Calendário opcional (semântica Quartz; sem FK física).

**Dicas de consulta:** Tabela central do scheduler; detalhes em QRTZ_CRON_TRIGGERS/QRTZ_SIMPLE_TRIGGERS/QRTZ_BLOB_TRIGGERS conforme TRIGGER_TYPE.

## QRTZ_TRIGGER_LISTENERS

Listeners de trigger registrados por trigger.

**Ciclo de vida:** Normalmente vazia.

**PK:** TRIGGER_GROUP, TRIGGER_LISTENER, TRIGGER_NAME

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TRIGGER_GROUP` | varchar(255) | N | Nome do grupo do trigger Quartz; compõe a PK (TRIGGER_GROUP, TRIGGER_NAME) e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_GROUP |
| 🔑 `TRIGGER_LISTENER` | varchar(255) | N | Nome do TriggerListener registrado para o trigger; parte da PK. |  |  |
| 🔑 `TRIGGER_NAME` | varchar(255) | N | Nome do trigger Quartz dentro do grupo; compõe a PK e liga ao QRTZ_TRIGGERS. |  | QRTZ_TRIGGERS.TRIGGER_NAME |

**Relacionamentos (saem desta tabela):**

- `(TRIGGER_GROUP, TRIGGER_NAME)` → **QRTZ_TRIGGERS** `(TRIGGER_GROUP, TRIGGER_NAME)` · N:1 · physical-fk/confirmed — Listener registrado para o trigger.

**Dicas de consulta:** FK física para QRTZ_TRIGGERS.
