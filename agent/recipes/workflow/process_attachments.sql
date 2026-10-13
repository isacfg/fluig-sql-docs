-- workflow/process_attachments: Listar anexos e suas versões registradas
-- Result grain: one attachment association; unmatched document versions retained
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Join lógico ANEXO_PROCES -> DOCUMENTO é probable; verificar na instância.
-- Assumption: A versão registrada pode estar excluída ou não ser a corrente.
SELECT a.COD_EMPRESA, a.NUM_PROCES, a.NUM_SEQ_ANEXO, a.NR_DOCUMENTO,
       a.NR_VERSAO, a.DT_ANEXO, d.DS_PRINCIPAL_DOCUMENTO, d.LOG_DELETE
FROM ANEXO_PROCES AS a
LEFT JOIN DOCUMENTO AS d ON d.COD_EMPRESA = a.COD_EMPRESA
  AND d.NR_DOCUMENTO = a.NR_DOCUMENTO AND d.NR_VERSAO = a.NR_VERSAO
WHERE a.COD_EMPRESA = :tenant_id AND a.NUM_PROCES = :process_id
ORDER BY a.NUM_SEQ_ANEXO;
