"""Structural checks for planning/handoffs.json, the receiving-handoff ledger (docs/OWNERSHIP_HANDOFFS.md).

These check the ledger's shape, its pending-by-default rules and the shape of a recorded decision. They do not read
GitHub, so they cannot confirm a consumer, a reviewer's authority or a decision.
"""
import datetime as dt
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / 'planning/handoffs.json').read_text(encoding='utf-8'))
REPO = re.compile(r'Pick-Your-AI/[A-Za-z0-9_.-]+')
COMMIT = re.compile(r'[0-9a-f]{40}')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
DECISIONS = ('pending', 'accepted', 'accepted_with_conditions', 'rejected')
# A GitHub login: letters, digits and single hyphens, at most 39 characters.
LOGIN = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}')
# A GitHub issue or pull-request decision, or an immutable blob; a general webpage is not a receipt.
DECISION_URL = re.compile(
    r'https://github\.com/(Pick-Your-AI/[A-Za-z0-9_.-]+)/(?:'
    r'(?:issues|pull)/\d+(?:#(?:issuecomment|pullrequestreview|discussion_r)-?\d+)?'
    r'|blob/[0-9a-f]{40}/[^\s#?]+)')


class HandoffLedgerTests(unittest.TestCase):
    def test_every_entry_has_exactly_the_declared_fields(self):
        fields = set(LEDGER['entry_fields'])
        for entry in LEDGER['handoffs']:
            self.assertEqual(set(entry), fields, entry['id'])

    def test_ids_are_unique_and_ordered(self):
        ids = [entry['id'] for entry in LEDGER['handoffs']]
        self.assertEqual(ids, [f'H{n:02d}' for n in range(1, len(ids) + 1)])

    def test_one_consumer_per_entry_with_a_dated_readback(self):
        for entry in LEDGER['handoffs']:
            consumer = entry['consumer']
            self.assertRegex(consumer['repository'], REPO, entry['id'])
            self.assertIsInstance(consumer['issue'], int, entry['id'])
            self.assertIn(entry['consumer_status'], ('confirmed', 'unresolved'), entry['id'])
            self.assertRegex(entry['consumer_evidence']['read_on'], DATE, entry['id'])
            self.assertIn(entry['consumer_evidence']['state'], ('open', 'closed'), entry['id'])
            if entry['consumer_status'] == 'unresolved':
                self.assertTrue(entry['unresolved_reason'], entry['id'])

    def test_a_closed_issue_is_never_a_confirmed_consumer(self):
        for entry in LEDGER['handoffs']:
            if entry['consumer_evidence']['state'] == 'closed':
                self.assertEqual(entry['consumer_status'], 'unresolved', entry['id'])

    def test_links_and_gates_are_separate_and_no_native_blocker_is_assumed(self):
        for entry in LEDGER['handoffs']:
            self.assertIn(entry['kind'], ('information', 'acceptance_gate'), entry['id'])
            self.assertIs(entry['native_blocker'], False, entry['id'])
            self.assertEqual(bool(entry['required_for']), entry['kind'] == 'acceptance_gate', entry['id'])

    def test_producer_artifacts_pin_a_commit_only_when_they_exist(self):
        for entry in LEDGER['handoffs']:
            artifact = entry['producer_artifact']
            self.assertIn(artifact['status'], ('existing', 'planned', 'unresolved'), entry['id'])
            if artifact['status'] == 'existing':
                self.assertRegex(artifact['commit'], COMMIT, entry['id'])
                self.assertTrue(artifact['paths'], entry['id'])
            else:
                self.assertIsNone(artifact['commit'], entry['id'])
            if artifact['status'] == 'planned':
                self.assertTrue(artifact['planned_by'], entry['id'])
            if artifact['status'] == 'unresolved':
                self.assertTrue(artifact['unresolved_reason'], entry['id'])

    def test_a_decision_stays_pending_with_nobody_named_until_a_reviewer_records_it(self):
        for entry in LEDGER['handoffs']:
            decision = entry['decision']
            self.assertEqual(set(decision), {'value', 'url', 'date'}, entry['id'])
            self.assertIn(decision['value'], DECISIONS, entry['id'])
            if decision['value'] == 'pending':
                self.assertEqual(decision, {'value': 'pending', 'url': None, 'date': None}, entry['id'])
                self.assertIsNone(entry['reviewer'], entry['id'])
                self.assertIsNone(entry['reviewer_authority'], entry['id'])
                self.assertEqual(entry['conditions'], [], entry['id'])

    def test_a_recorded_decision_names_its_reviewer_authority_link_date_and_reviewed_commit(self):
        # docs/OWNERSHIP_HANDOFFS.md: a decision counts as recorded once reviewer, reviewer_authority, decision.url,
        # decision.date and producer_artifact.commit all exist; the URL and date follow the coverage-receipt rules.
        today = dt.date.today()
        for entry in LEDGER['handoffs']:
            decision = entry['decision']
            if decision['value'] == 'pending':
                continue
            self.assertEqual(entry['consumer_status'], 'confirmed', entry['id'])
            self.assertIsInstance(entry['reviewer'], str, entry['id'])
            self.assertTrue(LOGIN.fullmatch(entry['reviewer']), entry['id'])
            self.assertIsInstance(entry['reviewer_authority'], str, entry['id'])
            self.assertRegex(entry['reviewer_authority'], DATE, entry['id'])
            link = DECISION_URL.fullmatch(decision['url'] or '')
            self.assertTrue(link, entry['id'])
            self.assertEqual(link.group(1), entry['consumer']['repository'], entry['id'])
            date = dt.date.fromisoformat(decision['date'])
            self.assertEqual(date.isoformat(), decision['date'], entry['id'])
            self.assertLessEqual(date, today, entry['id'])
            artifact = entry['producer_artifact']
            self.assertEqual(artifact['status'], 'existing', entry['id'])
            self.assertRegex(artifact['commit'], COMMIT, entry['id'])

    def test_conditions_and_follow_ups_travel_with_the_entry(self):
        for entry in LEDGER['handoffs']:
            self.assertIsInstance(entry['conditions'], list, entry['id'])
            for condition in entry['conditions']:
                self.assertTrue(isinstance(condition, str) and condition.strip(), entry['id'])
            if entry['decision']['value'] == 'accepted_with_conditions':
                self.assertTrue(entry['conditions'], entry['id'])
            self.assertIsInstance(entry['follow_ups'], list, entry['id'])
            for follow_up in entry['follow_ups']:
                self.assertEqual(set(follow_up), {'item', 'owner', 'when'}, entry['id'])
                for value in follow_up.values():
                    self.assertTrue(isinstance(value, str) and value.strip(), entry['id'])

    def test_the_record_and_the_ledger_name_the_same_entries(self):
        record = (ROOT / 'docs/OWNERSHIP_HANDOFFS.md').read_text(encoding='utf-8')
        named = set(re.findall(r'\bH\d{2}\b', record))
        self.assertEqual(named, {entry['id'] for entry in LEDGER['handoffs']})


if __name__ == '__main__':
    unittest.main()
