#!/usr/bin/env python3
"""Offline application contract validation; never certifies research facts or rights."""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import ipaddress
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
KINDS = {"application_product", "product_family", "application_release", "application_offering", "application_feature", "integration", "model", "vendor"}
USES = {"display", "cache", "export", "api", "commercial"}
VERSION = "0.1.0"
PREFIXES = {"application_product": "app:", "product_family": "family:", "application_release": "release:", "application_offering": "offering:", "application_feature": "feature:", "integration": "integration:", "model": "model:", "vendor": "vendor:"}


def fail(errors, path, message):
    errors.append(f"{path}: {message}")


def schema_errors(value, schema, path="$", root_schema=None):
    """Evaluate the JSON Schema vocabulary used by this version, without dependencies.

    This is deliberately not advertised as a general-purpose JSON Schema library.
    New contract keywords must be implemented and tested before they can be used.
    """
    errors = []
    if root_schema is None:
        root_schema = schema
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{path}: unsupported schema reference {ref}"]
        target = root_schema
        for token in ref[2:].split("/"):
            target = target[token.replace("~1", "/").replace("~0", "~")]
        errors.extend(schema_errors(value, target, path, root_schema))
    if "const" in schema and value != schema["const"]:
        fail(errors, path, f"must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        fail(errors, path, f"not an allowed value: {value!r}")
    types = schema.get("type")
    if types:
        types = [types] if isinstance(types, str) else types
        matches = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "null": value is None,
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        }
        if not any(matches.get(t, False) for t in types):
            fail(errors, path, "expected type " + "/".join(types))
            return errors
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                fail(errors, path, f"missing required property {name}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for name in value.keys() - properties.keys():
                fail(errors, path, f"unknown property {name}")
        for name, child in properties.items():
            if name in value:
                errors.extend(schema_errors(value[name], child, f"{path}.{name}", root_schema))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            fail(errors, path, "too few items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            fail(errors, path, "duplicate array items")
        for i, child in enumerate(value):
            if "items" in schema:
                errors.extend(schema_errors(child, schema["items"], f"{path}[{i}]", root_schema))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            fail(errors, path, "string too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            fail(errors, path, "string does not match required pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            fail(errors, path, "below minimum")
    for child in schema.get("allOf", []):
        errors.extend(schema_errors(value, child, path, root_schema))
    if "anyOf" in schema and not any(not schema_errors(value, s, path, root_schema) for s in schema["anyOf"]):
        fail(errors, path, "does not satisfy any allowed shape")
    if "if" in schema:
        branch = "then" if not schema_errors(value, schema["if"], path, root_schema) else "else"
        if branch in schema:
            errors.extend(schema_errors(value, schema[branch], path, root_schema))
    return errors


def check_schema_vocabulary(schema):
    allowed = {"$schema", "$id", "$ref", "$defs", "title", "description", "type", "const", "enum", "required", "properties", "additionalProperties", "items", "minItems", "uniqueItems", "minLength", "pattern", "minimum", "allOf", "anyOf", "if", "then", "else"}
    errors = []
    def walk(node, path):
        if not isinstance(node, dict):
            errors.append(f"{path}: schema node is not an object")
            return
        for key in node.keys() - allowed:
            errors.append(f"{path}: unsupported schema keyword {key}")
        for key in ("properties", "$defs"):
            for name, child in node.get(key, {}).items():
                walk(child, f"{path}/{key}/{name}")
        for key in ("items", "if", "then", "else"):
            if key in node:
                walk(node[key], f"{path}/{key}")
        for key in ("allOf", "anyOf"):
            for i, child in enumerate(node.get(key, [])):
                walk(child, f"{path}/{key}/{i}")
        if "$ref" in node:
            target = schema
            try:
                assert node["$ref"].startswith("#/")
                for token in node["$ref"][2:].split("/"):
                    target = target[token.replace("~1", "/").replace("~0", "~")]
                assert isinstance(target, dict)
            except (KeyError, AssertionError, TypeError):
                errors.append(f"{path}: unresolved local reference")
    walk(schema, "schema")
    return errors


def date_value(value, path, errors, as_of, nullable=False):
    if value is None and nullable:
        return None
    try:
        parsed = dt.date.fromisoformat(value)
        if value != parsed.isoformat():
            raise ValueError("not canonical")
        if parsed > as_of:
            fail(errors, path, "date is in the future")
        return parsed
    except (ValueError, TypeError):
        fail(errors, path, "must be a real ISO YYYY-MM-DD date")
        return None


def normalize_identity(value):
    """Comparison key only: preserve the original evidence spelling in records.

    Invisible format characters (Unicode category Cf, e.g. zero-width space, soft hyphen,
    word joiner, BOM) are removed so they cannot make one identity compare as another.
    """
    text = "".join(ch for ch in unicodedata.normalize("NFKC", value or "") if unicodedata.category(ch) != "Cf")
    return " ".join(text.strip().casefold().removeprefix("@").split())


def has_substantive_content(value):
    """Check content after the same Unicode and whitespace normalization used for identities."""
    return bool(normalize_identity(value))


def load_json(path):
    """Reject ambiguous object keys and non-JSON numbers before applying gates."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key!r}")
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError(f"non-finite JSON number: {value}")
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            invalid_constant(value)
        return number
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_pairs,
                      parse_constant=invalid_constant, parse_float=finite_float)


def url_errors(url, path, errors, synthetic=False):
    # Metadata validation only. Retrieval code must separately recheck resolved
    # addresses and every redirect; this deliberately performs no DNS/network I/O.
    try:
        if not isinstance(url, str) or not url or any(ord(c) <= 32 or ord(c) == 127 for c in url) or "\\" in url:
            raise ValueError()
        p = urlsplit(url)
        if p.scheme not in {"http", "https"} or not p.hostname or p.username is not None or p.password is not None or p.query:
            raise ValueError()
        _ = p.port  # Invalid/out-of-range ports must not escape validation.
        host = p.hostname.rstrip(".").lower()
        if "%" in host:
            raise ValueError()
        if ":" not in host:
            host = host.encode("idna").decode("ascii").lower()
        if host == "localhost" or host.endswith((".localhost", ".local", ".internal", ".lan", ".home")):
            raise ValueError()
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = None
        if address is not None:
            if not address.is_global or address.is_multicast or address.is_reserved:
                raise ValueError()
            mapped = getattr(address, "ipv4_mapped", None)
            if mapped is not None and not mapped.is_global:
                raise ValueError()
        else:
            # Browsers accept integer, octal, hexadecimal and short IPv4 forms.
            # Reject these ambiguous numeric hosts, rather than resolving them.
            if "." not in host or re.fullmatch(r"(?:0x[0-9a-f]+|[0-9]+)", host.rsplit(".", 1)[-1]):
                raise ValueError()
            labels = host.split(".")
            if len(host) > 253 or any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in labels):
                raise ValueError()
        if not synthetic and (host.endswith((".invalid", ".test", ".example")) or host in {"example.com", "example.org", "example.net"}):
            raise ValueError()
    except (ValueError, TypeError, UnicodeError):
        fail(errors, path, "needs a stable public HTTP(S) URL, without credentials or query parameters; fixture URLs are test-only")


def unique_map(items, key, path, errors):
    result = {}
    for item in items:
        value = item[key]
        if value in result:
            fail(errors, path, f"duplicate {key}: {value}")
        result[value] = item
    return result


def validate_record(record, *, as_of=None, allow_synthetic=False, taxonomy=None):
    as_of = as_of or dt.datetime.now(dt.timezone.utc).date()
    schema = load_json(SCHEMA_DIR / "application.schema.json")
    errors = check_schema_vocabulary(schema) + schema_errors(record, schema)
    if errors:
        return errors
    def finite_json(value, path):
        if isinstance(value, float) and not math.isfinite(value):
            fail(errors, path, "non-finite numbers are not valid JSON research values")
        elif isinstance(value, dict):
            for key, child in value.items():
                finite_json(child, path + "." + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                finite_json(child, f"{path}[{index}]")
    finite_json(record, "$")
    synthetic = record["synthetic"]
    if synthetic and not allow_synthetic:
        fail(errors, "$", "synthetic data is restricted to tests/fixtures")
    if record["entity_type"] != "application_product":
        fail(errors, "$", "models, integrations, releases and offerings cannot masquerade as application products")
    identity = record["identity"]
    for key in ("name", "vendor_name"):
        if not normalize_identity(identity[key]):
            fail(errors, "identity", f"{key} must not be blank")
    if any(not normalize_identity(alias) for alias in identity["aliases"]):
        fail(errors, "identity", "aliases must not be blank")
    if identity["canonical_url"] is not None:
        url_errors(identity["canonical_url"], "identity.canonical_url", errors, synthetic)
    if record["record_id"] != identity["product_id"]:
        fail(errors, "identity", "record_id must equal the product_id")
    for key, kind in (("product_id", "application_product"), ("vendor_id", "vendor"), ("family_id", "product_family")):
        if identity[key] is not None and not identity[key].startswith(PREFIXES[kind]):
            fail(errors, "identity", f"{key} must use the {PREFIXES[kind]} namespace")
    refs = {identity["product_id"]: "application_product", identity["vendor_id"]: "vendor"}
    if identity["family_id"]:
        refs[identity["family_id"]] = "product_family"
    for node in record["entities"]:
        if node["id"] in refs:
            fail(errors, "entities", "duplicate or ambiguous entity identity " + node["id"])
        refs[node["id"]] = node["entity_type"]
        if not node["id"].startswith(PREFIXES[node["entity_type"]]):
            fail(errors, "entities", "entity ID namespace must match entity kind")
        if node["url"] is not None:
            url_errors(node["url"], "entities." + node["id"] + ".url", errors, synthetic)
        if node["entity_type"] in {"application_release", "application_offering", "application_feature"} and node["product_id"] != identity["product_id"]:
            fail(errors, "entities", "child release/offering/feature must identify this product")
        if node["entity_type"] == "application_release" and node["version"] is None:
            fail(errors, "entities", "release identity requires a concrete version")
    sources = unique_map(record["sources"], "id", "sources", errors)
    claims = unique_map(record["claims"], "id", "claims", errors)
    rights = unique_map(record["rights_decisions"], "id", "rights_decisions", errors)
    for sid, source in sources.items():
        url_errors(source["url"], f"sources.{sid}.url", errors, synthetic)
        date_value(source["accessed_on"], f"sources.{sid}.accessed_on", errors, as_of)
    for cid, claim in claims.items():
        path = f"claims.{cid}"
        subject = claim["subject"]
        if refs.get(subject["id"]) != subject["entity_type"]:
            fail(errors, path, "claim subject must resolve to an exact registered entity and kind")
        offering = claim["scope"]["offering_id"]
        if offering is not None and refs.get(offering) != "application_offering":
            fail(errors, path, "scoped offering_id must resolve to a registered application offering for this product")
        if offering is not None and subject["entity_type"] == "application_offering" and subject["id"] != offering:
            fail(errors, path, "offering subject and scoped offering_id must agree")
        if not normalize_identity(claim["researcher"]):
            fail(errors, path, "researcher must not be blank")
        missing = set(claim["source_ids"]) - sources.keys()
        if missing:
            fail(errors, path, "unresolved source IDs: " + ", ".join(sorted(missing)))
        if claim["value_status"] in {"unknown", "not_disclosed", "not_applicable", "disputed"}:
            if claim["value"] is not None:
                fail(errors, path, "unknown, disputed or inapplicable values must remain null, never zero or false")
            if claim["verification_status"] != "unverified":
                fail(errors, path, "unknown/disputed/inapplicable cannot be independently verified")
        elif claim["value"] is None:
            fail(errors, path, "known/unsupported claims require an explicit value")
        if claim["value_status"] == "unsupported" and (claim["source_status"] != "checked" or not claim["explicit_negative_evidence"]):
            fail(errors, path, "unsupported needs checked explicit negative evidence; omission is unknown")
        if claim["value_status"] == "unsupported" and claim["value"] is not False:
            fail(errors, path, "unsupported claims must use the explicit JSON false value")
        if claim["source_status"] == "checked":
            if not claim["source_ids"] or not any(sources[s]["authority"] == "primary" for s in claim["source_ids"] if s in sources):
                fail(errors, path, "checked claims require primary source evidence")
            date_value(claim["checked_on"], path + ".checked_on", errors, as_of)
            for sid in claim["source_ids"]:
                if sid in sources and claim["checked_on"] is not None and sources[sid]["accessed_on"] > claim["checked_on"]:
                    fail(errors, path, "source access date is later than claim check")
        elif claim["checked_on"] is not None:
            fail(errors, path, "unchecked claim cannot have a checked date")
        if claim["temporal_scope"] == "version_pinned" and not has_substantive_content(claim["version"]):
            fail(errors, path, "version-pinned facts need a concrete version")
        if claim["temporal_scope"] == "current_state" and claim["source_status"] == "checked" and claim["as_of"] != claim["checked_on"]:
            fail(errors, path, "current-state facts must display their checked date as as_of")
        date_value(claim["as_of"], path + ".as_of", errors, as_of, nullable=True)
        review = claim["review"]
        if review["reviewed_on"] is not None:
            date_value(review["reviewed_on"], path + ".reviewed_on", errors, as_of)
        if review["status"] == "approved":
            if not normalize_identity(review["reviewer"]) or normalize_identity(review["reviewer"]) == normalize_identity(claim["researcher"]):
                fail(errors, path, "approved claim requires a reviewer other than its researcher")
            reviewed = date_value(review["reviewed_on"], path + ".reviewed_on", errors, as_of)
            checked = date_value(claim["checked_on"], path + ".checked_on", errors, as_of, nullable=True)
            if reviewed and checked and reviewed < checked:
                fail(errors, path, "review predates the latest source check")
            if review["decision_url"] is None:
                fail(errors, path, "approved review requires a decision receipt")
            else:
                url_errors(review["decision_url"], path + ".decision_url", errors, synthetic)
        verification = claim["verification"]
        if claim["verification_status"] == "verified":
            if claim["source_status"] != "checked" or verification is None:
                fail(errors, path, "verified requires checked provenance plus independent verification receipt")
            else:
                if not verification["independent"]:
                    fail(errors, path, "vendor measurements are not independent verification")
                if not normalize_identity(verification["verifier"]) or normalize_identity(verification["verifier"]) == normalize_identity(claim["researcher"]):
                    fail(errors, path, "verification must be independent of the claim researcher")
                if normalize_identity(verification["verifier"]) in {normalize_identity(identity["vendor_name"]), *(normalize_identity(sources[s]["publisher"]) for s in claim["source_ids"] if s in sources and sources[s]["authority"] == "primary")}:
                    fail(errors, path, "verification must be independent of the product vendor")
                verified = date_value(verification["verified_on"], path + ".verified_on", errors, as_of)
                if verified and claim["checked_on"] is not None and verified.isoformat() < claim["checked_on"]:
                    fail(errors, path, "verification predates latest claim check")
                url_errors(verification["receipt_url"], path + ".receipt_url", errors, synthetic)
                if not has_substantive_content(verification["limitations"]):
                    fail(errors, path, "verification receipts require their limitations")
                if verification["method"] == "reproduced_test" and not has_substantive_content(verification["protocol_version"]):
                    fail(errors, path, "reproduced tests require a pinned protocol version")
                if verification["method"] == "independent_second_source":
                    vs = verification["source_id"]
                    if vs not in sources or sources.get(vs, {}).get("authority") != "independent" or vs not in claim["source_ids"]:
                        fail(errors, path, "second-source verification needs a cited independent source")
                    elif normalize_identity(sources[vs]["publisher"]) in {normalize_identity(identity["vendor_name"]), *(normalize_identity(sources[s]["publisher"]) for s in claim["source_ids"] if s in sources and sources[s]["authority"] == "primary")}:
                        fail(errors, path, "independent source publisher cannot be the product vendor or primary publisher")
        elif verification is not None:
            fail(errors, path, "unverified claims must not carry a verification receipt")
        if claim["evidence_grade"] == "independent_measurement":
            if claim["verification_status"] != "verified" or verification is None:
                fail(errors, path, "independent_measurement requires a valid independent verification receipt, not vendor documentation alone")
            if not has_substantive_content(claim["method_and_limitations"]):
                fail(errors, path, "independent_measurement requires method and limitations")
        if claim["evidence_grade"] == "estimate" and not has_substantive_content(claim["method_and_limitations"]):
            fail(errors, path, "estimates require method, assumptions and limitations")
        if claim["fact_type"] == "pricing" and claim["value_status"] == "known":
            value = claim["value"]
            price_schema = load_json(SCHEMA_DIR / "pricing.schema.json")
            errors.extend(schema_errors(value, price_schema, path + ".value"))
            if not isinstance(value, dict) or schema_errors(value, price_schema):
                continue
            date_value(value["effective_on"], path + ".value.effective_on", errors, as_of)
            if refs.get(value["offering_id"]) != "application_offering":
                fail(errors, path, "pricing requires an exact registered application offering")
            if offering is not None and offering != value["offering_id"]:
                fail(errors, path, "priced offering and scoped offering_id must agree")
            if subject["id"] != value["offering_id"]:
                fail(errors, path, "price subject must be the priced offering")
            if claim["temporal_scope"] != "current_state":
                fail(errors, path, "pricing is current-state, never timeless")
            if value["amount_status"] == "known" and value["amount"] is None:
                fail(errors, path, "known price requires a decimal amount, including sourced zero")
            if value["amount_status"] == "known" and (not value["currency"] or not value["regions"] or not value["billing_period"] or not value["meter"] or not value["commitment"]):
                fail(errors, path, "known price needs currency, region, meter, period and commitment")
            if value["amount_status"] != "known" and value["amount"] is not None:
                fail(errors, path, "unknown/contact-sales/custom price must not invent an amount")
    for rid, right in rights.items():
        path = f"rights.{rid}"
        if right["source_id"] not in sources:
            fail(errors, path, "rights decision references an unknown source")
        date_value(right["decided_on"], path + ".decided_on", errors, as_of)
        if right["expires_on"] is not None:
            try:
                dt.date.fromisoformat(right["expires_on"])
            except ValueError:
                fail(errors, path, "expires_on must be a real date")
        if right["decision"] == "allowed":
            if not has_substantive_content(right["reviewer"]) or not right["decision_url"]:
                fail(errors, path, "allowed source use requires reviewer and decision receipt")
        if right["decision_url"]:
            url_errors(right["decision_url"], path + ".decision_url", errors, synthetic)
    relation_targets = {
        "renamed_from": {"application_product"}, "replaces": {"application_product"},
        "replaced_by": {"application_product"}, "fork_of": {"application_product"},
        "discontinued_successor": {"application_product"}, "member_of": {"product_family"},
        "sold_by": {"vendor"}, "uses_model": {"model"},
        "integrates_with": {"integration", "application_product"},
    }
    for relation in record["relationships"]:
        if relation["target_entity_type"] not in relation_targets[relation["relation"]]:
            fail(errors, "relationships", "target entity kind is invalid for relationship " + relation["relation"])
        if relation["target_id"] == identity["product_id"]:
            fail(errors, "relationships", "self relationship is not a product identity distinction")
        if not relation["target_id"].startswith(PREFIXES[relation["target_entity_type"]]):
            fail(errors, "relationships", "target identity namespace must match kind")
        for cid in relation["claim_ids"]:
            if cid not in claims:
                fail(errors, "relationships", "relationship has unresolved evidence claim")
    for cid in record["classification"]["classification_claim_ids"]:
        if cid not in claims or claims[cid]["fact_type"] != "classification":
            fail(errors, "classification", "classification claim must resolve to a classification assertion")
    if taxonomy is not None:
        category_ids = {c["id"] for c in taxonomy["categories"]}
        for cid in record["classification"]["category_ids"]:
            if cid not in category_ids:
                fail(errors, "classification", "category ID is not in the current taxonomy: " + cid)
        for claim in record["claims"]:
            if claim["field"].startswith("facets.") and claim["value_status"] == "known":
                name = claim["field"].split(".", 1)[1]
                vocabulary = taxonomy["facets"].get(name)
                if vocabulary is None:
                    fail(errors, "classification", "facet is not in the current taxonomy: " + name)
                elif isinstance(vocabulary, list):
                    values = claim["value"] if isinstance(claim["value"], list) else [claim["value"]]
                    if any(v not in vocabulary for v in values):
                        fail(errors, "classification", "facet value is not in the current taxonomy: " + name)
    publication = record["publication"]
    if publication["state"] in {"eligible", "published"} and not publication["fields"]:
        fail(errors, "publication", "eligible/published requires explicit admitted fields; never whole-record clearance")
    seen_fields = set()
    seen_scopes = set()
    for field in publication["fields"]:
        cid = field["claim_id"]
        if cid in seen_fields:
            fail(errors, "publication", "duplicate publication claim " + cid)
        seen_fields.add(cid)
        if cid not in claims:
            fail(errors, "publication", "unknown claim " + cid)
            continue
        claim = claims[cid]
        if field["display_verification_status"] != claim["verification_status"] or field["display_evidence_grade"] != claim["evidence_grade"]:
            fail(errors, "publication", "display grade/status must preserve the claim's actual evidence grade")
        if publication["state"] not in {"eligible", "published"}:
            continue
        scope_key = json.dumps([claim["subject"], claim["field"], claim["version"], claim["scope"]], sort_keys=True)
        if scope_key in seen_scopes:
            fail(errors, "publication", "multiple claims for the same exact field/scope require explicit conflict reconciliation")
        seen_scopes.add(scope_key)
        if claim["value_status"] not in {"known", "unsupported"} or claim["source_status"] != "checked" or claim["review"]["status"] != "approved":
            fail(errors, "publication", "published facts must be checked and independently reviewed; unknown remains unknown outside admitted facts")
        if claim["evidence_state"] != "active":
            fail(errors, "publication", "withdrawn, superseded or recheck-required evidence cannot be published")
        for sid in claim["source_ids"]:
            if sid in sources and sources[sid]["state"] != "active":
                fail(errors, "publication", "inactive source cannot support publication")
            for use in field["uses"]:
                authorized = False
                for rid in field["rights_decision_ids"]:
                    right = rights.get(rid)
                    if right is None:
                        fail(errors, "publication", "unknown rights decision " + rid)
                        continue
                    expires = right["expires_on"]
                    if right["decision"] == "allowed" and right["source_id"] == sid and claim["field"] in right["fields"] and use in right["uses"] and (expires is None or expires >= as_of.isoformat()):
                        authorized = True
                if not authorized:
                    fail(errors, "publication", f"no current field-specific {use} rights for {cid} / {sid}")
    if publication["state"] == "published":
        if publication["release_url"] is None or publication["consumer_acceptance_url"] is None:
            fail(errors, "publication", "published requires immutable release and consumer acceptance receipts")
        for key in ("release_url", "consumer_acceptance_url"):
            if publication[key]:
                url_errors(publication[key], "publication." + key, errors, synthetic)
    return errors


def validate_directory(path, *, as_of=None, taxonomy=None, identity_resolutions=None):
    errors = []
    identities = {}
    urls = {}
    names = {}
    files = sorted(path.glob("*.json")) if path.exists() else []
    for file in files:
        try:
            record = load_json(file)
        except (ValueError, OSError) as exc:
            errors.append(f"{file}: {exc}")
            continue
        record_errors = validate_record(record, as_of=as_of, taxonomy=taxonomy)
        errors.extend(f"{file}: {error}" for error in record_errors)
        if record_errors:
            continue
        rid = record["record_id"]
        if rid in identities:
            errors.append(f"{file}: duplicate product identity also in {identities[rid]}")
        identities[rid] = str(file)
        for name in [record["identity"]["name"], *record["identity"]["aliases"]]:
            names.setdefault(normalize_identity(name), set()).add(rid)
        url = record["identity"]["canonical_url"]
        if url is not None:
            parts = urlsplit(url)
            normalized = parts._replace(scheme=parts.scheme.lower(), netloc=parts.netloc.lower(), path=parts.path.rstrip("/")).geturl()
            if normalized in urls:
                errors.append(f"{file}: duplicate canonical URL; resolve aliases/rebrands against {urls[normalized]}")
            urls[normalized] = str(file)
    resolutions = {}
    if identity_resolutions is None:
        identity_resolutions = []
    if not isinstance(identity_resolutions, list):
        errors.append("identity resolutions must be a list of explicit reviewed decisions")
        identity_resolutions = []
    for resolution in identity_resolutions:
        before = len(errors)
        if not isinstance(resolution, dict) or not {"normalized_name", "product_ids", "decision", "researcher", "reviewer", "reviewed_on", "decision_url"} <= resolution.keys():
            errors.append("identity resolution requires scoped product IDs and review metadata")
            continue
        name, product_ids = resolution["normalized_name"], resolution["product_ids"]
        if not isinstance(name, str) or not name or name != normalize_identity(name) or name in resolutions:
            errors.append("identity resolution name must be unique and normalized")
            continue
        if not isinstance(product_ids, list) or any(not isinstance(x, str) for x in product_ids) or len(set(product_ids)) != len(product_ids) or set(product_ids) != names.get(name, set()) or len(product_ids) < 2:
            errors.append("identity resolution must match all colliding product IDs exactly")
        if resolution["decision"] != "distinct_products":
            errors.append("duplicate/rebranded identities must be consolidated, not counted through a resolution")
        researcher, reviewer = resolution["researcher"], resolution["reviewer"]
        if not isinstance(researcher, str) or not isinstance(reviewer, str) or not normalize_identity(researcher) or not normalize_identity(reviewer) or normalize_identity(researcher) == normalize_identity(reviewer):
            errors.append("identity resolution requires an independent reviewer")
        date_value(resolution["reviewed_on"], "identity resolution reviewed_on", errors, as_of or dt.datetime.now(dt.timezone.utc).date())
        url_errors(resolution["decision_url"], "identity resolution decision_url", errors)
        if len(errors) == before:
            resolutions[name] = set(product_ids)
    for name, product_ids in names.items():
        if len(product_ids) > 1 and resolutions.get(name) != product_ids:
            errors.append(f"unresolved name/alias collision {name!r}: {', '.join(sorted(product_ids))}; consolidate or supply an independently reviewed distinct-products decision")
    return files, errors


def price_observation_key(claim, sources):
    """Identify a repeated observation, even when a copy is assigned a new ID."""
    fields = ("subject", "field", "value_status", "value", "version", "scope", "as_of", "checked_on")
    source_urls = {source["id"]: source["url"] for source in sources}
    evidence = sorted(source_urls.get(sid, sid) for sid in claim["source_ids"])
    return json.dumps([[claim[key] for key in fields], evidence], sort_keys=True, ensure_ascii=False)


def validate_pricing_record(record, applications, *, as_of=None, allow_synthetic=False):
    """Validate separate price evidence against its canonical product and offering."""
    schema = load_json(SCHEMA_DIR / "pricing-record.schema.json")
    errors = check_schema_vocabulary(schema) + schema_errors(record, schema)
    if errors:
        return errors
    application = applications.get(record["application_id"])
    if application is None:
        return ["pricing: application_id does not resolve to a valid canonical application record"]
    offerings = {entity["id"] for entity in application["entities"] if entity["entity_type"] == "application_offering"}
    if record["offering_id"] not in offerings:
        errors.append("pricing: offering_id must already be declared by the canonical application")
    if record["claim"]["fact_type"] != "pricing":
        errors.append("pricing: standalone pricing records must contain a pricing claim")
    if record["claim"]["subject"] != {"id": record["offering_id"], "entity_type": "application_offering"}:
        errors.append("pricing: the claim subject must be the exact offering_id")
    observation = price_observation_key(record["claim"], record["sources"])
    for existing in application["claims"]:
        if existing["id"] == record["claim"]["id"] or (existing["fact_type"] == "pricing" and price_observation_key(existing, application["sources"]) == observation):
            errors.append("pricing: observation duplicates a claim embedded in the canonical application")
    if record["synthetic"] != application["synthetic"]:
        errors.append("pricing: synthetic and real identities may not be mixed")
    if record["publication"]["state"] == "published" and application["publication"]["state"] not in {"eligible", "published"}:
        errors.append("pricing: published pricing requires an admitted parent application")
    # Reuse precisely the same claim/source/rights gates; do not invent identity
    # facts or maintain an inconsistent second implementation of evidence checks.
    envelope = copy.deepcopy(application)
    envelope.update(synthetic=record["synthetic"], claims=[record["claim"]], sources=record["sources"], rights_decisions=record["rights_decisions"], publication=record["publication"], known_unknowns=record["known_unknowns"], research_notes=record["research_notes"], relationships=[], classification={"category_ids": [], "facet_notes": [], "classification_claim_ids": []})
    errors.extend(validate_record(envelope, as_of=as_of, allow_synthetic=allow_synthetic))
    return errors


def validate_pricing_directory(path, applications, *, as_of=None):
    files = sorted(path.glob("*.json")) if path.exists() else []
    errors, ids, claim_ids, observations = [], set(), set(), set()
    for file in files:
        try:
            record = load_json(file)
        except (ValueError, OSError) as exc:
            errors.append(f"{file}: {exc}")
            continue
        failures = validate_pricing_record(record, applications, as_of=as_of)
        errors.extend(f"{file}: {error}" for error in failures)
        if failures:
            continue
        if record["record_id"] in ids:
            errors.append(f"{file}: duplicate price observation record ID")
        ids.add(record["record_id"])
        cid = (record["application_id"], record["claim"]["id"])
        observation = (record["application_id"], price_observation_key(record["claim"], record["sources"]))
        if cid in claim_ids or observation in observations:
            errors.append(f"{file}: duplicate standalone price observation")
        claim_ids.add(cid)
        observations.add(observation)
    return files, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "applications")
    parser.add_argument("--pricing-dir", type=Path, default=ROOT / "data" / "pricing")
    parser.add_argument("--taxonomy", type=Path, default=ROOT / "taxonomy" / "taxonomy.json")
    parser.add_argument("--identity-resolutions", type=Path, default=ROOT / "data" / "identity-resolutions.json")
    parser.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.datetime.now(dt.timezone.utc).date())
    args = parser.parse_args()
    errors = []
    for file in sorted(SCHEMA_DIR.glob("*.schema.json")):
        errors.extend(f"{file}: {e}" for e in check_schema_vocabulary(load_json(file)))
    taxonomy = load_json(args.taxonomy) if args.taxonomy.exists() else None
    resolutions = load_json(args.identity_resolutions) if args.identity_resolutions.exists() else []
    files, data_errors = validate_directory(args.data_dir, as_of=args.as_of, taxonomy=taxonomy, identity_resolutions=resolutions)
    errors.extend(data_errors)
    applications = {}
    if not data_errors:
        applications = {record["record_id"]: record for record in (load_json(file) for file in files)}
    pricing_files, pricing_errors = validate_pricing_directory(args.pricing_dir, applications, as_of=args.as_of)
    errors.extend(pricing_errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Application contract {VERSION}: {len(files)} real application records and {len(pricing_files)} pricing records structurally valid; no evidence, rights or capability verification performed.")
    if not files:
        print("No real product research has been admitted. Empty intake is valid scaffolding, not catalog coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
