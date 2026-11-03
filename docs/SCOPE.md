# Application scope

Version 1.1 (proposed) · Decision record: [research/foundations/application-scope.md](../research/foundations/application-scope.md) · Refs #64

This page is the short, normative statement of what this repository researches. The decision record holds the reasoning, the boundary cases, the sources and the open questions. A scope decision does not establish that any product exists, works as described or may be published.

## In scope

An **application** is identifiable software that gives a person or organization a usable workflow in which AI materially performs or assists the task. It must be one of:

- a standalone product (web, desktop, mobile, CLI, browser extension or hosted service);
- an **independently identifiable module** of a suite, with its own entry point, name **and** offering;
- a complete self-hosted or local application that a user installs and operates;
- a **software-delivered service**: a vendor-operated workflow, even with humans in the loop, that the customer uses through software and buys as a defined offering. Its records keep the human-service steps and the software-automation steps apart.

Products whose job is producing software, such as coding assistants and app or website builders, are applications. Components that other software builds in are not (see the libraries row below).

Eligible audiences: every value of the taxonomy's `audience` facet, `unknown` included. Eligible delivery: every value of its `deployment` and `distribution_rights` facets. This is a plain-language summary; structured `facets.*` claims use the enumerated values in `taxonomy/taxonomy.json`. Predictive, classification, perception, recommendation and optimization workflows count alongside generative and agentic ones.

## Out of scope (record and link instead)

| Entity | Where it lives |
| --- | --- |
| Foundation models, model releases, provider inference routes | `pick-your-ai-research` T1 ([#4](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/4); providers [#5](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/5)), `model:` link only |
| Hardware: accelerators, compute, devices and components sold as hardware; inference engines, hosting and generic infrastructure | `pick-your-ai-research` T2 ([#8](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/8)) and T6 ([#34](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/34)). A device's companion app is open question U2 |
| Pure libraries, SDKs, frameworks, protocols, connectors and stand-alone MCP components, unless a distinct usable application product or module can be identified | `pick-your-ai-research` T4 ([#24](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/24)), `integration:` link |
| Datasets, benchmarks and papers | Sources or linked entities, not applications. Their receiving owners are pending (APP-F01.02, #65) |
| Directories of other products | Discovery sources, unless the directory itself offers an AI-assisted application workflow |
| Consultancies and agencies without a software-delivered workflow | Service-provider note, outside application counts |
| Announcements, demos, prototypes and products that were never usable | Candidate note until a usable offering is evidenced |

Waitlisted, preview, deprecated and retired products are not out of scope. A product with an identity and an entry point keeps a lifecycle record (`lifecycle`, `availability`), but it is not counted as an active or currently available application. The decision record says when a product gets a lifecycle record and when it gets a candidate note. Whether an unmaintained open-source project is usable is open question U3.

## Counting rules

- One application identity per product. Editions, plans, regions, languages and platforms are offerings or facets, not new applications.
- The same product on another surface, such as an editor plugin of a chat app, is an offering with an `access_surface` value, not a second application.
- A branded AI feature inside a broader product gets a `feature:` record. It becomes an application only when it has an independent entry point, name **and** offering (see the decision table).
- A suite is one application (`product_form: suite`). A module that meets the module rule is its own `app:` record linked to the suite. Until APP-F04.01 (#76) sets aggregate counting rules, counts never add a suite and its modules together.
- The word "AI" in marketing is a discovery lead, not evidence of a material AI workflow.
- Unknown stays unknown. An unexamined product is not out of scope, and a failed check is not a negative finding.

## Relationship to the builder and to #47

This directory is a broad, evidence-backed reference corpus (research #509, G12). It does not change the frozen builder contract (research `contracts/v1/`). It makes no product-validation, demand, exclusivity or launch claim, so it is compatible with #47's NARROW program decision. Whether any application data reaches the builder is a separate consumer handoff.
