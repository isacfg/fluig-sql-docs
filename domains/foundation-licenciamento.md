# Domínio: foundation-licenciamento

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## CONTROL_LICENC

Controle de licenciamento do produto: chaves de licença inicial e de emergência e CNPJ licenciado.

**Ciclo de vida:** Poucas linhas, gravadas na ativação/renovação de licença.

**Atenção:** Sem COD_EMPRESA. Contém chaves de licença (sensível).

**PK:** NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NUM_SEQ` | integer | N | Identificador sequencial da licença (licenseId). |  |  |
| `DES_CHAVE_EMERGEN` | varchar(255) | S | Chave de licença de emergência. |  |  |
| `COD_CNPJ` | varchar(255) | S | CNPJ do licenciado (federalId). |  |  |
| `DES_CHAVE_INICIAL` | varchar(255) | S | Chave de licença inicial. |  |  |

**Dicas de consulta:** Dados sensíveis (CNPJ e chaves de licença): não expor.
