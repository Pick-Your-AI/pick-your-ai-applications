# Ownership and receiving handoffs

Version 1.0 (proposed) · Refs #65 (tasks #90, #91) · Machine-readable ledger: [planning/handoffs.json](../planning/handoffs.json)

This record says where each application fact and each implementation responsibility lives, and what a cross-repository handoff must carry. It refines the scaffold's [HANDOFFS.md](HANDOFFS.md). It grants no approval, creates no repository and implies no consumer implementation. Every receiving decision listed here is **pending** until a real reviewer records it at an exact revision.

## Responsibility matrix (task #90)

| Concern | Canonical owner (artifact) | This repository's role | Interface |
| --- | --- | --- | --- |
| Application identity, offerings, features, application claims | **This repository** (`data/applications/`, decision records) | Owns | — |
| Application prices and commercial terms | **This repository** (`data/pricing/`) | Owns; reuses shared price semantics | research [#39](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/39) when shared units change |
| Models, model releases, providers, inference routes | research T1 ([#4](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/4)) | Links with `model:`, only when the vendor discloses the relationship | Disclosed relationship claim; never an inferred backend |
| Tools, APIs, MCP components, frameworks, connectors | research T4 ([#24](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/24), [#26](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/26)) | Links with `integration:` | Product-versus-interface rule (`docs/SCOPE.md`, B3/B4) |
| Accelerators, engines, hosting, runtime fit | research T2/T6 and the COMPUTE families | Records an application's stated runtime requirements as scoped claims | No second fit rule; fit decisions stay in research |
| Shared component contract | research [#40](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/40) | Application contract 0.1.0 is separate; frozen `contracts/v1` unchanged | A proposal and impact note for any shared use |
| Evidence grades and freshness | research [#41](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/41) | Reuses the grades; no inherited universal freshness period | Same vocabulary, cited |
| Source-use and redistribution rights | research [#60](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/60) decisions | Records source, field and use decisions per claim | No blanket grant from any prior decision |
| Application task evaluation | research [#36](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/36) (T6) | Proposes app-task protocols (F05) | Does not duplicate model or runtime calibration |
| Datasets and benchmarks | [pick-your-ai-datasets #1](https://github.com/Pick-Your-AI/pick-your-ai-datasets/issues/1) | Links datasets an application produces or uses | Separate dataset identity and rights |
| Papers and literature | [pick-your-ai-papers #1](https://github.com/Pick-Your-AI/pick-your-ai-papers/issues/1) | Links papers as sources | A paper is never an application record |
| Ingestion, validation runtime, release | [pick-your-ai-catalog-pipeline #1](https://github.com/Pick-Your-AI/pick-your-ai-catalog-pipeline/issues/1) | Produces versioned, eligible projections and change events | Pipeline code lives in its own repository |
| Public directory UI | `pick-your-ai-website` (#15, #24) | Supplies directory requirements (F06) | Frontend implementation stays in the website repository |
| Mobile clients | [Apple #1](https://github.com/Pick-Your-AI/pick-your-ai-apple/issues/1), [Android #1](https://github.com/Pick-Your-AI/pick-your-ai-android/issues/1) | Supplies the same eligible interface when a receiving need is accepted | No automatic issue cloning |
| Broad scope and coverage | research [#509](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509) (G12) | Child program | Scope changes reconcile with #509 and #47 |

**T1/T4 crosswalk (task #90, S01).** T1 owns *what model, from which provider, served how*. T4 owns *which tool, API or integration component*. This repository owns *which product a person uses, in which offering*. An application can **use** a model, **expose** an integration or **contain** a feature. Those relationships never merge the identities, and a missing disclosure stays unknown.

**Runtime stays with its owners (task #90, S02).** The catalog-pipeline and website repositories own all ingestion, publication and UI code. This repository supplies contracts, eligible data and receiving tests only.

## Receiving receipt (task #91)

A handoff is **delivered** only when a receipt records all of:

| Field | Meaning |
| --- | --- |
| `producer_artifact` | Exact path(s) and immutable commit in this repository |
| `contract_versions` | Application contract and taxonomy versions |
| `fields_and_uses` | Exact field paths and intended uses (display, cache, export, api, commercial) |
| `evidence_conditions` | Source dates, grades and limitations that travel with the data |
| `consumer` | Receiving repository, issue and the revision it reviewed |
| `reviewer` | GitHub identity of the actual receiving reviewer |
| `decision` | `accepted`, `accepted_with_conditions`, `rejected` or `pending`, with the decision URL and date |
| `conditions` | Retained conditions and migration or compatibility assumptions |
| `correction_and_rollback` | How corrections, withdrawals and rollbacks propagate |
| `follow_ups` | Unresolved items with owners |

Until every field exists, the entry stays `pending`. A consumer repository or issue whose identity is not confirmed is recorded as `unresolved`, never assumed (task #91, S02). The ledger in `planning/handoffs.json` starts with every entry pending, and no reviewer is named for any.
