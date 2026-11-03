# Ownership matrix and receiving receipts

Version 1.1 (proposed) · Refs #65 (tasks #90, #91) · Machine-readable ledger: [planning/handoffs.json](../planning/handoffs.json)

This record says where each application fact and each implementation responsibility lives, and what a cross-repository handoff must carry. It grants no approval, creates no repository and implies no consumer implementation. Every receiving decision listed here is **pending** until the consumer's actual reviewer records it at an exact revision.

**Precedence.** Where this record and the scaffold's [HANDOFFS.md](HANDOFFS.md) differ, this record governs ownership, receipts and the ledger. HANDOFFS.md stays the scaffold's summary, and it still holds the website research requirements, which F06.03 refines. The taxonomy's category pointers to HANDOFFS.md change only in a versioned taxonomy update. External references name their repository; a bare `#N` is an issue in this repository.

## Responsibility matrix (task #90)

| Concern | Canonical owner (artifact) | This repository's role | Interface | Ledger |
| --- | --- | --- | --- | --- |
| Application identity, offerings, features, application claims | **This repository** (`data/applications/`, decision records) | Owns. Reuses market research's records with attribution (next row) | Market reuse below; identity rules in `docs/TAXONOMY_AND_COVERAGE.md` | None: this repository decides its own records |
| Competitors and commercial validation | research market program ([research #47](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/47)–#66: the competitor catalog and its identity decisions, the synthesis, the #49 matrix states) | Reuses records with attribution; no bulk import. Keeps #47's NARROW decision and does not repeat its recruitment or willingness-to-pay studies | Attribution and source-use decisions per reused record (APP-F03.01) | H14, H15 |
| Application prices and commercial terms | **This repository** (`data/pricing/`) | Owns; reuses shared price semantics | [research #39](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/39) when shared units change | H07 |
| Models, model releases, providers, inference routes | research T1 ([README](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T1-model-selection/README.md), blob `f368200b`; research #4, closed) | Links with `model:`, only when the vendor discloses the relationship | Disclosed relationship claim; never an inferred backend | H02 |
| Tools, APIs, MCP components, frameworks, connectors | research T4 ([README](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T4-agents-integrations/README.md), blob `72502d70`; research #24 and #26, closed) | Links with `integration:` | The product-versus-interface counting rules in `docs/SCOPE.md` (APP-F01.01, #141) | H03 |
| Accelerators, engines, hosting, runtime fit | research T2 and T6; fit rules COMPUTE-01/02 ([compute-capacity rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T2-infrastructure/rules/compute-capacity.md), blob `e9813b80`); runtime sizing [research #61](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/61) | Records an application's stated runtime requirements as scoped claims (APP-F02.03) | No second fit rule; fit decisions stay in research | H17 |
| Shared component contract | [research #40](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/40) (closed) | Application contract 0.1.0 is separate; frozen `contracts/v1` unchanged | A proposal and impact note for any shared use | H04 |
| Evidence grades and freshness | [research #41](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/41) (closed) | Reuses the grades; no inherited universal freshness period | Same vocabulary, cited | H05 |
| Source-use and redistribution rights | [research #60](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/60) decisions (closed), under research #41's source policy | Records source, field and use decisions per claim | No blanket grant from any prior decision | H06, H20 |
| Application task evaluation | [research #36](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/36) (T6, closed); research #61 and [#62](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/62) for their existing empirical scopes | Proposes app-task protocols (F05) | Does not duplicate model or runtime calibration | H08, H18 |
| Datasets and benchmarks | [pick-your-ai-datasets #1](https://github.com/Pick-Your-AI/pick-your-ai-datasets/issues/1) | Links datasets an application produces or uses, once the contract can express it | Separate dataset identity and rights; not expressible in contract 0.1.0 | H11 |
| Papers and literature | [pick-your-ai-papers #1](https://github.com/Pick-Your-AI/pick-your-ai-papers/issues/1) | Links papers as sources (`sources`) | A paper is never an application record | H12 |
| Ingestion, validation runtime, release | Catalog pipeline: receiving identity to be confirmed. [pick-your-ai-catalog-pipeline #1](https://github.com/Pick-Your-AI/pick-your-ai-catalog-pipeline/issues/1) is the candidate | Produces versioned, eligible projections and change events | Pipeline code lives in its own repository | H09 |
| Public directory UI | pick-your-ai-website ([#15](https://github.com/Pick-Your-AI/pick-your-ai-website/issues/15), [#24](https://github.com/Pick-Your-AI/pick-your-ai-website/issues/24); website Project #3, not read back here) | Supplies directory requirements (F06) | Frontend implementation stays in the website repository | H10, H19 |
| Mobile clients | [pick-your-ai-apple #1](https://github.com/Pick-Your-AI/pick-your-ai-apple/issues/1), [pick-your-ai-android #1](https://github.com/Pick-Your-AI/pick-your-ai-android/issues/1) | Supplies the same eligible interface when a receiving need is accepted | No automatic issue cloning | H13, H16 |
| Broad scope and coverage | [research #509](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509) (G12) and research #47 | Child program | Scope changes reconcile with research #509 and research #47 | H01, H14 |

**T1/T4 crosswalk (task #90, S01).** T1 owns *what model, from which provider, served how*. T4 owns *which tool, API or integration component*. This repository owns *which product a person uses, in which offering*. An application can **use** a model, **expose** an integration or **contain** a feature. Those relationships never merge the identities, and a missing disclosure stays unknown.

**Runtime stays with its owners (task #90, S02).** The catalog-pipeline and website repositories own all ingestion, publication and UI code. This repository supplies contracts, eligible data and receiving tests only.

**Consumer readbacks.** Every consumer was read back on 2026-11-03: its repository, issue number, title and state are in the ledger's `consumer_evidence`. Eight research issues named here are closed: #4, #24, #26, #36, #39, #40, #41 and #60. A closed issue cannot record a receiving decision, so the ledger marks those consumers `unresolved` until the workstream's current receiving venue is confirmed with its owners. That is a readback, not a finding about the workstreams.

## Receiving receipt (task #91)

| Field | Meaning |
| --- | --- |
| `producer_artifact` | `{repository, paths[], commit, status, planned_by}`. `commit` is the 40-character commit the consumer reviews, or null while `status` is `planned` or `unresolved`. An unresolved artifact says why (`unresolved_reason`); an artifact can name the `fields` it means within its paths |
| `contract_versions` | Application contract and taxonomy versions |
| `fields_and_uses` | Exact field paths and intended uses (display, cache, export, api, commercial), each with the producer's rights-decision IDs or the reason a field is withheld |
| `evidence_conditions` | Source dates, grades and limitations that travel with the data |
| `consumer` | `{repository, issue, commit}`: the receiving repository and issue, and the consumer's own commit when the decision rests on one |
| `reviewer` | GitHub identity of the actual receiving reviewer |
| `reviewer_authority` | Why that reviewer can decide for the consumer: the live assignee or owner, or a linked delegation, with the date it was checked |
| `decision` | `{value, url, date}`. `value` is `accepted`, `accepted_with_conditions`, `rejected` or `pending` |
| `conditions` | Retained conditions and migration or compatibility assumptions |
| `correction_and_rollback` | How corrections, withdrawals and rollbacks propagate |
| `follow_ups` | Unresolved items with owners |

**Decision and delivery.**
- `decision.value` stays `pending` until the receiving reviewer records an actual decision.
- A decision counts as recorded once `reviewer`, `reviewer_authority`, `decision.url`, `decision.date` and `producer_artifact.commit` all exist. It is kept as recorded, even while other fields are incomplete.
- A handoff is **delivered** when its decision is `accepted` or `accepted_with_conditions` and every applicable field is recorded. A field that does not apply states why. Open conditions do not block delivery; they travel in `conditions` and `follow_ups`.
- A `rejected` decision is never delivered.

**The same rules as the receipts this repository already validates.** Coverage acceptance receipts (`scripts/validate_planning.py`) and this receipt use the same rules:
- commits are 40 hexadecimal characters;
- `decision.url` is a GitHub pull-request or issue decision, or an immutable blob URL, because a general webpage is not a receipt;
- `decision.date` is a real calendar date, not in the future.

The fields map onto that receipt like this:

| This receipt | Coverage receipt |
| --- | --- |
| `producer_artifact.commit` | `artifact_commit` |
| `consumer.commit` | `consumer_commit` |
| `decision.url` | `receipt_url` |
| `decision.date` | `accepted_on` |
| `reviewer` | `reviewer` |

A record's `publication.consumer_acceptance_url`, and any coverage receipt, must point to an accepting ledger decision that covers that record, field and use at that commit.

**No rights from a receipt.** A receiving decision grants no source-use rights. Rights come only from the producer's per-claim source, field and use decisions (H06, H20).

**Who may decide.**
- The reviewer must be able to decide for the consumer, as `reviewer_authority` records. An absent owner is never shown as having approved anything (#65 AC3).
- The reviewer is not the author of the producer revision under review (compare the contract's reviewer rule).

**Entry fields (task #91, S01 and S02).** Each ledger entry also carries:

| Field | Meaning |
| --- | --- |
| `kind` | `information` or `acceptance_gate` (#65 AC2) |
| `native_blocker` | `false` unless a native GitHub blocker is approved |
| `owning_package` | The application work package that delivers the producer artifact. `null` when nothing can express it yet |
| `required_for` | The work packages whose delivery needs this receipt; empty for information links |
| `consumer_status` | `confirmed` when the consumer was read back and can record a decision, otherwise `unresolved` |
| `consumer_evidence` | The dated readback: `read_on`, `state`, `title` |
| `unresolved_reason` | Why an unresolved consumer or artifact is unresolved |

The ledger has one consumer per entry. A consumer whose identity or receiving need is not confirmed is recorded as `unresolved`, never assumed (task #91, S02). Silence is unknown, not refusal.

**What closes #65 (proposed).** #65 needs no H-entry to be accepted. It closes when:
- every matrix interface maps to a ledger entry, or says why it needs none;
- every entry names a confirmed or unresolved consumer, its producing artifact and a pending or recorded decision;
- an independent reviewer accepts this record at an exact revision.

Each entry's `required_for` names the other packages whose delivery waits on it.
