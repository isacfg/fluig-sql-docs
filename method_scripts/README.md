# Pipeline e fontes da camada de SQL

`generate_agent.py` funciona em um clone comum deste repositório, usando os arquivos versionados, sem conexão com banco:

```bash
python3 method_scripts/generate_agent.py
```

Fontes versionadas:

- `catalog_overrides.json`: anotações revisadas aplicadas pelo pipeline ao catálogo base.
- `semantic_overrides.json`: grain de negócio revisado, conceitos, filtros, datas preferidas e avisos. Cada regra referencia a ficha original; semânticas desconhecidas continuam explícitas.
- `recipe_catalog.json`: 28 recipes, SQL completo, intenção, parâmetros, grain, modo temporal, fontes e avisos esperados.
- `query_rules.json`: política do planner, incluindo verificações estáticas implementadas e recomendações manuais.

`validate_sql.py` e `check_catalog.py` requerem a versão de SQLGlot fixada em `requirements.txt`. O template `github_actions.example.yml` instala essa dependência, valida o catálogo, testa casos de erro e verifica que os artefatos gerados não mudam. Para ativá-lo, copie para `.github/workflows/validate.yml` usando uma credencial com escopo `workflow`; as mesmas verificações também podem ser executadas localmente.

## Pipeline completo com os intermediários locais

Os intermediários e os binários do Fluig não estão versionados. É preciso fornecer um diretório de trabalho contendo `ddl.json`, `entities.json` e `out/batch_*.json` para executar `merge.py` e `assemble.py`. `entities.json` pode ser reextraído por `parse_entities.py`; as descrições dos batches existentes continuam aproveitáveis.

```bash
# A partir da raiz do clone; substitua os caminhos pelos seus intermediários.
python3 method_scripts/parse_entities.py /caminho/mapeamentos-java /caminho/work/entities.json
# Execute os próximos comandos com cwd=/caminho/work:
python3 /caminho/clone/method_scripts/merge.py
python3 /caminho/clone/method_scripts/assemble.py /caminho/clone
```

A sequência original é `parse_ddl.py` → `parse_entities.py` → `merge.py` → `batches.py` → enriquecimento → `assemble.py`. `batches.py` fornece até 12 registros de queries completas por tabela ao enriquecimento; esse limite de contexto não limita o catálogo final.

A extração corrigida lê atributos em ordem variável, nomes literais e constantes resolvidas, texto sem truncamento (incluindo concatenação de literais) e `NamedNativeQuery` com `resultClass` antes de `query`. `merge.py` guarda `observed_queries` com linguagem e proveniência. `assemble.py` mantém o schema original e as correções de referências USER_CODE/LOGIN para FDN_USERTENANT, preserva as queries e gera automaticamente `agent/`. A extração ampliada acrescenta 29 relações HQL ao grafo original; o grafo de planejamento verifica completude e UNIQUE antes de promover joins.

As quatro queries de entidades não mapeadas ficam no intermediário `entities.json`, disponível após a extração. Queries observadas não são traduzidas automaticamente de HQL nem promovidas a recipes. A análise de filtros/joins dessas queries permanece marcada como não realizada.
