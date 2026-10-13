# Working in fluig-sql-docs

This repository documents the Fluig 1.8.2 clean-install MySQL schema and provides SQL planning metadata. Read README.md, CONTRIBUTING.md and agent/README.md before changing the catalog.

## Sources and generated output

- Edit method_scripts/semantic_overrides.json for reviewed business grain and filters.
- Edit method_scripts/recipe_catalog.json for recipes, intents and expected warnings.
- Edit method_scripts/query_rules.json for planning policy.
- Edit method_scripts/catalog_overrides.json for reviewed base-catalog annotations; the full assembly pipeline applies these before writing schema and table cards.
- Treat agent/ files other than its README as generated output. Run python3 method_scripts/generate_agent.py and commit the generated changes.
- Keep schema.json and by_table/ cards consistent. Base-schema changes also affect domain documentation, the index and structural relationships.

## Evidence and validation

Preserve confidence, provenance, tenant keys, version keys and explicit unknowns. HQL reference queries are not executable SQL recipes. A documented relationship alone does not establish a grain-preserving join.

Use synthetic data. Do not include credentials, personal data, production dumps or product binaries.

Install method_scripts/requirements.txt in an isolated Python environment. Run method_scripts/check_catalog.py and python3 -m unittest discover -s tests -v for tool/catalog changes. Check documentation links and git diff --check for editorial changes. Add behavior regressions when modifying the parser or validator; do not add implementation-mirroring tests for simple wording edits.

The GitHub Actions configuration in method_scripts/github_actions.example.yml is a template. Activate it only when requested and when the publishing credential supports workflow changes.
