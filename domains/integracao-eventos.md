# Domínio: integracao-eventos

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_INTEGRATION

Componentes de integração registrados (bean/EJB por nome JNDI) que recebem eventos de integração, ordenados por prioridade.

**Ciclo de vida:** Registrados na implantação; poucas linhas.

**Atenção:** Unique (provável) por JNDI_NAME. Ordenação por PRIORITY (findAllOrderByPriority).

**PK:** INTEGRATION_ID · **Unique:** (JNDI_NAME)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `INTEGRATION_ID` | bigint(20) | N | Chave primária da integração. |  |  |
| `JNDI_NAME` | varchar(120) | N | Nome JNDI do componente que implementa a integração. |  |  |
| `PRIORITY` | int(11) | N | Prioridade de execução; menor valor primeiro (ordenação ascendente presumida). |  |  |

**Relacionamentos (saem desta tabela):**

- `(INTEGRATION_ID)` → **FDN_INTEGRATIONEVENT** `(INTEGRATION_ID)` · 1:N · physical-fk/confirmed — Eventos tratados pela integração.

**Dicas de consulta:** Tabela global, sem tenant.

## FDN_INTEGRATIONEVENT

Eventos de integração que cada integração (FDN_INTEGRATION) declara tratar. Cada linha é um nome de evento.

**Ciclo de vida:** Registrada junto com a integração.

**Atenção:** Unique (provável) INTEGRATION_ID + EVENT_NAME.

**PK:** INTEGRATIONEVENT_ID · **Unique:** (EVENT_NAME, INTEGRATION_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `INTEGRATIONEVENT_ID` | bigint(20) | N | Chave primária. |  |  |
| `EVENT_NAME` | varchar(120) | N | Nome do evento de integração. |  |  |
| `EXPLICIT` | bit(1) | N | Indica se o evento precisa ser solicitado explicitamente (não é disparado por padrão). | 1=explícito; 0=implícito |  |
| `INTEGRATION_ID` | bigint(20) | N | Integração dona do evento. |  | FDN_INTEGRATION.INTEGRATION_ID |

**Relacionamentos (saem desta tabela):**

- `(INTEGRATION_ID)` → **FDN_INTEGRATION** `(INTEGRATION_ID)` · N:1 · physical-fk/confirmed — Integração dona.

**Dicas de consulta:** Join com FDN_INTEGRATION para obter JNDI_NAME.

## FDN_INTEGRATIONLISTENEREVT

Listeners externos registrados para eventos de integração, com informações de conexão síncrona e assíncrona.

**Ciclo de vida:** Cadastro por integração externa; poucas linhas.

**Atenção:** Unique (provável) EVENT_NAME + LISTENER_ID. Sem FK; EVENT_NAME casa com FDN_INTEGRATIONEVENT.EVENT_NAME por valor.

**PK:** INTEGRATION_LISTENER_EVT_ID · **Unique:** (EVENT_NAME, LISTENER_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `INTEGRATION_LISTENER_EVT_ID` | bigint(20) | N | Chave primária. |  |  |
| `ASYNC_CON_INFO` | varchar(4000) | S | Informações de conexão para entrega assíncrona (endpoint/destino). |  |  |
| `EVENT_NAME` | varchar(120) | N | Nome do evento escutado. |  | FDN_INTEGRATIONEVENT.EVENT_NAME |
| `LISTENER_ID` | varchar(120) | N | Identificador do listener registrado. |  |  |
| `SYNC_CON_INFO` | varchar(4000) | S | Informações de conexão para entrega síncrona (endpoint/destino). |  |  |

**Relacionamentos (saem desta tabela):**

- `(EVENT_NAME)` → **FDN_INTEGRATIONEVENT** `(EVENT_NAME)` · N:1 · logical-probable/probable — Casa por nome do evento, sem FK.

**Dicas de consulta:** ASYNC_CON_INFO/SYNC_CON_INFO podem conter URLs ou credenciais; tratar como sensíveis.
