# Referências e componentes de terceiros

## Fluig e TOTVS

Este é um catálogo comunitário independente sobre o banco de dados do Fluig. Os nomes Fluig e TOTVS são usados para identificar o produto documentado; não indicam afiliação, certificação ou endosso do fornecedor.

Os nomes de tabelas, colunas, entidades e queries identificam interfaces e estruturas do produto. Os registros em `observed_queries` preservam texto SQL/HQL e referências de origem para análise técnica. Essa proveniência não implica transferência de titularidade nem altera direitos aplicáveis a materiais de terceiros.

A [licença MIT](LICENSE) adotada pelo projeto se aplica às contribuições originais de seus autores. Ela não concede direitos adicionais sobre o produto Fluig, suas marcas ou outros materiais de terceiros. O repositório não distribui instaladores, JARs, credenciais ou dados de produção.

## Dependências das ferramentas

O validador utiliza [SQLGlot](https://github.com/tobymao/sqlglot), instalado separadamente pela versão fixada em `method_scripts/requirements.txt`. Consulte os avisos e a licença fornecidos pelo próprio projeto ao redistribuir essa dependência.

O template de CI referencia `actions/checkout` e `actions/setup-python`; esses componentes também são fornecidos separadamente e possuem suas próprias licenças.

## Contribuições

Preserve proveniência e avisos de atribuição. Ao propor um material novo, identifique sua origem e verifique se pode autorizar sua redistribuição. Não inclua conteúdo de terceiros sob a licença do projeto por mera ausência de um aviso no arquivo.
