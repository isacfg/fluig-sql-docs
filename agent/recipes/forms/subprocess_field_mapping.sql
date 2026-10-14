-- forms/subprocess_field_mapping: Listar mapeamento de campos para subprocessos
-- Result grain: one configured field mapping
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: MAP_FLOW é exibido sem decodificar valores não confirmados.
SELECT PROCESS_FORM_MAP.TENANT_ID, PROCESS_FORM_MAP.FORM_MAP_ID, PROCESS_FORM_MAP.PROCESS_CODE, PROCESS_FORM_MAP.VERSION, PROCESS_FORM_MAP.STATE_SEQUENCE,
       PROCESS_FORM_MAP.PROCESS_FIELD, PROCESS_FORM_MAP.SUB_PROCESS_CODE, PROCESS_FORM_MAP.SUB_PROCESS_FIELD, PROCESS_FORM_MAP.MAP_FLOW
FROM PROCESS_FORM_MAP
WHERE PROCESS_FORM_MAP.TENANT_ID = :tenant_id AND PROCESS_FORM_MAP.PROCESS_CODE = :process_code AND PROCESS_FORM_MAP.VERSION = :process_version
ORDER BY PROCESS_FORM_MAP.FORM_MAP_ID;
