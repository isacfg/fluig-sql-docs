import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'method_scripts'))
from generate_agent import generate,read
from validate_sql import validate
from check_catalog import check


class ValidatorTests(unittest.TestCase):
    def rules(self,sql,**kw):
        return {i['rule'] for i in validate(sql,**kw)['issues']}

    def test_catalog_and_all_recipes(self):
        check()

    def test_missing_tenant(self):
        self.assertIn('tenant-filter',self.rules('SELECT NUM_PROCES FROM PROCES_WORKFLOW'))

    def test_or_does_not_guarantee_tenant(self):
        self.assertIn('tenant-filter',self.rules('SELECT p.NUM_PROCES FROM PROCES_WORKFLOW p WHERE p.COD_EMPRESA=:tenant_id OR p.LOG_ATIV=1'))

    def test_tenant_in_every_or_branch(self):
        self.assertNotIn('tenant-filter',self.rules('SELECT p.NUM_PROCES FROM PROCES_WORKFLOW p WHERE (p.COD_EMPRESA=:tenant_id AND p.LOG_ATIV=1) OR (p.COD_EMPRESA=:tenant_id AND p.LOG_ATIV=0)'))

    def test_tenant_identifier_in_comment_not_predicate(self):
        self.assertIn('tenant-filter',self.rules('SELECT p.NUM_PROCES FROM PROCES_WORKFLOW p -- COD_EMPRESA=:tenant_id'))

    def test_left_join_cannot_filter_preserved_side(self):
        sql='SELECT p.NUM_PROCES FROM PROCES_WORKFLOW p LEFT JOIN TAR_PROCES t ON t.NUM_PROCES=p.NUM_PROCES AND t.COD_EMPRESA=p.COD_EMPRESA AND t.COD_EMPRESA=:tenant_id'
        self.assertIn('tenant-filter',self.rules(sql))

    def test_scalar_subquery_cannot_filter_parent(self):
        sql='SELECT p.NUM_PROCES, (SELECT COUNT(*) FROM TAR_PROCES t WHERE t.COD_EMPRESA=:tenant_id AND t.COD_EMPRESA=p.COD_EMPRESA) FROM PROCES_WORKFLOW p'
        self.assertIn('tenant-filter',self.rules(sql))

    def test_partial_join_even_with_both_tenant_filters(self):
        sql='SELECT t.NUM_PROCES FROM TAR_PROCES t JOIN PROCES_WORKFLOW p ON p.NUM_PROCES=t.NUM_PROCES WHERE t.COD_EMPRESA=:tenant_id AND p.COD_EMPRESA=:tenant_id'
        self.assertIn('complete-join',self.rules(sql))

    def test_missing_attachment_version(self):
        sql='SELECT a.NUM_SEQ_ANEXO FROM ANEXO_PROCES a JOIN DOCUMENTO d ON a.COD_EMPRESA=d.COD_EMPRESA AND a.NR_DOCUMENTO=d.NR_DOCUMENTO WHERE a.COD_EMPRESA=:tenant_id'
        self.assertIn('complete-join',self.rules(sql,document_mode='historical'))

    def test_count_after_task_join_has_fanout_warning(self):
        sql='SELECT COUNT(*) FROM PROCES_WORKFLOW p JOIN TAR_PROCES t ON p.NUM_PROCES=t.NUM_PROCES AND p.COD_EMPRESA=t.COD_EMPRESA WHERE p.COD_EMPRESA=:tenant_id'
        self.assertIn('row-multiplication',self.rules(sql))

    def test_unknown_column_and_table(self):
        self.assertIn('unknown-table-column',self.rules('SELECT p.NO_SUCH_COLUMN FROM PROCES_WORKFLOW p WHERE p.COD_EMPRESA=:tenant_id'))
        self.assertIn('unknown-table-column',self.rules('SELECT x.ID FROM NO_SUCH_TABLE x'))

    def test_ambiguous_column(self):
        self.assertIn('unknown-table-column',self.rules('SELECT NUM_PROCES FROM TAR_PROCES t JOIN PROCES_WORKFLOW p ON t.COD_EMPRESA=p.COD_EMPRESA AND t.NUM_PROCES=p.NUM_PROCES WHERE p.COD_EMPRESA=:tenant_id'))

    def test_document_current_and_history(self):
        sql='SELECT d.NR_VERSAO FROM DOCUMENTO d WHERE d.COD_EMPRESA=:tenant_id'
        self.assertIn('document-current-version',self.rules(sql))
        self.assertNotIn('document-current-version',self.rules(sql,document_mode='historical'))

    def test_star_and_qualified_star_on_lob(self):
        for projection in ('*','d.*'):
            self.assertIn('avoid-select-star-lob',self.rules(f'SELECT {projection} FROM DOCUMENTO d WHERE d.COD_EMPRESA=:tenant_id'))
        self.assertNotIn('avoid-select-star-lob',self.rules('SELECT COUNT(*) FROM DOCUMENTO d WHERE d.COD_EMPRESA=:tenant_id',document_mode='historical'))

    def test_deprecated_timestamp(self):
        self.assertIn('deprecated-column',self.rules('SELECT t.DEADLINEDATE FROM TAR_PROCES t WHERE t.COD_EMPRESA=:tenant_id'))

    def test_user_code_not_declared_unique(self):
        edges=read(ROOT/'agent/join_graph.json')['joins']
        relevant=[e for e in edges if e['from_table']=='TAR_PROCES' and e['to_table']=='FDN_USERTENANT']
        self.assertTrue(relevant)
        self.assertTrue(all(not e['safe'] and not e['preserves_grain'] for e in relevant))

    def test_global_user_needs_scope(self):
        self.assertIn('global-user-scope',self.rules('SELECT u.FULL_NAME FROM FDN_USER u'))

    def test_cte_requires_explicit_manual_lineage_review(self):
        sql='WITH x AS (SELECT p.COD_EMPRESA,p.NUM_PROCES FROM PROCES_WORKFLOW p WHERE p.COD_EMPRESA=:tenant_id) SELECT x.NUM_PROCES FROM x'
        self.assertIn('derived-tenant-scope',self.rules(sql))

    def test_not_a_query_and_multiple_statements(self):
        self.assertIn('query-only',self.rules('DELETE FROM PROCES_WORKFLOW'))
        self.assertIn('query-only',self.rules('SELECT 1; SELECT 2'))

    def test_cross_join_is_not_hidden_by_another_valid_join(self):
        sql="SELECT t.NUM_PROCES FROM TAR_PROCES t JOIN PROCES_WORKFLOW p ON t.COD_EMPRESA=p.COD_EMPRESA AND t.NUM_PROCES=p.NUM_PROCES CROSS JOIN FDN_ROLE r WHERE p.COD_EMPRESA=:tenant_id AND r.TENANT_ID=:tenant_id"
        self.assertIn('unobserved-join',self.rules(sql))

    def test_unterminated_string_is_a_reported_syntax_error(self):
        self.assertIn('syntax',self.rules("SELECT 'unterminated"))

    def test_cli_fails_on_tenant_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.sql';path.write_text('SELECT NUM_PROCES FROM PROCES_WORKFLOW')
            run=subprocess.run([sys.executable,str(ROOT/'method_scripts/validate_sql.py'),str(path)],capture_output=True,text=True)
            self.assertEqual(run.returncode,1)
            self.assertEqual(json.loads(run.stdout)['status'],'error')


class RecipeBehaviorTests(unittest.TestCase):
    def test_exists_keeps_process_grain_and_tenant(self):
        db=sqlite3.connect(':memory:')
        db.executescript('''CREATE TABLE PROCES_WORKFLOW (COD_EMPRESA INTEGER, NUM_PROCES INTEGER, COD_DEF_PROCES TEXT, START_DATE TEXT, LOG_ATIV INTEGER);
CREATE TABLE TAR_PROCES (COD_EMPRESA INTEGER, NUM_PROCES INTEGER, CD_MATRICULA TEXT, LOG_ATIV INTEGER, IDI_STATUS INTEGER);
INSERT INTO PROCES_WORKFLOW VALUES (1,10,'purchase','2026-01-01',1),(2,10,'other','2026-01-02',1),(1,11,'purchase','2026-01-03',1);
INSERT INTO TAR_PROCES VALUES (1,10,'alice',1,0),(1,10,'alice',1,1),(2,10,'alice',1,0),(1,11,'alice',0,2);''')
        sql=(ROOT/'agent/recipes/workflow/processes_with_pending_tasks.sql').read_text()
        rows=db.execute(sql,dict(tenant_id=1,user_code='alice')).fetchall()
        self.assertEqual(rows,[(1,10,'purchase','2026-01-01')]); db.close()

    def test_attachment_uses_recorded_version(self):
        db=sqlite3.connect(':memory:')
        db.executescript('''CREATE TABLE ANEXO_PROCES (COD_EMPRESA INTEGER,NUM_PROCES INTEGER,NUM_SEQ_ANEXO INTEGER,NR_DOCUMENTO INTEGER,NR_VERSAO INTEGER,DT_ANEXO TEXT);
CREATE TABLE DOCUMENTO (COD_EMPRESA INTEGER,NR_DOCUMENTO INTEGER,NR_VERSAO INTEGER,DS_PRINCIPAL_DOCUMENTO TEXT,LOG_DELETE INTEGER);
INSERT INTO ANEXO_PROCES VALUES (1,10,1,100,1,'2026-01-01');
INSERT INTO DOCUMENTO VALUES (1,100,1,'recorded',0),(1,100,2,'current',0),(2,100,1,'other tenant',0);''')
        sql=(ROOT/'agent/recipes/workflow/process_attachments.sql').read_text()
        rows=db.execute(sql,dict(tenant_id=1,process_id=10)).fetchall()
        self.assertEqual(len(rows),1);self.assertEqual(rows[0][-2],'recorded'); db.close()


class PipelineTests(unittest.TestCase):
    def test_agent_generation_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'schema.json').write_bytes((ROOT/'schema.json').read_bytes());generate(p)
            for f in (p/'agent').rglob('*'):
                if f.is_file():self.assertEqual(f.read_bytes(),(ROOT/f.relative_to(p)).read_bytes(),str(f))

    def test_parser_preserves_long_queries_constants_and_native_attributes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);q='SELECT x FROM Example x WHERE '+('x.name = :name AND '*200)+'x.id = :id'
            (p/'Example.java').write_text('package demo;\n@Entity\n@Table(name = "EXAMPLE")\n@NamedQuery(name = Example.FIND, query = '+json.dumps(q)+')\n@NamedNativeQuery(name = "native", resultClass = Example.class, query = "SELECT * FROM EXAMPLE")\npublic class Example {\n public static final String FIND = "Example.find";\n @Column(name = "ID")\n private Long id;\n}\n')
            out=p/'entities.json'
            run=subprocess.run([sys.executable,str(ROOT/'method_scripts/parse_entities.py'),str(p),str(out)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            qs=read(out)['demo.Example']['queries'];self.assertEqual(qs[0]['name'],'Example.find');self.assertEqual(qs[0]['query'],q)
            self.assertTrue(qs[1]['native']);self.assertEqual(qs[1]['query'],'SELECT * FROM EXAMPLE')

    def test_parser_does_not_truncate_concatenated_query_literals(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'Example.java').write_text('package demo;\n@Entity\n@Table(name = "EXAMPLE")\n@NamedQuery(query = "SELECT x " + "FROM Example x WHERE x.id = :id", name = "Example.concat")\npublic class Example {\n}\n')
            out=p/'entities.json'
            run=subprocess.run([sys.executable,str(ROOT/'method_scripts/parse_entities.py'),str(p),str(out)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(read(out)['demo.Example']['queries'][0]['query'],'SELECT x FROM Example x WHERE x.id = :id')


if __name__=='__main__':unittest.main()
