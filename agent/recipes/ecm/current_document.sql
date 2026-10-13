-- ecm/current_document: Obter estado corrente de um documento
-- Result grain: one active non-deleted document version; current uniqueness is an application invariant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT d.COD_EMPRESA, d.NR_DOCUMENTO, d.NR_VERSAO, d.DS_PRINCIPAL_DOCUMENTO,
       d.TP_DOCUMENTO, d.NR_DOCUMENTO_PAI, d.DT_ATUALIZACAO
FROM DOCUMENTO AS d
WHERE d.COD_EMPRESA = :tenant_id AND d.NR_DOCUMENTO = :document_id
  AND d.VERSAO_ATIVA = 1 AND d.LOG_DELETE = 0;
