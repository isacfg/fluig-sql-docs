# Domínio: security-oauth-tokens

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## RESET_PASSWORD_TOKEN

Token de redefinição de senha ("esqueci minha senha") emitido para um usuário do tenant. Recebe linha quando o usuário solicita reset.

**Ciclo de vida:** Criada na solicitação de reset; consumida/expirada via CREATION_DATE. Volume baixo.

**Atenção:** Sem COD_EMPRESA; vínculo ao tenant é via USER_TENANT_ID (FDN_USERTENANT).

**PK:** TOKEN_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `TOKEN_ID` | BIGINT(20) | N | Id numérico (BIGINT) do token; chave primária. |  |  |
| `USER_TENANT_ID` | bigint(20) | N | Id do vínculo usuário/tenant que solicitou o reset. |  | FDN_USERTENANT.USER_TENANT_ID |
| `NEW_PASS_TOKEN` | varchar(36) | S | UUID (36 chars) enviado ao usuário para autorizar a definição de nova senha. Mapeado no campo Java f6token. |  |  |
| `CREATION_DATE` | DATETIME | S | Data/hora de emissão do token; base para verificar expiração. |  |  |

**Relacionamentos (saem desta tabela):**

- `(USER_TENANT_ID)` → **FDN_USERTENANT** `(USER_TENANT_ID)` · N:1 · logical-probable/probable — Usuário/tenant dono do token de reset (FK lógica; sem constraint física)

**Dicas de consulta:** Dado sensível: NEW_PASS_TOKEN permite redefinir a senha do usuário. Juntar com FDN_USERTENANT por USER_TENANT_ID.

## SESSAO_TOKEN

Tokens de sessão (UUID) associados a um login, com marca do último uso. Usada pela entidade Token do foundation/webdesk.

**Ciclo de vida:** Linhas criadas ao emitir token de sessão; VAL_ULT_USO atualizado a cada uso.

**Atenção:** Sem tenant nem FK; ligação ao usuário é só pelo texto LOGIN.

**PK:** COD_TOKEN

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_TOKEN` | varchar(40) | N | UUID (varchar 40) do token de sessão; PK. Campo Java uuid. |  |  |
| `VAL_ULT_USO` | bigint | S | Instante do último uso do token, provável epoch em milissegundos (Long lastTimeUsed). |  |  |
| `LOGIN` | varchar(50) | S | Login do usuário dono do token (texto). |  | FDN_USERTENANT.LOGIN |

**Relacionamentos (saem desta tabela):**

- `(LOGIN)` → **FDN_USERTENANT** `(LOGIN)` · N:1 · logical-probable/probable — Login do dono do token; sem FK [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Dado sensível: COD_TOKEN é credencial de sessão. LOGIN refere FDN_USERTENANT.LOGIN por valor.
