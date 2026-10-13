-- ecm/current_counts_by_type: Contar versões correntes por tipo de documento
-- Result grain: one document type per tenant; counts current-version rows
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.TP_DOCUMENTO, COUNT(*) AS current_version_count
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.VERSAO_ATIVA = 1 AND d.LOG_DELETE = 0
GROUP BY d.COD_EMPRESA, d.TP_DOCUMENTO;
