# Admission and publication policy

Version 1.0 (proposed) · Refs #67 (tasks #94, #95) · Method: [RESEARCH_METHOD.md](RESEARCH_METHOD.md) · Contract: [APPLICATION_CONTRACT.md](APPLICATION_CONTRACT.md)

Which evidence changes allow a claim or record to move forward, back, or out. Every transition names the evidence it needs and who is accountable. Nothing advances automatically: merging a PR or passing tests changes no state.

## Claim states (task #94)

| From → to | Required evidence | Accountable |
| --- | --- | --- |
| candidate → **source checked** | A primary source read on a real, recorded date, scoped to the exact subject and conditions | Researcher |
| source checked → **reviewed** (`review: approved`) | A named non-author reviewer checks the claim against the cited source at the exact revision; affiliations disclosed (REVIEW_POLICY) | Reviewer |
| reviewed → **independently verified** (`verification: verified`) | An independent verifier with a pinned reproducible protocol and receipt, or an independent second source | Verifier |
| reviewed → **publication eligible** | An allowed source-use decision for every cited source **for the intended use** (display, cache, export, api, commercial), with a reviewer and receipt; `evidence_state: active`; no unresolved conflict for the same subject, field and scope | Reviewer + rights decision |
| eligible → **published** | A release receipt **and** a consuming owner's acceptance receipt (OWNERSHIP_HANDOFFS) | Release owner + consumer |

Independent verification is **not** required for eligibility. A reviewed, rights-cleared `vendor_claim` may be shown, provided its grade is displayed with it. Verification is a stronger label, not a gate.

## Paths out and back (task #95)

| Event | Transition | What happens |
| --- | --- | --- |
| Reviewer rejects | → `review: rejected` | The claim stays in history with the reason; the record returns to notes for that field |
| Sources conflict | → `value_status: disputed` | Both positions and their evidence stay visible; the claim cannot be admitted until a reviewer resolves it |
| Source withdrawn or corrected | → `evidence_state: withdrawn` or `superseded` | The field leaves every projection at the next release; a withdrawal event goes to consumers; re-review starts |
| Rights withdrawn or expired | Field ineligible for the affected uses | Removed from those projections at the next release; other uses keep their own decisions |
| Change signal (new version, changed terms, reported error) | → `evidence_state: recheck_required` | The claim stays displayed with its date until rechecked, unless the signal shows it is wrong (then withdrawn) |
| Product discontinued | Lifecycle claim recorded; identity **retired**, never deleted | History, aliases and successors stay; the record leaves active listings |
| Undisclosed material affiliation found | Affected claims → re-review | Reviewed again by an unaffiliated reviewer |

## Independence of the three tracks

| Track | Changes when | Does not imply |
| --- | --- | --- |
| Research completion | A decision record meets its issue's acceptance criteria and its receiving decisions are recorded | That anything is published |
| Issue state | A maintainer closes the issue after the above | That records are eligible |
| Publication eligibility | Per claim, by the rules above | That research is complete, or that the issue is closed |

## Record states (contract `publication.state`)

`notes` → `proposed` → `eligible` → `published`, where a record is only as eligible as the claims its manifest admits. A record can return to `notes` if all its admitted claims are withdrawn or rejected. Retirement is a lifecycle fact on the identity, not a publication state.
