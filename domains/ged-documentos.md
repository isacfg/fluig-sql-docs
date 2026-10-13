# Domínio: ged-documentos

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## APROVACAO

Registro da aprovação de um documento do GED por um aprovador em um nível de aprovação (resultado, data, observação, assinatura).

**Ciclo de vida:** Linhas criadas ao enviar versão de documento para aprovação; atualizadas quando o aprovador decide.

**Atenção:** PK (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC). Resultado nulo = pendente.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do aprovador. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Número do documento aprovado. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_NIV_APROVAC` | integer | N | Número do nível de aprovação do documento. |  | NIVEL_APROVACAO.NUM_NIV_APROVAC |
| 🔑 `NR_VERSAO` | integer | N | Versão do documento em aprovação. |  | DOCUMENTO.NR_VERSAO |
| `APROVADO` | bit | S | Indica se o aprovador aprovou o documento (true) ou não/ainda pendente. | 1=aprovado; 0/NULL=não aprovado ou pendente |  |
| `DT_APROVA` | date | S | Data em que a aprovação foi registrada. |  |  |
| `LOG_ASS_OBRIGATORIA` | bit | S | Indica se a assinatura eletrônica é obrigatória nesta aprovação. | 1=obrigatória; 0=não |  |
| `OBSERVACAO` | longtext | S | Observação/justificativa do aprovador (texto longo). |  |  |
| `LOG_ASSINADO` | bit | S | Indica se o aprovador assinou eletronicamente. | 1=assinado; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão de documento sendo aprovada.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` → **NIVEL_APROVACAO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` · N:1 · logical-probable/probable — Nível de aprovação ao qual o registro pertence.

**Dicas de consulta:** Filtrar COD_EMPRESA; juntar com APROVADOR pela mesma PK (tipo usuário). OBSERVACAO é LOB.

## APROVADOR

Define os aprovadores (usuário ou grupo) designados para cada nível de aprovação de uma versão de documento do GED.

**Ciclo de vida:** Criada ao configurar o fluxo de aprovação do documento; removida/recriada ao alterar aprovadores.

**Atenção:** PK inclui IDI_TIP_APRVDOR: CD_MATRICULA pode ser matrícula de usuário ou código de grupo conforme o tipo.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, IDI_TIP_APRVDOR, CD_MATRICULA, NUM_NIV_APROVAC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `IDI_TIP_APRVDOR` | integer | N | Tipo do aprovador; define se CD_MATRICULA é usuário ou grupo. | 0=usuário; 1=grupo |  |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário ou código do grupo aprovador, conforme IDI_TIP_APRVDOR. |  | FDN_USERTENANT.USER_CODE ou FDN_GROUP.GROUP_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Número do documento do GED. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_NIV_APROVAC` | integer | N | Número do nível de aprovação. |  | NIVEL_APROVACAO.NUM_NIV_APROVAC |
| 🔑 `NR_VERSAO` | integer | N | Versão do documento. |  | DOCUMENTO.NR_VERSAO |
| `LOG_ASS_OBRIGATORIA` | bit | S | Indica se a assinatura eletrônica é obrigatória para este aprovador. | 1=obrigatória; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` → **NIVEL_APROVACAO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` · N:1 · logical-probable/probable — Nível ao qual o aprovador pertence.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC)` → **APROVACAO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC)` · 1:1 · logical-probable/probable — Registro de decisão do aprovador; só existe para tipo usuário (para grupo a decisão é gravada pelo usuário que aprova).

**Dicas de consulta:** Para obter usuários de aprovadores tipo grupo é preciso expandir o grupo.
