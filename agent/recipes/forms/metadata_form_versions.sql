-- forms/metadata_form_versions: Listar versões de formulário de metadados com documento
-- Result grain: one metadata-form version
-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).
-- Validation: static schema checks only; not executed on a Fluig database.
SELECT m.TENANT_ID, m.ID, m.TITLE, m.DOCUMENT_ID, m.DCMNT_VRSN_NMBER,
       m.VERSION_STATUS, d.DS_PRINCIPAL_DOCUMENTO, d.LOG_DELETE
FROM ECM_METADATA_FORM AS m
JOIN DOCUMENTO AS d ON d.COD_EMPRESA = m.TENANT_ID AND d.NR_DOCUMENTO = m.DOCUMENT_ID
  AND d.NR_VERSAO = m.DCMNT_VRSN_NMBER
WHERE m.TENANT_ID = :tenant_id AND m.DOCUMENT_ID = :document_id
ORDER BY m.DCMNT_VRSN_NMBER;
