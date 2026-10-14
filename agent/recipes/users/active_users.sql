-- users/active_users: Listar usuários ativos do tenant com nome
-- Result grain: one tenant-user association
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT FDN_USERTENANT.TENANT_ID, FDN_USERTENANT.USER_TENANT_ID, FDN_USERTENANT.USER_CODE, FDN_USERTENANT.LOGIN, FDN_USER.FULL_NAME
FROM FDN_USERTENANT
JOIN FDN_USER ON FDN_USER.USER_ID = FDN_USERTENANT.USER_ID
WHERE FDN_USERTENANT.TENANT_ID = :tenant_id AND FDN_USERTENANT.USER_STATE = 1
ORDER BY FDN_USERTENANT.LOGIN;
