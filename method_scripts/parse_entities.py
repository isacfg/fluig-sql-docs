import re, sys, json, os
root = sys.argv[1]; out = sys.argv[2]
files = []
for dp, dn, fn in os.walk(root, followlinks=True):
    for f in fn:
        if f.endswith('.java'): files.append(os.path.join(dp, f))
const = {}
CONST_RE = re.compile(r'(?:public\s+)?static\s+final\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;')
srcs = {}
for p in files:
    try: t = open(p, encoding='utf-8', errors='replace').read()
    except: continue
    if '@Entity' in t or '@Embeddable' in t or '@MappedSuperclass' in t or 'static final String' in t:
        srcs[p] = t
for p, t in srcs.items():
    cm = re.search(r'\bclass\s+(\w+)', t) or re.search(r'\binterface\s+(\w+)', t)
    if not cm: continue
    for m in CONST_RE.finditer(t):
        const.setdefault(cm.group(1) + '.' + m.group(1), m.group(2)); const.setdefault(m.group(1), m.group(2))
def resolve(expr):
    expr = expr.strip()
    m = re.match(r'"([^"]*)"$', expr)
    if m: return m.group(1)
    return const.get(expr) or const.get(expr.split('.')[-1]) or ('?' + expr)
def ann_attr(a, name):
    m = re.search(r'\b' + name + r'\s*=\s*("[^"]*"|[\w.]+)', a)
    return m.group(1) if m else None
def split_top_level(text, delimiter):
    parts = []; start = 0; depth = 0; quoted = False; escaped = False
    for i, ch in enumerate(text):
        if escaped: escaped = False; continue
        if quoted and ch == "\\": escaped = True; continue
        if ch == '"': quoted = not quoted
        if quoted: continue
        if ch in '({[': depth += 1
        elif ch in ')}]': depth -= 1
        elif ch == delimiter and depth == 0:
            parts.append(text[start:i].strip()); start = i + 1
    return parts + [text[start:].strip()]

def resolve_query_expression(expression):
    resolved = []
    for part in split_top_level(expression, '+'):
        if part.startswith('"'):
            try: value = json.loads(part)
            except json.JSONDecodeError: return '?' + expression
        else: value = resolve(part)
        if value.startswith('?'): return '?' + expression
        resolved.append(value)
    return ''.join(resolved)

entities = {}
for p, t in srcs.items():
    if not re.search(r'^@(Entity|Embeddable|MappedSuperclass)\b', t, re.M): continue
    pk = re.search(r'^package\s+([\w.]+);', t, re.M)
    cm = re.search(r'^((?:@[^\n]*\n)*)public\s+(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+([\w.<>]+))?', t, re.M)
    if not cm: continue
    fq = (pk.group(1) + '.' if pk else '') + cm.group(2)
    if fq in entities: continue
    head = t[:cm.end()]
    kind = 'entity' if re.search(r'^@Entity', head, re.M) else 'embeddable' if '@Embeddable' in head else 'mappedsuperclass'
    tm = re.search(r'@Table\(\s*name\s*=\s*("[^"]*"|[\w.]+)', head)
    table = resolve(tm.group(1)) if tm else None
    if kind == 'entity' and not table: table = cm.group(2); implicit = True
    else: implicit = False
    ent = dict(implicit_table=implicit, fqcn=fq, kind=kind, table=table, extends=cm.group(3), idclass=None, file=p.split('/sources/')[-1], fields=[], queries=[])
    ic = re.search(r'@IdClass\((\w+)', head)
    if ic: ent['idclass'] = ic.group(1)
    # Walk complete annotations: attribute order varies and native queries may
    # have resultClass before query. Preserve full text, including constant names.
    for qm in re.finditer(r'@(NamedQuery|NamedNativeQuery)\(', head):
        start = qm.end(); depth = 1; quoted = False; escaped = False; end = start
        for end in range(start, len(head)):
            ch = head[end]
            if escaped: escaped = False; continue
            if ch == "\\" and quoted: escaped = True; continue
            if ch == '"': quoted = not quoted
            if not quoted:
                if ch == '(': depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0: break
        annotation = head[start:end]
        expressions = {}
        for part in split_top_level(annotation, ','):
            if '=' in part:
                key, value = part.split('=', 1)
                if key.strip() in ('name', 'query'): expressions[key.strip()] = value.strip()
        attrs = {key: resolve_query_expression(value) for key, value in expressions.items()}
        if 'name' in attrs and 'query' in attrs:
            ent['queries'].append(dict(name=attrs['name'], query=attrs['query'],
                native=qm.group(1) == 'NamedNativeQuery',
                extraction_status='unresolved-constant' if any(v.startswith('?') for v in attrs.values()) else 'literal-or-resolved-constant'))
    body = t[cm.end():]
    anns = ''; depth = 0
    for line in body.split('\n'):
        s = line.strip()
        if not s: continue
        if s.startswith('@'):
            anns += ' ' + s; continue
        if s.startswith('//') or s.startswith('/*') or s.startswith('*'): continue
        fm = re.match(r'(?:private|protected|public)?\s*(?:static\s+)?(?:final\s+)?(?:transient\s+)?([\w.<>\[\], ?]+?)\s+(\w+)\s*(?:=\s*[^;]*)?;\s*$', s)
        if fm and '(' not in s.split('=')[0] and not s.startswith(('return', 'import', 'package')) and 'static' not in s.split(fm.group(1))[0]:
            f = dict(name=fm.group(2), type=fm.group(1).strip(), col=None, id=False, embedded_id='@EmbeddedId' in anns, lob='@Lob' in anns, transient='@Transient' in anns, rel=None, joins=[])
            cmm = re.search(r'@Column\(([^)]*)\)', anns)
            if cmm and ann_attr(cmm.group(1), 'name'): f['col'] = resolve(ann_attr(cmm.group(1), 'name'))
            f['id'] = bool(re.search(r'@Id\b', anns)); 
            if '@Enumerated' in anns: f['enum'] = True
            rm = re.search(r'@(ManyToOne|OneToMany|OneToOne|ManyToMany)\(([^)]*)\)', anns)
            if rm:
                f['rel'] = rm.group(1); mb = ann_attr(rm.group(2), 'mappedBy'); te = ann_attr(rm.group(2), 'targetEntity')
                if mb: f['mapped_by'] = mb.strip('"')
                if te: f['target'] = te.replace('.class', '')
            for jm in re.finditer(r'@JoinColumn\(([^)]*)\)', anns):
                n = ann_attr(jm.group(1), 'name'); r = ann_attr(jm.group(1), 'referencedColumnName')
                f['joins'].append(dict(col=resolve(n) if n else None, ref=resolve(r) if r else None))
            if re.search(r'@Table|@Entity', anns): pass
            ent['fields'].append(f); anns = ''
        elif not s.startswith(('}', '{')) and '(' in s: anns = ''
    entities[fq] = ent
json.dump(entities, open(out, 'w'), indent=1, ensure_ascii=False)
n = lambda k: sum(1 for e in entities.values() if e['kind'] == k)
print(len(entities), 'entities-ish', n('entity'), 'entity', n('embeddable'), 'embeddable', n('mappedsuperclass'), 'msc', 'consts', len(const))
print('with table', sum(1 for e in entities.values() if e['table']), 'unresolved', [e['table'] for e in entities.values() if e['table'] and e['table'].startswith('?')][:10])
