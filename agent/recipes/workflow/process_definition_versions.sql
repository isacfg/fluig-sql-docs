-- workflow/process_definition_versions: Listar versões de uma definição
-- Result grain: one process definition version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT VERS_DEF_PROCES.COD_EMPRESA, VERS_DEF_PROCES.COD_DEF_PROCES, VERS_DEF_PROCES.NUM_VERS, VERS_DEF_PROCES.LOG_ATIV,
       VERS_DEF_PROCES.LOG_BLOQDO, VERS_DEF_PROCES.DES_VERS, DEF_PROCES.DES_DEF_PROCES
FROM VERS_DEF_PROCES
JOIN DEF_PROCES ON DEF_PROCES.COD_EMPRESA = VERS_DEF_PROCES.COD_EMPRESA AND DEF_PROCES.COD_DEF_PROCES = VERS_DEF_PROCES.COD_DEF_PROCES
WHERE VERS_DEF_PROCES.COD_EMPRESA = :tenant_id AND VERS_DEF_PROCES.COD_DEF_PROCES = :process_code
ORDER BY VERS_DEF_PROCES.NUM_VERS;
