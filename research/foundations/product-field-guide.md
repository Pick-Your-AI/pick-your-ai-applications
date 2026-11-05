# APP-F02.03 product field guide, part 1: user-facing capabilities and where they run

Issue: #70 (task #100; #101 follows) · Version 0.1.0 (proposed) · Status: proposed for review · Recorded: 2026-11-03
Value shapes: [schemas/product-profile.schema.json](../../schemas/product-profile.schema.json)

## User decision

Which product facts do people need to compare applications, and at what level: the product, an offering, a feature or a release?

This part covers what a person can do with a product and where it runs:
- inputs and outputs, at feature level (task #100, S01);
- availability, kept apart from account eligibility and from platform testing (task #100, S02);
- clients and platforms, deployment, installation, network dependence and runtime requirements.

Enterprise conditions (SSO, SCIM, RBAC, tenancy, retention, training use, export, residency, support and SLA) are part 2, task #101.

## Principles

1. **Every fact is a claim.** Each field below is a claim `field` in the existing application contract. It has an exact subject and scope (offering, region, locale, platform, conditions), sources, dates, grade and review. The guide adds no new record kind.
2. **Facets first.** Where the taxonomy already has a facet (`facets.availability`, `facets.access_surface`, `facets.deployment`, `facets.input_modality`, `facets.output_modality`), that facet claim carries the fact, and this guide adds no second field for it. Facets classify an offering. The fields here add the detail a comparison needs.
3. **Unknown stays unknown.** An unknown, undisclosed or inapplicable value stays `null` at claim level (`value_status`). Inside a known value, a sub-field the source does not state is left out, and leaving it out means *not stated*, never none, zero or unlimited. "Unlimited" needs a source that says so.
4. **The right level.** A capability is claimed for the feature or product that has it, an availability fact for the offering it applies to, and a requirement for the release it was stated for. A fact true of one plan, platform or release is never spread to the others.
5. **Nothing is inferred across entities.**
   - An application's deployment says nothing about how its models are served. That serving mode is research T0's per-component classification: who runs the serving runtime and on what capacity ([deployment-mode note](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T0-configuration/deployment-mode.md), blob `8d64fcc0`, read 2026-11-03, Summary and Definitions sections only).
   - A model's size never yields an application's runtime requirements.
   - Hardware fit stays with research T2's COMPUTE rules and runtime sizing (research #61).

## The fields

| Field | Subject | `fact_type` | Value (`$defs` in the profile schema) | Scope it needs | Evidence that can support it |
| --- | --- | --- | --- | --- | --- |
| `facets.input_modality`, `facets.output_modality` | feature or product | `classification` | Taxonomy facet value | offering, platform when they differ | Primary documentation; vendor claim |
| `product.io` | **feature**, or product when it has one workflow | `capability` | `io`: one entry per input or output channel, each with modality, formats, limits and conditions | offering, platform, conditions | Primary documentation; vendor claim. A measured limit is an independent measurement |
| `facets.availability` | offering | `availability` | Taxonomy facet value: what the vendor **advertises** | region, platform, offering | Primary documentation; vendor claim |
| `product.availability.eligibility` | offering | `availability` | `eligibility`: which kind of account can get it, and on what requirements | region, offering, conditions | Primary documentation of the rule (`basis: documented_rule`), or an observed sign-up (`basis: observed_sign_up`) |
| `product.availability.platform_test` | release, or offering with a version | `availability` | `platform_test`: a workflow run on a stated client, OS and architecture, and what happened | platform, offering | Independent measurement only (below) |
| `facets.access_surface` | offering or release | `classification` | Taxonomy facet value | platform | Primary documentation |
| `product.platform.client` | offering or release | `availability` | `client_platform`: operating systems, architectures, minimum OS versions | platform | Primary documentation; vendor claim |
| `facets.deployment` | offering | `classification` | Taxonomy facet value: vendor-hosted, customer-hosted, local or hybrid | offering | Primary documentation |
| `product.installation` | offering or release | `availability` | `installation`: install methods, and whether admin rights or an account are needed to install | platform | Primary documentation |
| `product.network` | offering or release | `capability` | `network`: whether it works offline (full, partial, none), what works offline, and what needs the network | platform, conditions | Primary documentation; vendor claim. Observed behavior is an independent measurement |
| `product.runtime.requirements` | **release** (`temporal_scope: version_pinned`) | `availability` | `runtime_requirements`: a minimum or a recommended set (memory, storage, accelerator, OS, architecture) and what it applies to | platform, conditions | Primary documentation; vendor claim. Measured fit is not recorded here |

### Inputs and outputs at feature level (S01)

- **One channel per direction and modality.** A feature that reads PDFs and images and writes text has three channels. The modality uses the taxonomy's input or output values (the schema refuses an output-only value such as `code` on an input). `formats` lists file types as the source names them.
- **Limits keep their own scope.** A limit has a kind, a decimal amount, a unit, what it applies to (per file, request, session, day or month) and its conditions, for example a plan, or "web client only". A limit stated for one plan or platform is claimed for that offering or platform only.
- **What stays out.** An unstated limit is left out, never recorded as "no limit". A limit that differs by plan is one claim per offering. Whether a limit holds in practice is an independent measurement with its receipt, not a reading of documentation.

### Advertised, eligible and tested are three facts (S02)

| Fact | Field | What it means | What it does not mean |
| --- | --- | --- | --- |
| Advertised | `facets.availability` | The vendor says the offering is generally available, in preview, waitlisted, limited, regional, retired or unavailable | That any given person can get it |
| Eligible | `product.availability.eligibility` | A stated kind of account, in the scoped region and plan, can obtain it: by the documented rule, or as observed in a sign-up on the claim's date | That it works on any platform |
| Tested | `product.availability.platform_test` | A named workflow ran on a stated client version, OS version and architecture, and it worked, partly worked or failed | That it works elsewhere, or for every account |

The three are never merged. A "works on Linux" claim built from advertised availability is refused. A sign-up observation records only what the researcher's own account could do, on that date, in that region. It makes no claim about other account kinds.

A platform test is an observation, so the contract requires it to be an `independent_measurement` with a verification receipt: someone other than the researcher reproduces it under a pinned protocol. Until then it stays in a research note, and the field stays unknown.

### Clients, deployment and installation

- `facets.access_surface` says which surfaces exist (web, desktop, mobile, browser or IDE extension, CLI). `product.platform.client` adds the operating systems, architectures and minimum versions the source states for one offering or release.
- `facets.deployment` says where the application runs. It never says where its models run, and a local application can still call hosted models. That is a `model:` relationship, and `product.network` records `inference` in `needs_network_for`.
- `product.installation` lists the install methods the source documents: app store, direct download, package manager, extension store, IDE marketplace, container image, source build, or hosted web with nothing to install. It also records whether installing needs admin rights or an account, when the source says so.

### Network dependence and offline use

`product.network` keeps three facts apart:
- `offline`: does the workflow run with no network at all, partly, or not at all;
- `works_offline`: what runs offline, in plain words from the source;
- `needs_network_for`: what does need the network, for example activation, sign-in, licence checks, updates, model downloads, inference, sync or telemetry.

"Works offline" in marketing is a vendor claim about the scoped release. An observation that it does is an independent measurement with its receipt.

### Runtime requirements for local applications

- `product.runtime.requirements` records what the vendor states for one release: a `minimum` or a `recommended` set, never mixed in one claim. Each set has memory, storage, accelerator use (not used, optional or required, GPU or NPU), accelerator memory, operating systems and architectures, and `applies_to`, which names what the set is for (for example "the bundled small model", "a 7B model at 4-bit").
- A requirement is claimed for the release it was stated for. It is never derived from model size, parameter count or another release's figures.
- Whether a given machine actually fits stays with research: T2's COMPUTE-01/02 rules apply to the serving component ([compute-capacity rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T2-infrastructure/rules/compute-capacity.md), blob `e9813b80`), and research #61 owns runtime sizing. This guide adds no second fit rule.

## What the schemas change

- **`schemas/product-profile.schema.json` is new.** It holds the value shapes above, using only the schema keywords the validator supports. It is a proposal; nothing binds a claim's value to it yet.
- **`schemas/application.schema.json` is unchanged in this part.** Binding a `product.*` claim's value to its shape would be a versioned contract change, the way pricing claims bind to `pricing.schema.json`. That binding is proposed for review after part 2, so both parts' fields can be bound in one versioned change.

## Inputs (information only, no native blockers)

| Source | Version | Read | Part read |
| --- | --- | --- | --- |
| Application contract 0.1.0, taxonomy 0.1.0 (this repository) | This branch's base `9ba7d9b` | 2026-11-03 | Claim semantics, facet rule, facet values |
| [research T0 deployment mode](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T0-configuration/deployment-mode.md) (research #3, closed) | Blob `8d64fcc0bf16222b0ed3e06dc53c396e525c0741` | 2026-11-03 | Summary and Definitions only: the operator/capacity vocabulary informs this guide and classifies no application |
| [research T2 compute-capacity rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T2-infrastructure/rules/compute-capacity.md) | Blob `e9813b80dfd638fdb8f3b8a1e96a57420a069d15` | 2026-11-03 | COMPUTE-01/02 headings and the shared-applicability section only |
| research #35, T6 guardrails (closed) | — | Not read | The backlog names it as information for safety boundaries. This part claims no safety capability, so nothing here relies on it |

## Acceptance mapping (APP-F02.03, the part this covers)

| Criterion | Where |
| --- | --- |
| Every field has type, meaning, allowed unknown state and evidence scope | The field table, with value shapes in the profile schema; unknown stays at claim level (principle 3) |
| Hosted and self-operated offerings are represented without inferring model deployment mode | Principle 5; "Clients, deployment and installation" |
| Security/compliance claims retain issuer, scope, dates and documentary limits | Part 2 (#101) |
| Portability, deletion and BYOK/BYOM claims identify product, plan and date, and documented promises are distinguished from exercised behavior | Part 2 (#101) |
| Factual conclusions scoped or unknown; source dates real | No product claims are made; every external source is pinned with what was read |
| Receiving decisions linked or pending | Pending: an independent application-research reviewer; research #61 as information for runtime requirements (H17 in the F01.02 ledger, #147) |
| #100 S01: modality and input/output constraints at feature level | "Inputs and outputs at feature level" |
| #100 S02: advertised availability separate from account eligibility and platform testing | "Advertised, eligible and tested are three facts" |

## Review requested

An independent application-research reviewer on this exact revision. Structural validation (`validate_applications.py`, `validate_planning.py`, tests) is reported separately from factual acceptance.
