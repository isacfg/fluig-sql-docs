-- workflow/processes_with_pending_tasks: Listar solicitações com tarefas pendentes do usuário sem duplicar
-- Result grain: one process instance; EXISTS avoids task fanout
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT p.COD_EMPRESA, p.NUM_PROCES, p.COD_DEF_PROCES, p.START_DATE
FROM PROCES_WORKFLOW AS p
WHERE p.COD_EMPRESA = :tenant_id AND p.LOG_ATIV = 1
  AND EXISTS (SELECT 1 FROM TAR_PROCES AS t
              WHERE t.COD_EMPRESA = p.COD_EMPRESA AND t.NUM_PROCES = p.NUM_PROCES
                AND t.CD_MATRICULA = :user_code AND t.LOG_ATIV = 1 AND t.IDI_STATUS IN (0, 1))
ORDER BY p.NUM_PROCES;
