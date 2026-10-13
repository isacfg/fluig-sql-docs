-- ecm/files_by_publisher: Listar arquivos correntes publicados por um usuário
-- Result grain: one current file document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.DS_PRINCIPAL_DOCUMENTO, d.CD_PUBLICADOR
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.CD_PUBLICADOR = :user_code AND d.TP_DOCUMENTO = '2'
  AND d.VERSAO_ATIVA = 1 AND d.LOG_DELETE = 0
ORDER BY d.NR_DOCUMENTO;
