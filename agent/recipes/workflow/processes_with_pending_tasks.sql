-- workflow/processes_with_pending_tasks: Listar solicitações com tarefas pendentes do usuário sem duplicar
-- Result grain: one process instance; EXISTS avoids task fanout
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT PROCES_WORKFLOW.COD_EMPRESA, PROCES_WORKFLOW.NUM_PROCES, PROCES_WORKFLOW.COD_DEF_PROCES, PROCES_WORKFLOW.START_DATE
FROM PROCES_WORKFLOW
WHERE PROCES_WORKFLOW.COD_EMPRESA = :tenant_id AND PROCES_WORKFLOW.LOG_ATIV = 1
  AND EXISTS (SELECT 1 FROM TAR_PROCES
              WHERE TAR_PROCES.COD_EMPRESA = PROCES_WORKFLOW.COD_EMPRESA AND TAR_PROCES.NUM_PROCES = PROCES_WORKFLOW.NUM_PROCES
                AND TAR_PROCES.CD_MATRICULA = :user_code AND TAR_PROCES.LOG_ATIV = 1 AND TAR_PROCES.IDI_STATUS IN (0, 1))
ORDER BY PROCES_WORKFLOW.NUM_PROCES;
