# Domínio: bpm-workflow

56 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## ADHOC_PROCES

Tarefas ad hoc (atividades avulsas criadas em tempo de execução) vinculadas a um estado/atividade de uma instância de processo.

**Ciclo de vida:** Uma linha por tarefa ad hoc criada pelo usuário numa instância; cresce com uso do recurso.

**Atenção:** PK (COD_EMPRESA, NUM_PROCES, NUM_SEQ): NUM_SEQ aqui é a sequência do estado do processo (processStateSequence), não sequência própria.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo (solicitação) que contém a tarefa ad hoc. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ` | integer | N | Sequência do estado/atividade do processo (processStateSequence) à qual a tarefa ad hoc está ligada. |  | ESTADO_PROCES.NUM_SEQ |
| `CD_MATRICULA` | varchar(255) | S | Matrícula do usuário que criou a tarefa ad hoc. |  | FDN_USERTENANT.USER_CODE |
| `DT_CRIACAO` | date | S | Data (sem hora) de criação da tarefa ad hoc. |  |  |
| `DS_ADHOC_PROCES` | varchar(4000) | S | Descrição livre da tarefa ad hoc, até 4000 caracteres. |  |  |
| `NOM_ADHOC_PROCES` | varchar(200) | S | Nome/título da tarefa ad hoc, até 200 caracteres. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância de processo dona da tarefa ad hoc.

**Dicas de consulta:** Filtrar COD_EMPRESA. Para ligar à tarefa-pai use ADHOC_PROCES_WORKFLOW.

## ADHOC_PROCES_WORKFLOW

Relaciona a instância de processo pai (e seu estado) às instâncias de sub-processo geradas para tarefas ad hoc.

**Ciclo de vida:** Uma linha por tarefa ad hoc que gerou instância de workflow própria.

**Atenção:** PK de 4 colunas: pai (NUM_PROCES_PAI + NUM_SEQ_PROCES_PAI) e filho (NUM_PROCES).

**PK:** COD_EMPRESA, NUM_PROCES_PAI, NUM_SEQ_PROCES_PAI, NUM_PROCES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROCES_PAI` | integer | N | Número da instância de processo pai onde a tarefa ad hoc foi criada. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ_PROCES_PAI` | integer | N | Sequência do estado/atividade da instância pai à qual a tarefa ad hoc está ligada. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo (workflow) criada para a tarefa ad hoc. |  | PROCES_WORKFLOW.NUM_PROCES |
| `NOM_TAR_ADHOC_PROCES` | varchar(200) | S | Nome da tarefa ad hoc, até 200 caracteres. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância filha criada para a tarefa ad hoc.
- `(COD_EMPRESA, NUM_PROCES_PAI)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância pai (relação não listada pela heurística; deduzida do nome da coluna).
- `(COD_EMPRESA)` → **PROCES_WORKFLOW** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — WorkflowAdHocProcess.findActiveByParent
- `(NUM_PROCES)` → **PROCES_WORKFLOW** `(NUM_PROCES)` · N:1 · hql-join/confirmed — WorkflowAdHocProcess.findActiveByParent

**Dicas de consulta:** Dois joins distintos a PROCES_WORKFLOW (pai e filho); use aliases.

## ANEXO_PROCES

Anexos (documentos do GED) vinculados a instâncias de processo de workflow, com histórico de onde/por quem foram incluídos.

**Ciclo de vida:** Uma linha por anexo adicionado a uma solicitação; cresce com o uso de anexos em processos.

**Atenção:** PK (COD_EMPRESA, NUM_PROCES, NUM_SEQ_ANEXO). As 15 colunas VALOR_CAMPO_xx são LOB genéricos, normalmente vazios.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_ANEXO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NUM_SEQ_ANEXO` | integer | N | Sequência do anexo dentro da instância de processo; compõe a PK. |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo ao qual o anexo pertence. |  | PROCES_WORKFLOW.NUM_PROCES |
| `DT_ANEXO` | datetime | S | Data e hora em que o anexo foi incluído. |  |  |
| `CD_MATRICULA` | varchar(150) | S | Matrícula do usuário que anexou o documento. |  | FDN_USERTENANT.USER_CODE |
| `NR_DOCUMENTO` | integer | S | Número do documento do GED (ECM) anexado à instância. |  | DOCUMENTO.NR_DOCUMENTO |
| `VALOR_CAMPO_01` | longtext | S | Slot 1 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_10` | longtext | S | Slot 10 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_11` | longtext | S | Slot 11 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_12` | longtext | S | Slot 12 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_13` | longtext | S | Slot 13 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_14` | longtext | S | Slot 14 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_15` | longtext | S | Slot 15 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_02` | longtext | S | Slot 2 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_03` | longtext | S | Slot 3 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_04` | longtext | S | Slot 4 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_05` | longtext | S | Slot 5 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_06` | longtext | S | Slot 6 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_07` | longtext | S | Slot 7 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_08` | longtext | S | Slot 8 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `VALOR_CAMPO_09` | longtext | S | Slot 9 de valor de campo de formulário associado ao anexo (texto longo, uso genérico; semântica depende do processo). |  |  |
| `NUM_SEQ_MOVTO_ORIG` | integer | S | Sequência do movimento do processo em que o anexo foi originalmente incluído. |  |  |
| `NUM_SEQ_THREAD_ORIG` | integer | S | Sequência da thread do processo em que o anexo foi originalmente incluído. |  |  |
| `NR_VERSAO` | integer | S | Versão do documento GED anexado. |  | DOCUMENTO.NR_VERSAO |
| `REPLACEMENT_ID` | varchar(150) | S | Matrícula do substituto em nome de quem o anexo foi incluído, quando há substituição. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância dona do anexo.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento GED anexado (relação lógica não listada pela heurística).

**Dicas de consulta:** Colunas VALOR_CAMPO_xx são longtext: evitar SELECT *. Binário do anexo está no GED (DOCUMENTO/arquivo), não aqui.

## APONT_TAR_PROCES

Apontamentos de esforço (tempo gasto) registrados por usuários em tarefas de instâncias de processo.

**Ciclo de vida:** Uma linha por apontamento; cresce com uso de apontamento de horas.

**Atenção:** PK de 6 colunas identifica a tarefa (processo, movimento, usuário, transferência) mais a sequência do apontamento.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, CD_MATRICULA, NUM_SEQ_TRANSF, NUM_SEQ_APONT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NUM_SEQ_APONT` | integer | N | Sequência do apontamento dentro da tarefa/usuário. |  |  |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que apontou o tempo. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequência do movimento do processo (tarefa). |  | MOVTO_PROCES.NUM_SEQ_MOVTO |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ_TRANSF` | integer | N | Sequência de transferência da tarefa entre usuários. |  | TAR_PROCES.NUM_SEQ_TRANSF |
| `DAT_APONT` | date | S | Data do apontamento (sem hora). |  |  |
| `NUM_SEGS_APONT` | integer | S | Duração apontada em segundos. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` → **TAR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` · N:1 · logical-probable/probable — Tarefa do usuário em que o tempo foi apontado.

**Dicas de consulta:** Somar NUM_SEGS_APONT para esforço total. Filtrar COD_EMPRESA.

## COLAB_SUBSTTO

Configuração de substituição de usuário (delegação): quem é substituído, quem substitui, período e quais tipos de tarefa (GED/workflow) são delegados.

**Ciclo de vida:** Criada por usuário/admin ao cadastrar ausência; mantida após fim da vigência.

**Atenção:** PK substituta COLLEAGUE_REPLACEMENT_ID. Vigência por DAT_INIC_VALID/DAT_FIM_VALID (datas sem hora).

**PK:** COLLEAGUE_REPLACEMENT_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COLLEAGUE_REPLACEMENT_ID` | bigint | N | Identificador único (surrogate) da substituição. |  |  |
| `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário substituído (ausente). |  | FDN_USERTENANT.USER_CODE |
| `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| `COD_SUBSTTO` | varchar(50) | N | Matrícula do usuário substituto. |  | FDN_USERTENANT.USER_CODE |
| `DAT_FIM_VALID` | date | S | Data final de vigência da substituição. |  |  |
| `DAT_INIC_VALID` | date | S | Data inicial de vigência da substituição. |  |  |
| `LOG_TAR_GED` | bit | S | Substituto visualiza tarefas do GED (aprovações) do substituído. | 1=sim; 0=não |  |
| `LOG_TAR_WORKFLOW` | bit | S | Substituto visualiza tarefas de workflow do substituído. | 1=sim; 0=não |  |
| `DSL_REPLACEMENT_JUSTIFY` | varchar(500) | S | Justificativa da substituição, até 500 caracteres. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COLLEAGUE_REPLACEMENT_ID)` → **COLAB_SUBSTTO_PROCESSO** `(COLLEAGUE_REPLACEMENT_ID)` · 1:N · logical-probable/probable — Processos específicos delegados nesta substituição.
- `(COD_EMPRESA, COD_SUBSTTO)` → **FDN_USERTENANT** `(TENANT_ID, USER_CODE)` · N:1 · logical-probable/probable — Usuário substituto. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Substituição vigente: hoje entre DAT_INIC_VALID e DAT_FIM_VALID. Quem é substituto: COD_SUBSTTO; substituído: CD_MATRICULA. Ver COLAB_SUBSTTO_PROCESSO para restrição a processos.

## COLAB_SUBSTTO_PROCESSO

Lista de processos (definições) aos quais uma substituição de usuário se aplica.

**Ciclo de vida:** Linhas criadas junto com a substituição quando limitada a processos específicos.

**Atenção:** Colunas CD_MATRICULA, COD_EMPRESA e COD_SUBSTTO duplicam dados de COLAB_SUBSTTO e são anuláveis.

**PK:** COLLEAGUE_PROCESS_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COLLEAGUE_PROCESS_ID` | bigint | N | Identificador único (surrogate) da linha. |  |  |
| `CD_MATRICULA` | varchar(50) | S | Matrícula do usuário substituído (cópia de COLAB_SUBSTTO.CD_MATRICULA). |  | FDN_USERTENANT.USER_CODE |
| `COLLEAGUE_REPLACEMENT_ID` | bigint | S | Substituição à qual o processo pertence. |  | COLAB_SUBSTTO.COLLEAGUE_REPLACEMENT_ID |
| `COD_EMPRESA` | bigint | S | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| `COD_PROCESS` | varchar(50) | N | Código da definição de processo delegada. |  | DEF_PROCES.COD_DEF_PROCES |
| `COD_SUBSTTO` | varchar(50) | S | Matrícula do substituto (cópia de COLAB_SUBSTTO.COD_SUBSTTO). |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COLLEAGUE_REPLACEMENT_ID)` → **COLAB_SUBSTTO** `(COLLEAGUE_REPLACEMENT_ID)` · N:1 · logical-probable/probable — Substituição pai.
- `(COD_EMPRESA, COD_PROCESS)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-probable/probable — Definição de processo delegada.

**Dicas de consulta:** Colunas anuláveis; preferir COLLEAGUE_REPLACEMENT_ID para join.

## COMPON_GRAF_PROCES

Componentes gráficos (nós do diagrama) de uma versão de definição de processo, com posição e tipo.

**Ciclo de vida:** Gerada ao salvar/publicar a versão do processo no modelador; imutável por versão.

**Atenção:** PK (COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_COMPON_GRAF).

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_COMPON_GRAF

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_COMPON_GRAF` | integer | N | Sequência do componente gráfico dentro da versão do processo. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo. |  | DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `IDI_TIP_COMPON_GRAF` | integer | S | Tipo do componente gráfico do diagrama (ex.: atividade, gateway); valores não confirmados no código. |  |  |
| `NUM_POS_X` | integer | S | Posição horizontal (X) do componente no diagrama, em pixels. |  |  |
| `NUM_POS_Y` | integer | S | Posição vertical (Y) do componente no diagrama, em pixels. |  |  |
| `DES_COMPON_GRAF` | varchar(4000) | S | Nome/rótulo do componente (stateName), até 4000 caracteres. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão do processo dona do componente.

**Dicas de consulta:** Filtrar por COD_DEF_PROCES+NUM_VERS.

## DEF_PROCES

Definição (cabeçalho) de processo de workflow BPM: dados comuns a todas as versões, como categoria, prazos, notificações e gestor.

**Ciclo de vida:** Criada ao cadastrar o processo; versões ficam em VERS_DEF_PROCES.

**Atenção:** PK (COD_EMPRESA, COD_DEF_PROCES). Metadados por versão estão em VERS_DEF_PROCES.

**PK:** COD_EMPRESA, COD_DEF_PROCES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código/identificador do processo (processId). |  |  |
| `LOG_ATIV` | bit | S | Processo ativo. | 1=ativo; 0=inativo |  |
| `NUM_DIA_BASE` | integer | S | Dia base para cálculo de prazo/SLA. |  |  |
| `NUM_MES_BASE` | integer | S | Mês base para cálculo de prazo/SLA. |  |  |
| `COD_CATEG` | varchar(250) | S | Código da categoria do processo. |  | CATEG_PROCES.COD_CATEG |
| `IDI_TIP_COMPLEMENTO` | integer | S | Nível de permissão de complementos (complementsLevel). | 0=desabilitado; 1=solicitante, responsável e gestor; 2=todos os participantes e gestor; 3=todos os usuários |  |
| `NUM_HRS_PRAZ` | integer | S | Prazo padrão em horas. |  |  |
| `DSL_INSTRUC` | varchar(2000) | S | Instruções do processo, até 2000 caracteres. |  |  |
| `DES_KEYWORD` | varchar(255) | S | Palavras-chave para busca do processo. |  |  |
| `DSL_CONFIGUR_MECAN_GEST` | longtext | S | Configuração do mecanismo de atribuição do gestor do processo (texto longo). |  |  |
| `COD_MECAN_ATRIBUIC_GESTOR` | varchar(255) | S | Código do mecanismo de atribuição que determina o gestor. |  | MECAN_ATRIBUIC.COD_MECAN_ATRIBUIC |
| `LOG_NOTIF_RESPONS_COMPL` | bit | S | Notifica o responsável em complementos. | 1=sim; 0=não |  |
| `LOG_NOTIF_GESTOR_COMPL` | bit | S | Notifica o gestor em complementos. | 1=sim; 0=não |  |
| `LOG_NOTIF_REQUISIT_COMPL` | bit | S | Notifica o solicitante em complementos. | 1=sim; 0=não |  |
| `COD_PERIOD_EXPED` | varchar(50) | S | Código do período de expediente usado nos prazos. |  | PERIOD_EXPED.COD_PERIOD_EXPED |
| `DES_DEF_PROCES` | varchar(250) | S | Descrição do processo, até 250 caracteres. |  |  |
| `LOG_PROCES_PUBLIC` | bit | S | Processo público (acessível sem autenticação/ampla). | 1=público; 0=restrito |  |
| `IDI_FREQ_SNAPSHOT` | integer | S | Frequência de snapshot do CAP. | 0=nunca; 1=diária; 2=semanal; 3=mensal; 4=anual |  |
| `LOG_ATUALIZA_VERS_FICHA` | bit | S | Atualiza a versão do cartão do formulário (ficha) única. | 1=sim; 0=não |  |
| `COD_VOL_FISIC` | varchar(20) | S | Código do volume físico de armazenamento. |  |  |
| `NUM_HRS_PRAZ_WARNING` | integer | S | Horas de antecedência para aviso de prazo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · 1:N · logical-probable/probable — Versões da definição.
- `(COD_EMPRESA, COD_DEF_PROCES)` → **DOC_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · 1:N · logical-probable/probable — Diagramas BPMN publicados.

**Dicas de consulta:** Filtrar COD_EMPRESA. Algumas FKs lógicas de baixa confiança.

## DIAGNOSIS_PROCESS_LOG

Log de auditoria das ações de diagnóstico em processos e instâncias, como troca de versão de script e reenvio.

**Ciclo de vida:** Uma linha por ação de diagnóstico; cresce conforme uso.

**Atenção:** Usa TENANT_ID. PROCESS_ID e PROCESS_VERSION podem ser nulos em ações de instância.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador único (autogerado). |  |  |
| `TENANT_ID` | bigint | N | Tenant dono da linha. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | S | Código da definição de processo afetada. |  | DEF_PROCES.COD_DEF_PROCES |
| `PROCESS_VERSION` | integer | N | Versão da definição de processo afetada. |  | VERS_DEF_PROCES.NUM_VERS |
| `INSTANCE_ID` | integer | S | Número da instância de processo, quando a ação é por instância. |  | PROCES_WORKFLOW.NUM_PROCES |
| `USER_ID` | varchar(255) | N | Código do usuário que executou a ação. |  | FDN_USERTENANT.USER_CODE |
| `ACTION` | integer | N | Código da ação de diagnóstico (DiagnosisProcessLogActionType). | 101=INSTANCE_CHANGE_SCRIPT_VERSION; 102=INSTANCE_RESEND; 103=INSTANCE_VERBOSE_SCRIPT; 104=INSTANCE_DOWNLOAD; 201=PROCESS_NEW_SCRIPT_VERSION; 202=PROCESS_CHANGE_SCRIPT_VERSION; 203=PROCESS_ANALYSIS_SCRIPT |  |
| `ACTION_DATE` | datetime | N | Data e hora da ação. |  |  |
| `ACTION_VALUE` | longtext | S | Detalhe/valor da ação, texto longo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-probable/probable — Processo diagnosticado.
- `(TENANT_ID, INSTANCE_ID)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância diagnosticada.
- `(USER_ID)` → **FDN_USER** `(USER_ID)` · N:1 · logical-probable/probable — Inferência heurística por nome; USER_ID aqui guarda o código do usuário, confirmar coluna alvo.

**Dicas de consulta:** Índice por (TENANT_ID, PROCESS_ID, PROCESS_VERSION, INSTANCE_ID). ACTION_VALUE pode ter scripts.

## DOC_PROCES

Diagramas BPMN (XML) publicados de processos, uma linha por versão.

**Ciclo de vida:** Criada em cada publicação do diagrama.

**Atenção:** PK (COD_EMPRESA, COD_DOC_PROCES, NUM_VERS). CLB_XML_PROCES é LOB grande.

**PK:** COD_EMPRESA, COD_DOC_PROCES, NUM_VERS

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DOC_PROCES` | varchar(50) | N | Identificador do processo BPMN (processId). |  |  |
| 🔑 `NUM_VERS` | integer | N | Número da versão do diagrama. |  |  |
| `LOG_ATIV` | bit | S | Versão ativa. | 1=ativa; 0=inativa |  |
| `DAT_DOC_PROCES` | datetime | N | Data e hora de criação/publicação do diagrama. |  |  |
| `COD_DEF_PROCES` | varchar(50) | S | Definição de processo associada. |  | DEF_PROCES.COD_DEF_PROCES |
| `DES_DOC_PROCES` | varchar(250) | S | Descrição do processo, até 250 caracteres. |  |  |
| `CLB_XML_PROCES` | longtext | S | XML BPMN completo do diagrama. |  |  |
| `CD_PUBLICADOR` | varchar(255) | S | Matrícula do usuário que publicou. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão da definição; NUM_VERS pode divergir do diagrama (heurística).

**Dicas de consulta:** Evitar SELECT * por causa de CLB_XML_PROCES.

## ESTADO_PROCES

Estado/atividade (nó do fluxo BPM) de uma versão de definição de processo: tarefas, gateways, eventos, subprocessos e fim, com prazos, notificações, atribuição e posição no diagrama (entidade ProcessState).

**Ciclo de vida:** Criada ao salvar/publicar uma versão do processo no modelador; imutável após release da versão. Volume proporcional a versões x atividades.

**Atenção:** Chave composta (empresa, processo, versão, sequência). Cada versão do processo duplica seus estados. NUM_SEQ é compartilhado no espaço de ids do diagrama.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | Sequência (id numérico dentro da versão do processo) do estado/atividade do diagrama. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `NUM_PERC_CSENSO` | integer | S | Percentual de consenso exigido para aprovar atividade conjunta (LOG_CONJTA) entre os responsáveis. |  |  |
| `NUM_HRS_TOLERA_RESPONS` | integer | S | Horas de tolerância após o prazo antes de notificar atraso ao responsável da tarefa. |  |  |
| `NUM_HRS_TOLERA_GESTOR` | integer | S | Horas de tolerância após o prazo antes de notificar atraso ao gestor. |  |  |
| `NUM_HRS_TOLERA_REQUISIT` | integer | S | Horas de tolerância após o prazo antes de notificar atraso ao requisitante do processo. |  |  |
| `LOG_DECIS_AUTOM` | bit | S | Indica atividade/decisão automática (gateway exclusivo executado pelo motor sem usuário). | 1=automática; 0=manual |  |
| `IDI_TIP_BPMN` | integer | S | Tipo BPMN do elemento (enum ProcessStateBpmnType): evento, tarefa, subprocesso, gateway ou loop. | 10=start normal;11=start message;12=start timer;13=start conditional;14=start signal;15=start parallel multiple;16=start multiple;30=intermediate normal;31=int. message;32=int. timer;33=int. escalation;34=int. compensate;35=int. conditional;36=int. link;37=int. signal;38=int. parallel multiple;39=int. multiple;40=int. message receive;41=int. signal receive;42=int. link receive;43=int. error;60=end normal;61=end message;62=end escalation;63=end error;64=end signal;65=end cancel;66=end multiple;67=end compensate;68=end terminate;80=task normal;81=task user;82=task service;83=task receive;84=task mail;85=task manual;86=task business rule;87=task script;100=subprocess normal;101=subprocess adhoc;120=gateway exclusive;121=gateway inclusive;122=gateway event;123=gateway exclusive event;124=gateway parallel event;125=gateway complex;126=gateway parallel;127=gateway join;140=loop none;141=loop default;142=loop multi thread |  |
| `LOG_CANCELA_SUBPROC` | bit | S | Indica se o cancelamento da atividade cancela também o subprocesso em execução. | 1=cancela subprocesso |  |
| `LOG_SOLICIT_CONTRA_SENHA` | bit | S | Exige contra-senha (nova confirmação de senha) do usuário ao concluir a atividade. | 1=exige |  |
| `DEADLINE_FORM_FIELDNAME` | varchar(255) | S | Nome do campo do formulário que fornece a data do prazo da atividade (prazo dinâmico). |  |  |
| `NUM_HRS_PRAZ` | integer | S | Prazo da atividade em horas para o responsável concluir. |  |  |
| `LOG_SOLICIT_ASS_DIGITAL` | bit | S | Exige assinatura digital do usuário ao concluir a atividade. | 1=exige |  |
| `DSL_CONFIGUR_MECAN_ATRIBUIC` | longtext | S | Configuração (serializada, texto longo) do mecanismo de atribuição: parâmetros de grupo/papel/campo/etc. |  |  |
| `COD_MECAN_ATRIBUIC` | varchar(25) | S | Código do mecanismo de atribuição de responsável da atividade (ex.: usuário, grupo, papel, campo). |  | MECAN_ATRIBUIC.COD_MECAN_ATRIBUIC |
| `TIPO_EXEC` | integer | S | Tipo de execução da atividade de serviço/automática. |  |  |
| `NUM_ESFOR_PREVIS` | integer | S | Esforço previsto para a atividade (quantidade; unidade definida em IDI_CALC_ESFOR). |  |  |
| `IDI_CALC_ESFOR` | integer | S | Tipo/unidade de cálculo do esforço previsto (NUM_ESFOR_PREVIS). |  |  |
| `NUM_PASTA_FORM` | integer | S | Id (NR_DOCUMENTO) da pasta do GED onde o formulário da atividade/processo é armazenado. |  | DOCUMENTO.NR_DOCUMENTO |
| `NUM_HRS_FREQ_RESPONS` | integer | S | Frequência em horas de repetição das notificações de atraso/acompanhamento ao responsável. |  |  |
| `NUM_HRS_FREQ_GESTOR` | integer | S | Frequência em horas das notificações ao gestor. |  |  |
| `NUM_HRS_FREQ_REQUISIT` | integer | S | Frequência em horas das notificações ao requisitante. |  |  |
| `LOG_INIBE_TRANSF` | bit | S | Indica se a transferência da tarefa para outro usuário está inibida nesta atividade. | 1=proíbe transferir |  |
| `LOG_ESTADO_INICIAL` | bit | S | Marca o estado inicial (start) da versão do processo. | 1=inicial |  |
| `DSL_INSTRUC` | longtext | S | Texto de instruções exibido ao usuário na atividade (longtext, pode conter HTML). |  |  |
| `LOG_CONJTA` | bit | S | Indica atividade conjunta: vários responsáveis precisam concluir (ver NUM_PERC_CSENSO). | 1=conjunta |  |
| `NUM_HRS_EXPIRAC_RESPONS` | integer | S | Horas antes do vencimento para avisar o responsável (aviso de expiração). |  |  |
| `NUM_HRS_EXPIRAC_GESTOR` | integer | S | Horas antes do vencimento para avisar o gestor. |  |  |
| `NUM_HRS_EXPIRAC_REQUISIT` | integer | S | Horas antes do vencimento para avisar o requisitante. |  |  |
| `LOG_NOTIF_RESPONS_ATRASO` | bit | S | Notificar o responsável quando a tarefa atrasar. | 1=notifica |  |
| `LOG_NOTIF_RESPONS_ACOMPTO` | bit | S | Notificar o responsável para acompanhamento (aviso antes do prazo). | 1=notifica |  |
| `LOG_NOTIF_GESTOR_ATRASO` | bit | S | Notificar o gestor quando a tarefa atrasar. | 1=notifica |  |
| `LOG_NOTIF_GESTOR_ACOMP` | bit | S | Notificar o gestor para acompanhamento. | 1=notifica |  |
| `LOG_NOTIF_REQUISIT_ATRASO` | bit | S | Notificar o requisitante quando a tarefa atrasar. | 1=notifica |  |
| `LOG_NOTIF_REQUISIT_ACOMPTO` | bit | S | Notificar o requisitante para acompanhamento. | 1=notifica |  |
| `NUM_SEQ_PAI` | integer | S | NUM_SEQ do elemento pai no diagrama (raia/subprocesso/grupo que contém este estado). |  | LIN_PROCES.NUM_SEQ |
| `COD_PERIOD_EXPED` | varchar(50) | S | Código do período de expediente usado para calcular prazos em horas úteis. |  | PERIOD_EXPED.COD_PERIOD_EXPED |
| `NUM_POS_X` | integer | S | Posição horizontal (X, em pixels) do elemento no diagrama do processo. |  |  |
| `NUM_POS_Y` | integer | S | Posição vertical (Y, em pixels) do elemento no diagrama do processo. |  |  |
| `IDI_ASSUME_COLAB` | integer | S | Modo de seleção/assunção do colaborador responsável (default x personalizado, ver AssignmentType). | 0=atribuição padrão (DEFAULT_ASSIGNMENT);1=atribuição personalizada (CUSTOM_ASSIGNMENT) |  |
| `LOG_ENVIA_ATIV_SUB` | bit | S | Envia o fluxo para a próxima atividade dentro do subprocesso. | 1=sim |  |
| `COD_SINAL` | integer | S | Id do sinal BPMN associado ao evento de sinal. |  | PROCES_SIGNAL.COD_SINAL |
| `DES_ESTADO` | varchar(200) | S | Descrição da atividade/estado. |  |  |
| `NOM_ESTADO` | varchar(200) | S | Nome da atividade/estado exibido no diagrama e na tarefa. |  |  |
| `IDI_TIP_ESTADO` | integer | S | Tipo funcional do estado (enum ProcessStateType). | 0=simples;1=automático;2=subprocesso;3=fork;4=join;6=fim |  |
| `LOG_SUB_PROCES` | bit | S | Indica que o estado é um subprocesso (chama outro processo). | 1=subprocesso |  |
| `COD_DEF_SUB_PROCES` | varchar(50) | S | Código da definição do processo chamado como subprocesso. |  | DEF_PROCES.COD_DEF_PROCES |
| `LOG_TRANSF_ANEXO` | bit | S | Transfere os anexos para o subprocesso. | 1=transfere |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES_TRIGGER** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · 1:N · hql-join/confirmed — Gatilhos (timer/sinal/etc.) do estado, usados em ProcessStateTrigger.findInitialTimerTrigger.
- `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` → **MECAN_ATRIBUIC** `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` · N:1 · logical-probable/probable — Mecanismo de atribuição de responsável.
- `(COD_EMPRESA, COD_SINAL)` → **PROCES_SIGNAL** `(COD_EMPRESA, COD_SINAL)` · N:1 · logical-probable/probable — Sinal BPMN do evento.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-confirmed/confirmed — Versão da definição de processo à qual o estado pertence.
- `(NUM_VERS)` → **ESTADO_PROCES_TRIGGER** `(NUM_VERS)` · N:1 · hql-join/confirmed — ProcessStateTrigger.findInitialTimerTrigger
- `(COD_DEF_PROCES)` → **ESTADO_PROCES_TRIGGER** `(COD_DEF_PROCES)` · N:1 · hql-join/confirmed — ProcessStateTrigger.findInitialTimerTrigger
- `(COD_EMPRESA)` → **ESTADO_PROCES_TRIGGER** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — ProcessStateTrigger.findInitialTimerTrigger
- `(NUM_SEQ)` → **ESTADO_PROCES_TRIGGER** `(NUM_SEQ)` · N:1 · hql-join/confirmed — ProcessStateTrigger.findInitialTimerTrigger

**Dicas de consulta:** Sempre filtrar por COD_EMPRESA + COD_DEF_PROCES + NUM_VERS (as versões coexistem). LOG_ESTADO_INICIAL=1 localiza o start. DSL_INSTRUC e DSL_CONFIGUR_MECAN_ATRIBUIC são longtext. IDI_TIP_BPMN dá o tipo BPMN fino; IDI_TIP_ESTADO o tipo funcional.

## ESTADO_PROCES_COND

Condições de decisão (saídas) associadas a um estado automático/gateway: expressão ou mapa de regras que determina o estado de destino (entidade ConditionProcessState).

**Ciclo de vida:** Criada ao modelar gateways/decisões; ordenada por NUM_SEQ_ORD_FORMUL.

**Atenção:** Ordem de avaliação = NUM_SEQ_ORD_FORMUL; CONDITION_TYPE define se DES_FORMUL_ESTADO é expressão.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, NUM_SEQ_ORD_FORMUL

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_ORD_FORMUL` | integer | N | Ordem de avaliação da condição dentro do estado (1,2,...). |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | NUM_SEQ do estado (gateway/automático) dono da condição. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `DES_FORMUL_ESTADO` | varchar(350) | S | Expressão da condição (script/fórmula) que, se verdadeira, leva ao estado de destino. |  |  |
| `NUM_SEQ_ESTADO_DEST` | integer | N | NUM_SEQ do estado de destino quando a condição é satisfeita. |  | ESTADO_PROCES.NUM_SEQ |
| `DSL_CONFIGUR_MECAN_ATRIBUIC` | longtext | S | Configuração serializada do mecanismo de atribuição para o estado de destino. |  |  |
| `COD_MECAN_ATRIBUIC` | varchar(25) | S | Código do mecanismo de atribuição aplicado ao destino da condição. |  | MECAN_ATRIBUIC.COD_MECAN_ATRIBUIC |
| `CONDITION_TYPE` | integer | N | Tipo da condição: por expressão ou por mapa de regras. | 0=expressão (CONDITION_BY_EXPRESSION);1=mapa de regras (CONDITION_BY_RULES_MAP) |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado (gateway/decisão) dono da condição.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_ESTADO_DEST)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado de destino da condição (NUM_SEQ_ESTADO_DEST -> NUM_SEQ).
- `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` → **MECAN_ATRIBUIC** `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` · N:1 · logical-probable/probable — Mecanismo de atribuição.

**Dicas de consulta:** Juntar a ESTADO_PROCES pelas 4 colunas-chave; ordenar por NUM_SEQ_ORD_FORMUL.

## ESTADO_PROCES_SCRIPT

Script de condição (nome de arquivo/identificador) associado a um estado de evento condicional (ProcessStateConditionScript).

**Ciclo de vida:** Criada ao configurar evento condicional por script; poucas linhas.

**Atenção:** NUM_SEQ_CONDITION identifica a condição dentro do estado.

**PK:** COD_EMPRESA, NUM_SEQ_CONDITION, COD_DEF_PROCES, NUM_SEQ, NUM_VERS

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_CONDITION` | integer | N | Sequência da condição dentro do estado (várias condições por estado). |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | NUM_SEQ do estado (campo Java stateSequence) dono do script. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `DSL_SCRIPT` | varchar(255) | S | Script/expressão da condição (até 255 caracteres) avaliada pelo motor. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado/atividade do processo ao qual esta linha pertence.

**Dicas de consulta:** Juntar a ESTADO_PROCES por COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ.

## ESTADO_PROCES_SERVICE

Configuração de serviço (integração) executado por um estado de tarefa de serviço: nome do serviço, tentativas e frequência (ProcessStateService).

**Ciclo de vida:** Criada ao modelar tarefa de serviço no processo.

**Atenção:** PK substituta (PROCESS_STATE_SERVICE_ID).

**PK:** PROCESS_STATE_SERVICE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PROCESS_STATE_SERVICE_ID` | bigint | N | Chave substituta da configuração de serviço do estado. |  |  |
| `NUM_TENTATIVAS` | integer | N | Número máximo de tentativas de execução do serviço em caso de falha. |  |  |
| `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| `NUM_TEMPO` | integer | S | Intervalo/frequência entre execuções ou tentativas (unidade em IDI_TEMPO). |  |  |
| `IDI_TEMPO` | integer | S | Unidade de tempo de NUM_TEMPO (default 0 quando nulo). |  |  |
| `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| `NUM_SEQ` | integer | N | NUM_SEQ do estado dono do serviço. |  | ESTADO_PROCES.NUM_SEQ |
| `NOM_SERVICE` | varchar(200) | S | Nome do serviço cadastrado (serviço corporativo/integração) chamado pela tarefa. |  |  |
| `MSG_SUCESS` | varchar(200) | S | Mensagem de sucesso associada à execução do serviço. |  |  |
| `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado/atividade do processo ao qual esta linha pertence.

**Dicas de consulta:** Juntar a ESTADO_PROCES pelas 4 colunas-chave. Tipo de execução (manual/posterior/imediata) está em ESTADO_PROCES.TIPO_EXEC (ProcessStateServiceExecutionType 0=MANUAL,1=POSTERIOR,2=IMMEDIATE, mapeamento provável).

## ESTADO_PROCES_SIGNAL

Vínculo entre um estado de evento condicional/sinal e um sinal BPMN (ProcessStateConditionSignal).

**Ciclo de vida:** Criada ao configurar eventos de sinal no processo.

**PK:** COD_EMPRESA, NUM_SEQ_CONDITION, COD_DEF_PROCES, NUM_SEQ, NUM_VERS

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_CONDITION` | integer | N | Sequência da condição dentro do estado. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | NUM_SEQ do estado (stateSequence) dono do sinal. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `COD_SINAL` | integer | S | Id do sinal BPMN escutado/disparado. |  | PROCES_SIGNAL.COD_SINAL |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado/atividade do processo ao qual esta linha pertence.
- `(COD_EMPRESA, COD_SINAL)` → **PROCES_SIGNAL** `(COD_EMPRESA, COD_SINAL)` · N:1 · logical-probable/probable — Sinal BPMN referenciado.

## ESTADO_PROCES_TRIGGER

Gatilhos (timers/eventos) de um estado: agendamento, frequência e valor de disparo para eventos iniciais/intermediários de timer (ProcessStateTrigger).

**Ciclo de vida:** Criada ao modelar eventos de timer/mensagem; JOB_NAME liga ao agendador.

**Atenção:** Consultada por findInitialTimerTrigger para eventos de início por timer.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, NUM_SEQ_TRIGGER

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | NUM_SEQ do estado (stateSequence) dono do gatilho. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_SEQ_TRIGGER` | integer | N | Sequência do gatilho dentro do estado. |  |  |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `DSL_DIA_SEMANA` | varchar(255) | S | Dias da semana (lista textual) em que o timer dispara. |  |  |
| `DSL_FREQUENCIA` | varchar(255) | S | Frequência/expressão de repetição do timer. |  |  |
| `JOB_NAME` | varchar(255) | S | Nome do job agendado (scheduler) criado para o gatilho. |  |  |
| `COD_TRIGGER` | integer | S | Tipo de execução (runType) da frequência do timer. | 0=minuto;1=hora;2=dia;3=dia útil;4=mês;5=semana do mês;6=dia da semana;99=segundo |  |
| `DSL_TIME_TRIGGER` | varchar(255) | S | Horário/instante de disparo do timer (texto). |  |  |
| `IDI_CALC_ESFOR` | integer | S | Tipo do gatilho (campo Java type, enum ProcessStateTriggerType); nome de coluna reaproveitado de IDI_CALC_ESFOR. | 0=sinal;1=mensagem;2=timer;3=condicional;4=múltiplo;5=paralelo |  |
| `DSL_VALUE` | varchar(4000) | S | Valor/parâmetro do gatilho (até 4000 caracteres), ex.: expressão ou intervalo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · hql-join/confirmed — Estado dono do gatilho (join em findInitialTimerTrigger).

**Dicas de consulta:** Para timers de início, juntar a ESTADO_PROCES com LOG_ESTADO_INICIAL=1.

## EVENT_FICHA

Script de evento (JavaScript) de um formulário/ficha, por documento e versão (CardEvent).

**Ciclo de vida:** Criada ao salvar eventos do formulário no editor de formulários.

**Atenção:** Versionada por NR_VERSAO; LOG_APLIC_TODAS_VERS indica aplicação a versões anteriores.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_EVENT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número do documento (formulário) no GED ao qual o evento pertence. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `COD_EVENT` | varchar(25) | N | Nome/código do evento do formulário (ex.: displayFields, validateForm). |  | EVENT_GERAL.COD_EVENT |
| 🔑 `NR_VERSAO` | integer | N | Versão do documento do formulário. |  | DOCUMENTO.NR_VERSAO |
| `DSL_EVENT` | longtext | N | Código-fonte (longtext) do script do evento. |  |  |
| `LOG_APLIC_TODAS_VERS` | bit | S | Indica se o evento vale também para versões anteriores do formulário. | 1=aplica a todas as versões |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento (formulário) dono do evento.
- `(COD_EMPRESA, COD_EVENT)` → **EVENT_GERAL** `(COD_EMPRESA, COD_EVENT)` · N:1 · logical-probable/probable — Evento global de mesmo nome; relação por nome, sem FK.

**Dicas de consulta:** Contém código executável; tratar como dado, não executar.

## EVENT_GERAL

Eventos globais (scripts JavaScript) disponíveis a todo o ambiente do tenant, ex.: eventos globais de workflow (GlobalEvent).

**Ciclo de vida:** Criada/atualizada pelo administrador em Eventos Globais.

**PK:** COD_EMPRESA, COD_EVENT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `COD_EVENT` | varchar(50) | N | Nome do evento global (chave com COD_EMPRESA). |  |  |
| `DSL_EVENT` | longtext | N | Código-fonte (longtext) do script do evento global. |  |  |

**Dicas de consulta:** Código executável; não executar.

## EVENT_PROCES

Scripts de evento (JavaScript) de uma versão de processo, com histórico de versões do script (WorkflowProcessEvent).

**Ciclo de vida:** Criada ao salvar eventos do processo; nova SCRIPT_VERSION a cada alteração.

**Atenção:** Várias linhas por evento (SCRIPT_VERSION); a mais alta é a atual.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_EVENT, SCRIPT_VERSION

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `COD_EVENT` | varchar(50) | N | Nome do evento de processo (ex.: beforeTaskSave, afterProcessCreate). |  | EVENT_GERAL.COD_EVENT |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| 🔑 `SCRIPT_VERSION` | integer | N | Versão do script do evento; incrementa a cada edição. |  |  |
| `DSL_EVENT` | longtext | N | Código-fonte (longtext) do script. |  |  |
| `AUTHOR_ID` | varchar(255) | S | Matrícula do usuário autor da versão do script. |  | FDN_USER.COLLEAGUE_ID |
| `CREATE_DATE` | datetime | S | Data/hora de criação da versão do script. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão do processo dona do evento.

**Dicas de consulta:** Filtrar a maior SCRIPT_VERSION para o script vigente (HISTOR_PROCES.SCRIPT_VERSION registra a usada). Código executável.

## FLUIG_RUNTIMEDATA_PROCESS_MNGR

Armazenamento chave/valor de dados de runtime do gerenciador de processos (BPM); sem entidade JPA no código.

**Ciclo de vida:** Escrita pelo próprio módulo BPM; poucas linhas.

**Atenção:** Sem entidade mapeada; significado inferido do nome.

**PK:** DATA_KEY

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DATA_KEY` | varchar(255) | N | Chave do dado de runtime do gerenciador de processos. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor (até 4000 caracteres) associado à chave. |  |  |

**Dicas de consulta:** Tabela sem tenant; não consultar sem conhecer a chave.

## FORM_DATASET

Associa um formulário (documento/versão) a datasets usados por ele (FormDataset).

**Ciclo de vida:** Criada ao vincular datasets no formulário.

**Atenção:** UK_FORMDATASET001 (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_DATASET).

**PK:** FORM_DATASET_ID · **Unique:** (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_DATASET)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `FORM_DATASET_ID` | bigint | N | Chave substituta do vínculo. |  |  |
| `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| `COD_DATASET` | varchar(100) | N | Código do dataset vinculado ao formulário. |  | SERV_DATASET.COD_DATASET |
| `NR_DOCUMENTO` | integer | N | Número do documento do formulário. |  | DOCUMENTO.NR_DOCUMENTO |
| `NR_VERSAO` | integer | N | Versão do documento do formulário. |  | DOCUMENTO.NR_VERSAO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DATASET)` → **SERV_DATASET** `(COD_EMPRESA, COD_DATASET)` · N:1 · physical-fk/confirmed — FK física para o dataset.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Formulário dono do vínculo.
- `(COD_EMPRESA)` → **DOCUMENTO** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — FormDataset.FIND_RELATION_WITH_OTHERS_FORMS
- `(NR_DOCUMENTO)` → **DOCUMENTO** `(NR_DOCUMENTO)` · N:1 · hql-join/confirmed — FormDataset.FIND_RELATION_WITH_OTHERS_FORMS
- `(NR_VERSAO)` → **DOCUMENTO** `(NR_VERSAO)` · N:1 · hql-join/confirmed — FormDataset.FIND_RELATION_WITH_OTHERS_FORMS

**Dicas de consulta:** Na lista de colunas aparece também uma linha CONSTRAINT (UK_FORMDATASET001), que é a unique key, não coluna real.

## HISTOR_ACES

Histórico de acessos de usuários a documentos por dia (AccessLog).

**Ciclo de vida:** Uma linha por usuário/documento/dia de acesso.

**Atenção:** PK inclui a data; sem hora.

**PK:** COD_EMPRESA, CD_MATRICULA, DAT_ACES, NR_DOCUMENTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DAT_ACES` | date | N | Data do acesso ao documento. |  |  |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que acessou o documento. |  | FDN_USER.COLLEAGUE_ID |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número do documento acessado. |  | DOCUMENTO.NR_DOCUMENTO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento acessado (NR_DOCUMENTO).

**Dicas de consulta:** Registra comportamento de usuário (dado pessoal indireto).

## HISTOR_CONVER

Histórico de conversões de instâncias de processo de uma versão de definição para outra (ConversionHistory).

**Ciclo de vida:** Uma linha por execução de conversão de versão.

**PK:** COD_EMPRESA, NUM_SEQ_CONVER

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_CONVER` | integer | N | Sequência da conversão (id dentro da empresa). |  |  |
| `CD_MATRICULA` | varchar(255) | S | Matrícula do usuário que executou a conversão. |  | FDN_USER.COLLEAGUE_ID |
| `DAT_CONVER` | date | S | Data da conversão. |  |  |
| `NUM_HRS_CONVER` | integer | S | Hora da conversão (inteiro; formato provável HHmm ou segundos do dia). |  |  |
| `COD_DEF_PROCES` | varchar(255) | S | Código do processo convertido. |  | DEF_PROCES.COD_DEF_PROCES |
| `NUM_VERS_ORIG` | integer | S | Versão de origem do processo antes da conversão. |  | VERS_DEF_PROCES.NUM_VERS |
| `NUM_VERS` | integer | S | Versão de destino do processo após a conversão. |  | VERS_DEF_PROCES.NUM_VERS |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão de destino.
- `(COD_EMPRESA, NUM_SEQ_CONVER)` → **HISTOR_CONVER_ESTADO** `(COD_EMPRESA, NUM_SEQ_CONVER)` · 1:N · logical-probable/probable — Mapeamento de estados da conversão.

## HISTOR_CONVER_ESTADO

Mapeamento de estados na conversão: estado de origem x estado de destino por conversão (ConversionHistoryState).

**Ciclo de vida:** Uma linha por estado mapeado em cada conversão.

**PK:** COD_EMPRESA, NUM_SEQ_CONVER, NUM_SEQ_ESTADO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_CONVER` | integer | N | Sequência da conversão pai. |  | HISTOR_CONVER.NUM_SEQ_CONVER |
| 🔑 `NUM_SEQ_ESTADO` | integer | N | NUM_SEQ do estado na versão de origem. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_SEQ_ESTADO_CONVER` | integer | S | NUM_SEQ do estado correspondente na versão de destino. |  | ESTADO_PROCES.NUM_SEQ |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_SEQ_CONVER)` → **HISTOR_CONVER** `(COD_EMPRESA, NUM_SEQ_CONVER)` · N:1 · logical-probable/probable — Conversão pai.

## HISTOR_PROCES

Histórico de movimentações de uma instância de processo: cada passagem entre estados, com datas, links seguidos, thread e versão da definição (ProcessHistory).

**Ciclo de vida:** Uma linha por movimentação; cresce continuamente com o uso (tabela grande).

**Atenção:** Índices: NUM_SEQ_MOVTO_ANT; (COD_EMPRESA, LOG_ATIV, NUM_SUB_PROCES); (COD_EMPRESA, DAT_MOVTO); KEY PROCESHISTORY02 (NUM_SUB_PROCES, NUM_PROCES).

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequência da movimentação dentro da instância. |  |  |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo (processInstanceId). |  | PROCES_WORKFLOW.NUM_PROCES |
| `LOG_ATIV` | bit | S | Indica movimentação ativa (estado corrente da instância/thread). | 1=ativa;0=encerrada |  |
| `LOG_FLUXO_AUTOM` | bit | S | Movimentação feita por link automático. | 1=automático |  |
| `NUM_SEQ_CONVER` | integer | S | Sequência da conversão de versão que gerou a movimentação (quando houve). |  | HISTOR_CONVER.NUM_SEQ_CONVER |
| `LOG_FLUXO_PADRAO` | bit | S | Movimentação feita pelo link padrão. | 1=padrão |  |
| `DAT_MOVTO` | date | S | Data da movimentação. |  |  |
| `HRA_MOVTO` | varchar(8) | S | Hora da movimentação (texto até 8 caracteres, HH:mm:ss). |  |  |
| `NUM_SEQ_MOVTO_ANT` | integer | S | NUM_SEQ_MOVTO da movimentação anterior (encadeamento). |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| `LOG_FLUXO_RET` | bit | S | Movimentação feita por link de retorno. | 1=retorno |  |
| `NUM_SEQ_ESTADO` | integer | S | NUM_SEQ do estado em que a instância entrou nesta movimentação. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_SUB_PROCES` | integer | S | Id do subprocesso (instância filha) associado; 0 quando não é subprocesso. |  |  |
| `NUM_SEQ_THREAD` | integer | S | Sequência da thread (ramo paralelo) da instância. |  | THREAD_PROCES.NUM_SEQ_THREAD |
| `MOVTO_DATE_TIME` | datetime | S | Data e hora completas da movimentação. |  |  |
| `SCRIPT_VERSION` | integer | N | Versão dos scripts de evento do processo vigente na movimentação. |  | EVENT_PROCES.SCRIPT_VERSION |
| `PROCESS_DEFINITION_VERSION` | integer | S | Versão da definição de processo usada na movimentação. |  | VERS_DEF_PROCES.NUM_VERS |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD)` → **THREAD_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD)` · N:1 · logical-probable/probable — Thread da instância.
- `(COD_EMPRESA, NUM_SEQ_CONVER, NUM_SEQ_ESTADO)` → **HISTOR_CONVER_ESTADO** `(COD_EMPRESA, NUM_SEQ_CONVER, NUM_SEQ_ESTADO)` · N:1 · logical-probable/probable — Conversão aplicada.
- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância de processo.
- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO_ANT)` → **HISTOR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` · N:1 · logical-probable/probable — Auto-relação: movimentação anterior.

**Dicas de consulta:** Filtrar sempre por COD_EMPRESA e NUM_PROCES. Ordenar por NUM_SEQ_MOVTO. LOG_ATIV=1 para posição atual.

## HISTOR_TRANSF_PENDCIA

Histórico de transferências de pendências (tarefas) entre usuários (PendencyTransferHistory).

**Ciclo de vida:** Uma linha por transferência de tarefa.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, CD_MATRICULA, NUM_SEQ_TRANSF, SEQ_MOVTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do responsável da pendência transferida. |  | FDN_USER.COLLEAGUE_ID |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequência da movimentação do processo a que a pendência pertence. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| 🔑 `NUM_PROCES` | integer | N | Número da instância de processo. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `SEQ_MOVTO` | integer | N | Sequência do registro de transferência (parte da PK). |  |  |
| 🔑 `NUM_SEQ_TRANSF` | integer | N | Sequência da tarefa transferida (pendência). |  | TAR_PROCES.NUM_SEQ_TRANSF |
| `COD_USUAR_DEST` | varchar(255) | S | Matrícula do usuário que recebeu a tarefa. |  | FDN_USER.COLLEAGUE_ID |
| `COD_USUAR_ORIG` | varchar(255) | S | Matrícula do usuário que transferiu a tarefa. |  | FDN_USER.COLLEAGUE_ID |
| `DTT_TRANSF` | datetime | S | Data e hora da transferência. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` → **TAR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` · N:1 · logical-probable/probable — Tarefa do processo transferida.

**Dicas de consulta:** Dado pessoal: matrículas de origem/destino.

## ICONE

Cadastro de ícones associados a extensões/tipos MIME de arquivos exibidos no GED (Icon).

**Ciclo de vida:** Carga inicial; poucas linhas.

**PK:** COD_EMPRESA, NR_ICONE

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NR_ICONE` | integer | N | Id numérico do ícone. |  |  |
| `COD_EXTENS_ASSOC` | varchar(15) | S | Extensão de arquivo associada ao ícone (ex.: pdf). |  |  |
| `NM_ARQUIVO_ICONE` | varchar(255) | S | Nome do arquivo de imagem do ícone. |  |  |
| `COD_MIME_TYPE` | varchar(120) | S | MIME type associado ao ícone. |  |  |
| `DS_UTILIZACAO` | varchar(2000) | N | Descrição do uso do ícone (obrigatória). |  |  |

## LINK_PROCES

Link (transição/seta) entre dois estados do fluxo de uma versão de processo, com rótulos, tipo e flags de fluxo (ProcessLink).

**Ciclo de vida:** Criada ao modelar o fluxo.

**Atenção:** Índice PROCESLINK02 (COD_EMPRESA, NUM_VERS, NUM_SEQ_ESTADO_INICIAL, COD_DEF_PROCES).

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_LINK` | integer | N | Sequência do link dentro da versão do processo. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `DES_LABEL_ACAO` | varchar(255) | S | Rótulo da ação exibido ao usuário para tomar esta transição. |  |  |
| `LOG_FLUXO_AUTOM` | bit | S | Link automático (seguido pelo motor). | 1=automático |  |
| `LOG_FLUXO_PADRAO` | bit | S | Link padrão (default) de uma decisão. | 1=padrão |  |
| `DES_EXPRESSAO` | varchar(255) | S | Expressão da condição do link. |  |  |
| `NUM_SEQ_ESTADO_FINAL` | integer | S | NUM_SEQ do estado de destino. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_SEQ_ESTADO_INICIAL` | integer | S | NUM_SEQ do estado de origem. |  | ESTADO_PROCES.NUM_SEQ |
| `DES_LABEL_NOME` | varchar(255) | S | Nome/rótulo do link no diagrama. |  |  |
| `DES_LABEL_RET` | varchar(255) | S | Rótulo da ação de retorno. |  |  |
| `LOG_PERMITE_RET` | bit | S | Permite retornar por este link. | 1=permite |  |
| `IDI_FLUXO` | integer | S | Tipo do link. |  |  |
| `MOVEMENT_TITLE` | varchar(70) | S | Título da movimentação gerada ao seguir o link. |  |  |
| `MOVEMENT_DESCRIPTION` | varchar(255) | S | Descrição da movimentação gerada pelo link. |  |  |
| `MOVEMENT_ACCESS_LINK` | varchar(70) | S | Descrição do link de acesso da movimentação. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão do processo.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_ESTADO_INICIAL)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado de origem.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_ESTADO_FINAL)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Estado de destino.

**Dicas de consulta:** Para o grafo, juntar duas vezes a ESTADO_PROCES (inicial/final).

## LINK_PROCES_ASSOC

Associação de um link do processo a um componente gráfico (nota, documento, banco de dados) do diagrama (ProcessLinkAssoc).

**Ciclo de vida:** Criada ao ligar artefatos BPMN a fluxos.

**Atenção:** Nome da coluna Java divergente: NUM_SEQ_COMPON_GRAF é mapeado como initialStateSequence.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_LINK` | integer | N | Sequência do link associado. |  | LINK_PROCES.NUM_SEQ_LINK |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `NUM_SEQ_ESTADO_FINAL` | integer | S | NUM_SEQ do elemento de destino da associação. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_SEQ_COMPON_GRAF` | integer | S | NUM_SEQ do componente gráfico (nota/documento/banco) de origem da associação. |  | COMPON_GRAF_PROCES.NUM_SEQ_COMPON_GRAF |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_COMPON_GRAF)` → **COMPON_GRAF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_COMPON_GRAF)` · N:1 · logical-probable/probable — Componente gráfico da associação.

## LINK_PROCES_BEND

Pontos de curva (dobras) do desenho de um link no diagrama (ProcessLinkBend).

**Ciclo de vida:** Criada ao desenhar o fluxo.

**Atenção:** Somente geometria.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK, NUM_SEQ_CURV

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NUM_SEQ_CURV` | integer | N | Sequência do ponto de curva dentro do link. |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `NUM_SEQ_LINK` | integer | N | Sequência do link ao qual a curva pertence. |  | LINK_PROCES.NUM_SEQ_LINK |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `NUM_POS_X` | integer | S | Posição horizontal (X, em pixels) do elemento no diagrama do processo. |  |  |
| `NUM_POS_Y` | integer | S | Posição vertical (Y, em pixels) do elemento no diagrama do processo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK)` → **LINK_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK)` · N:1 · logical-probable/probable — Link dono da curva.

## LIN_PROCES

Raias (swimlanes), pools e grupos do diagrama de uma versão de processo (SwimLane).

**Ciclo de vida:** Criada ao modelar o processo.

**Atenção:** NUM_SEQ pode ser usado como NUM_SEQ_PAI em ESTADO_PROCES.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK e filtro obrigatório de multi-tenancy. |  |  |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código (processId) da definição de processo BPM a que a linha pertence. |  | VERS_DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | Sequência (id numérico dentro da versão do processo) do estado/atividade do diagrama. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo (versionamento do processo). |  | VERS_DEF_PROCES.NUM_VERS |
| `COD_COR_LIN` | varchar(255) | S | Cor da raia (código/hex). |  |  |
| `NUM_ALT_LIN` | integer | S | Altura da raia em pixels. |  |  |
| `SEQ_PAI` | integer | S | NUM_SEQ da raia/pool pai. |  | LIN_PROCES.NUM_SEQ |
| `NUM_POS_X` | integer | S | Posição horizontal (X, em pixels) do elemento no diagrama do processo. |  |  |
| `NUM_POS_Y` | integer | S | Posição vertical (Y, em pixels) do elemento no diagrama do processo. |  |  |
| `NOM_LIN` | varchar(200) | S | Nome da raia (campo Java stateName). |  |  |
| `TIP_LIN` | integer | S | Tipo da raia (SwimLaneType). | 1=pool;2=simples;3=grupo |  |
| `NUM_LAR_LIN` | integer | S | Largura da raia em pixels. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão do processo.

## MECAN_ATRIBUIC

Cadastro de mecanismos de atribuicao do workflow (quem recebe a tarefa de uma atividade). Inclui mecanismos padrao e customizados com classes de configuracao/controle.

**Ciclo de vida:** Linhas criadas ao cadastrar mecanismo customizado; poucas linhas por tenant.

**Atenção:** PK (COD_EMPRESA, COD_MECAN_ATRIBUIC). IDI_TIP_PROG_CONFIG segue enum AssignmentType.

**PK:** COD_EMPRESA, COD_MECAN_ATRIBUIC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_MECAN_ATRIBUIC` | varchar(25) | N | Codigo identificador do mecanismo de atribuicao (ex.: usado nas atividades do processo). |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `IDI_TIP_PROG_CONFIG` | integer | S | Tipo do mecanismo: padrao ou customizado (enum AssignmentType). | 0=DEFAULT_ASSIGNMENT; 1=CUSTOM_ASSIGNMENT |  |
| `DSL_MECAN_ATRIBUIC` | longtext | S | Descricao longa (LOB) do mecanismo, exibida ao configurar a atividade. |  |  |
| `DES_PROG_CONFIG` | varchar(255) | S | Nome da classe/programa Java de configuracao do mecanismo. |  |  |
| `DES_PROG_CONTROL` | varchar(255) | S | Nome da classe/programa Java que executa a logica de atribuicao. |  |  |
| `DES_MECAN_ATRIBUIC` | varchar(2000) | S | Descricao curta do mecanismo de atribuicao. |  |  |
| `NOM_MECAN_ATRIBUIC` | varchar(50) | S | Nome do mecanismo de atribuicao exibido ao usuario. |  |  |
| `DES_PROG_PRE_SEL` | varchar(255) | S | Nome da classe Java de pre-selecao de usuarios do mecanismo. |  |  |

**Dicas de consulta:** Filtrar por COD_EMPRESA. Referenciado por atividades de processo via codigo do mecanismo.

## PARAM_APLICAT

Parametros de configuracao de aplicativos (cadastro APLICATIVO) por tenant: nome, tipo, valor padrao e se pode variar por usuario.

**Ciclo de vida:** Criada ao cadastrar/configurar aplicativo; baixo volume.

**Atenção:** PK (COD_EMPRESA, COD_APLICAT, NOM_PARAM). Valores por usuario ficam em PARAM_APLICAT_USUAR.

**PK:** COD_EMPRESA, COD_APLICAT, NOM_PARAM

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_APLICAT` | varchar(50) | N | Codigo do aplicativo dono do parametro. |  | APLICATIVO.COD_APLICAT |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NOM_PARAM` | varchar(50) | N | Nome do parametro do aplicativo. |  |  |
| `LOG_FORMAT_SENHA` | bit | S | Indica que o valor deve ser tratado/exibido como senha. | 1=formato senha; 0=texto |  |
| `LOG_VARIAC_USUAR` | bit | S | Indica que o valor pode variar por usuario (override em PARAM_APLICAT_USUAR). | 1=valor por usuario; 0=global | PARAM_APLICAT_USUAR |
| `IDI_TIP_PARAM` | integer | N | Tipo de dado do parametro (campo parameterType); valores nao confirmados. |  |  |
| `VAL_PARAM` | varchar(255) | N | Valor do parametro (padrao/global), em texto. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_APLICAT)` → **APLICATIVO** `(COD_EMPRESA, COD_APLICAT)` · N:1 · logical-probable/probable — Aplicativo dono do parametro.

**Dicas de consulta:** VAL_PARAM pode ser senha quando LOG_FORMAT_SENHA=1 (sensivel). Filtrar por COD_EMPRESA.

## PARAM_APLICAT_USUAR

Valor de parametro de aplicativo especifico de um usuario, sobrepondo o valor padrao de PARAM_APLICAT.

**Ciclo de vida:** Criada quando um usuario personaliza um parametro com LOG_VARIAC_USUAR=1.

**Atenção:** PK (COD_EMPRESA, CD_MATRICULA, NOM_PARAM, COD_APLICAT).

**PK:** COD_EMPRESA, CD_MATRICULA, NOM_PARAM, COD_APLICAT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_APLICAT` | varchar(50) | N | Codigo do aplicativo ao qual o parametro pertence. |  | APLICATIVO.COD_APLICAT |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matricula do usuario dono do valor personalizado. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NOM_PARAM` | varchar(50) | N | Nome do parametro personalizado. |  | PARAM_APLICAT.NOM_PARAM |
| `VAL_PARAM` | varchar(255) | N | Valor do parametro para o usuario. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_APLICAT, NOM_PARAM)` → **PARAM_APLICAT** `(COD_EMPRESA, COD_APLICAT, NOM_PARAM)` · N:1 · logical-probable/probable — Definicao do parametro cujo valor e sobreposto por usuario.

**Dicas de consulta:** Pode conter valores sensiveis (senhas de aplicativo). Fazer join com PARAM_APLICAT por (COD_EMPRESA, COD_APLICAT, NOM_PARAM).

## PENDCIA_NOTIF_EMAIL

Fila de e-mails de notificacao pendentes de envio (assunto, corpo, remetente, destinatarios e template).

**Ciclo de vida:** Linha inserida ao enfileirar notificacao e removida/processada pelo envio; volume transitorio.

**Atenção:** PK (COD_EMPRESA, NUM_SEQ). NUM_SEQ e sequencial proprio, nao FK.

**PK:** COD_EMPRESA, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ` | integer | N | Sequencial da pendencia de e-mail dentro do tenant. |  |  |
| `DAT_CRIAC` | date | S | Data de criacao da pendencia. |  |  |
| `HRA_CRIAC` | varchar(8) | S | Hora de criacao em texto (HH:mm:ss). |  |  |
| `DSL_TEXT_EMAIL` | varchar(2000) | S | Corpo do e-mail a enviar (ate 2000 caracteres). |  |  |
| `DES_TIT_EMAIL` | varchar(255) | S | Assunto do e-mail. |  |  |
| `COD_TEMPL_EMAIL` | varchar(10) | S | Codigo do template de e-mail usado na notificacao. |  |  |
| `DES_EMAIL_DE` | varchar(255) | S | Endereco de e-mail do remetente. |  |  |
| `DES_NOM_DE` | varchar(255) | S | Nome de exibicao do remetente. |  |  |
| `LOG_EMAIL_HTML` | bit | S | Indica se o corpo e HTML. | 1=HTML; 0=texto puro |  |
| `CD_MATR_PARA` | varchar(50) | S | Matricula do usuario destinatario. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `DSL_LISTA_EMAIL_PARA` | varchar(2000) | S | Lista de e-mails destinatarios avulsos, em texto. |  |  |

**Dicas de consulta:** Contem e-mails e nomes (dado pessoal). A relacao inferida com CONTROL_LICENC e falsa.

## PERIOD_EXPED

Periodos de expediente: faixas de horas uteis por dia da semana, usadas no calculo de prazos de workflow.

**Ciclo de vida:** Criada ao cadastrar periodo de expediente; baixo volume.

**Atenção:** PK (COD_EMPRESA, COD_PERIOD_EXPED, NUM_DIA_PERIOD, NUM_SEQ_PERIOD): uma linha por faixa em cada dia.

**PK:** COD_EMPRESA, COD_PERIOD_EXPED, NUM_DIA_PERIOD, NUM_SEQ_PERIOD

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_PERIOD_EXPED` | varchar(50) | N | Codigo do periodo de expediente. |  |  |
| 🔑 `NUM_SEQ_PERIOD` | integer | N | Sequencial da faixa horaria dentro do dia. |  |  |
| 🔑 `NUM_DIA_PERIOD` | integer | N | Dia da semana da faixa (campo weekDay); codificacao exata nao confirmada. |  |  |
| `NUM_HORA_FIM_PERIOD` | integer | S | Hora de fim da faixa, em inteiro (unidade nao confirmada). |  |  |
| `NUM_HORA_INIC_PERIOD` | integer | S | Hora de inicio da faixa, em inteiro (unidade nao confirmada). |  |  |

**Dicas de consulta:** Horas armazenadas como inteiro (unidade provavel: segundos/minutos desde 0h; verificar). Named queries BusinessPeriod.findAll/findByCode.

## PROCESS_APP_CONFIG

Configuracao de mapeamento de campos de aplicativo por atividade de processo (APP_FIELD/APP_KEY) definida na modelagem do processo.

**Ciclo de vida:** Criada ao salvar o processo na modelagem; fixa por versao de processo.

**Atenção:** PK ID. Por versao de processo (PROCESS_ID, PROCESS_VERSION) e atividade (STATE_SEQUENCE).

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Identificador sequencial da configuracao. |  |  |
| `APP_FIELD` | varchar(50) | N | Nome do campo do aplicativo configurado. |  |  |
| `APP_KEY` | varchar(50) | N | Chave do aplicativo associada ao campo. |  |  |
| `DESCRIPTION` | longtext | S | Descricao longa (LOB) da configuracao. |  |  |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `PROCESS_VERSION` | integer | N | Versao da definicao de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `STATE_SEQUENCE` | integer | N | Sequencia da atividade (estado) do processo. |  | ESTADO_PROCES.NUM_SEQ |
| `TENANT_ID` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, PROCESS_VERSION, STATE_SEQUENCE)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade do processo a que a configuracao se aplica.

**Dicas de consulta:** Filtrar por TENANT_ID+PROCESS_ID+PROCESS_VERSION. Valores em runtime ficam em PROCESS_APP_VALUE.

## PROCESS_APP_VALUE

Valores em runtime de campos de aplicativo por instancia e movimentacao de processo.

**Ciclo de vida:** Inserida durante a execucao de instancias de processo.

**Atenção:** PK ID; indice PROCESAPPVALUE02 em (INSTANCE_ID, MOVEMENT_SEQUENCE, TENANT_ID, APP_FIELD, APP_KEY).

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial do valor. |  |  |
| `APP_FIELD` | varchar(50) | N | Nome do campo do aplicativo (ver PROCESS_APP_CONFIG.APP_FIELD). |  | PROCESS_APP_CONFIG.APP_FIELD |
| `APP_KEY` | varchar(50) | N | Chave do aplicativo (ver PROCESS_APP_CONFIG.APP_KEY). |  | PROCESS_APP_CONFIG.APP_KEY |
| `INSTANCE_ID` | int(11) | N | Numero da instancia de processo. |  | PROCES_WORKFLOW.NUM_PROCES |
| `MOVEMENT_SEQUENCE` | int(11) | N | Sequencia da movimentacao da instancia a que o valor pertence. |  | MOVTO_PROCES.NUM_SEQ_MOVTO |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `VALUE` | varchar(4000) | S | Valor gravado (ate 4000 caracteres). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, INSTANCE_ID)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instancia de processo dona do valor.

**Dicas de consulta:** Consultar por TENANT_ID+INSTANCE_ID+MOVEMENT_SEQUENCE.

## PROCESS_ATTACHMENT_RULES

Regras de validacao de anexos por atividade de processo (operador, quantidade, nome do anexo e mensagem de erro).

**Ciclo de vida:** Criada ao salvar processo na modelagem; por versao.

**Atenção:** PK ID; indice PROCESSATTACHMENTRULES01.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da regra. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `PROCESS_VERSION` | integer | N | Versao da definicao de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `STATE_SEQUENCE` | integer | N | Sequencia da atividade onde a regra vale. |  | ESTADO_PROCES.NUM_SEQ |
| `OPERATOR` | integer | N | Operador de comparacao da regra sobre a quantidade de anexos; codificacao nao confirmada. |  |  |
| `AMOUNT` | varchar(255) | S | Quantidade de anexos comparada pelo operador (texto). |  |  |
| `NAME` | varchar(255) | S | Nome do anexo ao qual a regra se aplica. |  |  |
| `MESSAGE` | varchar(4000) | S | Mensagem exibida quando a regra e violada. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, PROCESS_VERSION, STATE_SEQUENCE)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade do processo onde a regra e aplicada.

**Dicas de consulta:** Consultar por TENANT_ID+PROCESS_ID+PROCESS_VERSION+STATE_SEQUENCE.

## PROCESS_COND_AUTOMATIC_RULES

Condicoes das regras de transicao automatica de atividade (campo, operador, valor), agrupadas por expressao e ordem.

**Ciclo de vida:** Criada ao salvar processo na modelagem; por versao.

**Atenção:** PK ID; indice ESTADOPROCESSCONDRULE. Coluna PROCESS_VERSION mapeia 'version'; STATE_SEQUENCE mapeia 'sequence'.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Identificador sequencial da condicao. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `PROCESS_VERSION` | integer | N | Versao da definicao de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `STATE_SEQUENCE` | integer | N | Sequencia da atividade com a regra automatica. |  | ESTADO_PROCES.NUM_SEQ |
| `EXPRESSION_ORDER` | integer | N | Ordem da expressao (grupo) dentro da atividade. |  |  |
| `RULE_ORDER` | integer | N | Ordem da condicao dentro da expressao. |  |  |
| `OPERATOR` | integer | N | Operador de comparacao; codificacao nao confirmada. |  |  |
| `FIELD` | varchar(255) | N | Campo avaliado pela condicao. |  |  |
| `RULE_VALUE` | varchar(255) | S | Valor comparado (fixo ou nome de campo conforme VALUE_TYPE). |  |  |
| `VALUE_TYPE` | integer | S | Tipo do valor comparado. | 0=BY_FORM_VALUE_TYPE (valor vem de campo do formulario); 1=FIX_VALUE_TYPE (valor fixo) |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, PROCESS_VERSION, STATE_SEQUENCE)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade com regra automatica.

**Dicas de consulta:** VALUE_TYPE define se RULE_VALUE e fixo ou campo do formulario.

## PROCESS_CUSTOM_TRANSLATE

Traducoes customizadas (chave/descricao) por idioma de uma versao de processo.

**Ciclo de vida:** Criada ao salvar traducoes do processo; por versao.

**Atenção:** PK ID; indice PROCESSCUSTOMTRANSLATE01.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da traducao. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo traduzida. |  | PROCES.COD_DEF_PROCES |
| `LANGUAGE` | varchar(5) | N | Codigo do idioma da traducao (ate 5 caracteres, ex.: pt_BR). |  |  |
| `VERSION` | int(11) | N | Versao do processo a que a traducao pertence. |  | VERS_DEF_PROCES.NUM_VERS |
| `TRANSLATE_KEY` | varchar(255) | S | Chave customizada a ser traduzida. |  |  |
| `DESCRIPTION` | varchar(4000) | S | Texto traduzido para a chave no idioma. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, VERSION)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versao do processo traduzida.

**Dicas de consulta:** Coluna TRANSLATE_KEY mapeia o campo 'key'. LANGUAGE ex.: pt_BR, en_US.

## PROCESS_DEFINITION_TRANSLATE

Traducao por idioma de descricao, instrucao e categoria da definicao de processo.

**Ciclo de vida:** Criada ao salvar traducoes do processo.

**Atenção:** PK ID; indice PROCESSDEFINITIONTRANSLATE01. Nao versionada.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da traducao. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `LANGUAGE` | varchar(5) | N | Codigo do idioma (ex.: pt_BR). |  |  |
| `DESCRIPTION` | varchar(250) | S | Descricao do processo traduzida. |  |  |
| `INSTRUCTION` | varchar(2000) | S | Instrucao do processo traduzida. |  |  |
| `CATEGORY` | varchar(250) | S | Nome da categoria do processo traduzido (campo categoryId). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-probable/probable — Definicao de processo traduzida.

**Dicas de consulta:** Ver tambem PROCESS_VERSION_TRANSLATE para textos por versao.

## PROCESS_ELEMENT_TRANSLATE

Traducao por idioma de elementos (atividades) do processo: nome, rotulos de acao, titulo/descricao de movimentacao e instrucao.

**Ciclo de vida:** Criada ao salvar traducoes do processo; por versao.

**Atenção:** PK ID; indice PROCESSELEMENTTRANSLATE01. Named query findProcessElementTranslate.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da traducao. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `LANGUAGE` | varchar(5) | N | Codigo do idioma (ex.: pt_BR). |  |  |
| `SEQUENCE` | int(11) | N | Sequencia da atividade/elemento do processo traduzido. |  | ESTADO_PROCES.NUM_SEQ |
| `VERSION` | int(11) | N | Versao do processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `NAME` | varchar(255) | S | Nome da atividade traduzido. |  |  |
| `ACTION_LABEL` | varchar(255) | S | Rotulo traduzido do botao de acao (enviar) da atividade. |  |  |
| `RETURN_LABEL` | varchar(255) | S | Rotulo traduzido da acao de retorno. |  |  |
| `MOVEMENT_TITLE` | varchar(70) | S | Titulo traduzido da movimentacao (max 70 caracteres). |  |  |
| `MOVEMENT_DESCRIPTION` | varchar(255) | S | Descricao traduzida da movimentacao. |  |  |
| `MOVEMENT_ACCESS_LINK` | varchar(70) | S | Descricao traduzida do link de acesso da movimentacao. |  |  |
| `INSTRUCTION` | varchar(4000) | S | Instrucao traduzida da atividade. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, VERSION, SEQUENCE)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade traduzida.

**Dicas de consulta:** SEQUENCE e a sequencia da atividade (ESTADO_PROCES.NUM_SEQ).

## PROCESS_FORM_MAP

Mapeamento de campos de formulario entre processo pai e subprocesso, por atividade.

**Ciclo de vida:** Criada ao configurar atividade de subprocesso na modelagem.

**Atenção:** PK FORM_MAP_ID (gerado). Por versao de processo pai.

**PK:** FORM_MAP_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `FORM_MAP_ID` | bigint | N | Identificador sequencial do mapeamento. |  |  |
| `MAP_FLOW` | integer | N | Direcao do mapeamento entre pai e subprocesso; codificacao nao confirmada. |  |  |
| `PROCESS_CODE` | varchar(255) | N | Codigo do processo pai. |  | PROCES.COD_DEF_PROCES |
| `PROCESS_FIELD` | varchar(255) | N | Campo do formulario do processo pai. |  |  |
| `STATE_SEQUENCE` | integer | N | Sequencia da atividade de subprocesso no processo pai. |  | ESTADO_PROCES.NUM_SEQ |
| `SUB_PROCESS_CODE` | varchar(255) | N | Codigo do subprocesso. |  | PROCES.COD_DEF_PROCES |
| `SUB_PROCESS_FIELD` | varchar(255) | N | Campo do formulario do subprocesso. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `VERSION` | integer | N | Versao do processo pai. |  | VERS_DEF_PROCES.NUM_VERS |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_CODE, VERSION, STATE_SEQUENCE)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade de subprocesso do processo pai.

**Dicas de consulta:** MAP_FLOW indica direcao (pai->sub ou sub->pai); codificacao nao confirmada.

## PROCESS_INSTANCE_MANAGER

Cache de usuarios gestores/participantes associados a uma instancia de processo, com data de cache.

**Ciclo de vida:** Inserida/atualizada ao calcular o gestor da instancia; transitoria.

**Atenção:** PK ID; indice PROCESSINSTANCEMANAGER02.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `INSTANCE_ID` | int(11) | N | Numero da instancia de processo. |  | PROCES_WORKFLOW.NUM_PROCES |
| `USER_ID` | varchar(150) | N | Codigo/matricula do usuario gestor da instancia. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `CACHE_DATE` | datetime | S | Data/hora em que a linha foi gravada no cache. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, INSTANCE_ID)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instancia de processo.

**Dicas de consulta:** USER_ID e codigo do usuario (nao a PK de FDN_USER); a relacao inferida por nome nao se aplica diretamente.

## PROCESS_OBSERVATION

Observacoes e historico de anexos de uma instancia de processo, por atividade/thread/movimentacao (informacao, erro, inclusao/alteracao/exclusao de anexo).

**Ciclo de vida:** Inserida durante a execucao de instancias (movimentacoes, anexos); volume alto.

**Atenção:** PK OBSERVATION_ID. TENANT_ID mapeia companyId. Indice PROCESOBSERVATION01 (NUM_PROCESS, NUM_SEQ).

**PK:** OBSERVATION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OBSERVATION_ID` | bigint | N | Identificador sequencial da observacao. |  |  |
| `COLLEAGUE_ID` | varchar(255) | N | Matricula do usuario autor da observacao. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `TENANT_ID` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `MOV_SEQ` | integer | S | Sequencia da movimentacao do processo associada. |  | MOVTO_PROCES.NUM_SEQ_MOVTO |
| `OBSERVATION` | longtext | S | Texto (LOB) da observacao. |  |  |
| `DT_OBSERVATION` | datetime | N | Data/hora de registro da observacao. |  |  |
| `OBS_TYPE` | integer | S | Tipo da observacao (enum ProcessObservationType). | 0=INFO; 1=ERROR; 2=ATTACH_INSERT; 3=ATTACH_UPDATE; 4=ATTACH_DELETE |  |
| `NUM_PROCESS` | integer | N | Numero da instancia de processo. |  | PROCES_WORKFLOW.NUM_PROCES |
| `NUM_SEQ` | integer | N | Sequencia da atividade (estado) do processo onde a observacao ocorreu. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_THREAD` | integer | N | Sequencia da thread do processo. |  | THREAD_PROCES.NUM_SEQ_THREAD |
| `FILE_NAME` | varchar(4000) | S | Nome do arquivo anexo quando a observacao e de anexo. |  |  |
| `NR_VERSAO` | integer | S | Versao do documento anexo. |  | DOCUMENTO.NR_VERSAO |
| `NR_DOCUMENTO` | integer | S | Numero do documento do GED anexado. |  | DOCUMENTO.NR_DOCUMENTO |
| `REPLACEMENT_ID` | varchar(150) | S | Matricula do substituto que agiu em nome do usuario, quando houve substituicao. |  | FDN_USERTENANT.USER_CODE (via matricula) |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, NUM_PROCESS)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instancia de processo observada.

**Dicas de consulta:** NUM_SEQ e a sequencia da atividade, nao FK para CONTROL_LICENC. OBS_TYPE segue enum ProcessObservationType.

## PROCESS_VERSION_TRANSLATE

Traducao por idioma e versao de descricao, instrucao, instrucao de versao e categoria do processo.

**Ciclo de vida:** Criada ao salvar traducoes da versao do processo.

**Atenção:** PK ID; indice PROCESSVERSIONTRANSLATE01.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da traducao. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| `PROCESS_ID` | varchar(50) | N | Codigo da definicao de processo. |  | PROCES.COD_DEF_PROCES |
| `LANGUAGE` | varchar(5) | N | Codigo do idioma (ex.: pt_BR). |  |  |
| `VERSION` | int(11) | N | Versao do processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `DESCRIPTION` | varchar(250) | S | Descricao da versao traduzida. |  |  |
| `INSTRUCTION` | varchar(2000) | S | Instrucao do processo traduzida. |  |  |
| `VERSION_INSTRUCTION` | varchar(2000) | S | Instrucao especifica da versao traduzida. |  |  |
| `CATEGORY` | varchar(250) | S | Categoria do processo traduzida (campo categoryId). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, PROCESS_ID, VERSION)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versao do processo traduzida.

**Dicas de consulta:** Complementa PROCESS_DEFINITION_TRANSLATE (nivel definicao).

## PROCES_SIGNAL

Cadastro de sinais (eventos de sinal BPMN) que processos podem emitir e aguardar.

**Ciclo de vida:** Criada ao definir sinal; baixo volume.

**Atenção:** PK (COD_EMPRESA, COD_SINAL). Named query Signal.findAll.

**PK:** COD_EMPRESA, COD_SINAL

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_SINAL` | integer | N | Codigo numerico do sinal. |  |  |
| `DES_SINAL` | varchar(200) | S | Descricao/nome do sinal. |  |  |

## PROCES_SIGNAL_INSTANCE

Ocorrencias de sinal emitidas por instancias de processo, com dados do sinal e atividade de origem.

**Ciclo de vida:** Inserida quando uma atividade emite um sinal.

**Atenção:** PK (COD_EMPRESA, COD_SINAL, COD_SINAL_INSTANCE).

**PK:** COD_EMPRESA, COD_SINAL, COD_SINAL_INSTANCE

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_SINAL` | integer | N | Codigo do sinal emitido. |  | PROCES_SIGNAL.COD_SINAL |
| 🔑 `COD_SINAL_INSTANCE` | integer | N | Sequencial da ocorrencia do sinal. |  |  |
| `COD_DEF_PROCES` | varchar(50) | S | Codigo da definicao do processo que emitiu o sinal. |  | PROCES.COD_DEF_PROCES |
| `NUM_PROCES` | integer | S | Numero da instancia de processo emissora. |  | PROCES_WORKFLOW.NUM_PROCES |
| `DES_SINAL_DATA` | varchar(200) | S | Dados/payload do sinal (ate 200 caracteres). |  |  |
| `NUM_SEQ` | integer | S | Sequencia da atividade que emitiu o sinal. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_VERS` | integer | S | Versao da definicao de processo. |  | VERS_DEF_PROCES.NUM_VERS |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_SINAL)` → **PROCES_SIGNAL** `(COD_EMPRESA, COD_SINAL)` · N:1 · logical-probable/probable — Sinal emitido.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade emissora do sinal.
- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instancia emissora do sinal.

**Dicas de consulta:** Origem do sinal: COD_DEF_PROCES+NUM_VERS+NUM_SEQ (atividade) e NUM_PROCES (instancia).

## PROCES_SIGNAL_RECEIVERS

Receptores de sinal: threads de instancias de processo aguardando um sinal em uma atividade de captura.

**Ciclo de vida:** Inserida quando a atividade passa a aguardar sinal; LOG_ATIV controla se ainda ativa.

**Atenção:** PK de 7 colunas (tenant, processo, versao, atividade, sinal, instancia, thread).

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, COD_SINAL, NUM_PROCES, NUM_SEQ_THREAD

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Codigo da definicao do processo receptor. |  | PROCES.COD_DEF_PROCES |
| 🔑 `NUM_PROCES` | integer | N | Numero da instancia de processo que aguarda o sinal. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `COD_SINAL` | integer | N | Codigo do sinal aguardado. |  | PROCES_SIGNAL.COD_SINAL |
| 🔑 `NUM_SEQ` | integer | N | Sequencia da atividade receptora. |  | ESTADO_PROCES.NUM_SEQ |
| 🔑 `NUM_SEQ_THREAD` | integer | N | Sequencia da thread da instancia que aguarda. |  | THREAD_PROCES.NUM_SEQ_THREAD |
| 🔑 `NUM_VERS` | integer | N | Versao da definicao do processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `LOG_ATIV` | bit | S | Indica se o receptor segue ativo aguardando o sinal. | 1=ativo; 0=encerrado |  |
| `CD_MATRICULA` | varchar(255) | S | Matricula do usuario associado ao receptor (responsavel). |  | FDN_USERTENANT.USER_CODE (via matricula) |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_SINAL)` → **PROCES_SIGNAL** `(COD_EMPRESA, COD_SINAL)` · N:1 · logical-probable/probable — Sinal aguardado.
- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` → **ESTADO_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ)` · N:1 · logical-probable/probable — Atividade receptora.
- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD)` → **THREAD_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD)` · N:1 · logical-probable/probable — Thread da instancia aguardando.

**Dicas de consulta:** Filtrar LOG_ATIV=1 para receptores ainda aguardando. Join com PROCES_SIGNAL por (COD_EMPRESA, COD_SINAL).

## PROCES_WORKFLOW

Instancia (solicitacao) de processo de workflow: dados de abertura, solicitante, prazo, status e vinculo com a versao da definicao e com o formulario.

**Ciclo de vida:** Uma linha por solicitacao, criada ao iniciar o processo; atualizada em andamento e ao encerrar/cancelar. Tabela central e de alto volume.

**Atenção:** PK (COD_EMPRESA, NUM_PROCES). LOG_ATIV indica instancia aberta. Muitas tabelas de workflow referenciam NUM_PROCES.

**PK:** COD_EMPRESA, NUM_PROCES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROCES` | integer | N | Numero da instancia de processo (numero da solicitacao). |  |  |
| `LOG_ATIV` | bit | S | Indica se a instancia ainda esta ativa (aberta). | 1=ativa; 0=encerrada |  |
| `NUM_SEQ_ANEXO_PRINC` | integer | S | Sequencia do anexo principal da solicitacao. |  |  |
| `NR_DOCUMENTO_CARD` | integer | S | Numero do documento de registro (card) de formulario associado. |  | DOCUMENTO.NR_DOCUMENTO |
| `NR_DOCUMENTO_CARD_INDEX` | integer | S | Numero do documento do fichario (card index) do formulario. |  | DOCUMENTO.NR_DOCUMENTO |
| `CLOSURE_STATUS` | integer | S | Situacao do prazo da instancia (enum WorkflowProcessClosureStatus). | 0=OPEN; 1=ON_TIME; 2=WARNING; 3=EXPIRED |  |
| `DEADLINE_DATE` | datetime | S | Data/hora limite (prazo) da instancia. |  |  |
| `END_DATE` | datetime | S | Data/hora de encerramento da instancia. |  |  |
| `NOTIFY_DELAY` | bit | N | Indica se a notificacao de atraso ja foi/deve ser enviada. | 1=sim; 0=nao |  |
| `PERIOD_ID` | varchar(255) | S | Codigo do periodo de expediente usado no calculo de prazo. |  | PERIOD_EXPED.COD_PERIOD_EXPED |
| `COD_DEF_PROCES` | varchar(50) | S | Codigo da definicao do processo instanciado. |  | PROCES.COD_DEF_PROCES |
| `COD_MATR_REQUISIT` | varchar(150) | S | Matricula do solicitante que abriu a instancia. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `NUM_PROCES_ORIG` | integer | S | Numero da instancia pai quando esta e um subprocesso. |  | PROCES_WORKFLOW.NUM_PROCES |
| `NUM_SEQ_THREAD_ORIG` | integer | S | Sequencia da thread do processo pai que originou o subprocesso. |  | THREAD_PROCES.NUM_SEQ_THREAD |
| `START_DATE` | datetime | S | Data/hora de abertura da instancia. |  |  |
| `STATUS` | integer | S | Situacao da instancia; codigos nao confirmados nos fontes lidos (provavel: aberta/cancelada/finalizada). |  |  |
| `TOTAL_DEADLINE` | integer | S | Prazo total da instancia, em unidade nao confirmada (provavel segundos/minutos). |  |  |
| `TOTAL_RUNTIME` | bigint | S | Tempo total de execucao acumulado, em unidade nao confirmada. |  |  |
| `TOTAL_WARNING` | integer | S | Tempo total ate o aviso de prazo, em unidade nao confirmada. |  |  |
| `COD_UUID` | varchar(36) | S | UUID da instancia (36 caracteres). |  |  |
| `NUM_VERS` | integer | S | Versao da definicao de processo usada. |  | VERS_DEF_PROCES.NUM_VERS |
| `WARNING_DATE` | datetime | S | Data/hora em que o prazo entra em aviso. |  |  |
| `SCRIPT_VERSION` | integer | N | Versao do script de processo aplicada a instancia (NOT NULL). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versao da definicao de processo da instancia.
- `(COD_EMPRESA, NUM_PROCES_ORIG)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instancia pai (subprocesso).
- `(COD_EMPRESA)` → **ANEXO_PROCES** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — ProcessAttachment.countByProcessInstance
- `(NUM_PROCES)` → **ANEXO_PROCES** `(NUM_PROCES)` · N:1 · hql-join/confirmed — ProcessAttachment.countByProcessInstance

**Dicas de consulta:** Filtrar sempre por COD_EMPRESA. Para abertas use LOG_ATIV=1; indices WORKFLOWPROCES01-06 favorecem filtros por COD_DEF_PROCES, STATUS, CLOSURE_STATUS, DEADLINE_DATE. Contem matricula do solicitante.

## TAR_CONHECIMENTO_USUARIO

Registra que um usuário tomou conhecimento (ciência) de uma tarefa de processo transferida/atribuída, por movimentação e sequência de transferência.

**Ciclo de vida:** Linha inserida quando o usuário registra ciência da tarefa; mantida enquanto a instância existir.

**Atenção:** PK espelha a de TAR_PROCES (sem tabela de dados adicional). Entidade UserKnowledgeTask.

**PK:** COD_EMPRESA, NUM_PROCES, CD_MATRICULA, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que tomou conhecimento da tarefa. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequência da movimentação (etapa) da instância. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| 🔑 `NUM_PROCES` | integer | N | Número da instância (solicitação) de processo de workflow. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ_TRANSF` | integer | N | Sequência de transferência da tarefa (0 = original). |  | TAR_PROCES.NUM_SEQ_TRANSF |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` → **TAR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA)` · 1:1 · logical-probable/probable — Mesma PK da tarefa de processo do usuário.
- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` → **HISTOR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` · N:1 · logical-probable/probable — Movimentação do processo.

**Dicas de consulta:** Join por todas as 5 colunas da PK com TAR_PROCES.

## TAR_PROCES

Atribuição de tarefa de processo a um usuário: uma linha por usuário responsável por uma etapa (movimentação) de uma instância, com status, prazos, avisos de atraso e conclusão. Base da central de tarefas do workflow.

**Ciclo de vida:** Criada quando a etapa é atribuída a um usuário (ou transferida); atualizada ao concluir, transferir ou cancelar. Volume alto (cresce com as instâncias).

**Atenção:** PK composta de 5 colunas; NUM_SEQ_TRANSF distingue transferências. Colunas DEADLINEDATE/DEADLINEHOUR/INITIALTERMDATE/INITIALTERMHOUR/TASKCOMPLETIONDATE/TASKCOMPLETIONHOUR são legadas (@Deprecated); usar DEADLINE/START_DATE/END_DATE. Tarefas abertas: IDI_STATUS<=1 e LOG_ATIV=1.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário atribuído à tarefa (responsável). |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequência da movimentação (etapa) da instância à qual a tarefa pertence. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| 🔑 `NUM_PROCES` | integer | N | Número da instância (solicitação) de processo de workflow. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ_TRANSF` | integer | N | Sequência de transferência da atribuição (0 = atribuição original, >0 = transferida). |  |  |
| `LOG_ATIV` | bit | S | Indica se a atribuição está ativa (tarefa corrente do usuário). | 1=ativa; 0=inativa/histórico |  |
| `ASSIGN_START_DATE` | datetime | S | Data/hora em que a tarefa foi atribuída ao usuário. |  |  |
| `ASSIGN_END_DATE` | datetime | S | Data/hora em que a atribuição terminou (conclusão, transferência ou cancelamento). |  |  |
| `DAT_MSG_ATRASO_RESPONS` | date | S | Data do envio da mensagem de atraso ao responsável. |  |  |
| `NUM_HORA_MSG_ATRASO_RESPONS` | integer | S | Hora do envio da mensagem de atraso ao responsável. |  |  |
| `COD_MATR_ESCOLHID` | longtext | S | Matrículas escolhidas para a próxima atribuição (lista serializada). |  | FDN_USERTENANT.USER_CODE |
| `NUM_SEQ_ESCOLHID` | integer | S | Sequência da etapa escolhida para o próximo destino. |  |  |
| `CLOSURE_STATUS` | integer | S | Situação do prazo da tarefa (enum WorkflowProcessClosureStatus). | 0=OPEN; 1=ON_TIME; 2=WARNING; 3=EXPIRED |  |
| `CD_MATRICULA_CONCLUS` | varchar(150) | S | Matrícula de quem efetivamente concluiu a tarefa (pode ser substituto ou gestor). |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| `IDI_TIP_CONCLUS` | integer | S | Tipo de conclusão: por quem a tarefa foi concluída (enum ProcessTaskCompleteType). | 0=MANAGER; 1=REPLACEMENT; 2=REPLACEMENT_MANAGER |  |
| `DEADLINE` | datetime | S | Data/hora limite (prazo) da tarefa. |  |  |
| `DEADLINEDATE` | datetime | S | Legado: data do prazo (campo deprecated, separado de hora). |  |  |
| `DEADLINEHOUR` | integer | S | Legado: hora do prazo (deprecated). |  |  |
| `END_DATE` | datetime | S | Data/hora de término da tarefa. |  |  |
| `INITIALTERMDATE` | datetime | S | Legado: data inicial do prazo (deprecated). |  |  |
| `INITIALTERMHOUR` | integer | S | Legado: hora inicial do prazo (deprecated). |  |  |
| `DAT_MSG_ATRASO_GESTOR` | date | S | Data do envio da mensagem de atraso ao gestor. |  |  |
| `NUM_HORA_MSG_ATRASO_GESTOR` | integer | S | Hora do envio da mensagem de atraso ao gestor. |  |  |
| `DAT_MSG_EXPIRAC_RESPONS` | date | S | Data do aviso de expiração enviado ao responsável. |  |  |
| `NUM_HORA_MSG_EXPIRAC_RESPONS` | integer | S | Hora do aviso de expiração enviado ao responsável. |  |  |
| `DAT_MSG_EXPIRAC_GESTOR` | date | S | Data do aviso de expiração enviado ao gestor. |  |  |
| `NUM_HORA_MSG_EXPIRAC_GESTOR` | integer | S | Hora do aviso de expiração enviado ao gestor. |  |  |
| `DAT_MSG_EXPIRAC_REQUISIT` | date | S | Data do aviso de expiração enviado ao requisitante. |  |  |
| `NUM_HORA_MSG_EXPIRAC_REQUISIT` | integer | S | Hora do aviso de expiração enviado ao requisitante. |  |  |
| `DAT_MSG_ATRASO_REQUISIT` | date | S | Data do envio da mensagem de atraso ao requisitante. |  |  |
| `NUM_HORA_MSG_ATRASO_REQUISIT` | integer | S | Hora do envio da mensagem de atraso ao requisitante. |  |  |
| `START_DATE` | datetime | S | Data/hora de início do prazo/execução da tarefa. |  |  |
| `IDI_STATUS` | integer | S | Status da tarefa (enum ProcessTaskStatusType). | 0=NOT_COMPLETED; 1=PENDING_CONSENSUS; 2=COMPLETED; 3=TRANSFERRED; 4=CANCELED |  |
| `TASKCOMPLETIONDATE` | datetime | S | Legado: data de conclusão (deprecated); preferir END_DATE. |  |  |
| `TASKCOMPLETIONHOUR` | integer | S | Legado: hora de conclusão (deprecated). |  |  |
| `DSL_OBS_TAR` | longtext | S | Observação textual registrada na tarefa (longtext). |  |  |
| `LOG_ASSINADO` | bit | S | Indica se a tarefa foi assinada digitalmente. | 1=assinada; 0=não |  |
| `DS_ARQUIVO_HASH` | varchar(255) | S | Hash do arquivo de assinatura da tarefa. |  |  |
| `DS_NOME_ARQUIVO_ASS` | varchar(255) | S | Nome do arquivo de assinatura da tarefa. |  |  |
| `WARNING_DATE` | datetime | S | Data/hora a partir da qual a tarefa entra em alerta de prazo. |  |  |
| `TOTAL_RUNTIME` | bigint(20) | S | Tempo total de execução da tarefa, em milissegundos. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · hql-join/confirmed — Instância de processo à qual a tarefa pertence (join em queries HQL).
- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` → **HISTOR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` · N:1 · logical-probable/probable — Movimentação (etapa) atribuída; sem FK física.
- `(CD_MATRICULA)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Usuário responsável. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]
- `(COD_EMPRESA)` → **PROCES_WORKFLOW** `(COD_EMPRESA)` · N:1 · hql-join/confirmed — WorkflowProcess.findPending
- `(NUM_PROCES)` → **PROCES_WORKFLOW** `(NUM_PROCES)` · N:1 · hql-join/confirmed — WorkflowProcess.findPending

**Dicas de consulta:** Filtrar por COD_EMPRESA. Tarefas pendentes do usuário: LOG_ATIV=1 AND IDI_STATUS IN (0,1) (índice PROCESSTASK04). Colunas DATE de aviso e hora são separadas. DSL_OBS_TAR é longtext. DS_NOME_ARQUIVO_ASS/DS_ARQUIVO_HASH ligados a assinatura.

## THREAD_PROCES

Threads paralelas (fork/join) de uma instância de processo: cada linha representa um ramo paralelo ativo ou finalizado.

**Ciclo de vida:** Criada quando o processo bifurca em atividades paralelas; marcada inativa ao juntar. Volume proporcional às instâncias com paralelismo.

**Atenção:** NUM_SEQ_THREAD identifica a thread dentro da instância.

**PK:** COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROCES` | integer | N | Número da instância (solicitação) de processo de workflow. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `NUM_SEQ_THREAD` | integer | N | Sequência da thread paralela dentro da instância. |  |  |
| `LOG_ATIV` | bit | S | Indica se a thread está ativa. | 1=ativa; 0=encerrada |  |
| `COD_MATR_ESCOLHID` | longtext | S | Matrículas escolhidas para a atribuição da thread (lista serializada). |  | FDN_USERTENANT.USER_CODE |
| `NUM_SEQ_ESCOLHID` | integer | S | Sequência da atividade escolhida para a thread. |  |  |
| `NUM_SEQ_MOVTO_FORK` | integer | N | Sequência da movimentação em que ocorreu o fork. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| `NUM_SEQ_MOVTO_THREAD` | integer | N | Sequência da movimentação corrente da thread. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_PROCES)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Instância dona da thread.

**Dicas de consulta:** Consultar por (COD_EMPRESA, NUM_PROCES); COD_MATR_ESCOLHID é longtext.

## VAL_HORA_COLAB

Histórico do valor da hora de trabalho de um colaborador, usado para custeio de tarefas/processos; cada linha vale a partir do momento da atualização.

**Ciclo de vida:** Nova linha a cada alteração do valor-hora; mantém histórico. Volume baixo.

**Atenção:** Dado financeiro/sensível. Valor vigente = linha ativa mais recente.

**PK:** COD_EMPRESA, DAT_ATUALIZ, HRA_ATUALIZ, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do colaborador ao qual o valor-hora pertence. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `DAT_ATUALIZ` | date | N | Data da atualização do valor-hora. |  |  |
| 🔑 `HRA_ATUALIZ` | varchar(8) | N | Hora da atualização, texto (formato HH:mm:ss ou similar). |  |  |
| `LOG_ATIV` | bit | S | Indica se o registro é o valor vigente. | 1=ativo; 0=histórico |  |
| `CD_MATRICULA_RESPONS` | varchar(150) | S | Matrícula do responsável que registrou a alteração. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| `VAL_HORA` | double | S | Valor monetário da hora do colaborador. |  |  |

**Relacionamentos (saem desta tabela):**

- `(CD_MATRICULA)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Colaborador. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Informação salarial sensível. Named query: findAll.

## VERBOSE_SCRIPT_LOG

Registra habilitação do log detalhado (verbose) de scripts para um item (ex.: uma instância de processo) solicitada por um usuário.

**Ciclo de vida:** Linha criada quando o usuário ativa o log verboso; consultada pelo motor ao executar scripts. Volume baixo.

**Atenção:** Usa TENANT_ID. Único tipo definido: SCRIPT_TYPE=1 (PROCESS_INSTANCE), onde IDENTIFIER é o número da instância.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Chave primária gerada do registro. |  |  |
| `TENANT_ID` | bigint | N | Tenant/empresa. |  | FDN_TENANT.TENANT_ID |
| `SCRIPT_TYPE` | integer | N | Tipo do alvo do log verboso, enum VerboseScriptLogType. | 1=PROCESS_INSTANCE |  |
| `IDENTIFIER` | integer | N | Identificador do alvo conforme SCRIPT_TYPE (para tipo 1, NUM_PROCES da instância). |  | PROCES_WORKFLOW.NUM_PROCES |
| `USER_ID` | varchar(255) | N | Usuário que solicitou o log verboso. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| `CREATE_DATE` | datetime | N | Data/hora de criação do registro. |  |  |

**Relacionamentos (saem desta tabela):**

- `(USER_ID)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — USER_ID guarda o código do usuário (varchar), não o USER_ID numérico de FDN_USER; a heurística por nome é enganosa. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]
- `(TENANT_ID, IDENTIFIER)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · N:1 · logical-probable/probable — Quando SCRIPT_TYPE=1, IDENTIFIER é a instância.

**Dicas de consulta:** Filtrar por TENANT_ID e SCRIPT_TYPE. Índice VERBOSESCRIPTLOG01 (TENANT_ID, SCRIPT_TYPE, IDENTIFIER).
