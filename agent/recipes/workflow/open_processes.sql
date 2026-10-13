-- workflow/open_processes: Listar solicitações abertas
-- Result grain: one process instance per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT p.COD_EMPRESA, p.NUM_PROCES, p.COD_DEF_PROCES, p.NUM_VERS,
       p.COD_MATR_REQUISIT, p.START_DATE, p.DEADLINE_DATE
FROM PROCES_WORKFLOW AS p
WHERE p.COD_EMPRESA = :tenant_id AND p.LOG_ATIV = 1
ORDER BY p.NUM_PROCES;
