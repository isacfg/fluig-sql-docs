-- workflow/pending_tasks_by_user: Listar tarefas pendentes de um usuário
-- Result grain: one task assignment (five-column TAR_PROCES PK)
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT t.COD_EMPRESA, t.NUM_PROCES, t.NUM_SEQ_MOVTO, t.NUM_SEQ_TRANSF,
       t.CD_MATRICULA, t.IDI_STATUS, t.START_DATE, t.DEADLINE, p.COD_DEF_PROCES
FROM TAR_PROCES AS t
JOIN PROCES_WORKFLOW AS p ON p.COD_EMPRESA = t.COD_EMPRESA AND p.NUM_PROCES = t.NUM_PROCES
WHERE t.COD_EMPRESA = :tenant_id AND t.CD_MATRICULA = :user_code
  AND t.LOG_ATIV = 1 AND t.IDI_STATUS IN (0, 1)
ORDER BY t.DEADLINE, t.NUM_PROCES, t.NUM_SEQ_MOVTO, t.NUM_SEQ_TRANSF;
