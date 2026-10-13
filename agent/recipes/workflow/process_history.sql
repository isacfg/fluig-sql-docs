-- workflow/process_history: Listar histórico de uma solicitação
-- Result grain: one process movement per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT h.COD_EMPRESA, h.NUM_PROCES, h.NUM_SEQ_MOVTO, h.NUM_SEQ_MOVTO_ANT,
       h.NUM_SEQ_ESTADO, h.NUM_SEQ_THREAD, h.MOVTO_DATE_TIME, h.LOG_ATIV
FROM HISTOR_PROCES AS h
WHERE h.COD_EMPRESA = :tenant_id AND h.NUM_PROCES = :process_id
ORDER BY h.NUM_SEQ_MOVTO;
