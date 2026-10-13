"""Deterministic, conservative SQL planning layer; stdlib-only generation."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TENANT_COLUMNS = ('COD_EMPRESA', 'TENANT_ID', 'COMPANY_ID')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def tenant_column(table):
    cols = {c['name'] for c in table['columns']}
    return next((c for c in TENANT_COLUMNS if c in cols), None)


def unique_keys(table):
    keys = [table['primary_key']] + table['unique_constraints']
    keys += [i['columns'] for i in table['indexes'] if i['unique']]
    # SQL nullable UNIQUE keys are not sufficient for arbitrary equality joins
    # with null-safe operators; our canonical joins use ordinary equality.
    return [set(k) for k in keys if k]


def is_unique(table, columns):
    return any(k <= set(columns) for k in unique_keys(table))


def build_graph(tables):
    graph = []
    seen = set()
    for name, table in sorted(tables.items()):
        for r in table['relationships']:
            target = r['to_table'].upper()
            fc, tc = list(map(str.upper, r['from_cols'])), list(map(str.upper, r['to_cols']))
            if target not in tables or not fc or len(fc) != len(tc):
                continue
            dest = tables[target]
            if not set(fc) <= {c['name'] for c in table['columns']} or not set(tc) <= {c['name'] for c in dest['columns']}:
                continue
            pairs = list(zip(fc, tc))
            st, dt = tenant_column(table), tenant_column(dest)
            supplemented = False
            if st and dt and (st, dt) not in pairs:
                # Same-named tenant columns only: cross-name equality needs
                # explicit source evidence (e.g. ECM_METADATA_FORM -> DOCUMENTO).
                if st == dt:
                    pairs.insert(0, (st, dt)); supplemented = True
            tenant_ok = not (st and dt) or (st, dt) in pairs
            identity = (name, target, tuple(sorted(pairs)))
            if identity in seen:
                continue
            seen.add(identity)
            full_target = is_unique(dest, [b for _, b in pairs])
            full_source = is_unique(table, [a for a, _ in pairs])
            for reverse in (False, True):
                source, to = (target, name) if reverse else (name, target)
                directed = [(b, a) for a, b in pairs] if reverse else pairs
                unique_to = full_source if reverse else full_target
                unique_from = full_target if reverse else full_source
                card = ('1:1' if unique_from else 'N:1') if unique_to else ('1:N' if unique_from else 'N:unknown')
                risk = False if unique_to else (True if unique_from else None)
                warnings = []
                if not tenant_ok: warnings.append('Tenant mapping is incomplete; supply verified tenant mapping before use.')
                if not unique_to: warnings.append('Destination equality columns are not a declared unique key; rows may multiply.')
                if r.get('status') != 'confirmed': warnings.append('Relationship is probable; disclose this assumption and verify on the instance.')
                if supplemented: warnings.append('Same-name tenant equality added by planning policy; not copied from the original relationship.')
                edge = dict(id=f'join-{len(graph)+1:04d}', from_table=source, to_table=to,
                    on=[f'{source}.{a} = {to}.{b}' for a, b in directed],
                    column_pairs=[dict(from_column=a, to_column=b) for a, b in directed],
                    cardinality=card, observed_cardinality=r['cardinality'],
                    confidence=r.get('status', 'probable'), source_kind=r['kind'],
                    evidence=r.get('description', ''), direction='reverse' if reverse else 'forward',
                    tenant_complete=tenant_ok, tenant_policy_added=supplemented,
                    destination_unique=unique_to, safe=unique_to and tenant_ok and r.get('status') == 'confirmed',
                    preserves_grain=unique_to and tenant_ok,
                    row_multiplication_risk=risk, aggregation_warning=not unique_to,
                    warnings=warnings)
                graph.append(edge)
    # Keep partial observations in the graph, but explicitly block selecting a
    # strict subset when a more complete edge exists for this pair.
    for edge in graph:
        pairs = {(p['from_column'], p['to_column']) for p in edge['column_pairs']}
        edge['superseded_by'] = [other['id'] for other in graph
            if other['from_table'] == edge['from_table'] and other['to_table'] == edge['to_table']
            and pairs < {(p['from_column'], p['to_column']) for p in other['column_pairs']}]
        edge['canonical'] = edge['preserves_grain'] and not edge['superseded_by']
        if edge['superseded_by']:
            edge['safe'] = False; edge['canonical'] = False
            edge['warnings'].append('Partial join: use the complete edge listed in superseded_by.')
    return graph


def generate(root):
    root = Path(root)
    schema = read(root / 'schema.json')
    tables = schema['tables']
    overrides = read(HERE / 'semantic_overrides.json')
    catalog = read(HERE / 'recipe_catalog.json')
    graph = build_graph(tables)
    cards = {}
    for name, table in sorted(tables.items()):
        o = overrides.get(name, {})
        tenant = tenant_column(table)
        grain = dict(description=o.get('grain_description', f"{table['purpose']} Stored-row grain follows the declared primary key; business grain needs review."),
            columns=table['primary_key'], basis='declared-primary-key',
            confidence='reviewed-schema-description' if 'grain_description' in o else 'structural-only',
            business_grain_reviewed='grain_description' in o)
        required = [dict(column=tenant, operator='=', parameter='tenant_id', reason='tenant isolation',
            exceptions='Cross-tenant administration requires an explicit, authorized scope.')] if tenant else []
        scoped_joins = [e for e in graph if e['from_table'] == name and e['canonical']]
        lob = [c['name'] for c in table['columns'] if any(k in c['type'].upper() for k in ('TEXT', 'BLOB', 'CLOB', 'BINARY'))]
        card = dict(name=name, domain=table['domain'], purpose=table['purpose'],
            schema_card=f'by_table/{name}.json', business_concepts=o.get('business_concepts', [table['domain'], name]),
            grain=grain, tenant=dict(column=tenant, required=bool(tenant), scope='direct' if tenant else 'no-direct-tenant-column; determine ownership via related scoped tables'),
            required_filters=required, canonical_filters=o.get('canonical_filters', {}),
            semantic_evidence=o.get('evidence', f'by_table/{name}.json: primary_key; lifecycle; key_notes; notes_for_agents'),
            canonical_joins=scoped_joins,
            join_effects=[dict(join_id=e['id'], table=e['to_table'], cardinality=e['cardinality'],
                multiplies_rows=e['row_multiplication_risk'], aggregation_warning=e['aggregation_warning'])
                for e in graph if e['from_table'] == name and not e['superseded_by']],
            deprecated_columns=o.get('deprecated_columns', []), preferred_columns=o.get('preferred_columns', {}),
            lob_columns=lob, indexes=table['indexes'],
            query_examples=[r['path'] for r in catalog if name in r['tables']],
            observed_queries_path=f'agent/observed_queries/{name}.json' if table.get('observed_queries') else None,
            observed_query_count=len(table.get('observed_queries', [])),
            warnings=o.get('warnings', []) + ([] if table['primary_key'] else ['No declared primary key: stored-row uniqueness and business grain require review.']))
        card['query_semantics'] = {k: card[k] for k in ('grain', 'required_filters', 'canonical_filters')}
        cards[name] = card
        write(root / 'agent' / 'tables' / f'{name}.json', card)
        if table.get('observed_queries'):
            write(root / 'agent' / 'observed_queries' / f'{name}.json', table['observed_queries'])
    intents = []
    for r in catalog:
        path = root / 'agent' / r['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        header = [f"-- {r['id']}: {r['intent']}", f"-- Result grain: {r['result_grain']}", '-- Dialect: MySQL; bind named parameters through your driver (do not interpolate).',
                  '-- Validation: static schema checks only; not executed on a Fluig database.']
        header += [f'-- Assumption: {note}' for note in r.get('assumptions', [])]
        path.write_text('\n'.join(header) + '\n' + r['sql'].strip() + '\n', encoding='utf-8')
        intents.append({k: v for k, v in r.items() if k != 'sql'})
    write(root / 'agent' / 'intents.json', dict(format_version=1, intents=intents))
    write(root / 'agent' / 'join_graph.json', dict(format_version=1, basis='schema relationships + declared uniqueness + tenant policy', joins=graph))
    write(root / 'agent' / 'query_rules.json', read(HERE / 'query_rules.json'))
    write(root / 'agent' / 'terminology.json', dict(format_version=1, concepts=[dict(table=n, aliases=o['business_concepts']) for n, o in overrides.items() if o.get('business_concepts')]))
    write(root / 'agent' / 'index.json', dict(format_version=1, schema_version='Fluig 1.8.2 clean-install MySQL',
        files=dict(intents='agent/intents.json', joins='agent/join_graph.json', rules='agent/query_rules.json', terminology='agent/terminology.json'),
        counts=dict(tables=len(cards), reviewed_business_grains=sum(c['grain']['business_grain_reviewed'] for c in cards.values()),
            recipes=len(catalog), observed_queries=sum(c['observed_query_count'] for c in cards.values())),
        tables=[dict(name=n, path=f'agent/tables/{n}.json', domain=c['domain'], tenant_column=c['tenant']['column'],
            grain_columns=c['grain']['columns'], business_grain_reviewed=c['grain']['business_grain_reviewed'],
            observed_query_count=c['observed_query_count']) for n, c in cards.items()]))
    print(f'agent: {len(cards)} cards, {len(catalog)} recipes, {len(graph)} directed joins')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=str(HERE.parent))
    generate(parser.parse_args().root)
