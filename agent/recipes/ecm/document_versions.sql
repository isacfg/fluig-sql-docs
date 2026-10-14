-- ecm/document_versions: Listar versões de um documento incluindo lixeira
-- Result grain: one document version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.VERSAO_ATIVA,
       DOCUMENTO.LOG_DELETE, DOCUMENTO.DS_VERSAO, DOCUMENTO.DT_CRIACAO, DOCUMENTO.DT_ATUALIZACAO
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.NR_DOCUMENTO = :document_id
ORDER BY DOCUMENTO.NR_VERSAO;
