"""APP-F02.01 identity invariants (#96, #97). Every record and decision here is synthetic.

The cases follow research/foundations/application-identity.md. They never fetch a
source, create a real application or stand for a real identity decision.
"""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
AS_OF = dt.date(2026, 11, 17)
spec = importlib.util.spec_from_file_location('identity_applications', ROOT / 'scripts' / 'validate_applications.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
REVIEW = {'researcher': 'synthetic-researcher', 'reviewer': 'synthetic-reviewer', 'reviewed_on': '2026-11-17',
          'decision_url': 'https://github.com/Pick-Your-AI/synthetic-test-only/pull/1'}


def product(slug, name, aliases=()):
    """A real-intake-shaped synthetic record, valid only inside a temporary directory."""
    record = json.loads((ROOT / 'tests/fixtures/synthetic_checked.json').read_text())
    record['synthetic'] = False
    record['record_id'] = record['identity']['product_id'] = 'app:synthetic-' + slug
    record['claims'][0]['subject']['id'] = record['record_id']
    record['identity'].update(name=name, aliases=list(aliases), canonical_url='https://github.com/Pick-Your-AI/synthetic-test-only/' + slug)
    record['sources'][0]['url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/blob/main/docs.md'
    record['claims'][0]['review']['decision_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/pull/1'
    record['rights_decisions'][0]['decision_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/issues/1'
    return record


def merged(retired, survivor, **overrides):
    return {'decision': 'merged', 'retired_product_ids': retired, 'surviving_product_id': survivor, **REVIEW, **overrides}


def split(retired, successors, **overrides):
    return {'decision': 'split', 'retired_product_id': retired, 'successor_product_ids': successors, **REVIEW, **overrides}


def directory_errors(records, decisions=None):
    with tempfile.TemporaryDirectory() as d:
        for i, record in enumerate(records):
            (Path(d) / f'{i}.json').write_text(json.dumps(record))
        return v.validate_directory(Path(d), as_of=AS_OF, identity_resolutions=decisions)[1]


class RecordIdentityTests(unittest.TestCase):
    def errors(self, record):
        return v.validate_record(record, as_of=AS_OF)

    def test_rename_keeps_one_product_and_the_old_name_as_alias(self):
        self.assertEqual([], self.errors(product('renamed', 'Synthetic New Name', ['Synthetic Old Name'])))

    def test_alias_repeating_the_name_is_inconsistent(self):
        errors = self.errors(product('a', 'Synthetic Alpha', [' SYNTHETIC  alpha ']))
        self.assertTrue(any('must not repeat the product name' in e for e in errors), errors)

    def test_aliases_differing_only_by_case_or_spacing_are_one_alias(self):
        errors = self.errors(product('a', 'Synthetic Alpha', ['Old Alpha', 'old  ALPHA']))
        self.assertTrue(any('distinct after normalization' in e for e in errors), errors)

    def test_aliases_differing_only_by_invisible_characters_are_one_alias(self):
        errors = self.errors(product('a', 'Synthetic Alpha', ['Old Alpha', 'Old​ Alpha']))
        self.assertTrue(any('distinct after normalization' in e for e in errors), errors)

    def test_unknown_operator_is_not_given_a_placeholder_vendor(self):
        cases = (('vendor:unknown', 'Synthetic Vendor'), ('vendor:synthetic', ' Unknown '), ('vendor:n-a', 'Synthetic Vendor'),
                 ('vendor:tbd', 'Synthetic Vendor'), ('vendor:synthetic', 'Undisclosed'), ('vendor:unknown_vendor', 'Synthetic Vendor'),
                 ('vendor:synthetic', 'N.A.'), ('vendor:synthetic', 'Unknown.'), ('vendor:synthetic', '?'), ('vendor:synthetic', 'Unknown Vendor'))
        for vendor_id, vendor_name in cases:
            with self.subTest(vendor_id=vendor_id, vendor_name=vendor_name):
                record = product('a', 'Synthetic Alpha')
                record['identity'].update(vendor_id=vendor_id, vendor_name=vendor_name)
                errors = self.errors(record)
                self.assertTrue(any('operator is unknown' in e for e in errors), errors)

    def test_named_operator_is_accepted(self):
        record = product('a', 'Synthetic Alpha')
        record['identity'].update(vendor_id='vendor:synthetic-unknownish-labs', vendor_name='Synthetic Unknownish Labs')
        self.assertEqual([], self.errors(record))


class DirectoryIdentityTests(unittest.TestCase):
    def test_duplicate_canonical_product_id_is_rejected(self):
        a = product('a', 'Synthetic Alpha')
        b = copy.deepcopy(a); b['identity'].update(name='Synthetic Beta', canonical_url=a['identity']['canonical_url'] + '-b')
        self.assertTrue(any('duplicate product identity' in e for e in directory_errors([a, b])))

    def test_alias_shared_with_another_product_needs_a_reviewed_decision(self):
        a, b = product('a', 'Synthetic Alpha', ['Synthetic Shared']), product('b', 'Synthetic Beta', ['synthetic shared'])
        self.assertTrue(any('name/alias collision' in e for e in directory_errors([a, b])))

    def test_same_name_distinct_products_keep_the_existing_decision_shape(self):
        a, b = product('a', 'Synthetic Same'), product('b', 'Synthetic Same')
        decision = {'decision': 'distinct_products', 'normalized_name': 'synthetic same',
                    'product_ids': ['app:synthetic-a', 'app:synthetic-b'], **REVIEW}
        self.assertEqual([], directory_errors([a, b], [decision]))

    def test_merge_retires_duplicates_into_a_live_survivor(self):
        survivor = product('survivor', 'Synthetic Survivor', ['Synthetic Duplicate'])
        self.assertEqual([], directory_errors([survivor], [merged(['app:synthetic-duplicate'], 'app:synthetic-survivor')]))

    def test_merged_id_cannot_stay_live_or_be_reused(self):
        survivor, duplicate = product('survivor', 'Synthetic Survivor'), product('duplicate', 'Synthetic Duplicate')
        errors = directory_errors([survivor, duplicate], [merged(['app:synthetic-duplicate'], 'app:synthetic-survivor')])
        self.assertTrue(any('still a live record' in e for e in errors), errors)

    def test_merge_survivor_must_be_live(self):
        errors = directory_errors([product('other', 'Synthetic Other')], [merged(['app:synthetic-duplicate'], 'app:synthetic-missing')])
        self.assertTrue(any('not a live record' in e for e in errors), errors)

    def test_merge_into_itself_is_rejected(self):
        survivor = product('survivor', 'Synthetic Survivor')
        errors = directory_errors([survivor], [merged(['app:synthetic-survivor'], 'app:synthetic-survivor')])
        self.assertTrue(any('into itself' in e for e in errors), errors)

    def test_split_retires_one_id_into_several_live_products(self):
        records = [product('editor', 'Synthetic Editor'), product('viewer', 'Synthetic Viewer')]
        self.assertEqual([], directory_errors(records, [split('app:synthetic-suite', ['app:synthetic-editor', 'app:synthetic-viewer'])]))

    def test_split_needs_two_live_successors(self):
        records = [product('editor', 'Synthetic Editor')]
        for successors in (['app:synthetic-editor'], ['app:synthetic-editor', 'app:synthetic-missing']):
            with self.subTest(successors=successors):
                self.assertTrue(directory_errors(records, [split('app:synthetic-suite', successors)]))

    def test_id_retired_twice_is_rejected(self):
        records = [product('a', 'Synthetic Alpha'), product('b', 'Synthetic Beta')]
        decisions = [merged(['app:synthetic-old'], 'app:synthetic-a'), merged(['app:synthetic-old'], 'app:synthetic-b')]
        self.assertTrue(any('more than one identity decision' in e for e in directory_errors(records, decisions)))

    def test_id_listed_twice_in_one_merge_is_not_reported_as_two_decisions(self):
        errors = directory_errors([product('a', 'Synthetic Alpha')], [merged(['app:synthetic-old', 'app:synthetic-old'], 'app:synthetic-a')])
        self.assertTrue(any('duplicate array items' in e for e in errors), errors)
        self.assertFalse(any('more than one identity decision' in e for e in errors), errors)

    def test_chained_changes_resolve_through_history(self):
        records = [product('c', 'Synthetic Gamma')]
        decisions = [merged(['app:synthetic-a'], 'app:synthetic-b'), merged(['app:synthetic-b'], 'app:synthetic-c')]
        self.assertEqual([], directory_errors(records, decisions))

    def test_cyclic_changes_are_rejected(self):
        records = [product('c', 'Synthetic Gamma')]
        decisions = [merged(['app:synthetic-a'], 'app:synthetic-b'), merged(['app:synthetic-b'], 'app:synthetic-a')]
        self.assertTrue(any('cycle' in e for e in directory_errors(records, decisions)))

    def test_change_needs_independent_dated_review(self):
        survivor = product('survivor', 'Synthetic Survivor')
        for key, value in (('reviewer', ' SYNTHETIC-RESEARCHER '), ('reviewed_on', '2026-02-30'), ('reviewed_on', '2099-01-01'),
                           ('decision_url', 'http://localhost./x'), ('reviewer', '')):
            with self.subTest(key=key, value=value):
                self.assertTrue(directory_errors([survivor], [merged(['app:synthetic-old'], 'app:synthetic-survivor', **{key: value})]))

    def test_malformed_change_reports_errors_instead_of_crashing(self):
        survivor = product('survivor', 'Synthetic Survivor')
        cases = ({'decision': 'merged'}, merged('app:synthetic-old', 'app:synthetic-survivor'), merged([], 'app:synthetic-survivor'),
                 merged(['family:synthetic'], 'app:synthetic-survivor'), merged(['app:synthetic-old'], None),
                 split('app:synthetic-old', 'app:synthetic-survivor'), merged(['app:synthetic-old'], 'app:synthetic-survivor', note='x'),
                 {'decision': 'renamed'}, {'decision': []}, {'decision': {}}, 'merged', None)
        for decision in cases:
            with self.subTest(decision=decision):
                self.assertTrue(directory_errors([survivor], [decision]))


class IdentitySchemaTests(unittest.TestCase):
    def test_identity_schema_uses_only_the_supported_vocabulary(self):
        self.assertEqual([], v.check_schema_vocabulary(v.load_json(ROOT / 'schemas/application-identity.schema.json')))


if __name__ == '__main__':
    unittest.main()
