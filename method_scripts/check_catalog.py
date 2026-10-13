"""Validate the generated catalog and every SQL recipe without a database."""
from pathlib import Path
import re

from generate_agent import HERE, read, unique_keys
from validate_sql import validate


def check(root=HERE.parent):
    root=Path(root)
    tables=read(root/'schema.json')['tables']
    idx=read(root/'agent/index.json')
    catalog=read(root/'agent/intents.json')['intents']
    assert idx['counts']['tables']==len(tables)
    assert idx['counts']['recipes']==len(catalog)==len(list((root/'agent/recipes').rglob('*.sql')))
    for name,t in tables.items():
        assert read(root/f'by_table/{name}.json')==t, name
        card=read(root/f'agent/tables/{name}.json')
        columns={c['name'] for c in t['columns']}
        assert card['grain']['columns']==t['primary_key'],name
        assert set(card['deprecated_columns'])<=columns,name
        assert set(card['preferred_columns'].values())<=columns,name
        assert all(f['column'] in columns for f in card['required_filters']),name
        for filters in card['canonical_filters'].values():
            for f in filters:
                # Filter expressions are table-local; parameters and literals
                # aren't identifiers. SQLGlot checks recipes independently.
                col=f.split()[0]
                assert col in columns,(name,f)
        for path in card['query_examples']:
            assert (root/'agent'/path).is_file(),path
        if card['observed_queries_path']:
            observed=read(root/card['observed_queries_path'])
            assert observed==t['observed_queries'],name
            assert len(observed)==card['observed_query_count'],name
            assert all(q['language'] in ('sql','hql') and q['source_entity'] and q['query'] for q in observed)
    for edge in read(root/'agent/join_graph.json')['joins']:
        f,t=tables[edge['from_table']],tables[edge['to_table']]
        assert all(p['from_column'] in {c['name'] for c in f['columns']} and p['to_column'] in {c['name'] for c in t['columns']} for p in edge['column_pairs'])
        if edge['safe']:
            assert edge['tenant_complete'] and edge['confidence']=='confirmed' and not edge['superseded_by']
            assert any(k <= {p['to_column'] for p in edge['column_pairs']} for k in unique_keys(t))
    warnings=0
    for recipe in catalog:
        sql=(root/'agent'/recipe['path']).read_text()
        params=set(re.findall(r':([a-z_]+)',sql))
        assert params=={p['name'] for p in recipe['parameters']},recipe['id']
        assert recipe['start_table'] in recipe['tables']
        assert set(recipe['tables'])<=set(tables),recipe['id']
        result=validate(sql,root=root,document_mode=recipe['document_mode'])
        assert result['errors']==0,(recipe['id'],result)
        actual={i['rule'] for i in result['issues'] if i['severity']=='warning'}
        assert actual==set(recipe['expected_warnings']),(recipe['id'],result)
        warnings+=result['warnings']
    print(f'PASS: {len(tables)} table cards, {len(catalog)} recipes, {warnings} documented warnings; static checks only.')


if __name__=='__main__': check()
