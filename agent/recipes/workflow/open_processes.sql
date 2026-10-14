-- workflow/open_processes: Listar solicitações abertas
-- Result grain: one process instance per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT PROCES_WORKFLOW.COD_EMPRESA, PROCES_WORKFLOW.NUM_PROCES, PROCES_WORKFLOW.COD_DEF_PROCES, PROCES_WORKFLOW.STATUS,
       PROCES_WORKFLOW.COD_MATR_REQUISIT, PROCES_WORKFLOW.START_DATE, PROCES_WORKFLOW.DEADLINE_DATE
FROM PROCES_WORKFLOW
WHERE PROCES_WORKFLOW.COD_EMPRESA = :tenant_id AND PROCES_WORKFLOW.LOG_ATIV = 1
ORDER BY PROCES_WORKFLOW.NUM_PROCES;
