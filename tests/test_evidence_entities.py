"""Offline shape/drift tests; every observation below is synthetic and unperformed."""
import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evidence_validation", ROOT / "scripts/validate_applications.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
AS_OF = dt.date(2026, 11, 17)


def load_schema(name):
    return v.load_json(ROOT / "schemas" / (name + ".schema.json"))


def synthetic_attempt(outcome="failed_access"):
    """A hypothetical fixture, never a receipt of source access or review."""
    return {
        "schema_version": "0.1.0-proposal", "entity_type": "application_observation_proposal",
        "synthetic": True, "id": "observation:synthetic-attempt", "researcher": "synthetic-researcher",
        "subject": {"id": "app:synthetic-tool", "entity_type": "application_product"},
        "field": "capabilities.synthetic", "scope": {
            "offering_id": None, "region": None, "locale": None, "platform": None, "conditions": []},
        "temporal_scope": "current_state", "version": None, "release_channel": None,
        "source_locator": "https://source.example.invalid/synthetic-only", "source_id": None,
        "attempted_on": "2026-11-17", "outcome": outcome, "checked_on": None,
        "access_note": "Synthetic inaccessible-source scenario; no request was made.", "claim_ids": [],
        "evidence_state": "active", "supersedes_observation_ids": [], "disputes_observation_ids": [],
        "review": {"status": "pending", "reviewer": None, "reviewed_on": None, "decision_url": None},
        "limitations": "Synthetic fixture only; no source, product, review or permission was verified."
    }


class EvidenceEntityTests(unittest.TestCase):
    def setUp(self):
        self.application = load_schema("application")
        self.claim = load_schema("claim")
        self.source = load_schema("source")
        self.observation = load_schema("observation")
        self.record = v.load_json(ROOT / "tests/fixtures/synthetic_checked.json")

    def test_standalone_entities_exactly_match_authoritative_inline_shapes(self):
        metadata = {"$schema", "$id", "title", "description", "$defs"}
        for name in ("claim", "source"):
            schema = getattr(self, name)
            shape = {k: value for k, value in schema.items() if k not in metadata}
            self.assertEqual(self.application["$defs"][name], shape)
        self.assertEqual({k: self.application["$defs"][k] for k in ("subject", "review", "verification")},
                         self.claim["$defs"])
        self.assertNotIn("$defs", self.source)

    def test_all_proposal_schemas_use_supported_resolvable_local_vocabulary(self):
        for schema in (self.claim, self.source, self.observation):
            self.assertEqual([], v.check_schema_vocabulary(schema))
        for name in ("subject", "review"):
            self.assertEqual(self.application["$defs"][name], self.observation["$defs"][name])
        self.assertEqual(self.application["$defs"]["claim"]["properties"]["scope"],
                         self.observation["properties"]["scope"])

    def test_standalone_and_embedded_validation_agree_on_valid_and_invalid_shapes(self):
        for name, value in (("claim", self.record["claims"][0]), ("source", self.record["sources"][0])):
            variants = [value, {**value, "unexpected": True}, {}]
            variants.extend({k: val for k, val in value.items() if k != omitted} for omitted in value)
            for variant in variants:
                standalone = v.schema_errors(variant, getattr(self, name))
                embedded = v.schema_errors(variant, self.application["$defs"][name], root_schema=self.application)
                self.assertEqual(embedded, standalone)
            self.assertEqual([], v.schema_errors(value, getattr(self, name)))

    def test_failed_access_does_not_become_a_check_or_sourced_claim(self):
        attempt = synthetic_attempt()
        self.assertEqual([], v.schema_errors(attempt, self.observation))
        for change in ({"checked_on": "2026-11-17"}, {"source_id": "source:invented"},
                       {"claim_ids": ["claim:invented"]}, {"verification": {"independent": True}}):
            with self.subTest(change=change):
                self.assertTrue(v.schema_errors({**attempt, **change}, self.observation))

    def test_checked_attempt_requires_dated_source_and_claim_links(self):
        attempt = synthetic_attempt("checked")
        self.assertTrue(v.schema_errors(attempt, self.observation))
        attempt.update(checked_on="2026-11-17", source_id="source:synthetic", claim_ids=["claim:synthetic"],
                       access_note="Synthetic checked shape; no actual source check occurred.")
        self.assertEqual([], v.schema_errors(attempt, self.observation))
        for field in ("checked_on", "source_id"):
            self.assertTrue(v.schema_errors({**attempt, field: None}, self.observation))
        self.assertTrue(v.schema_errors({**attempt, "claim_ids": []}, self.observation))

    def test_history_scope_and_review_remain_explicit(self):
        attempt = synthetic_attempt()
        attempt.update(evidence_state="disputed", disputes_observation_ids=["observation:synthetic-other"],
                       supersedes_observation_ids=["observation:synthetic-earlier"])
        self.assertEqual([], v.schema_errors(attempt, self.observation))
        self.assertTrue(v.schema_errors({**attempt, "disputes_observation_ids": []}, self.observation))
        self.assertTrue(v.schema_errors({**attempt, "supersedes_observation_ids": ["claim:wrong-kind"]}, self.observation))
        attempt["review"]["verifier"] = "synthetic-reviewer-is-not-verifier"
        self.assertTrue(v.schema_errors(attempt, self.observation))
        del attempt["review"]["verifier"]
        attempt.update(temporal_scope="version_pinned")
        self.assertTrue(v.schema_errors(attempt, self.observation))
        attempt["version"] = "synthetic-v1"
        self.assertEqual([], v.schema_errors(attempt, self.observation))
        del attempt["scope"]["platform"]
        self.assertTrue(v.schema_errors(attempt, self.observation))

    def test_proposed_sidecar_cannot_be_admitted_or_grant_publication(self):
        attempt = synthetic_attempt()
        self.assertTrue(v.validate_record(attempt, as_of=AS_OF, allow_synthetic=True))
        for property_name in ("publication", "rights_decisions", "verification_status"):
            self.assertTrue(v.schema_errors({**attempt, property_name: "approved"}, self.observation))

    def test_standalone_shape_does_not_replace_record_semantic_gates(self):
        claim = self.record["claims"][0]
        claim["verification_status"] = "verified"
        self.assertEqual([], v.schema_errors(claim, self.claim))
        errors = v.validate_record(self.record, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any("independent verification receipt" in error for error in errors), errors)
        claim["verification_status"] = "unverified"
        claim["source_ids"] = ["source:unresolved"]
        errors = v.validate_record(self.record, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any("unresolved source IDs" in error for error in errors), errors)

    def test_duplicate_keys_are_rejected_before_shape_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "synthetic.json"
            path.write_text('{"outcome":"failed_access","outcome":"checked"}')
            with self.assertRaisesRegex(ValueError, "duplicate JSON"):
                v.load_json(path)

    def test_observation_date_shape_is_not_calendar_or_retrieval_evidence(self):
        attempt = synthetic_attempt()
        attempt["attempted_on"] = "2026-02-30"
        self.assertEqual([], v.schema_errors(attempt, self.observation))
        errors = []
        v.date_value(attempt["attempted_on"], "attempted_on", errors, AS_OF)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
