"""No-network tests of dangerous bootstrap boundaries and resume behavior."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('provision_github', (HERE / 'provision_github.py') if (HERE / 'provision_github.py').exists() else (HERE.parent / 'scripts/provision_github.py'))
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class ProvisionerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = p.State(Path(self.temp.name) / 'state.json')
        self.node = {'id':'APP-PROGRAM','title':'Program','_title':'[APP-PROGRAM] Program',
                     '_body':'<!-- plan-id: APP-PROGRAM -->\n', 'parent_id':None,
                     'status':'Backlog','priority':'Critical','labels':['type: program']}
        self.issue = {'id':101,'node_id':'I_101','number':1,'html_url':'https://github.com/'+p.TARGET+'/issues/1',
                      'title':self.node['_title'],'body':self.node['_body'],'state':'open','labels':[{'name':'type: program'}]}
        self.config = {'fields':[{'name':'Status','type':'SINGLE_SELECT','node_key':'status','options':['Backlog','Done']},
                                 {'name':'Priority','type':'SINGLE_SELECT','node_key':'priority','options':['Critical','Low']}]}

    def runner(self, gh):
        return p.Provisioner(Path(self.temp.name), {'nodes':[self.node]}, self.config, gh, self.state)

    def test_recorded_project_rename_does_not_create_duplicate(self):
        root = Path(self.temp.name)
        (root / 'planning').mkdir()
        (root / 'planning/GITHUB_ESTABLISHMENT_RECEIPT.json').write_text(json.dumps({
            'repository': p.TARGET, 'project_url': 'https://github.com/orgs/Pick-Your-AI/projects/10'}), encoding='utf-8')
        gh = type('Fake', (), {'apply': True})()
        runner = self.runner(gh)
        project = {'id': 'P10', 'number': 10, 'title': 'Renamed project',
                   'url': 'https://github.com/orgs/Pick-Your-AI/projects/10',
                   'readme': None, 'public': False, 'closed': False}
        runner.projects = lambda: ('ORG', [project])
        runner.ensure_project()
        self.assertEqual(runner.project['id'], 'P10')
        self.assertEqual(runner.report['project_title_drift']['observed_title'], 'Renamed project')

    def test_missing_recorded_project_never_falls_back_to_title(self):
        self.state.data['project'] = {'id': 'P10', 'number': 10}
        runner = self.runner(type('Fake', (), {'apply': True})())
        runner.projects = lambda: ('ORG', [{'id': 'P11', 'number': 11, 'title': p.PROJECT_TITLE}])
        with self.assertRaisesRegex(p.BootstrapError, 'refusing duplicate creation'):
            runner.ensure_project()

    def test_default_dry_run_is_offline(self):
        config = dict(self.config, labels=[])
        output = io.StringIO()
        with patch.object(p, 'load_plan', return_value=({'nodes':[self.node]},config)), patch.object(p.subprocess, 'run') as run, contextlib.redirect_stdout(output):
            code = p.main(['--root', self.temp.name])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())['remote_calls'], 0)
        run.assert_not_called()

    def test_duplicate_remote_marker_stops(self):
        another = dict(self.issue, number=2, id=102)
        with self.assertRaisesRegex(p.BootstrapError, 'Duplicate live marker'):
            p.index_issues([self.issue, another])

    def test_multiple_markers_on_one_issue_stops(self):
        issue = dict(self.issue, body=self.issue['body']+'<!-- plan-id: APP-C01 -->')
        with self.assertRaises(p.BootstrapError): p.index_issues([issue])

    def test_preexisting_issue_changed_body_is_not_overwritten(self):
        gh = type('Fake', (), {'apply':True})()
        runner = self.runner(gh)
        with self.assertRaisesRegex(p.BootstrapError, 'preserved'):
            runner.check_issue(self.node, dict(self.issue, body=self.issue['body']+'Human progress'))

    def test_issue_resume_reuses_exact_marker_without_mutation(self):
        gh = type('Fake', (), {'apply':True})()
        runner = self.runner(gh)
        runner.all_issues = lambda: {'APP-PROGRAM':self.issue}
        runner.ensure_issues()
        self.assertEqual(self.state.data['issues']['APP-PROGRAM']['number'],1)
        self.assertEqual(runner.report['issues_verified'],1)

    def test_json_payload_goes_to_stdin_without_shell(self):
        gh = p.GitHub(self.state, apply=True)
        payload = {'title':'literal $(command) and `backticks`','body':'line one\nline two'}
        with patch.object(p.subprocess, 'run', return_value=subprocess.CompletedProcess([],0,'{"id":1}','')) as run:
            self.assertEqual(gh.api('repos/'+p.TARGET+'/issues','POST',payload,mutation=True), {'id':1})
        args, kwargs = run.call_args
        self.assertIsInstance(args[0],list)
        self.assertNotIn('shell',kwargs)
        self.assertEqual(json.loads(kwargs['input']),payload)
        self.assertNotIn('$(command)',str(args[0]))
        self.assertNotIn('pending_action', self.state.data)

    def test_rate_limit_preserves_checkpoint_and_never_retries(self):
        gh = p.GitHub(self.state, apply=True)
        response = subprocess.CompletedProcess([],1,'{"message":"API rate limit exceeded"}','gh: HTTP 403')
        with patch.object(p.subprocess,'run',return_value=response) as run:
            with self.assertRaisesRegex(p.BootstrapError,'rate limit'):
                gh.api('repos/'+p.TARGET+'/issues','POST',{'title':'x'},mutation=True)
        self.assertEqual(run.call_count,1)
        self.assertIn('pending_action',p.read_json(self.state.path))

    def test_timeout_preserves_unknown_outcome(self):
        gh = p.GitHub(self.state,apply=True)
        with patch.object(p.subprocess,'run',side_effect=subprocess.TimeoutExpired('gh',60)) as run:
            with self.assertRaisesRegex(p.BootstrapError,'outcome may be unknown'):
                gh.api('repos/'+p.TARGET+'/issues','POST',{'title':'x'},mutation=True)
        self.assertEqual(run.call_count,1)
        self.assertIn('pending_action',self.state.data)

    def test_verify_cannot_mutate(self):
        gh = p.GitHub(self.state,apply=False)
        with patch.object(p.subprocess,'run') as run:
            with self.assertRaisesRegex(p.BootstrapError,'read-only'):
                gh.api('repos/'+p.TARGET+'/issues','POST',{},mutation=True)
        run.assert_not_called()

    def test_graphql_partial_error_keeps_pending(self):
        gh=p.GitHub(self.state,apply=True)
        response=subprocess.CompletedProcess([],0,'{"data":{"u0":{}},"errors":[{"type":"RATE_LIMITED"}]}','')
        with patch.object(p.subprocess,'run',return_value=response):
            with self.assertRaises(p.BootstrapError):gh.graphql('mutation{x}',mutation=True)
        self.assertIn('pending_action',self.state.data)

    def test_native_parent_conflict_is_never_replaced(self):
        calls=[]
        def api(endpoint,*args,**kwargs):
            calls.append((endpoint,kwargs))
            return {'id':509,'number':509} if endpoint.endswith('/509') else {'id':777,'number':777}
        gh=type('Fake',(),{'apply':True,'api':staticmethod(api)})()
        runner=self.runner(gh);runner.issue_map={'APP-PROGRAM':self.issue}
        with self.assertRaisesRegex(p.BootstrapError,'conflicting native parent'):runner.ensure_parents()
        self.assertFalse(any(c[1].get('mutation') for c in calls))

    def test_existing_project_values_are_preserved(self):
        gh=type('Fake',(),{'apply':True})()
        runner=self.runner(gh);runner.issue_map={'APP-PROGRAM':self.issue};runner.project={'id':'P1'}
        item={'id':'IT1','fieldValues':{'nodes':[{'name':'Done','field':{'name':'Status'}}]}}
        runner.items=lambda:{'I_101':item}
        runner.item_snapshot=lambda _:item
        with self.assertRaisesRegex(p.BootstrapError,'preserving live triage'):runner.ensure_items()

    def test_missing_project_values_batched_and_read_back(self):
        calls=[]
        def graphql(query,variables=None,mutation=False):
            calls.append((query,variables,mutation)); return {}
        gh=type('Fake',(),{'apply':True,'graphql':staticmethod(graphql)})()
        runner=self.runner(gh);runner.issue_map={'APP-PROGRAM':self.issue};runner.project={'id':'P1'}
        runner.field_map={'Status':{'id':'F1','options':[{'id':'O1','name':'Backlog'}]},'Priority':{'id':'F2','options':[{'id':'O2','name':'Critical'}]}}
        first={'I_101':{'id':'IT1','fieldValues':{'nodes':[]}}}
        last={'I_101':{'id':'IT1','fieldValues':{'nodes':[{'name':'Backlog','field':{'name':'Status'}},{'name':'Critical','field':{'name':'Priority'}}]}}}
        responses=iter([first,last]);runner.items=lambda:next(responses)
        runner.item_snapshot=lambda _:first['I_101']
        runner.ensure_items()
        self.assertEqual(len(calls),1)
        self.assertEqual(len(calls[0][1]),2)
        self.assertTrue(calls[0][2])
        self.assertEqual(runner.report['project_values_verified'],2)

    def test_mutation_budget_stops_without_api_call(self):
        gh=p.GitHub(self.state,apply=True,max_mutations=1);gh.mutations=1
        with patch.object(p.subprocess,'run') as run:
            with self.assertRaisesRegex(p.BootstrapError,'budget'):gh.api('graphql','POST',{},mutation=True)
        run.assert_not_called()

    def test_missing_scaffold_never_claims_delivery(self):
        runner=self.runner(type('Fake',(),{'apply':False})())
        runner.verify_scaffold(None)
        self.assertFalse(runner.report['scaffold_committed'])
        self.assertFalse(runner.report['mission_complete'])

if __name__=='__main__':unittest.main()
