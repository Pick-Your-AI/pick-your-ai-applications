<!-- plan-id: APP-F03.04 -->
# Research privacy, security and provenance disclosures

## User decision

What trust information does the supplier actually document for a specific product/plan?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Cover training-data use, prompts/outputs retention, deletion, subprocessors, region, encryption, access and incident disclosures.
- Distinguish certification reports, marketing assertions, implemented controls and actual tested behavior.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `research/foundations/trust-evidence.md`
- `templates/trust-assessment.md`

## Research questions

- Cover training-data use, prompts/outputs retention, deletion, subprocessors, region, encryption, access and incident disclosures.
- Distinguish certification reports, marketing assertions, implemented controls and actual tested behavior.
- What does the supplier state about input/output ownership, commercial use, confidentiality and reuse restrictions for each product/plan/date?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F03`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#35`: Existing guardrail research is context, not an app-specific certification. Native blocker: no.
- **information** — `Pick-Your-AI/pick-your-ai-research#41`: Public source and rights requirements still apply. Native blocker: no.

## Acceptance criteria

- [ ] Trust claims bind product/plan and dated documentary scope.
- [ ] No absence of an incident or named certification becomes proof of safety/compliance.
- [ ] Sensitive security findings and private customer information stay outside public research.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.
- [ ] Input/output ownership and commercial-use claims remain attributed supplier statements; independent legal conclusions are not implied.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
