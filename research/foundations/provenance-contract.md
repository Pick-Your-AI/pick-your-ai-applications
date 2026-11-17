# Evidence entities and observation proposal

Refs #71, #102, #103. Proposed on 2026-11-17 against application intake
`0.1.0` at `19f6cf2c23668e1b426882ab3c2be8cfce1f899e`.
This decision proposal records contract design, not completed product research,
source access, independent review, rights approval or consumer acceptance.

## Authority and compatibility

The existing [`application.schema.json`](../../schemas/application.schema.json)
and [`validate_applications.py`](../../scripts/validate_applications.py) remain
responsible for admitted application records. The new standalone
[`claim.schema.json`](../../schemas/claim.schema.json) and
[`source.schema.json`](../../schemas/source.schema.json) reproduce their inline
shapes exactly. The claim schema includes its transitive local subject, review
and verification definitions. All references are local; no schema fetch occurs.
Tests compare the definitions and validation results so future drift requires an
explicit version/compatibility decision. These files do not change research's
frozen `contracts/v1` or introduce standalone claim/source intake directories.

A claim binds a subject, field, value status and product/version/plan/platform/
region/locale conditions to sources, dates and evidence grade. Unknown and
disputed values remain null under the existing semantic checks. Source records
represent dated documentary locators, with active, unavailable, withdrawn or
superseded states. A failed attempt is not evidence of a product's absence,
unsupported behavior or a completed source check.

## Proposed observation sidecar

[`observation.schema.json`](../../schemas/observation.schema.json) introduces
`application_observation_proposal` with schema version `0.1.0-proposal` and an
`observation:` identifier. It is a separately identified research sidecar proposal,
not an admitted application, a claim value or an export format. There is no
observation ingestion command or production sidecar directory in this change.

Each attempt names its researcher, subject, field, scope, version/channel,
source locator, attempted date, outcome and limitations. Nullable scope fields
preserve unknown conditions; notes explain applicability. A `failed_access`
attempt has no checked date, source-record link or claim links. Its access note
explains what failed without guessing source content. A hypothetical `checked`
attempt requires a checked date, source ID and claim links. Schema acceptance
alone cannot establish that access actually occurred or those links resolve.

Keep earlier attempts immutable. A later observation lists the older identifiers
in `supersedes_observation_ids`; the older observation can be marked superseded
with a retained audit explanation. Disputed attempts link counterpart observation
IDs in `disputes_observation_ids` and describe both positions in their access note
and limitations. Normalize units, plan, release, region and observation date
before treating positions as contradictory. Preserve withdrawn attempts and
source dates. History links convey no winning fact or publication permission.

Observation review assesses the attempt record. It is separate from a claim's
`verification` receipt, whose independent verifier and pinned protocol or second
source remain subject to existing semantic gates. An observation cannot carry a
verification status or grant rights. A reviewer is never silently substituted
for an independent verifier. A checked vendor document remains unverified unless
the separate claim evidence satisfies the existing verification rules.

## Validation boundary and receiving questions

The three schemas use only the vocabulary supported by the existing offline
validator. Shapes cannot enforce real calendar dates, stable public locator
safety, actual source access, identity independence, chronological ordering,
reference existence or an acyclic observation history. Standalone claim/source
shape checks also do not replace existing application semantic validation.
Tests deliberately demonstrate this boundary rather than implying enforcement.

Before adopting the observation sidecar, the integrator must define its storage
and loading boundary and implement calendar/URL checks, researcher/reviewer
identity checks, source/claim/subject reference resolution, checked-date ordering,
self-link/cycle rejection and scoped history reconciliation. It must specify how
source withdrawal affects linked observations and admitted claims without losing
history. No existing validator, schema or publication gate is changed here.

Source/field/intended-use decisions still follow
[`RESEARCH_WORKFLOW.md`](../../docs/RESEARCH_WORKFLOW.md) and
[`APPLICATION_CONTRACT.md`](../../docs/APPLICATION_CONTRACT.md).
Neither public access nor a source shape supplies display, cache, export, API or
commercial permission. The repository's
[`REVIEW_POLICY.md`](../../docs/REVIEW_POLICY.md) requires non-author review of
the exact revision and affected receiving-owner review. Any shared adoption
requires the separate versioned proposal described in issue #71; research #40
and #41 links are informational, not newly declared native blockers.

Acceptance remains pending. This change supplies original design prose and
synthetic offline tests only. It contains no actual observation, source-check
receipt, review approval, rights receipt or independently verified product claim.
Consumer adoption, real-source evidence, source-use decisions and exact-revision
review must be recorded separately before those outcomes are asserted.
