-- users/user_by_code: Localizar vínculos por matrícula sem assumir unicidade
-- Result grain: one matching tenant-user association; more than one may match
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Conferir unicidade de (TENANT_ID, USER_CODE) antes de enriquecer tarefas por matrícula.
SELECT ut.TENANT_ID, ut.USER_TENANT_ID, ut.USER_CODE, ut.LOGIN, ut.USER_STATE
FROM FDN_USERTENANT AS ut
WHERE ut.TENANT_ID = :tenant_id AND ut.USER_CODE = :user_code
ORDER BY ut.USER_TENANT_ID;
