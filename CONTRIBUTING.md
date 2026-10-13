# Como contribuir

Contribuições podem corrigir descrições, revisar grain, comprovar relações, documentar diferenças entre versões e adicionar recipes SQL.

## Antes de começar

Procure uma issue existente. Para uma mudança grande ou nova versão do catálogo, abra uma issue descrevendo o objetivo e o impacto nos consumidores atuais. Para uma correção pontual, pode abrir o pull request diretamente.

Use português nos guias e descrições de negócio, mantendo nomes de tabelas, colunas e campos JSON como estão. As convenções de uma recipe ou ficha existente são a referência para novos registros.

## Ambiente local

Requer Python 3.10 ou superior.

```bash
git clone https://github.com/SEU_USUARIO/fluig-sql-docs.git
cd fluig-sql-docs
python3 -m venv .venv
.venv/bin/python -m pip install -r method_scripts/requirements.txt
git switch -c sua-alteracao
```

## Onde editar

- **Grain, conceitos, filtros e datas preferidas:** `method_scripts/semantic_overrides.json`.
- **Recipes, intenções, parâmetros e avisos esperados:** `method_scripts/recipe_catalog.json`.
- **Regras de consulta:** `method_scripts/query_rules.json` e, quando necessário, `validate_sql.py`.
- **Anotações revisadas do catálogo base:** `method_scripts/catalog_overrides.json`. O pipeline completo aplica esses ajustes antes de gerar as fichas e os domínios.
- **Estrutura, tipos, chaves e relações:** `schema.json`, com evidência da versão e atualização consistente de `by_table/`, `domains/`, `index.md` e `relationships.md`. O pipeline completo pode reproduzir esses arquivos quando os intermediários estiverem disponíveis; veja `method_scripts/README.md`.

Os arquivos de `agent/`, exceto seu README, são gerados. Edite a fonte correspondente e execute `generate_agent.py`; inclua no PR os artefatos atualizados.

## Evidência e confiança

Informe a versão do Fluig, o banco utilizado e a evidência que sustenta a alteração: DDL mínimo, constraint, mapeamento de aplicação ou resultado de uma verificação reproduzível.

Não transforme relação `probable` em `confirmed` com base apenas na semelhança de nomes. Uma PK/UNIQUE comprova unicidade estrutural, mas não a existência de uma relação. Preserve avisos e valores desconhecidos quando não houver evidência suficiente.

Para uma recipe, informe intenção, grain do resultado, tabela raiz, parâmetros, modo temporal, fontes e avisos esperados. Inclua tenant em cada ramo relevante, versões completas nos joins e projeções explícitas. Não declare execução em banco real quando houve somente validação estática.

Use dados sintéticos em exemplos e testes. Não envie credenciais, dumps, dados pessoais, instaladores, JARs ou materiais cuja redistribuição você não possa autorizar.

## Verificações

```bash
python3 method_scripts/generate_agent.py
.venv/bin/python method_scripts/check_catalog.py
.venv/bin/python -m unittest discover -s tests -v
git diff --check
```

Para mudar o parser ou o validador, inclua regressões que mostrem o comportamento antes/depois. Para documentação simples, confira os links e a consistência com o catálogo.

## Pull requests

Descreva o problema, a alteração, a evidência e as verificações realizadas. Inclua o impacto em grain, tenant, versões ou compatibilidade quando pertinente. Evite alterações de formatação em massa nos JSONs; preserve o formato dos arquivos existentes.

Se um exemplo ainda depender de uma suposição, deixe-a registrada na ficha ou recipe e no PR. Os mantenedores podem pedir evidências adicionais ou restringir a mudança à versão comprovada.

## Licença das contribuições

Ao enviar código ou documentação original para este projeto, você concorda em disponibilizar sua contribuição sob a [licença MIT](LICENSE) e declara que pode conceder esses direitos. Materiais de terceiros devem manter suas atribuições e condições próprias; veja [THIRD_PARTY.md](THIRD_PARTY.md).

Preserve o aviso de copyright de Isaac Figueiredo (@isacfg) e o texto da licença em redistribuições do projeto. Autores de novas contribuições podem acrescentar seus próprios avisos sem remover os existentes; não é exigida cessão de direitos ao mantenedor.
