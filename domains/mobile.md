# Domínio: mobile

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_USERMOBILETOKEN

Tokens de acesso/refresh do app mobile por usuário do IdP.

**Ciclo de vida:** Upsert por usuário ao autenticar no mobile.

**Atenção:** Sem TENANT_ID; COMPANY_ID é string do IdP.

**PK:** USER_IDIDP

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `USER_IDIDP` | varchar(255) | N | Id do usuário no IdP (provedor de identidade); PK. |  | FDN_USERTENANT.USER_IDIDP |
| `ACCESSTOKEN` | varchar(255) | N | Access token do app mobile para o usuário. SENSÍVEL. |  |  |
| `COMPANY_ID` | varchar(255) | N | Identificador da empresa/tenant no IdP (string). |  |  |
| `EXPIRESIN` | bigint(20) | N | Validade do token em segundos (OAuth expires_in). |  |  |
| `ISSUEDTIME` | bigint(20) | N | Instante de emissão do token, ms desde epoch (provável). |  |  |
| `REFRESHTOKEN` | varchar(255) | N | Refresh token do app mobile. SENSÍVEL. |  |  |

**Dicas de consulta:** ACCESSTOKEN e REFRESHTOKEN são sensíveis.
