-- ecm/deleted_documents: Listar versões de documentos na lixeira
-- Result grain: one deleted document version; multiple versions may exist
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO, DOCUMENTO.VERSAO_ATIVA
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.LOG_DELETE = 1
ORDER BY DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO;
