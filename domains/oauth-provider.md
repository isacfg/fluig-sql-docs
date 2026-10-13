# Domínio: oauth-provider

5 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_OAUTHAPP

Aplicação (consumidor) OAuth registrada no Fluig, com consumer key/secret e provedor.

**Ciclo de vida:** Criada ao registrar app OAuth; poucas linhas.

**Atenção:** CONSUMER_KEY único globalmente.

**PK:** OAUTH_APP_ID · **Unique:** (CONSUMER_KEY)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OAUTH_APP_ID` | bigint(20) | N | Identificador da aplicação OAuth registrada (consumidor) (PK). |  |  |
| `CALLBACK_URL` | varchar(1023) | S | URL de callback da aplicação OAuth. |  |  |
| `CONSUMER_KEY` | varchar(255) | N | Consumer key da aplicação; único globalmente (UK). |  |  |
| `CONSUMER_SECRET` | varchar(1023) | N | Consumer secret da aplicação. SENSÍVEL. |  |  |
| `DEFAULT_APP` | bit(1) | N | Indica se é a aplicação OAuth padrão do provedor. |  |  |
| `DESCRIPTION` | varchar(120) | N | Descrição/nome amigável da aplicação OAuth. |  |  |
| `OAUTH_PROVIDER_ID` | bigint(20) | N | Provedor OAuth ao qual a aplicação pertence (FK física). |  | FDN_OAUTHPROVIDER.OAUTH_PROVIDER_ID |

**Relacionamentos (saem desta tabela):**

- `(OAUTH_PROVIDER_ID)` → **FDN_OAUTHPROVIDER** `(OAUTH_PROVIDER_ID)` · N:1 · physical-fk/confirmed — Provedor da aplicação (JPA FDNOAuthApplication.provider).

**Dicas de consulta:** CONSUMER_SECRET é sensível.

## FDN_OAUTHAPPDATA

Propriedades extras chave/valor de uma aplicação OAuth.

**Ciclo de vida:** Criada junto com configuração da aplicação.

**PK:** OAUTH_APP_DATA_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OAUTH_APP_DATA_ID` | bigint(20) | N | Identificador do par propriedade/valor da aplicação (PK). |  |  |
| `PROPERTY` | varchar(255) | N | Nome da propriedade extra da aplicação OAuth (chave). |  |  |
| `VALUE` | varchar(255) | N | Valor da propriedade extra. |  |  |
| `OAUTH_APP_ID` | bigint(20) | N | Aplicação OAuth dona da propriedade (FK física). |  | FDN_OAUTHAPP.OAUTH_APP_ID |

**Relacionamentos (saem desta tabela):**

- `(OAUTH_APP_ID)` → **FDN_OAUTHAPP** `(OAUTH_APP_ID)` · N:1 · physical-fk/confirmed — Propriedades extras da aplicação.

**Dicas de consulta:** JOIN por OAUTH_APP_ID.

## FDN_OAUTHAPPTOKEN

Tokens OAuth (request/access) emitidos para uma aplicação OAuth, com data de criação e expiração.

**Ciclo de vida:** Criada nas etapas do fluxo OAuth; expiradas devem ser limpas.

**PK:** OAUTH_APP_TOKEN_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OAUTH_APP_TOKEN_ID` | bigint(20) | N | Identificador do token emitido para a aplicação (PK). |  |  |
| `CLIENT_DATA` | varchar(1023) | S | Dados adicionais do cliente associados ao token (texto livre). |  |  |
| `CREATION_DATE` | datetime | N | Data/hora de emissão do token. |  |  |
| `EXPIRATION_DATE` | datetime | N | Data/hora de expiração do token. |  |  |
| `TOKEN` | varchar(255) | S | Valor do token (request/authorize/access token conforme OAUTH_TYPE). SENSÍVEL. |  |  |
| `TOKEN_ACCESS` | varchar(1023) | S | Access token propriamente dito, após autorização. SENSÍVEL. |  |  |
| `TOKEN_SECRET` | varchar(1023) | S | Token secret OAuth 1.0 pareado ao token. SENSÍVEL. |  |  |
| `OAUTH_TYPE` | varchar(255) | S | Fase/tipo do token OAuth (ex.: request vs access); valores exatos não confirmados. |  |  |
| `OAUTH_APP_ID` | bigint(20) | N | Aplicação OAuth a que o token pertence (FK física). |  | FDN_OAUTHAPP.OAUTH_APP_ID |

**Relacionamentos (saem desta tabela):**

- `(OAUTH_APP_ID)` → **FDN_OAUTHAPP** `(OAUTH_APP_ID)` · N:1 · physical-fk/confirmed — Tokens emitidos para a aplicação.

**Dicas de consulta:** TOKEN, TOKEN_ACCESS e TOKEN_SECRET são sensíveis.

## FDN_OAUTHAPPUSER

Autorização de um usuário (login) a uma aplicação OAuth, ligando ao token emitido.

**Ciclo de vida:** Criada quando o usuário autoriza a aplicação.

**PK:** OAUTH_APP_USER_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OAUTH_APP_USER_ID` | bigint(20) | N | Identificador da autorização usuário-aplicação (PK). |  |  |
| `LOGIN` | varchar(255) | N | Login do usuário que autorizou a aplicação OAuth. |  | FDN_USERTENANT.LOGIN |
| `OAUTH_APP_ID` | bigint(20) | N | Aplicação OAuth autorizada pelo usuário. |  | FDN_OAUTHAPP.OAUTH_APP_ID |
| `OAUTH_APP_TOKEN_ID` | bigint(20) | N | Token emitido nesta autorização (FK física). |  | FDN_OAUTHAPPTOKEN.OAUTH_APP_TOKEN_ID |

**Relacionamentos (saem desta tabela):**

- `(OAUTH_APP_TOKEN_ID)` → **FDN_OAUTHAPPTOKEN** `(OAUTH_APP_TOKEN_ID)` · N:1 · physical-fk/confirmed — Token emitido nesta autorização.
- `(OAUTH_APP_ID)` → **FDN_OAUTHAPP** `(OAUTH_APP_ID)` · N:1 · jpa-join/confirmed — Aplicação autorizada (FDNOAuthApplicationUser.application).
- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · logical-probable/probable — Usuário que autorizou, por login. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** JOIN com FDN_OAUTHAPPTOKEN e FDN_OAUTHAPP; LOGIN é dado pessoal.

## FDN_OAUTHPROVIDER

Provedor OAuth (URLs de request/access/autorização e método de assinatura), por tenant.

**Ciclo de vida:** Criada ao cadastrar provedor.

**Atenção:** TENANT_ID nulo pode indicar provedor global. CODE único.

**PK:** OAUTH_PROVIDER_ID · **Unique:** (CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `OAUTH_PROVIDER_ID` | bigint(20) | N | Identificador do provedor OAuth (PK). |  |  |
| `ACCESS_TOKEN_URL` | varchar(255) | S | URL do endpoint de access token do provedor. |  |  |
| `CODE` | varchar(120) | N | Código único do provedor (UK global). |  |  |
| `DESCRIPTION` | varchar(120) | N | Descrição do provedor; único por tenant junto com TENANT_ID (índice FDNOAUTHPROVI003). |  |  |
| `OAUTH_PROVIDER_NAME` | varchar(255) | N | Nome do provedor OAuth. |  |  |
| `REQUEST_METHOD` | varchar(6) | N | Método HTTP usado nas requisições de token (ex.: GET/POST). |  |  |
| `REQUEST_TOKEN_URL` | varchar(255) | S | URL do endpoint de request token. |  |  |
| `SIGNATURE_METHOD` | varchar(40) | S | Método de assinatura OAuth 1.0 (ex.: HMAC-SHA1). |  |  |
| `TENANT_ID` | bigint(20) | S | Tenant dono do provedor; nulo = provedor global/padrão do sistema. |  | FDN_TENANT.TENANT_ID |
| `USER_AUTHORIZATION_URL` | varchar(255) | S | URL onde o usuário autoriza o acesso. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant dono (nulo = global).

**Dicas de consulta:** Filtrar por TENANT_ID ou NULL.
