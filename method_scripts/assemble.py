import json, glob, os, collections, sys, shutil, re
OUT = sys.argv[1]
model = json.load(open('model.json'))
docs = {}
for f in sorted(glob.glob('out/batch_*.json')):
    try: d = json.load(open(f))
    except Exception as e: print('BAD JSON', f, e); continue
    for t in d['tables']: docs[t['name'].upper()] = t
missing_tables = [n for n in model if n not in docs]
print('tables documented', len(docs), 'missing', missing_tables)
final = collections.OrderedDict(); gaps = []
for n in sorted(model, key=lambda x: (docs.get(x, {}).get('domain') or model[x]['domain'], x)):
    m = model[n]; a = docs.get(n, {})
    acols = {c['name'].upper(): c for c in a.get('columns', [])}
    cols = []
    for c in m['columns']:
        ac = acols.get(c['name'], {})
        if not ac: gaps.append((n, c['name']))
        pkpos = m['pk'].index(c['name']) + 1 if c['name'] in m['pk'] else None
        cols.append(dict(name=c['name'], type=c['type'], nullable=c['nullable'], default=c['default'], pk_position=pkpos,
            purpose=ac.get('purpose', ''), semantic_type=ac.get('semantic_type', ''), values=ac.get('values', ''), refs=ac.get('refs', ''), confidence=ac.get('confidence', ''),
            java_field=(c['java'][0]['field'] if c['java'] else None), java_type=(c['java'][0]['type'] if c['java'] else None), java_entity=(c['java'][0]['entity'] if c['java'] else None)))
    rels, rejected, seen = [], [], set()
    key = lambda to, fc: (to.upper(), tuple(x.upper() for x in fc))
    for r in a.get('relationships', []):
        k = key(r['to_table'], r['from_cols'])
        if r.get('status') == 'rejected': rejected.append(r); continue
        seen.add(k); rels.append(r)
    for r in m['rel']:
        k = key(r['to_table'], r['from_cols'])
        if k in seen: continue
        if r['kind'] == 'inferred-name-match': continue   # unvetted heuristics are dropped unless agent kept them
        if any(x['to_table'].upper() == r['to_table'] and set(map(str.upper, x['from_cols'])) == set(r['from_cols']) for x in rejected): continue
        seen.add(k)
        rels.append(dict(to_table=r['to_table'], from_cols=r['from_cols'], to_cols=r['to_cols'], cardinality='N:1', kind=r['kind'], description=r['evidence'], status='confirmed'))
    final[n] = dict(name=n, domain=a.get('domain') or m['domain'], module=m['module'], purpose=a.get('purpose', ''), lifecycle=a.get('lifecycle', ''), key_notes=a.get('key_notes', ''),
        notes_for_agents=a.get('notes_for_agents', ''), primary_key=m['pk'], unique_constraints=m['uniques'], indexes=[dict(name=i['name'], unique=i['unique'], columns=i['cols']) for i in m['indexes']],
        jpa_entities=[e['fqcn'] for e in m['entities']], observed_queries=m.get('observed_queries', []), columns=cols, relationships=rels, rejected_relationships=rejected)
# Keep the prior reviewed correction reproducible in every descriptive field.
def normalize_user_refs(value):
    if isinstance(value, str):
        return re.sub(r'FDN_USER\.(USER_CODE|LOGIN)\b', r'FDN_USERTENANT.\1', value)
    if isinstance(value, list): return [normalize_user_refs(v) for v in value]
    if isinstance(value, dict): return {k: (v if k == 'observed_queries' else normalize_user_refs(v)) for k, v in value.items()}
    return value
final = normalize_user_refs(final)
# Reviewed catalog annotations override enrichment output deterministically.
with open(os.path.join(os.path.dirname(__file__), 'catalog_overrides.json'), encoding='utf-8') as source:
    annotations = json.load(source)
for name, fields in annotations.items():
    final[name].update(fields)
# post-fix of invalid agent edges
for n, t in final.items():
    keep = []
    for r in t['relationships']:
        to = r['to_table'].upper()
        if to == 'FDN_USER' and set(r['to_cols']) & {'USER_CODE', 'LOGIN'}: r['to_table'] = 'FDN_USERTENANT'; r['description'] = (r.get('description') or '') + ' [alvo corrigido: USER_CODE/LOGIN pertencem a FDN_USERTENANT]'
        if to == 'PROCES': r['to_table'] = 'DEF_PROCES'
        d = final.get(r['to_table'].upper())
        if not d or not set(map(str.upper, r['to_cols'])) <= {c['name'] for c in d['columns']}: print('dropped invalid edge', n, r['to_table'], r['to_cols']); continue
        keep.append(r)
    t['relationships'] = keep
# inbound
for n, t in final.items():
    t['referenced_by'] = []
for n, t in final.items():
    for r in t['relationships']:
        x = final.get(r['to_table'].upper())
        if x is not None: x['referenced_by'].append(dict(from_table=n, from_cols=r['from_cols'], to_cols=r['to_cols'], cardinality=r['cardinality'], kind=r['kind']))
print('column gaps', len(gaps), gaps[:10])
os.makedirs(OUT + '/by_table', exist_ok=True); os.makedirs(OUT + '/domains', exist_ok=True)
json.dump(dict(generated_from='TOTVS Fluig 1.8.2 (DDL MySQL de createtable + mapeamentos JPA)', tables=final), open(OUT + '/schema.json', 'w'), indent=1, ensure_ascii=False)
for n, t in final.items(): json.dump(t, open(f'{OUT}/by_table/{n}.json', 'w'), indent=1, ensure_ascii=False)
esc = lambda s: (s or '').replace('|', '\\|').replace('\n', ' ')
doms = collections.defaultdict(list)
for t in final.values(): doms[t['domain']].append(t)
for dom, ts in doms.items():
    L = [f'# Domínio: {dom}', '', f'{len(ts)} tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.', '']
    for t in ts:
        L += [f'## {t["name"]}', '', t['purpose'], '']
        if t['lifecycle']: L += [f'**Ciclo de vida:** {t["lifecycle"]}', '']
        if t['key_notes']: L += [f'**Atenção:** {t["key_notes"]}', '']
        L += [f'**PK:** {", ".join(t["primary_key"]) or "(nenhuma)"}' + (f' · **Unique:** ' + '; '.join('(' + ', '.join(u) + ')' for u in t['unique_constraints']) if t['unique_constraints'] else ''), '']
        L += ['| Coluna | Tipo | Null | Finalidade | Valores | Ref |', '|---|---|---|---|---|---|']
        for c in t['columns']:
            L.append(f'| {"🔑 " if c["pk_position"] else ""}`{c["name"]}` | {esc(c["type"])} | {"S" if c["nullable"] else "N"} | {esc(c["purpose"])} | {esc(c["values"])} | {esc(c["refs"])} |')
        L.append('')
        if t['relationships']:
            L += ['**Relacionamentos (saem desta tabela):**', '']
            for r in t['relationships']: L.append(f'- `({", ".join(r["from_cols"])})` → **{r["to_table"]}** `({", ".join(r["to_cols"])})` · {r["cardinality"]} · {r["kind"]}/{r.get("status","")} — {esc(r.get("description",""))}')
            L.append('')
        if t['notes_for_agents']: L += [f'**Dicas de consulta:** {t["notes_for_agents"]}', '']
    open(f'{OUT}/domains/{dom}.md', 'w').write('\n'.join(L))
# index
L = ['# Índice de tabelas', '', '| Tabela | Domínio | PK | Colunas | Finalidade |', '|---|---|---|---|---|']
for n, t in sorted(final.items()): L.append(f'| `{n}` | {t["domain"]} | {esc(", ".join(t["primary_key"]))} | {len(t["columns"])} | {esc(t["purpose"])} |')
open(OUT + '/index.md', 'w').write('\n'.join(L))
# relationships
L = ['# Relacionamentos', '', 'Lista plana de arestas `origem → destino` (FK física, join JPA/HQL, ou relação lógica validada). Diagramas Mermaid por domínio logo abaixo.', '', '| Origem | Colunas | Destino | Colunas | Card. | Tipo | Status |', '|---|---|---|---|---|---|---|']
edges = []
for n, t in final.items():
    for r in t['relationships']:
        edges.append((n, r)); L.append(f'| {n} | {", ".join(r["from_cols"])} | {r["to_table"]} | {", ".join(r["to_cols"])} | {r["cardinality"]} | {r["kind"]} | {r.get("status","")} |')
L += ['', '# Diagramas ER por domínio (relações dentro do domínio + arestas para outros domínios)', '']
for dom, ts in doms.items():
    names = {t['name'] for t in ts}; es = [(n, r) for n, r in edges if n in names]
    if not es: continue
    L += [f'## {dom}', '', '```mermaid', 'erDiagram']
    for n, r in es:
        card = {'1:1': '||--||', '1:N': '||--o{', 'N:M-via-this-table': '}o--o{'}.get(r['cardinality'], '}o--||')
        lab = ','.join(r['from_cols'])[:40].replace('"', "'")
        L.append(f'  {n} {card} {r["to_table"]} : "{lab}"')
    L += ['```', '']
open(OUT + '/relationships.md', 'w').write('\n'.join(L))
print('edges', len(edges), collections.Counter(r.get('status') for _, r in edges), 'rejected', sum(len(t['rejected_relationships']) for t in final.values()))

# Generate the SQL planning layer from the same final schema.
from generate_agent import generate
generate(OUT)
