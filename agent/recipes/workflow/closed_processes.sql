-- workflow/closed_processes: Listar solicitações encerradas (inclui possíveis canceladas)
-- Result grain: one process instance per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: LOG_ATIV=0 não distingue conclusão e cancelamento; valores de STATUS não confirmados.
SELECT PROCES_WORKFLOW.COD_EMPRESA, PROCES_WORKFLOW.NUM_PROCES, PROCES_WORKFLOW.COD_DEF_PROCES, PROCES_WORKFLOW.STATUS, PROCES_WORKFLOW.END_DATE
FROM PROCES_WORKFLOW
WHERE PROCES_WORKFLOW.COD_EMPRESA = :tenant_id AND PROCES_WORKFLOW.LOG_ATIV = 0
ORDER BY PROCES_WORKFLOW.END_DATE, PROCES_WORKFLOW.NUM_PROCES;
