# APP-F01 synthesis: governance, scope and review

Epic: #10 · Work packages: #64, #65 (closed), #66, #67 · Child tasks: #88–#95 (#88 and #90–#95 closed; #89 open) · Status: foundations merged on `main`; parent syntheses and the two APP-F01.01 receiving decisions are still pending · Observed: 2026-11-17T21:00Z at `main` [`89e663a`](https://github.com/Pick-Your-AI/pick-your-ai-applications/commit/89e663afad0e112e060402a21e8cdaa5591e22ac)

History: first recorded 2026-10-31 (#145). An earlier revision of this refresh read `main` at `d4a185c`, before #156–#161 and #163 merged. The tables below replace that snapshot. They report GitHub issue and PR state as read back at the observation time. An acceptance comment is cited only as a comment; it is not treated as issue closure.

## What has landed vs what remains open

| Package / issue | Decision / artifact | State at `89e663a` |
| --- | --- | --- |
| F01.01 scope (#64 open; #88 closed, #89 open) | Four-part inclusion test; 15-case boundary table; audience and form vocabularies; explicit compatibility with research #47 NARROW | Merged via #141 (`e57808b`) and #146 (`83c8f6f`, head `63d8ada`): [docs/SCOPE.md](../../docs/SCOPE.md), [application-scope.md](application-scope.md). #88 closed 2026-11-17 with an acceptance receipt. #89 and #64 stay open: they need the H01 and H14 receiving decisions and a disposition for boundary questions U1–U4 |
| F01.02 ownership (#65 closed; #90, #91 closed) | Repository-to-concern matrix with T1/T4 crosswalk; eleven-field receiving receipt; 20-entry handoff ledger (`H01–H20`) | Merged via #142 (`aea4188`) and #147 (`c360bb4`, head `905bce0`): [docs/OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md), [planning/handoffs.json](../../planning/handoffs.json). #161 (`1713315`) then merged its closed-issue wording as a local proposal. That change records no consumer acceptance |
| F01.03 review (#66 open; #92, #93 closed) | Review matrix by change type; no silent evidence upgrades; disagreements visible; affiliation disclosure by kind; sponsorship separation | Merged via #143 (`294930e`), #148 (`6c3d397`, head `1e4cc4d`) and #161's local policy adoption (`1713315`): [docs/REVIEW_POLICY.md](../../docs/REVIEW_POLICY.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), [templates/research-note.md](../../templates/research-note.md). #66 stays open until its parent synthesis is reviewed and merged. A proposed patch is in [#154](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/154#issuecomment-6960728398) but has not been published as a PR. Contributor routing in #139 is still in review |
| F01.04 states (#67 open; #94, #95 closed) | Claim transitions with required evidence and accountability; rejection, dispute, withdrawal, recheck and retirement paths; three independent tracks; parent-closure gates | Merged via #144 (`cc3a79e`, head `5de9bd7`) and #161 (`1713315`, head `7851bbc`): [docs/RESEARCH_METHOD.md](../../docs/RESEARCH_METHOD.md), [docs/ADMISSION_POLICY.md](../../docs/ADMISSION_POLICY.md). #94 closed 20:29Z and #95 closed 20:34Z, each with an acceptance receipt. #67 stays open until its parent synthesis is reviewed at an exact revision |

All four work packages keep unknowns explicit and keep model, component, runtime and dataset ownership with their existing research owners.

## Pending gates at the observation time

| Item | Owner / tracking | State |
| --- | --- | --- |
| Required `validate` check on `main` | Merged PR #136 (`65f8666`, 2026-11-04) | Live. `.github/workflows/validate.yml` runs on pushes and PRs. Ruleset `25725543` enforces `validate`, non-author approval of the latest push, and an extra approval for unattributed commits. `validate` passed on `89e663a` |
| APP-F01.01 receiving decisions: `H01` (research #509, G12 scope) and `H14` (research #47, NARROW compatibility) | The receiving research owners, recorded under [OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md) | **Pending.** These are the only `acceptance_gate` entries with APP-F01 in `required_for`. Producer documents are on `main` at `63d8ada`. No reviewer, decision URL or date is recorded |
| `H09` (catalog-pipeline #1) and `H10` (website #15) | APP-F06.01 / APP-F06.03 | **Pending**, but they gate F06 export and directory delivery, not APP-F01 |
| The 16 other entries (`H02–H08`, `H11–H13`, `H15–H20`) | Information links | **Pending.** Information links create no acceptance gate for any F01 parent ([ADMISSION_POLICY.md](../../docs/ADMISSION_POLICY.md), "Parent closure") |
| #66 and #67 parent receiving decisions | Not applicable | Neither parent changes an interface that another repository consumes. REVIEW_POLICY records "None required", and H05 (#67's handoff) is information-only. Each parent still needs its own reviewed synthesis |
| Boundary questions U1–U4 | Domain owners named in [application-scope.md](application-scope.md) | Open |
| Contributor routing (#139) | Non-author reviewers | Open. The 2026-11-05 CHANGES_REQUESTED review targets an earlier head (`67ad07d`). Current head `245ef98` has one approval and still needs that reviewer's re-review |

## Acceptance (epic #10)

- **Work packages meet their criteria and independent review:** partly met. #65 and child tasks #88 and #90–#95 are closed with acceptance receipts. #64 and #89 wait on H01/H14. #66 and #67 each wait on a reviewed parent synthesis.
- **Versioned decisions keep unknowns and ownership boundaries:** met across the merged foundation documents.
- **Final receiving gates evidenced without claiming deployment:** pending. No consumer acceptance is recorded for any of `H01–H20`. Merged local proposals (#161) and passing checks are not receiving receipts.

Keep `#10`, `#64`, `#66`, `#67` and `#89` open until the required reviews and receiving decisions are recorded.
