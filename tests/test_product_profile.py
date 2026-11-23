"""The product comparison value shapes (schemas/product-profile.schema.json, APP-F02.03): the schema keeps to the
validator's keyword set, and synthetic values show what each shape takes and refuses. No real product is described."""
import copy
import datetime as dt
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AS_OF = dt.date(2026, 11, 17)
spec = importlib.util.spec_from_file_location("application_validation", ROOT / "scripts" / "validate_applications.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
PROFILE = json.loads((ROOT / "schemas" / "product-profile.schema.json").read_text(encoding="utf-8"))
FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "synthetic_enterprise_profile.json").read_text(encoding="utf-8"))
TAXONOMY = json.loads((ROOT / "taxonomy" / "taxonomy.json").read_text(encoding="utf-8"))

PART2_FIELD_TO_SHAPE = {
    "product.runtime.requirements": "runtime_requirements",
    "product.enterprise.identity_access": "enterprise_identity_access",
    "product.enterprise.tenancy": "enterprise_tenancy",
    "product.data.retention": "data_retention",
    "product.data.training_use": "training_use",
    "product.data.portability_deletion": "portability_deletion",
    "product.data.residency": "data_residency",
    "product.support.sla": "support_sla",
    "product.security.assurance": "security_assurance",
    "product.security.byok_byom": "byok_byom",
}

EXAMPLES = {
    "io": [
        {"direction": "input", "modality": "documents", "formats": ["pdf"], "conditions": [],
         "limits": [{"kind": "file_size", "amount": "50", "unit": "MB", "per": "file", "conditions": ["web client"]}]},
        {"direction": "output", "modality": "text", "formats": [], "limits": [], "conditions": []},
    ],
    "eligibility": {"account_kind": "individual", "eligible": True, "requirements": ["age 18 or over"],
                    "basis": "documented_rule"},
    "platform_test": {"result": "works", "client_version": "1.2.3", "operating_system": "linux",
                      "operating_system_version": "24.04", "architecture": "x86_64", "workflow": "summarize a PDF"},
    "client_platform": {"operating_systems": ["windows", "macos"], "architectures": ["x86_64", "arm64"],
                        "minimum_os_versions": [{"operating_system": "macos", "version": "13"}]},
    "installation": {"methods": ["direct_download", "package_manager"]},
    "network": {"offline": "partial", "works_offline": ["editing"], "needs_network_for": ["sign_in", "inference"]},
    "runtime_requirements": {"kind": "minimum", "memory_gib": "16", "accelerator": "optional_gpu",
                             "operating_systems": ["linux"], "architectures": ["x86_64"],
                             "applies_to": "the bundled model"},
    "enterprise_control_state": {"documented_status": "documented_with_conditions",
                                 "entitlement_scope": "included_in_plan",
                                 "configured_enforcement": "admin_configurable",
                                 "exercised_status": "documented_only",
                                 "conditions": ["Requires verified organization domain"]},
    "enterprise_identity_access": {
        "control_kind": "sso",
        "protocols_or_models": ["SAML 2.0", "OIDC"],
        "state": {"documented_status": "documented", "entitlement_scope": "enterprise_contract_only",
                  "configured_enforcement": "admin_configurable", "exercised_status": "documented_only"},
    },
    "enterprise_tenancy": {
        "isolation_model": "logical_tenant_isolation",
        "dedicated_encryption_boundary": True,
        "state": {"documented_status": "documented", "entitlement_scope": "included_in_plan",
                  "configured_enforcement": "mandatory_default", "exercised_status": "documented_only"},
    },
    "data_retention": {
        "data_class": "prompts_and_inputs",
        "retention_mode": "configurable_window",
        "duration_days": "30",
        "state": {"documented_status": "documented", "entitlement_scope": "included_in_plan",
                  "configured_enforcement": "admin_configurable", "exercised_status": "documented_only"},
    },
    "training_use": {
        "default_policy": "excluded_from_training_by_default",
        "opt_out_mechanism": "contractual_term",
        "human_review_exception": False,
        "state": {"documented_status": "documented", "entitlement_scope": "included_in_plan",
                  "configured_enforcement": "mandatory_default", "exercised_status": "documented_only"},
    },
    "portability_deletion": {
        "capability": "data_export",
        "initiator": "workspace_admin",
        "export_formats": ["json", "markdown"],
        "completeness": "partial_user_artifacts_only",
        "deletion_sla_days": "30",
        "retained_backups_note": "Immutable backups purge on a 30-day rolling cycle",
        "state": {"documented_status": "documented", "entitlement_scope": "included_in_plan",
                  "configured_enforcement": "admin_configurable", "exercised_status": "independently_exercised"},
    },
    "data_residency": {
        "regions": ["EU"],
        "applies_to_stages": ["storage_at_rest", "backups"],
        "pinning_guarantee": "storage_pinned_inference_routed",
        "cross_border_exceptions": ["Model inference requests may fail over outside EU"],
        "state": {"documented_status": "documented_with_conditions",
                  "entitlement_scope": "enterprise_contract_only",
                  "exercised_status": "documented_only"},
    },
    "support_sla": {
        "channels": ["email_ticket", "dedicated_account_manager"],
        "coverage_hours": "24x7 P1; business hours P2-P4",
        "first_response_hours": "4",
        "uptime_sla_percent": "99.9",
        "uptime_measurement_window": "calendar month",
        "remedy_kind": "service_credit",
        "exclusions": ["Excludes upstream model provider outages"],
        "state": {"documented_status": "documented_with_conditions",
                  "entitlement_scope": "enterprise_contract_only",
                  "exercised_status": "documented_only"},
    },
    "security_assurance": {
        "framework_or_standard": "SOC 2 Type II",
        "issuer": "Synthetic Audit Firm LLP",
        "covered_scope": "Synthetic Enterprise web control plane",
        "period_start": "2025-11-01",
        "period_end": "2026-10-31",
        "expires_on": "2027-10-31",
        "report_access": "nda_trust_portal",
        "documentary_limits": ["Summary page reviewed; full report requires NDA"],
    },
    "byok_byom": {
        "kind": "byok_encryption",
        "supported_targets": ["AWS KMS"],
        "residual_exposure_or_fee_notes": ["Search index keys remain vendor-managed"],
        "state": {"documented_status": "documented_with_conditions",
                  "entitlement_scope": "paid_add_on",
                  "configured_enforcement": "opt_in_disabled_by_default",
                  "exercised_status": "documented_only"},
    },
}


def errors(name, value):
    return validator.schema_errors(value, {"$ref": f"#/$defs/{name}"}, "$", PROFILE)


class ProductProfileTests(unittest.TestCase):
    def test_the_schema_uses_only_supported_keywords(self):
        self.assertEqual([], validator.check_schema_vocabulary(PROFILE))

    def test_each_shape_takes_its_example(self):
        for name, value in EXAMPLES.items():
            self.assertEqual([], errors(name, value), name)

    def test_an_input_cannot_have_an_output_only_modality(self):
        value = copy.deepcopy(EXAMPLES["io"])
        value[0]["modality"] = "code"
        self.assertTrue(errors("io", value))

    def test_a_known_input_can_omit_unstated_details(self):
        value = [{"direction": "input", "modality": "documents", "formats": ["pdf"]}]
        self.assertEqual([], errors("io", value))

    def test_sourced_empty_io_details_are_valid(self):
        value = [{"direction": "input", "modality": "documents", "formats": [],
                  "limits": [], "conditions": []}]
        self.assertEqual([], errors("io", value))

    def test_provided_io_details_keep_their_types(self):
        value = [{"direction": "input", "modality": "documents", "formats": "pdf"}]
        self.assertTrue(errors("io", value))
        value[0]["formats"] = ["pdf"]
        value[0]["limits"] = "none"
        self.assertTrue(errors("io", value))
        value[0].pop("limits")
        value[0]["conditions"] = None
        self.assertTrue(errors("io", value))

    def test_a_limit_is_a_decimal_string_with_its_scope(self):
        value = copy.deepcopy(EXAMPLES["io"])
        value[0]["limits"][0]["amount"] = 50
        self.assertTrue(errors("io", value), "a number, not a decimal string")
        value[0]["limits"][0]["amount"] = "unlimited"
        self.assertTrue(errors("io", value), "unlimited is not an amount")
        del value[0]["limits"][0]["per"]
        self.assertTrue(errors("io", value))

    def test_eligibility_says_how_it_is_known(self):
        value = dict(EXAMPLES["eligibility"])
        del value["basis"]
        self.assertTrue(errors("eligibility", value))
        value["basis"] = "advertised"
        self.assertTrue(errors("eligibility", value), "advertised availability is facets.availability, not eligibility")

    def test_a_platform_test_names_exactly_what_ran(self):
        for missing in ("client_version", "operating_system_version", "architecture", "workflow"):
            value = dict(EXAMPLES["platform_test"])
            del value[missing]
            self.assertTrue(errors("platform_test", value), missing)

    def test_runtime_requirements_say_what_they_apply_to_and_never_mix_minimum_and_recommended(self):
        value = dict(EXAMPLES["runtime_requirements"])
        del value["applies_to"]
        self.assertTrue(errors("runtime_requirements", value))
        value = dict(EXAMPLES["runtime_requirements"], kind="minimum_or_recommended")
        self.assertTrue(errors("runtime_requirements", value))

    def test_partial_network_knowledge_can_omit_unstated_network_uses(self):
        value = {"offline": "partial", "works_offline": ["editing"]}
        self.assertEqual([], errors("network", value))

    def test_sourced_empty_network_details_are_valid(self):
        value = {"offline": "partial", "works_offline": [], "needs_network_for": []}
        self.assertEqual([], errors("network", value))

    def test_provided_network_details_keep_their_types(self):
        value = {"offline": "partial", "needs_network_for": "inference"}
        self.assertTrue(errors("network", value))
        value["needs_network_for"] = ["inference"]
        value["works_offline"] = None
        self.assertTrue(errors("network", value))

    def test_unknown_fields_are_refused_everywhere(self):
        for name, value in EXAMPLES.items():
            if isinstance(value, dict):
                self.assertTrue(errors(name, dict(value, guessed=True)), name)

    def test_the_guide_names_every_shape(self):
        guide = (ROOT / "research" / "foundations" / "product-field-guide.md").read_text(encoding="utf-8")
        for name in (*EXAMPLES, "iso_date"):
            self.assertIn(f"`{name}`", guide, name)

    def test_enterprise_control_separates_existence_entitlement_enforcement_and_exercise(self):
        minimal = {"documented_status": "documented", "exercised_status": "documented_only"}
        self.assertEqual([], errors("enterprise_control_state", minimal))
        for missing in ("documented_status", "exercised_status"):
            bad = dict(minimal)
            del bad[missing]
            self.assertTrue(errors("enterprise_control_state", bad), missing)
        self.assertTrue(errors("enterprise_control_state", {**minimal, "documented_status": "unknown"}))
        self.assertTrue(errors("enterprise_control_state", {**minimal, "entitlement_scope": "all_users"}))
        self.assertTrue(errors("enterprise_control_state", {**minimal, "configured_enforcement": True}))

    def test_retention_and_sla_use_decimal_strings_when_stated_and_allow_omission(self):
        minimal_ret = {
            "data_class": "prompts_and_inputs",
            "retention_mode": "zero_data_retention",
            "state": {"documented_status": "documented", "exercised_status": "documented_only"},
        }
        self.assertEqual([], errors("data_retention", minimal_ret))
        self.assertTrue(errors("data_retention", {**minimal_ret, "duration_days": 30}))
        self.assertTrue(errors("data_retention", {**minimal_ret, "duration_days": "forever"}))
        minimal_sla = {
            "channels": ["email_ticket"],
            "state": {"documented_status": "documented", "exercised_status": "documented_only"},
        }
        self.assertEqual([], errors("support_sla", minimal_sla))
        self.assertTrue(errors("support_sla", {**minimal_sla, "uptime_sla_percent": 99.9}))

    def test_numeric_sla_promises_require_their_measurement_windows(self):
        base = copy.deepcopy(EXAMPLES["support_sla"])
        self.assertEqual([], errors("support_sla", base))
        for field in ("uptime_measurement_window", "coverage_hours"):
            bad = dict(base)
            del bad[field]
            self.assertTrue(errors("support_sla", bad), field)
        for metric, context in (("uptime_sla_percent", "uptime_measurement_window"),
                                ("first_response_hours", "coverage_hours")):
            partial = dict(base)
            del partial[metric]
            del partial[context]
            self.assertEqual([], errors("support_sla", partial), metric)
        self.assertTrue(errors("support_sla", {**base, "uptime_measurement_window": ""}))

    def test_unsupported_enterprise_claim_requires_explicit_negative_evidence(self):
        record = copy.deepcopy(FIXTURE)
        claim = next(c for c in record["claims"] if c["id"] == "claim:sso")
        claim.update(value_status="unsupported", value=False, explicit_negative_evidence=False)
        result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
        self.assertTrue(any("explicit negative evidence" in e for e in result), result)
        claim["explicit_negative_evidence"] = True
        self.assertEqual([], validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True))
        claim["value"] = {}
        result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
        self.assertTrue(any("explicit JSON false" in e for e in result), result)

    def test_assurance_retains_issuer_scope_dates_and_nonempty_limits(self):
        base = copy.deepcopy(EXAMPLES["security_assurance"])
        for missing in ("framework_or_standard", "issuer", "covered_scope", "report_access", "documentary_limits"):
            bad = copy.deepcopy(base)
            del bad[missing]
            self.assertTrue(errors("security_assurance", bad), missing)
        self.assertTrue(errors("security_assurance", {**base, "documentary_limits": []}))
        self.assertTrue(errors("security_assurance", {**base, "expires_on": "2027/10/31"}))

    def test_residency_portability_and_byok_keep_stages_and_notes_typed(self):
        self.assertTrue(errors("data_residency", {**EXAMPLES["data_residency"], "regions": []}))
        self.assertTrue(errors("data_residency", {**EXAMPLES["data_residency"], "applies_to_stages": ["everywhere"]}))
        self.assertTrue(errors("portability_deletion", {**EXAMPLES["portability_deletion"], "deletion_sla_days": 30}))
        self.assertTrue(errors("byok_byom", {**EXAMPLES["byok_byom"], "kind": "custom_crypto"}))

    def assert_fixture_shapes(self, record):
        self.assertEqual([], validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True))
        self.assertTrue(validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=False))
        checked = 0
        for claim in record["claims"]:
            shape = PART2_FIELD_TO_SHAPE.get(claim["field"])
            if not shape:
                continue
            if claim["value_status"] in ("unknown", "not_disclosed", "not_applicable", "disputed"):
                self.assertIsNone(claim["value"], claim["id"])
            elif claim["value_status"] == "unsupported":
                self.assertIs(claim["value"], False, claim["id"])
                self.assertTrue(claim["explicit_negative_evidence"])
            else:
                self.assertEqual("known", claim["value_status"], claim["id"])
                self.assertEqual([], errors(shape, claim["value"]), claim["id"])
                checked += 1
        return checked

    def test_synthetic_enterprise_fixture_satisfies_contract_and_profile_shapes(self):
        self.assertGreaterEqual(self.assert_fixture_shapes(FIXTURE), 10)

    def test_unsupported_envelope_requires_false_and_bypasses_known_object_shape(self):
        record = copy.deepcopy(FIXTURE)
        claim = next(c for c in record["claims"] if c["id"] == "claim:sso")
        claim.update(value_status="unsupported", value=False, explicit_negative_evidence=True)
        self.assertEqual(9, self.assert_fixture_shapes(record))
        for bad in (None, {}, {"documented_status": "explicitly_unavailable"}):
            claim["value"] = bad
            result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
            self.assertTrue(any("explicit JSON false" in e for e in result), result)
        claim.update(value=False, source_status="unchecked", checked_on=None)
        result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
        self.assertTrue(any("explicit negative evidence" in e for e in result), result)

    def test_documented_not_entitled_and_disabled_are_separately_scoped_claims(self):
        record = copy.deepcopy(FIXTURE)
        original = next(c for c in record["claims"] if c["id"] == "claim:sso")
        record["claims"].remove(original)
        for dimension in ("feature_exists", "plan_entitlement", "configured_enforcement"):
            claim = copy.deepcopy(original)
            claim["id"] += "-" + dimension.replace("_", "-")
            claim["scope"]["conditions"] = ["Synthetic SSO dimension=" + dimension]
            state = {"documented_status": "documented", "exercised_status": "documented_only"}
            if dimension == "plan_entitlement":
                state["entitlement_scope"] = "not_entitled"
            if dimension == "configured_enforcement":
                state["configuration_status"] = "disabled"
                claim["scope"]["conditions"].append("Synthetic configuration only; no real account tested")
            claim["value"]["state"] = state
            record["claims"].append(claim)
            self.assertEqual("known", claim["value_status"])
            self.assertEqual([], errors("enterprise_identity_access", claim["value"]))
        self.assertEqual([], validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True))
        for status in ("enabled", "disabled"):
            self.assertEqual([], errors("enterprise_control_state", {**state, "configuration_status": status}))
        for guessed in (False, "unknown", "admin_configurable"):
            self.assertTrue(errors("enterprise_control_state", {**state, "configuration_status": guessed}))

    def test_each_unknown_control_dimension_retains_null_and_scope(self):
        for dimension in ("feature_exists", "plan_entitlement", "configured_enforcement"):
            record = copy.deepcopy(FIXTURE)
            claim = next(c for c in record["claims"] if c["id"] == "claim:sso")
            claim.update(value_status="unknown", value=None)
            claim["scope"]["conditions"] = ["Synthetic SSO dimension=" + dimension]
            self.assertEqual(9, self.assert_fixture_shapes(record))
            for guessed in (False, {}, {"configuration_status": "disabled"}):
                claim["value"] = guessed
                result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
                self.assertTrue(any("must remain null" in e for e in result), result)

    def test_explicitly_unavailable_cannot_carry_configuration_status(self):
        unavailable = {"documented_status": "explicitly_unavailable", "exercised_status": "documented_only"}
        self.assertEqual([], errors("enterprise_control_state", unavailable))
        for status in ("enabled", "disabled"):
            contradictory = {**unavailable, "configuration_status": status}
            self.assertTrue(errors("enterprise_control_state", contradictory), status)
            wrapped = {**EXAMPLES["enterprise_identity_access"], "state": contradictory}
            self.assertTrue(errors("enterprise_identity_access", wrapped), status)
            record = copy.deepcopy(FIXTURE)
            claim = next(c for c in record["claims"] if c["id"] == "claim:sso")
            claim["value"]["state"] = contradictory
            result = validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True)
            self.assertTrue(any("explicitly_unavailable" in e and "configuration_status" in e for e in result), result)
        # Positive controls: documented + not_entitled and documented + disabled/enabled remain valid in both schema and intake.
        for valid_state in (
            {"documented_status": "documented", "entitlement_scope": "not_entitled", "exercised_status": "documented_only"},
            {"documented_status": "documented", "configuration_status": "disabled", "exercised_status": "documented_only"},
            {"documented_status": "documented", "configuration_status": "enabled", "exercised_status": "documented_only"},
        ):
            self.assertEqual([], errors("enterprise_control_state", valid_state))
            record = copy.deepcopy(FIXTURE)
            claim = next(c for c in record["claims"] if c["id"] == "claim:sso")
            claim["value"]["state"] = valid_state
            self.assertEqual([], validator.validate_record(record, as_of=AS_OF, taxonomy=TAXONOMY, allow_synthetic=True))


if __name__ == "__main__":
    unittest.main()
