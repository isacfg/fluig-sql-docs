# Domínio: bpm-definicao-processo

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## PROPRIED_AVANCAD_PROCES

Propriedades avançadas (chave/valor) de uma versão de definição de processo, configuradas no modelador.

**Ciclo de vida:** Gravadas ao salvar/publicar uma versão do processo; regravadas por versão. Volume baixo.

**Atenção:** Versionada: sempre inclui NUM_VERS. Entidade AdvancedProcessProperties.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_PROPRIED

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo (processId). |  | DEF_PROCES.COD_DEF_PROCES |
| 🔑 `COD_PROPRIED` | varchar(200) | N | Identificador/nome da propriedade avançada. |  |  |
| 🔑 `NUM_VERS` | integer | N | Número da versão da definição de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `DSL_VAL_PROPRIED` | varchar(2000) | S | Valor da propriedade (texto até 2000 caracteres). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão de processo dona da propriedade (sem FK física).

**Dicas de consulta:** Consultar por (COD_EMPRESA, COD_DEF_PROCES, NUM_VERS). Named queries: findAll, findByProcess.

## SEGUR_ANEXO_PROCES

Regras de segurança de anexos por versão de processo: define quem (mecanismo de atribuição) tem qual nível de acesso aos anexos da solicitação.

**Ciclo de vida:** Gravadas ao salvar a definição do processo; substituídas por versão.

**Atenção:** Versionada por NUM_VERS. NUM_SEQ é sequência da regra dentro do processo/versão, não a de PENDCIA_NOTIF_EMAIL.

**PK:** COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `COD_DEF_PROCES` | varchar(50) | N | Código da definição de processo à qual a regra se aplica. |  | DEF_PROCES.COD_DEF_PROCES |
| 🔑 `NUM_SEQ` | integer | N | Sequência da regra de segurança dentro do processo/versão. |  |  |
| 🔑 `NUM_VERS` | integer | N | Versão da definição de processo. |  | VERS_DEF_PROCES.NUM_VERS |
| `IND_NIV_ACES` | varchar(8) | S | Nível de acesso concedido aos anexos (código textual definido no modelador). |  |  |
| `DSL_CONFIGUR_MECAN_ATRIBUIC` | longtext | S | Configuração (serializada) do mecanismo de atribuição que resolve os usuários da regra. |  |  |
| `COD_MECAN_ATRIBUIC` | varchar(25) | N | Código do mecanismo de atribuição (engineAllocationId), ex.: por usuário, grupo ou papel. |  | MECAN_ATRIBUIC.COD_MECAN_ATRIBUIC |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` → **VERS_DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES, NUM_VERS)` · N:1 · logical-probable/probable — Versão de processo dona da regra.
- `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` → **MECAN_ATRIBUIC** `(COD_EMPRESA, COD_MECAN_ATRIBUIC)` · N:1 · logical-probable/probable — Mecanismo de atribuição referenciado por código; o mecanismo pode ser customizado e não necessariamente existir como linha.

**Dicas de consulta:** Consultar por (COD_EMPRESA, COD_DEF_PROCES, NUM_VERS). Named query: findByProcess.
