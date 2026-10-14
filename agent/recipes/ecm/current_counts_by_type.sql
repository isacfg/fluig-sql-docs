-- ecm/current_counts_by_type: Contar versões correntes por tipo de documento
-- Result grain: one document type per tenant; counts current-version rows
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.TP_DOCUMENTO, COUNT(*)
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.VERSAO_ATIVA = 1 AND DOCUMENTO.LOG_DELETE = 0
GROUP BY DOCUMENTO.COD_EMPRESA, DOCUMENTO.TP_DOCUMENTO;
