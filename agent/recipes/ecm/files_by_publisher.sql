-- ecm/files_by_publisher: Listar arquivos correntes publicados por um usuário
-- Result grain: one current file document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO, DOCUMENTO.CD_PUBLICADOR
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.CD_PUBLICADOR = :user_code AND DOCUMENTO.TP_DOCUMENTO = '2'
  AND DOCUMENTO.VERSAO_ATIVA = 1 AND DOCUMENTO.LOG_DELETE = 0
ORDER BY DOCUMENTO.NR_DOCUMENTO;
