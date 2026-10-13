# Domínio: social-forms

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## FIELD

Campo de formulário analisado pela camada social/forms (controle de enquete/formulário social), com tipo, rótulo e obrigatoriedade. Pode ter campo pai (hierarquia).

**Ciclo de vida:** Gerada junto com SOCIALFORMCONTROL ao registrar formulário; FIELDREMOVED marca remoção lógica.

**Atenção:** Sem tenant. Auto-relacionada (FIELD_ID = pai). Colunas sem mapeamento Java direto (entidade em war social-public-api-web).

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | integer | N | Id do campo; PK. |  |  |
| `DATATYPE` | varchar(255) | S | Tipo de dado do campo do formulário (texto livre, ex.: tipo do campo). |  |  |
| `GOODDATAID` | integer | S | Id do dado/registro "bom" do campo; significado exato não confirmado. |  |  |
| `LABEL` | varchar(255) | S | Rótulo exibido do campo. |  |  |
| `MOBILE` | bit | S | Indica se o campo se aplica/exibe no mobile. | 1=sim; 0=não |  |
| `NAME` | varchar(255) | S | Nome técnico do campo no formulário. |  |  |
| `FIELDREMOVED` | bit | S | Remoção lógica do campo (Java removed). | 1=removido; 0=ativo |  |
| `REQUIRED` | bit | S | Indica campo obrigatório. | 1=obrigatório; 0=opcional |  |
| `WIDTH` | integer | S | Largura do campo (unidades de layout do formulário). |  |  |
| `FIELD_ID` | integer | S | Campo pai (auto-relação). |  | FIELD.ID |
| `SOCIALFORMCONTROLID` | bigint | S | Controle de formulário social ao qual o campo pertence. |  | SOCIALFORMCONTROL.ID |

**Relacionamentos (saem desta tabela):**

- `(FIELD_ID)` → **FIELD** `(ID)` · N:1 · physical-fk/confirmed — Campo pai (hierarquia de campos)
- `(SOCIALFORMCONTROLID)` → **SOCIALFORMCONTROL** `(ID)` · N:1 · physical-fk/confirmed — Controle de formulário que agrupa os campos

**Dicas de consulta:** Soft-delete via FIELDREMOVED. Chaves em minúsculas no PK/FK candidates; colunas reais são maiúsculas.

## SOCIALFORMCONTROL

Controle de formulário/enquete social vinculado a um documento do ECM, com hash e versão do formulário.

**Ciclo de vida:** Criado ao publicar formulário no social; MD5/VERSION controlam alterações.

**Atenção:** Unique DOCUMENTID. Sem TENANTID.

**PK:** id · **Unique:** (documentId)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do controle; PK. |  |  |
| `ALLOWEDTOSHOWPARCIALRESULTS` | bit | S | Permite exibir resultados parciais. | 1=sim; 0=não |  |
| `DOCUMENTID` | integer | N | Id do documento de formulário no ECM. |  | DOCUMENTO.NR_DOCUMENTO |
| `MD5` | varchar(255) | N | Hash MD5 da definição do formulário. |  |  |
| `QUANTITATIVE` | bit | S | Formulário quantitativo (resultados numéricos). | 1=sim; 0=não |  |
| `VERSION` | integer | S | Versão do formulário. |  |  |

**Relacionamentos (saem desta tabela):**

- `(DOCUMENTID)` → **DOCUMENTO** `(NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento de formulário do ECM; sem FK

**Dicas de consulta:** DOCUMENTID refere o documento de formulário do ECM (provável DOCUMENTO.NR_DOCUMENTO).

## SOCIALFORMEVENT

Regra de evento de formulário social (habilitar/exibir/validar campo conforme condição) por documento e atividade.

**Ciclo de vida:** Criada ao configurar regras do formulário.

**Atenção:** Multi-tenant (TENANTID). Relação com DETAIL via FORMEVENTID.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do evento; PK. |  |  |
| `ACTION` | varchar(255) | N | Ação do evento, enum FormActionType (texto). | DISABLE; DISAPPEAR; VALIDATE; DEFINE; ANALYTICS |  |
| `ACTIVITY` | integer | N | Atividade do processo à qual a regra se aplica. |  |  |
| `DOCUMENTID` | integer | N | Id do documento do formulário. |  | DOCUMENTO.NR_DOCUMENTO |
| `EXPRESSION` | varchar(255) | S | Expressão/script gerado da condição. |  |  |
| `FIELD` | varchar(255) | N | Nome do campo afetado. |  |  |
| `FIRSTACTIVITY` | bit | S | Aplica-se à primeira atividade. | 1=sim; 0=não |  |
| `LOGICALCONDITION` | varchar(255) | S | Operador lógico que combina condições. |  |  |
| `MESSAGE` | varchar(255) | S | Mensagem exibida (validação). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |

**Relacionamentos (saem desta tabela):**

- `(DOCUMENTID)` → **DOCUMENTO** `(NR_DOCUMENTO)` · N:1 · logical-probable/probable — Documento de formulário do ECM; sem FK

**Dicas de consulta:** Condição completa nas linhas de SOCIALFORMEVENTDETAIL.

## SOCIALFORMEVENTDETAIL

Condição individual (operação, tipo e valor) de um evento de formulário social.

**Ciclo de vida:** Criada junto com SOCIALFORMEVENT.

**Atenção:** Sem tenant.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do detalhe; PK. |  |  |
| `OPERATION` | varchar(255) | N | Operador de comparação, enum FormOperationType (texto). | EQUAL_TO(==); NOT_EQUAL(!=); GREATER_THEN(>); LESS_THEN(<); GREATER_THEN_OR_EQUAL_TO(>=); LESS_THEN_OR_EQUAL_TO(<=) |  |
| `TYPE` | varchar(255) | N | Tipo de valor comparado, enum FormValueType (texto). | EMPTY; EMAIL; (demais não listados) |  |
| `VALUE` | varchar(255) | S | Valor de comparação. |  |  |
| `FORMEVENTID` | bigint | S | Evento ao qual a condição pertence. |  | SOCIALFORMEVENT.ID |

**Relacionamentos (saem desta tabela):**

- `(FORMEVENTID)` → **SOCIALFORMEVENT** `(ID)` · N:1 · physical-fk/confirmed — Evento dono da condição
