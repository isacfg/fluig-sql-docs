# Domínio: infraestrutura-servidor

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_SERVER_INFO

Informações de diagnóstico publicadas por instâncias do servidor Fluig (nome, IP e valor da informação) em data de inserção.

**Ciclo de vida:** Escrita periódica pelas instâncias; sem entidade JPA mapeada (acesso por SQL nativo).

**Atenção:** Sem entidade JPA. A relação inferida com QRTZ_SCHEDULER_STATE é por coincidência de nome e não foi confirmada.

**PK:** DATA_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `DATA_ID` | bigint(20) | N | Chave primária do registro. |  |  |
| `INSTANCE_NAME` | VARCHAR(250) | N | Nome da instância/nó do servidor Fluig. |  |  |
| `INSTANCE_IP` | VARCHAR(250) | N | Endereço IP da instância (dado de infraestrutura). |  |  |
| `INFORMATION_VALUE` | VARCHAR(4000) | N | Valor da informação publicada (texto até 4000 caracteres). |  |  |
| `DATE_INSERT` | DATE | N | Data de inserção do registro. |  |  |

**Relacionamentos (saem desta tabela):**

- `(INSTANCE_NAME)` → **QRTZ_SCHEDULER_STATE** `(INSTANCE_NAME)` · N:1 · logical-probable/probable — Provável mesmo nome de nó em cluster, mas não confirmado no código.

**Dicas de consulta:** Sem coluna de tenant; global.
