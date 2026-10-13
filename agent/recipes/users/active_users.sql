-- users/active_users: Listar usuários ativos do tenant com nome
-- Result grain: one tenant-user association
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT ut.TENANT_ID, ut.USER_TENANT_ID, ut.USER_CODE, ut.LOGIN, u.FULL_NAME
FROM FDN_USERTENANT AS ut
JOIN FDN_USER AS u ON u.USER_ID = ut.USER_ID
WHERE ut.TENANT_ID = :tenant_id AND ut.USER_STATE = 1
ORDER BY ut.LOGIN;
