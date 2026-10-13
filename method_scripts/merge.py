import json, re, collections, os
d = json.load(open('ddl.json'))['tables']; ents = json.load(open('entities.json'))
by_simple = collections.defaultdict(list)
for e in ents.values(): by_simple[e['fqcn'].split('.')[-1]].append(e)
def ent_by_name(n):
    n = n.split('.')[-1].replace('.class', '').split('<')[-1].rstrip('>').replace('[]', '')
    return by_simple.get(n, [None])[0]
def tbl_of(e, seen=()):
    if e is None: return None
    if e['table'] and e['table'].upper() in d: return e['table'].upper()
    if e.get('extends') and e['fqcn'] not in seen:
        return tbl_of(ent_by_name(e['extends']), seen + (e['fqcn'],))
    return None
# table -> entities (direct + inheritance children)
t2e = collections.defaultdict(list)
for e in ents.values():
    if e['kind'] != 'entity': continue
    t = tbl_of(e)
    if t: t2e[t].append(e)
def all_fields(e, depth=0):
    """fields of entity incl. embedded id classes and superclass"""
    out = []
    for f in e['fields']:
        if f['embedded_id'] or (f['type'] and ent_by_name(f['type']) and ent_by_name(f['type'])['kind'] == 'embeddable' and not f['col']):
            emb = ent_by_name(f['type'])
            if emb and depth < 3:
                for g in all_fields(emb, depth + 1): g = dict(g); g['embedded_in'] = f['name']; g['id'] = f['embedded_id'] or g.get('id'); out.append(g)
                continue
        out.append(f)
    if e.get('extends') and depth < 4:
        p = ent_by_name(e['extends'])
        if p and p['kind'] in ('mappedsuperclass', 'entity', 'embeddable'): out += all_fields(p, depth + 1)
    return out
def domain(n, mod):
    P = lambda *p: n.startswith(p)
    if P('QRTZ_'): return 'scheduler-quartz'
    if P('FDN_ALERT'): return 'foundation-alerts'
    if P('FDN_OAUTH', 'FDN_AUTHORIZE', 'FDN_USERTOKEN', 'FDN_REQUEST_NONCE', 'FDN_USERMOBILE', 'FDN_JAAS', 'SESSAO_TOKEN', 'RESET_PASSWORD'): return 'security-oauth-tokens'
    if P('FDN_PDATA', 'FDN_PERSONALDATA'): return 'privacy-lgpd'
    if P('FDN_USER', 'FDN_ROLE', 'FDN_GROUP', 'FDN_PERMISSION', 'FDN_RESOURCE', 'FDN_RESTORE', 'FDN_TENANT', 'FDN_IDENTITY', 'FDN_SERVICE_OPERATION', 'FDN_PRODUCT'): return 'foundation-identity-access'
    if P('FDN_'): return 'foundation-platform'
    if P('WCM_'): return 'wcm-portal'
    if P('I18N', 'FDN_LITERAL', 'FDN_BUNDLE'): return 'i18n'
    if P('ECM_COLLAB'): return 'ecm-collaboration'
    if P('ECM_') : return 'ecm-metadata-forms'
    if P('FACT_', 'ACTIVITY_DIM', 'FLOW_DIM', 'TIME_DIM', 'USER_DIM', 'PROCES_VERSION_DIM'): return 'bpm-analytics-dw'
    if P('META_LIST', 'FILTER', 'PREFER', 'FAVORITOS'): return 'ecm-lists-filters'
    if P('DOCTO', 'DOCUMENTO', 'DOCUMENT_', 'TIPO_DOC', 'DEFAULT_PROPRIED', 'CONFIGUR_SEGUR', 'ASSUNTO', 'CONFIGUR_OBRIG', 'TAG', 'TERMO', 'SINONIMO', 'MARCA', 'FICHA', 'CAMPO_CUSTOM', 'PROPRIED_EXT', 'LINK_DOCTO', 'VERS', 'CONHECIMENTO', 'AREA_DEST', 'TEMA'): return 'ecm-documents'
    if mod.startswith('03001'): return 'social'
    if mod.startswith('04001'): return 'use-policy'
    if mod.startswith('08001'): return 'rating'
    if mod.startswith('02001'): return 'bpm-workflow'
    return 'foundation-platform'
model = {}
for n, t in d.items():
    es = t2e.get(n, [])
    prim = [e for e in es if e['table'] and e['table'].upper() == n] or es
    colmap = collections.OrderedDict()
    for c in t['columns']: colmap[c['name']] = dict(c, java=[])
    unmatched = []
    for e in es:
        for f in all_fields(e):
            if f['transient'] or not f['col']: continue
            cn = f['col'].upper()
            if cn in colmap: colmap[cn]['java'].append(dict(field=f['name'], type=f['type'], entity=e['fqcn'].split('.')[-1], lob=f['lob'], enum=f.get('enum', False), id=bool(f.get('id')), embedded_in=f.get('embedded_in')))
            else: unmatched.append((e['fqcn'].split('.')[-1], f['name'], f['col']))
    model[n] = dict(name=n, module=t['module'], domain=domain(n, t['module']), pk=t['pk'], columns=list(colmap.values()), indexes=t['indexes'], uniques=t['uniques'], fks=t['fks'],
        entities=[dict(fqcn=e['fqcn'], file=e['file'], kind=e['kind'], extends=e.get('extends')) for e in es],
        queries=[q['name'] for e in es for q in e['queries']], _q=[q for e in es for q in e['queries']], rel=[])
# relations
def add(src, scols, dst, dcols, kind, ev):
    if src not in model or dst not in model: return
    r = dict(from_table=src, from_cols=scols, to_table=dst, to_cols=dcols, kind=kind, evidence=ev)
    if not any(x['to_table'] == dst and x['from_cols'] == scols and x['to_cols'] == dcols for x in model[src]['rel']): model[src]['rel'].append(r)
for n, m in model.items():
    for fk in m['fks']: add(n, fk['cols'], fk['ref_table'], fk['ref_cols'], 'physical-fk', fk['name'])
for n, m in model.items():
    for e in t2e.get(n, []):
        for f in all_fields(e):
            if f['rel'] in ('ManyToOne', 'OneToOne') and f['joins']:
                tgt = ent_by_name(f.get('target') or f['type']); tt = tbl_of(tgt)
                if tt: add(n, [j['col'].upper() for j in f['joins'] if j['col']], tt, [(j['ref'] or '').upper() for j in f['joins'] if j['col']], 'jpa-join', f"{e['fqcn'].split('.')[-1]}.{f['name']}")
# hql joins
alias_re = re.compile(r'(?:\bfrom|\bjoin|,)\s+(\w+)\s+(?:as\s+)?(\w+)', re.I)
eq_re = re.compile(r'(\w+)\.([\w.]+)\s*=\s*(\w+)\.([\w.]+)')
def col_for(e, path):
    last = path.split('.')[-1]
    for f in all_fields(e):
        if f['name'] == last and f['col']: return f['col'].upper()
    return None
for n, m in model.items():
    for q in m['_q']:
        if q.get('native'): continue
        al = {}
        for a in alias_re.finditer(q['query']):
            if ent_by_name(a.group(1)): al[a.group(2)] = ent_by_name(a.group(1))
        for x in eq_re.finditer(q['query']):
            ea, eb = al.get(x.group(1)), al.get(x.group(3))
            if ea and eb and ea is not eb:
                ta, tb = tbl_of(ea), tbl_of(eb); ca, cb = col_for(ea, x.group(2)), col_for(eb, x.group(4))
                if ta and tb and ta != tb and ca and cb: add(ta, [ca], tb, [cb], 'hql-join', q['name'])
# inferred by PK column-name match
pkset = {n: m['pk'] for n, m in model.items()}
GENERIC = {'COD_EMPRESA', 'TENANT_ID', 'COMPANY_ID', 'ID', 'VERSION', 'NUM_VERS'}
abs_pk = pkset.get('ECM_ABSTRACT_FORM_ITEM')
for n, m in model.items():
    cn = {c['name'] for c in m['columns']}
    if n.startswith('ECM_') and n.endswith('_FORM_ITEM') and n != 'ECM_ABSTRACT_FORM_ITEM' and {'METADATAFORM_ID', 'HTML_ID'} <= cn and 'ID' not in cn:
        add(n, ['METADATAFORM_ID', 'HTML_ID'], 'ECM_ABSTRACT_FORM_ITEM', ['METADATAFORM_ID', 'HTML_ID'], 'table-per-class-subtype', 'JPA TABLE_PER_CLASS: this table repeats the abstract parent columns; (METADATAFORM_ID,HTML_ID) is unique in the parent'); continue
    cand = []
    for u, pk in pkset.items():
        if u == n or not pk: continue
        core = [c for c in pk if c not in GENERIC]
        if not core or not set(pk) <= cn or pk == ['ID']: continue
        if set(pk) == set(m['pk']): continue   # same PK = shared-pk / 1:1, not a plain FK
        if any(r['to_table'] == u for r in m['rel']): continue
        cand.append(u)
    # keep only the most specific targets (drop A when some matched B has PK superset of A's PK)
    keep = [u for u in cand if not any(v != u and set(pkset[v]) > set(pkset[u]) for v in cand)]
    for u in keep: add(n, pkset[u], u, pkset[u], 'inferred-name-match', 'all columns of target PK present in this table (heuristic, unconfirmed)')
for m in model.values(): m.pop('_q')
json.dump(model, open('model.json', 'w'), indent=1, ensure_ascii=False)
kinds = collections.Counter(r['kind'] for m in model.values() for r in m['rel'])
print(kinds, 'cols w/ java', sum(1 for m in model.values() for c in m['columns'] if c['java']), 'of', sum(len(m['columns']) for m in model.values()))
print(collections.Counter(m['domain'] for m in model.values()))
