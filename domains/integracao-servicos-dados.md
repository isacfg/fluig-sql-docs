# Domínio: integracao-servicos-dados

1 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## SERV_DADOS

Cadastro de serviços de dados (data services) externos usados por datasets e integrações: SOAP, Progress, REST e JDBC, com URL e credenciais.

**Ciclo de vida:** Criada/editada pelo administrador em Serviços; poucas linhas por empresa.

**Atenção:** Contém credenciais (COD_USUAR_AUTENTIC, COD_SENHA_AUTENTIC). Entidade DataService (módulo foundation-dataservice).

**PK:** COD_EMPRESA, NOM_SERV_DADOS

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `COD_EMPRESA` | bigint | N | Identificador da empresa/tenant (companyId); parte da PK. Filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NOM_SERV_DADOS` | varchar(50) | N | Nome único do serviço de dados dentro da empresa; é o identificador usado por datasets e scripts. |  |  |
| `CLB_BINDING` | longtext | S | Definição/binding serializada do serviço (ex.: WSDL ou descritor), até ~100000 caracteres. |  |  |
| `COD_TIPO_SEGTO` | integer | S | Tipo de segurança de autenticação do serviço (ex.: WS-Security); código numérico. |  |  |
| `DES_SERV_DADOS` | varchar(255) | S | Descrição livre do serviço de dados. |  |  |
| `IDI_TIP_SERV` | integer | N | Tipo do serviço de dados conforme enum DataServiceEnum. | 1=SOAP; 2=PROGRESS; 3=REST; 4=JDBC |  |
| `NOM_URL_SERV` | varchar(255) | N | URL de endpoint ou connection string do serviço. |  |  |
| `DRIVER` | varchar(255) | S | Driver JDBC (DatabaseDriver) usado quando o tipo é JDBC. |  |  |
| `DSL_PARAM_EXTRA` | varchar(500) | S | Parâmetros extras de conexão/chamada (até 500 caracteres). |  |  |
| `LOG_EXPIRATION_TIME` | bigint | S | Tempo de retenção/expiração, em milissegundos, do log de requisições do serviço. |  |  |
| `LOG_REQUEST_ACTIVE` | bit | S | Indica se o log de requisições ao serviço está ativo. | 1=log ativo; 0=inativo |  |
| `OAUTH_ID` | bigint | S | Identificador da configuração OAuth associada ao serviço. |  |  |
| `COD_AMBIEN_PROGRESS` | varchar(255) | S | Ambiente/biblioteca Progress (progressLibId) usado em serviços do tipo Progress. |  |  |
| `DES_OBJ_REMOTO` | varchar(255) | S | Objeto remoto (nome do programa/objeto) invocado em serviços Progress. |  |  |
| `COD_USUAR_AUTENTIC` | varchar(255) | S | Usuário de autenticação no serviço externo. |  |  |
| `COD_SENHA_AUTENTIC` | varchar(255) | S | Senha de autenticação no serviço externo (armazenada, possivelmente criptografada). |  |  |
| `WS_ENGINE` | integer | S | Engine/stack SOAP usada para gerar o cliente do web service (código numérico). |  |  |
| `WS_PACKAGE` | varchar(255) | S | Pacote Java usado para as classes geradas do web service. |  |  |
| `WSS_XML_CONFIG` | varchar(255) | S | Configuração XML WS-Security do serviço. |  |  |
| `SOAP_AUTHENTICATION_TYPE` | varchar(255) | S | Tipo de autenticação SOAP, conforme enum SOAPAuthenticationType. | none=sem autenticação; basic=HTTP Basic |  |

**Dicas de consulta:** Dado sensível: COD_USUAR_AUTENTIC e COD_SENHA_AUTENTIC (credenciais). Nunca expor. Referenciado por nome em datasets/serviços. Named queries: findAll, find, findByType.
