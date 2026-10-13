-- forms/current_form_definitions: Listar fichários correntes do GED
-- Result grain: one current form-definition document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.DS_PRINCIPAL_DOCUMENTO, d.NM_DATASET
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.TP_DOCUMENTO = '4' AND d.VERSAO_ATIVA = 1 AND d.LOG_DELETE = 0
ORDER BY d.NR_DOCUMENTO;
