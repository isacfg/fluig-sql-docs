-- workflow/current_movements: Listar posições atuais da solicitação
-- Result grain: one active movement; parallel threads may return multiple rows
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT HISTOR_PROCES.COD_EMPRESA, HISTOR_PROCES.NUM_PROCES, HISTOR_PROCES.NUM_SEQ_MOVTO, HISTOR_PROCES.NUM_SEQ_ESTADO, HISTOR_PROCES.NUM_SEQ_THREAD
FROM HISTOR_PROCES
WHERE HISTOR_PROCES.COD_EMPRESA = :tenant_id AND HISTOR_PROCES.NUM_PROCES = :process_id AND HISTOR_PROCES.LOG_ATIV = 1
ORDER BY HISTOR_PROCES.NUM_SEQ_MOVTO;
