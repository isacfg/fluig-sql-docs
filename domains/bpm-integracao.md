# Domínio: bpm-integracao

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## ADAPTER

Cadastro de adapters (conectores externos) do Fluig; cada adapter aponta para um caminho de implementação e é referenciado por APLICATIVO.

**Ciclo de vida:** Linhas criadas via administração; volume muito baixo (dezenas).

**Atenção:** PK composta (COD_EMPRESA, COD_ADAPTER). Sem soft-delete.

**PK:** COD_EMPRESA, COD_ADAPTER

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_ADAPTER` | varchar(50) | N | Identificador textual do adapter, único dentro do tenant. |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| `NOM_ADAPTER` | varchar(50) | N | Descrição/nome exibido do adapter (campo Java description). |  |  |
| `CAMINHO_ADAPTER` | varchar(2000) | N | Caminho (path) do artefato/implementação do adapter, até 2000 caracteres. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_ADAPTER)` → **APLICATIVO** `(COD_EMPRESA, COD_ADAPTER)` · 1:N · logical-probable/probable — APLICATIVO.COD_ADAPTER referencia o adapter usado pelo aplicativo (inferido pelo nome de colunas; entidade sem @JoinColumn).

**Dicas de consulta:** Sempre filtrar COD_EMPRESA. Tabela de configuração, sem dados pessoais.

## AMBIEN_PROGRESS

Cadastro de ambientes/bibliotecas Progress (ProgressLib) usados para integração com sistemas Datasul/Progress.

**Ciclo de vida:** Config administrativa, volume baixo.

**Atenção:** PK (COD_EMPRESA, COD_AMBIEN_PROGRES).

**PK:** COD_EMPRESA, COD_AMBIEN_PROGRES

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_AMBIEN_PROGRES` | varchar(50) | N | Identificador do ambiente Progress (progressLibId). |  |  |
| `DES_AMBIEN_PROGRESS` | varchar(255) | S | Descrição do ambiente Progress. |  |  |

**Dicas de consulta:** Filtrar COD_EMPRESA.

## APLICATIVO

Cadastro de aplicativos externos executáveis (linha de comando) que o Fluig dispara através de um adapter.

**Ciclo de vida:** Config administrativa, volume baixo.

**Atenção:** PK (COD_EMPRESA, COD_APLICAT).

**PK:** COD_EMPRESA, COD_APLICAT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_APLICAT` | varchar(50) | N | Identificador do aplicativo (applicationId). |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| `COD_ADAPTER` | varchar(50) | N | Adapter que executa o aplicativo. |  | ADAPTER.COD_ADAPTER |
| `LIN_COMANDO` | varchar(1000) | N | Linha de comando a executar, até 1000 caracteres. |  |  |
| `DES_APLICAT` | varchar(512) | S | Descrição do aplicativo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_ADAPTER)` → **ADAPTER** `(COD_EMPRESA, COD_ADAPTER)` · N:1 · logical-probable/probable — Adapter usado pelo aplicativo (sem @JoinColumn; casamento por nome e semântica).

**Dicas de consulta:** Filtrar COD_EMPRESA. LIN_COMANDO pode conter caminhos/credenciais: tratar como sensível.
