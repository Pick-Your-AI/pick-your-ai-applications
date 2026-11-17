"""Reconcile coverage with local records; never certify source truth or rights."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

from validate_applications import date_value, load_json, url_errors, validate_directory, validate_record

COUNTERS = (
    "candidate_sightings_count", "deduplicated_product_count", "offering_count",
    "primary_sourced_product_count", "reviewed_product_count",
    "independently_measured_product_count", "publication_eligible_product_count",
    "published_product_count",
)


def reconcile(ledger, records, surveys=(), *, as_of=None, taxonomy=None,
              allow_synthetic=False):
    """Return per-stage global unions after checking every category's actual members.

    The synthetic switch is for unit tests only. The CLI never enables it. A
    product with one reviewed/eligible field is not a wholly verified product.
    """
    as_of = as_of or dt.datetime.now(dt.timezone.utc).date()
    rows = {row["category_id"]: row for row in ledger["rows"]}
    memberships = {cid: {key: set() for key in COUNTERS} for cid in rows}
    products = {}
    for record in records:
        errors = validate_record(record, as_of=as_of, taxonomy=taxonomy,
                                 allow_synthetic=allow_synthetic)
        if errors:
            raise ValueError("coverage requires valid application records: " + errors[0])
        pid = record["record_id"]
        if pid in products:
            raise ValueError("duplicate coverage product identity")
        products[pid] = record
        if not record["classification"]["category_ids"]:
            raise ValueError("coverage cannot omit an unclassified admitted product; resolve its researched category or retain it in notes")
        sources = {source["id"]: source for source in record["sources"]}
        claims = [claim for claim in record["claims"]
                  if claim["evidence_state"] == "active"
                  and claim["value_status"] in {"known", "unsupported"}]
        primary = any(sources[sid]["authority"] == "primary"
                      and sources[sid]["state"] == "active"
                      for claim in claims if claim["source_status"] == "checked"
                      for sid in claim["source_ids"])
        reviewed = primary and any(
            claim["source_status"] == "checked" and claim["review"]["status"] == "approved"
            and all(sources[sid]["state"] == "active" for sid in claim["source_ids"])
            for claim in claims)
        measured = primary and any(claim["evidence_grade"] == "independent_measurement"
                       and claim["verification_status"] == "verified"
                       and (claim["verification"] or {}).get("method") == "reproduced_test"
                       for claim in claims)
        state = record["publication"]["state"]
        stages = {
            "deduplicated_product_count": True,
            "primary_sourced_product_count": primary,
            "reviewed_product_count": reviewed,
            "independently_measured_product_count": measured,
            "publication_eligible_product_count": state in {"eligible", "published"},
            "published_product_count": state == "published",
        }
        for cid in record["classification"]["category_ids"]:
            if cid not in rows:
                raise ValueError("record category has no coverage row")
            for counter, qualifies in stages.items():
                if qualifies:
                    memberships[cid][counter].add(pid)
            memberships[cid]["offering_count"].update(
                (pid, entity["id"]) for entity in record["entities"]
                if entity["entity_type"] == "application_offering")

    seen_categories, sightings = set(), {}
    included = {cid: set() for cid in rows}
    for survey in surveys:
        if not isinstance(survey, dict) or set(survey) != {"schema_version", "category_id", "sightings"}:
            raise ValueError("candidate survey requires version, category and sightings")
        cid = survey["category_id"]
        if survey["schema_version"] != "0.1.0" or not isinstance(cid, str) or cid not in rows or cid in seen_categories:
            raise ValueError("candidate survey category/version is invalid or duplicated")
        seen_categories.add(cid)
        if not isinstance(survey["sightings"], list):
            raise ValueError("candidate sightings must be a list")
        for sighting in survey["sightings"]:
            required = {"id", "source_url", "accessed_on", "product_id", "disposition", "reason", "synthetic"}
            if not isinstance(sighting, dict) or set(sighting) != required:
                raise ValueError("candidate sighting requires scoped discovery metadata")
            sid = sighting["id"]
            if not isinstance(sid, str) or not sid.startswith("sighting:") or not sid[9:].strip():
                raise ValueError("candidate sighting needs a stable sighting: ID")
            if type(sighting["synthetic"]) is not bool or (sighting["synthetic"] and not allow_synthetic):
                raise ValueError("synthetic sightings cannot enter real coverage")
            errors = []
            url_errors(sighting["source_url"], "candidate source", errors, sighting["synthetic"])
            date_value(sighting["accessed_on"], "candidate access", errors, as_of)
            if errors:
                raise ValueError("invalid candidate provenance: " + errors[0])
            if not isinstance(sighting["reason"], str) or not sighting["reason"].strip():
                raise ValueError("candidate disposition needs a reason")
            disposition, pid = sighting["disposition"], sighting["product_id"]
            if disposition not in ("unresolved", "included", "excluded"):
                raise ValueError("unknown candidate disposition")
            if disposition == "included":
                if not isinstance(pid, str) or pid not in products or cid not in products[pid]["classification"]["category_ids"]:
                    raise ValueError("included candidate must resolve to a product in this category")
                included[cid].add(pid)
            elif pid is not None:
                raise ValueError("unresolved/excluded candidate must not assert an admitted product ID")
            if sid in memberships[cid]["candidate_sightings_count"]:
                raise ValueError("duplicate candidate sighting within category")
            if sid in sightings and sightings[sid] != sighting:
                raise ValueError("one sighting ID has conflicting discovery metadata")
            sightings[sid] = sighting
            memberships[cid]["candidate_sightings_count"].add(sid)

    global_members = {key: set() for key in COUNTERS}
    for cid, row in rows.items():
        if included[cid] != memberships[cid]["deduplicated_product_count"]:
            raise ValueError(f"{cid}: admitted product membership needs included discovery sightings")
        for counter in COUNTERS:
            value = row.get(counter)
            if type(value) is not int or value != len(memberships[cid][counter]):
                raise ValueError(f"{cid}: {counter} disagrees with actual record membership")
            global_members[counter].update(memberships[cid][counter])
        receipt_products = {pid for receipt in row.get("acceptance_receipts", [])
                            for pid in receipt["product_ids"]}
        if receipt_products != memberships[cid]["published_product_count"]:
            raise ValueError(f"{cid}: publication receipts name different products from the admitted records")
        basis = row.get("coverage_basis")
        if basis is not None:
            values = basis.get("numerator_product_ids") if isinstance(basis, dict) else None
            if (not isinstance(values, list) or any(not isinstance(pid, str) for pid in values)
                    or len(set(values)) != len(values)):
                raise ValueError(f"{cid}: coverage basis needs a unique string list of numerator product IDs")
            if set(values) != memberships[cid]["deduplicated_product_count"]:
                raise ValueError(f"{cid}: percentage numerator differs from actual product membership")
    return {key: len(values) for key, values in global_members.items()}


def reconcile_repository(root: Path, ledger, taxonomy, *, as_of=None):
    """Read the explicit local corpus, without network access or implicit fixtures."""
    resolution_path = root / "data/identity-resolutions.json"
    resolutions = load_json(resolution_path) if resolution_path.exists() else []
    files, errors = validate_directory(root / "data/applications", as_of=as_of,
                                      taxonomy=taxonomy, identity_resolutions=resolutions)
    if errors:
        raise ValueError("coverage requires a valid, deduplicated application corpus: " + errors[0])
    records = [load_json(path) for path in files]
    surveys = [load_json(path) for path in sorted((root / "research/candidates").glob("*.json"))]
    return reconcile(ledger, records, surveys, taxonomy=taxonomy, as_of=as_of)
