-- forms/form_field_definitions: Listar definições de campos de fichário e versão
-- Result grain: one field definition per form version and logical table
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT FICHARIO_CAMPO.COD_EMPRESA, FICHARIO_CAMPO.NR_FICHARIO, FICHARIO_CAMPO.NR_VERSAO, FICHARIO_CAMPO.COD_TABELA, FICHARIO_CAMPO.COD_CAMPO, FICHARIO_CAMPO.TIPO_CAMPO
FROM FICHARIO_CAMPO
WHERE FICHARIO_CAMPO.COD_EMPRESA = :tenant_id AND FICHARIO_CAMPO.NR_FICHARIO = :form_id AND FICHARIO_CAMPO.NR_VERSAO = :form_version
ORDER BY FICHARIO_CAMPO.COD_TABELA, FICHARIO_CAMPO.COD_CAMPO;
