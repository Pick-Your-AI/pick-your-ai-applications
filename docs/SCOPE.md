# Application scope

Version 1.0 (proposed) · Decision record: [research/foundations/application-scope.md](../research/foundations/application-scope.md) · Refs #64

This page is the short, normative statement of what this repository researches. The decision record holds the reasoning, the boundary cases and the open questions. A scope decision does not establish that any product exists, works as described or may be published.

## In scope

An **application** is identifiable software that gives a person or organization a usable workflow in which AI materially performs or assists the task. It must be one of:

- a standalone product (web, desktop, mobile, CLI, browser extension or hosted service);
- an **independently identifiable module** of a suite, with its own entry point, name or offering;
- a complete self-hosted or local application that a user installs and operates;
- a **software-delivered service**: a vendor-operated workflow, even with humans in the loop, that the customer uses through software and buys as a defined offering.

Eligible audiences: individual consumers, professionals, teams, organizations and public bodies. Eligible delivery: hosted, local, hybrid, open source, source-available and proprietary. Predictive, classification, perception, recommendation and optimization workflows count alongside generative and agentic ones.

## Out of scope (record and link instead)

| Entity | Where it lives |
| --- | --- |
| Foundation models, model releases, provider inference routes | `pick-your-ai-research` T1 (`model:` link only) |
| Accelerators, inference engines, hosting, generic infrastructure | `pick-your-ai-research` T2/T6 |
| Libraries, SDKs, frameworks, protocols, connectors, stand-alone MCP components | `pick-your-ai-research` T4 (`integration:` link) |
| Datasets, benchmarks, papers, directories | Datasets and papers programs; sources, not applications |
| Consultancies and agencies without a software-delivered workflow | Service-provider note, outside application counts |
| Announcements, demos, waitlists, abandoned or unconfirmed products | Candidate note until a usable offering is evidenced |

## Counting rules

- One application identity per product. Editions, plans, regions, languages and platforms are offerings or facets, not new applications.
- A branded AI feature inside a broader product gets a `feature:` record. It becomes an application only when it has an independent entry point, offering or product identity (see the decision table).
- The word "AI" in marketing is a discovery lead, not evidence of a material AI workflow.
- Unknown stays unknown. An unexamined product is not out of scope, and a failed check is not a negative finding.

## Relationship to the builder and to #47

This directory is a broad, evidence-backed reference corpus (research #509, G12). It does not change the frozen builder contract (research `contracts/v1/`). It makes no product-validation, demand, exclusivity or launch claim, so it is compatible with #47's NARROW program decision. Whether any application data reaches the builder is a separate consumer handoff.
