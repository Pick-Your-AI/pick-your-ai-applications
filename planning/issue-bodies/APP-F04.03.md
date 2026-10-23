<!-- plan-id: APP-F04.03 -->
# Define freshness, retirement and corrections

## User decision

What changes trigger renewed review or downstream withdrawal?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Track source changes, stale current-state facts, plan changes, acquisitions, shutdowns and rights withdrawals.
- Separate immutable release facts from current product state.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `docs/MAINTENANCE.md`
- `schemas/change-event.schema.json`
- `templates/correction.md`

## Research questions

- Track source changes, stale current-state facts, plan changes, acquisitions, shutdowns and rights withdrawals.
- Separate immutable release facts from current product state.

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F04`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#41`: Version-pinned facts and dated current-state policy are canonical. Native blocker: no.
- **information** — `APP-F06.02`: Publication projection must support withdrawal. Native blocker: no.

## Acceptance criteria

- [ ] Records retain actual last-check and effective dates.
- [ ] No unsupported universal TTL is imposed as existing policy.
- [ ] Corrections propagate to linked projections and preserve revision history.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
