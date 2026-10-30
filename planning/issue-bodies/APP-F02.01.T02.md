<!-- plan-id: APP-F02.01.T02 -->
# Validate identity invariants

## User decision

Schema and fixtures for identity changes

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Schema and fixtures for identity changes

### Excluded / existing owners

- Frozen builder contract changes
- Website or pipeline runtime implementation
- Unsupported product or publication claims

## Deliverables

- `research/foundations/application-identity.md`
- `schemas/application-identity.schema.json`
- `schemas/application.schema.json`

## Research questions

- Which records are the same product and which are related editions or services?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Small subtasks

- [ ] APP-F02.01.T02.S01: Reject duplicate canonical IDs and inconsistent aliases.
- [ ] APP-F02.01.T02.S02: Exercise merge/split and unknown operator cases without manufacturing real data.

## Dependencies and receiving handoffs

Planning parent: `APP-F02.01`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#5`: Provider/operator identity is reusable context. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#6`: Do not confuse an application with a model release. Native blocker: no.

## Acceptance criteria

- [ ] The named output is committed with scope, actual evidence references and retained unknowns.
- [ ] A reviewer assesses the exact revision; structural validation is reported separately from factual acceptance.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Sequencing judgment for the research plan; not a product score.

Readiness rationale: Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
