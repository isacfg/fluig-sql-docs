# Domínio: assinatura-digital

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_DIGITALSIGNATURE

Configuração de assinatura digital por tenant: tipo de assinatura e número de licenças. Uma linha por tenant licenciado.

**Ciclo de vida:** Configurada na ativação de licença; pouquíssimas linhas.

**Atenção:** Unique (provável) por TENANT_ID.

**PK:** DIGITAL_SIGNATURE_ID · **Unique:** (TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DIGITAL_SIGNATURE_ID` | bigint(20) | N | Chave primária. |  |  |
| `DIGITAL_SIGNATURE_TYPE` | int(11) | S | Tipo de assinatura digital (enum DigitalSignatureType). | CADES e CMS (enum; mapeamento ordinal/string não confirmado) |  |
| `LICENSE_NUMBER` | int(11) | S | Quantidade de licenças de assinatura digital contratadas. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant licenciado. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant da licença.

**Dicas de consulta:** Consultar por TENANT_ID (findByTenantId).
