-- users/user_by_code: Localizar vínculos por matrícula sem assumir unicidade
-- Result grain: one matching tenant-user association; more than one may match
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Conferir unicidade de (TENANT_ID, USER_CODE) antes de enriquecer tarefas por matrícula.
SELECT FDN_USERTENANT.TENANT_ID, FDN_USERTENANT.USER_TENANT_ID, FDN_USERTENANT.USER_CODE, FDN_USERTENANT.LOGIN, FDN_USERTENANT.USER_STATE
FROM FDN_USERTENANT
WHERE FDN_USERTENANT.TENANT_ID = :tenant_id AND FDN_USERTENANT.USER_CODE = :user_code
ORDER BY FDN_USERTENANT.USER_TENANT_ID;
