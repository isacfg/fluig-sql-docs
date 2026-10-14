-- ecm/current_document: Obter estado corrente de um documento
-- Result grain: one active non-deleted document version; current uniqueness is an application invariant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT DOCUMENTO.COD_EMPRESA, DOCUMENTO.NR_DOCUMENTO, DOCUMENTO.NR_VERSAO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO,
       DOCUMENTO.TP_DOCUMENTO, DOCUMENTO.NR_DOCUMENTO_PAI, DOCUMENTO.DT_ATUALIZACAO
FROM DOCUMENTO
WHERE DOCUMENTO.COD_EMPRESA = :tenant_id AND DOCUMENTO.NR_DOCUMENTO = :document_id
  AND DOCUMENTO.VERSAO_ATIVA = 1 AND DOCUMENTO.LOG_DELETE = 0;
