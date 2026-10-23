# Research-integrity validation hardening

PR #136 follow-up, October 23, 2026. These rules validate metadata consistency;
passing tests is not a factual verification, rights grant, reviewer authentication,
publication event or authorization to merge. No real product records are added.

## Claims, prices and identity

A non-null `claim.scope.offering_id` must resolve to this product's declared
`application_offering`. An offering subject, scoped offer and priced offer cannot
contradict one another. Null scope remains valid for genuinely product-wide facts.

For independence comparisons, researcher/reviewer/verifier and publisher names are
normalized using Unicode NFKC, case folding, trimmed/collapsed whitespace and an
optional leading `@`. Original spelling is retained. Blank identities are rejected.
This prevents spelling variations from satisfying a non-author gate; it does not
prove two different names belong to different people. Reviewers must still check
actual identity and conflicts. Every non-null review date is validated, including
pending and rejected reviews.

`unsupported` is an explicit JSON **false** with checked negative evidence. It is
not `0`, `"false"`, a truthy value or an empty container. Unknown/disputed/inapplicable
values continue to be null. An `independent_measurement` grade requires the existing
verified-evidence gate: an independent verifier and either a pinned reproduced-test
receipt or a cited independent source, with method and limitations. A source labeled
independent cannot simultaneously identify the vendor/primary publisher as its
publisher. A source check alone is not independent measurement.

Relationship verbs constrain target types. Rename/replacement/fork/successor
relations target products; `member_of` targets a family; `sold_by` a vendor;
`uses_model` a model; `integrates_with` an integration or another application.
These links remain evidence-qualified, not compatibility guarantees.

Standalone prices must not repeat a claim embedded in the canonical application.
A new observation or claim ID cannot evade detection of the same scoped observation
and evidence URLs. Multiple standalone files are checked for duplicate claim IDs
within one product and equivalent observation content. Distinct dated observations
and genuinely different offerings remain separate. Source/review/rights gates still
apply, and no price is admitted because a uniqueness check passed.

## Ambiguous JSON and public locators

Application, pricing, schema and command-line taxonomy inputs reject duplicate
object keys (including escaped spellings), NaN, infinities and numeric overflow.
There is no silently accepted first/last-key interpretation.

URL validation normalizes trailing DNS dots and IDNA hostnames, rejects local and
reserved addresses, and rejects ambiguous integer, octal, hexadecimal and shortened
IPv4 representations. Credentials, query parameters, invalid ports, whitespace,
controls and backslashes remain disallowed. Test-only reserved domains require
`synthetic: true`. This is offline metadata validation, **not** a network-fetch or
SSRF defense: any future retriever must check resolved addresses and each redirect.

## Names and aliases across product records

Normalized names and aliases are indexed across the application intake directory.
A collision is not automatically a duplicate, but it cannot silently count as two
products. Consolidate actual rebrands/aliases into their canonical record. Genuine
name-sharing by distinct products requires an explicit independently reviewed
resolution in optional `data/identity-resolutions.json` (or `--identity-resolutions`).
This file is an array of objects containing:

- `normalized_name`: exact normalized collision key.
- `product_ids`: all and only the distinct canonical IDs in that collision.
- `decision`: `distinct_products` (not a way to preserve duplicated/rebranded rows).
- `researcher`, `reviewer`, `reviewed_on`, `decision_url`: independent, dated decision metadata and a stable public decision reference.

The resolution does not override duplicate canonical URLs, product IDs, source
rights or claim evidence. No real resolution is fabricated in the empty scaffold.

## Coverage receipts and percentages

`acceptance_receipts` remains an empty array for the zero-start ledger. Nonempty
entries must be objects with `receipt_url`, `artifact_commit`, `consumer_commit`,
`product_ids`, `category_id`, `reviewer` and `accepted_on`. Receipt URLs identify a
canonical GitHub PR/issue decision or a file at a 40-character immutable commit.
Both commit fields are exact lowercase 40-character hashes. Product IDs are unique
canonical `app:` IDs, the category matches the row, and the acceptance date is real
and nonfuture. The union of receipt product IDs must equal `published_product_count`;
a truthy string or the same product repeated cannot support an inflated count.

These checks examine declared metadata only. Actual acceptance, artifact content
and public website readback remain independently reviewed delivery evidence.

Any `coverage_percent`, `coverage_percentage` or `market_coverage_percent` needs
nonempty source sets, an explicit bounded denominator definition and a real
nonfuture survey cutoff. `coverage_basis` supplies `numerator_product_ids` and
`denominator_product_ids`, both unique canonical ID lists. The denominator is
nonempty, the numerator is a subset and its size matches the deduplicated-product
count. Percentage values must be finite numbers in [0, 100] and equal the computed
ratio (within 1e-9 numerical tolerance); round only at display time. Such a percentage
covers that enumerated survey, never the open-world total of all AI applications.

## Safe provisioning resumption

Before `--apply` makes remote calls, `provision_github.py` creates the ignored local
`.bootstrap-started.json` marker even when `--state` points outside the repository.
The marker contains no credential or checkpoint path. Exact-scaffold comparisons
exclude it. Do not remove the marker merely to force regeneration.

The renderer refuses to regenerate a plan with a local marker, a default checkpoint,
live GitHub identifiers, or `planning/GITHUB_ESTABLISHMENT_RECEIPT.json`. For a legacy
external checkpoint created before this safeguard, also supply
`python scripts/render_backlog.py --state /absolute/path/to/checkpoint.json`;
`--state` may be repeated. Unknown external checkpoints cannot be discovered by an
offline renderer; operators must declare them. A fresh unprovisioned plan can still
be rendered. None of these safeguards grants GitHub access or changes live triage.
