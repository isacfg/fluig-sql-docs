-- workflow/open_counts_by_definition: Contar solicitações abertas por definição
-- Result grain: one process definition per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT PROCES_WORKFLOW.COD_EMPRESA, PROCES_WORKFLOW.COD_DEF_PROCES, COUNT(*)
FROM PROCES_WORKFLOW
WHERE PROCES_WORKFLOW.COD_EMPRESA = :tenant_id AND PROCES_WORKFLOW.LOG_ATIV = 1
GROUP BY PROCES_WORKFLOW.COD_EMPRESA, PROCES_WORKFLOW.COD_DEF_PROCES;
