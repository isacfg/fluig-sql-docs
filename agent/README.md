# Planejar → montar → validar SQL

Esta camada contém fichas compactas das 333 tabelas, 28 recipes MySQL, intenções de negócio, aliases, joins direcionais e regras de validação. Leia apenas as fichas e queries observadas necessárias à pergunta.

## Protocolo do planner

1. Identifique a intenção em `intents.json`; procure sinônimos em `terminology.json`.
2. Defina o grain do resultado pedido: solicitação, atribuição de tarefa, movimentação, versão de documento, usuário do tenant ou valor de campo.
3. Escolha a tabela raiz que naturalmente possui esse grain. Localize a ficha em `index.json`.
4. Carregue `tables/<TABELA>.json` e, para tipos/colunas/chaves, `../by_table/<TABELA>.json`.
5. Escolha `canonical_joins`. Se precisar de filhos, examine `join_graph.json` e o efeito na quantidade de linhas. Use aliases diferentes em autojoins.
6. Aplique `required_filters` e os `canonical_filters` pertinentes à intenção. Passe parâmetros por binding do driver; não interpole valores.
7. Confira tenant, versões, datas e exclusão lógica em **cada alias**. Não use estado corrente para buscar a versão histórica registrada num anexo.
8. Confira multiplicação de linhas. Para contar solicitações, prefira a tabela raiz com `EXISTS` para tarefas. Para vários tenants, a identidade é `(COD_EMPRESA, NUM_PROCES)`; `COUNT(DISTINCT NUM_PROCES)` sozinho pode subcontar.
9. Consulte índices e escolha predicados compatíveis com seus prefixos. Confirme desempenho com `EXPLAIN` na instância.
10. Use uma recipe como ponto de partida e, quando útil, consulte `observed_queries/<TABELA>.json` para evidência de uso no Fluig.
11. Gere SQL no dialeto solicitado. As recipes usam MySQL e placeholders `:nome`; adapte o binding para o driver.
12. Valide tabelas, colunas, ambiguidades, tenant, joins completos, versão e grain com `query_rules.json` e `method_scripts/validate_sql.py`.
13. Declare relações `probable`, grain de negócio não revisado e demais suposições. Confirme o DDL real e, antes de usar em produção, resultados e plano no banco da instância.

## Contrato das fichas

- `grain.columns`: PK física do schema de instalação. `business_grain_reviewed=true` em 22 tabelas principais; as demais preservam finalidade e grain estrutural, sem inventar semântica de negócio. A única tabela sem PK declarada recebe aviso explícito.
- `tenant.column`: coluna local de tenant. Ausência da coluna não significa acesso global; determine a propriedade através das relações com tabelas de tenant. Consultas administrativas entre tenants precisam de escopo explícito.
- `required_filters`: restrições de escopo. `canonical_filters`: listas de predicados locais, separadas por intenção; não aplique todos simultaneamente. `closed` de PROCES_WORKFLOW é inatividade e não decodifica conclusão versus cancelamento.
- `canonical_joins`: candidatos completos que preservam o grain estrutural da origem; podem conter `confidence=probable` e `safe=false`. A intenção ainda pode exigir filtros temporais e escolher INNER ou LEFT JOIN.
- `safe=true`: relação confirmada, tenant alinhado e destino com PK/UNIQUE declarada nas colunas de igualdade. **Não** comprova autorização, existência de todas as linhas, qualidade dos dados ou semântica de um indicador de versão corrente. INNER JOIN pode eliminar linhas sem correspondente.
- `preserves_grain=true`: igualdade no máximo com uma linha de destino. `row_multiplication_risk=true`: destino não único e origem única; `null`: cardinalidade estrutural não resolvida. Ambos exigem conferência antes de agregar.
- `superseded_by`: arestas parciais mantidas como evidência, bloqueadas para escolha canônica. Nunca use só NUM_PROCES quando a relação completa inclui COD_EMPRESA.
- `tenant_policy_added=true`: igualdade de tenant com o mesmo nome foi acrescentada pela política do planner; não é evidência extraída da query original. Mapeamentos entre nomes diferentes dependem de relação documentada.
- `observed_queries_path`: evidência isolada das fichas compactas. Cada registro preserva nome, texto completo, entidade e caminho da fonte, `language` (`hql` ou `sql`) e tipo de extração. `tables` lista somente a tabela proprietária; `filters`/`joins` vazios e `analysis_status` dizem explicitamente que o texto ainda não foi analisado. HQL não é SQL executável. Queries observadas podem ter filtros inadequados para outra intenção.
- `deprecated_columns` e `preferred_columns`: em TAR_PROCES, usar DEADLINE/START_DATE/END_DATE em vez das seis colunas antigas de data/hora.

`FDN_USERTENANT` possui UNIQUE em LOGIN e em `(TENANT_ID, USER_ID)`, mas não em `(TENANT_ID, USER_CODE)`. A matrícula de uma tarefa não permite concluir unicidade por DDL. O grafo conserva esse join com aviso, sem promovê-lo a seguro. Grupos globais e memberships herdadas exigem análise além das recipes de vínculos diretos.

## Recipes e validação

`intents.json` liga pergunta → tabela raiz → tabelas → recipe, incluindo grain do resultado, parâmetros, fontes, modo temporal e avisos esperados. Há 11 recipes de workflow, 7 de GED, 5 de usuários e 5 de formulários. A recipe de anexos usa a versão registrada, não a versão corrente do documento; a de solicitações com tarefas usa EXISTS para evitar duplicação.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r method_scripts/requirements.txt
.venv/bin/python method_scripts/validate_sql.py agent/recipes/workflow/pending_tasks_by_user.sql
.venv/bin/python method_scripts/validate_sql.py agent/recipes/ecm/document_versions.sql --document-mode historical
.venv/bin/python method_scripts/check_catalog.py
.venv/bin/python -m unittest discover -s tests -v
```

Execute os comandos da raiz do repositório. O validador emite JSON e retorna 1 para erros; `--strict` retorna 1 também para avisos. Os modos `current`, `historical` e `unspecified` são explícitos: ele não tenta adivinhar a intenção lendo comentários. `check_catalog.py` usa o modo de cada recipe e exige exatamente seus avisos declarados.

O validador faz análise estática sobre a AST com SQLGlot: resolve nomes e ambiguidades, testa restrições de tenant garantidas em AND/OR, propaga tenant por igualdades e verifica chaves dos joins conhecidos. Detecta LOBs em projeções com wildcard, colunas deprecated e fanout. Não executa SQL nem comprova permissão do usuário. CTEs/tabelas derivadas e RIGHT/FULL JOIN recebem aviso para revisão manual de linhagem/tenant; joins não documentados ou sem igualdade garantida também recebem aviso. Não é um verificador completo de SQL nem estima desempenho. Dados e hotfixes da instância continuam sendo a referência final.

Há 1.218 queries observadas associadas a 224 tabelas. A extração completa encontra outras quatro em entidades sem tabela correspondente no DDL; elas permanecem no intermediário `entities.json`, sem ficha de tabela inventada.

## Regeneração

Os arquivos de `agent/`, exceto este README, são gerados por `method_scripts/generate_agent.py` a partir de `schema.json` e três fontes versionadas: `semantic_overrides.json`, `recipe_catalog.json` e `query_rules.json`. Edite essas fontes, não as fichas/recipes geradas.

```bash
python3 method_scripts/generate_agent.py
```

A geração usa somente a biblioteca padrão. Para refazer o pipeline completo, veja `method_scripts/README.md`. `assemble.py` gera a camada automaticamente; `merge.py` preserva as queries observadas antes de descartar o campo temporário usado para análise HQL.
