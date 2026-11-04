<!-- plan-id: APP-F06.01 -->
# Define versioned application export contract

## User decision

What stable application artifact should the shared pipeline and website consume?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Define stable entity/claim/source/offer IDs, schema version, release identity and cross-references.
- Specify unknowns, evidence labels, field rights, corrections, removals and backward compatibility.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `contracts/applications/v0/README.md`
- `schemas/application-export.schema.json`
- `docs/CONSUMER_CONTRACT.md`

## Research questions

- Define stable entity/claim/source/offer IDs, schema version, release identity and cross-references.
- Specify unknowns, evidence labels, field rights, corrections, removals and backward compatibility.

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F06`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#40`: Shared adoption needs affected-owner/version review. Native blocker: no.
- **information** — `APP-F02.04`: Claim and evidence identities are foundational inputs. Native blocker: no.

## Acceptance criteria

- [ ] Export semantics do not mutate frozen component v1.
- [ ] Synthetic examples are isolated and rejected from production exports.
- [ ] Actual pipeline/website reviewers receive a concrete proposed interface and pending decisions remain explicit.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
