# fluig-sql-docs

[Licença MIT](LICENSE) · [Como contribuir](CONTRIBUTING.md) · [Histórico](CHANGELOG.md)

Catálogo comunitário do banco de dados do **Fluig 1.8.2**, com documentação por tabela e uma camada de planejamento de SQL para agentes de IA.

**333 tabelas · 2.809 colunas · 28 recipes SQL · 1.218 queries de referência**

O projeto ajuda desenvolvedores, analistas e agentes a localizar dados, escolher o grain do resultado, montar joins completos e validar consultas antes de usá-las em uma instância. É um projeto independente, sem vínculo oficial com a TOTVS.

## Comece aqui

- **Consultar o schema:** abra o [índice de tabelas](index.md) e carregue a ficha em [`by_table/`](by_table/).
- **Gerar SQL com um agente:** siga o [protocolo de planejamento](agent/README.md), começando por [`agent/intents.json`](agent/intents.json).
- **Adaptar uma consulta:** escolha um dos [exemplos SQL](agent/recipes/) e confira seus parâmetros, grain e suposições.
- **Contribuir:** leia [CONTRIBUTING.md](CONTRIBUTING.md).

## Instalação e uso

A documentação e os arquivos JSON podem ser lidos diretamente, sem instalar dependências. Os scripts de geração e validação usam Python 3.10 ou superior; os testes foram executados com Python 3.14, e o template de CI usa Python 3.12.

```bash
git clone https://github.com/isacfg/fluig-sql-docs.git
cd fluig-sql-docs
python3 -m venv .venv
.venv/bin/python -m pip install -r method_scripts/requirements.txt
```

Valide uma recipe de tarefas pendentes:

```bash
.venv/bin/python method_scripts/validate_sql.py \
  agent/recipes/workflow/pending_tasks_by_user.sql
```

Para consultar versões históricas, declare a intenção temporal:

```bash
.venv/bin/python method_scripts/validate_sql.py \
  agent/recipes/ecm/document_versions.sql --document-mode historical
```

O validador retorna JSON. Erros produzem código de saída `1`; `--strict` também trata avisos como falha. A validação é estática: ela não conecta ao banco nem executa SQL.

As recipes usam MySQL e parâmetros nomeados como `:tenant_id` e `:user_code`. Adapte o binding ao seu driver e passe valores como parâmetros. Oracle e SQL Server exigem conferir o dialeto e o schema da instância.

## Um exemplo: solicitações sem duplicação

Para listar solicitações com tarefas pendentes de um usuário, use a solicitação como raiz e `EXISTS` para testar tarefas. Isso preserva uma linha por `(COD_EMPRESA, NUM_PROCES)` mesmo quando existem várias tarefas para a mesma solicitação.

```sql
SELECT p.COD_EMPRESA, p.NUM_PROCES, p.COD_DEF_PROCES
FROM PROCES_WORKFLOW AS p
WHERE p.COD_EMPRESA = :tenant_id
  AND p.LOG_ATIV = 1
  AND EXISTS (
    SELECT 1
    FROM TAR_PROCES AS t
    WHERE t.COD_EMPRESA = p.COD_EMPRESA
      AND t.NUM_PROCES = p.NUM_PROCES
      AND t.CD_MATRICULA = :user_code
      AND t.LOG_ATIV = 1
      AND t.IDI_STATUS IN (0, 1)
  );
```

A [recipe completa](agent/recipes/workflow/processes_with_pending_tasks.sql) inclui metadados e ordenação. Veja o [protocolo do agente](agent/README.md) para escolher joins, versões e filtros.

## Conteúdo do repositório

| Caminho | Conteúdo |
| --- | --- |
| [`index.md`](index.md) | Tabela → domínio, PK e finalidade |
| [`by_table/`](by_table/) | Fichas completas de cada tabela: tipos, colunas, chaves, índices e relações |
| [`domains/`](domains/) | Documentação agrupada por domínio funcional |
| [`relationships.md`](relationships.md) | Relações estruturais e diagramas ER |
| [`schema.json`](schema.json) | Catálogo completo para consumo por máquina |
| [`agent/index.json`](agent/index.json) | Índice das 333 fichas compactas para agentes |
| [`agent/intents.json`](agent/intents.json) | Intenção de negócio → tabelas → recipe |
| [`agent/tables/`](agent/tables/) | Grain, tenant, filtros, joins canônicos e riscos |
| [`agent/join_graph.json`](agent/join_graph.json) | Grafo direcional com completude de chaves e efeito sobre o grain |
| [`agent/query_rules.json`](agent/query_rules.json) | Regras de planejamento e validação |
| [`agent/terminology.json`](agent/terminology.json) | Conceitos e sinônimos de negócio |
| [`agent/recipes/`](agent/recipes/) | 28 consultas: workflow, GED, usuários e formulários |
| [`agent/observed_queries/`](agent/observed_queries/) | Queries SQL/HQL de referência, com linguagem e proveniência |
| [`method_scripts/`](method_scripts/) | Fontes editáveis, geração, validação e template de CI |
| [`tests/`](tests/) | Regressões do parser, do validador e das recipes |

Para economizar contexto, carregue primeiro a intenção e as fichas pertinentes. Consulte o `schema.json` completo apenas quando necessário.

## Conceitos importantes

- **Grain:** a unidade representada por uma linha. Solicitação, atribuição de tarefa, movimentação e versão de documento são unidades diferentes.
- **Tenant:** delimite `COD_EMPRESA` nas tabelas legadas e `TENANT_ID` nas tabelas de plataforma. Consulte a ficha para outros identificadores de escopo.
- **Documentos:** `DOCUMENTO` guarda versões. Para estado corrente, use `VERSAO_ATIVA = 1 AND LOG_DELETE = 0`; anexos históricos podem exigir uma versão específica.
- **Usuários:** `FDN_USER` representa a pessoa global; `FDN_USERTENANT` guarda seu vínculo com tenant, login e matrícula. `(TENANT_ID, USER_CODE)` não possui UNIQUE declarado neste catálogo.
- **Joins:** um relacionamento documentado pode estar incompleto ou multiplicar linhas. Confira `canonical`, `superseded_by`, `confidence` e `preserves_grain` antes de usá-lo.
- **HQL:** queries de referência com `language = "hql"` usam entidades e propriedades Java; precisam de tradução antes de execução como SQL.

## Cobertura e limites

A referência estrutural usa o DDL MySQL de instalação do Fluig 1.8.2 e mapeamentos JPA. Chaves físicas, relações de aplicação e relações lógicas possuem classificação e confiança explícitas.

- As 333 tabelas têm grain estrutural documentado; o grain de negócio foi revisado nas 22 tabelas principais. Uma tabela não tem PK declarada e recebe aviso específico.
- Há 707 colunas sem correspondência com campo JPA e 136 colunas com confiança baixa. Valores de enum desconhecidos ficam vazios.
- As 28 recipes passaram nas verificações estáticas. Duas mantêm avisos documentados de relação provável; nenhuma foi executada em uma instância real do Fluig.
- Migrações e hotfixes não foram reaplicados ao catálogo. Tipos e colunas podem diferir no banco de uma instalação.
- Tabelas dinâmicas de formulários (`ml...`) e datasets internos estão fora do mapa.
- O validador sinaliza casos que precisam de revisão manual, como linhagem de CTEs e certos outer joins. Não estima desempenho nem comprova autorização.

Confira sempre os resultados e o plano de execução na instância que será consultada. Este repositório contém documentação e ferramentas; não distribui instaladores, JARs ou dados de produção do Fluig.

## Desenvolvimento

```bash
# Regenerar a camada agent/ a partir do catálogo versionado
python3 method_scripts/generate_agent.py

# Validar todas as fichas e recipes
.venv/bin/python method_scripts/check_catalog.py

# Executar a suíte de regressão
.venv/bin/python -m unittest discover -s tests -v
```

Os detalhes do pipeline e as fontes editáveis estão em [`method_scripts/README.md`](method_scripts/README.md). A configuração de GitHub Actions está disponível como [`template`](method_scripts/github_actions.example.yml).

## Comunidade

Correções de relações, novos exemplos e evidências de versões são bem-vindos. Use as [issues](https://github.com/isacfg/fluig-sql-docs/issues) para discutir alterações e abra um pull request seguindo o [guia de contribuição](CONTRIBUTING.md).

A convivência segue o [Código de Conduta](CODE_OF_CONDUCT.md). Para questões de segurança, consulte [SECURITY.md](SECURITY.md). Consulte também [CHANGELOG.md](CHANGELOG.md) para acompanhar a evolução do catálogo e [THIRD_PARTY.md](THIRD_PARTY.md) para referências de terceiros.

## Licença

As contribuições originais de código e documentação deste projeto são disponibilizadas sob a [licença MIT](LICENSE). Referências e materiais de terceiros mantêm seus próprios direitos e avisos; veja [THIRD_PARTY.md](THIRD_PARTY.md).
