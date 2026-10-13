-- ecm/document_versions: Listar versões de um documento incluindo lixeira
-- Result grain: one document version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.VERSAO_ATIVA,
       d.LOG_DELETE, d.DS_VERSAO, d.DT_CRIACAO, d.DT_ATUALIZACAO
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.NR_DOCUMENTO = :document_id
ORDER BY d.NR_VERSAO;
