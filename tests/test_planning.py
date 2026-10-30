"""Failure cases for graph integrity, truthful coverage and Project alignment."""
import copy
import importlib.util
import json
import unittest
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('planning_validator',ROOT/'scripts/validate_planning.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
render_spec=importlib.util.spec_from_file_location('backlog_renderer',ROOT/'scripts/render_backlog.py')
renderer=importlib.util.module_from_spec(render_spec); render_spec.loader.exec_module(renderer)


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.args=[json.loads((ROOT/p).read_text()) for p in ['taxonomy/taxonomy.json','coverage/ledger.json','planning/backlog.json','planning/project-config.json']]

    def reject(self, fragment):
        with self.assertRaisesRegex(ValueError,fragment): mod.validate(*self.args)

    def test_authored_plan_has_complete_distinct_hierarchy(self):
        self.assertEqual(mod.validate(*self.args)['native_relationships_internal'],134)

    def test_orphan_issue_rejected(self):
        self.args[2]['nodes'][-1]['parent_id']='APP-NOPE'; self.reject('orphan')

    def test_parent_cycle_rejected(self):
        nodes=self.args[2]['nodes']; task=next(n for n in nodes if n['kind']=='task'); parent=next(n for n in nodes if n['id']==task['parent_id']); parent['parent_id']=task['id']; self.reject('cyclic')

    def test_duplicate_checklist_identity_rejected(self):
        task=next(n for n in self.args[2]['nodes'] if n['kind']=='task'); task['subtasks'][0]['id']='APP-PROGRAM'; self.reject('duplicate delivery')

    def test_published_counts_need_prerequisites(self):
        self.args[1]['rows'][0]['published_product_count']=1; self.reject('prerequisites')

    def test_unknown_denominator_cannot_become_percentage(self):
        self.args[1]['rows'][0]['coverage_percent']=100; self.reject('without denominator')

    def test_unprovisioned_plan_cannot_claim_github_success(self):
        self.args[2]['nodes'][0]['github']['native_parent_verified']=True; self.reject('asserts live')

    def test_project_value_must_exist(self):
        self.args[2]['nodes'][0]['status']='Complete'; self.reject('Project options')

    def test_coverage_boolean_is_not_numeric_count(self):
        self.args[1]['rows'][0]['candidate_sightings_count']=True; self.reject('nonnegative integers')

    def test_unsafe_deliverable_path_rejected(self):
        self.args[2]['nodes'][0]['deliverable_paths']=['../secret']; self.reject('unsafe')

    def test_taxonomy_orphan_rejected(self):
        self.args[0]['categories'][0]['group_id']='missing'; self.reject('orphan category')

    def test_regeneration_preserves_partial_provisioning(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'.bootstrap-state.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'provisioning state exists'): renderer.guard_regeneration(root)

    def test_regeneration_preserves_live_issue_identifiers(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'planning').mkdir()
            self.args[2]['nodes'][0]['github']['number']=1
            (root/'planning/backlog.json').write_text(json.dumps(self.args[2]))
            with self.assertRaisesRegex(ValueError,'live GitHub state exists'): renderer.guard_regeneration(root)


if __name__=='__main__': unittest.main()
