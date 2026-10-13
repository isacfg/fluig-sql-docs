# Domínio: mobile-push

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FDN_PUSH

Registros de dispositivos móveis para notificações push: tokens de acesso, de canal e de dispositivo por usuário OAuth/aplicativo.

**Ciclo de vida:** Criada no registro do dispositivo e atualizada em renovações de token; volume proporcional a dispositivos.

**Atenção:** Contém tokens e IMEI (sensíveis). PUSH_SERVICE e PUSH_APP são enums gravados como string.

**PK:** PUSH_ID

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `PUSH_ID` | bigint(20) | N | Chave primária. |  |  |
| `ACCESS_TOKEN` | varchar(255) | N | Token de acesso OAuth associado ao dispositivo (sensível). |  |  |
| `IMEI` | varchar(255) | S | IMEI/identificador do dispositivo (dado pessoal). |  |  |
| `CHANNEL_TOKEN` | varchar(255) | S | Token do canal de push no provedor (sensível). |  |  |
| `MOBILE_LANGUAGE` | varchar(5) | S | Idioma do dispositivo (ex.: pt_BR, até 5 caracteres). |  |  |
| `MOBILE_TOKEN` | varchar(255) | N | Token do dispositivo móvel para envio de push (sensível). |  |  |
| `PUSH_STATUS` | varchar(255) | N | Status do registro de push, em texto livre (valores não confirmados). |  |  |
| `TENANT_ID` | bigint(20) | N | Tenant do registro. |  | FDN_TENANT.TENANT_ID |
| `TOKEN_CREATION_DATE` | date | S | Data de criação do token. |  |  |
| `TOKEN_LAST_UPDATE_DATE` | date | S | Data da última atualização do token. |  |  |
| `FDN_OAUTH_APPLICATION_USER_ID` | bigint(20) | N | Vínculo usuário-aplicativo OAuth dono do dispositivo. |  | FDN_OAUTHAPPUSER.OAUTH_APP_USER_ID |
| `PUSH_SERVICE` | varchar(13) | S | Serviço de push usado. | URBAN_AIRSHIP; FIREBASE |  |
| `PUSH_APP` | varchar(15) | S | Aplicativo móvel de destino. | MY_FLUIG; MY_APPROVAL |  |

**Relacionamentos (saem desta tabela):**

- `(FDN_OAUTH_APPLICATION_USER_ID)` → **FDN_OAUTHAPPUSER** `(OAUTH_APP_USER_ID)` · N:1 · physical-fk/confirmed — Usuário/aplicativo OAuth dono.
- `(TENANT_ID)` → **FDN_TENANT** `(TENANT_ID)` · N:1 · logical-probable/probable — Tenant, sem FK.

**Dicas de consulta:** Nunca expor tokens e IMEI.
