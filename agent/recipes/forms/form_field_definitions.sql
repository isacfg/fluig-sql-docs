-- forms/form_field_definitions: Listar definições de campos de fichário e versão
-- Result grain: one field definition per form version and logical table
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT f.COD_EMPRESA, f.NR_FICHARIO, f.NR_VERSAO, f.COD_TABELA, f.COD_CAMPO, f.TIPO_CAMPO
FROM FICHARIO_CAMPO AS f
WHERE f.COD_EMPRESA = :tenant_id AND f.NR_FICHARIO = :form_id AND f.NR_VERSAO = :form_version
ORDER BY f.COD_TABELA, f.COD_CAMPO;
