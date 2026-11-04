# Applications repository: organization and research alignment

Inspection date: 2026-10-22. This is an implementation-planning interpretation of the current source documents, not a change to their accepted policies, a source-use grant, a product-capability verification, or a claim that the proposed repository resources already exist. The user's current execution request authorizes establishing the dedicated applications scope proposed in [research #509](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509).

## Binding conventions to preserve

| Area | Observed organization convention | Applications adaptation |
| --- | --- | --- |
| Research scope | [Research CONTRIBUTING](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/CONTRIBUTING.md) separates research completion from runtime implementation. | Deliver an evidence-backed applications research corpus and consumer contract. Do not claim a deployed public directory. |
| Ownership | GitHub Assignees are authoritative. Live co-assignees and authorized delegation supersede old owner tables. | Leave research packages unassigned until actual assignment; do not invent acceptance by people named in historical workstreams. Record reviewer roles separately from personal approval. |
| Access | [Organization CONTRIBUTING](https://github.com/Pick-Your-AI/.github/blob/main/CONTRIBUTING.md) uses team grants and limits team membership changes to designated administrators. | Reuse authorized maintainer teams when actually available. CODEOWNERS is a review-routing file, not proof of repository access or required-review enforcement. |
| Reviews | One non-author approval is required; a later push needs a non-pusher approval. Maintainers use the documented branch-restriction bypass only after approval/checks. | Scaffold initialization does not grant ongoing self-approval. Use focused PRs and report any actual enforcement/approval gaps without inventing review receipts. |
| Workflow | Contributors use `contrib/<login>/<topic>` branches. All workflows may use only GitHub-owned `actions/*`. | Add local offline validators and a minimal Actions workflow using only permitted actions. Do not clone deployments or secret-dependent workflows. |
| Hierarchy | Native sub-issues track separately owned or independently reviewable deliverables; small steps are checklists. Do not duplicate native child links as a body checklist. | Program → domain/foundation epic → work package → independently reviewable task. Small subtasks inside tasks are checklists. Do not manufacture separately tracked issue records for trivial editing steps. |
| Issue body | User decision; scope in/out; research questions; deliverable; comparison fields/evidence; dependencies/relationships; acceptance criteria; open questions. | Reuse these headings for every package. Program and epics additionally require child-outcome synthesis and receiving handoffs. |
| Labels and Project | Labels express type/topic. Project fields express status, priority, workstream/readiness. Assignees are not duplicated in a custom Owner field. | Use `type: research` for applications research; `type: workstream` is reserved by current research guidance for T0–T6. Add only meaningful primary topic labels. |
| Dates | Current technical guidance has no invented due dates, effort estimates, iterations or artificial deadlines. | Source access dates and actual mutation/readback timestamps are evidence, not delivery promises. Leave scheduling fields absent unless real commitments exist. |
| Completion | Partial PR uses `Refs`; full acceptance and handoffs are required before `Closes`. A merged partial contribution does not imply Done. | Leave all future research packages open/Backlog; schema and taxonomy scaffold completion never upgrades product records or closes the research program. |

The live native child collection of [research #47](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/47) was read on the inspection date and contains twelve workstream children (#48–59). [Apple program #1](https://github.com/Pick-Your-AI/pick-your-ai-apple/issues/1) has eighteen native epic children (#2–19). These confirm the organization uses actual parent relations, rather than body-only issue lists. They are examples to adapt, not authority to duplicate their scope or move their issues.

## Evidence states are distinct

The [research method](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/RESEARCH_METHOD.md), [submission workflow](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/RESEARCH_WORKFLOW.md), [shared prompt rules](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/prompts/SHARED.md), and [#41 source policy](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/T0-configuration/catalog-data-sources.md) govern claim-level evidence.

| Term | Required meaning |
| --- | --- |
| Candidate | Discovery lead; no factual capability conclusion. |
| Source checked | Claim was checked against the cited primary source on its recorded access date. This is not independently verified behavior. |
| Primary documentation | Publisher documentation of the fact it controls, with exact claim scope. One source can also contain vendor performance claims of a different evidence grade. |
| Vendor claim | Publisher capability/performance statement not independently reproduced. |
| Independent measurement | Reproducible measurement with pinned inputs, method, conditions and limits. |
| Estimate | Derived result with method and assumptions; never silently a measured value. |
| Reviewed research | An actual reviewer accepted a specific contribution/scope. Merging a proposal does not establish publication rights or permanent freshness. |
| Verified | Eligible independent corroboration or reproduction linked to the specific claim. A vendor page read is insufficient. |
| Publication eligible | The intended field/source/use combination has the necessary reviewed permission, notices, evidence and consumer gates. This is separate from source checking, review and verification. |

Preserve the market [feature matrix](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/49) states: **Exercised**, **Documented**, **Unsupported**, **Unknown**. Exercised is limited to the actual test; Documented may be an unverified vendor claim; Unsupported requires explicit negative evidence; silence remains Unknown. Do not equate Unknown with false, unsupported, zero price or absent functionality. Do not equate human review with independent measurement.

Application claims must bind product identity, feature, release/channel, plan/edition, account or entitlement conditions, platform, geography, language and observation date where relevant. Pricing additionally needs currency, billing interval, minimums, usage meters, included quotas, overages, taxes/discount conditions and effective dates. No universal price, legal suitability, certification, safety or performance conclusion follows from a marketing page.

## Source-use and publication gates

[The publication eligibility handoff](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/PUBLICATION_ELIGIBILITY_HANDOFF.md) establishes no blanket publication grant for complete existing proposals. Its precise source-by-use restrictions remain in force; an application-directory expansion supplies no automatic new source-use permission.

1. Admit the entity as an explicit research candidate with provenance and unresolved questions. Do not invent facts to make a complete record.
2. Capture claim-level source URL, publisher, actual access date/status, exact scope, evidence class and limitations. Failed source access remains failed.
3. Record distinct intended-use decisions for retrieval, research, display, caching, export and redistribution. Assess text, metadata, prices, logos, screenshots, benchmarks and user reviews separately; a software code license does not grant every asset or scraped compilation.
4. Normalize and review claims without changing their evidence grade. Preserve conflict history, aliases and retired offers rather than overwriting earlier truth.
5. Form a bounded field-level publication projection containing only eligible fields. Mixed-source records cannot inherit the most permissive source's grant. Unknown permission cannot become a grant; maintain withheld fields and reason codes.
6. Require an actual receiving decision on the projection/contract before claiming consumption. Keep approved research, eligible artifact, released artifact and website presentation separate.
7. On withdrawal, changed terms, correction or retirement, invalidate affected projection/version, preserve history and coordinate downstream correction. No scheduled crawler or third-party integration is enabled merely by creating the backlog.

The current source policy does **not** prescribe a universal TTL. Version-pinned facts retain their exact revision and are rechecked when corrected or the selected version changes. Current-state prices, availability, quotas, regions and terms display an actual “as of” date. Applications maintenance cadence may be proposed with rationale, but must not be represented as an already accepted #41 requirement.

## Canonical boundaries and handoffs

| Concern | Existing source of truth | Applications responsibility |
| --- | --- | --- |
| Frozen component kinds and compatibility | [#40 / CONTRACT_MAPPING](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/CONTRACT_MAPPING.md) | Propose a separately versioned application metadata contract. Do not append `application` to frozen v1 or edit its generators/tests. Supply a mapping proposal if an accepted integration needs one. |
| Model/provider/context identity | [T1 summary](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/T1-model-selection/README.md) | Cross-link a product's disclosed underlying model/provider only when actually sourced. Product name, operator, model family and serving route are distinct. Do not infer undisclosed models. |
| Framework/tool/integration/MCP/memory | [T4 summary](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/T4-agents-integrations/README.md) | Research end-user products; reuse T4 component references. A product and its integration package are separate related identities, not automatic duplicates. Listing an MCP integration implies neither security nor an app's whole-product capability. |
| Competitors and commercial validation | [Market method](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/docs/market-research/research-methodology.md), #47–#66 | Reuse existing entity/source evidence with provenance. Preserve #47's NARROW empirical product-validation decision alongside this broader directory corpus. Do not duplicate customer recruitment or willingness-to-pay studies. |
| Rights and freshness | #41, accepted #60 source decisions | Record application-specific evidence/use proposals and request scoped receiving review. Do not reopen or replace their accepted policy decisions. |
| Pricing and cost | #39 | Provide app-plan rates and units with exact conditions; request receiving review for any shared price semantics. Do not disguise unsupported meters as a supported builder unit. |
| Evaluation methodology | #36, #61/#62 for their existing empirical scopes | Define app-task experiments and comparative conditions; avoid duplicating model/runtime benchmark calibration. No live rank until evidence is comparable and publication eligible. |
| Ingestion/publication operations | Dedicated catalog-pipeline mission if created | Supply application contracts and source policies; do not build a competing ingestion service in this research repo. Confirm the actual receiving repository and issue before hardcoding them as delivered. |
| Website/mobile implementation | Website Project #3 and existing Apple/Android projects | Supply research and consumer requirements; record actual receiving acceptance. Search UI, rendering, deployment and client implementation remain in their owning repositories. |

## Proposed Project configuration

This is a proposal for the new Applications Project. The current technical vocabulary below was read from research CONTRIBUTING/SHARED, **not retrieved as today's live Project field IDs**. The market `project-configuration.json` was inspected as a repository snapshot; it is not proof of the present live board.

| Field | Proposed options | Reason |
| --- | --- | --- |
| Status | Backlog; Ready; In Progress; In Review; Blocked; Done | Reuse technical research semantics. Backlog does not imply work has started. |
| Priority | Critical; High; Medium; Low | Reuse technical sequencing language. Record rationale per item. |
| Workstream | Application domain and foundation epic IDs | Applications are outside T0–T6; do not repurpose their Tier field. |
| Work Type | Program; Epic; Research; Specification; Dataset; Validation; Decision | Distinguish hierarchy/output while native parent fields preserve actual relations. |
| Research Confidence | Unverified; Low; Medium; High | New planning items start Unverified; this is not a product rating. |
| Readiness | Ready; Needs input; Blocked; Awaiting decision | Actual inputs/decision must support state. An unassigned item is Backlog until accountable ownership is settled. |
| Dependency Status | Unblocked; Waiting; Blocked | Only genuine prerequisites justify native blocked-by edges. Informational cross-links remain separate. |

Use built-in Assignees, Labels, Parent issue and Sub-issues progress. Add no duplicate Owner/Status labels, dates, iterations or invented estimates. Refresh live field IDs before mutation. Useful views: all work; domain coverage; foundations; ready research; evidence review; publication handoffs; blocked/decision work. A view is not delivered until its actual filters/grouping are read back.

## Licensing and reviewer routing inspection

The research repository's [LICENSE](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/LICENSE), blob `68047eb6cfc0dce6c9cdfcf79583c6a36e6807f7`, is MIT with copyright 2026 Pick Your AI contributors. The organization and sustainability repository root inventories contain no LICENSE at this inspection. Sustainability [CONTRIBUTING](https://github.com/Pick-Your-AI/pick-your-ai-sustainability/blob/main/CONTRIBUTING.md) explicitly routes license/IP stewardship questions to its E01.07 work. Its missing license is not permission to copy that corpus.

For new original application research scaffolding and code, matching the research repository's MIT license is a reasonable project choice. Add a separate rights/third-party notice: the repository license does not grant rights in externally cited documentation, prices, logos, screenshots, reviews, benchmark data, vendor trademarks or third-party compilations. Source-by-use decisions remain necessary. Do not copy or relicense external material merely to populate the new public repository.

The research [.github/CODEOWNERS](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/.github/CODEOWNERS), blob `e874ca7a987be72dd3ff2f767828ca770f0ebbcb`, uses individual handles with default `@CompleteDotTech`; its tier and market-specific rules name historical path reviewers. It contains **no team slugs**. The `.github` and sustainability repositories' `.github/` directories contain workflows only and the attempted CODEOWNERS paths returned 404. Therefore no authoritative `Research Lead Maintainers` team slug is established from these files. Read actual organization team identity before writing team handles or repository grants; do not derive a slug from its display name. A valid CODEOWNERS entry also requires appropriate repository access and does not itself enforce review.

## Acceptance and validation to carry into repository

Validate taxonomy IDs/parentage, record schemas, unique keys/IDs, candidate versus approved paths, source/claim references, actual calendar dates, explicit unknowns, evidence/publication prerequisites, identity alias conflicts, hierarchy acyclicity, coverage counters, and consumer projection eligibility. Fixture examples must be visibly synthetic and outside real proposal data.

Validation is offline unless explicitly stated. It does not establish source truth, permission, freshness, legal conclusions, availability, security certification, benchmark reproducibility or personal approval. Tests should exercise failure cases such as a documented claim marked Verified without evidence, an Unknown claim turned false, mixed-source rights laundering, duplicate entities, orphan native children and publication of a withheld field.

The foundation backlog accompanying this note names future deliverables and central receiving decisions without pretending they already exist. The taxonomy and machine-readable plan can be structurally complete while every product research entry remains unverified. No repository seed should claim verified product capabilities unless actual research and eligible independent evidence has been completed.
