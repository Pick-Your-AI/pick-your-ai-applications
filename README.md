# Pick Your AI Applications

Research and planning for an evidence-backed directory of end-user and enterprise AI applications, products and software services.

**Status: repository establishment and research backlog. Product research has not started. There are no verified product records or publication-approved records in this scaffold.** Taxonomy coverage describes planned research areas, not an exhaustive census of all AI software.

Parent: [Pick-Your-AI research #509, G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509).

**Live delivery:** [program #1](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/1) contains the native hierarchy for all 135 planned issues and 134 internal parent relationships. [Project #10](https://github.com/orgs/Pick-Your-AI/projects/10) exists; its item and field population is still pending. The scaffold is submitted in [PR #136](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/136), not yet merged. See the [establishment status](planning/ESTABLISHMENT_STATUS.md) for review, access-policy and cross-repository handoff gates.

## Scope

Research software that people or organizations use to accomplish a task: assistants, coding products, creative tools, business software, research applications, industry products, automation services and complete self-hosted applications. Include predictive, classification, perception, recommendation and optimization applications alongside generative products. Identifiable software-delivered services, including human-assisted operational services with a distinct software workflow, are in scope; generic consulting or implementation agencies without that workflow stay outside application counts. Include hosted, local, open-source, proprietary, mobile, desktop, web and hybrid delivery when supported by evidence. Record AI-enabled features within broader products without treating every feature as a new product.

Model families, checkpoints, inference engines, hardware, framework libraries, stand-alone MCP components and builder compatibility remain with [pick-your-ai-research](https://github.com/Pick-Your-AI/pick-your-ai-research). Link those records when their relationship to an application is actually disclosed. Dataset and literature directories have separate research ownership. Implementation of the public directory remains with [pick-your-ai-website](https://github.com/Pick-Your-AI/pick-your-ai-website).

## Start here

- [Taxonomy](taxonomy/README.md): domains, categories, subcategories, facets and exclusions.
- [Live backlog](planning/LIVE_BACKLOG.md): native GitHub program and epic entry points, plus the complete verified issue-ID mapping.
- [Authored delivery plan](planning/BACKLOG.md): program, epics, work packages, task and subtask structure.
- [Organization alignment](docs/ORGANIZATION_ALIGNMENT.md): inspected policies, ownership and existing handoffs.
- [Research workflow](docs/RESEARCH_WORKFLOW.md): candidate discovery through reviewed evidence and a separate publication decision.
- [Application contract](docs/APPLICATION_CONTRACT.md): standalone versioned metadata; no changes to research's frozen builder v1.
- [Coverage ledger](coverage/README.md): explicit denominators, overlap, unknowns and zero-start counters.
- [Resumable setup](docs/PROVISIONING.md): dry-run-first provisioning helper and exact remote readback.
- [Establishment receipt](planning/ESTABLISHMENT_STATUS.md): actual remote operations and remaining setup blockers.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md), the assigned issue and the organization policy. Use native sub-issues for independently reviewable deliverables. Keep small steps as task/subtask checklists. Live issue assignees determine ownership; a planning entry does not assign a person or establish their approval.

```sh
python scripts/validate_applications.py
python scripts/validate_planning.py
python -m unittest discover -s tests -v
```

Validation checks structure and evidence prerequisites. It does not prove source truth, independent reproduction, legal permission, product quality or live website delivery. Synthetic examples live only under `tests/fixtures/` and never count as researched applications.

## Evidence and rights

Unknown is different from Unsupported. Reading a primary source establishes a dated source check, not independently verified behavior. Scope every claim by relevant product, feature, release, plan, platform, geography and date. Separate claimed capability, documented availability, exercised behavior, independent evidence, price and publication eligibility.

Original repository code and documentation use the [MIT license](LICENSE), following the existing research repository. That license does not relicense third-party text, screenshots, logos, reviews, source databases or other evidence. See [THIRD_PARTY_RIGHTS.md](THIRD_PARTY_RIGHTS.md).
