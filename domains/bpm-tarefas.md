# Domínio: bpm-tarefas

7 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## TAR_CTRAL

Tabela raiz (herança JOINED, entidade Task) das tarefas do gerenciador de tarefas: um registro por tarefa com dono, prazo e status. Subtipos em TAR_DOCTO, TAR_ESFOR, TAR_PARTIC, TAR_WORKFLOW.

**Ciclo de vida:** Criada ao gerar uma tarefa (workflow, documento, to-do); atualizada na conclusão. Volume médio a alto.

**Atenção:** Herança JOINED: o tipo é determinado pela existência de linha na tabela filha (mesma PK COD_EMPRESA+COD_TAREFA). Não confundir com TAR_PROCES (atribuições de processo).

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código sequencial da tarefa dentro da empresa (gerado via SEQ_ECM). |  | SEQ_ECM.CD_TABELA |
| `DAT_CONCLUS_TAR` | date | S | Data efetiva de conclusão da tarefa. |  |  |
| `NUM_HRS_CONCLUS_TAR` | integer | S | Hora de conclusão da tarefa, inteiro de hora (formato interno do Fluig). |  |  |
| `DAT_CRIACAO` | date | S | Data de criação da tarefa. |  |  |
| `NUM_HRS_CRIACAO` | integer | S | Hora de criação da tarefa (inteiro). |  |  |
| `NUM_HRS_PRAZ` | integer | S | Prazo da tarefa em horas. |  |  |
| `DES_TAREFA` | varchar(2000) | S | Descrição/título da tarefa. |  |  |
| `DAT_FIM_PRAZ` | date | S | Data limite prevista para conclusão. |  |  |
| `CD_MATRICULA` | varchar(150) | S | Matrícula do dono (responsável) da tarefa. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| `IDI_STATUS` | integer | S | Status da tarefa (enum TaskStatus, ordinal). | 0=New; 1=Consensus; 2=Completed; 3=Transferred; 4=Cancelled; 5=Started; 6=Paused |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_DOCTO** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · jpa-join/confirmed — Subtipo tarefa de documento.
- `(COD_EMPRESA, COD_TAREFA)` → **TAR_ESFOR** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Subtipo tarefa de esforço registrado.
- `(COD_EMPRESA, COD_TAREFA)` → **TAR_PARTIC** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Subtipo tarefa to-do.
- `(COD_EMPRESA, COD_TAREFA)` → **TAR_WORKFLOW** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · jpa-join/confirmed — Subtipo tarefa de workflow.

**Dicas de consulta:** Índice CENTRAL_TC (COD_EMPRESA, CD_MATRICULA, IDI_STATUS, NUM_HRS_CONCLUS_TAR) atende a central de tarefas. Datas e horas são separadas (DATE + int).

## TAR_DOCTO

Subtipo de tarefa (herança JOINED de Task) ligado a um documento específico do GED; base para tarefas de edição e revisão de documento.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Herança JOINED: PK = FK para TAR_CTRAL. Tem subtipos TAR_DOCTO_EDIC e TAR_DOCTO_REVIS.

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `NR_DOCUMENTO` | integer | S | Número do documento do GED associado à tarefa. |  | DOCUMENTO.NR_DOCUMENTO |
| `NR_VERSAO` | integer | S | Versão do documento associada à tarefa. |  | DOCUMENTO.NR_VERSAO |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_CTRAL** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa base (herança JOINED).
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento (versão) alvo da tarefa; sem FK física.

**Dicas de consulta:** Join com TAR_CTRAL para obter dono, prazo e status.

## TAR_DOCTO_EDIC

Subtipo de TAR_DOCTO para tarefas de edição de documento; guarda o documento de destino da edição.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Herança JOINED em dois níveis (TAR_CTRAL > TAR_DOCTO > TAR_DOCTO_EDIC).

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `NUM_DOCTO_DEST` | integer | S | Número do documento de destino da edição. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_DOCTO** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa de documento base.

**Dicas de consulta:** Join via TAR_DOCTO e TAR_CTRAL.

## TAR_DOCTO_REVIS

Subtipo de TAR_DOCTO para tarefas de revisão de documento; sem colunas além da PK.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Tabela marcadora: o tipo de tarefa é indicado apenas pela existência da linha.

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_DOCTO** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa de documento base.

**Dicas de consulta:** Usar para filtrar tarefas de revisão via EXISTS.

## TAR_ESFOR

Subtipo de Task (EffortRecordedTask) para tarefas de esforço registrado; tabela marcadora sem colunas além da PK.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Tipo indicado pela existência da linha.

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_CTRAL** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa base.
- `(COD_EMPRESA, COD_TAREFA)` → **TAR_WORKFLOW** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · jpa-join/confirmed — TAR_WORKFLOW herda de TAR_ESFOR (FK de TAR_WORKFLOW aponta para esta tabela).

**Dicas de consulta:** WorkflowTask é filha desta tabela, portanto tarefas de workflow também têm linha aqui.

## TAR_PARTIC

Subtipo de Task (ToDoTask) para tarefas to-do/de participação; tabela marcadora sem colunas além da PK.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Tipo indicado pela existência da linha.

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_CTRAL** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa base.

**Dicas de consulta:** Join com TAR_CTRAL para os dados da tarefa.

## TAR_WORKFLOW

Subtipo de tarefa que liga uma tarefa do gerenciador à movimentação (etapa) de uma instância de processo de workflow.

**Ciclo de vida:** Uma linha por tarefa do subtipo, criada junto com a linha de TAR_CTRAL.

**Atenção:** Herda de TAR_ESFOR (herança JOINED).

**PK:** COD_EMPRESA, COD_TAREFA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `NUM_SEQ_MOVTO` | integer | S | Sequência da movimentação (etapa) do processo a que a tarefa se refere. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| `NUM_PROCES` | integer | S | Número da instância (solicitação) de processo de workflow. |  | PROCES_WORKFLOW.NUM_PROCES |
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_TAREFA` | integer | N | Código da tarefa (taskId); parte da PK e elo da herança JOINED com TAR_CTRAL. |  | TAR_CTRAL.COD_TAREFA |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_TAREFA)` → **TAR_ESFOR** `(COD_EMPRESA, COD_TAREFA)` · 1:1 · physical-fk/confirmed — Tarefa pai na hierarquia JOINED.
- `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` → **HISTOR_PROCES** `(COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO)` · N:1 · logical-probable/probable — Movimentação do processo; sem FK física.

**Dicas de consulta:** Usar named queries findWorkflowTaskByMovementSequence[AndUser].
