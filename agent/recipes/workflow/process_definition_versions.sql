-- workflow/process_definition_versions: Listar versões de uma definição
-- Result grain: one process definition version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT v.COD_EMPRESA, v.COD_DEF_PROCES, v.NUM_VERS, v.LOG_ATIV,
       v.LOG_BLOQDO, v.DES_VERS, d.DES_DEF_PROCES
FROM VERS_DEF_PROCES AS v
JOIN DEF_PROCES AS d ON d.COD_EMPRESA = v.COD_EMPRESA AND d.COD_DEF_PROCES = v.COD_DEF_PROCES
WHERE v.COD_EMPRESA = :tenant_id AND v.COD_DEF_PROCES = :process_code
ORDER BY v.NUM_VERS;
