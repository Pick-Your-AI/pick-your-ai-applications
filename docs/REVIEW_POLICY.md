# Review and conflict policy

Version 1.0 (proposed) · Refs #66 (tasks #92, #93) · Organization rules: [.github CONTRIBUTING](https://github.com/Pick-Your-AI/.github/blob/main/CONTRIBUTING.md)

Reviews keep the directory truthful and commercially neutral. A review checks the evidence, not the reputation of the contributor or the product.

## Who reviews what

| Change | Required review | Notes |
| --- | --- | --- |
| Research note (incomplete) | One non-author reviewer | Checks that unknowns stay unknown and sources are real and dated |
| Structured record or price (proposal) | One non-author **application research reviewer** | Checks every claim against its cited source on the stated date |
| Decision record or policy change | One non-author reviewer **plus** each affected receiving owner | Receiving owners are listed in `planning/handoffs.json` |
| Contract, schema or taxonomy change | As above, plus research #40 when shared use is affected | Frozen research `contracts/v1` is never changed here |
| Synthetic test fixtures | One non-author reviewer | Fixtures stay in `tests/fixtures/` and never count as research |

All of these follow the organization rule: one approval from someone other than the author, re-approval after any later push, and a merge by a maintainer.

## Evidence integrity

- **No silent upgrades.** A vendor statement stays `vendor_claim`, a reading of documentation stays `checked`/`unverified`, and only an independent reproduction or second source makes a claim `verified`. A reviewer may downgrade a grade, but may not upgrade one without the evidence the contract requires.
- **Review the exact revision.** Approvals name the commit reviewed. A later push needs a new review.
- **Disagreement stays visible.** When reviewers or sources disagree, record both positions, the evidence for each and who holds them. The claim stays `disputed` until resolved. Disagreements are never closed by deleting a side.
- **Structural checks are not acceptance.** Passing validators and tests is reported separately from factual review.

## Disclosure and conflicts of interest

Contributors and reviewers disclose **material affiliations** with any product or vendor in the change: employment, contracting, investment, sponsorship, a referral or affiliate arrangement, or a direct competitor relationship. Disclose the *kind* of relationship only. Personal data, contract terms and amounts are never required or recorded.

| Situation | Rule |
| --- | --- |
| Contributor is affiliated with the product | Allowed. The PR states the affiliation, and the record is reviewed by someone without one. |
| Reviewer is affiliated with the product or a direct competitor | The reviewer recuses; another non-author reviews. |
| A vendor submits or corrects its own record | Treated as a `vendor_claim` source. It is reviewed like any other evidence and never admitted as independent verification. |
| Sponsored or paid placement is offered | Declined for research records. Sponsorship never affects inclusion, field values or ordering. |
| A correction request disputes an admitted claim | Reviewed under the same rules; the original claim and the correction both stay in history until a reviewer decides. |

Undisclosed material affiliations found later trigger a re-review of the affected records.

## Enforcement status

Read back on 2026-10-31 from `GET /repos/Pick-Your-AI/pick-your-ai-applications/rulesets`. The empty result recorded on #66 was observed before these rulesets were created on 2026-10-23.

| Enforced by a repository ruleset | Not enforced (policy only) |
| --- | --- |
| On the default branch: one approving review; approval of the latest push by someone other than its pusher; the required `validate` check; no deletion or force-push. This ruleset has no bypass actors. | Review by each affected receiving owner, for decision records and policy changes |
| Contributor branches limited to `contrib/**` and `dependabot/**`, with tags and other branches restricted. Organization admins and the maintain and admin repository roles can bypass this. | Affiliation disclosure and recusal, the evidence-grade rules, and research #40 review of shared-contract changes |
| | Code-owner approval: CODEOWNERS routes reviews, but no ruleset requires it |

The `validate` check comes from `.github/workflows/validate.yml`, which #136 adds. Until #136 merges, a pull request based on `main` cannot produce it. Rulesets enforce who may merge and that the structure validates. Whether a review actually checked the evidence still depends on the reviewer following this policy.
