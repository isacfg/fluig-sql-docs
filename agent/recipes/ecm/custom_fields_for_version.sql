-- ecm/custom_fields_for_version: Listar valores customizados de uma versão de documento
-- Result grain: one custom field value per document version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Join lógico com CAMPO_CUSTOM é probable. COD_VALOR é projetado explicitamente porque é o valor solicitado.
SELECT v.COD_EMPRESA, v.NR_DOCUMENTO, v.NR_VERSAO, v.COD_CAMPO_CUSTOM, c.DES_CAMPO_CUSTOM, v.COD_VALOR
FROM DOCTO_CAMPO_CUSTOM AS v
LEFT JOIN CAMPO_CUSTOM AS c ON c.COD_EMPRESA = v.COD_EMPRESA AND c.COD_CAMPO_CUSTOM = v.COD_CAMPO_CUSTOM
WHERE v.COD_EMPRESA = :tenant_id AND v.NR_DOCUMENTO = :document_id AND v.NR_VERSAO = :document_version
ORDER BY v.COD_CAMPO_CUSTOM;
