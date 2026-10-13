# Domínio: calendario-feriados

4 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## CALEND_GLOBAL

Feriados globais da empresa (entidade FDNHoliday). Cada linha é um feriado de um calendário identificado por COD_FER_CALEND, fixo (dia/mês) ou de um ano específico.

**Ciclo de vida:** Cadastrado manualmente por administradores; volume baixo (dezenas a centenas por empresa).

**Atenção:** Multi-tenant por COD_EMPRESA (e não TENANT_ID). Se NUM_ANO_FER é nulo, provavelmente o feriado se repete todo ano (não confirmado no código). FDN_LOCALHOLIDAY referencia esta tabela por (ID, COD_EMPRESA).

**PK:** ID · **Unique:** (ID, COD_EMPRESA); (COD_FER_CALEND)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária (surrogate) do feriado. |  |  |
| `COD_EMPRESA` | bigint(20) | N | Código da empresa/tenant dona do feriado; compõe a referência de FDN_LOCALHOLIDAY. |  | FDN_TENANT.TENANT_ID |
| `COD_FER_CALEND` | varchar(50) | N | Identificador textual (código/descrição) do feriado no calendário; usado em validateDescription para evitar duplicidade. |  |  |
| `NUM_DIA_FER` | int(11) | S | Dia do mês do feriado (1-31). |  |  |
| `NUM_MES_FER` | int(11) | S | Mês do feriado (1-12). |  |  |
| `NUM_ANO_FER` | int(11) | S | Ano do feriado; nulo provavelmente indica feriado recorrente anual. |  |  |

**Dicas de consulta:** Filtrar por COD_EMPRESA. Associação a locais via FDN_LOCALHOLIDAY (HOLIDAY_ID, COMPANY_ID) -> (ID, COD_EMPRESA).

## FDN_LOCAL

Locais (unidades/filiais) com coordenadas geográficas, raio e fuso horário, usados para associar feriados e usuários. Pode haver um local padrão por empresa.

**Ciclo de vida:** Cadastro administrativo; poucas linhas.

**Atenção:** Usa COMPANYID (não COD_EMPRESA/TENANT_ID). DEFAULT_LOCALE marca o local padrão.

**PK:** ID · **Unique:** (COMPANYID, NAME)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária do local. |  |  |
| `COMPANYID` | bigint(20) | N | Empresa/tenant dona do local. |  | FDN_TENANT.TENANT_ID |
| `DEFAULT_LOCALE` | bit(1) | S | Indica o local padrão da empresa. | 1=local padrão; 0/NULL=não |  |
| `LATITUDE` | double | S | Latitude em graus decimais. |  |  |
| `LONGITUDE` | double | S | Longitude em graus decimais. |  |  |
| `NAME` | varchar(255) | N | Nome do local. |  |  |
| `RADIUS` | double | S | Raio de abrangência em torno das coordenadas (unidade não confirmada, provável metros/km). |  |  |
| `TIMEZONE` | varchar(255) | S | Identificador de fuso horário (ex.: America/Sao_Paulo). |  |  |

**Relacionamentos (saem desta tabela):**

- `(ID)` → **FDN_LOCALHOLIDAY** `(LOCAL_ID)` · 1:N · physical-fk/confirmed — Feriados do local.
- `(ID)` → **FDN_LOCALUSER** `(LOCAL_ID)` · 1:N · physical-fk/confirmed — Usuários do local.
- `(ID)` → **FDN_SITE** `(LOCAL_ID)` · 1:N · physical-fk/confirmed — Sites de volume do local.

**Dicas de consulta:** Filtrar por COMPANYID.

## FDN_LOCALHOLIDAY

Associação entre local (FDN_LOCAL) e feriado global (CALEND_GLOBAL): feriados que valem para cada local.

**Ciclo de vida:** Criada ao vincular feriados a locais.

**Atenção:** Chave de feriado composta (HOLIDAY_ID, COMPANY_ID) = CALEND_GLOBAL (ID, COD_EMPRESA).

**PK:** ID · **Unique:** (LOCAL_ID, HOLIDAY_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária. |  |  |
| `HOLIDAY_ID` | bigint(20) | N | Feriado vinculado. |  | CALEND_GLOBAL.ID |
| `COMPANY_ID` | bigint(20) | N | Empresa do feriado; parte da chave composta do feriado. |  | CALEND_GLOBAL.COD_EMPRESA |
| `LOCAL_ID` | bigint(20) | N | Local ao qual o feriado se aplica. |  | FDN_LOCAL.ID |

**Relacionamentos (saem desta tabela):**

- `(LOCAL_ID)` → **FDN_LOCAL** `(ID)` · N:1 · physical-fk/confirmed — Local.
- `(HOLIDAY_ID, COMPANY_ID)` → **CALEND_GLOBAL** `(ID, COD_EMPRESA)` · N:1 · jpa-join/confirmed — Feriado global (join composto).

**Dicas de consulta:** Join com CALEND_GLOBAL deve usar as duas colunas.

## FDN_LOCALUSER

Associação de usuários a locais (FDN_LOCAL). Cada linha vincula um código de usuário a um local.

**Ciclo de vida:** Mantida pela administração de locais.

**Atenção:** USER_CODE é texto (login), sem FK.

**PK:** ID · **Unique:** (COMPANYID, USER_CODE)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `ID` | bigint(20) | N | Chave primária. |  |  |
| `COMPANYID` | bigint(20) | N | Empresa/tenant da associação. |  | FDN_TENANT.TENANT_ID |
| `USER_CODE` | varchar(255) | S | Código (login) do usuário associado ao local. |  | FDN_USERTENANT.USER_CODE |
| `LOCAL_ID` | bigint(20) | N | Local do usuário. |  | FDN_LOCAL.ID |

**Relacionamentos (saem desta tabela):**

- `(LOCAL_ID)` → **FDN_LOCAL** `(ID)` · N:1 · physical-fk/confirmed — Local.
- `(USER_CODE)` → **FDN_USERTENANT** `(USER_CODE)` · N:1 · logical-probable/probable — Usuário por login; sem FK. [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]

**Dicas de consulta:** Filtrar por COMPANYID; dado pessoal (login).
