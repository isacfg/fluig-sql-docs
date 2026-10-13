import json, os, collections
m = json.load(open('model.json'))
os.makedirs('batches', exist_ok=True); os.makedirs('out', exist_ok=True)
order = sorted(m.values(), key=lambda t: (t['domain'], t['name']))
batches, cur, cc = [], [], 0
for t in order:
    nc = len(t['columns'])
    if cur and (len(cur) >= 24 or cc + nc > 230 or cur[-1]['domain'] != t['domain'] and cc > 120):
        batches.append(cur); cur, cc = [], 0
    cur.append(t); cc += nc
if cur: batches.append(cur)
for i, b in enumerate(batches, 1):
    tabs = []
    for t in b:
        tabs.append(dict(name=t['name'], domain_hint=t['domain'], module=t['module'], pk=t['pk'],
            entities=[dict(class_=e['fqcn'], file_suffix=e['file']) for e in t['entities']],
            columns=[dict(name=c['name'], type=c['type'], nullable=c['nullable'], default=c['default'], java=[dict(field=j['field'], type=j['type'], entity=j['entity'], enum=j['enum'], lob=j['lob']) for j in c['java']]) for c in t['columns']],
            uniques=t['uniques'], indexes=[dict(name=x['name'], unique=x['unique'], cols=x['cols']) for x in t['indexes']],
            candidate_relations=[dict(to=r['to_table'], from_cols=r['from_cols'], to_cols=r['to_cols'], kind=r['kind'], evidence=r['evidence']) for r in t['rel']],
            named_queries=t.get('observed_queries', t['queries'])[:12]))
    json.dump(dict(batch=i, tables=tabs), open(f'batches/batch_{i:02d}.json', 'w'), indent=1, ensure_ascii=False)
    print(i, len(b), sum(len(t['columns']) for t in b), b[0]['domain'], '..', b[-1]['domain'], [t['name'] for t in b][:3])
