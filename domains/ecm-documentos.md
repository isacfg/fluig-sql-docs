# Domínio: ecm-documentos

3 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## LOG_COP_CONTROLAD

Log de emissao de copias controladas (impressao controlada) de documentos do GED. Cada linha registra protocolo, documento/versao, area, emissor e impressora.

**Ciclo de vida:** Inserida a cada emissao de copia controlada; apenas append, sem atualizacao esperada.

**Atenção:** PK (NUM_PROTOC, COD_EMPRESA). Entidade ControlledCopyLog. Documento identificado por NR_DOCUMENTO+NR_VERSAO.

**PK:** NUM_PROTOC, COD_EMPRESA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_PROTOC` | integer | N | Numero de protocolo sequencial da copia controlada emitida. |  |  |
| `CD_MATR_RESPONS_AREA` | varchar(255) | S | Matricula do responsavel pela area atribuida a copia controlada. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `COD_AREA` | varchar(255) | N | Codigo da area destinataria da copia controlada. |  | AREA_DEST.COD_AREA |
| `NR_DOCUMENTO` | integer | N | Numero (id) do documento do GED cuja copia foi emitida. |  | DOCUMENTO.NR_DOCUMENTO |
| `COD_SERVID_EXEC` | varchar(255) | S | Identificador do servidor que executou a emissao da copia. |  |  |
| `CD_MATR_EMISSOR` | varchar(255) | S | Matricula do usuario que emitiu a copia controlada. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `DAT_EMIS` | date | N | Data de emissao da copia controlada. |  |  |
| `HRA_EMIS` | varchar(255) | N | Hora de emissao no formato texto (HH:mm:ss provavel). |  |  |
| `NOM_LOCALIZ_IMPRSOR` | varchar(255) | S | Nome/localizacao da impressora usada na emissao. |  |  |
| `NR_VERSAO` | integer | N | Versao do documento cuja copia foi emitida. |  | DOCUMENTO.NR_VERSAO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_AREA)` → **AREA_DEST** `(COD_EMPRESA, COD_AREA)` · N:1 · logical-probable/probable — Area destinataria da copia; nome coincide, sem FK fisica nem join no codigo verificado.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento/versao cuja copia foi emitida.

**Dicas de consulta:** Filtrar por COD_EMPRESA. Join com DOCUMENTO por (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO). Contem matriculas de usuario.

## MOVTO_APROVAC

Movimentos de aprovacao de documentos do GED: cada acao (analise, aprovacao, assinatura) de um aprovador numa iteracao e nivel de aprovacao de uma versao.

**Ciclo de vida:** Inserida a cada acao de aprovador no fluxo de aprovacao do documento; cresce com o uso de aprovacao.

**Atenção:** PK composta de 6 colunas (tenant, documento, versao, iteracao, nivel, sequencia de movimento).

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_SEQ_ITERAC, NUM_NIV_APROVAC, NUM_SEQ_MOVTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Numero do documento do GED em aprovacao. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_SEQ_ITERAC` | integer | N | Sequencial da iteracao (rodada) de aprovacao do documento. |  |  |
| 🔑 `NUM_NIV_APROVAC` | integer | N | Numero do nivel de aprovacao onde ocorreu o movimento. |  | NIVEL_APROVACAO.NUM_NIV_APROVAC |
| 🔑 `NUM_SEQ_MOVTO` | integer | N | Sequencial do movimento dentro da iteracao/nivel. |  |  |
| 🔑 `NR_VERSAO` | integer | N | Versao do documento em aprovacao. |  | DOCUMENTO.NR_VERSAO |
| `LOG_ANALIS` | bit | S | Indica se o aprovador ja analisou o documento neste movimento. | 1=analisado; 0=nao |  |
| `LOG_APROVADO` | bit | S | Indica se o movimento resultou em aprovacao. | 1=aprovado; 0=reprovado/nao aprovado |  |
| `LOG_ITERAC_FECHADA` | bit | S | Indica se este movimento fechou a iteracao de aprovacao. | 1=iteracao fechada; 0=aberta |  |
| `CD_MATRICULA` | varchar(150) | N | Matricula do aprovador que realizou o movimento. |  | FDN_USERTENANT.USER_CODE (via matricula) |
| `DAT_MOVTO_APROVAC` | date | S | Data do movimento de aprovacao. |  |  |
| `HRA_MOVTO_APROVAC` | varchar(8) | S | Hora do movimento em texto (HH:mm:ss). |  |  |
| `DSL_OBS_MOVTO_APROVAC` | longtext | S | Observacao textual (LOB) registrada pelo aprovador. |  |  |
| `DAT_ENVIO_APROVAC` | date | S | Data em que o documento foi enviado para aprovacao. |  |  |
| `LOG_ASSINADO` | bit | S | Indica se o movimento foi assinado digitalmente/eletronicamente. | 1=assinado; 0=nao |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC)` → **APROVACAO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC)` · N:1 · logical-probable/probable — Aprovador designado no nivel; todas as colunas da PK de APROVACAO existem aqui, sem FK fisica.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` → **NIVEL_APROVACAO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC)` · N:1 · logical-probable/probable — Nivel de aprovacao ao qual o movimento pertence (adicionada: PK de NIVEL_APROVACAO coberta).
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento/versao em aprovacao.

**Dicas de consulta:** Filtrar por COD_EMPRESA+NR_DOCUMENTO+NR_VERSAO. Flags LOG_* sao bit (0/1) anulaveis.

## NIVEL_APROVACAO

Niveis de aprovacao configurados para uma versao de documento do GED, com modo de aprovacao e descricao do nivel.

**Ciclo de vida:** Criada ao configurar o fluxo de aprovacao do documento; poucas linhas por versao.

**Atenção:** PK (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC). Named query ApprovalLevel.findApprovalLevelsForDocument.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dona da linha; faz parte da PK e deve ser filtrada em toda consulta. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NR_DOCUMENTO` | integer | N | Numero do documento do GED ao qual o nivel pertence. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_NIV_APROVAC` | integer | N | Numero (ordem) do nivel de aprovacao. |  |  |
| 🔑 `NR_VERSAO` | integer | N | Versao do documento ao qual o nivel pertence. |  | DOCUMENTO.NR_VERSAO |
| `IDI_TIP_APROVAC` | integer | N | Modo de aprovacao do nivel (campo approvalMode); valores nao confirmados no codigo lido. |  |  |
| `DES_TIP_APROVAC` | varchar(255) | N | Descricao textual do nivel de aprovacao (campo levelDescription). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versao do documento dona do nivel.

**Dicas de consulta:** Filtrar por COD_EMPRESA+NR_DOCUMENTO+NR_VERSAO.
