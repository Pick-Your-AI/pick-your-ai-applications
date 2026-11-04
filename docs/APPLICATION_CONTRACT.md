# Application research contract — proposal 0.1.0

This contract is the initial, independently versioned application research intake design. It supports notes, source-checked claims and separately admitted publication fields. It has **not** been accepted as a production catalog or website interface. Shared-schema and consuming-owner reviews remain separate backlog deliverables. The existing research repository's frozen `contracts/v1/` is unchanged.

## Identity and scope

An application product is an end-user or enterprise software product that exposes a recognizable workflow. A model, model weight, inference engine, hosting instance, library, hardware component or integration endpoint does not become an application simply by receiving a product name.

| Entity | ID namespace | Meaning |
| --- | --- | --- |
| Application product | `app:` | A durable product identity across versions and plans. |
| Product family | `family:` | Related products marketed together; not a duplicate product record. |
| Application release | `release:` | A specific version of an application, pinned explicitly. |
| Application offering | `offering:` | A separately purchasable or available plan, distribution or regional offering. |
| Application feature | `feature:` | A feature within a product; not automatically an independent application. |
| Integration | `integration:` | A linked adapter or interoperability entity owned by the relevant research stream. |
| Model | `model:` | An informational relationship to underlying model research; not a compatibility assertion. |
| Vendor | `vendor:` | The publisher or responsible business identity. |

Aliases remain attached to canonical product identities. Rebrands, forks, acquisitions, replacements and discontinued successors are evidence-linked relationships rather than reasons to count the same product multiple times. Integration and model relationships do not imply that every version, region or product plan supports them.

`identity`, proposed category IDs and research notes are intake locators. Their existence in JSON does not certify the product name, availability or category as reviewed. **Only factual claims admitted by the publication manifest may be rendered as product facts.** Product identity facts also need corresponding reviewed claims before a consumer can display them as approved directory content.

## Claim semantics

Every claim identifies an exact subject, a field path, a value status, applicable offering/region/locale/platform/conditions, source IDs, dates, grade, review and limitations.

| Dimension | Values and meaning |
| --- | --- |
| Value status | `known`, `unknown`, `not_disclosed`, `not_applicable`, `disputed`, `unsupported`. Unknown, undisclosed, disputed and inapplicable values remain JSON `null`; they never become zero or false. |
| Source status | `unchecked` or `checked`. Checked means a researcher inspected eligible primary evidence on the stated date. |
| Verification status | `unverified` or `verified`. Reading documentation does not produce independent verification. |
| Evidence grade | `primary_documentation`, `vendor_claim`, `independent_measurement`, `estimate`, matching the shared research method. |
| Evidence state | `active`, `recheck_required`, `withdrawn`, `superseded`. Retain corrections and superseded observations in notes/history rather than overwriting the audit trail. |
| Review | `pending`, `approved`, `rejected`. Approval requires a named reviewer other than the researcher, date and decision receipt. The validator checks the recorded metadata, not whether a human actually approved it. |

`unsupported` needs checked, explicit negative evidence. Absence from a product page is not a negative result. If an exhaustive source supports an absence-based conclusion, record that exact completeness assertion and its review in the limitation/evidence trail before using an explicit negative claim.

Independent verification requires an independent verifier plus either a pinned reproducible-test protocol and receipt or an explicitly cited independent second source. Vendor measurements remain distinguishable from independent reproduction. Estimates require their methods, assumptions and limitations. No field creates a ranking, endorsement, security certification or regulated-use approval.

## Dates and freshness

Version-pinned facts require a version. Current-state facts, including prices, availability, terms and regions, carry their checked date as the visible `as_of` value. The shared policy adopts **no automatic TTL**; merely old evidence does not become false or verified. Source corrections, changed versions, withdrawn evidence and explicitly required rechecks trigger review. Known source-rights expiration is enforced independently of this freshness rule.

The validator rejects future check/access/review dates and impossible dates. It does not fetch pages or establish that current-state evidence is still current. Researchers and consumers must preserve the dated scope and apply actual change evidence.

## Pricing and business terms

Pricing observations use the separate [pricing schema](../schemas/pricing.schema.json) within a pricing claim's value. They reference an exact application offering. This application contract is separate from the frozen component Pricebook v1 and does not extend its units or billing semantics.

Separate `data/pricing/*.json` records use [the pricing-record envelope](../schemas/pricing-record.schema.json): an immutable observation ID, canonical application ID, offering ID, one pricing claim, its source evidence, rights decisions and publication manifest. The canonical application must exist and declare that exact offering. Standalone price evidence uses the same claim/review/rights validation as embedded claims; a price file cannot bypass those gates. Do not duplicate the same observation in both locations. A published standalone price also requires an admitted parent application.

A known numeric amount requires a decimal string, currency, region, billing period, meter and commitment. Decimal strings avoid binary floating-point ambiguity. A sourced free price may be `"0"`; an undisclosed, custom or contact-sales price has `amount: null` with its appropriate `amount_status`. Missing currency, quotas, tax treatment, included allowances or overage details remain explicitly unknown. Promotional conditions, minimum seats, term commitments and tax status are not silently omitted from comparisons. A price observation is dated and does not establish a full total-cost estimate.

## Source use and publication

Each source has a stable public HTTP(S) locator, authority, publisher, access date and state. Source locators must not contain credentials or query parameters; record a stable canonical locator and sanitized description instead of a signed URL. An accessible source is not a reuse license.

Rights decisions identify one source, exact field paths and intended uses: `display`, `cache`, `export`, `api`, `commercial`. Decisions can be allowed, denied, unknown or unclear. An allowed decision requires a reviewer and linked receipt with conditions. Display permission does not grant API/export/commercial permission. A field's approval does not clear an entire source, table or file. The validator rejects source/field/use gaps and expired grants for fields marked eligible or published.

Publication states are `notes`, `proposed`, `eligible`, `published`. Neither merging a record nor passing tests advances a state automatically. Eligible/published manifests must list every admitted claim, intended use and rights decision. Each admitted fact must be checked, independently reviewed, active and have use-specific rights for every cited source. The displayed grade/status must exactly match the claim. Multiple admitted claims for the same subject/field/version/scope require explicit reconciliation; unresolved conflicts stay in notes.

Published state additionally requires a release receipt and a consuming-owner acceptance receipt. These are recorded references, not an automated proof of content immutability or authorization. Pipeline release hashing/signing, consumer acceptance, display of unknown fields, cross-repository entity resolution and source-rights approval remain implementation/research handoffs. The application validator does not implement those services.

## Files and commands

Real intake is `data/applications/*.json` and `data/pricing/*.json`. Synthetic examples exist **only** in `tests/fixtures/` and use reserved example hosts plus `synthetic: true`. Ordinary intake rejects those records.

When `taxonomy/taxonomy.json` is present, category IDs must resolve to that taxonomy. Claims named `facets.<facet_name>` use its enumerated vocabulary where one is specified. Language, geography, accessibility and enterprise-control facets remain structured scoped claims rather than invented boolean defaults. Taxonomy adoption is a review decision; structural reference validation does not approve a classification.

```sh
python scripts/validate_applications.py
python -m unittest discover -s tests -p 'test_application_contract.py' -v
```

The Python validator has no external dependencies. It evaluates only the JSON Schema vocabulary used by these schemas, rejects unsupported schema keywords and applies semantic cross-reference, identity, date, evidence, pricing and publication checks. It is not a general-purpose JSON Schema engine. Add implementation and regression coverage before introducing a new schema keyword.

Structural validation does **not** verify sources, capabilities, prices, legal interpretations, actual review identity, claimed independent reproduction, remote artifacts, publication licenses or completeness. The empty initial intake reports zero real records and explicitly does not claim research coverage.

## Canonical policy references

- [Organization contribution and review policy](https://github.com/Pick-Your-AI/.github/blob/main/CONTRIBUTING.md)
- [Research contributor instructions](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/AGENTS.md)
- [Shared execution and evidence rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/prompts/SHARED.md)
- [Research method](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/RESEARCH_METHOD.md)
- [Research workflow](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/RESEARCH_WORKFLOW.md)
- [Parent coverage audit, applications gap G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509)
