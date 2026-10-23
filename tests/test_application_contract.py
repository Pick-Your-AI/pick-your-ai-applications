"""Meaningful rejection tests for evidence, identity, pricing and publication boundaries."""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("application_validation", ROOT / "scripts" / "validate_applications.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
AS_OF = dt.date(2026, 10, 22)


class ApplicationContractTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "tests" / "fixtures" / "synthetic_checked.json").read_text())

    def errors(self, allow_synthetic=True):
        return validator.validate_record(self.record, as_of=AS_OF, allow_synthetic=allow_synthetic)

    def assertRejected(self, text):
        errors = self.errors()
        self.assertTrue(any(text in e for e in errors), errors)

    def test_checked_documentation_can_be_displayed_as_unverified(self):
        self.assertEqual([], self.errors())
        self.assertEqual("unverified", self.record["publication"]["fields"][0]["display_verification_status"])

    def test_fixture_cannot_enter_real_catalog(self):
        self.assertTrue(any("synthetic data" in e for e in self.errors(False)))

    def test_unknown_is_valid_research_but_never_false(self):
        self.record["publication"] = {"state": "notes", "fields": [], "release_url": None, "consumer_acceptance_url": None}
        c = self.record["claims"][0]
        c.update(value_status="unknown", value=None, source_status="unchecked", checked_on=None, source_ids=[], as_of=None)
        c["review"] = {"status": "pending", "reviewer": None, "reviewed_on": None, "decision_url": None}
        self.assertEqual([], self.errors())
        c["value"] = False
        self.assertRejected("must remain null")

    def test_absence_is_not_unsupported(self):
        self.record["claims"][0].update(value_status="unsupported", value=False)
        self.assertRejected("explicit negative evidence")

    def test_source_check_is_not_independent_verification(self):
        self.record["claims"][0]["verification_status"] = "verified"
        self.assertRejected("independent verification receipt")

    def test_display_cannot_upgrade_evidence(self):
        self.record["publication"]["fields"][0]["display_verification_status"] = "verified"
        self.assertRejected("display grade/status")

    def test_public_url_does_not_confer_reuse_rights(self):
        self.record["rights_decisions"][0]["decision"] = "unknown"
        self.assertRejected("field-specific display rights")

    def test_display_rights_do_not_confer_api_rights(self):
        self.record["publication"]["fields"][0]["uses"].append("api")
        self.assertRejected("field-specific api rights")

    def test_one_field_does_not_clear_entire_record(self):
        self.record["rights_decisions"][0]["fields"] = ["*"]
        self.assertRejected("field-specific display rights")

    def test_expired_rights_block_publication(self):
        self.record["rights_decisions"][0]["expires_on"] = "2026-10-21"
        self.assertRejected("field-specific display rights")

    def test_recheck_required_facts_are_not_publishable(self):
        self.record["claims"][0]["evidence_state"] = "recheck_required"
        self.assertRejected("recheck-required evidence")

    def test_no_arbitrary_ttl_expires_dated_facts(self):
        self.record["sources"][0]["accessed_on"] = "2025-01-01"
        self.record["claims"][0].update(checked_on="2025-01-01", as_of="2025-01-01")
        self.assertEqual([], self.errors())

    def test_source_withdrawal_blocks_publication(self):
        self.record["sources"][0]["state"] = "withdrawn"
        self.assertRejected("inactive source")

    def test_future_and_impossible_dates_rejected(self):
        self.record["sources"][0]["accessed_on"] = "2026-10-23"
        self.assertRejected("date is in the future")
        self.record["sources"][0]["accessed_on"] = "2026-02-30"
        self.assertRejected("real ISO")

    def test_current_state_requires_as_of_label(self):
        self.record["claims"][0]["as_of"] = None
        self.assertRejected("display their checked date")

    def test_version_pinned_claim_requires_version(self):
        self.record["claims"][0]["temporal_scope"] = "version_pinned"
        self.assertRejected("concrete version")

    def test_self_review_does_not_approve_claim(self):
        c = self.record["claims"][0]
        c["review"]["reviewer"] = c["researcher"]
        self.assertRejected("reviewer other than its researcher")

    def test_model_cannot_be_encoded_as_application_product(self):
        self.record["record_id"] = self.record["identity"]["product_id"] = "model:weights"
        self.assertRejected("app: namespace")

    def test_unresolved_claim_subject_rejected(self):
        self.record["claims"][0]["subject"]["id"] = "offering:invented"
        self.assertRejected("exact registered entity")

    def test_independent_reproduction_requires_protocol(self):
        c = self.record["claims"][0]
        c["verification_status"] = "verified"
        c["verification"] = {"method": "reproduced_test", "independent": True, "verifier": "synthetic-verifier", "verified_on": "2026-10-22", "receipt_url": "https://review.example.invalid/test/1", "protocol_version": None, "source_id": None, "limitations": "Synthetic; not a real run."}
        self.assertRejected("pinned protocol")
        c["verification"]["protocol_version"] = "synthetic-protocol@1"
        c["verification"]["verified_on"] = "2026-02-30"
        self.assertRejected("real ISO")

    def test_secondary_vendor_article_is_not_independent_source(self):
        c = self.record["claims"][0]
        c["verification_status"] = "verified"
        c["verification"] = {"method": "independent_second_source", "independent": True, "verifier": "synthetic-verifier", "verified_on": "2026-10-22", "receipt_url": "https://review.example.invalid/test/1", "protocol_version": None, "source_id": "source:documentation", "limitations": "Synthetic; not a real run."}
        self.assertRejected("cited independent source")

    def test_published_requires_release_and_consumer_receipts(self):
        self.record["publication"]["state"] = "published"
        self.assertRejected("immutable release and consumer acceptance")

    def test_no_blanket_eligible_record(self):
        self.record["publication"]["fields"] = []
        self.assertRejected("explicit admitted fields")

    def test_source_url_rejects_credentials_and_private_address(self):
        self.record["sources"][0]["url"] = "https://user:secret@host.example.invalid/docs"
        self.assertRejected("stable public HTTP")
        self.record["sources"][0]["url"] = "http://127.0.0.1/docs"
        self.assertRejected("stable public HTTP")

    def add_price(self):
        self.record["entities"].append({"id": "offering:synthetic-standard", "entity_type": "application_offering", "name": "Synthetic Standard", "product_id": self.record["record_id"], "version": None, "url": None})
        c = self.record["claims"][0]
        c.update(subject={"id": "offering:synthetic-standard", "entity_type": "application_offering"}, field="pricing.standard", fact_type="pricing")
        self.record["rights_decisions"][0]["fields"] = ["pricing.standard"]
        c["value"] = {"offering_id": "offering:synthetic-standard", "plan_name": "Synthetic Standard", "amount_status": "known", "amount": "0", "currency": "USD", "regions": ["US"], "billing_period": "month", "meter": "seat-month", "commitment": "monthly", "tax_treatment": "unknown", "minimum_seats": 1, "included_allowance": None, "overage_terms": None, "promotion_conditions": None, "effective_on": "2026-10-21"}
        return c["value"]

    def test_sourced_zero_price_is_distinct_from_unknown(self):
        value = self.add_price()
        self.assertEqual([], self.errors())
        value["amount_status"] = "unknown"
        self.assertRejected("must not invent an amount")
        value["amount"] = None
        self.assertEqual([], self.errors())

    def test_price_needs_exact_offering_and_meter_context(self):
        value = self.add_price()
        value["offering_id"] = self.record["record_id"]
        self.assertRejected("registered application offering")
        value["offering_id"] = "offering:synthetic-standard"
        value["meter"] = None
        self.assertRejected("currency, region, meter")

    def test_empty_real_intake_does_not_fabricate_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            files, errors = validator.validate_directory(Path(directory), as_of=AS_OF)
        self.assertEqual([], files)
        self.assertEqual([], errors)

    def test_schema_keyword_drift_is_rejected(self):
        self.assertTrue(validator.check_schema_vocabulary({"type": "object", "unsupportedKeyword": True}))

    def test_nonfinite_numeric_claim_is_not_valid_json(self):
        self.record["claims"][0]["value"] = float("nan")
        self.assertRejected("non-finite numbers")

    def test_required_source_authority_and_unique_nonempty_ids(self):
        del self.record["sources"][0]["authority"]
        self.assertRejected("missing required property authority")
        self.record["sources"][0]["authority"] = "primary"
        self.record["sources"].append(copy.deepcopy(self.record["sources"][0]))
        self.record["sources"][-1]["title"] = "Different metadata cannot reuse a source ID"
        self.assertRejected("duplicate id")
        self.record["sources"].pop()
        self.record["claims"][0]["id"] = ""
        self.assertRejected("required pattern")

    def test_taxonomy_references_and_facets_are_checked(self):
        taxonomy = {"categories": [{"id": "APP-C01"}], "facets": {"access_surface": ["web", "unknown"]}}
        self.record["classification"]["category_ids"] = ["nonexistent"]
        errors = validator.validate_record(self.record, as_of=AS_OF, allow_synthetic=True, taxonomy=taxonomy)
        self.assertTrue(any("not in the current taxonomy" in error for error in errors), errors)
        self.record["classification"]["category_ids"] = ["APP-C01"]
        self.record["claims"][0].update(field="facets.access_surface", value="unsupported-surface")
        errors = validator.validate_record(self.record, as_of=AS_OF, allow_synthetic=True, taxonomy=taxonomy)
        self.assertTrue(any("facet value" in error for error in errors), errors)

    def test_separate_price_requires_canonical_application_and_offering(self):
        self.add_price()
        price = {"schema_version": "0.1.0", "record_id": "price:synthetic-standard-20261021", "entity_type": "application_price", "synthetic": True, "application_id": self.record["record_id"], "offering_id": "offering:synthetic-standard", "sources": self.record["sources"], "claim": self.record["claims"][0], "rights_decisions": self.record["rights_decisions"], "publication": self.record["publication"], "known_unknowns": [], "research_notes": ["Synthetic price wrapper."]}
        applications = {self.record["record_id"]: self.record}
        self.assertEqual([], validator.validate_pricing_record(price, applications, as_of=AS_OF, allow_synthetic=True))
        errors = validator.validate_pricing_record(price, {}, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any("canonical application" in error for error in errors), errors)
        price["offering_id"] = "offering:invented"
        errors = validator.validate_pricing_record(price, applications, as_of=AS_OF, allow_synthetic=True)
        self.assertTrue(any("must already be declared" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
