# Admission and publication policy

Version 1.1 (proposed) · Refs #67 (tasks #94, #95) · Method: [RESEARCH_METHOD.md](RESEARCH_METHOD.md) · Contract: [APPLICATION_CONTRACT.md](APPLICATION_CONTRACT.md)

Which evidence changes allow a claim or record to move forward, back, or out. Every transition names the evidence it needs and who is accountable. Nothing advances automatically: merging a PR or passing tests changes no state.

## Claim states (task #94)

| From → to | Required evidence | Accountable |
| --- | --- | --- |
| candidate → **source checked** | A primary source read on a real, recorded date, scoped to the exact subject and conditions | Researcher |
| source checked → **reviewed** (`review.status: approved`) | A named reviewer other than the claim's researcher checks the claim against the cited source at the exact revision, with a dated decision receipt; affiliations disclosed (REVIEW_POLICY) | Reviewer |
| reviewed → **independently verified** (`verification_status: verified`, receipt in `verification`) | An independent verifier with a pinned reproducible protocol and receipt, or an independent second source | Verifier |
| reviewed → **publication eligible** | An allowed, unexpired source-use decision for every cited source, covering the claim's exact field path **and** each intended use (display, cache, export, api, commercial), with a reviewer and receipt; every cited source `state: active`; `evidence_state: active`; `value_status` `known` or `unsupported`; no unresolved conflict for the same subject, field, version and scope | Reviewer + rights decision |
| eligible → **published** | A release receipt **and** a consuming owner's acceptance receipt (OWNERSHIP_HANDOFFS) | Release owner + consumer |

Independent verification is **not** required for eligibility. A reviewed, rights-cleared `vendor_claim` may be shown, provided its grade is displayed with it. Verification is a stronger label, not a gate.

## Paths out and back (task #95)

| Event | Transition | What happens |
| --- | --- | --- |
| Reviewer rejects | → `review.status: rejected` | The claim stays in history with the reason; the record returns to notes for that field |
| Sources conflict | → `value_status: disputed` | Both positions and their evidence stay visible; the claim cannot be admitted until a reviewer resolves it |
| Source withdrawn or corrected | → `evidence_state: withdrawn` or `superseded` | The field leaves every projection at the next release; a withdrawal event goes to consumers; re-review starts |
| Rights withdrawn or expired | Field ineligible for the affected uses | Removed from those projections at the next release; other uses keep their own decisions |
| Change signal (new version, changed terms, reported error) | → `evidence_state: recheck_required` | The claim leaves `publication.fields` and is not admitted again until rechecked and re-reviewed; an already released artifact keeps its dated value until the next release. If the signal shows the claim is wrong, it is withdrawn |
| Product discontinued | Lifecycle claim recorded; identity **retired**, never deleted | History, aliases and successors stay; the record leaves active listings |
| Undisclosed material affiliation found | Affected claims → re-review | Reviewed again by an unaffiliated reviewer |

Withdrawal retains the historical claim, original source/check dates, prior review
and rights decisions, and links to the superseding decision with its reason and
reviewed revision. Removing a field from a current projection does not erase its
evidence history or establish that a replacement is accepted.

## Independence of the three tracks

| Track | Changes when | Does not imply |
| --- | --- | --- |
| Research completion | A decision record meets its issue's acceptance criteria and its receiving decisions are recorded | That anything is published |
| Issue state | A maintainer closes the issue after the above | That records are eligible |
| Publication eligibility | Per claim, by the rules above | That research is complete, or that the issue is closed |

## Parent closure (task #95)

A program, epic or work-package parent closes only when its own acceptance
criteria and the following conditions are met:

1. Each in-scope native child outcome is accepted against its criteria at an
   exact reviewed revision, or has an explicit, reviewed scope disposition with
   rationale and evidence (for example, a duplicate linked to the accepted
   canonical outcome, or work removed from the agreed parent scope). A blocked,
   deferred, rejected or unresolved child is never counted as completed. If its
   required outcome remains in scope, the parent stays open. Preserve native
   relationships and the original evidence; do not delete history to clear a gate.
2. The existing parent decision record contains a synthesis of the resulting
   outcome, preserved invariants, limitations and unresolved questions. It links
   the accepted child revisions, scope dispositions and their actual review
   decisions. A non-author reviewer assesses the exact parent revision; a merged
   partial PR or a green check does not supply that acceptance. No new ledger or
   separate synthesis artifact is required.
3. Any affected receiving decisions required by the parent's scope are recorded
   with the actual reviewer, reviewed revision, scope and retained conditions,
   following [OWNERSHIP_HANDOFFS.md](OWNERSHIP_HANDOFFS.md). Missing required
   decisions remain pending and keep the parent open. For internal-only work with
   no affected consumer, state that and why; an informational cross-link creates
   no external acceptance gate.

Issue closure, product verification and publication eligibility remain separate
outcomes. A parent synthesis records only the evidence actually obtained and
retains unknowns; it never upgrades a child or a product claim by aggregation.

## Record states (contract `publication.state`)

`notes` → `proposed` → `eligible` → `published`, where a record is only as eligible as the claims its manifest admits. Claims that stop being admissible leave the manifest; a record with no admissible claim left (for example, all withdrawn, superseded, rejected or awaiting recheck) must return to `notes` or `proposed`, because an eligible or published record cannot have an empty manifest. Retirement is a lifecycle fact on the identity, not a publication state.

## APP-F01.04 acceptance synthesis

Recorded 2026-11-17 for #67, at `main` `89e663afad0e112e060402a21e8cdaa5591e22ac`. This is the parent synthesis that "Parent closure" (condition 2) requires. It records only evidence that exists on GitHub.

**Accepted children.** Both native children are closed with acceptance receipts:

- [#94](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/94), claim states and evidence transitions. Delivered by PR #144 (merge `cc3a79e`). Its exact head `5de9bd7e68b4bd3999f7052bb7342b4e9c23c209` has a [non-author approval](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/144#pullrequestreview-5777753393). [Closure receipt](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/94#issuecomment-6960099855).
- [#95](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/95), acceptance, withdrawal and parent closure. Delivered by PR #161 (merge `1713315`). Its exact head `7851bbcac0fbe361bc9cba71c5578dfb6b89a95d` has a [non-author approval](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/161#pullrequestreview-5946062757). [Closure receipt](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/95#issuecomment-6960224052).

No child was deferred, rejected or removed from scope.

**Outcome against #67's acceptance criteria:**

| Criterion | Where it is met |
| --- | --- |
| Each state transition has required evidence and accountable review | "Claim states" and "Paths out and back" above. Every forward, backward and exit transition names its evidence and who is accountable. Nothing advances on a merge or a passing check |
| Unknown cannot become false/zero by default | [RESEARCH_METHOD.md](RESEARCH_METHOD.md), "Unknown never becomes false or zero" and "Feature-matrix states". An absent or failed check is Unknown, and `unsupported` needs checked, explicit negative evidence |
| Research completion, issue state and publication eligibility are independent | "Independence of the three tracks" above |
| Factual conclusions are scoped or explicitly unknown, with real dates | RESEARCH_METHOD "Every claim is scoped" and "Freshness"; "candidate → source checked" requires a real, recorded check date |
| Required receiving decisions are linked or remain pending | None is required (see below) |

**Receiving decisions.** This package's only handoff, `H05` (research #41), is an `information` entry with an empty `required_for` in [planning/handoffs.json](../planning/handoffs.json). The research #60 link in #67 is information-only as well. The method changes no interface that another repository consumes, so no receiving decision is required. A later change that does alter a consumed interface needs its own decision under [OWNERSHIP_HANDOFFS.md](OWNERSHIP_HANDOFFS.md).

**Limits.**
- This method is used locally. It has not been adopted by research #41 or any consumer.
- No real application record has been admitted, reviewed, verified or published under these states; the ledger is still empty.
- Passing validators and tests show structure only. They are not source truth, independent reproduction, source-use rights or consumer acceptance.

#67 can close once a non-author reviews this synthesis at its exact revision and it merges. Closing #67 does not close epic #10 or accept any external handoff.
