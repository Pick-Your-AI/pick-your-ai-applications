<!-- plan-id: APP-C11 -->
# Software testing, review and quality assurance

## User decision

Products that assist software verification, review, debugging and quality workflows.

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Include an identifiable software product, independently discoverable product module, or software-delivered service that offers an AI-assisted end-user workflow within this definition; record the evidence for AI involvement.

### Excluded / existing owners

- Evaluation datasets and benchmark suites are linked to their existing owners.
- Passing generated tests does not demonstrate correctness or security.

## Deliverables

- `research/categories/software-quality.md`
- `research/candidates/software-quality.json`
- `coverage/ledger.json`

## Research questions

- Which distinct products or independently identifiable modules document a material AI-assisted software testing, review and quality assurance workflow, and which discovered entities fail the inclusion rule?
- Which offerings, versions, languages, regions and access conditions qualify the evidence for test targets and execution environment, reproduction and failure artifacts, review and false-positive controls?
- What user choices are changed by ci and repository integrations, data and dependency exposure, and what remains Unknown or disputed?
- Which claims are primary documentation, vendor claims, independent measurements or estimates; what separate source-use and receiving-owner decisions are still missing?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

Category comparison fields:

- Test targets and execution environment
- Reproduction and failure artifacts
- Review and false-positive controls
- CI and repository integrations
- Data and dependency exposure

Research territories (not verified capabilities):

- APP-C11.01: Test generation and maintenance
- APP-C11.02: Autonomous UI/API testing
- APP-C11.03: Code review
- APP-C11.04: Bug reproduction and debugging
- APP-C11.05: Software quality and coverage analysis
- APP-C11.06: Application security testing assistance

## Tasks and small subtasks

- [ ] APP-C11.T01: Define the survey and permitted source plan
  - [ ] APP-C11.T01.S01: Write inclusion/exclusion decisions for Test generation and maintenance, Autonomous UI/API testing, Code review and the remaining subcategories.
  - [ ] APP-C11.T01.S02: Declare source families, languages, regions, cutoff and discovery stop/expansion rule.
  - [ ] APP-C11.T01.S03: Inspect source/material/use rights and record permitted retrieval or unresolved decisions before acquisition.
- [ ] APP-C11.T02: Discover and reconcile product identities
  - [ ] APP-C11.T02.S01: Collect permitted candidate leads with primary identity links and retain failed/gated reads.
  - [ ] APP-C11.T02.S02: Separate product, suite/module, offering/plan, release, operator, model and integration identities; resolve aliases and acquisitions without deleting history.
  - [ ] APP-C11.T02.S03: Cross-link existing T1/T4 and market records with original evidence dates and review status; do not mass-import their claims.
- [ ] APP-C11.T03: Build the evidence-backed comparison
  - [ ] APP-C11.T03.S01: Investigate Test targets and execution environment; Reproduction and failure artifacts; Review and false-positive controls.
  - [ ] APP-C11.T03.S02: Investigate CI and repository integrations; Data and dependency exposure.
  - [ ] APP-C11.T03.S03: Map each claim to dated evidence, applicable offering/version/conditions and grade; retain Unknown, contradiction and unperformed-test states.
  - [ ] APP-C11.T03.S04: Record pricing units/conditions and claim-specific rights, privacy, security and accessibility gaps; do not infer unsupported functionality.
- [ ] APP-C11.T04: Review, reconcile coverage and hand off
  - [ ] APP-C11.T04.S01: Run structural/reference checks and an independent claim/source review against the exact submitted revision.
  - [ ] APP-C11.T04.S02: Update category/subcategory coverage with distinct identities, evidence depth, rights state and explicit remaining gaps.
  - [ ] APP-C11.T04.S03: Prepare the scoped export/website/pipeline receiving packet with versioned artifact IDs and consumer requirements.
  - [ ] APP-C11.T04.S04: Record actual review and receiving decisions; keep unchecked tasks and unresolved research open until their own criteria are met.

## Dependencies and receiving handoffs

Planning parent: `APP-D02`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.


## Acceptance criteria

- [ ] A decision record at research/categories/software-quality.md defines its bounded source/language/region survey and accounts for all six named subcategories, including explicit unexamined gaps.
- [ ] Candidate identities are deduplicated into product, module, offering, version and operator relationships; excluded/component entities retain a linked routing reason.
- [ ] All comparison fields have scoped evidence or explicit Unknown; every factual claim records primary source, access date, evidence grade, version/offering and relevant conditions.
- [ ] Terms, privacy/security, accessibility and pricing findings remain claim-specific and dated; vendor documentation is never labeled independently verified without eligible corroboration or reproduction.
- [ ] The category ledger reports actual distinct-product counts, known unknowns and next actions against its declared denominator; it does not claim global exhaustiveness.
- [ ] Independent review and material source/contract/consumer handoffs are recorded at the reviewed revision; acceptance concerns bounded research, with publication eligibility and website delivery kept separate.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Expand domain breadth after the shared identity/evidence method is usable; independent discovery can start sooner.

Readiness rationale: Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
