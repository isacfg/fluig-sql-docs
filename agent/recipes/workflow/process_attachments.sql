-- workflow/process_attachments: Listar anexos e suas versões registradas
-- Result grain: one attachment association; unmatched document versions retained
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Join lógico ANEXO_PROCES -> DOCUMENTO é probable; verificar na instância.
-- Assumption: A versão registrada pode estar excluída ou não ser a corrente.
SELECT ANEXO_PROCES.COD_EMPRESA, ANEXO_PROCES.NUM_PROCES, ANEXO_PROCES.NUM_SEQ_ANEXO, ANEXO_PROCES.NR_DOCUMENTO,
       ANEXO_PROCES.NR_VERSAO, ANEXO_PROCES.DT_ANEXO, DOCUMENTO.DS_PRINCIPAL_DOCUMENTO, DOCUMENTO.LOG_DELETE
FROM ANEXO_PROCES
LEFT JOIN DOCUMENTO ON DOCUMENTO.COD_EMPRESA = ANEXO_PROCES.COD_EMPRESA
  AND DOCUMENTO.NR_DOCUMENTO = ANEXO_PROCES.NR_DOCUMENTO AND DOCUMENTO.NR_VERSAO = ANEXO_PROCES.NR_VERSAO
WHERE ANEXO_PROCES.COD_EMPRESA = :tenant_id AND ANEXO_PROCES.NUM_PROCES = :process_id
ORDER BY ANEXO_PROCES.NUM_SEQ_ANEXO;
