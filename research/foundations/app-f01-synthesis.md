# APP-F01 synthesis: governance, scope and review

Epic: #10 · Work packages: #64, #65 (closed), #66, #67 · Child tasks: #88–#95 · Status: partial foundations merged on `main`, pending independent/receiving acceptance · Refreshed: 2026-11-17 (initially recorded 2026-10-31)

## What has landed vs what remains open

| Package / issue | Decision / artifact | Current state on `main` (`19f6cf2`) and open PRs |
| --- | --- | --- |
| F01.01 scope (#64; tasks #88, #89) | Four-part inclusion test; 15-case boundary table; audience and form vocabularies; explicit compatibility with research #47 NARROW | Merged via #141 and #146 (`63d8ada`): [docs/SCOPE.md](../../docs/SCOPE.md), [application-scope.md](application-scope.md). Keep `#64`, `#88`, `#89` open pending U1–U4 boundary decisions and `H01`/`H14` receiving acceptance |
| F01.02 ownership (#65 closed; tasks #90, #91) | Repository-to-concern matrix with T1/T4 crosswalk; ten-field receiving receipt; 20-entry pending handoff ledger (`H01–H20`) | Merged via #142 and #147 (`c360bb4`): [docs/OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md), [planning/handoffs.json](../../planning/handoffs.json). PR #161 proposes clarifying closed-issue receiving eligibility on `handoffs.json` / `OWNERSHIP_HANDOFFS.md`; `#90` and `#91` remain open |
| F01.03 review (#66; tasks #92, #93) | Review matrix by change type; no silent evidence upgrades; disagreements visible; affiliation disclosure by kind; sponsorship separation | Merged via #143 and #148 (`6c3d397`): [docs/REVIEW_POLICY.md](../../docs/REVIEW_POLICY.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), [templates/research-note.md](../../templates/research-note.md). Open PR #139 connects entrypoints to central `.github` escalation routing; PR #161 proposes scoped adoption wording; `#66`, `#92`, `#93` remain open |
| F01.04 states (#67; tasks #94, #95) | Claim transitions with required evidence and accountability; rejection, dispute, withdrawal, recheck and retirement paths; three independent tracks | Merged via #144 (`cc3a79e`): [docs/RESEARCH_METHOD.md](../../docs/RESEARCH_METHOD.md), [docs/ADMISSION_POLICY.md](../../docs/ADMISSION_POLICY.md). PR #161 proposes explicit task #95 parent-closure gates; `#67`, `#94`, `#95` remain open |

All four work packages keep unknowns explicit and keep model, component, runtime and dataset ownership with their existing research owners.

## Current status of pending gates (2026-11-17)

| Item | Owner / tracking | State (as of 2026-11-17) |
| --- | --- | --- |
| Required `validate` check on `main` | Merged PR #136 (`65f8666`, 2026-11-04) | **Live on `main`.** `.github/workflows/validate.yml` runs on push and PRs; ruleset `25725543` actively enforces `validate`, non-author latest-push approval, and extra approval on unattributed commits |
| Independent review of each merged/open package at its exact revision | Non-author application research reviewers (`REVIEW_POLICY.md`) | Partial: #141–#149 and #151 merged; open PRs #139, #152, #153, #155–#163 await required non-author approvals / maintainer disposition before any package closure |
| Receiving decisions `H01–H20` (`planning/handoffs.json`) | Owners listed in [OWNERSHIP_HANDOFFS.md](../../docs/OWNERSHIP_HANDOFFS.md) | **All 20 (`H01–H20`) pending.** Live readback on 2026-11-17 confirms `H01`/`H14` producer docs (`docs/SCOPE.md`, `application-scope.md`) are already present on `main` (`63d8ada`), `research#4`, `#26`, `#36`, `#39`, `#40`, `#41`, `#60` remain `closed` (requiring venue/owner confirmation before recording decisions), and `research#47`, `#61`, `#62`, `#509`, `website#15`/`#24`, `catalog-pipeline#1`, `datasets#1`, `papers#1`, `apple#1`, `android#1` remain `open` with zero recorded acceptance URLs |
| Open policy/handoff follow-ups (#139, #161) | Maintainers & non-author reviewers | Pending review/merge (`#161` modifies `handoffs.json` explanation strings cleanly without claiming consumer acceptance; commit-pinning `H01`/`H14` in `handoffs.json` can follow without merge conflict) |
| Boundary questions U1–U4 | Domain owners named in [application-scope.md](application-scope.md) | open |

## Acceptance (epic #10)

- **Work packages meet their criteria and independent review:** #65 is closed; #64, #66, #67 and child tasks #88–#95 stay open pending remaining reviews, #95/escalation reconciliation, and required receiving receipts.
- **Versioned decisions keep unknowns and ownership boundaries:** met across the merged foundation documents.
- **Final receiving gates evidenced without claiming deployment:** pending; zero consumer acceptance receipts (`H01–H20`) are recorded.

Keep `#10`, `#64`, `#66`, `#67`, and `#88–#95` open until required reviews and receiving decisions are recorded.
