-- workflow/definition_states: Listar atividades de uma versão de processo
-- Result grain: one state in one specified definition version per tenant
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT ESTADO_PROCES.COD_EMPRESA, ESTADO_PROCES.COD_DEF_PROCES, ESTADO_PROCES.NUM_VERS, ESTADO_PROCES.NUM_SEQ,
       ESTADO_PROCES.NOM_ESTADO, ESTADO_PROCES.DES_ESTADO, ESTADO_PROCES.IDI_TIP_BPMN, ESTADO_PROCES.LOG_ESTADO_INICIAL
FROM ESTADO_PROCES
WHERE ESTADO_PROCES.COD_EMPRESA = :tenant_id AND ESTADO_PROCES.COD_DEF_PROCES = :process_code AND ESTADO_PROCES.NUM_VERS = :process_version
ORDER BY ESTADO_PROCES.NUM_SEQ;
