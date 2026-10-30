<!-- plan-id: APP-F01.02 -->
# Define source ownership and receiving interfaces

## User decision

Where should each application fact and implementation responsibility live?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Map research, datasets, papers, catalog pipeline, website and mobile responsibilities.
- Define exact artifact/revision/field and review-receipt requirements for cross-repo handoffs.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `docs/OWNERSHIP_HANDOFFS.md`
- `planning/handoffs.json`

## Research questions

- Map research, datasets, papers, catalog pipeline, website and mobile responsibilities.
- Define exact artifact/revision/field and review-receipt requirements for cross-repo handoffs.

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F01`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#40`: Shared component contract authority remains central. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#41`: Reuse evidence/freshness policy. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#26`: Reuse tool and integration component semantics. Native blocker: no.

## Acceptance criteria

- [ ] Every interface names a producing artifact and receiving responsibility without duplicating implementation.
- [ ] Information links and native prerequisites are separate.
- [ ] Absent owners are not represented as having approved anything.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
