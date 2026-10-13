# Mapa do schema do banco — TOTVS Fluig 1.8.2

Referência para agentes de IA: 333 tabelas, 2809 colunas, finalidade de cada tabela/coluna, chaves, índices e relacionamentos.

## Gerar SQL com agentes

Comece em [`agent/README.md`](agent/README.md): o protocolo agora é **planejar → montar → validar**. [`agent/index.json`](agent/index.json) localiza as 333 fichas com grain e escopo; [`agent/intents.json`](agent/intents.json) liga perguntas de negócio a 28 recipes SQL; [`agent/join_graph.json`](agent/join_graph.json) informa chaves completas, confiança e risco de multiplicação; [`agent/query_rules.json`](agent/query_rules.json) fornece as regras do planner.

As fichas estruturam filtros de tenant, filtros por intenção, joins canônicos, colunas deprecated e exemplos. O grain estrutural cobre todas as tabelas; o grain de negócio foi revisado nas 22 principais. Há também 1.218 Named Queries/HQL preservadas com proveniência em `schema.json`, nas fichas originais e em `agent/observed_queries/`, carregadas separadamente das fichas compactas.

O validador em [`method_scripts/validate_sql.py`](method_scripts/validate_sql.py) confere nomes, tenant, joins, versões e riscos de duplicação. As recipes passaram na validação estática; duas possuem avisos documentados de relação provável. Não foram executadas em uma instância real do Fluig. Veja [`method_scripts/README.md`](method_scripts/README.md) para regeneração e testes.

## Como consumir o schema (ordem sugerida)
1. `index.md` — uma linha por tabela (domínio, PK, finalidade). Comece aqui para localizar tabelas.
2. `domains/<dominio>.md` — tabelas do domínio com colunas (tipo, null, finalidade, valores de enum/flag, referências) e relações.
3. `by_table/<TABELA>.json` — ficha completa de UMA tabela (mais barato em contexto que o schema inteiro).
4. `relationships.md` — lista plana de arestas + diagramas Mermaid ER por domínio.
5. `schema.json` — tudo em um arquivo (máquina).

| Arquivo de domínio | Tabelas |
|---|---|
| `domains/acesso-recente.md` | 1 |
| `domains/assinatura-digital.md` | 1 |
| `domains/audit.md` | 2 |
| `domains/bpm-analytics-dw.md` | 10 |
| `domains/bpm-cap.md` | 2 |
| `domains/bpm-definicao-processo.md` | 2 |
| `domains/bpm-forms.md` | 2 |
| `domains/bpm-integracao.md` | 3 |
| `domains/bpm-process-definition.md` | 3 |
| `domains/bpm-tarefas.md` | 7 |
| `domains/bpm-workflow.md` | 56 |
| `domains/bpm-workflow-erro.md` | 1 |
| `domains/calendario-feriados.md` | 4 |
| `domains/concorrencia-lock.md` | 1 |
| `domains/configuracao-parametros.md` | 1 |
| `domains/datasets.md` | 1 |
| `domains/document-management.md` | 1 |
| `domains/ecm-collaboration.md` | 3 |
| `domains/ecm-documentos.md` | 3 |
| `domains/ecm-documents.md` | 26 |
| `domains/ecm-forms.md` | 3 |
| `domains/ecm-lists-filters.md` | 14 |
| `domains/ecm-metadata-forms.md` | 29 |
| `domains/ecm-search.md` | 3 |
| `domains/foundation-alert.md` | 9 |
| `domains/foundation-dataservice.md` | 1 |
| `domains/foundation-identity-access.md` | 18 |
| `domains/foundation-licenciamento.md` | 1 |
| `domains/foundation-platform.md` | 4 |
| `domains/foundation-tenancy.md` | 4 |
| `domains/ged-documentos.md` | 2 |
| `domains/i18n.md` | 6 |
| `domains/infraestrutura-sequencias.md` | 1 |
| `domains/infraestrutura-servidor.md` | 1 |
| `domains/integracao-datasets.md` | 1 |
| `domains/integracao-eventos.md` | 3 |
| `domains/integracao-servicos-dados.md` | 1 |
| `domains/integracao-servidores.md` | 1 |
| `domains/mail.md` | 1 |
| `domains/mobile.md` | 1 |
| `domains/mobile-push.md` | 1 |
| `domains/monitoring-metrics.md` | 3 |
| `domains/notificacao-email.md` | 1 |
| `domains/oauth-integracao.md` | 1 |
| `domains/oauth-provider.md` | 5 |
| `domains/permissoes-categorias.md` | 2 |
| `domains/privacy-lgpd.md` | 6 |
| `domains/rating.md` | 1 |
| `domains/scheduler-quartz.md` | 12 |
| `domains/security-audit.md` | 1 |
| `domains/security-oauth-tokens.md` | 2 |
| `domains/seguranca.md` | 4 |
| `domains/seguranca-api.md` | 1 |
| `domains/seguranca-auditoria.md` | 1 |
| `domains/social.md` | 21 |
| `domains/social-forms.md` | 4 |
| `domains/use-policy.md` | 5 |
| `domains/volumes-sites.md` | 3 |
| `domains/wcm-portal.md` | 16 |
| `domains/wcm-portal-apps.md` | 1 |
| `domains/wcm-portal-pages.md` | 2 |
| `domains/wcm-resources.md` | 4 |
| `domains/wcm-store.md` | 1 |
| `domains/wcm-theme.md` | 1 |

## Convenções do Fluig (úteis para montar queries)
- **Multi-tenant:** `COD_EMPRESA` (tabelas ECM/BPM legadas) e `TENANT_ID` (tabelas FDN_/WCM_) identificam o tenant e quase sempre fazem parte da PK. Filtre sempre.
- **Prefixos:** `FDN_*` foundation (usuários, papéis, permissões, OAuth, alertas, LGPD); `WCM_*` portal/páginas/widgets/temas; `ECM_*` formulários de metadados e colaboração; `QRTZ_*` Quartz; nomes em português abreviado (`DEF_PROCES`, `PROCES_WORKFLOW`, `DOCUMENTO`, `TAR_*`, `HISTOR_*`) = workflow (BPM) e gestão de documentos (GED).
- **Prefixos de coluna (legado):** `COD_`=código, `NUM_`/`NR_`=número, `DES_`/`DSL_`=descrição/texto, `IDI_`=indicador inteiro (enum), `LOG_`=booleano, `CD_MATRICULA`/`COD_MATR_*`=código (matrícula) do usuário, `DAT_`/`DT_`=data.
- **Usuários:** `FDN_USER` é a pessoa global; `FDN_USERTENANT` é o vínculo com o tenant e guarda `USER_CODE`/`LOGIN`. Colunas de "matrícula" nas tabelas legadas referenciam `FDN_USERTENANT.USER_CODE` (+ tenant), não `FDN_USER`.
- **Tabelas dinâmicas fora deste mapa:** cada formulário/ficha publicado cria tabelas próprias em runtime (`ml<empresa><n>...`), e datasets internos não são tabelas. Não constam no DDL de instalação.

## Como foi gerado e limites (leia antes de confiar cegamente)
- **Estrutura (tabelas, colunas, tipos, PK, índices, FKs físicas):** extraída dos scripts `createtable/mysql` dos jars `*-fluig-database-*` do Fluig 1.8.2. É o schema de instalação limpa; alterações dos `Update*Tables_*` (migrações em código) não foram reaplicadas. Variantes Oracle/SQL Server podem diferir em tipos.
- **Mapeamento Java:** entidades JPA decompiladas (jadx) cruzadas por nome de coluna (`java_field`/`java_type` em cada coluna; 707 colunas sem entidade correspondente).
- **Relacionamentos:** o banco tem poucas FKs físicas. `kind`: `physical-fk` (DDL), `jpa-join`/`hql-join` (código), `table-per-class-subtype`, `logical-*` (inferidas por nome de coluna e validadas/rejeitadas por agente lendo o código). `status`: `confirmed` ou `probable`. Relações inferidas e rejeitadas ficam em `rejected_relationships` na ficha da tabela.
- **Finalidade/valores de colunas:** redigidas por agentes de IA a partir do código decompilado; `confidence=low` em 136 colunas. Valores de enum só aparecem quando confirmados no código — vazio ≠ inexistente.
- Para dados reais, confirme no banco da instância (versões/hotfixes podem ter colunas extras).
