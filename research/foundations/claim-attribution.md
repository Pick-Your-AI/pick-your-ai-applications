# APP-F03.02 — Atomic claim attribution and contradiction decisions (proposal)

Refs #73, #106, #107. This method explains how to record conflicting or superseded application claims. It creates **no real product evidence, accepted source-use grant, resolved conflict or consumer publication decision**. The local [application contract](../../docs/APPLICATION_CONTRACT.md), [review policy](../../docs/REVIEW_POLICY.md) and shared research #41 source policies remain authoritative.

## User decision

When two sources appear to disagree, can the researcher show precisely **which product, offering, release, region, field, conditions and time each source describes** before calling the facts contradictory? Where an actual conflict remains, record all positions, the evidence and the accountable next action rather than silently selecting a favorable value.

## 1. Provenance mapping: atomic field rather than whole-document truth

A source may support several field-specific claims, and one field may be supported or disputed by multiple sources. Record a separate provenance mapping for each atomic claim:

| Required dimension | Recorded information and constraint |
| --- | --- |
| Subject | Canonical application ID (or unresolved candidate), operator, specific offering, release/channel, platform, locale/region, account entitlement |
| Field/value | Exact field path, typed value, units/currency/meter where applicable; distinguish known, unknown, not_disclosed, not_applicable, disputed and unsupported |
| Validity scope | Applicability/effective period, version, environment, plan and documented exceptions; no global conclusion from a narrow tier |
| Source locator | Stable public HTTP(S) URL without signed query/credentials, publisher/authority, document identity/version and section locator |
| Source event | Actual checked date, access outcome (readable/gated/failed/withdrawn), source as-of/effective date, revision captured in a permitted original summary |
| Evidence | primary_documentation, vendor_claim, independent_measurement or estimate, plus precise limitation and verification status/receipt where applicable |
| Rights | **Each** source ID × field path × intended use (display, cache, export, API, commercial), decision, scope and reviewer receipt; no inheritance from a permissive neighboring field |
| Review/history | Researcher and material affiliation, non-author reviewer and exact revision, previous/superseding claim IDs, reason for any change |

Keep original summaries, exact URLs and permitted brief quotations only when necessary and allowed. Third-party source material cannot be copied merely because the repository itself is public/MIT. Gated documents and private artifacts remain outside public Git. A source check is not independent verification; a second source must qualify for the **exact** claim, and any human approval is a separate state.

## 2. Normalize before deciding whether there is a contradiction

1. **Identity.** Check product vs suite vs module/feature, operator/rebrand, plan/edition, release and platform. Two similarly named products are not assumed identical; use the independently reviewed identity rules if they exist.
2. **Time.** Separate effective term dates, access dates, observed test dates, report periods and historical replacements. A past price and current price do not contradict if their validity windows are different.
3. **Units.** Normalize without discarding raw source value: currency and conversion-rate date (if any), unit, billing period, tax treatment, included quota, per-seat/per-request meters, commitments, region and overages. Do not invent missing conversions or compare incomparable meters.
4. **Conditions.** Compare only matching entitlement, environment, geography, language, account type and feature availability. An enterprise-only term and a consumer statement can both be true.
5. **Claim type.** Separate official published terms under their stated applicability, supplier marketing statements, actual independent reproduction, estimates, and source absence. Missing mention is **Unknown**, not an explicit negative.
6. **Source access and rights.** Mark unreadable, gated or withdrawn sources as such; do not infer their contents. Citation/reference eligibility and rights to quote/export are independent from whether the researcher inspected a URL.

Use a conflict record only after normalization exposes **the same scoped field with incompatible eligible assertions** or when the scope cannot be resolved and both interpretations materially affect the user decision. A different amount/feature under different plans or dates is a scope distinction, not an automatically disputed fact.

## 3. Conflict disposition decision table

| Decision | Required evidence and behavior |
| --- | --- |
| **Distinct scope** | Both statements remain under their respective product/plan/version/time/region scopes; no artificial "winner" |
| **Controlled precedence** | Where binding and applicable official plan terms or release-specific documents are actually checked and more specific than general marketing, explain precisely why the narrow applicable terms control that field; keep the broader source and its conflicting wording as historical/limited context. Never claim universal source hierarchy |
| **Superseded** | A later source explicitly changes or corrects the same subject/field and effective conditions; retain earlier value, source/checked date, effective window, replacement reason and reviewer receipt |
| **Disputed** | Sources of comparable applicability disagree and there is insufficient independently accepted reason to choose, or authoritative conditions are unclear; preserve both positions, set normalized field to disputed with null value as contract requires, and queue precise recheck |
| **Unknown/not disclosed** | No inspected eligible evidence resolves the field; use null/appropriate status and a next action, not a guessed value, false, zero or Unsupported |
| **Unsupported** | Only with explicit, scoped negative evidence and any needed completeness assertion/review; marketing silence or a failed page is insufficient |
| **Withdrawn/recheck required** | A source or rights grant is withdrawn/changed, an issue is plausibly raised, or documented conditions change; preserve history, pause affected projection and send to the accepted correction workflow |

A reviewer examines the exact source revisions, subjects, normalization and why a decision was selected. Equal-rank unresolved conflicts stay disputed even if a second reviewer prefers one. A conflict is not resolved by deletion, ranking, removing the less convenient source or promoting a supplier statement to verified.

## 4. Mapping to the current contract

The existing [application contract](../../docs/APPLICATION_CONTRACT.md) already provides claim IDs, source IDs, claim scope, evidence status, review and source-use decisions. Preserve these structures. An unresolved disputed value is **null**; do not silently store a favored value with a caveat that a consumer might omit. Retain superseded evidence in notes/history, and reflect eligible current claims only in a separately rights-cleared publication manifest. This proposed prose does not alter the frozen research contracts or authorize a new field in schema v0.1.0.

Source/field rights decisions use the same exact source IDs for each intended use. A field backed by two sources must have permission for its proposed use for **each** admitted source. An independent measurement does not grant republication rights to the source's figures or images. The review receipt on a proposal is not a substitute for the consuming website/pipeline owner's acceptance at an immutable version.

## 5. Independent review, correction and private safety

Use [conflict-record template](../../templates/conflict-record.md). The reviewer verifies primary source access and the recorded dates, compares the normalized scopes and unit conversions, checks source-use rights and material affiliations, and records approval or a clearly reasoned dispute at the reviewed commit. Do not backdate reviews or claim a human decision from a validator result.

Corrections preserve original evidence and previous review decisions. A plausible correction changes the state to **recheck_required**, and publication of that claim pauses until the review process reaches a decision. Do not publish secrets, exploit detail, customer contracts, raw private reports or PII in a conflict record; use [SECURITY.md](../../SECURITY.md) for private vulnerability reporting. No live host testing or vendor contact is enabled by this policy.

## 6. Consumer handoff and acceptance status

The directory may eventually display dated and attributed competing positions and explicit unknowns, but its UI and publication projections belong to website and catalog-pipeline owners under [HANDOFFS](../../docs/HANDOFFS.md). A receiving owner must accept the exact artifact/version, fields, source-use conditions, display wording and rollback behavior. The template below collects proposed receipts and keeps unavailable ones pending.

**State: proposed guidance only.** No product assertions, original document inspections, source-use approvals, reviewer acceptance or consumer release occurred in this document. Closing #73/#106/#107 requires exact-revision independent review and any required receiving handoffs.
