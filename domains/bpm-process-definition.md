# Domínio: bpm-process-definition

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## PROPRIED_EXT

Propriedades estendidas (nome/valor) de estados/atividades de uma definição de processo (BPM), por versão.

**Ciclo de vida:** Gravada na publicação da versão do processo; imutável após a versão publicada.

**Atenção:** PK (COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, COD_PROPRIED). NUM_SEQ é a sequência do estado (atividade).

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, COD_PROPRIED

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo. |  | DEF_PROCES.COD_DEF_PROCES |
| 🔑 `COD_PROPRIED` | varchar(200) | N | Nome da propriedade estendida. |  |  |
| 🔑 `NUM_SEQ` | integer | N | Sequência do estado/atividade do processo dono da propriedade. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Versão da definição do processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `LOG_DEFAULT_PROPRIED` | bit | S | Indica propriedade padrão do produto (vs. definida pelo usuário). | 1=padrão |  |
| `DS_PRINCIPAL_PROPRIED` | varchar(2000) | S | Descrição da propriedade. |  |  |
| `CD_TIPO_PROPRIED` | integer | S | Tipo da propriedade (inteiro); valores não confirmados. |  |  |
| `DSL_VAL_PROPRIED` | varchar(2000) | S | Valor da propriedade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado/atividade dono da propriedade.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_PROPRIED)` → **PROPRIED_AVANCAD_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_PROPRIED)` · N:1 · logical-probable/probable — Heurística de nome; não confirmada.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **SEGUR_ANEXO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Heurística; não confirmada.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão do processo.

**Dicas de consulta:** Filtrar por COD_DEF_PROCES e NUM_VERS.

## VERS_DEF_PROCES

Versões de definições de processo (BPM): uma linha por versão publicada/em edição do processo com seu diagrama e opções.

**Ciclo de vida:** Criada ao salvar/publicar nova versão no Fluig Studio/modelador; LOG_ATIV marca a vigente.

**Atenção:** PK (COD_EMPRESA, COD_DEF_PROCES, NUM_VERS). CLB_IMG_PROCES é longtext grande.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo. |  | DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão do processo. |  |  |
| `LOG_ATIV` | bit | S | Versão ativa (vigente) do processo. | 1=ativa |  |
| `LOG_BLOQDO` | bit | S | Versão bloqueada (não permite novas solicitações/edição). | 1=bloqueada |  |
| `BPMN_VERS` | integer | S | Versão do modelo BPMN usado. |  |  |
| `LOG_CONTROLA_SEGUR_ANEXO` | bit | N | Controla segurança de anexos do processo. | 1=controla |  |
| `LOG_SOLICIT_CONTRA_SENHA` | bit | S | Exige contra-senha (confirmação de senha) para movimentação. | 1=exige |  |
| `LOG_EDIC` | bit | S | Versão em modo de edição (não publicada). | 1=em edição |  |
| `NUM_PASTA_FORM` | integer | S | NR_DOCUMENTO do formulário (fichário) associado. |  | DOCUMENTO.NR_DOCUMENTO |
| `LOG_HERDA_SEGUR_FORM` | bit | S | Formulário herda segurança do processo. | 1=herda |  |
| `MOBILE_READY` | bit | S | Processo preparado para mobile. | 1=pronto |  |
| `CLB_IMG_PROCES` | longtext | S | Diagrama do processo serializado (XML/imagem em texto longo). |  |  |
| `LOG_ATUALIZA_VERS_DOCTO_ANEXO` | bit | N | Atualiza versão dos documentos anexos ao movimentar. | 1=atualiza |  |
| `DES_VERS` | varchar(200) | S | Descrição da versão. |  |  |
| `SCRIPT_VERSION` | integer | N | Versão do script/modelo de eventos do processo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · hql-join/confirmed — Definição do processo (findAvailableProcess).
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES_ALERT** `(TENANT_ID, PROCESS_ID, PROCESS_VERSION)` · 1:N · logical-confirmed/probable — Alertas de análise estática da versão.
- `(COD_DEF_PROCES)` → **DEF_PROCES** `(COD_DEF_PROCES)` · N:1 · hql-join/confirmed — ProcessDefinitionVersion.findAvailableProcess
- `(COD_EMPRESA)` → **DEF_PROCES** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — ProcessDefinitionVersion.findAvailableProcess

**Dicas de consulta:** Filtrar por COD_DEF_PROCES e LOG_ATIV=1 para versão vigente. CLB_IMG_PROCES é grande: evitar SELECT *.

## VERS_DEF_PROCES_ALERT

Alertas de análise (boas práticas/riscos) gerados para versões de definição de processo.

**Ciclo de vida:** Gerada ao validar/publicar versão; reprocessável.

**Atenção:** Usa TENANT_ID, PROCESS_ID e PROCESS_VERSION (nomes em inglês). ALERT_TYPE embute o local (dezena).

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa). |  |  |
| `PROCESS_ID` | varchar(50) | N | Código da definição de processo. |  | DEF_PROCES.COD_DEF_PROCES |
| `PROCESS_VERSION` | integer | N | Versão do processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `SCRIPT_VERSION` | integer | N | Versão do script analisado. |  |  |
| `ALERT_TYPE` | integer | N | Tipo do alerta. | 1001=gerente sem mecanismo; 2001=tarefas automáticas; 2002=processo padrão com versão local; 3001=throw sem catch; 3002=uso de conexões do banco; 3003=service manager em script comum; 4001=condição de alta frequência; 4002=serviço de alta frequência; 5001=tradução para estado desconhecido; 5002=tradução difere do processo; 5003=tradução difere do estado |  |
| `ALERT_LOCAL` | integer | S | Local do alerta. | 10=definição; 20=versão da definição; 30=script; 40=estado; 50=tradução |  |
| `DETAILS` | longtext | S | Detalhes do alerta (texto longo). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, PROCESS_VERSION)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-confirmed/probable — Versão analisada.

**Dicas de consulta:** Join com VERS_DEF_PROCES por tenant, processo e versão.
