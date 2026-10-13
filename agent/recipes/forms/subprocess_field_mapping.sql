-- forms/subprocess_field_mapping: Listar mapeamento de campos para subprocessos
-- Result grain: one configured field mapping
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: MAP_FLOW é exibido sem decodificar valores não confirmados.
SELECT m.TENANT_ID, m.FORM_MAP_ID, m.PROCESS_CODE, m.VERSION, m.STATE_SEQUENCE,
       m.PROCESS_FIELD, m.SUB_PROCESS_CODE, m.SUB_PROCESS_FIELD, m.MAP_FLOW
FROM PROCESS_FORM_MAP AS m
WHERE m.TENANT_ID = :tenant_id AND m.PROCESS_CODE = :process_code AND m.VERSION = :process_version
ORDER BY m.FORM_MAP_ID;
