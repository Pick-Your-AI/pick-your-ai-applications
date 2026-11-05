# APP-F01.01 decision record: application inclusion and exclusion

Issue: #64 (tasks #88 review boundary cases, #89 accept scope and exclusions) · Version 1.1 (proposed), the same version as docs/SCOPE.md · Status: proposed for review · Recorded: 2026-10-31, revised 2026-11-03
Normative summary: [docs/SCOPE.md](../../docs/SCOPE.md)

## User decision

Which purchasable, installable or directly usable AI software and service entities belong in this directory, and which belong elsewhere?

## Inputs (information only, no native blockers)

Local rules, at this commit:
- Taxonomy 0.1.0 (`taxonomy/taxonomy.json`): global exclusions, boundary cases and facet values.
- Application contract 0.1.0 (`docs/APPLICATION_CONTRACT.md`): identity namespaces.
- `docs/TAXONOMY_AND_COVERAGE.md`: identity rules, including the module rule and the lifecycle-record rule.

External sources, each pinned with what was read. Anything beyond the part read is unknown here.

| Source | Version | Read | Part read |
| --- | --- | --- | --- |
| [research #509](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509), the coverage audit | Issue body, last updated 2026-10-31T03:27:21Z | 2026-11-03 | Item 5 and row G12 only |
| [research #47 synthesis](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/market/synthesis.md) | Blob `0f5cfff57671097695ceef9fd62906587b90e6b5`, the same blob `evidence/taxonomy-inspection-references.json` pins | 2026-11-03 | Line 5 (adopted disposition) and lines 64–69 (go, narrow or stop) only |
| [research #513](https://github.com/Pick-Your-AI/pick-your-ai-research/pull/513), proposed Stage 0 ledger (draft) | Head `0c20de82e2c5fc6fb0e0ccf20b91a0dfee36acad` | 2026-11-03 | Row G12 of `coverage-ledger-proposal.md` only |
| [research T2 compute-capacity rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T2-infrastructure/rules/compute-capacity.md) | Blob `e9813b80dfd638fdb8f3b8a1e96a57420a069d15` | 2026-11-03 | The COMPUTE-01 and COMPUTE-02 headings and the shared-applicability section only |

What those parts say, as far as this record relies on them:
- **#509, G12:** a standalone application directory is justified because applications are a different entity kind from model and runtime components. The T4 #26 integrations and the market competitor catalog stay linked sources: "do not duplicate an integration as an application without an identity rule".
- **#47:** NARROW is adopted. It tests whether a reconstructable decision record improves one coherent comparison over the best applicable existing substitute and a README/manifest baseline. Broad T0–T6 product expansion, exclusivity, commercial launch, and a positive demand or runtime verdict remain unsupported. The synthesis calls this a research-scope decision, not a completed comparison.
- **#513, G12:** "Net new, deferred/outside Stage 0". It takes no Stage 0 action and asks for affected-owner agreement before any crosswalk. Nothing here depends on #513.
- **COMPUTE-01/02:** per-device memory feasibility, and the intersection of model, engine and accelerator backend, applied to the serving component. This record does not restate them.

## Decision 1: the inclusion test

An entity is an **application** when all four hold, each on evidence:

1. **Usable workflow:** a person or organization can use it to accomplish a task. A component that other software builds in fails this test: a library, SDK, framework, protocol or connector (taxonomy global exclusion 2). A product whose job is producing software passes it, for example a coding assistant (APP-C09) or an app or website builder (APP-C10).
2. **Material AI role:** AI performs or assists a core step of that workflow. Marketing use of "AI" is a lead, not evidence.
3. **Identifiable offering:** it has a name, entry point and way to obtain or access it (download, sign-up, plan, contract or install).
4. **Software delivery:** the customer reaches the workflow through software, including vendor-operated services with humans in the loop.

When any test is unknown, the entity stays a **candidate note** with the unknown recorded. It is not excluded and not admitted.

## Decision 2: boundary table (task #88, subtasks S01 and S02)

The examples are **illustrative archetypes**, not claims about any real product. A real case is decided with its own dated evidence.

| # | Archetype | Decision | Reason |
| --- | --- | --- | --- |
| B1 | A chat app whose responses come from a hosted model | Application (`app:`), with a `model:` link only if the vendor discloses the model | The workflow is the product; the model is a component owned by T1 |
| B2 | The same model's public API endpoint | **Excluded**; T1 record (#4, providers #5) | An inference route is not an end-user workflow |
| B3a | An official plugin that brings the same chat workflow into an editor | Offering of B1 with `access_surface: ide_extension` | Same workflow on another surface (taxonomy variants boundary; B14) |
| B3b | A plugin that is separately discoverable and materially distinct in access, release, contract or workflow from its host | Module: its own `app:` (`product_form: plugin_extension`) linked to its host | The module rule, `docs/TAXONOMY_AND_COVERAGE.md` |
| B3c | An adapter that connects other software to a service, with no workflow of its own | **Excluded**; `integration:`, owned by T4 (#24) | An adapter is an integration, never duplicated as an application (#509 G12) |
| B4 | A connector library or SDK for developers | **Excluded**; T4 | Built into other software; no usable workflow of its own |
| B5 | An agent builder where users assemble and run their own agents | Application | A usable builder is a product (taxonomy boundary: agent builders) |
| B6 | A marketplace listing many third-party bots | Discovery source; each listed bot needs its own identity decision | A marketplace is not one application |
| B7 | An AI summary button inside a word processor | `feature:` record on the word-processor application | No independent entry point or offering |
| B8 | The same capability sold as a separately priced add-on with its own name and console | Module: its own `app:` (`product_form: suite_module`) linked to its host | It gained an independent offering and entry point |
| B9 | A desktop app that runs open models locally | Application. Its runtime requirements are scoped claims; hardware fit stays with research T2 (COMPUTE-01/02) | Local delivery is in scope; hardware fit is not duplicated here |
| B10 | A transcription service where humans correct AI output, bought per minute through a portal | Software-delivered service (application). Its records keep which steps are human service and which are software automation | Customer uses a software workflow and a defined offering (taxonomy boundary: professional services) |
| B11 | A consultancy that builds custom AI systems on request | **Excluded**; service-provider note | No identifiable software-delivered offering |
| B12a | A product shown only in an announcement or demo, with no entry point | Candidate note | It was never usable, and no identity is evidenced yet |
| B12b | A named product with first-party documentation and a waitlist sign-up | Lifecycle record (`lifecycle: waitlist`, `availability: waitlist`); not counted as currently available | It has an identity and an entry point, but no usable offering yet |
| B13 | A product that was usable and is now discontinued | Retired identity with history (`lifecycle: discontinued`, `availability: retired`) | Retirement is history, not deletion (see F01.04) |
| B14 | The same app in different languages or on different platforms | One application; offerings and facets | No duplicate per language, platform or region |
| B15 | A dataset-labeling workbench | Application; the datasets it produces are separate entities | Taxonomy boundary: data labeling |
| B16 | An office suite sold as one product, with several AI-assisted modules | One application (`product_form: suite`). A module that meets the module rule is its own `app:` linked to the suite | Suite rule, `docs/TAXONOMY_AND_COVERAGE.md`. A `family:` groups separate products marketed together, not a suite's modules |
| B17 | A hardware device or component with AI features, such as an accelerator, a camera or earbuds | **Excluded** as hardware; T2 (#8). The device's companion app is U2 | Hardware is a different entity kind (`docs/APPLICATION_CONTRACT.md`, identity and scope) |

**When an AI feature deserves its own application record (S02):** only when the feature has an independent entry point, name **and** offering (purchasable, installable or separately accessible). A feature that is merely toggled on inside a host product stays a `feature:` record, even if it is marketed prominently. S02 is the test for AI features and is narrower than the general module rule in `docs/TAXONOMY_AND_COVERAGE.md` ("independently discoverable and materially distinct in access, release, contract or workflow"): a feature that meets S02 meets that rule, but a feature that meets only that rule stays a `feature:` record. This record does not change the general rule for other modules and extensions, which B3b and B16 apply.

**Lifecycle record or candidate note:** the base rule stands: announcements, inaccessible products, prototypes, waitlists and retired offerings can have lifecycle records, and none counts as a currently available application (`docs/TAXONOMY_AND_COVERAGE.md`; taxonomy global exclusion 5). This record only says which one a product gets:
- a **lifecycle record** when the product has an evidenced identity and an entry point, whether it was usable or is not usable yet (B12b, B13);
- a **candidate note** when it was never usable and has no evidenced identity (B12a). The taxonomy's "abandoned products" are this case: announced or previewed, never usable.

An unmaintained open-source project is left to U3.

## Decision 3: audiences and forms (task #89, S01)

| Dimension | Eligible values |
| --- | --- |
| Audience | All taxonomy `audience` values: individual, creator, developer, small_business, enterprise, educator, student, researcher, public_sector, professional and unknown |
| Product form | All taxonomy `product_form` values, including suite, suite_module, plugin_extension, software_delivered_service and unknown |
| Delivery | All taxonomy `deployment` and `distribution_rights` values |

This decision admits every existing value and adds none. Structured `facets.*` claims use the enumerated values in `taxonomy/taxonomy.json`, which `scripts/validate_applications.py` enforces; any vocabulary change belongs to APP-F02.02 as a versioned taxonomy migration. These are eligibility rules, not counts or coverage claims.

## Decision 4: compatibility with #47 NARROW

#47 adopted NARROW (pinned above). It tests whether a reconstructable decision record improves one coherent comparison over the best applicable existing substitute and a README/manifest baseline. Broad T0–T6 product expansion, exclusivity, commercial launch, and a positive demand or runtime verdict remain unsupported.

This directory is compatible because:

1. It is a reference research corpus with its own evidence, rights and publication gates.
2. It makes no product-validation, demand, exclusivity, launch or runtime claim.
3. It does not expand the builder's component kinds or change `contracts/v1`.
4. Any use of application data by the builder is a separate, owner-reviewed consumer handoff.

## Unresolved boundary cases (task #89, S02)

Recorded for future triage. No capability is assumed for any of them. Every proposed owner's acceptance is **pending**.

| ID | Question | Proposed decision owner | Consulted | Acceptance |
| --- | --- | --- | --- | --- |
| U1 | Operating-system-level assistants bundled with a platform: an application, or a feature of the OS product? | APP-F02.01 (#68), an identity question | D01 (#2); research T4 (#24) | pending |
| U2 | AI features in hardware devices (cameras, earbuds) whose workflow runs in a companion app: is the companion app the application? | D08 (#9) | research T2 (#8) | pending |
| U3 | Free open-source projects without a maintained release or an operator: when do they count as a usable offering? | F04 (#13), coverage | — | pending |
| U4 | Enterprise platforms where the customer configures every workflow: one application or several modules? | APP-F02.01 (#68), an identity question | D05 (#6) | pending |

## Acceptance mapping

| Criterion | Where it is met |
| --- | --- |
| Distinguish product, service, embedded AI feature, plugin, app suite and professional-service business (#64 scope) | Decision 2: B1 product, B7 and S02 feature, B3a–B3c plugin, B16 suite, B10 and B11 services |
| Exclusions for standalone models, hardware, inference engines, general agencies and purely speculative offerings (#64 scope) | B2, B17, the out-of-scope table in `docs/SCOPE.md`, B11, B12a |
| Boundary cases have reproducible examples with reasons | Decision 2 (B1–B17) |
| Application and model/provider identities remain distinct | Decision 1, B1–B4, out-of-scope table |
| Broad mission compatible with #47 NARROW | Decision 4 |
| Factual conclusions scoped or unknown | Every external source is pinned with its version, access date and part read (Inputs). Archetypes are labelled, and U1–U4 stay open |
| Receiving decisions linked or pending | Pending, each with its reviewer, revision, scope and conditions still to be recorded: the independent application-research reviewer; research #509 (G12 boundary); research #47 (inclusion decisions, `docs/HANDOFFS.md`); research T4 #24 (the integration distinction in B3c) |

## Changes in 1.1

These resolve findings 3–8 of the [31 Oct review](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/141#issuecomment-6547716634):
- Lifecycle records versus candidate notes follow the base rule, with B12 split into B12a and B12b. "Abandoned" is defined, and U3 is left open (finding 3).
- B3 has one outcome per deciding test (B3a–B3c). B16 (suites) and B17 (hardware) are added, and #64's scope items are in the acceptance table (finding 4).
- Inclusion test 1 excludes built-in components, not products that produce software. Every audience value is eligible, developers included (finding 5).
- #47 and T4 are listed as pending receivers. U1–U4 link their issues, with acceptance pending; U1 and U4 go to APP-F02.01 (finding 6).
- External sources are pinned. #47 is restated from the pinned lines, and #513's current G12 row replaces an earlier paraphrase (finding 7).
- Owners link their issues, or are pending APP-F01.02. The qualifiers for libraries, directories and human service are restored, and inference routes go to T1 throughout (finding 8).

## Review requested

An independent application-research reviewer on this exact revision; the #509 owner for the G12 boundary statement; the #47 owner for the inclusion decisions; and the T4 owner for B3c. Structural validation (`validate_applications.py`, `validate_planning.py`, tests) is reported separately from factual acceptance.
