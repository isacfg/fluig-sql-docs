import re, sys, json, glob, os
root = sys.argv[1]; out = sys.argv[2]
tables = {}
unparsed = []
def split_top(s):
    parts, depth, cur = [], 0, ''
    for ch in s:
        if ch == '(': depth += 1
        if ch == ')': depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): parts.append(cur.strip())
    return parts
def cols(s): return [c.strip().strip('`') for c in s.split(',')]
for mod in sorted(glob.glob(root + '/0*')):
    modname = os.path.basename(mod)
    for f in sorted(glob.glob(mod + '/createtable/mysql/*.sql')):
        txt = open(f, encoding='utf-8', errors='replace').read()
        txt = txt.replace('`', ''); txt = re.sub(r'--[^\n]*', '', txt); txt = re.sub(r'/\*.*?\*/', '', txt, flags=re.S)
        for stmt in [s.strip() for s in txt.split(';') if s.strip()]:
            m = re.match(r'create\s+table\s+`?(\w+)`?\s*\((.*)\)\s*(ENGINE.*)?$', stmt, re.I | re.S)
            if m:
                t = m.group(1).upper()
                tab = tables.setdefault(t, dict(name=t, module=modname, file=os.path.basename(f), columns=[], pk=[], indexes=[], uniques=[], fks=[]))
                for item in split_top(m.group(2)):
                    pk = re.match(r'primary\s+key\s*\((.*)\)', item, re.I | re.S)
                    if pk: tab['pk'] = cols(pk.group(1)); continue
                    uq = re.match(r'(?:constraint\s+\w+\s+)?unique\s*(?:key|index)?\s*\w*\s*\((.*)\)', item, re.I | re.S)
                    if uq: tab['uniques'].append(cols(uq.group(1))); continue
                    kx = re.match(r'(?:key|index)\s+(\w+)\s*\((.*)\)', item, re.I | re.S)
                    if kx: tab['indexes'].append(dict(name=kx.group(1), unique=False, cols=cols(re.sub(r'\s+(asc|desc)\b', '', kx.group(2), flags=re.I)))); continue
                    fk = re.match(r'(?:constraint\s+(\w+)\s+)?foreign\s+key\s*(?:\w+\s*)?\((.*?)\)\s*references\s+`?(\w+)`?\s*\((.*?)\)', item, re.I | re.S)
                    if fk: tab['fks'].append(dict(name=fk.group(1), cols=cols(fk.group(2)), ref_table=fk.group(3).upper(), ref_cols=cols(fk.group(4)))); continue
                    cm = re.match(r'`?(\w+)`?\s+(.*)$', item, re.S)
                    if cm:
                        rest = ' '.join(cm.group(2).split())
                        ty = re.match(r'(\w+(?:\s*\([^)]*\))?)', rest)
                        tab['columns'].append(dict(name=cm.group(1).upper(), type=ty.group(1) if ty else rest,
                            nullable=not re.search(r'not\s+null', rest, re.I),
                            default=(re.search(r'default\s+(\S+)', rest, re.I) or [None, None])[1],
                            pk_inline=bool(re.search(r'primary\s+key', rest, re.I)), raw=rest))
                continue
            m = re.match(r'create\s+(unique\s+)?index\s+`?(\w+)`?\s+on\s+`?(\w+)`?\s*\((.*)\)', stmt, re.I | re.S)
            if m:
                tables.setdefault(m.group(3).upper(), dict(name=m.group(3).upper(), module=modname, file=None, columns=[], pk=[], indexes=[], uniques=[], fks=[]))
                tables[m.group(3).upper()]['indexes'].append(dict(name=m.group(2), unique=bool(m.group(1)), cols=cols(re.sub(r'\s+(asc|desc)\b', '', m.group(4), flags=re.I)))); continue
            m = re.match(r'alter\s+table\s+`?(\w+)`?\s+(.*)$', stmt, re.I | re.S)
            if m:
                t = m.group(1).upper(); body = m.group(2)
                tab = tables.setdefault(t, dict(name=t, module=modname, file=None, columns=[], pk=[], indexes=[], uniques=[], fks=[]))
                for fk in re.finditer(r'add\s+constraint\s+(\w+)\s+foreign\s+key\s*\((.*?)\)\s*references\s+`?(\w+)`?\s*\((.*?)\)', body, re.I | re.S):
                    tab['fks'].append(dict(name=fk.group(1), cols=cols(fk.group(2)), ref_table=fk.group(3).upper(), ref_cols=cols(fk.group(4))))
                for uq in re.finditer(r'add\s+constraint\s+(\w+)\s+unique\s*\((.*?)\)', body, re.I | re.S):
                    tab['uniques'].append(cols(uq.group(2)))
                for ac in re.finditer(r'add\s+(?:column\s+)?(?!(?:constraint|primary|foreign|unique|index|key)\b)(\w+)\s+([^,]+)', body, re.I):
                    rest = ' '.join(ac.group(2).split()); ty = re.match(r'(\w+(?:\s*\([^)]*\))?)', rest)
                    if ty and not any(c['name'] == ac.group(1).upper() for c in tab['columns']):
                        tab['columns'].append(dict(name=ac.group(1).upper(), type=ty.group(1), nullable=not re.search(r'not\s+null', rest, re.I), default=None, pk_inline=False, raw=rest, via_alter=True))
                if not re.search(r'add\s+constraint|add\s+(column\s+)?\w', body, re.I): unparsed.append(stmt[:120])
                continue
            unparsed.append(stmt[:120])
for t in tables.values():
    for c in t['columns']:
        if c.pop('pk_inline', False) and c['name'] not in t['pk']: t['pk'].append(c['name'])
json.dump(dict(tables=tables, unparsed=unparsed), open(out, 'w'), indent=1, ensure_ascii=False)
print(len(tables), 'tables', sum(len(t['columns']) for t in tables.values()), 'cols', sum(len(t['fks']) for t in tables.values()), 'fks', len(unparsed), 'unparsed')
print('no columns:', [n for n, t in tables.items() if not t['columns']][:20])
for u in unparsed[:10]: print(' ?', u.replace('\n', ' '))
