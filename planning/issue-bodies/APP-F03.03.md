<!-- plan-id: APP-F03.03 -->
# Normalize application plans, prices and commercial restrictions

## User decision

What would a user pay for a specific app plan and what remains unknown?

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Separate subscription, seats, credits, metered consumption, outcome billing, trials, bundles and enterprise quotes.
- Record currency, billing interval, region, minimums, quotas, overages, add-ons, tax and promotional conditions.

### Excluded / existing owners

- Changing frozen research contracts/v1 or accepted research ownership
- Website/runtime implementation and unapproved source copying
- Claiming planned research or structural checks as independently verified product behavior

## Deliverables

- `research/foundations/application-pricing.md`
- `schemas/pricing.schema.json`
- `schemas/pricing-record.schema.json`

## Research questions

- Separate subscription, seats, credits, metered consumption, outcome billing, trials, bundles and enterprise quotes.
- Record currency, billing interval, region, minimums, quotas, overages, add-ons, tax and promotional conditions.
- What renewal, cancellation, refund, unused-credit and trial-to-paid conditions apply, and what model/API-key costs or vendor charges remain with BYOK/BYOM?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Native delivery hierarchy

2 independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes.

## Dependencies and receiving handoffs

Planning parent: `APP-F03`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#39`: Shared price semantics remain with the cost owner. Native blocker: no.
- **information** — `APP-F03.01`: Price-source publication rights require exact scope. Native blocker: no.

## Acceptance criteria

- [ ] A free trial is not represented as permanent free access.
- [ ] Unknown enterprise quotes and uncovered costs are not zero.
- [ ] Calculations show assumptions, effective dates and source scope; unsupported shared meters stay in app research.
- [ ] Every factual conclusion has scoped evidence or remains explicitly unknown; source access and review dates are real.
- [ ] Required receiving decisions are linked with actual reviewer, reviewed revision, scope and retained conditions; missing decisions remain pending.
- [ ] Rates and terms include renewal/cancellation/refunds, trial conversion and external-model costs or explicit Unknown, scoped by product/plan/region/date.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Foundation for truthful, reusable application research and downstream directory consumption.

Readiness rationale: Bounded planning and evidence-method work can start from the inspected organization standards; unassigned execution remains Backlog until ownership is accepted.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
