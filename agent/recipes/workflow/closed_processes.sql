-- workflow/closed_processes: Listar solicitações encerradas (inclui possíveis canceladas)
-- Result grain: one process instance per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: LOG_ATIV=0 não distingue conclusão e cancelamento; valores de STATUS não confirmados.
SELECT p.COD_EMPRESA, p.NUM_PROCES, p.COD_DEF_PROCES, p.STATUS, p.END_DATE
FROM PROCES_WORKFLOW AS p
WHERE p.COD_EMPRESA = :tenant_id AND p.LOG_ATIV = 0
ORDER BY p.END_DATE, p.NUM_PROCES;
