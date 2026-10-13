-- ecm/deleted_documents: Listar versões de documentos na lixeira
-- Result grain: one deleted document version; multiple versions may exist
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.DS_PRINCIPAL_DOCUMENTO, d.VERSAO_ATIVA
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.LOG_DELETE = 1
ORDER BY d.NR_DOCUMENTO, d.NR_VERSAO;
