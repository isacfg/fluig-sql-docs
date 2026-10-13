-- users/direct_user_roles: Listar papéis diretos de um login
-- Result grain: one direct user-role association
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Não representa permissões efetivas nem papéis herdados de grupos.
SELECT ur.TENANT_ID, ur.USERROLE_ID, ur.LOGIN, ur.ROLE_CODE, r.DESCRIPTION
FROM FDN_USERROLE AS ur
JOIN FDN_ROLE AS r ON r.TENANT_ID = ur.TENANT_ID AND r.ROLE_CODE = ur.ROLE_CODE
WHERE ur.TENANT_ID = :tenant_id AND ur.LOGIN = :login
ORDER BY ur.ROLE_CODE;
