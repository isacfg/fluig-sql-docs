-- forms/record_fields: Listar valores EAV de uma versão de ficha
-- Result grain: one field value per record version and logical table
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Tabelas ML dinâmicas não constam deste catálogo; não inferir nomes ou estrutura de linhas filhas.
SELECT FICHA.COD_EMPRESA, FICHA.NR_FICHA, FICHA.NR_VERSAO, FICHA.COD_TABELA, FICHA.COD_CAMPO, FICHA.NR_FICHARIO, FICHA.COD_VALOR
FROM FICHA
WHERE FICHA.COD_EMPRESA = :tenant_id AND FICHA.NR_FICHA = :record_id AND FICHA.NR_VERSAO = :record_version
ORDER BY FICHA.COD_TABELA, FICHA.COD_CAMPO;
