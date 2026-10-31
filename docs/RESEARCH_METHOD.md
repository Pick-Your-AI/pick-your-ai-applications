# Research method

Version 1.0 (proposed) · Refs #67 (task #94) · Contract: [APPLICATION_CONTRACT.md](APPLICATION_CONTRACT.md) · Shared grades: research [#41](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/41)

How application facts are found, checked and graded. Admission and publication are in [ADMISSION_POLICY.md](ADMISSION_POLICY.md).

## Every claim is scoped

A claim names its exact subject (application, offering, feature or release) and the conditions it holds under: plan, platform, region, locale, version or channel, and date. A fact true for one plan or region is not assumed for another.

## Four separate questions per claim

| Question | Field | Values | Rule |
| --- | --- | --- | --- |
| Was the source actually read? | `source_status` | `unchecked`, `checked` | `checked` means a researcher inspected eligible primary evidence on the stated date |
| What kind of evidence is it? | `evidence_grade` | `primary_documentation`, `vendor_claim`, `independent_measurement`, `estimate` | Same vocabulary as research #41; graded per claim, not per source |
| Has anyone independent confirmed it? | `verification` | `unverified`, `verified` | Requires an independent verifier plus a pinned reproducible protocol and receipt, or an independent second source |
| What does the evidence say? | `value_status` | `known`, `unknown`, `not_disclosed`, `not_applicable`, `disputed`, `unsupported` | `unsupported` needs checked, explicit negative evidence |

These never collapse into each other. Reading documentation makes a claim `checked`, never `verified`.

## Feature-matrix states

For capability comparisons: **Exercised** (we ran the workflow and recorded how), **Documented** (the vendor's own material says so), **Unsupported** (explicit negative evidence) and **Unknown** (everything else). Absence from a page is Unknown, not Unsupported. A failed attempt to check is Unknown, not a negative finding.

## Unknown never becomes false or zero

Unknown, undisclosed, disputed and inapplicable values are JSON `null` with their `value_status`. No default turns them into `false`, `0`, `"no"` or an empty list. A price that is not published is `amount: null` with its status, never `"0"`. This rule applies in research, in projections and in every consumer handoff.

## Freshness

There is no automatic expiry: old evidence is not false, and it is not refreshed by being old. Current-state facts (prices, availability, terms, regions) show their checked date as `as_of`. A recheck is triggered by real change signals, such as a source correction, a new version, changed terms, withdrawn rights or a reported error. Risk-based recheck schedules may be set per category in F04.

## Discovery

Use a reproducible, bounded method: queries, sources, date, language and region, recorded so another researcher can repeat it. Directories and search results are leads. Every candidate is checked against the product's own current material before any claim is made.
