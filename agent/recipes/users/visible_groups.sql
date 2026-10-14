-- users/visible_groups: Listar grupos visíveis do tenant
-- Result grain: one group per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT FDN_GROUP.TENANT_ID, FDN_GROUP.GROUP_ID, FDN_GROUP.GROUP_CODE, FDN_GROUP.DESCRIPTION, FDN_GROUP.GROUP_TYPE
FROM FDN_GROUP
WHERE FDN_GROUP.TENANT_ID = :tenant_id AND FDN_GROUP.INTERNAL = 0
ORDER BY FDN_GROUP.GROUP_CODE;
