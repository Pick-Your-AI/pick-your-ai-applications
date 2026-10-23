<!-- plan-id: APP-F02.03 -->
# Define product, plan, deployment and enterprise fields

## User decision

Which product facts are required for useful enterprise and end-user comparisons?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Specify platform, deployment/operator, installation, offline operation and enterprise plan facts.
- Scope SSO/SCIM/RBAC, administration, tenancy, retention, training use, export, data residence, support and SLA claims to documented plans.
- Review the initial schemas/application.schema.json definitions and embedded source/claim model; any extraction into separate schemas remains a proposed versioned change, not an implemented prerequisite.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `research/foundations/product-field-guide.md`
- `schemas/product-profile.schema.json`
- `schemas/application.schema.json`

## Research questions

- Specify platform, deployment/operator, installation, offline operation and enterprise plan facts.
- Scope SSO/SCIM/RBAC, administration, tenancy, retention, training use, export, data residence, support and SLA claims to documented plans.
- What export formats/completeness, migration/portability, account deletion versus retained backups, and customer-provided model/key entitlements are documented or actually exercised?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F02`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#3`: Existing operator/capacity vocabulary informs but does not automatically classify whole apps. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#35`: Reuse safety/guardrail boundary context. Native blocker: no.

## Acceptance criteria

- [ ] Every field has type, meaning, allowed unknown state and evidence scope.
- [ ] Hosted and self-operated offerings are represented without inferring model deployment mode.
- [ ] Security/compliance claims retain issuer, scope, dates and documentary limits.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.
- [ ] Portability, deletion and BYOK/BYOM claims identify product/plan/date and distinguish documented promises from exercised behavior.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
