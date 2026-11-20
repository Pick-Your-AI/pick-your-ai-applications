# APP-F02.03 product field guide: user-facing capabilities, deployment and enterprise conditions

Issue: #70 (tasks #100 and #101) · Version 0.1.0 (proposed) · Status: proposed for review · Recorded: 2026-11-17 (Part 1 #100 recorded 2026-11-03; Part 2 #101 added 2026-11-17)
Value shapes: [schemas/product-profile.schema.json](../../schemas/product-profile.schema.json)

## User decision

Which product facts do people need to compare applications, and at what level: the product, an offering, a feature or a release?

This guide specifies both parts of APP-F02.03:
- **Part 1 (#100):** what a person can do with a product and where it runs — inputs and outputs at feature level (`T01.S01`), availability kept apart from account eligibility and platform testing (`T01.S02`), clients and platforms, deployment, installation, network dependence and runtime requirements;
- **Part 2 (#101):** plan-conditioned enterprise governance, privacy, data handling, portability/deletion, residency, support/SLA, security assurance and BYOK/BYOM entitlements — distinguishing documented feature existence from plan entitlement, configured enforcement and independently exercised behavior (`T02.S01`), and requiring dated primary source links (`T02.S02`).

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

## Part 2: enterprise conditions, trust boundaries, portability, support and BYOK/BYOM (#101)

`facets.enterprise_controls` in `taxonomy/taxonomy.json` establishes the organizing rule: enterprise controls remain scoped claim records, and *"Enterprise plan naming is not proof of any control."* Each claim below MUST bind to an exact offering (`scope.offering_id`) or scoped release/region and carry dated source provenance (`source_ids`, `checked_on`, `as_of`).

| Field | Subject | `fact_type` | Value (`$defs` in the profile schema) | Scope & dates required | Evidence & verification rules |
| --- | --- | --- | --- | --- | --- |
| `product.enterprise.identity_access` | offering | `security` | `enterprise_identity_access` (uses `enterprise_control_state`): `sso`, `scim`, `rbac`, or `admin_audit_logs` | offering, conditions, `checked_on`, `as_of` | Primary documentation; independent verification requires reproducing configured enforcement (`exercised_status`) |
| `product.enterprise.tenancy` | offering | `security` | `enterprise_tenancy` (uses `enterprise_control_state`): shared vs logical vs single-tenant vs customer-hosted isolation | offering, region when regional, `checked_on`, `as_of` | Primary documentation; architecture docs and DPA terms stay attributed without inferring hardware/model isolation |
| `product.data.retention` | offering | `privacy` | `data_retention` (uses `enterprise_control_state`): `data_class`, `retention_mode`, optional `duration_days` (`decimal`) | offering, region when regional, conditions, `checked_on`, `as_of` | Dated privacy policy / DPA / product docs (`T02.S02`); leave unstated windows out and preserve `unknown` / `not_disclosed` at claim level |
| `product.data.training_use` | offering | `privacy` | `training_use` (uses `enterprise_control_state`): `default_policy`, optional `opt_out_mechanism`, optional `human_review_exception` | offering, region, conditions, `checked_on`, `as_of` | Dated privacy/DPA/terms (`T02.S02`); never infer "no training" from general confidentiality wording or an Enterprise label |
| `product.data.portability_deletion` | offering | `terms` (or `privacy`) | `portability_deletion` (uses `enterprise_control_state`): `data_export`, `account_deletion`, or `workspace_migration`, optional `export_formats`, `completeness`, `deletion_sla_days`, `retained_backups_note` | offering, conditions, `checked_on`, `as_of` | Dated terms/docs for documented promises; `exercised_status` distinguishes documentation from independent export/deletion testing |
| `product.data.residency` | offering | `privacy` | `data_residency` (uses `enterprise_control_state`): `regions`, `applies_to_stages` (storage vs inference vs backups vs telemetry vs support), optional `pinning_guarantee`, `cross_border_exceptions` | region, offering, conditions, `checked_on`, `as_of` | Dated regional/DPA docs (`T02.S02`); storage residency never establishes in-region inference or support access |
| `product.support.sla` | offering | `support` | `support_sla` (uses `enterprise_control_state`): `channels`, optional `coverage_hours`, `first_response_hours`, `uptime_sla_percent` (`decimal`), `uptime_measurement_window`, `remedy_kind`, `exclusions` | offering, conditions, `checked_on`, `as_of` | Dated support/SLA contract; response targets or uptime percentages require explicit contract text and stated exclusions |
| `product.security.assurance` | offering or product | `compliance` | `security_assurance` (uses `iso_date`): `framework_or_standard`, `issuer`, `covered_scope`, optional `period_start`/`period_end`/`expires_on`, `report_access`, non-empty `documentary_limits` | offering or product, region, conditions, `checked_on`, `as_of` | Retain issuer, exact covered scope, dates and access limits; never generate blanket "certified/compliant/secure" badges |
| `product.security.byok_byom` | offering | `security` (or `capability`) | `byok_byom` (uses `enterprise_control_state`): `byok_encryption`, `byom_model_endpoint`, or `byok_provider_api_key`, optional `supported_targets`, `residual_exposure_or_fee_notes` | offering, region, conditions, `checked_on`, `as_of` | Primary documentation for entitlement; independent verification required before marking `exercised_status` as exercised |

**Numeric SLA promises are scoped, not free-floating.** A documented `uptime_sla_percent` must include its `uptime_measurement_window` (for example, calendar month or rolling 30 days). `first_response_hours` must include `coverage_hours` identifying when that time applies. Omit both the number and its window when either is unreported; an absent measure never implies a zero response time, universal coverage, or a contractual guarantee. These are proposed `support_sla` value-shape constraints only; application contract `0.1.0` still does not bind `product.*` values.

### Feature existence vs plan entitlement vs configured enforcement (#101 T02.S01)

Every control using `enterprise_control_state` keeps five distinct facts separate:

| Question | Field / value | What it establishes | What it never implies |
| --- | --- | --- | --- |
| Does the vendor document the control at all? | `documented_status` (`documented`, `documented_with_conditions`, `explicitly_unavailable`) | Supplier docs or terms state the capability or its explicit unavailability for this scope | That it is included in every plan or turned on |
| Who is entitled to it on this offering? | `entitlement_scope` (`included_in_plan`, `paid_add_on`, `enterprise_contract_only`, `seat_or_tier_minimum`, `beta_or_limited`, `not_entitled`) | Commercial/plan gate documented for the scoped offering (`scope.offering_id`) | Default runtime enforcement |
| How is it enforced in tenant configuration? | `configured_enforcement` (`mandatory_default`, `admin_configurable`, `opt_in_disabled_by_default`) | Whether an admin/user must configure or enable it before it protects data | That an independent verifier observed it working |
| What state is evidenced for this configuration? | `configuration_status` (`enabled`, `disabled`) | The state of the exact documented or tested configuration identified in `scope.conditions` | That the product lacks the feature or the plan lacks entitlement |
| Has a claim been independently exercised? | `exercised_status` (`documented_only`, `independently_verified_config`, `independently_exercised`) | Whether the claim rests solely on vendor docs or on a reproduced configuration/functional test | Broad certification beyond the tested product, plan and workflow |

Rules for `enterprise_control_state`:
- Unstated sub-fields (`entitlement_scope`, `configured_enforcement`, `configuration_status`, `conditions`, `duration_days`, `opt_out_mechanism`, `export_formats`, etc.) are **omitted**, never recorded as `false`, `"0"` or `"unlimited"`.
- Missing disclosures at the claim level use `value_status: "unknown"` or `"not_disclosed"` with JSON `value: null`. A whole unsupported capability requires checked explicit negative evidence, `value_status: "unsupported"`, `explicit_negative_evidence: true` and literal JSON `value: false`. A structured `documented_status: "explicitly_unavailable"` object is never a valid Unsupported envelope; known-object shape validation applies only to `value_status: "known"`.
- A documented feature can have `documented_status: "documented"` and `entitlement_scope: "not_entitled"` for the selected offering. This is a **known scoped negative entitlement**, not whole-feature Unsupported. `configured_enforcement` describes default/configuration policy; `configuration_status: "disabled"` describes an evidenced configuration state. Neither implies the other.
- Keep existence, entitlement and configuration as separate claims when their evidence or scope differs. Identify the dimension and control in `scope.conditions`, including when the entire dimension is unknown (`value_status: "unknown"`, `value: null`). For example, SSO can be documented, not entitled on the selected plan, and disabled in a separately scoped configuration. Omitted `configuration_status` is unstated, never enabled or disabled. A configuration statement requires a sanitized exact configuration scope and its own source or permitted test receipt; do not publish private account or identity-provider details.
- Any claim with `exercised_status` set to `"independently_verified_config"` or `"independently_exercised"` **must** carry `evidence_grade: "independent_measurement"`, `verification_status: "verified"`, and a non-null `verification` receipt naming a verifier distinct from both the researcher and the vendor. Documentation alone always leaves `exercised_status: "documented_only"` and `verification_status: "unverified"`.

### Dated sources for privacy, retention, residency, portability and BYOK/BYOM (#101 T02.S02, #70)

- **Dated primary links are mandatory.** Privacy (`product.data.training_use`), retention (`product.data.retention`), residency (`product.data.residency`), portability/deletion (`product.data.portability_deletion`) and SLA/assurance claims are `current_state` facts: they require `temporal_scope: "current_state"`, a non-null `as_of` date, a non-null `checked_on` date, and at least one active canonical HTTP(S) source in `sources` whose `accessed_on` matches the inspection.
- **Account deletion vs retained backups.** `product.data.portability_deletion` separates user-initiated or admin-initiated production account deletion from backup retention (`retained_backups_note` and `deletion_sla_days`) and keeps export format (`export_formats`) separate from export `completeness` (`full_workspace_and_history` vs `partial_user_artifacts_only` vs `excludes_audit_logs_or_metadata`).
- **BYOK vs BYOM.** `product.security.byok_byom` distinguishes customer-managed KMS encryption keys (`byok_encryption`), bringing a customer's own external model endpoint (`byom_model_endpoint`), and entering a provider API key (`byok_provider_api_key`). Documented `residual_exposure_or_fee_notes` capture metadata/prompt transit through the vendor control plane or separate underlying API billing without conflating application deployment with model serving (`research #3`).
- **Assurance reports and documentary limits.** `product.security.assurance` requires `issuer`, exact `covered_scope`, `report_access` (`public`, `nda_trust_portal`, or `vendor_summary_only`) and non-empty `documentary_limits`, plus `iso_date` (`YYYY-MM-DD`) fields (`period_start`, `period_end`, `expires_on`) when stated. No security/compliance claim produces a blanket badge, composite trust score, or legal determination (`trust-evidence.md` in APP-F03.04 owns documentary trust intake and presentation boundaries; this guide defines the typed structured claim values).

## Review of `schemas/application.schema.json` (0.1.0) and proposed `0.2.0` binding path

Both #70 deliverables list `schemas/application.schema.json` for review while prohibiting unapproved breaking changes or extraction prerequisites in `0.1.0`.

### Assessment of `schemas/application.schema.json` (0.1.0)

1. **What `0.1.0` already supports cleanly:**
   - `$defs.claim` already provides all core evidence, provenance and scope metadata needed for Part 1 and Part 2: `subject` (`app:`, `feature:`, `offering:`, `release:`), `fact_type` (`classification`, `capability`, `availability`, `security`, `privacy`, `compliance`, `terms`, `support`), `value_status` (`known`, `unknown`, `not_disclosed`, `not_applicable`, `disputed`, `unsupported`), `source_status`, `verification_status`, `evidence_grade`, `checked_on`, `temporal_scope`, `version`, `as_of`, `scope.{offering_id, region, locale, platform, conditions}`, `evidence_state`, `explicit_negative_evidence`, `review`, `verification`, and `method_and_limitations`.
   - Keeping unknown/undisclosed values at `value: null` works identically across Part 1, Part 2 and `pricing` claims.
2. **Gaps in `0.1.0` that remain intentionally unbound until `0.2.0`:**
   - In `scripts/validate_applications.py`, `fact_type == "pricing"` with `value_status == "known"` already validates `claim.value` against `schemas/pricing.schema.json` (`validate_applications.py` line 378), whereas `product.*` claims leave `claim.value` generically typed in `0.1.0` (`object|array|string|number|boolean|null`).
   - `application.schema.json` `0.1.0` does not enforce a field-to-`$defs` lookup for `product.*` fields, does not enforce `subject.entity_type` or non-null `scope.offering_id` on plan-conditioned enterprise controls, and does not reject `exercised_status` != `"documented_only"` when `verification_status == "unverified"`.
   - Separate schema extraction (moving pricing or product-profile claims out of embedded `claims[]` or modifying `application.schema.json` `$id`/version) is **not** performed here because `0.1.0` must stay backward-compatible until independent review and downstream handoffs accept one coordinated contract bump.

### Proposed `0.2.0` validator & contract binding (for single versioned review)

If a future shared-use interface is proposed, obtain the genuinely affected receiving owners' decisions (research #40 and applicable catalog-pipeline/website owners) on that concrete artifact before adoption. The proposed coordinated `0.2.0` application contract bump would bind `claim.field` -> `$defs/<shape>` in `schemas/product-profile.schema.json` (analogous to `pricing` -> `pricing.schema.json`) as follows:

| `claim.field` | `$defs` shape | Required `fact_type` | Binding invariants to enforce in `0.2.0` |
| --- | --- | --- | --- |
| `product.io` | `io` | `capability` | `subject` is `feature` or `application_product` |
| `product.availability.eligibility` | `eligibility` | `availability` | non-null `scope.offering_id` and `as_of` |
| `product.availability.platform_test` | `platform_test` | `availability` | `evidence_grade == "independent_measurement"`, `verification_status == "verified"`, non-null `verification` |
| `product.platform.client` | `client_platform` | `availability` | non-null `scope.platform` or scoped offering/release |
| `product.installation` | `installation` | `availability` | `subject` is `application_offering` or `application_release` |
| `product.network` | `network` | `capability` | observed offline claim requires `independent_measurement` |
| `product.runtime.requirements` | `runtime_requirements` | `availability` | `temporal_scope == "version_pinned"` and non-null `version` |
| `product.enterprise.identity_access` | `enterprise_identity_access` | `security` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`; exercised rule below |
| `product.enterprise.tenancy` | `enterprise_tenancy` | `security` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`; exercised rule below |
| `product.data.retention` | `data_retention` | `privacy` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`, non-empty `source_ids` |
| `product.data.training_use` | `training_use` | `privacy` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`, non-empty `source_ids` |
| `product.data.portability_deletion` | `portability_deletion` | `terms` or `privacy` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`; `exercised_status != "documented_only"` requires `independent_measurement` + `verified` |
| `product.data.residency` | `data_residency` | `privacy` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `scope.region`, `as_of`, `checked_on`, non-empty `source_ids` |
| `product.support.sla` | `support_sla` | `support` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on` |
| `product.security.assurance` | `security_assurance` | `compliance` | `temporal_scope == "current_state"`, non-null `as_of`, `checked_on`, non-empty `documentary_limits` |
| `product.security.byok_byom` | `byok_byom` | `security` or `capability` | `temporal_scope == "current_state"`, non-null `scope.offering_id`, `as_of`, `checked_on`; `exercised_status != "documented_only"` requires `independent_measurement` + `verified` |

`schemas/application.schema.json` remains unchanged at `0.1.0` in this PR; `schemas/product-profile.schema.json` uses only the supported JSON Schema vocabulary in `scripts/validate_applications.py` (`check_schema_vocabulary` passes), and synthetic integration fixtures demonstrate compatibility against `0.1.0` today.

## Inputs (information only, no native blockers)

| Source | Version | Read | Part read |
| --- | --- | --- | --- |
| Application contract 0.1.0, taxonomy 0.1.0 (this repository) | Base `9ba7d9b` (Part 1); `19f6cf2` (Part 2 & schema review) | 2026-11-03; 2026-11-17 | Claim semantics, facet rule, facet values (`facets.enterprise_controls`, `application.schema.json` `$defs.claim`, `validate_applications.py`) |
| [research T0 deployment mode](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T0-configuration/deployment-mode.md) (research #3, closed) | Blob `8d64fcc0bf16222b0ed3e06dc53c396e525c0741` | 2026-11-03 | Summary and Definitions only: the operator/capacity vocabulary informs this guide and classifies no application |
| [research T2 compute-capacity rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/fef30de5428bf166f179ba3a9260c1a0348b880c/research/T2-infrastructure/rules/compute-capacity.md) | Blob `e9813b80dfd638fdb8f3b8a1e96a57420a069d15` | 2026-11-03 | COMPUTE-01/02 headings and the shared-applicability section only |
| research #35, T6 guardrails (closed) | — | Not read | Named in #70 as informational boundary context; this guide specifies structure and evidence boundaries without asserting safety or guardrail compliance for any product |

## Acceptance mapping (APP-F02.03, parts 1 and 2)

| Criterion | Where |
| --- | --- |
| Every field has type, meaning, allowed unknown state and evidence scope | Part 1 and Part 2 field tables, with `$defs` shapes in `schemas/product-profile.schema.json`; unknown stays `null` at claim level (`value_status`), unstated sub-fields omitted (Principle 3) |
| Hosted and self-operated offerings are represented without inferring model deployment mode | Principle 5; "Clients, deployment and installation"; `enterprise_tenancy`; `byok_byom` (`byom_model_endpoint` notes) |
| Security/compliance claims retain issuer, scope, dates and documentary limits | Part 2: `product.security.assurance` (`security_assurance` with required `issuer`, `covered_scope`, `report_access`, non-empty `documentary_limits` and optional `iso_date` period/expiry dates) |
| Portability, deletion and BYOK/BYOM claims identify product, plan and date, and documented promises are distinguished from exercised behavior | Part 2: `product.data.portability_deletion` (`portability_deletion`) and `product.security.byok_byom` (`byok_byom`), embedding `enterprise_control_state` (`exercised_status`) and claim-level `scope.offering_id` + `checked_on`/`as_of` |
| Factual conclusions scoped or unknown; source dates real | No real product claims are made; all repository fixtures are marked `synthetic: true` in `tests/fixtures/` with `.invalid` hosts |
| Receiving decisions linked or pending | Pending: qualified independent non-author review of this exact revision. H17 / research #61 is information only; a future concrete shared-use `0.2.0` interface has its own affected-owner acceptance |
| #100 S01: modality and input/output constraints at feature level | "Inputs and outputs at feature level (S01)" |
| #100 S02: advertised availability separate from account eligibility and platform testing | "Advertised, eligible and tested are three facts (S02)" |
| #101 S01: distinguish feature existence from entitlement and configured enforcement | "Feature existence vs plan entitlement vs configured enforcement (#101 T02.S01)" and `$defs/enterprise_control_state` |
| #101 S02: require dated source links for privacy, retention and regional service claims | "Dated sources for privacy, retention, residency, portability and BYOK/BYOM (#101 T02.S02, #70)" |
| Initial `schemas/application.schema.json` definitions reviewed; extraction remains proposed versioned change | "Review of `schemas/application.schema.json` (0.1.0) and proposed `0.2.0` binding path" (`0.1.0` left unbroken) |

## Review requested

An independent non-author application-research reviewer on this exact revision. Structural validation (`validate_applications.py`, `validate_planning.py`, `tests/test_product_profile.py` and full `tests/` suite) is reported separately from factual acceptance. Bounded #101 acceptance requires its scoped decision record merged and qualified non-author exact-revision review; parent #70 separately synthesizes #100 and #101. `planning/handoffs.json` records H17 as `kind: information`, `native_blocker: false`, `required_for: []` for research #61 runtime sizing. This change preserves that boundary and proposes no concrete new external interface, so H17 and future `0.2.0` adoption are not premerge or child-closure gates. Any actual future shared-use contract change needs its genuinely affected receiving owners' decisions at that revision; none is implied here.
