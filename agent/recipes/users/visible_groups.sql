-- users/visible_groups: Listar grupos visíveis do tenant
-- Result grain: one group per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT g.TENANT_ID, g.GROUP_ID, g.GROUP_CODE, g.DESCRIPTION, g.GROUP_TYPE
FROM FDN_GROUP AS g
WHERE g.TENANT_ID = :tenant_id AND g.INTERNAL = 0
ORDER BY g.GROUP_CODE;
