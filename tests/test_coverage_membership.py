"""Regression checks for invented coverage, identity overlap and receipt substitution."""
import copy
import datetime as dt
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage_membership import COUNTERS, reconcile, reconcile_repository
from validate_applications import load_json, schema_errors

AS_OF = dt.date(2026, 10, 22)


class CoverageMembershipTests(unittest.TestCase):
    def setUp(self):
        self.taxonomy = load_json(ROOT / "taxonomy/taxonomy.json")
        self.ledger = load_json(ROOT / "coverage/ledger.json")
        self.record = load_json(ROOT / "tests/fixtures/synthetic_checked.json")
        self.ledger["rows"] = self.ledger["rows"][:2]
        self.categories = [row["category_id"] for row in self.ledger["rows"]]
        self.record["classification"]["category_ids"] = self.categories
        classification = copy.deepcopy(self.record["claims"][0])
        classification.update(id="claim:classification", field="classification.category_ids",
                              fact_type="classification", value=self.categories)
        self.record["claims"].append(classification)
        self.record["classification"]["classification_claim_ids"] = [classification["id"]]
        self.sighting = {
            "id": "sighting:synthetic-discovery", "source_url": "https://docs.example.invalid/lead",
            "accessed_on": "2026-10-21", "product_id": self.record["record_id"],
            "disposition": "included", "reason": "Synthetic test membership only.", "synthetic": True,
        }
        self.surveys = [{"schema_version": "0.1.0", "category_id": cid,
                         "sightings": [copy.deepcopy(self.sighting)]} for cid in self.categories]
        for row in self.ledger["rows"]:
            row["research_status"] = "in_progress"
            for counter in ("candidate_sightings_count", "deduplicated_product_count",
                            "primary_sourced_product_count", "reviewed_product_count",
                            "publication_eligible_product_count"):
                row[counter] = 1

    def check(self):
        return reconcile(self.ledger, [self.record], self.surveys, as_of=AS_OF,
                         taxonomy=self.taxonomy, allow_synthetic=True)

    def test_zero_real_corpus_reconciles_without_manufacturing_records(self):
        ledger = load_json(ROOT / "coverage/ledger.json")
        self.assertEqual({key: 0 for key in COUNTERS},
                         reconcile_repository(ROOT, ledger, self.taxonomy, as_of=AS_OF))

    def test_positive_counts_without_actual_records_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "actual record membership"):
            reconcile(self.ledger, [], as_of=AS_OF)

    def test_overlapping_categories_count_one_product_globally(self):
        totals = self.check()
        self.assertEqual(1, totals["deduplicated_product_count"])
        self.assertEqual(1, totals["candidate_sightings_count"])
        self.assertEqual(1, totals["publication_eligible_product_count"])
        self.assertEqual(2, sum(row["deduplicated_product_count"] for row in self.ledger["rows"]))

    def test_omitted_admitted_product_is_rejected(self):
        self.ledger["rows"][0]["deduplicated_product_count"] = 0
        with self.assertRaisesRegex(ValueError, "actual record membership"):
            self.check()

    def test_synthetic_data_cannot_enter_cli_coverage(self):
        with self.assertRaisesRegex(ValueError, "synthetic data"):
            reconcile(self.ledger, [self.record], self.surveys, as_of=AS_OF)

    def test_unclassified_admitted_record_cannot_disappear_from_global_counts(self):
        unclassified = load_json(ROOT / "tests/fixtures/synthetic_checked.json")
        ledger = load_json(ROOT / "coverage/ledger.json")
        with self.assertRaisesRegex(ValueError, "unclassified admitted product"):
            reconcile(ledger, [unclassified], as_of=AS_OF, allow_synthetic=True)

    def test_pending_claim_does_not_erase_reviewed_eligible_field(self):
        pending = copy.deepcopy(self.record["claims"][0])
        pending.update(id="claim:pending", field="capability.pending")
        pending["review"] = {"status": "pending", "reviewer": None,
                             "reviewed_on": None, "decision_url": None}
        self.record["claims"].append(pending)
        totals = self.check()
        self.assertEqual(1, totals["reviewed_product_count"])
        self.assertEqual(1, totals["publication_eligible_product_count"])

    def test_independent_source_does_not_replace_required_primary_provenance(self):
        self.record["sources"][0]["authority"] = "independent"
        with self.assertRaisesRegex(ValueError, "primary source evidence"):
            self.check()

    def test_malformed_coverage_basis_returns_diagnostics_not_type_errors(self):
        for basis in ("bad", {"numerator_product_ids": None}, {"numerator_product_ids": [{}]},
                      {"numerator_product_ids": [self.record["record_id"]] * 2}):
            with self.subTest(basis=basis):
                self.ledger["rows"][0]["coverage_basis"] = basis
                with self.assertRaisesRegex(ValueError, "coverage basis needs"):
                    self.check()

    def test_counter_boolean_does_not_equal_one_product(self):
        self.ledger["rows"][0]["deduplicated_product_count"] = True
        with self.assertRaisesRegex(ValueError, "actual record membership"):
            self.check()

    def test_offerings_are_qualified_by_product_and_not_category(self):
        self.record["entities"] = [{"id": "offering:synthetic-plan", "entity_type": "application_offering",
                                    "name": "Synthetic plan", "product_id": self.record["record_id"],
                                    "version": None, "url": None}]
        for row in self.ledger["rows"]:
            row["offering_count"] = 1
        self.assertEqual(1, self.check()["offering_count"])

    def test_arbitrary_included_candidate_id_is_rejected(self):
        self.surveys[0]["sightings"][0]["product_id"] = "app:nonexistent"
        with self.assertRaisesRegex(ValueError, "resolve to a product"):
            self.check()

    def test_duplicate_sighting_does_not_inflate_discovery(self):
        self.surveys[0]["sightings"].append(copy.deepcopy(self.sighting))
        with self.assertRaisesRegex(ValueError, "duplicate candidate sighting"):
            self.check()

    def test_conflicting_reuse_of_sighting_id_is_rejected(self):
        self.surveys[1]["sightings"][0]["reason"] = "Different discovery event."
        with self.assertRaisesRegex(ValueError, "conflicting discovery metadata"):
            self.check()

    def test_unresolved_sighting_is_not_an_admitted_product(self):
        self.surveys[0]["sightings"][0]["disposition"] = "unresolved"
        with self.assertRaisesRegex(ValueError, "must not assert an admitted product"):
            self.check()

    def test_failed_source_identity_and_impossible_access_dates_rejected(self):
        for field, value in (("source_url", "http://127.0.0.1/private"),
                             ("accessed_on", "2026-02-30"), ("accessed_on", "2026-10-23")):
            with self.subTest(field=field, value=value):
                old = self.surveys[0]["sightings"][0][field]
                self.surveys[0]["sightings"][0][field] = value
                with self.assertRaisesRegex(ValueError, "invalid candidate provenance"):
                    self.check()
                self.surveys[0]["sightings"][0][field] = old

    def test_review_and_measurement_are_not_inferred_from_record_existence(self):
        self.ledger["rows"][0]["independently_measured_product_count"] = 1
        with self.assertRaisesRegex(ValueError, "independently_measured.*actual record membership"):
            self.check()

    def test_same_size_percentage_numerator_cannot_substitute_another_product(self):
        self.ledger["rows"][0]["coverage_basis"] = {"numerator_product_ids": ["app:other"]}
        with self.assertRaisesRegex(ValueError, "numerator differs"):
            self.check()

    def test_unrelated_publication_receipt_cannot_upgrade_coverage(self):
        self.ledger["rows"][0]["acceptance_receipts"] = [{"product_ids": ["app:other"]}]
        with self.assertRaisesRegex(ValueError, "different products"):
            self.check()

    def test_counter_envelope_rejects_missing_or_malformed_counts(self):
        schema = load_json(ROOT / "schemas/coverage-ledger.schema.json")
        self.assertEqual([], schema_errors(self.ledger, schema))
        del self.ledger["rows"][0]["offering_count"]
        self.assertTrue(schema_errors(self.ledger, schema))


if __name__ == "__main__":
    unittest.main()
