# Domínio: bpm-analytics-dw

10 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## ACTIVITY_DIM_CAP

Dimensão (modelo estrela do CAP, analytics de BPM) com as atividades de cada versão de processo.

**Ciclo de vida:** Populada/regravada pela extração de dados do CAP (CAPDataExtractorBI) a partir das definições de processo; volume = atividades x versões.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ACTIVITYID` | integer | N | ID numérico da atividade dentro da versão do processo (sequência da atividade no diagrama); parte da PK. |  |  |
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  |  |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  |  |
| `ACTIVITYNAME` | varchar(100) | S | Nome da atividade (desnormalizado da dimensão) no momento do snapshot. |  |  |
| `ISAUTOMATIC` | bit | S | Indica se a atividade é automática (serviço, sem tarefa humana). | true=atividade automática; false/NULL=não automática |  |
| `ISJOINT` | bit | S | Indica se a atividade é de junção (join/sincronização de fluxos paralelos). | true=atividade de junção |  |

**Relacionamentos (saem desta tabela):**

- `(COMPANYID, PROCESSID, PROCESSVERSION)` → **PROCES_VERSION_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Versão do processo da dimensão.

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado).

## FACT_ACTIVITY_COST_CAP

Fato de custo, esforço e prazo por atividade, dia e usuário (planejado/baseline vs realizado), separado por tarefas abertas, concluídas e canceladas.

**Ciclo de vida:** Linhas geradas por snapshot diário (named query findDateLastSnapShot busca a última data) pela extração do CAP; cresce por dia x atividade x usuário.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** ACTIVITYID, COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ACTIVITYID` | integer | N | Sequência (ID numérico) da atividade dentro da versão do processo; parte da PK. |  | ACTIVITY_DIM_CAP.ACTIVITYID |
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  | TIME_DIM_CAP.DAYID |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.MONTHID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSID |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSVERSION |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  | USER_DIM_CAP.USERSEQUENCE |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.YEARID |
| `ACTIVITYNAME` | varchar(100) | S | Nome da atividade (desnormalizado da dimensão) no momento do snapshot. |  |  |
| `BASELINECOSTCANCELTASKS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `BASELINECOSTCLOSEDTASKS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `BASELINECOSTOPENTASKS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `BASELINEDEADLINECANCELTASKS` | double | S | Soma de prazo (duração) planejado (baseline: valor previsto/estimado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `BASELINEDEADLINECLOSEDTASKS` | double | S | Soma de prazo (duração) planejado (baseline: valor previsto/estimado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `BASELINEDEADLINEOPENTASKS` | double | S | Soma de prazo (duração) planejado (baseline: valor previsto/estimado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `BASELINEEFFORTCANCELTASKS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `BASELINEEFFORTCLOSEDTASKS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `BASELINEEFFORTOPENTASKS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `NUMBEROFCANCELTASKS` | integer | S | Quantidade de tarefas da atividade canceladas no período do snapshot. |  |  |
| `NUMBEROFCLOSEDTASKS` | integer | S | Quantidade de tarefas da atividade concluídas no período do snapshot. |  |  |
| `NUMBEROFOPENTASKS` | integer | N | Quantidade de tarefas da atividade em aberto no snapshot (NOT NULL, ao contrário das demais contagens). |  |  |
| `REALCOSTCANCELTASKS` | double | S | Soma de custo realizado (apurado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `REALCOSTCLOSEDTASKS` | double | S | Soma de custo realizado (apurado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `REALCOSTOPENTASKS` | double | S | Soma de custo realizado (apurado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `REALDEADLINECANCELTASKS` | double | S | Soma de prazo (duração) realizado (apurado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `REALDEADLINECLOSEDTASKS` | double | S | Soma de prazo (duração) realizado (apurado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `REALDEADLINEOPENTASKS` | double | S | Soma de prazo (duração) realizado (apurado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `REALEFFORTCANCELTASKS` | double | S | Soma de esforço (horas) realizado (apurado) das tarefas (atividades) canceladas agregada no snapshot (double). |  |  |
| `REALEFFORTCLOSEDTASKS` | double | S | Soma de esforço (horas) realizado (apurado) das tarefas (atividades) concluídas agregada no snapshot (double). |  |  |
| `REALEFFORTOPENTASKS` | double | S | Soma de esforço (horas) realizado (apurado) das tarefas (atividades) em aberto agregada no snapshot (double). |  |  |
| `USERCODE` | varchar(255) | S | Código/login do usuário desnormalizado (varchar 255, ao contrário de 100 nas demais tabelas). |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION)` → **ACTIVITY_DIM_CAP** `(ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Atividade da versão do processo a que o fato se refere.
- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_COST_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo dia/processo/versão/usuário no fato de nível de processo; grão diferente (atividade vs processo), útil para drill-down, sem FK.
- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_VOLUME_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo dia/processo/versão/usuário no fato de nível de processo; grão diferente (atividade vs processo), útil para drill-down, sem FK.
- `(COMPANYID, DAYID, MONTHID, YEARID)` → **TIME_DIM_CAP** `(COMPANYID, DAYID, MONTHID, YEARID)` · N:1 · logical-probable/probable — Dia do snapshot na dimensão de tempo (relação lógica, sem FK).
- `(COMPANYID, USERSEQUENCE)` → **USER_DIM_CAP** `(COMPANYID, USERSEQUENCE)` · N:1 · logical-probable/probable — Usuário na dimensão (relação lógica, sem FK).
- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto).

## FACT_ACTIVITY_VOLUME_CAP

Fato de volume de tarefas por atividade, dia e usuário: abertas/concluídas/canceladas, dentro/fora do prazo.

**Ciclo de vida:** Snapshot diário gerado pela extração do CAP; crescimento por dia x atividade x usuário.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** ACTIVITYID, COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ACTIVITYID` | integer | N | Sequência (ID numérico) da atividade dentro da versão do processo; parte da PK. |  | ACTIVITY_DIM_CAP.ACTIVITYID |
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  | TIME_DIM_CAP.DAYID |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.MONTHID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSID |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSVERSION |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  | USER_DIM_CAP.USERSEQUENCE |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.YEARID |
| `ACTIVITYNAME` | varchar(100) | S | Nome da atividade (desnormalizado da dimensão) no momento do snapshot. |  |  |
| `CANCELLEDTASKS` | integer | S | Quantidade de tarefas da atividade canceladas no snapshot. |  |  |
| `CONCLUDEDTASKSINDEADLINE` | integer | S | Quantidade de tarefas concluídas dentro do prazo. |  |  |
| `CONCLUDEDTASKSOUTDEADLINE` | integer | S | Quantidade de tarefas concluídas fora do prazo (atrasadas). |  |  |
| `OPENTASKSINDEADLINE` | integer | S | Quantidade de tarefas ainda abertas e dentro do prazo. |  |  |
| `OPENTASKSOUTDEADLINE` | integer | S | Quantidade de tarefas ainda abertas e com prazo vencido. |  |  |
| `OPENINGS` | integer | S | Quantidade de aberturas (tarefas/solicitações iniciadas) no snapshot. |  |  |
| `OUTDEADLINEPREVIEWED` | integer | S | Quantidade de tarefas previstas para vencer o prazo (projeção de atraso); semântica inferida pelo nome. |  |  |
| `USERCODE` | varchar(100) | S | Código/login do usuário (colaborador) desnormalizado na linha de fato; corresponde a FDN_USERTENANT.USER_CODE. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION)` → **ACTIVITY_DIM_CAP** `(ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Atividade da versão do processo a que o fato se refere.
- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_COST_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo dia/processo/versão/usuário no fato de nível de processo; grão diferente (atividade vs processo), útil para drill-down, sem FK.
- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_VOLUME_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo dia/processo/versão/usuário no fato de nível de processo; grão diferente (atividade vs processo), útil para drill-down, sem FK.
- `(COMPANYID, DAYID, MONTHID, YEARID)` → **TIME_DIM_CAP** `(COMPANYID, DAYID, MONTHID, YEARID)` · N:1 · logical-probable/probable — Dia do snapshot na dimensão de tempo (relação lógica, sem FK).
- `(COMPANYID, USERSEQUENCE)` → **USER_DIM_CAP** `(COMPANYID, USERSEQUENCE)` · N:1 · logical-probable/probable — Usuário na dimensão (relação lógica, sem FK).
- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto).

## FACT_FLOW_VOLUME_CAP

Fato de volume de transições entre atividades (fluxos normais vs retornos) por dia e usuário.

**Ciclo de vida:** Snapshot diário gerado pela extração do CAP.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY, USERSEQUENCE, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  | TIME_DIM_CAP.DAYID |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.MONTHID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSID |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSVERSION |
| 🔑 `SOURCEACTIVITY` | integer | N | ID da atividade de origem da transição (fluxo) do processo. |  | ACTIVITY_DIM_CAP.ACTIVITYID |
| 🔑 `TARGETACTIVITY` | integer | N | ID da atividade de destino da transição (fluxo) do processo. |  | ACTIVITY_DIM_CAP.ACTIVITYID |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  | USER_DIM_CAP.USERSEQUENCE |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.YEARID |
| `NORMALFLOWS` | integer | S | Quantidade de transições normais (avanço) da atividade de origem para a de destino. |  |  |
| `RETURNEDFLOWS` | integer | S | Quantidade de transições de retorno (volta) da origem para o destino. |  |  |
| `SOURCEACTIVITYNAME` | varchar(100) | S | Nome da atividade de origem da transição, desnormalizado. |  |  |
| `TARGETACTIVITYNAME` | varchar(100) | S | Nome da atividade de destino da transição, desnormalizado. |  |  |
| `USERCODE` | varchar(100) | S | Código/login do usuário (colaborador) desnormalizado na linha de fato; corresponde a FDN_USERTENANT.USER_CODE. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_COST_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo grão (empresa/dia/processo/versão/usuário) de outro fato do processo; join por grão, não FK.
- `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` → **FACT_PROCES_VOLUME_CAP** `(COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID)` · 1:1 · logical-probable/probable — Mesmo grão (empresa/dia/processo/versão/usuário) de outro fato do processo; join por grão, não FK.
- `(COMPANYID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY)` → **FLOW_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY)` · N:1 · logical-probable/probable — Transição origem->destino na dimensão de fluxos.
- `(COMPANYID, DAYID, MONTHID, YEARID)` → **TIME_DIM_CAP** `(COMPANYID, DAYID, MONTHID, YEARID)` · N:1 · logical-probable/probable — Dia do snapshot na dimensão de tempo (relação lógica, sem FK).
- `(COMPANYID, USERSEQUENCE)` → **USER_DIM_CAP** `(COMPANYID, USERSEQUENCE)` · N:1 · logical-probable/probable — Usuário na dimensão (relação lógica, sem FK).
- `(COMPANYID, PROCESSID, PROCESSVERSION)` → **PROCES_VERSION_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Versão do processo na dimensão.
- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto).

## FACT_PROCES_COST_CAP

Fato de custo/esforço por processo, dia e usuário (baseline vs realizado) para processos abertos, concluídos e cancelados.

**Ciclo de vida:** Snapshot diário gerado pela extração do CAP.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  | TIME_DIM_CAP.DAYID |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.MONTHID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSID |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSVERSION |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  | USER_DIM_CAP.USERSEQUENCE |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.YEARID |
| `BASELINECOSTCANCELPROCESS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das processos canceladas agregada no snapshot (double). |  |  |
| `BASELINECOSTCLOSEDPROCESS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das processos concluídas agregada no snapshot (double). |  |  |
| `BASELINECOSTOPENPROCESS` | double | S | Soma de custo planejado (baseline: valor previsto/estimado) das processos em aberto agregada no snapshot (double). |  |  |
| `BASELINEEFFORTCANCELPROCESS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das processos canceladas agregada no snapshot (double). |  |  |
| `BASELINEEFFORTCLOSEDPROCESS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das processos concluídas agregada no snapshot (double). |  |  |
| `BASELINEEFFORTOPENPROCESS` | double | S | Soma de esforço (horas) planejado (baseline: valor previsto/estimado) das processos em aberto agregada no snapshot (double). |  |  |
| `NUMBEROFCANCELPROCESS` | integer | S | Quantidade de processos (solicitações) cancelados no snapshot. |  |  |
| `NUMBEROFCLOSEDPROCESS` | integer | S | Quantidade de processos (solicitações) concluídos no snapshot. |  |  |
| `NUMBEROFOPENPROCESS` | integer | S | Quantidade de processos (solicitações) em aberto no snapshot. |  |  |
| `REALCOSTCANCELPROCESS` | double | S | Soma de custo realizado (apurado) das processos canceladas agregada no snapshot (double). |  |  |
| `REALCOSTCLOSEDPROCESS` | double | S | Soma de custo realizado (apurado) das processos concluídas agregada no snapshot (double). |  |  |
| `REALCOSTOPENPROCESS` | double | S | Soma de custo realizado (apurado) das processos em aberto agregada no snapshot (double). |  |  |
| `REALEFFORTCANCELPROCESS` | double | S | Soma de esforço (horas) realizado (apurado) das processos canceladas agregada no snapshot (double). |  |  |
| `REALEFFORTCLOSEDPROCESS` | double | S | Soma de esforço (horas) realizado (apurado) das processos concluídas agregada no snapshot (double). |  |  |
| `REALEFFORTOPENPROCESS` | double | S | Soma de esforço (horas) realizado (apurado) das processos em aberto agregada no snapshot (double). |  |  |
| `USERCODE` | varchar(100) | S | Código/login do usuário (colaborador) desnormalizado na linha de fato; corresponde a FDN_USERTENANT.USER_CODE. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COMPANYID, PROCESSID, PROCESSVERSION)` → **PROCES_VERSION_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Versão do processo da dimensão.
- `(COMPANYID, DAYID, MONTHID, YEARID)` → **TIME_DIM_CAP** `(COMPANYID, DAYID, MONTHID, YEARID)` · N:1 · logical-probable/probable — Dia do snapshot na dimensão de tempo.
- `(COMPANYID, USERSEQUENCE)` → **USER_DIM_CAP** `(COMPANYID, USERSEQUENCE)` · N:1 · logical-probable/probable — Usuário na dimensão (USERSEQUENCE por empresa).
- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto).

## FACT_PROCES_VOLUME_CAP

Fato de volume de processos por dia e usuário: em aberto/concluídos dentro e fora do prazo, cancelados e aberturas.

**Ciclo de vida:** Snapshot diário gerado pela extração do CAP (named query findDateLastSnapShot).

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  | TIME_DIM_CAP.DAYID |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.MONTHID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSID |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  | PROCES_VERSION_DIM_CAP.PROCESSVERSION |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  | USER_DIM_CAP.USERSEQUENCE |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  | TIME_DIM_CAP.YEARID |
| `CANCELLED` | integer | S | Quantidade de processos cancelados no snapshot. |  |  |
| `CLOSEINTIME` | integer | S | Quantidade de processos concluídos dentro do prazo (campo Java closedInTime). |  |  |
| `CLOSELATE` | integer | S | Quantidade de processos concluídos com atraso (campo Java closedLate). |  |  |
| `OPENINTIME` | integer | S | Quantidade de processos em aberto dentro do prazo. |  |  |
| `OPENLATE` | integer | S | Quantidade de processos em aberto com prazo vencido. |  |  |
| `OPENINGS` | integer | S | Quantidade de aberturas (tarefas/solicitações iniciadas) no snapshot. |  |  |
| `USERCODE` | varchar(100) | S | Código/login do usuário (colaborador) desnormalizado na linha de fato; corresponde a FDN_USERTENANT.USER_CODE. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COMPANYID, PROCESSID, PROCESSVERSION)` → **PROCES_VERSION_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Versão do processo da dimensão.
- `(COMPANYID, DAYID, MONTHID, YEARID)` → **TIME_DIM_CAP** `(COMPANYID, DAYID, MONTHID, YEARID)` · N:1 · logical-probable/probable — Dia do snapshot na dimensão de tempo.
- `(COMPANYID, USERSEQUENCE)` → **USER_DIM_CAP** `(COMPANYID, USERSEQUENCE)` · N:1 · logical-probable/probable — Usuário na dimensão (USERSEQUENCE por empresa).
- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto).

## FLOW_DIM_CAP

Dimensão de fluxos (transições origem->destino entre atividades) de cada versão de processo.

**Ciclo de vida:** Populada pela extração do CAP a partir da definição do processo.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  |  |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  |  |
| 🔑 `SOURCEACTIVITY` | integer | N | ID da atividade de origem da transição (fluxo) do processo. |  |  |
| 🔑 `TARGETACTIVITY` | integer | N | ID da atividade de destino da transição (fluxo) do processo. |  |  |
| `ISRETURNALLOWED` | bit | S | Indica se a transição permite retorno (voltar) da atividade de destino para a de origem. | true=retorno permitido |  |
| `SOURCEACTIVITYNAME` | varchar(100) | S | Nome da atividade de origem da transição, desnormalizado. |  |  |
| `TARGETACTIVITYNAME` | varchar(100) | S | Nome da atividade de destino da transição, desnormalizado. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COMPANYID, PROCESSID, PROCESSVERSION)` → **PROCES_VERSION_DIM_CAP** `(COMPANYID, PROCESSID, PROCESSVERSION)` · N:1 · logical-probable/probable — Versão do processo da dimensão.

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado).

## PROCES_VERSION_DIM_CAP

Dimensão de versões de processos com a janela de vigência (início/fim em dia/mês/ano).

**Ciclo de vida:** Populada pela extração do CAP; uma linha por versão de processo e empresa.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, PROCESSID, PROCESSVERSION

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `PROCESSID` | varchar(100) | N | Código do processo BPM (definição de workflow) ao qual o registro se refere; parte da PK. |  |  |
| 🔑 `PROCESSVERSION` | integer | N | Número da versão da definição do processo BPM; parte da PK. |  |  |
| `VALIDITYENDDAY` | integer | S | Dia (1-31) do fim da vigência da versão do processo; NULL se ainda vigente (provável). |  |  |
| `VALIDITYENDMONTH` | integer | S | Mês (1-12) do fim da vigência da versão do processo. |  |  |
| `VALIDITYENDYEAR` | integer | S | Ano do fim da vigência da versão do processo. |  |  |
| `VALIDITYSTARTDAY` | integer | S | Dia (1-31) do início da vigência da versão do processo. |  |  |
| `VALIDITYSTARTMONTH` | integer | S | Mês (1-12) do início da vigência da versão do processo. |  |  |
| `VALIDITYSTARTYEAR` | integer | S | Ano do início da vigência da versão do processo. |  |  |

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado).

## TIME_DIM_CAP

Dimensão de tempo (calendário): uma linha por dia com data completa, feriado e dia da semana.

**Ciclo de vida:** Populada pela extração do CAP; volume = dias x empresas.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. As colunas DAYID/MONTHID/YEARID são mapeadas nos campos Java day/month/year. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, DAYID, MONTHID, YEARID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAYID` | integer | N | Dia do mês (1-31) do snapshot; componente da chave de tempo, não é surrogate key. |  |  |
| 🔑 `MONTHID` | integer | N | Mês (1-12) do snapshot; componente da chave de tempo. |  |  |
| 🔑 `YEARID` | integer | N | Ano (4 dígitos) do snapshot; componente da chave de tempo. |  |  |
| `COMPLEXDATE` | date | S | Data completa (DATE) correspondente a ANO/MÊS/DIA da linha de tempo. |  |  |
| `ISHOLIDAY` | bit | S | Indica se o dia é feriado. | true=feriado |  |
| `WEEKDAY` | integer | S | Dia da semana do dia; codificação (domingo=1 ou segunda=1) não confirmada no código. |  |  |

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado).

## USER_DIM_CAP

Dimensão de usuários do CAP com chave substituta USERSEQUENCE, código do usuário e custo por hora.

**Ciclo de vida:** Populada pela extração do CAP; HOURCOST alimenta cálculos de custo.

**Atenção:** Tabelas *_CAP são o data mart (estrela) do módulo CAP/analytics de BPM. A PK sempre inclui COMPANYID (tenant). Sem FKs físicas nem @JoinColumn: relações são lógicas por colunas de mesmo nome. Datas do snapshot ficam em DAYID/MONTHID/YEARID separados. Não foi localizado no código decompilado o ETL que popula as tabelas (CAPDataExtractorBI é apenas interface), então semântica de métricas é inferida de nomes.

**PK:** COMPANYID, USERSEQUENCE

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COMPANYID` | bigint | N | Identificador da empresa (tenant) do Fluig; faz parte da PK de todas as tabelas *_CAP. |  | FDN_TENANT.TENANT_ID |
| 🔑 `USERSEQUENCE` | integer | N | Sequência numérica do usuário na dimensão USER_DIM_CAP (chave substituta por empresa, não é a matrícula). |  |  |
| `HOURCOST` | double | S | Custo por hora do usuário (double), base do cálculo de custo realizado/baseline nos fatos de custo. |  |  |
| `USERCODE` | varchar(100) | S | Código/login do usuário (FDN_USERTENANT.USER_CODE) associado ao USERSEQUENCE. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(USERCODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Código do usuário; sem FK, join lógico por código (com empresa) -- apenas se a tabela tiver USERCODE. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Sempre filtrar por COMPANYID. Para agregar por período use YEARID/MONTHID/DAYID ou junte com TIME_DIM_CAP. Linhas de fato são snapshots (use o snapshot mais recente/um dia específico para não somar duplicado). USERCODE identifica usuário (dado pessoal indireto). HOURCOST é dado sensível (custo por hora do colaborador).
