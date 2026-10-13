-- workflow/open_counts_by_definition: Contar solicitações abertas por definição
-- Result grain: one process definition per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT p.COD_EMPRESA, p.COD_DEF_PROCES, COUNT(*) AS process_count
FROM PROCES_WORKFLOW AS p
WHERE p.COD_EMPRESA = :tenant_id AND p.LOG_ATIV = 1
GROUP BY p.COD_EMPRESA, p.COD_DEF_PROCES;
