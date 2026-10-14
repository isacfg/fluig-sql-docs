-- users/direct_group_members: Listar associações diretas de usuários de um grupo
-- Result grain: one membership association, not distinct users or effective membership
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Não expande subgrupos nem papéis herdados; múltiplas associações podem apontar para o mesmo usuário.
SELECT FDN_GROUPUSERROLE.TENANT_ID, FDN_GROUPUSERROLE.GROUPUSERROLE_ID, FDN_GROUPUSERROLE.GROUP_CODE, FDN_USERTENANT.USER_TENANT_ID, FDN_USERTENANT.LOGIN, FDN_USERTENANT.USER_CODE
FROM FDN_GROUPUSERROLE
JOIN FDN_USERTENANT ON FDN_USERTENANT.LOGIN = FDN_GROUPUSERROLE.LOGIN AND FDN_USERTENANT.TENANT_ID = FDN_GROUPUSERROLE.TENANT_ID
WHERE FDN_GROUPUSERROLE.TENANT_ID = :tenant_id AND FDN_GROUPUSERROLE.GROUP_CODE = :group_code AND FDN_GROUPUSERROLE.LOGIN IS NOT NULL
ORDER BY FDN_GROUPUSERROLE.GROUPUSERROLE_ID;
