# APP-F01 synthesis: governance, scope and review

Epic: #10 · Work packages: #64, #65 (closed), #66, #67 · Child tasks: #88–#95 (#88, #90–#94 closed 2026-11-17; #89, #95 open) · Status: partial foundations merged on `main`, pending remaining child/parent and receiving acceptance · Refreshed: 2026-11-17 (initially recorded 2026-10-31)

## What has landed vs what remains open

| Package / issue | Decision / artifact | Current state on `main` (`d4a185c`) and open PRs |
| --- | --- | --- |
| F01.01 scope (#64; tasks #88 closed, #89 open) | Four-part inclusion test; 15-case boundary table; audience and form vocabularies; explicit compatibility with research #47 NARROW | Merged via #141 and #146 (`63d8ada`): [docs/SCOPE.md](../../docs/SCOPE.md), [application-scope.md](application-scope.md). Task `#88` closed 2026-11-17; keep `#64` and `#89` open pending U1–U4 boundary decisions and `H01`/`H14` receiving acceptance |
| F01.02 ownership (#65 closed; tasks #90, #91 closed) | Repository-to-concern matrix with T1/T4 crosswalk; ten-field receiving receipt; 20-entry pending handoff ledger (`H01–H20`) | Merged via #142 and #147 (`c360bb4`): [docs/OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md), [planning/handoffs.json](../../planning/handoffs.json). Tasks `#90` and `#91` closed 2026-11-17; approved PR #161 updates closed-issue receiving eligibility wording without claiming consumer acceptance |
| F01.03 review (#66; tasks #92, #93 closed) | Review matrix by change type; no silent evidence upgrades; disagreements visible; affiliation disclosure by kind; sponsorship separation | Merged via #143 and #148 (`6c3d397`): [docs/REVIEW_POLICY.md](../../docs/REVIEW_POLICY.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), [templates/research-note.md](../../templates/research-note.md). Tasks `#92` and `#93` closed 2026-11-17; open PR #139 connects escalation routing (`PossumXI` approved, awaiting `@zwright8` re-review), and approved PR #161 scopes policy adoption |
| F01.04 states (#67; task #94 closed, #95 open) | Claim transitions with required evidence and accountability; rejection, dispute, withdrawal, recheck and retirement paths; three independent tracks | Merged via #144 (`cc3a79e`): [docs/RESEARCH_METHOD.md](../../docs/RESEARCH_METHOD.md), [docs/ADMISSION_POLICY.md](../../docs/ADMISSION_POLICY.md). Task `#94` closed 2026-11-17; approved PR #161 specifies task #95 parent-closure gates (`#67` and `#95` stay open until merged/accepted) |

All four work packages keep unknowns explicit and keep model, component, runtime and dataset ownership with their existing research owners.

## Current status of pending gates (2026-11-17)

| Item | Owner / tracking | State (as of 2026-11-17) |
| --- | --- | --- |
| Required `validate` check on `main` | Merged PR #136 (`65f8666`, 2026-11-04) | **Live on `main`.** `.github/workflows/validate.yml` runs on push and PRs; ruleset `25725543` actively enforces `validate`, non-author latest-push approval, and extra approval on unattributed commits |
| Independent review of each merged/open package at its exact revision | Non-author application research reviewers (`REVIEW_POLICY.md`) | Partial: #141–#149, #151, and #155 (`d4a185c`, APP-F02.01) merged; approved PRs #156–#161 await merge coordination; #139, #152, #153, #162, #163, and #164 remain in review |
| Receiving decisions `H01–H20` (`planning/handoffs.json`) | Owners listed in [OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md) | **All 20 (`H01–H20`) pending.** Live readback on 2026-11-17 confirms `H01`/`H14` producer docs (`docs/SCOPE.md`, `application-scope.md`) are already present on `main` (`63d8ada`), `research#4`, `#26`, `#36`, `#39`, `#40`, `#41`, `#60` remain `closed` (requiring venue/owner confirmation before recording decisions), and `research#47`, `#61`, `#62`, `#509`, `website#15`/`#24`, `catalog-pipeline#1`, `datasets#1`, `papers#1`, `apple#1`, `android#1` remain `open` with zero recorded acceptance URLs |
| Open policy/handoff follow-ups (#139, #161) | Maintainers & non-author reviewers | Pending review/merge (`#161` modifies `handoffs.json` explanation strings cleanly without claiming consumer acceptance; commit-pinning `H01`/`H14` in `handoffs.json` can follow without merge conflict) |
| Boundary questions U1–U4 | Domain owners named in [application-scope.md](application-scope.md) | open |

## Acceptance (epic #10)

- **Work packages meet their criteria and independent review:** #65 and child tasks #88, #90, #91, #92, #93, #94 are closed; #10, #64, #66, #67, #89, and #95 stay open pending remaining reviews, #95/escalation reconciliation, and required receiving receipts.
- **Versioned decisions keep unknowns and ownership boundaries:** met across the merged foundation documents.
- **Final receiving gates evidenced without claiming deployment:** pending; zero consumer acceptance receipts (`H01–H20`) are recorded.

Keep `#10`, `#64`, `#66`, `#67`, `#89`, and `#95` open until required reviews and receiving decisions are recorded.
