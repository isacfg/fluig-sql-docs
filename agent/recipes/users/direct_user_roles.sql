-- users/direct_user_roles: Listar papéis diretos de um login
-- Result grain: one direct user-role association
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Não representa permissões efetivas nem papéis herdados de grupos.
SELECT FDN_USERROLE.TENANT_ID, FDN_USERROLE.USERROLE_ID, FDN_USERROLE.LOGIN, FDN_USERROLE.ROLE_CODE, FDN_ROLE.DESCRIPTION
FROM FDN_USERROLE
JOIN FDN_ROLE ON FDN_ROLE.TENANT_ID = FDN_USERROLE.TENANT_ID AND FDN_ROLE.ROLE_CODE = FDN_USERROLE.ROLE_CODE
WHERE FDN_USERROLE.TENANT_ID = :tenant_id AND FDN_USERROLE.LOGIN = :login
ORDER BY FDN_USERROLE.ROLE_CODE;
