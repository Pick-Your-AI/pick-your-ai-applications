"""Structural checks for planning/handoffs.json, the receiving-handoff ledger (docs/OWNERSHIP_HANDOFFS.md).

These check the ledger's shape and its pending-by-default rules. They do not read GitHub, so they cannot confirm a
consumer, a reviewer's authority or a decision.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / 'planning/handoffs.json').read_text(encoding='utf-8'))
REPO = re.compile(r'Pick-Your-AI/[A-Za-z0-9_.-]+')
COMMIT = re.compile(r'[0-9a-f]{40}')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')


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

    def test_every_decision_starts_pending_with_nobody_named(self):
        for entry in LEDGER['handoffs']:
            self.assertEqual(entry['decision'], {'value': 'pending', 'url': None, 'date': None}, entry['id'])
            self.assertIsNone(entry['reviewer'], entry['id'])
            self.assertIsNone(entry['reviewer_authority'], entry['id'])

    def test_the_record_and_the_ledger_name_the_same_entries(self):
        record = (ROOT / 'docs/OWNERSHIP_HANDOFFS.md').read_text(encoding='utf-8')
        named = set(re.findall(r'\bH\d{2}\b', record))
        self.assertEqual(named, {entry['id'] for entry in LEDGER['handoffs']})


if __name__ == '__main__':
    unittest.main()
