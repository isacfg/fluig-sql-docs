-- workflow/process_history: Listar histórico de uma solicitação
-- Result grain: one process movement per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT HISTOR_PROCES.COD_EMPRESA, HISTOR_PROCES.NUM_PROCES, HISTOR_PROCES.NUM_SEQ_MOVTO, HISTOR_PROCES.NUM_SEQ_MOVTO_ANT,
       HISTOR_PROCES.NUM_SEQ_ESTADO, HISTOR_PROCES.NUM_SEQ_THREAD, HISTOR_PROCES.MOVTO_DATE_TIME, HISTOR_PROCES.LOG_ATIV
FROM HISTOR_PROCES
WHERE HISTOR_PROCES.COD_EMPRESA = :tenant_id AND HISTOR_PROCES.NUM_PROCES = :process_id
ORDER BY HISTOR_PROCES.NUM_SEQ_MOVTO;
