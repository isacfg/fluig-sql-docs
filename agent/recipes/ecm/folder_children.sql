-- ecm/folder_children: Listar filhos correntes de uma pasta
-- Result grain: one current child document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.TP_DOCUMENTO, d.DS_PRINCIPAL_DOCUMENTO
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.NR_DOCUMENTO_PAI = :folder_id
  AND d.VERSAO_ATIVA = 1 AND d.LOG_DELETE = 0
ORDER BY d.NR_DOCUMENTO;
