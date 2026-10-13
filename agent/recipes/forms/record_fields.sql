-- forms/record_fields: Listar valores EAV de uma versão de ficha
-- Result grain: one field value per record version and logical table
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
-- Assumption: Tabelas ML dinâmicas não constam deste catálogo; não inferir nomes ou estrutura de linhas filhas.
SELECT f.COD_EMPRESA, f.NR_FICHA, f.NR_VERSAO, f.COD_TABELA, f.COD_CAMPO, f.NR_FICHARIO, f.COD_VALOR
FROM FICHA AS f
WHERE f.COD_EMPRESA = :tenant_id AND f.NR_FICHA = :record_id AND f.NR_VERSAO = :record_version
ORDER BY f.COD_TABELA, f.COD_CAMPO;
