# Domínio: seguranca

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_JAASUSERGROUP

Associação login-grupo JAAS usada pela camada de segurança do app server.

**Ciclo de vida:** Mantida na sincronização de usuários/papéis.

**Atenção:** Único por (LOGIN, GROUP_CODE). Sem TENANT_ID.

**PK:** JAAS_USERGROUP_ID · **Unique:** (LOGIN, GROUP_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `JAAS_USERGROUP_ID` | bigint(20) | N | Identificador surrogate da associação usuário-grupo JAAS (PK). |  |  |
| `GROUP_CODE` | varchar(50) | S | Código do grupo/papel de segurança JAAS ao qual o login pertence. |  | FDN_GROUP.GROUP_CODE |
| `LOGIN` | varchar(150) | N | Login do usuário associado ao grupo JAAS. |  | FDN_USERTENANT.LOGIN |

**Relacionamentos (saem desta tabela):**

- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · logical-probable/probable — Login do usuário (sem FK física). [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Named queries por login e por login+grupo. LOGIN é dado pessoal.

## FDN_REQUEST_NONCE

Nonces de requisições para prevenção de replay e rastreio de status/falha.

**Ciclo de vida:** Inserida a cada requisição protegida; antigas removidas por rotina (findNoncesToDelete usa CREATE_DATE).

**Atenção:** Multi-tenant por TENANT_ID; PK é o nonce string.

**PK:** REQUEST_NONCE_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `REQUEST_NONCE_ID` | VARCHAR(255) | N | Nonce da requisição (string única, PK) usado contra replay. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant da requisição. |  | FDN_TENANT.TENANT_ID |
| `CREATE_DATE` | DATE | N | Data de criação do nonce; usada para limpeza (findNoncesToDelete). |  |  |
| `REQUEST_STATUS` | VARCHAR(50) | N | Status do processamento da requisição associada ao nonce; valores não enumerados no código. |  |  |
| `FAILURE_DESCRIPTION` | longtext | S | Texto da falha quando a requisição falhou. |  |  |
| `USER_CODE` | varchar(150) | S | Código do usuário autenticado na requisição, se houver. |  | FDN_USERTENANT.USER_CODE |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · physical-fk/confirmed — Tenant da requisição.

**Dicas de consulta:** Alto volume transitório; índice (TENANT_ID, CREATE_DATE). USER_CODE é dado pessoal.

## FDN_USERTOKEN

Tokens temporários enviados por e-mail a usuários para liberar recursos (ex.: acesso por link), com limite de uso e status.

**Ciclo de vida:** Criado ao gerar o token; STATUS atualizado ao usar/expirar.

**Atenção:** Multi-tenant por TENANT_ID; TOKEN único.

**PK:** USERTOKEN_ID · **Unique:** (TOKEN)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERTOKEN_ID` | bigint(20) | N | Identificador do token de usuário (PK). |  |  |
| `CREATION_DATE` | datetime | N | Data/hora de criação do token. |  |  |
| `EMAIL` | varchar(255) | N | E-mail do destinatário ao qual o token foi enviado. DADO PESSOAL. |  |  |
| `EXPIRATION_DATE` | datetime | N | Data/hora de expiração do token. |  |  |
| `MAX_TOKEN` | int(11) | S | Número máximo de usos permitidos do token. |  |  |
| `STATUS` | int(11) | N | Status do token (enum UserTokenStatus, código inteiro). | 0=CREATED; 1=FAILED; 2=SUCCESS; 3=EXPIRED |  |
| `TENANT_ID` | bigint(20) | N | Tenant do token. |  | FDN_TENANT.TENANT_ID |
| `TOKEN` | varchar(255) | N | Valor do token (único, UK_FDNUSERTOKEN001). SENSÍVEL. |  |  |
| `USED_TOKEN` | int(11) | S | Quantidade de usos já realizados do token. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant do token.

**Dicas de consulta:** EMAIL e TOKEN são sensíveis. Filtrar STATUS/TENANT_ID.

## FDN_USERTOKENRESOURCE

Recursos (hoje apenas URLs) liberados por um token de usuário.

**Ciclo de vida:** Criada junto com o token.

**Atenção:** Único por (USERTOKEN_ID, RESOURCE_CODE).

**PK:** USERTOKENRESOURCE_ID · **Unique:** (USERTOKEN_ID, RESOURCE_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USERTOKENRESOURCE_ID` | bigint(20) | N | Identificador do recurso liberado pelo token (PK). |  |  |
| `RESOURCE_CODE` | varchar(255) | N | Código do recurso liberado (para tipo URL, a própria URL). |  |  |
| `RESOURCE_TYPE` | int(11) | N | Tipo do recurso (enum FDNTokenResourceType, código inteiro). | 0=URL |  |
| `USERTOKEN_ID` | bigint(20) | N | Token de usuário ao qual o recurso pertence. |  | FDN_USERTOKEN.USERTOKEN_ID |

**Relacionamentos (saem desta tabela):**

- `(USERTOKEN_ID)` → **FDN_USERTOKEN** `(USERTOKEN_ID)` · N:1 · jpa-join/confirmed — Token dono do recurso (FDNUserTokenResource.userToken).

**Dicas de consulta:** JOIN com FDN_USERTOKEN.
