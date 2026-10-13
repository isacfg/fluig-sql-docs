# Domínio: foundation-identity-access

18 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_GROUP

Grupo de usuários do Fluig (de usuários, cloud ou comunidade), por tenant. Usado em permissões, papéis e agrupamento de usuários.

**Ciclo de vida:** Criado pela administração de grupos ou internamente (INTERNAL=1); volume baixo a médio.

**Atenção:** Identificado logicamente por (TENANT_ID, GROUP_CODE); FDN_GROUPUSERROLE referencia o grupo por esse par e não por GROUP_ID. TENANT_ID=-1 é usado para grupos globais (findByCodeWithoutTenant). Consultas de UI filtram INTERNAL=0.

**PK:** GROUP_ID · **Unique:** (TENANT_ID, GROUP_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `GROUP_ID` | bigint(20) | N | Chave primária surrogate do grupo. |  |  |
| `GROUP_CODE` | varchar(50) | S | Código do grupo, único por tenant; usado como referência lógica em permissões e membros. |  |  |
| `DESCRIPTION` | varchar(255) | S | Nome/descrição exibido do grupo; usado em ordenação e filtro LIKE. |  |  |
| `GROUP_TYPE` | varchar(50) | N | Tipo do grupo, string do enum FDNGroupType. | user=grupo de usuários; cloud=grupo cloud; community=grupo de comunidade |  |
| `INTERNAL` | bit(1) | N | Indica grupo interno do sistema, oculto das listagens normais (consultas filtram INTERNAL=false). | 1=interno do sistema; 0=criado pelo usuário |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.

**Dicas de consulta:** Sempre filtrar por TENANT_ID. Para listar grupos visíveis use INTERNAL=0. Membros em FDN_GROUPUSERROLE (por GROUP_CODE+TENANT_ID). Propriedades extras em FDN_GROUPDATA.

## FDN_GROUPDATA

Propriedades chave/valor adicionais de um grupo (FDN_GROUP).

**Ciclo de vida:** Linhas criadas/atualizadas junto com o grupo; volume baixo.

**Atenção:** Padrão EAV: um par DATA_KEY/DATA_VALUE por linha, filhas de FDN_GROUP.

**PK:** GROUPDATA_ID · **Unique:** (GROUPDATA_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `GROUPDATA_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DATA_KEY` | varchar(255) | N | Nome da propriedade do grupo (chave do par chave/valor). |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor textual da propriedade, até 4000 caracteres. |  |  |
| `GROUP_ID` | bigint(20) | N | Grupo dono da propriedade. |  | FDN_GROUP.GROUP_ID |

**Relacionamentos (saem desta tabela):**

- `(GROUP_ID)` → **FDN_GROUP** `(GROUP_ID)` · N:1 · jpa-join/confirmed — Grupo dono da propriedade (FDNGroupData.group).

**Dicas de consulta:** Junte com FDN_GROUP via GROUP_ID para obter o tenant.

## FDN_GROUPUSERROLE

Tabela de associação de membros de grupo: liga um grupo a um usuário (LOGIN), a um papel (ROLE_CODE) ou a um subgrupo (CHILD_GROUPCODE).

**Ciclo de vida:** Linhas criadas ao adicionar membros/papéis a um grupo, removidas ao remover; volume proporcional ao número de membros.

**Atenção:** Cada linha usa tipicamente apenas UM de LOGIN, ROLE_CODE ou CHILD_GROUPCODE (os demais NULL) -- inferido da nulabilidade; conferir ao consultar. Referencia grupos por código+tenant, não por ID.

**PK:** GROUPUSERROLE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `GROUPUSERROLE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `CHILD_GROUPCODE` | varchar(50) | S | Código do subgrupo membro do grupo (grupo aninhado); NULL se a linha for de usuário ou papel. |  | FDN_GROUP.GROUP_CODE |
| `GROUP_CODE` | varchar(50) | N | Código do grupo pai ao qual a linha pertence. |  | FDN_GROUP.GROUP_CODE |
| `LOGIN` | varchar(150) | S | Login do usuário membro do grupo; NULL se for papel ou subgrupo. |  | FDN_USERTENANT.LOGIN |
| `ROLE_CODE` | varchar(50) | S | Código do papel associado ao grupo; NULL se for usuário ou subgrupo. |  | FDN_ROLE.ROLE_CODE |
| `TENANT_ID` | bigint(20) | N | Tenant do grupo/membro; compõe a chave lógica junto com os códigos. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · jpa-join/confirmed — Usuário membro (FDNGroupUserRole.user); junção apenas por LOGIN.
- `(TENANT_ID, ROLE_CODE)` → **FDN_ROLE** `(TENANT_ID, ROLE_CODE)` · N:1 · jpa-join/confirmed — Papel associado ao grupo.
- `(TENANT_ID, CHILD_GROUPCODE)` → **FDN_GROUP** `(TENANT_ID, GROUP_CODE)` · N:1 · jpa-join/confirmed — Subgrupo membro.
- `(TENANT_ID, GROUP_CODE)` → **FDN_GROUP** `(TENANT_ID, GROUP_CODE)` · N:1 · physical-fk/confirmed — Grupo pai (FK física composta).
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.

**Dicas de consulta:** Junte sempre por (TENANT_ID, código). LOGIN é a ponte para FDN_USERTENANT.

## FDN_IDENTITYPARTNER

Parceiro de identidade/licenciamento do tenant: guarda credenciais de cliente, licença e quantidade de usuários licenciados.

**Ciclo de vida:** Criado no registro/ativação do tenant com o serviço de identidade; poucas linhas.

**Atenção:** Contém segredo (CLIENT_SECRET) e chave pública. Estado via enum IdentityPartnerState (ordinal).

**PK:** ID · **Unique:** (TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária. |  |  |
| `CLIENT_ID` | varchar(255) | S | Identificador de cliente (OAuth/identidade) do parceiro. |  |  |
| `CLIENT_SECRET` | varchar(255) | S | Segredo do cliente do parceiro de identidade (dado sensível). |  |  |
| `LAST_UPDATE` | bigint(20) | N | Timestamp da última atualização, em epoch (provavelmente milissegundos). |  |  |
| `LICENSE_ID` | varchar(255) | S | Identificador da licença associada ao tenant. |  |  |
| `LICENSED_USERS` | int(11) | N | Quantidade de usuários licenciados. |  |  |
| `PUBLIC_KEY` | varchar(255) | S | Chave pública do parceiro de identidade. |  |  |
| `QA` | bit(1) | N | Indica ambiente de QA/testes. | 1=QA; 0=produção |  |
| `STATE` | int(11) | N | Estado do parceiro, ordinal do enum IdentityPartnerState. | 0=TRIAL; 1=ACTIVE; 2=DEMO; 3=DOWN; 4=VIOLATED (ordem do enum; mapeamento ordinal presumido) |  |
| `TENANT_ID` | bigint(20) | N | Tenant do parceiro; FK física. |  | FDN_TENANT.TENANT_ID |
| `VALIDATION` | varchar(255) | S | Dado de validação da licença/parceiro (texto livre). |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.

**Dicas de consulta:** Contém CLIENT_SECRET e PUBLIC_KEY: dados sensíveis, não exponha.

## FDN_PERMISSION

Concessão de permissão sobre um recurso (FDN_RESOURCE) a um usuário, grupo ou papel.

**Ciclo de vida:** Linhas criadas ao conceder permissões na administração/painel de permissões; volume potencialmente alto.

**Atenção:** Beneficiário identificado por UM de LOGIN, GROUP_CODE ou ROLE_CODE (os outros NULL). PERMISSION é o nome da permissão (ex.: leitura/gravação) definida em FDN_RESOURCETYPEPERMISSION.

**PK:** PERMISSION_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PERMISSION_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DESCRIPTION` | varchar(255) | N | Descrição textual da concessão/permissão. |  |  |
| `GROUP_CODE` | varchar(50) | S | Código do grupo beneficiário; NULL se for usuário ou papel. |  | FDN_GROUP.GROUP_CODE |
| `LOGIN` | varchar(150) | S | Login do usuário beneficiário; NULL se for grupo ou papel. |  | FDN_USERTENANT.LOGIN |
| `PERMISSION` | varchar(150) | N | Nome/código da permissão concedida (até 150 chars), tipicamente de FDN_RESOURCETYPEPERMISSION.PERMISSION. |  | FDN_RESOURCETYPEPERMISSION.PERMISSION |
| `ROLE_CODE` | varchar(50) | S | Código do papel beneficiário; NULL se for usuário ou grupo. |  | FDN_ROLE.ROLE_CODE |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |
| `RESOURCE_ID` | bigint(20) | S | Recurso sobre o qual a permissão é concedida. |  | FDN_RESOURCE.RESOURCE_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · physical-fk/confirmed — Recurso protegido.
- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · logical-probable/probable — Usuário beneficiário, sem FK.
- `(TENANT_ID, GROUP_CODE)` → **FDN_GROUP** `(TENANT_ID, GROUP_CODE)` · N:1 · hql-join/confirmed — Grupo beneficiário (FDNGroup join FDNPermission em HQL).
- `(TENANT_ID, ROLE_CODE)` → **FDN_ROLE** `(TENANT_ID, ROLE_CODE)` · N:1 · logical-probable/probable — Papel beneficiário, sem FK.

**Dicas de consulta:** Para saber quem pode o quê: filtre por RESOURCE_ID e TENANT_ID e verifique qual das colunas LOGIN/GROUP_CODE/ROLE_CODE está preenchida.

## FDN_PERMISSION_MAPPING

Mapeamento entre permissões: ter PERMISSION em RESOURCE_CODE implica/concede TO_PERMISSION em TO_RESOURCE_CODE.

**Ciclo de vida:** Cadastrado por configuração/instalação; volume baixo.

**Atenção:** Referencia recursos por código (FDN_RESOURCE.RESOURCE_CODE), não por ID. O índice FDNPERMMAP001 sugere consulta pelo destino (TO_*). Semântica exata (herança de permissão) inferida.

**PK:** PERMISSION_MAPPING_ID · **Unique:** (TENANT_ID, RESOURCE_CODE, PERMISSION, TO_RESOURCE_CODE, TO_PERMISSION)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PERMISSION_MAPPING_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |
| `RESOURCE_CODE` | varchar(255) | N | Código do recurso de origem do mapeamento. |  | FDN_RESOURCE.RESOURCE_CODE |
| `PERMISSION` | varchar(60) | N | Permissão de origem no recurso de origem. |  | FDN_RESOURCETYPEPERMISSION.PERMISSION |
| `TO_RESOURCE_CODE` | varchar(255) | N | Código do recurso de destino ao qual a permissão é mapeada. |  | FDN_RESOURCE.RESOURCE_CODE |
| `TO_PERMISSION` | varchar(60) | N | Permissão equivalente concedida no recurso de destino. |  | FDN_RESOURCETYPEPERMISSION.PERMISSION |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_CODE)` → **FDN_RESOURCE** `(RESOURCE_CODE)` · N:1 · logical-probable/probable — Recurso de origem por código.
- `(TO_RESOURCE_CODE)` → **FDN_RESOURCE** `(RESOURCE_CODE)` · N:1 · logical-probable/probable — Recurso de destino por código.

**Dicas de consulta:** Sem FK; junte por código de recurso (e TENANT_ID quando aplicável).

## FDN_RESOURCE

Recurso protegido por permissão (tela, serviço, documento, método de API etc.), organizado em hierarquia e classificado por tipo.

**Ciclo de vida:** Registrado na instalação/deploy de módulos e dinamicamente para itens do usuário; volume médio a alto.

**Atenção:** Hierarquia por PARENT_ID. RESOURCE_CODE é a chave de negócio referenciada por código em FDN_PERMISSION_MAPPING. TENANT_ID NULL indica recurso global.

**PK:** RESOURCE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `RESOURCE_CODE` | varchar(255) | N | Código único do recurso protegido (até 255 chars). |  |  |
| `DESCRIPTION` | varchar(255) | S | Descrição curta do recurso. |  |  |
| `LONG_DESCRIPTION` | varchar(4000) | S | Descrição longa do recurso (até 4000 chars). |  |  |
| `INTERNAL` | bit(1) | N | Indica recurso interno do sistema. | 1=interno; 0=não interno |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |
| `PARENT_ID` | bigint(20) | S | Recurso pai na hierarquia; NULL para raiz. |  | FDN_RESOURCE.RESOURCE_ID |
| `RESOURCE_TYPE_ID` | bigint(20) | N | Tipo do recurso. |  | FDN_RESOURCETYPE.RESOURCE_TYPE_ID |
| `METHOD` | varchar(20) | S | Método HTTP (GET, POST etc.) quando o recurso representa endpoint de API; NULL caso contrário. |  |  |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_TYPE_ID)` → **FDN_RESOURCETYPE** `(RESOURCE_TYPE_ID)` · N:1 · jpa-join/confirmed — Tipo do recurso.
- `(PARENT_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · physical-fk/confirmed — Recurso pai (hierarquia).
- `(RESOURCE_ID)` → **FDN_PERMISSION** `(RESOURCE_ID)` · 1:N · physical-fk/confirmed — Permissões concedidas sobre o recurso.
- `(RESOURCE_ID)` → **FDN_RESTORE_PERMISSION_MAPPING** `(RESOURCE_ID)` · 1:N · physical-fk/confirmed — Backup de permissões do recurso.

**Dicas de consulta:** Percorra a árvore com PARENT_ID. Combine com FDN_PERMISSION por RESOURCE_ID.

## FDN_RESOURCETYPE

Tipos de recurso protegível (categorias de FDN_RESOURCE).

**Ciclo de vida:** Populada na instalação; poucas linhas.

**Atenção:** Define, via FDN_RESOURCETYPEPERMISSION, quais permissões existem para cada tipo.

**PK:** RESOURCE_TYPE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_TYPE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `RESOURCE_TYPE_CODE` | varchar(40) | N | Código do tipo de recurso (indexado). |  |  |
| `DESCRIPTION` | varchar(120) | N | Descrição do tipo de recurso. |  |  |
| `INTERNAL` | bit(1) | N | Indica tipo interno do sistema. | 1=interno; 0=não interno |  |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_TYPE_ID)` → **FDN_RESOURCE** `(RESOURCE_TYPE_ID)` · 1:N · jpa-join/confirmed — Recursos deste tipo.
- `(RESOURCE_TYPE_ID)` → **FDN_RESOURCETYPEPERMISSION** `(RESOURCE_TYPE_ID)` · 1:N · jpa-join/confirmed — Permissões válidas para o tipo.

**Dicas de consulta:** Tabela de domínio, sem tenant.

## FDN_RESOURCETYPEPERMISSION

Catálogo das permissões possíveis para cada tipo de recurso.

**Ciclo de vida:** Populada na instalação; poucas linhas.

**Atenção:** Única por tipo+permissão (unique key).

**PK:** RESOURCE_PERMISSION_ID · **Unique:** (PERMISSION, RESOURCE_TYPE_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `RESOURCE_PERMISSION_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DESCRIPTION` | varchar(60) | N | Descrição da permissão para exibição. |  |  |
| `PERMISSION` | varchar(60) | N | Nome/código da permissão (até 60 chars), ex.: ação permitida sobre o tipo. |  |  |
| `RESOURCE_TYPE_ID` | bigint(20) | N | Tipo de recurso ao qual a permissão se aplica. |  | FDN_RESOURCETYPE.RESOURCE_TYPE_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_TYPE_ID)` → **FDN_RESOURCETYPE** `(RESOURCE_TYPE_ID)` · N:1 · physical-fk/confirmed — Tipo de recurso.

**Dicas de consulta:** Tabela de domínio, sem tenant.

## FDN_RESTORE_PERMISSION_MAPPING

Backup em XML das permissões de um recurso, usado para restaurar permissões.

**Ciclo de vida:** Criada quando permissões de um recurso são salvas para restauração; volume baixo.

**Atenção:** Conteúdo em LOB (XML_PERMISSION).

**PK:** ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint | N | Chave primária. |  |  |
| `RESOURCE_ID` | bigint | N | Recurso cujas permissões foram salvas. |  | FDN_RESOURCE.RESOURCE_ID |
| `XML_PERMISSION` | longtext | S | XML serializado com as permissões do recurso a restaurar (longtext). |  |  |
| `TENANT_ID` | bigint | N | Tenant do recurso (sem FK declarada). |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(RESOURCE_ID)` → **FDN_RESOURCE** `(RESOURCE_ID)` · N:1 · physical-fk/confirmed — Recurso cujas permissões são restauradas.

**Dicas de consulta:** Evite selecionar XML_PERMISSION em varreduras (LOB).

## FDN_ROLE

Papel (role) de segurança do tenant, atribuído a usuários e grupos.

**Ciclo de vida:** Criado na administração de papéis ou internamente; volume baixo.

**Atenção:** Identificado logicamente por (TENANT_ID, ROLE_CODE), referenciado por código em FDN_USERROLE, FDN_GROUPUSERROLE e FDN_PERMISSION. Unique key provável em (TENANT_ID, ROLE_CODE).

**PK:** ROLE_ID · **Unique:** (TENANT_ID, ROLE_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ROLE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `ROLE_CODE` | varchar(50) | S | Código do papel, único por tenant. |  |  |
| `DESCRIPTION` | varchar(255) | S | Nome/descrição do papel. |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |
| `INTERNAL` | BIT(1) | S | Indica papel interno do sistema. | 1=interno; 0=não interno |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.
- `(TENANT_ID, ROLE_CODE)` → **FDN_USERROLE** `(TENANT_ID, ROLE_CODE)` · 1:N · jpa-join/confirmed — Usuários com este papel.

**Dicas de consulta:** Junte por (TENANT_ID, ROLE_CODE). Dados extras em FDN_ROLEDATA.

## FDN_ROLEDATA

Propriedades chave/valor adicionais de um papel (FDN_ROLE).

**Ciclo de vida:** Criadas junto com o papel; volume baixo.

**Atenção:** Padrão EAV.

**PK:** ROLEDATA_ID · **Unique:** (ROLEDATA_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ROLEDATA_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DATA_KEY` | varchar(255) | N | Nome da propriedade do papel. |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor textual da propriedade (até 4000). |  |  |
| `ROLE_ID` | bigint(20) | N | Papel dono da propriedade. |  | FDN_ROLE.ROLE_ID |

**Relacionamentos (saem desta tabela):**

- `(ROLE_ID)` → **FDN_ROLE** `(ROLE_ID)` · N:1 · physical-fk/confirmed — Papel dono da propriedade.

**Dicas de consulta:** Junte com FDN_ROLE via ROLE_ID.

## FDN_USER

Pessoa/usuário global do Fluig (dados pessoais independentes de tenant); o vínculo com cada tenant está em FDN_USERTENANT.

**Ciclo de vida:** Criado ao cadastrar usuário; pode ser anonimizado (LGPD).

**Atenção:** Um FDN_USER pode ter várias linhas em FDN_USERTENANT (uma por tenant). Para login/e-mail/estado use FDN_USERTENANT.

**PK:** USER_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USER_ID` | bigint(20) | N | Chave primária do usuário global. |  |  |
| `BIRTH_DATE` | datetime | S | Data de nascimento (dado pessoal). |  |  |
| `FIRST_NAME` | varchar(255) | S | Primeiro nome. |  |  |
| `FULL_NAME` | varchar(255) | S | Nome completo. |  |  |
| `LAST_NAME` | varchar(255) | S | Sobrenome. |  |  |
| `USER_TYPE` | int(11) | N | Tipo do usuário, enum FDNUserType (ordinal = código). | 0=NORMAL; 1=INTERNAL; 2=NOLOGIN; 3=APPLICATION |  |
| `ANONYMIZATION_DATE` | datetime | S | Data em que o usuário foi anonimizado (LGPD); NULL se não anonimizado. |  |  |
| `ANONYMIZATION_USER_ID` | bigint(20) | S | Usuário que executou a anonimização (auto-referência). |  | FDN_USER.USER_ID |

**Relacionamentos (saem desta tabela):**

- `(ANONYMIZATION_USER_ID)` → **FDN_USER** `(USER_ID)` · N:1 · physical-fk/confirmed — Usuário que anonimizou este registro.
- `(USER_ID)` → **FDN_USERTENANT** `(USER_ID)` · 1:N · jpa-join/confirmed — Vínculos do usuário com tenants.

**Dicas de consulta:** Dados pessoais: nome, data de nascimento. Respeite anonimização (ANONYMIZATION_DATE).

## FDN_USERDATA

Propriedades chave/valor adicionais do vínculo usuário-tenant (perfil e preferências).

**Ciclo de vida:** Criadas/atualizadas no cadastro e uso do perfil; volume alto.

**Atenção:** Padrão EAV; HIDE oculta valores. Referencia FDN_USERTENANT por USER_TENANT_ID. Suporta anonimização.

**PK:** USERDATA_ID · **Unique:** (USER_TENANT_ID, DATA_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERDATA_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DATA_KEY` | varchar(255) | N | Nome da propriedade do usuário (indexado). |  |  |
| `DATA_VALUE` | varchar(4000) | S | Valor da propriedade (até 4000 chars); pode conter dado pessoal. |  |  |
| `HIDE` | bit(1) | N | Indica valor oculto na interface. | 1=oculto; 0=visível |  |
| `USER_TENANT_ID` | bigint(20) | N | Vínculo usuário-tenant dono da propriedade. |  | FDN_USERTENANT.USER_TENANT_ID |
| `ANONYMIZATION_DATE` | datetime | S | Data da anonimização do dado. |  |  |
| `ANONYMIZATION_USER_ID` | bigint(20) | S | Vínculo usuário-tenant que executou a anonimização. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · jpa-join/confirmed — Dono da propriedade (FDNUserData.user).
- `(ANONYMIZATION_USER_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Quem anonimizou.

**Dicas de consulta:** Dados pessoais em DATA_VALUE. Filtre por DATA_KEY.

## FDN_USERLOGGING

Registro de usuário logado/sessão com data de vencimento (due date), por login e tenant.

**Ciclo de vida:** Linha criada no login e removida/expirada; volume proporcional a usuários ativos.

**Atenção:** Semântica exata inferida do nome e colunas; DUE_DATE em epoch.

**PK:** USERLOGGING_ID · **Unique:** (LOGIN); (TENANT_ID, LOGIN)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERLOGGING_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `DUE_DATE` | bigint(20) | N | Data/hora de expiração do registro, em epoch (provavelmente ms). |  |  |
| `LOGIN` | varchar(150) | N | Login do usuário (FDN_USERTENANT.LOGIN). |  | FDN_USERTENANT.LOGIN |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · physical-fk/confirmed — Usuário (FK por LOGIN).
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant, sem FK.

**Dicas de consulta:** Contém LOGIN (identificador do usuário).

## FDN_USERPICTURE

Foto/avatar do usuário (referência ao arquivo da imagem) por vínculo usuário-tenant.

**Ciclo de vida:** Criada/atualizada ao trocar a foto; uma por usuário-tenant.

**Atenção:** Guarda só o nome/caminho da imagem, não o binário.

**PK:** USERPICTURE_ID · **Unique:** (USER_TENANT_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERPICTURE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `PICTURE` | varchar(255) | S | Nome/caminho do arquivo da imagem do usuário. |  |  |
| `USER_TENANT_ID` | bigint(20) | N | Vínculo usuário-tenant dono da foto. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · 1:1 · physical-fk/confirmed — Usuário dono da foto.

## FDN_USERROLE

Atribuição de papéis (FDN_ROLE) a usuários por tenant.

**Ciclo de vida:** Criada ao atribuir papel ao usuário; volume proporcional a usuários x papéis.

**Atenção:** Referencia papel por (TENANT_ID, ROLE_CODE) e usuário por LOGIN.

**PK:** USERROLE_ID · **Unique:** (TENANT_ID, LOGIN, ROLE_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERROLE_ID` | bigint(20) | N | Chave primária surrogate. |  |  |
| `LOGIN` | varchar(150) | N | Login do usuário que possui o papel. |  | FDN_USERTENANT.LOGIN |
| `ROLE_CODE` | varchar(50) | N | Código do papel atribuído. |  | FDN_ROLE.ROLE_CODE |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dono do registro; FK para FDN_TENANT.TENANT_ID. Valor -1 indica registro global/sem tenant em consultas do código. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · jpa-join/confirmed — Usuário.
- `(TENANT_ID, ROLE_CODE)` → **FDN_ROLE** `(TENANT_ID, ROLE_CODE)` · N:1 · jpa-join/confirmed — Papel.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.

**Dicas de consulta:** Junte por LOGIN e (TENANT_ID, ROLE_CODE).

## FDN_USERTENANT

Vínculo do usuário (FDN_USER) com um tenant: contém login, e-mail, senha, estado e identificadores usados na autenticação.

**Ciclo de vida:** Criado ao cadastrar/convidar usuário no tenant; USER_STATE muda no ciclo de vida; volume = usuários do ambiente.

**Atenção:** Tabela central de usuário: LOGIN é usado como referência de usuário em muitas tabelas (FK por LOGIN). Contém e-mail e hash de senha.

**PK:** USER_TENANT_ID · **Unique:** (TENANT_ID, USER_ID); (LOGIN)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USER_TENANT_ID` | bigint(20) | N | Chave primária do vínculo usuário-tenant. |  |  |
| `EMAIL` | varchar(120) | N | E-mail do usuário (dado pessoal). |  |  |
| `FIRST_ACCESS` | bit(1) | N | Indica que o usuário ainda não fez o primeiro acesso (default true). | 1=primeiro acesso pendente; 0=já acessou |  |
| `IDP_ID` | varchar(255) | S | Identificador do usuário no provedor de identidade externo. |  |  |
| `LAST_UPDATE_DATE` | datetime | N | Data da última atualização do cadastro. |  |  |
| `LAST_SECURITY_UPDATE_DATE` | datetime | S | Data da última alteração de segurança (ex.: senha/permissões). |  |  |
| `LOCATION_ID` | bigint(20) | S | Identificador de localização/filial do usuário. |  |  |
| `LOGIN` | varchar(150) | N | Login do usuário no tenant; referência de usuário usada em permissões, papéis e grupos. |  |  |
| `PASSWORD` | varchar(512) | S | Hash/segredo da senha do usuário (até 512 chars; dado sensível). |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant do vínculo. |  | FDN_TENANT.TENANT_ID |
| `USER_CODE` | varchar(150) | S | Código/matrícula do usuário no tenant (distinto de LOGIN). |  |  |
| `USER_ID` | bigint(20) | N | Usuário global. |  | FDN_USER.USER_ID |
| `USER_STATE` | int(11) | N | Estado do usuário, ordinal do enum UserState. | 0=UNCONFIRMED; 1=ACTIVE; 2=BLOCKED; 3=REMOVED (ordem do enum; mapeamento ordinal) |  |
| `USER_UUID` | varchar(36) | S | UUID do usuário, gerado aleatoriamente na criação. |  |  |
| `ANONYMIZATION_DATE` | datetime | S | Data de anonimização (LGPD); NULL se não anonimizado. |  |  |
| `ANONYMIZATION_USER_ID` | bigint(20) | S | Vínculo usuário-tenant que executou a anonimização. |  | FDN_USERTENANT.USER_TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(USER_ID)` → **FDN_USER** `(USER_ID)` · N:1 · jpa-join/confirmed — Usuário global.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · jpa-join/confirmed — Tenant ao qual o registro pertence.
- `(ANONYMIZATION_USER_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · physical-fk/confirmed — Quem anonimizou.
- `(USER_TENANT_ID)` → **FDN_USERDATA** `(USER_TENANT_ID)` · 1:N · jpa-join/confirmed — Propriedades do usuário.

**Dicas de consulta:** Filtre sempre por TENANT_ID. Dados sensíveis: EMAIL, PASSWORD (hash), IDP_ID. Filtre USER_STATE=1 para ativos.
