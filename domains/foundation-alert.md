# Domínio: foundation-alert

9 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_ALERT

Alerta/notificacao da central de alertas do Fluig destinado a um usuario (receiver), ligado a um tipo de evento, a um objeto e a um local.

**Ciclo de vida:** Inserida quando um modulo dispara um alerta; IS_READ atualizado ao ler; removida por limpeza/expurgo junto com ALERTACTION, ALERTMETADATA e ALERTSENDER. Volume alto.

**Atenção:** Sem coluna de tenant propria; o tenant vem do destinatario (RECEIVER_ID -> FDN_USERTENANT). As colunas KEY e CONSTRAINT do input sao artefatos do DDL (indice FK e FK), nao colunas reais.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial do alerta (PK). |  |  |
| `PRIORITY` | varchar(20) | N | Prioridade do alerta (nome do enum FDNAlertPriority gravado como string). | NONE; LOW; NORMAL; MEDIUM; HIGH |  |
| `CREATION_DATE` | datetime | N | Data/hora de criacao do alerta. |  |  |
| `EVENT_TYPE_ID` | bigint(20) | S | Tipo de evento do alerta. |  | FDN_ALERTEVENTTYPE.ID |
| `OBJECT_ID` | bigint(20) | S | Objeto de negocio ao qual o alerta se refere. |  | FDN_ALERTOBJECT.ID |
| `PLACE_ID` | bigint(20) | S | Local/contexto (tambem um FDN_ALERTOBJECT) onde o evento ocorreu. |  | FDN_ALERTOBJECT.ID |
| `IS_READ` | bit(1) | N | Flag: alerta ja lido pelo destinatario. | 1=lido; 0=nao lido |  |
| `RECEIVER_ID` | bigint(20) | S | Usuario destinatario (USER_TENANT_ID de FDN_USERTENANT). |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(RECEIVER_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Destinatario do alerta.
- `(EVENT_TYPE_ID)` → **FDN_ALERTEVENTTYPE** `(ID)` · N:1 · jpa-join/confirmed — Tipo de evento.
- `(OBJECT_ID)` → **FDN_ALERTOBJECT** `(ID)` · N:1 · jpa-join/confirmed — Objeto alvo do alerta.
- `(PLACE_ID)` → **FDN_ALERTOBJECT** `(ID)` · N:1 · jpa-join/confirmed — Local do evento.
- `(ID)` → **FDN_ALERTACTION** `(ALERT_ID)` · 1:N · jpa-join/confirmed — Acoes do alerta.
- `(ID)` → **FDN_ALERTMETADATA** `(ALERT_ID)` · 1:N · jpa-join/confirmed — Metadados chave/valor.
- `(ID)` → **FDN_ALERTSENDER** `(ALERT_ID)` · 1:N · jpa-join/confirmed — Remetentes do alerta.

**Dicas de consulta:** Consultas tipicas: nao lidos por RECEIVER_ID e IS_READ=0. EVENT_TYPE_ID, OBJECT_ID e PLACE_ID sao nullable.

## FDN_ALERTACTION

Acoes executaveis associadas a um alerta (ex.: aprovar, abrir link), com descricao i18n e integracao opcional via JMS/HTTP.

**Ciclo de vida:** Criada junto com o alerta; IS_EXECUTED marcado ao executar; removida com o alerta.

**Atenção:** ACTION_TYPE e INTEGRATION_TYPE sao enums JPA ORDINAL (indice baseado em 0). KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial da acao (PK). |  |  |
| `ACTION_KEY` | varchar(255) | N | Chave identificadora da acao, interpretada pela aplicacao emissora. |  |  |
| `ACTION_TYPE` | int(11) | N | Tipo da acao (enum FDNAlertActionType, ordinal). | 0=MAIN (acao principal); 1=DEFAULT |  |
| `ALERT_ID` | bigint(20) | S | Alerta dono da acao. |  | FDN_ALERT.ID |
| `DESCRIPTION_AFTER_EXEC_KEY` | varchar(255) | S | Chave i18n da descricao exibida apos a execucao da acao. |  |  |
| `DESCRIPTION_KEY` | varchar(255) | N | Chave i18n da descricao/rotulo da acao. |  |  |
| `IS_EXECUTED` | bit(1) | N | Flag: acao ja executada. | 1=executada; 0=pendente |  |
| `HTTP_METHOD` | varchar(10) | S | Metodo HTTP usado quando INTEGRATION_TYPE=HTTP (ex.: GET/POST). |  |  |
| `INTEGRATION_TYPE` | int(11) | S | Forma de integracao da acao (enum FDNAlertIntegrationType, ordinal). | 0=JMS; 1=HTTP; 2=NONE |  |
| `URL` | varchar(500) | S | URL chamada/aberta pela acao (integracao HTTP ou link). |  |  |

**Relacionamentos (saem desta tabela):**

- `(ALERT_ID)` → **FDN_ALERT** `(ID)` · N:1 · physical-fk/confirmed — Alerta dono da acao.

**Dicas de consulta:** URL pode conter parametros/links internos; tratar com cuidado.

## FDN_ALERTAPPSENDER

Aplicacao/canal emissor de alertas registrado por tenant (ex.: central Fluig, e-mail, mobile), com JNDI do destino de entrega.

**Ciclo de vida:** Carga inicial/registro por tenant; IS_ACTIVE e IS_BLOCKED alterados por administracao. Volume baixo.

**Atenção:** Multi-tenant via TENANT_ID. Referenciada por FDN_ALERTCONFIG.SENDER_APP_ID. KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial do emissor (PK). |  |  |
| `IS_ACTIVE` | bit(1) | N | Flag: canal ativo. | 1=ativo; 0=inativo |  |
| `APP_CODE` | varchar(255) | S | Codigo curto da aplicacao emissora. |  |  |
| `APP_KEY` | varchar(255) | N | Chave unica da aplicacao emissora usada nas consultas (applicationKey). |  |  |
| `IS_BLOCKED` | bit(1) | S | Flag: canal bloqueado, nao pode ser ativado pelo usuario. | 1=bloqueado; 0=livre |  |
| `DESCRIPTION_KEY` | varchar(255) | N | Chave i18n da descricao do canal. |  |  |
| `JNDI_NAME` | varchar(255) | N | Nome JNDI do recurso (fila/servico) que entrega os alertas ao canal. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant dono do canal.
- `(ID)` → **FDN_ALERTCONFIG** `(SENDER_APP_ID)` · 1:N · physical-fk/confirmed — Preferencias de recebimento por canal.

**Dicas de consulta:** Filtre por TENANT_ID e IS_ACTIVE=1 (ver FDNAlertAppSender.findAllActiveByTenant).

## FDN_ALERTCONFIG

Preferencia de recebimento de alertas: para um tenant/usuario, evento e canal, define se o alerta e recebido (ligado/desligado/bloqueado).

**Ciclo de vida:** Criada ao configurar notificacoes (por tenant com USER_ID nulo = padrao do tenant, ou por usuario); RECEIVE atualizado ao alterar preferencias. Volume medio/alto.

**Atenção:** USER_ID NULL = configuracao padrao do tenant (queries com b.user IS NULL). Ha um unique key no DDL (colunas nao detalhadas no input, provavelmente combinando evento, canal, tenant e usuario). A coluna USER_ID mapeia userTenantId.

**PK:** ID · **Unique:** (USER_ID, EVENT_TYPE_ID, SENDER_APP_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial da configuracao (PK). |  |  |
| `SENDER_APP_ID` | bigint(20) | S | Canal/aplicacao emissora a que a preferencia se aplica. |  | FDN_ALERTAPPSENDER.ID |
| `EVENT_TYPE_ID` | bigint(20) | S | Tipo de evento a que a preferencia se aplica. |  | FDN_ALERTEVENTTYPE.ID |
| `RECEIVE` | int(11) | N | Estado de recebimento (enum FDNAlertSenderEventStatus, ordinal; consultas usam receive=1 para ativo). | 0=OFF; 1=ON; 2=BLOCKED |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) da configuracao. |  | FDN_TENANT.TENANT_ID |
| `USER_ID` | bigint(20) | S | Usuario da preferencia (USER_TENANT_ID); NULL para padrao do tenant. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · jpa-join/confirmed — Usuario dono da preferencia (a relacao e com FDN_USERTENANT, nao FDN_USER).
- `(EVENT_TYPE_ID)` → **FDN_ALERTEVENTTYPE** `(ID)` · N:1 · jpa-join/confirmed — Evento configurado.
- `(SENDER_APP_ID)` → **FDN_ALERTAPPSENDER** `(ID)` · N:1 · physical-fk/confirmed — Canal configurado.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant.

**Dicas de consulta:** Sempre filtrar por TENANT_ID. USER_ID IS NULL retorna o padrao do tenant.

## FDN_ALERTEVENTTYPE

Catalogo de tipos de evento de alerta (ex.: tarefa atribuida) por tenant e modulo, com chaves i18n e regras de agrupamento/remocao.

**Ciclo de vida:** Registrado por aplicacoes/modulos na instalacao ou por tenant; raramente alterado. Volume baixo.

**Atenção:** Multi-tenant via TENANT_ID. EVENT_KEY e a chave logica usada nas consultas. KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial do tipo de evento (PK). |  |  |
| `IS_ACTIVE` | bit(1) | N | Flag: tipo de evento ativo. | 1=ativo; 0=inativo |  |
| `CAN_REMOVE` | bit(1) | N | Flag: o alerta deste tipo pode ser removido pelo usuario. |  |  |
| `DESCRIPTION_KEY` | varchar(255) | N | Chave i18n da descricao do evento. |  |  |
| `EVENT_KEY` | varchar(50) | N | Chave unica do evento usada pelas aplicacoes para disparar alertas (ate 50 chars). |  |  |
| `GROUP_DESCRIPTION_KEY` | varchar(255) | S | Chave i18n da descricao quando varios alertas sao agrupados. |  |  |
| `GROUPED` | bit(1) | N | Flag: alertas deste tipo sao exibidos agrupados. |  |  |
| `ICON` | varchar(255) | S | Nome/classe do icone exibido para o evento. |  |  |
| `MODULE_ID` | bigint(20) | S | Modulo ao qual o evento pertence. |  | FDN_ALERTMODULE.ID |
| `ONLY_ADMIN` | bit(1) | N | Flag: evento visivel/configuravel apenas por administradores. |  |  |
| `REMOVE_AFTER_EXEC_ACTION` | bit(1) | N | Flag: alerta e removido apos a execucao de sua acao. |  |  |
| `IS_REQUIRED` | bit(1) | N | Flag: evento obrigatorio, usuario nao pode desativar o recebimento. |  |  |
| `SINGLE_DESCRIPTION_KEY` | varchar(255) | N | Chave i18n da descricao quando ha um unico alerta. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(MODULE_ID)` → **FDN_ALERTMODULE** `(ID)` · N:1 · physical-fk/confirmed — Modulo do evento.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant.

**Dicas de consulta:** Filtre por TENANT_ID; use ONLY_ADMIN para separar eventos administrativos.

## FDN_ALERTMETADATA

Pares chave/valor extras anexados a um alerta (parametros usados para montar a mensagem/link).

**Ciclo de vida:** Criados com o alerta; removidos com ele (removeAlertMetadatasByAlertIdsList).

**Atenção:** METADATA_VALUE e LOB (longtext). KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial (PK). |  |  |
| `ALERT_ID` | bigint(20) | S | Alerta dono do metadado. |  | FDN_ALERT.ID |
| `METADATA_KEY` | varchar(255) | N | Nome da chave do metadado. |  |  |
| `METADATA_VALUE` | longtext | S | Valor do metadado (texto longo, LOB). |  |  |

**Relacionamentos (saem desta tabela):**

- `(ALERT_ID)` → **FDN_ALERT** `(ID)` · N:1 · physical-fk/confirmed — Alerta dono.

**Dicas de consulta:** Coluna LOB: evite SELECT * em consultas volumosas. Valor pode conter dados de negocio.

## FDN_ALERTMODULE

Modulo/aplicacao do Fluig que agrupa tipos de evento de alerta, por tenant.

**Ciclo de vida:** Registrado na instalacao ou por tenant; raramente muda. Volume baixo.

**Atenção:** Multi-tenant via TENANT_ID. KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial do modulo (PK). |  |  |
| `DESCRIPTION_KEY` | varchar(255) | N | Chave i18n do nome/descricao do modulo. |  |  |
| `MODULE_KEY` | varchar(255) | N | Chave logica unica do modulo (findByKey). |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant.
- `(ID)` → **FDN_ALERTEVENTTYPE** `(MODULE_ID)` · 1:N · physical-fk/confirmed — Eventos do modulo.

**Dicas de consulta:** Filtre por TENANT_ID.

## FDN_ALERTOBJECT

Objeto de negocio (documento, tarefa, etc.) referenciado por um alerta, tanto como alvo (OBJECT_ID) quanto como local (PLACE_ID).

**Ciclo de vida:** Criado ao disparar alerta; removido com os alertas (removeAlertObjectsByIdsList). Volume alto.

**Atenção:** Nao ha coluna de tenant. OBJECT_ID aqui e o id do objeto na aplicacao de origem (nao PK desta tabela); PK e ID. Indice INDEX_ALERT_OBJECT_KEYS (OBJECT_ID,OBJECT_CLASS). Sem FK declarada; FDN_ALERT referencia por ID.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial (PK), referenciado por FDN_ALERT.OBJECT_ID e PLACE_ID. |  |  |
| `DESCRIPTION` | varchar(255) | S | Descricao/titulo do objeto exibido no alerta. |  |  |
| `LINK` | varchar(4000) | S | URL de navegacao ate o objeto (ate 4000 chars). |  |  |
| `NOTE` | varchar(700) | S | Observacao adicional sobre o objeto (ate 700 chars). |  |  |
| `OBJECT_CLASS` | varchar(255) | N | Classe/tipo do objeto na aplicacao de origem; combinado com OBJECT_ID identifica o objeto. |  |  |
| `OBJECT_DETAIL_KEY` | varchar(255) | S | Chave i18n de detalhe adicional do objeto. |  |  |
| `OBJECT_ID` | bigint(20) | N | Identificador do objeto na aplicacao de origem (ex.: id do documento); nao e FK. |  |  |
| `TYPE_DESCRIPTION_KEY` | varchar(255) | S | Chave i18n do rotulo do tipo do objeto. |  |  |

**Relacionamentos (saem desta tabela):**

- `(ID)` → **FDN_ALERT** `(OBJECT_ID)` · 1:N · jpa-join/confirmed — Alertas que apontam para este objeto.
- `(ID)` → **FDN_ALERT** `(PLACE_ID)` · 1:N · jpa-join/confirmed — Alertas que usam este objeto como local.

**Dicas de consulta:** Busca por objeto de origem: OBJECT_ID + OBJECT_CLASS (indice). Nao confundir OBJECT_ID com FDN_ALERT.OBJECT_ID.

## FDN_ALERTSENDER

Registra quem enviou/originou um alerta (usuario remetente) e por qual via.

**Ciclo de vida:** Criada com o alerta; removida com ele (removeAlertSendersByAlertIdsList). Volume alto.

**Atenção:** USER_ID referencia FDN_USERTENANT.USER_TENANT_ID (FK fisica), nao FDN_USER. KEY/CONSTRAINT do input sao artefatos do DDL.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial (PK). |  |  |
| `ALERT_ID` | bigint(20) | S | Alerta enviado. |  | FDN_ALERT.ID |
| `CREATION_DATE` | datetime | N | Data/hora do envio/registro do remetente. |  |  |
| `USER_ID` | bigint(20) | S | Usuario remetente (USER_TENANT_ID). |  | FDN_USERTENANT.USER_TENANT_ID |
| `VIA` | varchar(255) | S | Canal/meio pelo qual o alerta foi enviado. |  |  |

**Relacionamentos (saem desta tabela):**

- `(USER_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Usuario remetente.
- `(ALERT_ID)` → **FDN_ALERT** `(ID)` · N:1 · jpa-join/confirmed — Alerta enviado.

**Dicas de consulta:** Junte com FDN_USERTENANT e depois FDN_USER se precisar do login/nome.
