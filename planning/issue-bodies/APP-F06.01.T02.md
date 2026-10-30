<!-- plan-id: APP-F06.01.T02 -->
# Build contract fixtures

## User decision

Valid/invalid synthetic consumer fixtures

**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.

## Scope

### Included

- Valid/invalid synthetic consumer fixtures

### Excluded / existing owners

- Frozen builder contract changes
- Website or pipeline runtime implementation
- Unsupported product or publication claims

## Deliverables

- `contracts/applications/v0/README.md`
- `schemas/application-export.schema.json`
- `docs/CONSUMER_CONTRACT.md`

## Research questions

- What stable application artifact should the shared pipeline and website consume?

## Evidence and comparison rules

Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly.

## Small subtasks

- [ ] APP-F06.01.T02.S01: Exercise unknown prices, withdrawn claims and renamed products.
- [ ] APP-F06.01.T02.S02: Check consumer handling of unsupported schema revisions and missing evidence.

## Dependencies and receiving handoffs

Planning parent: `APP-F06.01`. Use the native parent relationship after provisioning.

Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.

- **information** — `Pick-Your-AI/pick-your-ai-research#40`: Shared adoption needs affected-owner/version review. Native blocker: no.
- **information** — `APP-F02.04`: Claim and evidence identities are foundational inputs. Native blocker: no.

## Acceptance criteria

- [ ] The named output is committed with scope, actual evidence references and retained unknowns.
- [ ] A reviewer assesses the exact revision; structural validation is reported separately from factual acceptance.

## Ownership and triage

Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.

Priority rationale: Sequencing judgment for the research plan; not a product score.

Readiness rationale: Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.

Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.
