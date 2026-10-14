-- ecm/folder_children: Listar filhos correntes de uma pasta
-- Result grain: one current child document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.TP_DOCUMENTO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.NR_DOCUMENTO_PAI = :folder_id
  AND DOCUMENTO.VERSAO_ATIVA = 1 AND DOCUMENTO.LOG_DELETE = 0
ORDER BY DOCUMENTO.NR_DOCUMENTO;
