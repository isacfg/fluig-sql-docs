-- workflow/current_movements: Listar posições atuais da solicitação
-- Result grain: one active movement; parallel threads may return multiple rows
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT h.COD_EMPRESA, h.NUM_PROCES, h.NUM_SEQ_MOVTO, h.NUM_SEQ_ESTADO, h.NUM_SEQ_THREAD
FROM HISTOR_PROCES AS h
WHERE h.COD_EMPRESA = :tenant_id AND h.NUM_PROCES = :process_id AND h.LOG_ATIV = 1
ORDER BY h.NUM_SEQ_MOVTO;
