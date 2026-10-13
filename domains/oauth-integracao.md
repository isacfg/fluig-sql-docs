# Domínio: oauth-integracao

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_AUTHORIZECLIENTDATA

Configuração de cliente de autenticação/autorização para consumir serviços externos (credenciais, URLs e tokens OAuth), por tenant e código.

**Ciclo de vida:** Criada ao cadastrar um serviço de integração; tokens atualizados em renovações.

**Atenção:** Multi-tenant por TENANT_ID; CODE identifica o serviço.

**PK:** AUTHORIZECLIENTDATA_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `AUTHORIZECLIENTDATA_ID` | bigint(20) | N | Identificador surrogate da configuração de cliente OAuth/serviço externo (PK). |  |  |
| `ACCESS_TOKEN` | varchar(2000) | S | Access token corrente obtido do provedor externo. SENSÍVEL. |  |  |
| `ACCESS_TOKEN_URL` | varchar(255) | S | URL do endpoint do provedor para obter o access token. |  |  |
| `AUTHENTICATION_TYPE` | varchar(255) | N | Tipo de autenticação do serviço externo (ex.: OAuth 1.0/2.0, basic). |  |  |
| `AUTHORIZATION_URL` | varchar(255) | S | URL do endpoint de autorização do provedor. |  |  |
| `CLIENT_ID` | varchar(255) | S | Client id OAuth 2 registrado no provedor externo. |  |  |
| `CODE` | varchar(120) | N | Código/nome lógico do serviço (chave de busca, ex.: findByServiceName); único por tenant. |  |  |
| `CONSUMER_KEY` | varchar(255) | S | Consumer key OAuth 1.0 do provedor externo. |  |  |
| `CONSUMER_SECRET` | varchar(1023) | S | Consumer secret OAuth 1.0. SENSÍVEL. |  |  |
| `CUSTOM` | varchar(1023) | S | Parâmetros customizados adicionais do serviço (texto livre, provavelmente serializado). |  |  |
| `DOMAIN` | varchar(255) | N | Domínio/host associado ao serviço externo. |  |  |
| `GRAND_TYPE` | varchar(255) | S | Grant type OAuth 2 (grafia "GRAND" do DDL; ex.: authorization_code, password). |  |  |
| `PASSWORD` | varchar(255) | S | Senha usada em autenticação básica/password grant. SENSÍVEL. |  |  |
| `REDIRECT_URI` | varchar(255) | S | URI de redirecionamento (callback) OAuth. |  |  |
| `REFRESH_TOKEN` | varchar(2000) | S | Refresh token OAuth 2. SENSÍVEL. |  |  |
| `REFRESH_TOKEN_URL` | varchar(255) | S | URL do endpoint para renovar o token. |  |  |
| `REQUEST_TOKEN_URL` | varchar(255) | S | URL do endpoint de request token (OAuth 1.0). |  |  |
| `SCOPE` | varchar(255) | S | Escopos OAuth solicitados. |  |  |
| `SECRET_TOKEN` | varchar(255) | S | Token secret OAuth 1.0. SENSÍVEL. |  |  |
| `SERVICE_TEST_URL` | varchar(255) | S | URL usada para testar a conexão com o serviço. |  |  |
| `SERVICE_URL` | varchar(255) | S | URL base do serviço externo consumido. |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant (empresa) dono da configuração. |  | FDN_TENANT.TENANT_ID |
| `USERNAME` | varchar(255) | S | Usuário para autenticação básica/password grant. |  |  |

**Relacionamentos (saem desta tabela):**

- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant dono.

**Dicas de consulta:** Contém credenciais e tokens (CONSUMER_SECRET, PASSWORD, ACCESS_TOKEN, REFRESH_TOKEN, SECRET_TOKEN): sensível, nunca expor. Filtrar TENANT_ID.
