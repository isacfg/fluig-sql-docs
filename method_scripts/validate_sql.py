"""Static schema and planning checks. Never connects to or executes on a DB."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

try:
    import sqlglot
    from sqlglot import exp
    from sqlglot.optimizer.qualify import qualify
    from sqlglot.optimizer.scope import traverse_scope, Scope
except ImportError:
    raise SystemExit('Install validator dependency: python3 -m pip install -r method_scripts/requirements.txt')

ROOT = Path(__file__).resolve().parents[1]


def guaranteed_atoms(expression):
    """Facts implied by all branches; OR is intersection, never union."""
    if expression is None:
        return {}
    if isinstance(expression, exp.Paren):
        return guaranteed_atoms(expression.this)
    if isinstance(expression, exp.And):
        return {**guaranteed_atoms(expression.this), **guaranteed_atoms(expression.expression)}
    if isinstance(expression, exp.Or):
        left, right = guaranteed_atoms(expression.this), guaranteed_atoms(expression.expression)
        return {k: v for k, v in left.items() if k in right}
    return {expression.sql(dialect='mysql').upper(): expression}


def validate(sql, root=ROOT, dialect='mysql', document_mode='unspecified'):
    root = Path(root)
    schema = json.loads((root / 'schema.json').read_text())['tables']
    graph = json.loads((root / 'agent/join_graph.json').read_text())['joins']
    cards = {n: json.loads((root / f'agent/tables/{n}.json').read_text()) for n in schema}
    issues = []
    def issue(rule, severity, message):
        item = dict(rule=rule, severity=severity, message=message)
        if item not in issues: issues.append(item)
    def report():
        errors = sum(x['severity'] == 'error' for x in issues)
        return dict(status='error' if errors else ('needs-review' if issues else 'static-checks-passed'),
            errors=errors, warnings=sum(x['severity'] == 'warning' for x in issues),
            document_mode=document_mode, checks='static-only; no database execution or permission verification', issues=issues)
    try:
        statements = [s for s in sqlglot.parse(sql, read=dialect) if s is not None]
    except (sqlglot.errors.ParseError, sqlglot.errors.TokenError) as e:
        issue('syntax', 'error', str(e)); return report()
    if len(statements) != 1 or not isinstance(statements[0], exp.Query) or statements[0].find(exp.Into):
        issue('query-only', 'error', 'Provide exactly one SELECT/UNION query.'); return report()
    tree = statements[0]
    for t in tree.find_all(exp.Table):
        # CTE names are resolved by qualify; check real tables in scopes below.
        if t.catalog or t.db:
            issue('schema-namespace', 'warning', f'Catalog/schema qualifier {t.sql()} must be verified on the instance.')
    original_scopes = list(traverse_scope(tree))
    for scope in original_scopes:
        for alias, (_, src) in scope.selected_sources.items():
            if isinstance(src, exp.Table) and src.name.upper() not in schema:
                issue('unknown-table-column','error', f'Unknown table: {src.name}')
        # Count(*) is not a projection wildcard.
        if any(s.is_star for s in scope.expression.selects):
            lob_tables = [src.name for _, src in scope.selected_sources.values()
                if isinstance(src, exp.Table) and src.name.upper() in cards and cards[src.name.upper()]['lob_columns']]
            if lob_tables: issue('avoid-select-star-lob', 'warning', 'Wildcard projection includes LOB tables: '+', '.join(lob_tables))
    if any(x['severity']=='error' for x in issues): return report()
    try:
        # Qualification resolves unqualified, correlated, CTE and derived columns
        # against the actual catalog, rejecting missing and ambiguous references.
        tree = qualify(tree, dialect=dialect, schema={n:{c['name']:'UNKNOWN' for c in t['columns']} for n,t in schema.items()},
            identify=False, quote_identifiers=False, validate_qualify_columns=True)
    except (sqlglot.errors.OptimizeError, sqlglot.errors.SchemaError) as e:
        issue('unknown-table-column','error', str(e)); return report()
    scopes = list(traverse_scope(tree))
    by_id = {id(s):s for s in scopes}
    sources = {}
    for sc in scopes:
        for alias, (_, src) in sc.selected_sources.items():
            if isinstance(src, exp.Table): sources[(id(sc), alias.upper())] = src.name.upper()
            elif isinstance(src, Scope):
                issue('derived-tenant-scope','warning', f'Derived source {alias}: tenant lineage and result grain require manual review.')
    def node(sc, column):
        if not isinstance(column, exp.Column): return None
        cursor = sc
        while cursor:
            key = (id(cursor), column.table.upper())
            if key in sources: return key + (column.name.upper(),)
            if any(a.upper() == column.table.upper() for a in cursor.selected_sources): return None
            cursor = cursor.parent
        return None
    def constant(e):
        return isinstance(e, (exp.Literal, exp.Placeholder, exp.Parameter))
    anchors = set()
    links = set()
    predicates = defaultdict(list)
    pair_conditions = defaultdict(set)
    def facts(sc, expression, outer_alias=None):
        for atom in guaranteed_atoms(expression).values():
            if not isinstance(atom, exp.EQ): continue
            left, right = node(sc, atom.this), node(sc, atom.expression)
            predicates[id(sc)].append(atom)
            if left and right:
                # Propagate outer scope anchors into correlated subqueries, not
                # out of a SELECT scalar subquery back into its unfiltered parent.
                if outer_alias:
                    if right[1] == outer_alias: links.add((left, right))
                    if left[1] == outer_alias: links.add((right, left))
                elif left[0] == right[0]:
                    links.add((left, right)); links.add((right, left))
                elif left[0] == id(sc): links.add((right, left))
                elif right[0] == id(sc): links.add((left, right))
                if left[:2] != right[:2]:
                    # Use source order to express effect from FROM root to JOIN.
                    order = list(sources)
                    a,b = sorted((left[:2],right[:2]), key=lambda k:order.index(k))
                    pair_conditions[(id(sc),a,b)].add((left[2],right[2]) if a==left[:2] else (right[2],left[2]))
            elif left and constant(atom.expression):
                if not outer_alias or left[1] == outer_alias: anchors.add(left)
            elif right and constant(atom.this):
                if not outer_alias or right[1] == outer_alias: anchors.add(right)
    for sc in scopes:
        where = sc.expression.args.get('where')
        facts(sc, where.this if where else None)
        for join in sc.expression.args.get('joins') or []:
            side = (join.args.get('side') or '').upper()
            if side == 'LEFT': facts(sc, join.args.get('on'), join.this.alias_or_name.upper())
            elif side in ('RIGHT', 'FULL'):
                issue('outer-join-scope','warning','RIGHT/FULL JOIN tenant propagation needs manual review.')
            else: facts(sc, join.args.get('on'))
    # Only tenant equalities propagate tenant scope, not arbitrary equalities.
    def tenant_node(n):
        return n[2] == cards[sources[n[:2]]]['tenant']['column']
    anchors = {n for n in anchors if tenant_node(n)}
    tenant_links = {(a,b) for a,b in links if tenant_node(a) and tenant_node(b)}
    while True:
        more = {b for a,b in tenant_links if a in anchors} - anchors
        if not more: break
        anchors |= more
    for key, name in sources.items():
        card = cards[name]; tenant = card['tenant']['column']
        if tenant and key+(tenant,) not in anchors:
            issue('tenant-filter','error', f'{key[1]} ({name}) must constrain {tenant} on every branch, directly or via a constrained tenant equality.')
        if name == 'FDN_USER':
            connected = any((a[:2]==key and sources[b[:2]]=='FDN_USERTENANT' and b[:2]+('TENANT_ID',) in anchors)
                or (b[:2]==key and sources[a[:2]]=='FDN_USERTENANT' and a[:2]+('TENANT_ID',) in anchors) for a,b in links)
            if not connected: issue('global-user-scope','warning','FDN_USER has no verified link to a scoped FDN_USERTENANT in this query.')
        if name == 'DOCUMENTO' and document_mode != 'historical':
            values = set()
            for atom in predicates[key[0]]:
                for c,v in ((atom.this,atom.expression),(atom.expression,atom.this)):
                    if node(by_id[key[0]],c) and node(by_id[key[0]],c)[:2] == key and isinstance(v,exp.Literal):
                        values.add((c.name.upper(),str(v.this)))
            if not {('VERSAO_ATIVA','1'),('LOG_DELETE','0')} <= values:
                issue('document-current-version','warning',f'{key[1]}: require VERSAO_ATIVA=1 AND LOG_DELETE=0 for current state, or declare --document-mode historical.')
    for sc in scopes:
        for col in sc.columns:
            n=node(sc,col)
            if n and n[2] in cards[sources[n[:2]]]['deprecated_columns']:
                issue('deprecated-column','warning',f'Deprecated column {col.sql()}; prefer the table card timestamps.')
    for (scid,a,b), actual in pair_conditions.items():
        source,to=sources[a],sources[b]
        candidates=[e for e in graph if e['from_table']==source and e['to_table']==to and not e['superseded_by']]
        matching=[e for e in candidates if {(p['from_column'],p['to_column']) for p in e['column_pairs']} <= actual]
        if not matching:
            if candidates: issue('complete-join','error',f'Incomplete or unrecognized join {a[1]} ({source}) -> {b[1]} ({to}); load the complete join_graph edge including tenant/version keys.')
            else: issue('unobserved-join','warning',f'No documented join for {source} -> {to}; verify equality columns and cardinality.')
        else:
            best=max(matching,key=lambda e:(len(e['column_pairs']),e['confidence']=='confirmed'))
            if best['confidence'] != 'confirmed': issue('probable-relationship','warning',f'{source} -> {to} is probable; declare and verify this assumption.')
            if not best['preserves_grain'] and a[0]==b[0]:
                issue('row-multiplication','warning',f'{source} -> {to} may multiply root rows; check requested grain before counting or aggregating.')
    # Check each joined alias, so one valid join cannot hide a second cross join.
    for sc in scopes:
        for join in sc.expression.args.get('joins') or []:
            key=(id(sc),join.this.alias_or_name.upper())
            if key in sources and not any(k[0]==id(sc) and key in k[1:] for k in pair_conditions):
                issue('unobserved-join','warning',f'No guaranteed column equality for joined alias {key[1]}; review cross/non-equi join grain manually.')
    return report()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('sql',type=Path); p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--dialect',choices=['mysql','oracle','tsql'],default='mysql')
    p.add_argument('--document-mode',choices=['unspecified','current','historical'],default='unspecified')
    p.add_argument('--strict',action='store_true',help='Fail on warnings as well as errors.')
    a=p.parse_args(); result=validate(a.sql.read_text(),a.root,a.dialect,a.document_mode)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result['errors'] or (a.strict and result['warnings']) else 0


if __name__=='__main__': sys.exit(main())
