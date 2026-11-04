<!-- plan-id: APP-F06.02.T02 -->
# Validate eligible projection behavior

## User decision

Offline admission checks and negative fixtures

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Offline admission checks and negative fixtures

### Excluded / existing owners

- Frozen builder contract changes
- Website or pipeline runtime implementation
- Unsupported product or publication claims

## Deliverables

- `docs/PUBLICATION_GATES.md`
- `schemas/publication-decision.schema.json`
- `scripts/validate_publication.py`

## Research questions

- Which fields can enter each public release and how are permissions enforced?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Small subtasks

- [ ] APP-F06.02.T02.S01: Reject a field with missing rights or missing attribution.
- [ ] APP-F06.02.T02.S02: Reject changed/withdrawn evidence from a current projection and preserve the audit reason.

## Dependencies and receiving handoffs

Planning parent: `APP-F06.02`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **acceptance_gate** — `APP-F03.01`: Final projection acceptance requires actual source-use decisions. Native blocker: no.
- **information** — `APP-F06.01`: Output contract must carry rights and revision metadata. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#41`: Evidence/source policy remains central. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#60`: No blanket grant is implied. Native blocker: no.

## Acceptance criteria

- [ ] The named output is committed with scope, actual evidence references and retained unknowns.
- [ ] A reviewer assesses the exact revision; structural validation is reported separately from factual acceptance.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Sequencing judgment for the research plan; not a product score.

Readiness rationale: Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
