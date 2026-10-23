"""Regression cases for PR #136: all records/receipts here are synthetic test data.

These tests never fetch a source, create a real application, or certify a receipt.
"""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
AS_OF = dt.date(2026, 10, 22)


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v = load_module('regression_applications', 'validate_applications.py')
p = load_module('regression_planning', 'validate_planning.py')
r = load_module('regression_renderer', 'render_backlog.py')
b = load_module('regression_provisioner', 'provision_github.py')


def fixture():
    return json.loads((ROOT / 'tests/fixtures/synthetic_checked.json').read_text())


def intake_fixture():
    """Exercise the real-intake code path ONLY in isolated temporary directories."""
    record = fixture()
    record['synthetic'] = False
    record['identity']['canonical_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only'
    record['sources'][0]['url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/blob/main/docs.md'
    record['claims'][0]['review']['decision_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/pull/1'
    record['rights_decisions'][0]['decision_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/issues/1'
    return record


def price_fixture(real_intake=False):
    app = intake_fixture() if real_intake else fixture()
    offering = 'offering:synthetic-standard'
    app['entities'].append({'id': offering, 'entity_type': 'application_offering', 'name': 'Synthetic plan',
                            'product_id': app['record_id'], 'version': None, 'url': None})
    claim = app['claims'][0]
    claim.update(fact_type='pricing', field='pricing.standard', subject={'id': offering, 'entity_type': 'application_offering'})
    claim['value'] = {'offering_id': offering, 'plan_name': 'Synthetic plan', 'amount_status': 'known',
                      'amount': '0', 'currency': 'USD', 'regions': ['US'], 'billing_period': 'month',
                      'meter': 'seat-month', 'commitment': 'monthly', 'tax_treatment': 'unknown',
                      'minimum_seats': 1, 'included_allowance': None, 'overage_terms': None,
                      'promotion_conditions': None, 'effective_on': '2026-10-21'}
    app['rights_decisions'][0]['fields'] = ['pricing.standard']
    price = {'schema_version': '0.1.0', 'record_id': 'price:synthetic-20261021', 'entity_type': 'application_price',
             'synthetic': app['synthetic'], 'application_id': app['record_id'], 'offering_id': offering,
             'sources': copy.deepcopy(app['sources']), 'claim': copy.deepcopy(claim),
             'rights_decisions': copy.deepcopy(app['rights_decisions']), 'publication': copy.deepcopy(app['publication']),
             'known_unknowns': [], 'research_notes': ['Synthetic temporary test; no actual price or receipt.']}
    return app, price


class ClaimIntegrityTests(unittest.TestCase):
    def check(self, record):
        return v.validate_record(record, as_of=AS_OF, allow_synthetic=True)

    def rejected(self, record, fragment):
        errors = self.check(record)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_scoped_offering_must_exist_and_have_offering_type(self):
        for offering in ('offering:invented', 'vendor:synthetic', 'app:synthetic-not-a-product'):
            with self.subTest(offering=offering):
                record = fixture(); record['claims'][0]['scope']['offering_id'] = offering
                self.rejected(record, 'scoped offering_id must resolve')

    def test_registered_offer_and_null_scope_remain_valid(self):
        record = fixture(); self.assertEqual([], self.check(record))
        app, _ = price_fixture(); app['claims'][0]['scope']['offering_id'] = app['entities'][0]['id']
        self.assertEqual([], self.check(app))

    def test_scoped_offer_cannot_belong_to_another_product(self):
        app, _ = price_fixture(); app['entities'][0]['product_id'] = 'app:other'
        app['claims'][0]['scope']['offering_id'] = app['entities'][0]['id']
        self.rejected(app, 'must identify this product')

    def test_price_subject_value_and_scope_must_agree(self):
        app, _ = price_fixture()
        second = copy.deepcopy(app['entities'][0]); second['id'] = 'offering:other'; app['entities'].append(second)
        app['claims'][0]['scope']['offering_id'] = second['id']
        self.rejected(app, 'must agree')

    def test_casing_whitespace_and_handle_prefix_cannot_self_approve(self):
        for reviewer in ('SYNTHETIC-RESEARCHER', ' synthetic-researcher ', '@Synthetic-Researcher', '\u3000SYNTHETIC-RESEARCHER\u3000', '  '):
            with self.subTest(reviewer=reviewer):
                record = fixture(); record['claims'][0]['review']['reviewer'] = reviewer
                self.rejected(record, 'reviewer other than its researcher')

    def test_invisible_format_characters_cannot_self_approve(self):
        for reviewer in ('synthetic-researcher\u200b', '\u200bSYNTHETIC-RESEARCHER', 'synthetic-\u00adresearcher',
                         'synthetic\u2060-researcher', 'synthetic-researcher\ufeff', '\u200b'):
            with self.subTest(reviewer=repr(reviewer)):
                record = fixture(); record['claims'][0]['review']['reviewer'] = reviewer
                self.assertTrue(self.check(record), 'invisible characters admitted a self-approval')

    def test_invisible_format_characters_cannot_fake_independent_verifier(self):
        for verifier in ('synthetic-researcher\u200b', 'synthetic\u2060vendor'.replace('\u2060', '\u2060 ')):
            with self.subTest(verifier=repr(verifier)):
                record = self.verified(); record['claims'][0]['verification']['verifier'] = verifier
                self.rejected(record, 'independent of')

    def test_blank_researcher_is_rejected(self):
        record = fixture(); record['claims'][0]['researcher'] = '  '
        self.rejected(record, 'researcher must not be blank')

    def verified(self):
        record = fixture(); claim = record['claims'][0]
        claim['verification_status'] = 'verified'
        claim['verification'] = {'method': 'reproduced_test', 'independent': True, 'verifier': 'synthetic-verifier',
                                 'verified_on': '2026-10-22', 'receipt_url': 'https://review.example.invalid/test/1',
                                 'protocol_version': 'synthetic-protocol@1', 'source_id': None, 'limitations': 'Synthetic test only.'}
        record['publication']['fields'][0]['display_verification_status'] = 'verified'
        return record

    def test_verifier_identity_is_normalized_against_researcher_and_vendor(self):
        for verifier in (' SYNTHETIC-RESEARCHER ', '@synthetic-researcher', ' SYNTHETIC VENDOR ', '  '):
            with self.subTest(verifier=verifier):
                record = self.verified(); record['claims'][0]['verification']['verifier'] = verifier
                self.rejected(record, 'independent of')

    def test_independent_measurement_cannot_relabel_vendor_documentation(self):
        record = fixture(); record['claims'][0]['evidence_grade'] = 'independent_measurement'
        record['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
        self.rejected(record, 'independent_measurement requires')

    def test_pinned_independent_measurement_receipt_is_structurally_valid(self):
        record = self.verified(); record['claims'][0]['evidence_grade'] = 'independent_measurement'
        record['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
        self.assertEqual([], self.check(record))
        record['claims'][0]['verification']['protocol_version'] = None
        self.rejected(record, 'pinned protocol')
        for method_and_limitations in ('   ', '\u200b'):
            with self.subTest(method_and_limitations=repr(method_and_limitations)):
                record = self.verified(); record['claims'][0]['evidence_grade'] = 'independent_measurement'
                record['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
                record['claims'][0]['method_and_limitations'] = method_and_limitations
                self.rejected(record, 'independent_measurement requires method and limitations')

    def test_reproduced_test_requires_substantive_protocol_version(self):
        valid = self.verified(); valid['claims'][0]['evidence_grade'] = 'independent_measurement'
        valid['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
        self.assertEqual([], self.check(valid))
        for protocol_version in ('   ', '\u200b'):
            with self.subTest(protocol_version=repr(protocol_version)):
                record = self.verified(); record['claims'][0]['evidence_grade'] = 'independent_measurement'
                record['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
                record['claims'][0]['verification']['protocol_version'] = protocol_version
                self.rejected(record, 'pinned protocol')

    def test_version_pinned_claim_requires_substantive_version(self):
        valid = fixture(); valid['claims'][0].update(temporal_scope='version_pinned', version='synthetic-app 2.1')
        self.assertEqual([], self.check(valid))
        for version in ('   ', '\u200b'):
            with self.subTest(version=repr(version)):
                record = copy.deepcopy(valid); record['claims'][0]['version'] = version
                self.rejected(record, 'version-pinned facts need a concrete version')

    def test_verification_receipt_requires_substantive_limitations(self):
        valid = self.verified(); valid['claims'][0]['evidence_grade'] = 'independent_measurement'
        valid['publication']['fields'][0]['display_evidence_grade'] = 'independent_measurement'
        self.assertEqual([], self.check(valid))
        for limitations in ('   ', '\u200b'):
            with self.subTest(limitations=repr(limitations)):
                record = copy.deepcopy(valid); record['claims'][0]['verification']['limitations'] = limitations
                self.rejected(record, 'verification receipts require their limitations')

    def test_allowed_rights_review_requires_substantive_reviewer(self):
        self.assertEqual([], self.check(fixture()))
        for reviewer in ('   ', '\u200b'):
            with self.subTest(reviewer=repr(reviewer)):
                record = fixture(); record['rights_decisions'][0]['reviewer'] = reviewer
                self.rejected(record, 'allowed source use requires reviewer and decision receipt')

    def test_estimate_requires_substantive_method_and_limitations(self):
        valid = fixture(); valid['claims'][0]['evidence_grade'] = 'estimate'
        valid['claims'][0]['method_and_limitations'] = 'Synthetic estimate assumes monthly usage and excludes taxes.'
        valid['publication']['fields'][0]['display_evidence_grade'] = 'estimate'
        self.assertEqual([], self.check(valid))
        for method_and_limitations in ('   ', '\u200b'):
            with self.subTest(method_and_limitations=repr(method_and_limitations)):
                record = copy.deepcopy(valid)
                record['claims'][0]['method_and_limitations'] = method_and_limitations
                self.rejected(record, 'estimates require method, assumptions and limitations')

    def test_pending_and_rejected_review_dates_are_validated(self):
        for status in ('pending', 'rejected'):
            for date in ('2026-02-30', '2026-10-23', '20261022'):
                with self.subTest(status=status, date=date):
                    record = fixture(); record['publication']['state'] = 'notes'; record['publication']['fields'] = []
                    record['claims'][0]['review'].update(status=status, reviewed_on=date)
                    self.assertTrue(self.check(record))

    def test_independent_source_cannot_be_the_vendor_with_a_new_label(self):
        record = self.verified(); claim = record['claims'][0]
        source = copy.deepcopy(record['sources'][0]); source.update(id='source:second', authority='independent', publisher=' SYNTHETIC VENDOR ')
        record['sources'].append(source); claim['source_ids'].append(source['id'])
        claim['verification'].update(method='independent_second_source', source_id=source['id'])
        record['publication'].update(state='notes', fields=[])
        self.rejected(record, 'independent source publisher')
        source['publisher'] = 'Synthetic Independent Lab'; self.assertEqual([], self.check(record))

    def test_null_pending_review_date_remains_valid(self):
        record = fixture(); record['publication']['state'] = 'notes'; record['publication']['fields'] = []
        record['claims'][0]['review'].update(status='pending', reviewer=None, reviewed_on=None, decision_url=None)
        self.assertEqual([], self.check(record))

    def test_unsupported_requires_boolean_false_not_just_negative_flag(self):
        for value in (True, 0, 1, 'false', {}, []):
            with self.subTest(value=value):
                record = fixture(); record['claims'][0].update(value_status='unsupported', value=value, explicit_negative_evidence=True)
                self.rejected(record, 'explicit JSON false')

    def test_explicit_sourced_negative_is_valid(self):
        record = fixture(); record['claims'][0].update(value_status='unsupported', value=False, explicit_negative_evidence=True)
        self.assertEqual([], self.check(record))

    def test_relationship_verbs_enforce_target_types(self):
        allowed = {'renamed_from': {'application_product'}, 'replaces': {'application_product'},
                   'replaced_by': {'application_product'}, 'fork_of': {'application_product'},
                   'discontinued_successor': {'application_product'}, 'member_of': {'product_family'},
                   'sold_by': {'vendor'}, 'uses_model': {'model'}, 'integrates_with': {'integration', 'application_product'}}
        for relation, targets in allowed.items():
            for kind, prefix in v.PREFIXES.items():
                with self.subTest(relation=relation, kind=kind):
                    record = fixture(); record['relationships'] = [{'relation': relation, 'target_entity_type': kind,
                        'target_id': prefix+'external', 'claim_ids': ['claim:capability']}]
                    errors = self.check(record)
                    if kind in targets: self.assertEqual([], errors)
                    else: self.assertTrue(any('invalid for relationship' in e for e in errors), errors)

    def test_noncanonical_local_and_numeric_urls_are_rejected(self):
        urls = ('http://localhost./x', 'http://LOCALHOST../x', 'http://2130706433/x', 'http://0x7f000001/x',
                'http://017700000001/x', 'http://127.1/x', 'http://127.000.000.001/x', 'http://0x7f.1/x',
                'http://[::ffff:127.0.0.1]/x', 'http://[::1]/x', 'http://host.local/x', 'http://intranet/x',
                'http://%6cocalhost/x', 'http://\uff4c\uff4f\uff43\uff41\uff4c\uff48\uff4f\uff53\uff54./x',
                ' https://github.com/x', 'https://github.com:99999/x', 'https://github.com\\@localhost/x')
        for url in urls:
            with self.subTest(url=url):
                errors = []; v.url_errors(url, 'source', errors, synthetic=True)
                self.assertTrue(errors)

    def test_public_locators_and_synthetic_only_reserved_hosts(self):
        for url in ('https://github.com/Pick-Your-AI/pick-your-ai-applications', 'https://github.com./x', 'https://8.8.8.8/x', 'https://[2606:4700:4700::1111]/x'):
            with self.subTest(url=url):
                errors = []; v.url_errors(url, 'source', errors); self.assertEqual([], errors)
        errors = []; v.url_errors('https://docs.example.invalid/x', 'source', errors); self.assertTrue(errors)
        errors = []; v.url_errors('https://docs.example.invalid/x', 'source', errors, synthetic=True); self.assertEqual([], errors)


class IntakeIntegrityTests(unittest.TestCase):
    def test_duplicate_keys_rejected_at_every_nesting_level(self):
        for text in ('{"publication":{},"publication":{}}', '{"claim":{"state":1,"state":2}}', '{"state":1,"sta\\u0074e":2}'):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as d:
                file = Path(d)/'test.json'; file.write_text(text)
                with self.assertRaisesRegex(ValueError, 'duplicate JSON'): v.load_json(file)

    def test_non_json_numbers_rejected_before_gates(self):
        for value in ('NaN', 'Infinity', '-Infinity', '1e999'):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as d:
                file = Path(d)/'test.json'; file.write_text('{"value":'+value+'}')
                with self.assertRaisesRegex(ValueError, 'non-finite'): v.load_json(file)

    def test_both_intake_directories_use_strict_loading(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d)/'test.json'; file.write_text('{"state":"first","state":"last"}')
            _, app_errors = v.validate_directory(Path(d), as_of=AS_OF)
            _, price_errors = v.validate_pricing_directory(Path(d), {}, as_of=AS_OF)
            self.assertTrue(any('duplicate JSON' in e for e in app_errors), app_errors)
            self.assertTrue(any('duplicate JSON' in e for e in price_errors), price_errors)

    def test_standalone_price_cannot_duplicate_parent_claim(self):
        app, price = price_fixture()
        errors = v.validate_pricing_record(price, {app['record_id']: app}, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any('duplicates a claim embedded' in e for e in errors), errors)
        price['claim']['id'] = 'claim:renamed-copy'; price['publication']['fields'][0]['claim_id'] = 'claim:renamed-copy'
        errors = v.validate_pricing_record(price, {app['record_id']: app}, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any('duplicates a claim embedded' in e for e in errors), errors)

    def test_nonduplicated_standalone_price_remains_valid(self):
        app, price = price_fixture(); app['claims'] = []; app['publication'].update(state='notes', fields=[])
        self.assertEqual([], v.validate_pricing_record(price, {app['record_id']: app}, as_of=AS_OF, allow_synthetic=True))

    def test_renamed_price_files_cannot_double_count_observation(self):
        app, price = price_fixture(real_intake=True); app['claims'] = []; app['publication'].update(state='notes', fields=[])
        other = copy.deepcopy(price); other['record_id'] = 'price:renamed-copy'; other['claim']['id'] = 'claim:renamed-copy'
        other['publication']['fields'][0]['claim_id'] = 'claim:renamed-copy'
        with tempfile.TemporaryDirectory() as d:
            for i, record in enumerate((price, other)): (Path(d)/f'{i}.json').write_text(json.dumps(record))
            _, errors = v.validate_pricing_directory(Path(d), {app['record_id']: app}, as_of=AS_OF)
            self.assertTrue(any('duplicate standalone' in e for e in errors), errors)

    def pair(self):
        a = intake_fixture(); a['identity']['name'] = 'Synthetic Alpha'; a['identity']['aliases'] = ['Previous Name']
        z = copy.deepcopy(a); z['record_id'] = z['identity']['product_id'] = 'app:synthetic-other'
        z['claims'][0]['subject']['id'] = z['record_id']; z['identity']['canonical_url'] += '-other'
        z['identity'].update(name='Synthetic Beta', aliases=[' PREVIOUS  NAME '])
        return a, z

    def directory_check(self, records, **kwargs):
        with tempfile.TemporaryDirectory() as d:
            for i, record in enumerate(records): (Path(d)/f'{i}.json').write_text(json.dumps(record))
            return v.validate_directory(Path(d), as_of=AS_OF, **kwargs)[1]

    def test_unresolved_cross_record_alias_collision_rejected(self):
        self.assertTrue(any('name/alias collision' in e for e in self.directory_check(self.pair())))

    def resolution(self, records):
        return {'normalized_name': 'previous name', 'product_ids': [x['record_id'] for x in records],
                'decision': 'distinct_products', 'researcher': 'synthetic-researcher', 'reviewer': 'synthetic-reviewer',
                'reviewed_on': '2026-10-22', 'decision_url': 'https://github.com/Pick-Your-AI/synthetic-test-only/pull/1'}

    def test_reviewed_distinct_products_can_share_a_name(self):
        records = self.pair()
        self.assertEqual([], self.directory_check(records, identity_resolutions=[self.resolution(records)]))

    def test_collision_resolution_cannot_use_self_review_or_partial_scope(self):
        records = self.pair()
        for key, value in (('reviewer', ' SYNTHETIC-RESEARCHER '), ('product_ids', ['app:synthetic-other']), ('reviewed_on', '2026-02-30'), ('decision_url', 'http://localhost./x')):
            with self.subTest(key=key):
                resolution = self.resolution(records); resolution[key] = value
                self.assertTrue(self.directory_check(records, identity_resolutions=[resolution]))

    def test_malformed_collision_resolution_reports_errors_instead_of_crashing(self):
        records = self.pair()
        for value in (None, [], {}, '', ' Wrong Case '):
            with self.subTest(value=value):
                resolution = self.resolution(records); resolution['normalized_name'] = value
                self.assertTrue(self.directory_check(records, identity_resolutions=[resolution]))

    def test_distinct_names_without_collision_need_no_resolution(self):
        a, z = self.pair(); z['identity']['aliases'] = []
        self.assertEqual([], self.directory_check((a, z)))


class PlanningIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.row = json.loads((ROOT/'coverage/ledger.json').read_text())['rows'][0]

    def receipt(self):
        return {'receipt_url': 'https://github.com/Pick-Your-AI/synthetic-test-only/pull/1',
                'artifact_commit': 'a'*40, 'consumer_commit': 'b'*40,
                'product_ids': ['app:synthetic-one'], 'category_id': self.row['category_id'],
                'reviewer': 'synthetic-reviewer', 'accepted_on': '2026-10-22'}

    def test_published_count_rejects_truthy_non_receipts(self):
        self.row['published_product_count'] = 1
        for receipts in ([''], ['not a receipt'], ['https://github.com/x/y/pull/1'], [None], [{}], 'text'):
            with self.subTest(receipts=receipts):
                self.row['acceptance_receipts'] = receipts
                with self.assertRaises(ValueError): p.validate_coverage_receipts(self.row, AS_OF)

    def test_published_count_must_match_distinct_receipt_products(self):
        self.row.update(published_product_count=2, acceptance_receipts=[self.receipt()])
        with self.assertRaisesRegex(ValueError, 'distinct products'): p.validate_coverage_receipts(self.row, AS_OF)
        self.row['published_product_count'] = 1; p.validate_coverage_receipts(self.row, AS_OF)

    def test_receipt_fields_cannot_be_blank_unscoped_or_unpinned(self):
        self.row['published_product_count'] = 1
        for key, value in (('category_id', 'APP-C99'), ('artifact_commit', 'main'), ('consumer_commit', ''),
                           ('reviewer', '  '), ('accepted_on', '2026-02-30'), ('accepted_on', '2026-10-23'),
                           ('receipt_url', 'https://example.com'), ('receipt_url', 'https://github.com/x/y'),
                           ('receipt_url', 'http://localhost/x'), ('receipt_url', ' https://github.com/x/y/pull/1'), ('product_ids', ['app:synthetic-one', 'app:synthetic-one'])):
            with self.subTest(key=key, value=value):
                receipt = self.receipt(); receipt[key] = value; self.row['acceptance_receipts'] = [receipt]
                with self.assertRaises(ValueError): p.validate_coverage_receipts(self.row, AS_OF)

    def test_immutable_receipt_url_is_accepted(self):
        receipt = self.receipt(); receipt['receipt_url'] = 'https://github.com/Pick-Your-AI/synthetic-test-only/blob/'+'a'*40+'/receipt.json'
        self.row.update(published_product_count=1, acceptance_receipts=[receipt]); p.validate_coverage_receipts(self.row, AS_OF)

    def bounded_row(self):
        self.row['survey_scope'].update(source_sets=['synthetic bounded set'], cutoff_date='2026-10-21', denominator_definition='Two enumerated synthetic product IDs')
        self.row.update(deduplicated_product_count=1, coverage_basis={'numerator_product_ids': ['app:one'], 'denominator_product_ids': ['app:one', 'app:two']}, coverage_percent=50)
        return self.row

    def test_coverage_percent_requires_numeric_finite_in_range(self):
        row = self.bounded_row()
        for value in (-1, 1000, True, '50', None, float('nan'), float('inf')):
            with self.subTest(value=value):
                row['coverage_percent'] = value
                with self.assertRaisesRegex(ValueError, 'finite number'): p.validate_coverage_percentages(row, AS_OF)

    def test_sources_alone_are_not_a_percentage_denominator(self):
        self.row['survey_scope']['source_sets'] = ['a source']; self.row['coverage_percent'] = 100
        with self.assertRaisesRegex(ValueError, 'without denominator'): p.validate_coverage_percentages(self.row, AS_OF)

    def test_percentage_is_recomputed_from_dated_enumerated_scope(self):
        row = self.bounded_row(); p.validate_coverage_percentages(row, AS_OF)
        row['coverage_percent'] = 51
        with self.assertRaisesRegex(ValueError, 'disagrees'): p.validate_coverage_percentages(row, AS_OF)
        row['coverage_percent'] = 50; row['survey_scope']['cutoff_date'] = None
        with self.assertRaisesRegex(ValueError, 'cutoff date'): p.validate_coverage_percentages(row, AS_OF)

    def test_invalid_denominator_membership_and_duplicate_ids_rejected(self):
        row = self.bounded_row(); row['coverage_basis']['numerator_product_ids'] = ['app:outside']
        with self.assertRaisesRegex(ValueError, 'numerator'): p.validate_coverage_percentages(row, AS_OF)
        row = self.bounded_row(); row['coverage_basis']['denominator_product_ids'] = ['app:one', 'app:one']
        with self.assertRaisesRegex(ValueError, 'unique canonical'): p.validate_coverage_percentages(row, AS_OF)

    def test_all_percentage_aliases_use_the_same_bounds(self):
        for key in ('coverage_percent', 'coverage_percentage', 'market_coverage_percent'):
            with self.subTest(key=key):
                row = self.bounded_row(); del row['coverage_percent']; row[key] = -1
                with self.assertRaisesRegex(ValueError, 'finite number'): p.validate_coverage_percentages(row, AS_OF)

    def test_external_checkpoint_blocks_regeneration(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'repo'; root.mkdir(); external = Path(d)/'custom-state.json'; external.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'provisioning state exists'): r.guard_regeneration(root, [external])

    def test_root_marker_preserves_custom_checkpoint_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); b.mark_live_plan(root); b.mark_live_plan(root)
            self.assertEqual(b.TARGET, json.loads((root/'.bootstrap-started.json').read_text())['target'])
            with self.assertRaisesRegex(ValueError, 'provisioning state exists'): r.guard_regeneration(root)

    def test_existing_remote_receipt_blocks_regeneration_without_checkpoint(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'planning').mkdir(); (root/'planning/GITHUB_ESTABLISHMENT_RECEIPT.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'live GitHub state'): r.guard_regeneration(root)

    def test_clean_unprovisioned_root_can_render(self):
        with tempfile.TemporaryDirectory() as d: r.guard_regeneration(Path(d))

    def test_wrong_repository_marker_is_preserved_and_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); marker = root/'.bootstrap-started.json'; marker.write_text('{"target":"other/repo"}')
            before = marker.read_bytes()
            with self.assertRaises(b.BootstrapError): b.mark_live_plan(root)
            self.assertEqual(before, marker.read_bytes())


if __name__ == '__main__': unittest.main()
