-- workflow/overdue_tasks: Listar tarefas pendentes vencidas
-- Result grain: one pending task assignment
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: as_of deve usar a convenção temporal da instância; deadline NULL não é vencido.
SELECT TAR_PROCES.COD_EMPRESA, TAR_PROCES.NUM_PROCES, TAR_PROCES.NUM_SEQ_MOVTO, TAR_PROCES.NUM_SEQ_TRANSF,
       TAR_PROCES.CD_MATRICULA, TAR_PROCES.DEADLINE
FROM TAR_PROCES
WHERE TAR_PROCES.COD_EMPRESA = :tenant_id AND TAR_PROCES.LOG_ATIV = 1 AND TAR_PROCES.IDI_STATUS IN (0, 1)
  AND TAR_PROCES.DEADLINE < :as_of
ORDER BY TAR_PROCES.DEADLINE;
