# APP-F02.03 product field guide: capabilities, deployment and enterprise conditions

Issue: #70 (tasks #100, #101) · Version 0.1.0 (proposed) · Status: proposed for review · Recorded: 2026-11-03; enterprise proposal added 2026-11-17
Value shapes: [schemas/product-profile.schema.json](../../schemas/product-profile.schema.json)

## User decision

Which product facts do people need to compare applications, and at what level: the product, an offering, a feature or a release?

This part covers what a person can do with a product and where it runs:
- inputs and outputs, at feature level (task #100, S01);
- availability, kept apart from account eligibility and from platform testing (task #100, S02);
- clients and platforms, deployment, installation, network dependence and runtime requirements.

Part 2 below specifies enterprise conditions for task #101. These are proposed research value shapes, not product facts, adopted enterprise policy or an application-admission binding.

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

## Part 2: enterprise conditions (task #101)

Each row below describes **one claim**, not a completeness checklist to fill with guesses. The existing claim envelope carries its product/feature/offering/release `subject`, `field`, `fact_type`, `scope.offering_id`, `scope.region`, `scope.platform`, `scope.conditions`, `version`, `temporal_scope`, `as_of`, source IDs, actual source-check date, evidence grade and review. Keep the plan/edition or account entitlement in the evidenced offering identity and conditions. Unknown plan, version or geography is recorded as unknown in that envelope and in unresolved notes; a null region never means worldwide. A conditional fact cannot be broadened to a whole product. The value's optional `conditions` adds detail without replacing envelope scope or provenance.

| Field | Subject and `fact_type` | Value shape | Required comparison distinction and evidence |
| --- | --- | --- | --- |
| `enterprise.control` | feature or offering; `capability` | `enterprise_control` | SSO, SCIM, RBAC and audit logs: a distinct claim for feature existence, plan entitlement or configured enforcement; documented availability never proves configuration |
| `enterprise.data_governance` | offering or release; `capability` | `data_governance` | One retention, deletion, residency or training-use statement per data category and scope; attribute the stated policy or commitment, preserve exceptions and backup limits |
| `enterprise.support` | offering; `capability` | `support_commitment` | Support response promises and SLA commitments are distinct; retain service hours, metric, measurement window, exclusions and remedies when stated |
| `enterprise.assurance` | offering or release; `capability` | `assurance_statement` | Attribute a certification, assessment or supplier assertion to its issuer, document and assessed scope; no application-wide compliance guarantee |
| `enterprise.portability` | offering or release; `capability` | `portability` | Separate export, import, migration and deletion; state formats, data categories, completeness, dependencies and residual data only when evidenced |
| `enterprise.external_model_access` | offering or release; `capability` | `external_model_access` | BYOK and BYOM are separate modes, not proof of local execution, free access, universal provider support or permission to use a model |

### Existence, entitlement and configured enforcement (S01)

`enterprise_control` requires a `control`, a `dimension` and an `enabled` boolean. `dimension` is exactly one of `feature_exists`, `plan_entitlement` or `configured_enforcement`. Record them as separate scoped claims, because a product can offer SSO while a particular plan lacks it or an account has not enabled it. A configuration claim must identify the tested or documented configuration in `scope.conditions`; customer settings, identity-provider identities and private audit data do not belong in public evidence. An observed enforcement test needs an authorized synthetic protocol, a run receipt and the contract's independent verification conditions before it is called an independent measurement. No such test is performed by this proposal.

Optional `protocols`, `details` and `conditions` describe only what the source states: for example which SSO protocol, which provisioning direction, which RBAC actions or which audit events. RBAC does not imply fine-grained authorization, SCIM does not imply complete deprovisioning, and an audit-log feature does not imply an immutable or complete security history. `enabled: false` can record a sourced disabled configuration; it does not silently make the feature unsupported. An explicit negative capability is an outer `value_status: unsupported` claim with `value: false`, checked sources and `explicit_negative_evidence: true`, as the existing contract requires.

### Data terms, dates and regional limitations (S02)

`data_governance` requires the `topic`, attributed `statement` and `basis` (`published_terms`, `contractual_commitment` or `vendor_statement`). The basis describes the document, not a new evidence grade or a legal conclusion. Keep user inputs, outputs, telemetry, logs, embeddings and backups separate when their treatment differs. `duration_days`, `backup_retention_days`, `locations`, `data_categories` and `exclusions` are optional details: omission means unstated, never zero retention, no exceptions or unrestricted geography. A sourced zero-day duration is the decimal string `"0"`, not an inferred default.

Retention, deletion, residency and training-use promises need dated source links through the claim envelope, with the exact product/plan/release/region and effective conditions. A residency statement must distinguish storage, processing, support access and backup locations in its statement or conditions; one location does not establish all four. Deletion-request availability, completion times, residual backups, legal holds and account termination are separate questions. Training terms must retain opt-in/opt-out conditions and relevant data categories. A policy or contract promise stays documentary evidence; an exercised deletion or geographic behavior claim needs its own permitted experiment and receipt. No customer data or restricted customer contract is collected here.

### Support, SLA and assurance statements

A `support_commitment` records either `support` or `sla`, with the attributed statement and documentary basis. Numeric `target` requires a metric, unit and measurement window. Do not turn response time into resolution time, advertised uptime into measured uptime, or service credits into a guaranteed remedy. Undisclosed remedies, operating hours and exclusions are omitted and remain unresolved; explicit empty arrays are appropriate only when evidence actually establishes no items.

An `assurance_statement` identifies its kind, issuer, document title, assessed scope, attributed statement and at least one retained limitation. `issued_on` and `valid_until` retain stated document dates when available; unknown dates are omitted and listed as unresolved, never replaced with the source-check date. These value shapes check date syntax only. Review must check real calendar dates, the exact document, coverage period, scope and whether the cited material supports the statement. A vendor's certification badge stays a supplier statement until the relevant issuer document is checked. A certificate for an organization, infrastructure supplier, region or historic service version does not automatically cover this application, plan or use case. This proposal provides no legal, security or regulatory compliance determination.

### Portability, lock-in and external-model access

`portability` requires an `operation` and attributed `statement`. An export-format list alone does not prove export completeness, round-trip import, preserved relationships or successful migration. Preserve missing attachments, configurations, history, proprietary formats, egress charges and replacement-service dependencies when documented, using `completeness`, `migration_requirements`, `residual_data` and conditions. Do not calculate a universal lock-in score from documentation completeness. A documented deletion promise is distinct from an exercised deletion result.

`external_model_access` requires the mode `byok` or `byom` and an attributed statement. Optional provider/model lists are positive statements about the exact offering, not universal compatibility. Record key handling, execution location, responsibilities, external costs and residual platform costs only when sourced. Missing cost fields mean unknown, not free. Actual prices use the separately scoped pricing contract; prose here does not create a numeric rate. BYOK does not establish who operates inference; BYOM does not establish model redistribution rights or local execution. Never place actual keys, account identifiers or private endpoints in values or fixtures.

### Missing values and acceptance boundaries

Unknown, undisclosed, inapplicable and disputed whole claims retain the existing `value_status` and null `value`; do not validate null against a known-value shape. Inside a known object, omit an unstated optional detail. Explicit empty lists, false booleans and zero decimal strings are substantive facts requiring evidence. A wholly unsupported capability uses the existing negative-claim envelope rather than an empty object, invented denial reason or fabricated known value. The tests use only synthetic fixture claims and reserved example hosts.

This part was written from the local contract, existing policy and baseline `19f6cf2c23668e1b426882ab3c2be8cfce1f899e`, inspected 2026-11-17. No new vendor terms, primary product facts, legal permissions, exercised behavior or independent measurements were researched. Each future real claim still needs actual dated primary evidence, a qualified non-author reviewer at its exact revision and separate source/field/use rights decisions. An affected receiving owner must accept any concrete shared-use or export interface, including research #40 when shared schema use is affected and pipeline/website owners for consumer consequences. No receiving decision is supplied here, and informational links do not become blanket blockers to drafting this proposal.

## What the schemas change

- **`schemas/product-profile.schema.json` contains the proposed values for both parts.** The enterprise definitions extend the existing product profiles using only schema keywords the validator supports. Nothing binds a claim's value to these shapes yet.
- **`schemas/application.schema.json` is unchanged in this part.** Binding a `product.*` or `enterprise.*` claim's value to its shape would be a separately reviewed, versioned contract change, the way pricing claims bind to `pricing.schema.json`. Part 2 does not introduce that binding; production admission still does not enforce these proposed value shapes.

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
| Security/compliance claims retain issuer, scope, dates and documentary limits | Part 2: assurance statements, with unknown document dates omitted and explicitly unresolved |
| Portability, deletion and BYOK/BYOM claims identify product, plan and date, and documented promises are distinguished from exercised behavior | Part 2: common scope, portability and external-model access |
| Factual conclusions scoped or unknown; source dates real | No product claims are made; every external source is pinned with what was read |
| Receiving decisions linked or pending | Pending: an independent application-research reviewer; research #61 as information for runtime requirements (H17 in the F01.02 ledger, #147) |
| #100 S01: modality and input/output constraints at feature level | "Inputs and outputs at feature level" |
| #100 S02: advertised availability separate from account eligibility and platform testing | "Advertised, eligible and tested are three facts" |

## Review requested

An independent application-research reviewer on this exact revision. Structural validation (`validate_applications.py`, `validate_planning.py`, tests) is reported separately from factual acceptance.

## Task #101 acceptance mapping

| Outcome | Where | Remaining gate |
| --- | --- | --- |
| S01: feature existence, entitlement and configured enforcement are distinct | Part 2 control dimension and scoped evidence rules | Actual source/review/configuration receipts for any future real claim |
| S02: dated privacy, retention and regional-service evidence | Part 2 data terms and existing claim envelope | Actual source checks; unknown details remain unresolved |
| Committed scoped output with unknowns | Part 2 and proposed profile definitions | Qualified non-author assessment of this revision |
| Exact-revision review separate from structural validation | Tests exercise synthetic shapes and existing claim semantics | PR review and affected receiving decisions remain pending; no application binding or consumer acceptance claimed |
