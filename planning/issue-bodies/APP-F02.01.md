<!-- plan-id: APP-F02.01 -->
# Define canonical application and organization identity

## User decision

Which records are the same product and which are related editions or services?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Separate vendor, operator, product family, concrete product, edition/plan, release/channel and distribution.
- Represent aliases, renames, mergers, spinouts, retired names and hosted versus open-source editions.
- Review the initial schemas/application.schema.json definitions and embedded source/claim model; any extraction into separate schemas remains a proposed versioned change, not an implemented prerequisite.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `research/foundations/application-identity.md`
- `schemas/application-identity.schema.json`
- `schemas/application.schema.json`

## Research questions

- Separate vendor, operator, product family, concrete product, edition/plan, release/channel and distribution.
- Represent aliases, renames, mergers, spinouts, retired names and hosted versus open-source editions.

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F02`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#5`: Provider/operator identity is reusable context. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#6`: Do not confuse an application with a model release. Native blocker: no.

## Acceptance criteria

- [ ] Identity rules prevent same-name collisions and preserve historical identifiers.
- [ ] Canonical IDs survive renames; merge/split rules retain redirects and evidence.
- [ ] Third-party app/store IDs are scoped aliases rather than sole canonical identity.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
