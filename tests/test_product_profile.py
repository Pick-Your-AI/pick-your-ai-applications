"""The product comparison value shapes (schemas/product-profile.schema.json, APP-F02.03): the schema keeps to the
validator's keyword set, and synthetic values show what each shape takes and refuses. No real product is described."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("application_validation", ROOT / "scripts" / "validate_applications.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
PROFILE = json.loads((ROOT / "schemas" / "product-profile.schema.json").read_text(encoding="utf-8"))

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
        for name in EXAMPLES:
            self.assertIn(f"`{name}`", guide, name)


if __name__ == "__main__":
    unittest.main()
