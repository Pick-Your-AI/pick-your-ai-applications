<!-- plan-id: APP-F05.01.T01 -->
# Specify evaluation identities

## User decision

An application workflow protocol

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- An application workflow protocol

### Excluded / existing owners

- Frozen builder contract changes
- Website or pipeline runtime implementation
- Unsupported product or publication claims

## Deliverables

- `docs/EVALUATION_METHOD.md`
- `schemas/evaluation-run.schema.json`
- `templates/evaluation-protocol.md`

## Research questions

- What constitutes an observed app capability under specific conditions?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Small subtasks

- [ ] APP-F05.01.T01.S01: Record account entitlement and variable service/model behavior.
- [ ] APP-F05.01.T01.S02: Define reproducible input and observed success measures without customer data.

## Dependencies and receiving handoffs

Planning parent: `APP-F05.01`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#36`: Central evaluation methodology informs comparability. Native blocker: no.
- **information** — `APP-F03.01`: Testing and evidence reuse must be permitted. Native blocker: no.

## Acceptance criteria

- [ ] The named output is committed with scope, actual evidence references and retained unknowns.
- [ ] A reviewer assesses the exact revision; structural validation is reported separately from factual acceptance.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Sequencing judgment for the research plan; not a product score.

Readiness rationale: Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
