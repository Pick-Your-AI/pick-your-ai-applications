# Coverage from actual record membership

Proposed local accounting method for #76, #112 and #113. This document does not
adopt a shared consumer contract, establish a market census, or accept research.
The starting ledger remains a dated zero-product baseline.

## Survey boundaries

The full population of AI applications is unknown. Each survey declares source
families, languages, regions, industry/workflow boundaries, deployment forms,
inclusion/exclusion rules, cutoff, and a stopping/expansion rule. An enumerated
sample is a denominator only for that sample. Neither 48 categories nor the
number of issues supplies a market denominator. Unexamined languages, regions,
industries and deployment forms stay in `known_unknowns` with a next action.

`coverage_percent` is optional. When present, the existing planning validator
requires a dated enumerated denominator and recomputes the fraction. The
membership check additionally compares its numerator IDs to admitted products;
equal-sized lists of unrelated IDs are rejected. No all-AI percentage is emitted.

## Counting rules

The normal planning command reconciles these fields against local files:

| Counter | Membership |
| --- | --- |
| Candidate sightings | Distinct discovery sighting IDs, including retained excluded/unresolved leads |
| Deduplicated products | Valid `data/applications/*.json` records classified in the category and linked to included sightings |
| Offerings | Distinct `(product ID, offering entity ID)` pairs in those records |
| Primary sourced | Products with at least one active checked known/explicit-negative claim linked to active primary evidence |
| Reviewed | Primary-sourced products with at least one active checked known/explicit-negative claim, approved review metadata, and active cited sources |
| Independently measured | Primary-sourced products with an active verified independent-measurement claim and `reproduced_test` receipt |
| Publication eligible | Valid records with an explicit eligible/published field projection |
| Published | Valid published records, with category receipt product IDs equal to the actual published members |

These are evidence-depth indicators. Existing checked-claim requirements retain
their primary-source prerequisite. One reviewed, measured or eligible claim
never means every field is reviewed, measured or cleared. An eligible field may
coexist with a pending claim outside the projection. Unknown, withheld and
disputed claims retain their own states. The application validator checks receipt metadata and
permission prerequisites; it does not authenticate an external decision or
reproduce a product. Actual publication readback and receiving decisions remain
human review requirements in `HANDOFFS.md` and `REVIEW_POLICY.md`.

Global counts use the union of IDs at each stage. A product classified in two
categories contributes once globally. Offering identity is qualified by product.
Candidate sightings stay separate from product identities and may be repeated
across categories only with identical metadata. Category totals are never added
and described as a distinct-product count.

## Candidate files

Each surveyed category has one `research/candidates/<category-slug>.json` object
with `schema_version: "0.1.0"`, its `category_id`, and a `sightings` list. A
sighting has exactly `id`, `source_url`, `accessed_on`, `product_id`,
`disposition`, `reason`, and `synthetic`. IDs begin `sighting:` and remain stable.
Use actual public source URLs and actual canonical access dates. Preserve a
reason for excluded leads. `unresolved` and `excluded` have null `product_id`;
`included` references an admitted product classified in that category. Failed
reads belong in research notes and never become successful discovery evidence.

Before recording acquired material, resolve the applicable retrieval and public
Git source-use conditions under the existing rights policy. The file format is
not permission to acquire or republish a source. Incomplete product findings
remain notes; this format cannot bypass product intake requirements.

Missing candidate files mean no recorded sightings, and must reconcile to zero.
Every admitted product needs an included sighting; historical migration must
recover real provenance rather than synthesize a discovery event. Fixtures are
allowed only through an explicit unit-test parameter. The CLI rejects them.
An admitted record without a researched category fails coverage reconciliation;
it is never silently omitted from the global totals. Resolve its classification
with evidence or retain the incomplete research in notes instead of guessing.

## Reproduce the checks

Run `python3 scripts/validate_applications.py`,
`python3 scripts/validate_planning.py`, and
`python3 -m unittest discover -s tests -v`.

The planning report includes global union counts. A mismatch fails locally and
in the existing `validate` workflow. `schemas/coverage-ledger.schema.json`
describes the counter envelope; semantic checks enforce record membership,
dates, identity, receipts and bounded denominators. Exact-revision independent
review is still required. Any external consumer adoption is a separate decision.
