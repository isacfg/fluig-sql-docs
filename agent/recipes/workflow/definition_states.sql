-- workflow/definition_states: Listar atividades de uma versão de processo
-- Result grain: one state in one specified definition version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT e.COD_EMPRESA, e.COD_DEF_PROCES, e.NUM_VERS, e.NUM_SEQ,
       e.NOM_ESTADO, e.DES_ESTADO, e.IDI_TIP_BPMN, e.LOG_ESTADO_INICIAL
FROM ESTADO_PROCES AS e
WHERE e.COD_EMPRESA = :tenant_id AND e.COD_DEF_PROCES = :process_code AND e.NUM_VERS = :process_version
ORDER BY e.NUM_SEQ;
