# Domínio: bpm-workflow-erro

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## PROCES_WORKFLOW_ERROR_LOG

Log de falhas ocorridas em operações assíncronas/de movimentação do workflow (envio, cancelamento, mover, timer etc.), guardando o payload serializado para reprocessamento e o stack trace.

**Ciclo de vida:** Uma linha por falha de instância; inserida pelo motor de workflow ao capturar exceção e removida/reprocessada pela tela de erros de processo. Volume baixo.

**Atenção:** Usa TENANT_ID (não COD_EMPRESA). Índice único (TENANT_ID, INSTANCE_ID): no máximo um erro registrado por instância.

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária sequencial do registro de erro (ID gerado via metalist rowid). |  |  |
| `TENANT_ID` | bigint | N | Tenant/empresa dona da instância com erro. |  | FDN_TENANT.TENANT_ID |
| `INSTANCE_ID` | integer | N | Número da instância de processo que falhou; único por tenant. |  | PROCES_WORKFLOW.NUM_PROCES |
| `STATE_SEQUENCE` | integer | S | Sequência de movimentação/estado (NUM_SEQ_MOVTO) em que o erro ocorreu. |  | HISTOR_PROCES.NUM_SEQ_MOVTO |
| `EXECUTOR_USER_CODE` | varchar(150) | S | Código do usuário que executava a operação quando falhou. |  | FDN_USERTENANT.USER_CODE (colleagueId; matrícula/login) |
| `METHOD` | integer | N | Código da operação do workflow que falhou, conforme enum ProcessWorkflowErrorMethod. | 100=send; 200=saveAndSendTask; 300=run async; 400=continueProcessThroughIntermediateError; 401=executeConditionTask; 402=runBpmnTimerTask; 403=completeExpiredTask; 500=cancelInstance (engine); 600=cancelInstance (service); 700=move; 800=saveAndSendTaskBatch; 900=takeTask |  |
| `DATA` | longtext | S | Payload serializado (VO de parâmetros do método) usado para reexecutar a operação. |  |  |
| `ERROR_MESSAGE` | varchar(512) | S | Mensagem curta da exceção (até 512 caracteres). |  |  |
| `ERROR_LOG` | longtext | S | Stack trace/log completo do erro. |  |  |
| `CREATED_AT` | datetime | N | Data/hora em que o erro foi registrado. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID, INSTANCE_ID)` → **PROCES_WORKFLOW** `(COD_EMPRESA, NUM_PROCES)` · 1:1 · logical-probable/probable — Instância de processo à qual o erro pertence (sem FK física).
- `(EXECUTOR_USER_CODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Usuário executor da operação. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Filtrar por TENANT_ID. DATA e ERROR_LOG são longtext e podem conter dados do formulário/stack trace; evitar selecioná-los em listagens. Pode conter dados sensíveis do processo.
