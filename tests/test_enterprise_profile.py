"""Synthetic enterprise value proposals and existing claim-envelope boundaries.

No real service, configured security control, source-use grant or consumer is tested.
The application validator is deliberately not changed to bind these value proposals.
"""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("enterprise_application_validation", ROOT / "scripts/validate_applications.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
PROFILE = json.loads((ROOT / "schemas/product-profile.schema.json").read_text(encoding="utf-8"))

EXAMPLES = {
    "enterprise_control": {"control": "sso", "dimension": "plan_entitlement", "enabled": True},
    "data_governance": {"topic": "retention", "statement": "Synthetic inputs are retained for seven days.",
                        "basis": "vendor_statement", "duration_days": "7"},
    "support_commitment": {"kind": "sla", "statement": "Synthetic monthly availability commitment.",
                           "basis": "published_terms", "metric": "availability", "target": "99.9",
                           "unit": "percent", "measurement_window": "calendar month"},
    "assurance_statement": {"kind": "supplier_assertion", "issuer": "Synthetic supplier",
                            "document_title": "Synthetic assurance statement", "assessed_scope": "Synthetic service only",
                            "statement": "Supplier asserts a scoped assessment.", "issued_on": "2026-10-21",
                            "limitations": ["Not an independent certification or compliance determination."]},
    "portability": {"operation": "export", "statement": "Synthetic document export is described.", "formats": ["json"]},
    "external_model_access": {"mode": "byok", "statement": "Synthetic plan accepts a customer-supplied key."},
}


def errors(name, value):
    return validator.schema_errors(value, {"$ref": f"#/$defs/{name}"}, "$", PROFILE)


def synthetic_claim_record():
    record = json.loads((ROOT / "tests/fixtures/synthetic_checked.json").read_text(encoding="utf-8"))
    record["publication"] = {"state": "notes", "fields": [], "release_url": None, "consumer_acceptance_url": None}
    record["rights_decisions"] = []
    claim = record["claims"][0]
    claim["field"] = "enterprise.control"
    claim["value"] = copy.deepcopy(EXAMPLES["enterprise_control"])
    claim["scope"].update(region="synthetic-region-a", conditions=["Synthetic enterprise plan; not a real offering."])
    claim["version"] = "synthetic-v1"
    return record


def record_errors(record):
    return validator.validate_record(record, allow_synthetic=True, as_of=dt.date(2026, 11, 17))


class EnterpriseProfileTests(unittest.TestCase):
    def test_known_enterprise_examples_validate_with_supported_schema_vocabulary(self):
        self.assertEqual([], validator.check_schema_vocabulary(PROFILE))
        for name, value in EXAMPLES.items():
            with self.subTest(shape=name):
                self.assertEqual([], errors(name, value))

    def test_control_existence_entitlement_and_enforcement_are_separate_values(self):
        for dimension in ("feature_exists", "plan_entitlement", "configured_enforcement"):
            self.assertEqual([], errors("enterprise_control", dict(EXAMPLES["enterprise_control"], dimension=dimension)))
        self.assertTrue(errors("enterprise_control", dict(EXAMPLES["enterprise_control"], dimension="exists_therefore_enforced")))
        self.assertTrue(errors("enterprise_control", {"control": "sso", "enabled": True}))

    def test_all_named_control_types_accept_a_scoped_disabled_configuration(self):
        for control in ("sso", "scim", "rbac", "audit_log"):
            value = {"control": control, "dimension": "configured_enforcement", "enabled": False,
                     "conditions": ["Synthetic configuration; no real account."]}
            self.assertEqual([], errors("enterprise_control", value))
        self.assertTrue(errors("enterprise_control", dict(value, enabled="unknown")))
        self.assertTrue(errors("enterprise_control", dict(value, enabled=0)))

    def test_unknown_optional_details_can_be_omitted_without_becoming_empty(self):
        for name, value in EXAMPLES.items():
            minimum = {key: value[key] for key in PROFILE["$defs"][name]["required"]}
            self.assertEqual([], errors(name, minimum), name)
            for key in PROFILE["$defs"][name]["properties"].keys() - minimum.keys():
                self.assertNotIn(key, minimum)

    def test_known_empty_lists_and_zero_retention_remain_distinct_from_omission(self):
        value = dict(EXAMPLES["data_governance"], duration_days="0", backup_retention_days="0", exclusions=[])
        self.assertEqual([], errors("data_governance", value))
        self.assertEqual([], errors("data_governance", {k: v for k, v in value.items() if k not in ("duration_days", "backup_retention_days", "exclusions")}))
        for wrong in (None, 0, "unknown", "-1"):
            self.assertTrue(errors("data_governance", dict(value, duration_days=wrong)), repr(wrong))

    def test_data_topics_do_not_imply_other_policy_topics(self):
        for topic in ("retention", "deletion", "residency", "training_use"):
            value = {"topic": topic, "basis": "published_terms", "statement": "Synthetic scoped documentary statement."}
            self.assertEqual([], errors("data_governance", value))
        self.assertTrue(errors("data_governance", dict(value, locations="worldwide")))
        self.assertTrue(errors("data_governance", dict(value, basis="independently_verified")))

    def test_numeric_sla_target_requires_metric_unit_and_measurement_window(self):
        for missing in ("metric", "unit", "measurement_window"):
            value = dict(EXAMPLES["support_commitment"])
            del value[missing]
            self.assertTrue(errors("support_commitment", value), missing)
        partial = {"kind": "support", "basis": "vendor_statement", "statement": "Synthetic response commitment; time unstated."}
        self.assertEqual([], errors("support_commitment", partial))
        self.assertTrue(errors("support_commitment", dict(partial, target="guaranteed")))

    def test_assurance_keeps_issuer_document_scope_and_limitations(self):
        for missing in ("issuer", "document_title", "assessed_scope", "limitations"):
            value = dict(EXAMPLES["assurance_statement"])
            del value[missing]
            self.assertTrue(errors("assurance_statement", value), missing)
        self.assertTrue(errors("assurance_statement", dict(EXAMPLES["assurance_statement"], limitations=[])))
        self.assertTrue(errors("assurance_statement", dict(EXAMPLES["assurance_statement"], compliance_guaranteed=True)))
        self.assertTrue(errors("assurance_statement", dict(EXAMPLES["assurance_statement"], issued_on="recent")))
        undated = dict(EXAMPLES["assurance_statement"])
        del undated["issued_on"]
        self.assertEqual([], errors("assurance_statement", undated))

    def test_portability_does_not_infer_round_trip_or_completeness(self):
        value = dict(EXAMPLES["portability"], residual_data="Synthetic backup treatment unstated.")
        self.assertEqual([], errors("portability", value))
        self.assertTrue(errors("portability", dict(value, formats="json")))
        self.assertTrue(errors("portability", dict(value, completeness=False)))
        self.assertTrue(errors("portability", dict(value, lock_in_score=0)))

    def test_byok_and_byom_preserve_unknown_execution_and_costs(self):
        for mode in ("byok", "byom"):
            value = {"mode": mode, "statement": "Synthetic scoped mode statement."}
            self.assertEqual([], errors("external_model_access", value))
            self.assertNotIn("external_costs", value)
            self.assertNotIn("model_execution_location", value)
        self.assertTrue(errors("external_model_access", dict(value, external_costs=0)))
        self.assertTrue(errors("external_model_access", dict(value, providers_or_models="all")))

    def test_extra_properties_and_null_known_objects_are_refused(self):
        for name, value in EXAMPLES.items():
            self.assertTrue(errors(name, dict(value, guessed=True)), name)
            self.assertTrue(errors(name, None), name)
            self.assertTrue(errors(name, {}), name)

    def test_scoped_unknown_enterprise_claim_is_null_and_keeps_its_conditions(self):
        record = synthetic_claim_record()
        claim = record["claims"][0]
        claim.update(value_status="unknown", value=None, source_status="unchecked", checked_on=None, source_ids=[], as_of=None)
        claim["review"] = {"status": "pending", "reviewer": None, "reviewed_on": None, "decision_url": None}
        self.assertEqual([], record_errors(record))
        self.assertEqual("synthetic-region-a", claim["scope"]["region"])
        self.assertEqual("synthetic-v1", claim["version"])
        for guessed in (False, 0, {}, []):
            claim["value"] = guessed
            self.assertTrue(any("must remain null" in e for e in record_errors(record)), repr(guessed))

    def test_unsupported_enterprise_capability_requires_explicit_checked_negative(self):
        record = synthetic_claim_record()
        claim = record["claims"][0]
        claim.update(value_status="unsupported", value=False)
        self.assertTrue(any("explicit negative evidence" in e for e in record_errors(record)))
        claim["explicit_negative_evidence"] = True
        self.assertEqual([], record_errors(record))
        claim["value"] = {}
        self.assertTrue(any("explicit JSON false" in e for e in record_errors(record)))

    def test_proposed_value_shapes_are_not_silently_bound_to_application_admission(self):
        record = synthetic_claim_record()
        self.assertEqual([], record_errors(record))
        # The known-value proposal refuses this wrong dimension. The existing
        # application contract still does not bind enterprise.* value shapes.
        record["claims"][0]["value"]["dimension"] = "invalid_dimension"
        self.assertTrue(errors("enterprise_control", record["claims"][0]["value"]))
        self.assertEqual([], record_errors(record))


if __name__ == "__main__":
    unittest.main()
