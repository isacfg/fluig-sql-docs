# Domínio: foundation-dataservice

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_SERVICE_OPERATION

Operação de serviço de dados (Data Service) configurável por tenant: descritor e implementação de uma operação de um serviço.

**Ciclo de vida:** Criada/alterada ao cadastrar serviços de dados customizados; volume baixo.

**Atenção:** Colunas DESCRIPTOR e IMPLEMENTATION são LOB (longtext) e podem conter código/definição. Sem FKs.

**PK:** OPERATION_ID · **Unique:** (TENANT_ID, NAME)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OPERATION_ID` | bigint | N | Chave primária surrogate. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |
| `SERVICE` | varchar(50) | N | Identificador do serviço de dados ao qual a operação pertence. |  |  |
| `NAME` | varchar(150) | N | Nome da operação (até 150 chars). |  |  |
| `DESCRIPTION` | varchar(255) | S | Descrição da operação. |  |  |
| `OPERATION` | varchar(150) | N | Identificador/nome técnico da operação dentro do serviço. |  |  |
| `DESCRIPTOR` | longtext | S | Descritor (definição de entradas/saídas) da operação, texto longo. |  |  |
| `IMPL_TYPE` | varchar(50) | N | Tipo de implementação da operação (string, até 50 chars). |  |  |
| `IMPLEMENTATION` | longtext | S | Corpo da implementação da operação, texto longo (LOB). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant dono; sem FK declarada.

**Dicas de consulta:** Evite selecionar DESCRIPTOR/IMPLEMENTATION em varreduras (LOB).
