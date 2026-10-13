-- users/direct_group_members: Listar associações diretas de usuários de um grupo
-- Result grain: one membership association, not distinct users or effective membership
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Não expande subgrupos nem papéis herdados; múltiplas associações podem apontar para o mesmo usuário.
SELECT m.TENANT_ID, m.GROUPUSERROLE_ID, m.GROUP_CODE, ut.USER_TENANT_ID, ut.LOGIN, ut.USER_CODE
FROM FDN_GROUPUSERROLE AS m
JOIN FDN_USERTENANT AS ut ON ut.LOGIN = m.LOGIN AND ut.TENANT_ID = m.TENANT_ID
WHERE m.TENANT_ID = :tenant_id AND m.GROUP_CODE = :group_code AND m.LOGIN IS NOT NULL
ORDER BY m.GROUPUSERROLE_ID;
