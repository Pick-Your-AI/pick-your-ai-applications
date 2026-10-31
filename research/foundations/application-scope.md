# APP-F01.01 decision record: application inclusion and exclusion

Issue: #64 (tasks #88 review boundary cases, #89 accept scope and exclusions) · Status: proposed for review · Recorded: 2026-10-31
Normative summary: [docs/SCOPE.md](../../docs/SCOPE.md)

## User decision

Which purchasable, installable or directly usable AI software and service entities belong in this directory, and which belong elsewhere?

## Inputs (information only, no native blockers)

- Taxonomy 1.0 global exclusions and boundary cases (`taxonomy/taxonomy.json`), Application contract 0.1.0 identity namespaces (`docs/APPLICATION_CONTRACT.md`).
- [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509): the applications expansion; prior research boundaries are preserved.
- [research #47 synthesis](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/market/synthesis.md): the adopted NARROW program disposition.
- [research #513](https://github.com/Pick-Your-AI/pick-your-ai-research/pull/513), proposed Stage 0 ledger. Its G12 row asks for product-versus-interface identity and cross-links before duplicating records. It is still a proposal; nothing here depends on its acceptance.

## Decision 1: the inclusion test

An entity is an **application** when all four hold, each on evidence:

1. **Usable workflow:** a person or organization can use it to accomplish a task, not only build something else.
2. **Material AI role:** AI performs or assists a core step of that workflow. Marketing use of "AI" is a lead, not evidence.
3. **Identifiable offering:** it has a name, entry point and way to obtain or access it (download, sign-up, plan, contract or install).
4. **Software delivery:** the customer reaches the workflow through software, including vendor-operated services with humans in the loop.

When any test is unknown, the entity stays a **candidate note** with the unknown recorded. It is not excluded and not admitted.

## Decision 2: boundary table (task #88, subtasks S01 and S02)

The examples are **illustrative archetypes**, not claims about any real product. A real case is decided with its own dated evidence.

| # | Archetype | Decision | Reason |
| --- | --- | --- | --- |
| B1 | A chat app whose responses come from a hosted model | Application (`app:`), with a `model:` link only if the vendor discloses the model | The workflow is the product; the model is a component owned by T1 |
| B2 | The same model's public API endpoint | **Excluded**; T1/T2 record | An inference route is not an end-user workflow |
| B3 | An official plugin that brings the chat app into an editor | `feature:` or `integration:` of B1, unless it has its own offering | Interface, not a second product (product-versus-interface rule, #513 G12) |
| B4 | A connector library or SDK for developers | **Excluded**; T4 | No usable end-user workflow |
| B5 | An agent builder where users assemble and run their own agents | Application | A usable builder is a product (taxonomy boundary: agent builders) |
| B6 | A marketplace listing many third-party bots | Discovery source; each listed bot needs its own identity decision | A marketplace is not one application |
| B7 | An AI summary button inside a word processor | `feature:` record on the word-processor application | No independent entry point or offering |
| B8 | The same capability sold as a separately priced add-on with its own name and console | Application module (`app:` with a family link) | It gained an independent offering and entry point |
| B9 | A desktop app that runs open models locally | Application; runtime requirements are scoped claims, fit stays with research COMPUTE-01/02 | Local delivery is in scope; hardware fit is not duplicated here |
| B10 | A transcription service where humans correct AI output, bought per minute through a portal | Software-delivered service (application) | Customer uses a software workflow and a defined offering (taxonomy boundary: professional services) |
| B11 | A consultancy that builds custom AI systems on request | **Excluded**; service-provider note | No identifiable software-delivered offering |
| B12 | A product announced with a waitlist and demo video only | Candidate note | No usable offering is evidenced yet |
| B13 | A discontinued product | Kept as a retired identity with history | Retirement is history, not deletion (see F01.04) |
| B14 | The same app in different languages or on different platforms | One application; offerings and facets | No duplicate per language, platform or region |
| B15 | A dataset-labeling workbench | Application; the datasets it produces are separate entities | Taxonomy boundary: data labeling |

**When an AI feature deserves its own application record (S02):** only when the feature has an independent entry point, name **and** offering (purchasable, installable or separately accessible). A feature that is merely toggled on inside a host product stays a `feature:` record, even if it is marketed prominently.

## Decision 3: audiences and forms (task #89, S01)

| Dimension | Eligible values |
| --- | --- |
| Audience | consumers; professionals and prosumers; teams and SMBs; enterprises; public sector; education |
| Product form | web app; desktop app; mobile app; CLI; browser extension; suite module; self-hosted or local application; hosted service; software-delivered service |
| Access | free; freemium; paid plan; contract or enterprise; open source; source-available |

These are facet vocabularies for classification, not counts or coverage claims.

## Decision 4: compatibility with #47 NARROW

#47 adopted NARROW: test whether a reconstructable decision record improves one coherent comparison. Broad T0–T6 product expansion, exclusivity, commercial launch and demand verdicts remain unsupported.

This directory is compatible because:

1. It is a reference research corpus with its own evidence, rights and publication gates.
2. It makes no product-validation, demand, exclusivity or launch claim.
3. It does not expand the builder's component kinds or change `contracts/v1`.
4. Any use of application data by the builder is a separate, owner-reviewed consumer handoff.

## Unresolved boundary cases (task #89, S02)

Recorded for future triage. No capability is assumed for any of them.

| ID | Question | Proposed owner |
| --- | --- | --- |
| U1 | Operating-system-level assistants bundled with a platform: an application, or a feature of the OS product? | Applications D01 with the research T4 owner |
| U2 | AI features in hardware devices (cameras, earbuds) whose workflow runs in a companion app: is the companion app the application? | Applications D08 |
| U3 | Free open-source projects without a maintained release or an operator: when do they count as a usable offering? | Applications F04 (coverage) |
| U4 | Enterprise platforms where the customer configures every workflow: one application or several modules? | Applications D05 |

## Acceptance mapping

| Criterion | Where it is met |
| --- | --- |
| Boundary cases have reproducible examples with reasons | Decision 2 (B1–B15) |
| Application and model/provider identities remain distinct | Decision 1, B1–B4, out-of-scope table in `docs/SCOPE.md` |
| Broad mission compatible with #47 NARROW | Decision 4 |
| Factual conclusions scoped or unknown | No product claims are made; archetypes are labelled; U1–U4 stay open |
| Receiving decisions linked or pending | Pending: independent application research reviewer; research #509 owner (G12 boundary) |

## Review requested

An independent application-research reviewer on this exact revision, and the #509 owner for the G12 boundary statement. Structural validation (`validate_applications.py`, `validate_planning.py`, tests) is reported separately from factual acceptance.
