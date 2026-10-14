-- ecm/custom_fields_for_version: Listar valores customizados de uma versão de documento
-- Result grain: one custom field value per document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Join lógico com CAMPO_CUSTOM é probable. COD_VALOR é projetado explicitamente porque é o valor solicitado.
SELECT DOCTO_CAMPO_CUSTOM.COD_EMPRESA, DOCTO_CAMPO_CUSTOM.NR_DOCUMENTO, DOCTO_CAMPO_CUSTOM.NR_VERSAO, DOCTO_CAMPO_CUSTOM.COD_CAMPO_CUSTOM, CAMPO_CUSTOM.DES_CAMPO_CUSTOM, DOCTO_CAMPO_CUSTOM.COD_VALOR
FROM DOCTO_CAMPO_CUSTOM
LEFT JOIN CAMPO_CUSTOM ON CAMPO_CUSTOM.COD_EMPRESA = DOCTO_CAMPO_CUSTOM.COD_EMPRESA AND CAMPO_CUSTOM.COD_CAMPO_CUSTOM = DOCTO_CAMPO_CUSTOM.COD_CAMPO_CUSTOM
WHERE DOCTO_CAMPO_CUSTOM.COD_EMPRESA = :tenant_id AND DOCTO_CAMPO_CUSTOM.NR_DOCUMENTO = :document_id AND DOCTO_CAMPO_CUSTOM.NR_VERSAO = :document_version
ORDER BY DOCTO_CAMPO_CUSTOM.COD_CAMPO_CUSTOM;
