# Domínio: bpm-cap

2 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## CONFIGUR_GRAF_COMPART

Compartilhamento de configurações de gráficos CAP (Controle e Acompanhamento de Processos) com usuários, grupos ou papéis.

**Ciclo de vida:** Uma linha por destinatário do compartilhamento de um gráfico.

**Atenção:** Toda a tabela é PK. NUM_SEQ_GRAF aponta para CONFIGUR_GRAF_USUAR_CAP.NUM_SEQ do dono (CD_MATRICULA).

**PK:** IDI_TIP_COMPART, CD_MATRICULA, COD_EMPRESA, NUM_SEQ_GRAF, DES_VAL_COMPART

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `IDI_TIP_COMPART` | integer | N | Tipo de destinatário do compartilhamento (attributionType); valores não confirmados no código. |  |  |
| 🔑 `CD_MATRICULA` | varchar(255) | N | Matrícula do dono do gráfico compartilhado. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ_GRAF` | integer | N | Sequência do gráfico do dono compartilhado. |  | CONFIGUR_GRAF_USUAR_CAP.NUM_SEQ |
| 🔑 `DES_VAL_COMPART` | varchar(255) | N | Identificador do destinatário (usuário, grupo ou papel) conforme IDI_TIP_COMPART. |  |  |

**Relacionamentos (saem desta tabela):**

- `(CD_MATRICULA, COD_EMPRESA, NUM_SEQ_GRAF)` → **CONFIGUR_GRAF_USUAR_CAP** `(CD_MATRICULA, COD_EMPRESA, NUM_SEQ)` · N:1 · logical-probable/probable — Gráfico compartilhado.

**Dicas de consulta:** Filtrar COD_EMPRESA.

## CONFIGUR_GRAF_USUAR_CAP

Configuração de gráficos do CAP (Controle e Acompanhamento de Processos) por usuário: quais métricas/séries exibir, processo analisado e frequência de snapshot.

**Ciclo de vida:** Uma linha por gráfico configurado pelo usuário; volume baixo.

**Atenção:** PK (CD_MATRICULA, COD_EMPRESA, NUM_SEQ). Muitas colunas LOG_* são flags de séries exibidas.

**PK:** CD_MATRICULA, COD_EMPRESA, NUM_SEQ

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `CD_MATRICULA` | varchar(255) | N | Matrícula do dono da configuração de gráfico. |  | FDN_USERTENANT.USER_CODE |
| 🔑 `COD_EMPRESA` | bigint | N | Tenant (empresa) dono da linha; sempre filtrar por este valor. |  | FDN_TENANT.TENANT_ID |
| 🔑 `NUM_SEQ` | integer | N | Sequência do gráfico para o usuário. |  |  |
| `LOG_PRAZ_PREVIS_CANCDO` | bit | S | Exibe prazo previsto (baseline) das tarefas canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_PREVIS_CANCDO` | bit | S | Exibe prazo médio previsto das tarefas canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_PREVIS_FINALIZ` | bit | S | Exibe prazo previsto das tarefas finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_PREVIS_FINALIZ` | bit | S | Exibe prazo médio previsto das tarefas finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_PREVIS_ABER` | bit | S | Exibe prazo previsto das tarefas abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_PREVIS_ABER` | bit | S | Exibe prazo médio previsto das tarefas abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_PREVIS_CANCDO` | bit | S | Exibe esforço previsto das tarefas canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_PREVIS_CANCDO` | bit | S | Exibe esforço médio previsto das tarefas canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_PREVIS_FINALIZ` | bit | S | Exibe esforço previsto das tarefas finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_PREVIS_FINAL` | bit | S | Exibe esforço médio previsto das tarefas finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_PREVIS_ABER` | bit | S | Exibe esforço previsto das tarefas abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_PREVIS_ABER` | bit | S | Exibe esforço médio previsto das tarefas abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_CANCDO` | bit | S | Exibe série de tarefas/instâncias canceladas. | 1=exibe/inclui; 0=não |  |
| `IDI_TIP_APRES` | integer | S | Tipo de apresentação do gráfico (chartType); valores não confirmados. |  |  |
| `COD_MATR_ESCOLHID` | varchar(255) | S | Matrícula do usuário escolhido como filtro do gráfico (choosedColleagueId). |  | FDN_USERTENANT.USER_CODE |
| `LOG_FINALIZ` | bit | S | Exibe série de finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_FINALIZ_PRAZ` | bit | S | Exibe finalizadas dentro do prazo. | 1=exibe/inclui; 0=não |  |
| `LOG_FINALIZ_ATRASO` | bit | S | Exibe finalizadas com atraso. | 1=exibe/inclui; 0=não |  |
| `DES_PRINC_GRAF` | varchar(255) | S | Título/descrição principal do gráfico. |  |  |
| `LOG_INVERTE_CATEG` | bit | S | Inverte categorias/séries do gráfico. | 1=exibe/inclui; 0=não |  |
| `LOG_MEDIA_MENSAL_FINALIZ` | bit | S | Exibe média mensal de finalizações. | 1=exibe/inclui; 0=não |  |
| `LOG_MEDIA_ABER` | bit | S | Exibe média mensal de aberturas. | 1=exibe/inclui; 0=não |  |
| `LOG_ABER_PRAZ` | bit | S | Exibe abertas dentro do prazo. | 1=exibe/inclui; 0=não |  |
| `LOG_ABER_ATRASO` | bit | S | Exibe abertas em atraso. | 1=exibe/inclui; 0=não |  |
| `LOG_ABER` | bit | S | Exibe série de abertas (opened). | 1=exibe/inclui; 0=não |  |
| `LOG_ABERT` | bit | S | Exibe série de aberturas (openings). | 1=exibe/inclui; 0=não |  |
| `NUM_ORDER_VIEW` | integer | S | Ordem de exibição do gráfico no painel. |  |  |
| `CD_MATRICULA_COMPART` | varchar(255) | S | Matrícula do dono original quando o gráfico é compartilhado (ownerColleagueId). |  | FDN_USERTENANT.USER_CODE |
| `NUM_SEQ_COMPART` | integer | S | Sequência do gráfico original do dono (ownerSequence). |  | CONFIGUR_GRAF_USUAR_CAP.NUM_SEQ |
| `LOG_PREVIS_ATRASO` | bit | S | Exibe previstas em atraso. | 1=exibe/inclui; 0=não |  |
| `COD_DEF_PROCES` | varchar(255) | S | Código da definição de processo analisada no gráfico. |  | DEF_PROCES.COD_DEF_PROCES |
| `NUM_SEQ_ESTADO` | integer | S | Sequência do estado/atividade do processo analisado. |  | ESTADO_PROCES.NUM_SEQ |
| `NUM_VERS` | integer | S | Versão da definição de processo analisada. |  | VERS_DEF_PROCES.NUM_VERS |
| `LOG_PRAZ_REAL_CANCDO` | bit | S | Exibe prazo real das canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_REAL_CANCDO` | bit | S | Exibe prazo médio real das canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_REAL_FINALIZ` | bit | S | Exibe prazo real das finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_REAL_FINALIZ` | bit | S | Exibe prazo médio real das finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_REAL_ABER` | bit | S | Exibe prazo real das abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_PRAZ_MEDIO_REAL_ABER` | bit | S | Exibe prazo médio real das abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_REAL_CANCDO` | bit | S | Exibe esforço real das canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_REAL_CANCDO` | bit | S | Exibe esforço médio real das canceladas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_REAL_FINALIZ` | bit | S | Exibe esforço real das finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_REAL_FINALIZ` | bit | S | Exibe esforço médio real das finalizadas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_REAL_ABER` | bit | S | Exibe esforço real das abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_ESFOR_MEDIO_REAL_ABER` | bit | S | Exibe esforço médio real das abertas. | 1=exibe/inclui; 0=não |  |
| `LOG_COMPART` | bit | S | Gráfico compartilhado com outros (ver CONFIGUR_GRAF_COMPART). | 1=exibe/inclui; 0=não |  |
| `LOG_MOSTRA_LEGENDA` | bit | S | Exibe legenda do gráfico. | 1=exibe/inclui; 0=não |  |
| `LOG_MOSTRA_NULO` | bit | S | Exibe valores nulos/zerados. | 1=exibe/inclui; 0=não |  |
| `IDI_FREQ_SNAPSHOT` | integer | S | Frequência do snapshot dos dados do gráfico. | 0=nunca; 1=diária; 2=semanal; 3=mensal; 4=anual |  |
| `NUM_REG_VISUALIZ` | integer | N | Quantidade de snapshots/registros exibidos no gráfico. |  |  |
| `IDI_TIP_GRAF` | integer | S | Tipo do gráfico CAP (type); valores não confirmados. |  |  |

**Relacionamentos (saem desta tabela):**

- `(CD_MATRICULA, COD_EMPRESA, NUM_SEQ)` → **CONFIGUR_GRAF_COMPART** `(CD_MATRICULA, COD_EMPRESA, NUM_SEQ_GRAF)` · 1:N · logical-probable/probable — Compartilhamentos do gráfico.
- `(COD_EMPRESA, COD_DEF_PROCES)` → **DEF_PROCES** `(COD_EMPRESA, COD_DEF_PROCES)` · N:1 · logical-probable/probable — Processo analisado (relação lógica não listada).

**Dicas de consulta:** Colunas LOG_* são bit; semântica deduzida dos nomes Java, sem verificação de uso na UI.
