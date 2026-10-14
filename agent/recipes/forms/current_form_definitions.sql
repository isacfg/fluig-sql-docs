-- forms/current_form_definitions: Listar fichários correntes do GED
-- Result grain: one current form-definition document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO, DOCUMENTO.NM_DATASET
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.TP_DOCUMENTO = '4' AND DOCUMENTO.VERSAO_ATIVA = 1 AND DOCUMENTO.LOG_DELETE = 0
ORDER BY DOCUMENTO.NR_DOCUMENTO;
