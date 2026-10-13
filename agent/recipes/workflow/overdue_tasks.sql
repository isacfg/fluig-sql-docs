-- workflow/overdue_tasks: Listar tarefas pendentes vencidas
-- Result grain: one pending task assignment
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: as_of deve usar a convenção temporal da instância; deadline NULL não é vencido.
SELECT t.COD_EMPRESA, t.NUM_PROCES, t.NUM_SEQ_MOVTO, t.NUM_SEQ_TRANSF,
       t.CD_MATRICULA, t.DEADLINE
FROM TAR_PROCES AS t
WHERE t.COD_EMPRESA = :tenant_id AND t.LOG_ATIV = 1 AND t.IDI_STATUS IN (0, 1)
  AND t.DEADLINE < :as_of
ORDER BY t.DEADLINE;
