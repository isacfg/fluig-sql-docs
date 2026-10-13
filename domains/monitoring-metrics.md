# Domínio: monitoring-metrics

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FLUIG_METRIC

Métricas de uso agregadas por dia: nome da métrica e contagem.

**Ciclo de vida:** Gravada periodicamente (por dia); volume moderado.

**Atenção:** Sem tenant. Índice IDX_FMETRIC001 em METRIC_DATE.

**PK:** METRIC_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `METRIC_ID` | bigint | N | PK surrogate da métrica. |  |  |
| `METRIC_COUNT` | integer | S | Contagem/valor da métrica na data. |  |  |
| `METRIC_DATE` | date | N | Dia a que a métrica se refere. |  |  |
| `METRIC` | varchar(255) | N | Nome/código da métrica de uso. |  |  |

**Dicas de consulta:** Filtrar por METRIC_DATE e METRIC.

## LS_METRIC

Cabeçalho de métricas de uso do License Server por tenant, identificando rotina e sub-rotina medidas.

**Ciclo de vida:** Criada na primeira medição de cada (tenant, rotina, subrotina); detalhes em LS_METRIC_DETAIL.

**Atenção:** Unique key (artefato UNIQUE), provavelmente TENANT_ID+ROUTINE+SUB_ROUTINE.

**PK:** METRIC_ID · **Unique:** (TENANT_ID, ROUTINE, SUB_ROUTINE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `METRIC_ID` | bigint(20) | N | PK surrogate da métrica. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant medido. |  | FDN_TENANT.TENANT_ID |
| `ROUTINE` | varchar(255) | N | Rotina/funcionalidade medida. |  |  |
| `SUB_ROUTINE` | varchar(255) | N | Sub-rotina medida dentro da rotina. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant medido.
- `(METRIC_ID)` → **LS_METRIC_DETAIL** `(METRIC_ID)` · 1:N · jpa-join/confirmed — Medições individuais.

**Dicas de consulta:** Join com LS_METRIC_DETAIL por METRIC_ID.

## LS_METRIC_DETAIL

Medições individuais (código, valor, instante) de métricas do License Server, com marca de processamento.

**Ciclo de vida:** Inserida a cada medição com LOG_PROCESSED=0; marcada como processada por rotina de envio/consolidação; volume alto.

**Atenção:** Índice IDX_METRICDETAIL001 (LOG_PROCESSED, METRIC_ID, METRIC_CODE, METRIC_TIME). Campo Java de METRIC_ID é mapeado como relação (metric).

**PK:** METRIC_DETAIL_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `METRIC_DETAIL_ID` | bigint(20) | N | PK surrogate da medição. |  |  |
| `METRIC_CODE` | varchar(255) | N | Código da métrica medida. |  |  |
| `METRIC_VALUE` | bigint(20) | N | Valor medido (inteiro longo). |  |  |
| `METRIC_TIME` | datetime | N | Instante da medição. |  |  |
| `LOG_PROCESSED` | bit | N | Indica se a medição já foi processada. | 0=pendente; 1=processada |  |
| `METRIC_ID` | bigint(20) | N | Cabeçalho de métrica (LS_METRIC) ao qual a medição pertence. |  | LS_METRIC.METRIC_ID |
| `LAPTIME` | bigint(20) | N | Tempo decorrido da operação medida (long; unidade provavelmente ms). |  |  |

**Relacionamentos (saem desta tabela):**

- `(METRIC_ID)` → **LS_METRIC** `(METRIC_ID)` · N:1 · physical-fk/confirmed — Cabeçalho da métrica (LSMetricDetail.metric).

**Dicas de consulta:** Consultar pendentes com LOG_PROCESSED=0.
