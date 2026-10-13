# Domínio: ecm-documents

26 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## AREA_DEST

Cadastro legado de áreas de destino (destinatários/áreas organizacionais) do módulo de documentos, com responsável e servidor de execução.

**Ciclo de vida:** Baixo volume, cadastro manual/legado (Datasul/Webdesk).

**Atenção:** PK (COD_EMPRESA, COD_AREA).

**PK:** COD_EMPRESA, COD_AREA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_AREA` | varchar(15) | N | Código da área de destino. |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| `DES_AREA` | varchar(2000) | S | Descrição da área de destino. |  |  |
| `COD_SERVID_EXEC` | varchar(20) | S | Código do servidor de execução associado à área. |  |  |
| `CD_MATR_RESPONS_AREA` | varchar(50) | S | Matrícula do responsável pela área. |  | FDN_USERTENANT.USER_CODE |
| `COD_USUARIO` | varchar(20) | S | Código do usuário associado/criador do registro. |  | FDN_USERTENANT.USER_CODE |

**Dicas de consulta:** Tabela legada; uso residual. Entidade DestinationArea (named query findAll).

## ASSUNTO

Assuntos (tópicos) de classificação de documentos; define se preenchimento é obrigatório e se há e-mail ao eliminar/atualizar.

**Ciclo de vida:** Cadastro administrativo, baixo volume.

**Atenção:** PK (COD_EMPRESA, CD_ASSUNTO).

**PK:** COD_EMPRESA, CD_ASSUNTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `CD_ASSUNTO` | integer | N | Código numérico do assunto. |  |  |
| `NM_ASSUNTO` | varchar(250) | N | Nome/descrição do assunto. |  |  |
| `LOG_ASSUNTO_OBRIG` | bit | S | Indica se informar este assunto é obrigatório. | 1=obrigatório; 0=não |  |
| `LOG_EMAIL_ELIMINA` | bit | S | Indica se envia e-mail quando documento do assunto é eliminado. | 1=envia; 0=não |  |
| `LOG_EMAIL_ATUALIZA` | bit | S | Indica se envia e-mail quando documento do assunto é atualizado. | 1=envia; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, CD_ASSUNTO)` → **ASSUNTO_FAVORITO** `(COD_EMPRESA, CD_ASSUNTO)` · 1:N · logical-probable/probable — Usuários que favoritaram o assunto.
- `(COD_EMPRESA, CD_ASSUNTO)` → **CONFIGUR_OBRIG_ASSUNTO** `(COD_EMPRESA, CD_ASSUNTO)` · 1:N · logical-probable/probable — Regras de obrigatoriedade por destinatário.

**Dicas de consulta:** Entidade Topic.

## ASSUNTO_FAVORITO

Assuntos marcados como favoritos por usuário.

**Ciclo de vida:** Uma linha por (usuário, assunto) favoritado.

**Atenção:** PK composta de 3 colunas.

**PK:** COD_EMPRESA, CD_ASSUNTO, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `CD_ASSUNTO` | integer | N | Assunto favoritado. |  | ASSUNTO.CD_ASSUNTO |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do usuário que favoritou. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, CD_ASSUNTO)` → **ASSUNTO** `(COD_EMPRESA, CD_ASSUNTO)` · N:1 · logical-probable/probable — Assunto favoritado (sem FK física).

**Dicas de consulta:** Entidade FavoriteTopic.

## CAMPO_CUSTOM

Definição de campos customizados (metadados extras) que podem ser associados a documentos.

**Ciclo de vida:** Cadastro administrativo, baixo volume.

**Atenção:** PK (COD_EMPRESA, COD_CAMPO_CUSTOM). Valores por documento em DOCTO_CAMPO_CUSTOM.

**PK:** COD_EMPRESA, COD_CAMPO_CUSTOM

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `COD_CAMPO_CUSTOM` | varchar(100) | N | Código/identificador do campo customizado. |  |  |
| `LOG_MOSTRA_TODOS_DOCTO` | bit | S | Indica se o campo é exibido em todos os documentos (alwaysShow). | 1=sempre exibe; 0=somente onde associado |  |
| `DES_CAMPO_CUSTOM` | varchar(255) | S | Descrição/rótulo do campo customizado. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_CAMPO_CUSTOM)` → **DOCTO_CAMPO_CUSTOM** `(COD_EMPRESA, COD_CAMPO_CUSTOM)` · 1:N · logical-probable/probable — Valores do campo por documento.

**Dicas de consulta:** Entidade CustomFields; query findAlwaysShow.

## CONFIGUR_OBRIG_ASSUNTO

Destinatários (usuário/grupo/todos) para os quais o assunto é obrigatório, por sequência.

**Ciclo de vida:** Linhas criadas ao configurar a obrigatoriedade do assunto.

**Atenção:** PK (COD_EMPRESA, CD_ASSUNTO, NUM_SEQ). NUM_SEQ é sequência local por assunto, NÃO referencia PENDCIA_NOTIF_EMAIL.

**PK:** COD_EMPRESA, CD_ASSUNTO, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NUM_SEQ` | integer | N | Sequência da linha dentro do assunto. |  |  |
| 🔑 `CD_ASSUNTO` | integer | N | Assunto configurado. |  | ASSUNTO.CD_ASSUNTO |
| `IDI_TIP_ATRIBUIC` | integer | S | Tipo do destinatário da atribuição: usuário, grupo ou todos, definindo como interpretar DES_VAL_ATRIBUIC. | 1=usuário; 2=grupo; 3=todos (DocumentSecurityConfigTypeEnum) |  |
| `DES_VAL_ATRIBUIC` | varchar(2000) | S | Valor da atribuição: matrícula do usuário ou código do grupo conforme IDI_TIP_ATRIBUIC; para tipo 3 (todos) é valor genérico. |  |  |
| `LOG_ASSUNTO_OBRIG` | bit | S | Indica se o assunto é obrigatório para o destinatário. | 1=obrigatório; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, CD_ASSUNTO)` → **ASSUNTO** `(COD_EMPRESA, CD_ASSUNTO)` · N:1 · logical-probable/probable — Assunto configurado (queries filtram por topicId).

**Dicas de consulta:** attributeType=3 (todos) via findEveryoneSubjects. Entidade MandatoryTopicConfig. Tipo 1 usuário, 2 grupo.

## CONFIGUR_SEGUR_DOCTO

Lista de permissões/restrições de segurança por documento e versão: quem (usuário, grupo ou todos) tem qual nível de acesso.

**Ciclo de vida:** Várias linhas por versão de documento, criadas ao definir segurança; volume alto.

**Atenção:** PK (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_SEQ). LOG_PERMIS=false representa restrição explícita (findRestrictions). LOG_EXCLUSIV_VERS_ANT mapeia o campo securityVersion.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_SEQ` | integer | N | Sequência da linha de segurança dentro da versão do documento. |  |  |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `IDI_TIP_ATRIBUIC` | integer | S | Tipo do destinatário da atribuição: usuário, grupo ou todos, definindo como interpretar DES_VAL_ATRIBUIC. | 1=usuário; 2=grupo; 3=todos (DocumentSecurityConfigTypeEnum) |  |
| `DES_VAL_ATRIBUIC` | varchar(2000) | S | Valor da atribuição: matrícula do usuário ou código do grupo conforme IDI_TIP_ATRIBUIC; para tipo 3 (todos) é valor genérico. |  |  |
| `LOG_PERMITE_DOWNLOAD` | bit | S | Indica se o destinatário pode baixar o arquivo. | 1=permite; 0=não |  |
| `LOG_PERMIS` | bit | S | Indica se a linha concede (true) ou restringe (false) a permissão. | 1=permissão concedida; 0=restrição |  |
| `IDI_NIV_PERMIS_SEGUR` | integer | S | Nível de permissão de segurança concedido. | -1=sem permissão; 0=leitura; 1=gravação; 2=modificação; 3=total (SolvedPermission) |  |
| `LOG_EXCLUSIV_VERS_ANT` | bit | S | Flag securityVersion; exclusivo/herdado da versão anterior (semântica não confirmada). |  |  |
| `LOG_LISTA_CONTDO` | bit | S | Indica se o destinatário pode listar o conteúdo (showContent); default true quando nulo. | 1=lista; 0=oculta |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão do documento protegida.

**Dicas de consulta:** Sempre filtrar por COD_EMPRESA+NR_DOCUMENTO+NR_VERSAO. DES_VAL_ATRIBUIC contém matrícula/grupo (user_ref/group ref).

## CONHECIMENTO

Registro de ciência/consulta de documentos por colaborador: primeira e última visualização de uma versão.

**Ciclo de vida:** Linha criada na primeira visualização e atualizada nas seguintes; volume alto.

**Atenção:** PK (COD_EMPRESA, CD_MATRICULA, NR_DOCUMENTO, NR_VERSAO). Existem tanto campos Calendar/datetime quanto date+hora legados.

**PK:** COD_EMPRESA, CD_MATRICULA, NR_DOCUMENTO, NR_VERSAO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do colaborador que consultou. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `DATA_HORA_PRIMEIRA_CONSULTA` | datetime | S | Data/hora da primeira consulta (firstView). |  |  |
| `DT_CONHECIMENTO` | date | S | Data em que o colaborador tomou conhecimento do documento. |  |  |
| `DATA_HORA_ULT_CONSULTA` | datetime | S | Data/hora da última consulta (lastView); indexada. |  |  |
| `DT_ULT_CONSULTA` | date | S | Data da última consulta (campo legado). |  |  |
| `HRA_ULT_CON` | varchar(8) | S | Hora da última consulta em texto (HH:mm:ss, campo legado). |  |  |
| `DS_VERSAO` | varchar(4000) | S | Descrição da versão no momento da consulta. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão consultada.

**Dicas de consulta:** Índices: (COD_EMPRESA,NR_DOCUMENTO,NR_VERSAO) e (DATA_HORA_ULT_CONSULTA,COD_EMPRESA). Entidade Knowledge.

## DEFAULT_PROPRIED_DOCTO

Propriedades padrão (atributo/valor/formato) associadas a uma versão de documento.

**Ciclo de vida:** Linhas criadas ao gravar o documento com propriedades padrão.

**Atenção:** PK (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NOM_ATRIBUTO).

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NOM_ATRIBUTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NOM_ATRIBUTO` | varchar(30) | N | Nome da propriedade/atributo padrão. |  |  |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `FORMAT_ATRIBUTO` | varchar(30) | S | Formato do valor do atributo (tipo/máscara). |  |  |
| `DES_VAL_ATRIBUIC` | varchar(2000) | S | Valor do atributo em texto. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão do documento dona da propriedade.

**Dicas de consulta:** Entidade DocumentDefaultProperty; consulta por documento.

## DOCTO_ALOCAD

Check-out/alocação de documentos: documento de origem alocado a um colaborador gerando um documento de destino (cópia de trabalho), usado também em edição WebDAV.

**Ciclo de vida:** Criada no check-out, LOG_ATIVO=false no check-in/devolução.

**Atenção:** PK (COD_EMPRESA, NUM_DOCTO_ORIG, NUM_VERS_ORIG, NUM_DOCTO_DEST). Duas entidades JPA (AllocatedDocument, LockedDocument).

**PK:** COD_EMPRESA, NUM_DOCTO_ORIG, NUM_VERS_ORIG, NUM_DOCTO_DEST

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NUM_DOCTO_DEST` | integer | N | Documento de destino (cópia de trabalho) gerada na alocação. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_DOCTO_ORIG` | integer | N | Documento de origem alocado. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_VERS_ORIG` | integer | N | Versão do documento de origem. |  | DOCUMENTO.NR_VERSAO |
| `LOG_ATIVO` | bit | S | Indica se a alocação está ativa. | 1=ativa; 0=encerrada |  |
| `DAT_DEVOL` | date | S | Data da devolução (check-in). |  |  |
| `HRA_DEVOL` | varchar(12) | S | Hora da devolução em texto (varchar 12). |  |  |
| `LOG_PERMITE_BUSCA` | bit | S | Indica se o check-out é permitido (checkoutAllowed). | 1=permitido; 0=não |  |
| `DAT_BUSCA` | date | S | Data do check-out (busca). |  |  |
| `HRA_BUSCA` | varchar(12) | S | Hora do check-out em texto (varchar 12). |  |  |
| `CD_MATRICULA` | varchar(150) | N | Matrícula do colaborador que alocou o documento. |  | FDN_USERTENANT.USER_CODE |
| `DSL_COMENT` | varchar(255) | S | Comentário informado na alocação/devolução. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NUM_DOCTO_ORIG, NUM_VERS_ORIG)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento/versão de origem.
- `(COD_EMPRESA, NUM_DOCTO_DEST)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento de destino (cópia de trabalho).

**Dicas de consulta:** Ativos: LOG_ATIVO=1 (findActive* por origem/destino). Entidade cacheável.

## DOCTO_ANOTACAO_COLAB

Anotações de colaboradores sobre páginas de um documento (posição X/Y, threads via anotação pai).

**Ciclo de vida:** Criada ao anotar o documento.

**Atenção:** PK 5 colunas inclui NR_ANOTACAO. DTT_CRIAC é bigint (epoch ms provável).

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NR_ANOTACAO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `NR_ANOTACAO` | integer | N | Número sequencial da anotação. |  |  |
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do autor da anotação. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `DSL_ANOTACAO` | varchar(2000) | S | Texto da anotação. |  |  |
| `DTT_CRIAC` | bigint | S | Data/hora de criação como bigint (epoch ms provável). |  |  |
| `NR_PAGINA` | integer | S | Página do documento onde a anotação foi feita. |  |  |
| `NR_ANOTACAO_PAI` | integer | S | NR_ANOTACAO da anotação pai (resposta); 0/nulo se raiz. |  | DOCTO_ANOTACAO_COLAB.NR_ANOTACAO |
| `NR_POSICAOX` | integer | S | Coordenada X da anotação na página. |  |  |
| `NR_POSICAOY` | integer | S | Coordenada Y da anotação na página. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão anotada.
- `(NR_ANOTACAO_PAI)` → **DOCTO_ANOTACAO_COLAB** `(NR_ANOTACAO)` · N:1 · logical-probable/probable — Auto-relação: anotação pai.

**Dicas de consulta:** Sem named queries; filtrar por documento+versão.

## DOCTO_APLICAT

Associação de documento a aplicativos (N:M documento-aplicativo).

**Ciclo de vida:** Linha por vínculo.

**Atenção:** Tabela de junção pura.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_APLICAT

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_APLICAT` | varchar(50) | N | Código do aplicativo associado. |  | APLICATIVO.COD_APLICAT |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_APLICAT)` → **APLICATIVO** `(COD_EMPRESA, COD_APLICAT)` · N:1 · logical-probable/probable — Aplicativo vinculado.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento vinculado.

**Dicas de consulta:** Entidade DocumentApplication.

## DOCTO_CAMPO_CUSTOM

Valor de cada campo customizado por versão de documento.

**Ciclo de vida:** Linha por (documento, versão, campo).

**Atenção:** COD_VALOR é longtext apesar do nome "código".

**PK:** COD_EMPRESA, NR_DOCUMENTO, COD_CAMPO_CUSTOM, NR_VERSAO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `COD_CAMPO_CUSTOM` | varchar(100) | N | Campo customizado. |  | CAMPO_CUSTOM.COD_CAMPO_CUSTOM |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `COD_VALOR` | longtext | S | Valor do campo customizado para o documento (texto longo). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, COD_CAMPO_CUSTOM)` → **CAMPO_CUSTOM** `(COD_EMPRESA, COD_CAMPO_CUSTOM)` · N:1 · logical-probable/probable — Definição do campo.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão do documento.

**Dicas de consulta:** LOB de texto; evitar SELECT * em volume.

## DOCTO_COMENT

Comentários de colaboradores em uma versão de documento.

**Ciclo de vida:** Linha por comentário.

**Atenção:** PK inclui DTT_CRIAC (datetime) para unicidade.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, DTT_CRIAC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do autor do comentário. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `DTT_CRIAC` | datetime | N | Data/hora do comentário. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `NM_COLABORADOR` | varchar(255) | S | Nome do autor, desnormalizado no momento do comentário. |  |  |
| `DSL_COMENT` | varchar(2000) | S | Texto do comentário. |  |  |
| `E_MAIL` | varchar(255) | S | E-mail do autor (dado pessoal). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão comentada.

**Dicas de consulta:** PII: E_MAIL, NM_COLABORADOR.

## DOCTO_CONTDO

Conteúdo binário (arquivo físico) de uma versão de documento quando armazenado no banco.

**Ciclo de vida:** Uma linha por arquivo da versão; volume e tamanho altos.

**Atenção:** BLOB longblob; em instalações com volume/FS externo pode ficar vazio. Evitar SELECT *.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NOM_ARQ_FISIC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NOM_ARQ_FISIC` | varchar(255) | N | Nome do arquivo físico do documento. |  |  |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `BLB_DOCTO_CONTDO` | longblob | S | Bytes do arquivo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão dona do arquivo.

**Dicas de consulta:** Não selecionar BLB_DOCTO_CONTDO sem necessidade. Entidade DocumentData.

## DOCTO_DESTAQ_COLAB

Marcação de "curtir/destacar" um documento por colaborador (DocumentEnjoy).

**Ciclo de vida:** Uma linha por colaborador por versão.

**Atenção:** PK (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA).

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula de quem destacou. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `DTT_CRIAC` | datetime | N | Data/hora do destaque. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão destacada.

**Dicas de consulta:** Entidade DocumentEnjoy.

## DOCTO_NOTIF

Inscrição de colaborador para notificações de alterações em um documento.

**Ciclo de vida:** Linha por assinante.

**Atenção:** Sem NR_VERSAO: vale para todas as versões do documento.

**PK:** COD_EMPRESA, NR_DOCUMENTO, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do assinante. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento monitorado.

**Dicas de consulta:** Entidade DocumentNotify.

## DOCTO_OBS_COLAB

Observações de colaboradores sobre uma versão de documento.

**Ciclo de vida:** Linha por observação.

**Atenção:** DTT_CRIAC é bigint (epoch), diferente de DOCTO_COMENT.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, DTT_CRIAC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do autor. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `DTT_CRIAC` | bigint | N | Data/hora de criação como bigint (epoch ms provável). |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `DSL_COMENT` | varchar(2000) | S | Texto da observação. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão observada.

**Dicas de consulta:** Entidade DocumentObservation.

## DOCTO_RANKING

Nota de avaliação (ranking) dada por colaborador a uma versão de documento.

**Ciclo de vida:** Uma linha por colaborador por versão.

**Atenção:** Média por documento calculada via agregação.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(150) | N | Matrícula do avaliador. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |
| `VAL_NOTA_RANKING` | float | S | Nota atribuída (float); escala não confirmada (provável 1-5). |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão avaliada.

**Dicas de consulta:** Entidade DocumentRanking.

## DOCTO_RELACDO

Relação entre documentos: uma versão de documento aponta para outros documentos relacionados.

**Ciclo de vida:** Linha por vínculo criado pelo usuário.

**Atenção:** Relação armazenada sem versão do relacionado. findInverseRelatedDocs busca pelo lado inverso.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_DOCTO_RELACDO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NUM_DOCTO_RELACDO` | integer | N | Documento relacionado (sem versão). |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Documento/versão de origem.
- `(COD_EMPRESA, NUM_DOCTO_RELACDO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento relacionado.

**Dicas de consulta:** Auto-relação de DOCUMENTO.

## DOCTO_SOCIAL

Mapeia pastas sociais (espaços/comunidades) para pastas de documentos, por alias e tipo de pasta.

**Ciclo de vida:** Criada quando um espaço social cria sua pasta ECM.

**Atenção:** Índice DOCTOSOCIALI001 em NR_DOCUMENTO. Entidade SocialFolder.

**PK:** COD_EMPRESA, COD_APELIDO, TP_PASTA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `TP_PASTA` | varchar(255) | N | Tipo da pasta social (ex. pasta de documentos do espaço). |  |  |
| 🔑 `COD_APELIDO` | varchar(255) | N | Alias do espaço social. |  |  |
| `BOO_SECURITY_ENABLE` | bit | S | Indica se a segurança é aplicada à pasta (null equivale a false). | 1=aplica; 0=não |  |
| `NR_DOCUMENTO` | integer | N | Documento (pasta) ECM associado. |  | DOCUMENTO.NR_DOCUMENTO |
| `FOLDER_ENABLE` | bit | S | Indica se a pasta social está habilitada. | 1=habilitada; 0=não |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-probable/probable — Pasta ECM do espaço.

**Dicas de consulta:** Lookup por (COD_EMPRESA, COD_APELIDO[, TP_PASTA]).

## DOCTO_TAG

Associação de tags a versões de documento.

**Ciclo de vida:** Linha por tag aplicada.

**Atenção:** Tabela de junção.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_TAG

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa/tenant (multi-tenancy); parte da PK, sempre filtrar por ele. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Número (ID lógico) do documento ECM, sem FK física para DOCUMENTO. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `COD_TAG` | varchar(100) | N | Código/texto da tag. |  | TAG.COD_TAG |
| 🔑 `NR_VERSAO` | integer | N | Número da versão do documento; par com NR_DOCUMENTO identifica a versão. |  | DOCUMENTO.NR_VERSAO |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO)` · N:1 · logical-probable/probable — Versão marcada.
- `(COD_EMPRESA, COD_TAG)` → **TAG** `(COD_EMPRESA, COD_TAG)` · N:1 · logical-probable/probable — Tag.

**Dicas de consulta:** Entidade DocumentTag.

## DOCUMENTO

Tabela central do ECM: cada linha é uma VERSÃO de um item da árvore de documentos do GED (pasta, arquivo, fichário de formulário, ficha, anexo de processo, link externo etc.), distinguido por TP_DOCUMENTO.

**Ciclo de vida:** Uma linha por versão (NR_DOCUMENTO + NR_VERSAO); nova versão cria nova linha e a anterior perde VERSAO_ATIVA. Exclusão é lógica (LOG_DELETE=1, lixeira). Volume alto, geralmente a maior tabela do ECM.

**Atenção:** PK composta (COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO). Sempre filtrar COD_EMPRESA, LOG_DELETE=0 e VERSAO_ATIVA=1 para obter o estado corrente. Hierarquia por NR_DOCUMENTO_PAI (0 = raiz). Pastas particulares usam LOG_DOCTO_PARTIC/COD_MATR_PARTIC.

**PK:** COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `NR_DOCUMENTO` | integer | N | Identificador lógico do documento/pasta; é o mesmo em todas as versões. |  |  |
| 🔑 `NR_VERSAO` | integer | N | Número sequencial da versão do documento. |  |  |
| `COD_UUID` | varchar(36) | S | UUID (36 caracteres) do documento, identificador estável usado por APIs/integrações. |  |  |
| `NR_ACESSOS` | integer | S | Contador de acessos/visualizações do documento; usado no ranking de documentos mais populares. |  |  |
| `VERSAO_ATIVA` | bit | S | Indica se esta é a versão ativa (vigente) do documento. | 1=versão ativa; 0=versão antiga |  |
| `DS_COMENTARIO_ADICIONAL` | longtext | S | Comentários adicionais livres informados na publicação (texto longo). |  |  |
| `PERMITIR_MULTI_FICHAS` | bit | S | Em fichário de formulário, permite que o mesmo usuário crie múltiplas fichas. | 1=permite várias fichas por usuário |  |
| `APROV_E_OU` | bit | S | Modo de aprovação com vários aprovadores: E (todos) ou OU (qualquer um). | 1/0 = todos vs. qualquer aprovador (sentido exato não confirmado) |  |
| `LOG_APROVADO` | bit | S | Indica se a versão foi aprovada no fluxo de aprovação de documentos. | 1=aprovado; 0=pendente de aprovação |  |
| `DT_APROVACAO` | date | S | Data em que a versão foi aprovada. |  |  |
| `CD_ATUALIZACAO` | integer | S | Código/identificador de atualização associado ao documento (sequência de atualização). |  |  |
| `DES_PRINC_FICHA` | varchar(255) | S | Descrição principal da ficha: texto que representa o registro de formulário (campo descritor do fichário). |  |  |
| `LOG_PASTA_CHECKOUT` | bit | S | Marca a pasta particular usada para armazenar documentos em check-out do usuário. | 1=pasta de check-out |  |
| `CD_MATRICULA` | varchar(255) | S | Matrícula do usuário criador/proprietário do documento. |  | FDN_USERTENANT.USER_CODE (colleagueId) |
| `IDI_TIP_ARMAZ_LP` | integer | S | Tipo de armazenamento/conversão para longo prazo (PDF/A) do documento. |  |  |
| `NUM_CRC` | bigint | S | CRC do arquivo físico, usado para detectar conteúdo duplicado/alterado. |  |  |
| `DT_CRIACAO` | date | S | Data de criação do documento (sem hora). |  |  |
| `NM_DATASET` | varchar(255) | S | Nome do dataset associado, quando o fichário/formulário expõe dados como dataset. |  |  |
| `LOG_DELETE` | bit | S | Exclusão lógica: 1 = documento na lixeira/excluído. | 1=excluído (lixeira); 0=ativo |  |
| `DS_PRINCIPAL_DOCUMENTO` | varchar(4000) | S | Descrição/nome exibido do documento ou pasta (até 4000 caracteres). |  |  |
| `NUM_DOCTO_PROPRIED` | integer | S | NR_DOCUMENTO do documento de propriedades (fichário/pasta) do qual este herda metadados. |  | DOCUMENTO.NR_DOCUMENTO |
| `NUM_VERS_PROPRIED` | integer | S | Versão do documento de propriedades referenciado em NUM_DOCTO_PROPRIED. |  | DOCUMENTO.NR_VERSAO |
| `TP_DOCUMENTO` | varchar(255) | N | Tipo do item do GED. | 0=pasta raiz; 1=pasta; 2=documento (arquivo); 3=link externo; 4=fichário (formulário); 5=ficha (registro de formulário); 6=publicado em pool; 7=anexo de workflow; 8=documento editável; 9=aplicação externa; 10=relatório/arquivo; 15=pasta social; 16=formulário de metadados |  |
| `CD_TIPO_DOC` | varchar(255) | S | Código do tipo de documento (classificação do usuário) aplicado ao item. |  | TIPO_DOCUMENTO.CD_TIPO_DOC |
| `LOG_PERMITE_DOWNLOAD` | bit | S | Indica se o download do arquivo é permitido. | 1=permite download |  |
| `LOG_RASCUNHO` | bit | S | Indica versão em rascunho (não publicada). | 1=rascunho |  |
| `DT_EXPIRACAO` | date | S | Data de expiração do documento (validade). |  |  |
| `LOG_DOCTO_EXPIRA` | bit | S | Indica se o documento possui prazo de expiração. | 1=expira |  |
| `CD_DOCUMENTO_EXT` | varchar(255) | S | Código/identificador externo do documento (integração com sistema externo). |  |  |
| `NR_ICONE` | integer | S | Número do ícone associado ao documento/pasta. |  | ICONE.NR_ICONE |
| `LOG_NAO_ALTERA` | bit | S | Documento imutável: não pode ser alterado. | 1=imutável |  |
| `LOG_INDEXAD` | bit | S | Indica se o documento já foi indexado no motor de busca. | 1=indexado; 0=pendente de indexação |  |
| `LOG_HERDA_APROV` | bit | S | Herda os aprovadores da pasta pai. | 1=herda aprovadores |  |
| `LOG_HERDA_SEGUR` | bit | N | Herda a segurança (permissões) da pasta pai. | 1=herda segurança do pai |  |
| `LOG_USA_VISUALIZ` | bit | S | Usa o visualizador interno do Fluig para exibir o arquivo. | 1=visualizador interno |  |
| `NR_MARCA_DAGUA` | integer | S | Marca d'água aplicada na visualização/download do documento. |  | MARCA_DAGUA.NR_MARCA_DAGUA |
| `DS_PALAVRA_CHAVE` | longtext | S | Palavras-chave do documento para busca (texto longo). |  |  |
| `CD_IDIOMA` | varchar(255) | S | Código do idioma do documento (ex.: pt_BR). |  |  |
| `DT_ATUALIZACAO` | date | S | Data da última modificação. |  |  |
| `HRA_ATUALIZ` | varchar(255) | S | Hora da última modificação, em texto (HH:mm:ss). |  |  |
| `COD_LISTA` | integer | S | Código da meta-lista (lista de metadados/formulário) vinculada ao documento. |  | META_LISTA.COD_LISTA |
| `COD_REG_LISTA` | integer | S | Código do registro dentro da meta-lista (card/registro de formulário). |  |  |
| `COD_MIME_TYPE` | varchar(255) | S | MIME type do arquivo (ex.: application/pdf). |  |  |
| `NR_DIAS_NOT_EXP` | integer | S | Dias de antecedência para notificar a expiração; NULL usa o parâmetro global. |  |  |
| `LOG_DATASET_ATIVO` | bit | S | Dataset considera apenas registros ativos do fichário. | 1=somente ativos |  |
| `NR_DOCUMENTO_PAI` | integer | S | NR_DOCUMENTO da pasta pai na árvore (0 = raiz). |  | DOCUMENTO.NR_DOCUMENTO |
| `IDI_STATUS_CONV_PDF` | integer | S | Status da conversão do arquivo para PDF para visualização. | 0=não convertido; 1=convertido; 2=conversão não suportada; 3=arquivo não encontrado; 4=OpenOffice indisponível; 5=erro de conversão |  |
| `COD_TIP_VISUALIZ` | varchar(255) | S | Motor de renderização/visualização de PDF utilizado (pdfRenderEngine). |  |  |
| `IDI_TIP_PERMIS` | integer | S | Tipo de permissão de segurança aplicada ao documento (default 0). |  |  |
| `NM_ARQUIVO_FISICO` | varchar(255) | S | Nome do arquivo físico gravado no volume de armazenamento. |  |  |
| `NUM_PRIORID` | integer | S | Prioridade do documento/ordem de exibição. |  |  |
| `COD_MATR_PARTIC` | varchar(255) | S | Matrícula do dono da pasta/documento particular (privado). |  | FDN_USERTENANT.USER_CODE (privateColleagueId) |
| `LOG_DOCTO_PARTIC` | bit | S | Indica documento/pasta particular do usuário. | 1=particular |  |
| `LOG_PROCES_BATCH` | bit | S | Indica que o documento está em processamento em lote. | 1=em processamento batch |  |
| `CD_PUBLICADOR` | varchar(255) | S | Matrícula do usuário que publicou esta versão. |  | FDN_USERTENANT.USER_CODE (publisherId) |
| `QUOTA` | integer | S | Cota de espaço da pasta (MB); 0/NULL sem cota. |  |  |
| `NM_ARQUIVOS_RELACIONADOS` | longtext | S | Lista de arquivos relacionados/anexos do documento (texto longo). |  |  |
| `IDI_TIP_RESTRIC` | integer | S | Tipo de restrição de segurança aplicada ao documento (default 0). |  |  |
| `FDN_SITECODE` | varchar(255) | S | Código do site/portal associado ao documento. |  |  |
| `NUM_TAM_ARQ_FISIC` | float | S | Tamanho do arquivo físico (em MB, float, conforme uso em cotas). |  |  |
| `DOCTO_SOCIAL` | varchar(255) | S | Indicador/identificador de documento social (rede social/feed). |  |  |
| `IDI_STATUS_ARMAZ_LP` | integer | S | Status do armazenamento de longo prazo do documento. |  |  |
| `CD_ASSUNTO` | integer | S | Código do assunto (tópico) do documento. |  | ASSUNTO.CD_ASSUNTO |
| `LOG_TRADUZIR` | bit | N | Indica que o documento é traduzível. | 1=traduzir |  |
| `LOG_ATUALIZ_PROPRIED_ISO` | bit | N | Atualizar propriedades ISO do documento. | 1=atualizar |  |
| `USED_QUOTA` | float | S | Espaço de cota já utilizado na pasta (MB). |  |  |
| `LOG_NOTIFICA_USUAR` | bit | S | Notifica usuários sobre alterações/publicação do documento. | 1=notificar |  |
| `DT_INI_VALIDADE` | date | S | Data de início da validade do documento. |  |  |
| `DS_VERSAO` | varchar(4000) | S | Descrição/comentário da versão (até 4000 caracteres). |  |  |
| `CD_VISAO` | varchar(255) | S | Código da visão associada ao documento. |  |  |
| `COD_VOL_FISIC` | varchar(255) | S | Código do volume físico de armazenamento onde o arquivo está. |  | VOLUME.COD_VOL_FISIC |
| `LOG_PUBLIC` | bit | S | Documento público (acessível sem autenticação). | 1=público |  |
| `METADATAFORM_VERSION_STATUS` | varchar(255) | S | Status da versão de formulário de metadados. |  |  |
| `HASH_ANNOTATIONS` | varchar(255) | S | Hash das anotações do documento; compara se anotações mudaram entre versões. |  |  |

**Relacionamentos (saem desta tabela):**

- `(NR_DOCUMENTO)` → **LINK_DOCTO_VIRTUAL** `(NR_DOCUMENTO)` · 1:N · hql-join/confirmed — Links virtuais que apontam para este documento (Document.findLinkDocuments).
- `(COD_EMPRESA, NR_DOCUMENTO_PAI)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-confirmed/confirmed — Auto-relação: pasta pai.
- `(COD_EMPRESA, CD_TIPO_DOC)` → **TIPO_DOCUMENTO** `(COD_EMPRESA, CD_TIPO_DOC)` · N:1 · logical-probable/probable — Tipo de documento.
- `(COD_EMPRESA, NR_MARCA_DAGUA)` → **MARCA_DAGUA** `(COD_EMPRESA, NR_MARCA_DAGUA)` · N:1 · logical-confirmed/confirmed — Marca d'água aplicada (query COUNT_DOCUMENTS_BY_WATERMARK).
- `(COD_EMPRESA, NR_ICONE)` → **ICONE** `(COD_EMPRESA, NR_ICONE)` · N:1 · logical-probable/probable — Ícone do item.
- `(COD_EMPRESA, COD_LISTA)` → **META_LISTA** `(COD_EMPRESA, COD_LISTA)` · N:1 · logical-probable/probable — Meta-lista de formulário.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` → **DOCTO_DESTAQ_COLAB** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` · 1:N · logical-probable/probable — Heurística; DOCTO_DESTAQ_COLAB é filho (por usuário) de DOCUMENTO por (EMPRESA,DOC,VERSAO); matrícula não é chave da relação.
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` → **DOCTO_RANKING** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` · 1:N · logical-probable/probable — Heurística; ranking por usuário refere o documento por (EMPRESA,DOC,VERSAO).
- `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` → **PREFER_PASTA** `(COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA)` · 1:N · logical-probable/probable — Heurística; preferências de pasta por usuário referenciam o documento.
- `(CD_MATRICULA)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Criador do documento (também CD_PUBLICADOR, COD_MATR_PARTIC). [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Filtrar sempre COD_EMPRESA; para estado atual usar VERSAO_ATIVA=1 AND LOG_DELETE=0. TP_DOCUMENTO é texto (comparar com aspas: '1','2'...). Colunas longtext: DS_COMENTARIO_ADICIONAL, DS_PALAVRA_CHAVE, NM_ARQUIVOS_RELACIONADOS. Contém matrículas de usuários (dado pessoal indireto). Arquivo físico em NM_ARQUIVO_FISICO + COD_VOL_FISIC. Hierarquia via NR_DOCUMENTO_PAI.

## DOCUMENT_ACCUSOFT_METRICS

Registro de métricas de uso do visualizador Accusoft (PrizmDoc) por tipo de arquivo: cada linha é um evento de conversão/visualização.

**Ciclo de vida:** Inserida a cada evento de métrica; apenas acréscimo. Pode crescer continuamente.

**Atenção:** Usa TENANT_ID (e não COD_EMPRESA). Sem FK.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint(20) | N | Identificador sequencial da métrica. |  |  |
| `TENANT_ID` | bigint(20) | N | Identificador do tenant/empresa dona da métrica. |  |  |
| `METRIC_KEY` | varchar(255) | N | Chave/nome da métrica Accusoft registrada. |  |  |
| `METRIC_TIME` | datetime | N | Data e hora do evento da métrica. |  |  |
| `MIME_TYPE` | varchar(120) | N | MIME type do arquivo processado. |  |  |
| `FILE_EXTENSION` | varchar(15) | N | Extensão do arquivo processado (ex.: pdf, docx). |  |  |

**Dicas de consulta:** Filtrar por TENANT_ID e METRIC_TIME. Útil só para licenciamento/estatística do visualizador.

## LINK_DOCTO_VIRTUAL

Links virtuais (atalhos): um documento aparece em uma pasta adicional sem ser copiado.

**Ciclo de vida:** Criada ao criar atalho para um documento; LOG_DELETE marca o link na lixeira.

**Atenção:** PK (COD_EMPRESA, NR_DOCTO_PAI_CORREN, NR_DOCUMENTO).

**PK:** COD_EMPRESA, NR_DOCTO_PAI_CORREN, NR_DOCUMENTO

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `NR_DOCTO_PAI_CORREN` | integer | N | Pasta pai atual em que o link aparece. |  | DOCUMENTO.NR_DOCUMENTO |
| 🔑 `NR_DOCUMENTO` | integer | N | Documento original apontado pelo link. |  | DOCUMENTO.NR_DOCUMENTO |
| `LOG_DELETE` | bit | S | Exclusão lógica do link. | 1=link na lixeira |  |
| `NR_DOCTO_PAI_ORIG` | integer | N | Pasta pai original do documento no momento da criação do link. |  | DOCUMENTO.NR_DOCUMENTO |

**Relacionamentos (saem desta tabela):**

- `(NR_DOCUMENTO)` → **DOCUMENTO** `(NR_DOCUMENTO)` · N:1 · hql-join/confirmed — Documento ligado (Document.findLinkDocuments).
- `(COD_EMPRESA, NR_DOCTO_PAI_CORREN)` → **DOCUMENTO** `(COD_EMPRESA, NR_DOCUMENTO)` · N:1 · logical-confirmed/confirmed — Pasta onde o link aparece.

**Dicas de consulta:** Para listar links de uma pasta: join DOCUMENTO d ON d.NR_DOCUMENTO=l.NR_DOCUMENTO com l.NR_DOCTO_PAI_CORREN=:pasta, l.LOG_DELETE=0, d.VERSAO_ATIVA=1.

## MARCA_DAGUA

Cadastro de marcas d'água (texto, fonte, cor, alinhamento) aplicáveis a documentos na visualização/download.

**Ciclo de vida:** Criada pelo administrador do GED; baixo volume.

**Atenção:** PK (COD_EMPRESA, NR_MARCA_DAGUA). Referenciada por DOCUMENTO.NR_MARCA_DAGUA.

**PK:** COD_EMPRESA, NR_MARCA_DAGUA

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `NR_MARCA_DAGUA` | integer | N | Identificador numérico da marca d'água. |  |  |
| `NOM_MARCA_DAGUA` | varchar(100) | N | Nome/descrição da marca d'água. |  |  |
| `DS_MARCA_DAGUA` | varchar(100) | N | Texto impresso na marca d'água. |  |  |
| `COLOR` | varchar(10) | N | Cor do texto (formato hexadecimal, ex.: #FF0000). |  |  |
| `FONT_FAMILY` | varchar(100) | N | Família de fonte usada. |  |  |
| `FONT_SIZE` | integer | N | Tamanho da fonte em pontos. |  |  |
| `HORIZONTAL_ALIGN` | varchar(10) | N | Alinhamento horizontal. | left; center; right |  |
| `VERTICAL_ALIGN` | varchar(10) | N | Alinhamento vertical. | top; middle; bottom (top confirmado) |  |
| `OPACITY` | integer | N | Opacidade em porcentagem (0-100). |  |  |
| `NUM_ROTACAO` | double | N | Rotação do texto em graus. |  |  |
| `LOG_DATA` | bit | S | Exibe a data atual na marca. | 1=exibe |  |
| `LOG_HORA` | bit | S | Exibe a hora atual na marca. | 1=exibe |  |
| `LOG_USUARIO` | bit | S | Exibe o usuário que acessa o documento. | 1=exibe |  |
| `LOG_VERSAO` | bit | S | Exibe a versão do documento. | 1=exibe |  |
| `LOG_DATA_CRIACAO` | bit | S | Exibe a data de criação do documento. | 1=exibe |  |
| `LOG_DATA_ATUALIZACAO` | bit | S | Exibe a data de atualização do documento. | 1=exibe |  |
| `TP_MARCA_DAGUA` | integer | N | Tipo da marca d'água (inteiro); valores não confirmados no código inspecionado. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, NR_MARCA_DAGUA)` → **DOCUMENTO** `(COD_EMPRESA, NR_MARCA_DAGUA)` · 1:N · logical-confirmed/confirmed — Documentos que usam a marca (DOCUMENTO.NR_MARCA_DAGUA).

**Dicas de consulta:** Antes de excluir, contar uso em DOCUMENTO.NR_MARCA_DAGUA.

## TIPO_DOCUMENTO

Cadastro de tipos de documento (classificação definida pelo cliente) aplicados a documentos do GED.

**Ciclo de vida:** Criada pelo administrador; baixo volume.

**Atenção:** PK (COD_EMPRESA, CD_TIPO_DOC). Não confundir com DOCUMENTO.TP_DOCUMENTO (tipo estrutural).

**PK:** COD_EMPRESA, CD_TIPO_DOC

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Código da empresa (tenant) dona do registro; faz parte da PK e deve ser filtrado em toda consulta. |  |  |
| 🔑 `CD_TIPO_DOC` | varchar(255) | N | Código do tipo de documento. |  |  |
| `DS_TIPO_DOC` | varchar(2000) | N | Descrição do tipo de documento. |  |  |

**Relacionamentos (saem desta tabela):**

- `(COD_EMPRESA, CD_TIPO_DOC)` → **DOCUMENTO** `(COD_EMPRESA, CD_TIPO_DOC)` · 1:N · logical-probable/probable — Documentos classificados neste tipo.

**Dicas de consulta:** Join com DOCUMENTO por COD_EMPRESA e CD_TIPO_DOC.
