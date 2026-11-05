# Review and conflict policy

Version 1.1 (proposed) · Refs #66 (tasks #92, #93) · Organization rules: [.github CONTRIBUTING](https://github.com/Pick-Your-AI/.github/blob/main/CONTRIBUTING.md)

Reviews keep the directory truthful and commercially neutral. A review checks the evidence, not the reputation of the contributor or the product.

## Who reviews what

| Change | Required review | Notes |
| --- | --- | --- |
| Research note (incomplete) | One non-author reviewer | Checks that unknowns stay unknown and sources are real and dated |
| Structured record or price (proposal) | One non-author **application research reviewer** | Checks every claim against its cited source on the stated date |
| Decision record or policy change | One non-author reviewer **plus** each affected receiving owner | Receiving owners are listed in `docs/HANDOFFS.md` until APP-F01.02 delivers `planning/handoffs.json`. A change that affects no receiving owner says so, with the reason |
| Contract, schema or taxonomy change | As above, plus research #40 when shared use is affected | Frozen research `contracts/v1` is never changed here |
| Validators, tests, `.github/workflows/`, CODEOWNERS or rulesets | One non-author maintainer | The required `validate` check runs the files such a change edits, so a passing check proves nothing about the change itself. The reviewer reads the changed checks |
| Synthetic test fixtures | One non-author reviewer | Fixtures stay in `tests/fixtures/` and never count as research |

All of these follow the organization rule:
- one approval from someone other than the author;
- approval of the latest push by someone other than its pusher;
- a merge by a maintainer.

**Application research reviewer (proposed).** This is a non-author who has read the contract and this policy, discloses as below, and either belongs to this repository's maintainer or lead team or is named on the PR by a maintainer. CODEOWNERS routes every path to one login (`.github/CODEOWNERS`); that routes requests, and it neither grants nor proves the role.

## Issues, branches and assignment

- **Issue headings.** Planned work keeps its plan ID heading (`[APP-…]`, from `planning/backlog.json`). New research uses the `[Research]` template and corrections use the `[Correction]` template (`.github/ISSUE_TEMPLATE/`).
- **Branches.** Contributors push to `contrib/<login>/<topic>`, and only to their own branches (organization policy).
- **Assignment.** Live assignees decide who owns an issue.
  - A contributor claims an issue by saying so on it. They self-assign if they can, or a maintainer assigns them.
  - Nobody is assigned without agreeing.
  - An assignee who stops says so on the issue and unassigns.
  - Assigning someone records ownership. It is never evidence that anything was reviewed.

## Evidence integrity

- **No silent upgrades.**
  - A vendor statement stays `vendor_claim`, and a reading of documentation stays `checked` with `verification_status: unverified`.
  - A claim becomes `verified` only as the contract requires: an independent verifier plus either a pinned, reproducible test protocol and its receipt, or an explicitly cited second source with `authority: independent`.
  - Any change to `source_status`, `verification_status` or `evidence_grade` is a correction recorded with its rationale.
- **Review the exact revision.** Approvals name the commit reviewed. A later push needs a new review.
- **Disagreement stays visible.**
  - When reviewers or sources disagree, record both positions, the evidence for each and who holds them.
  - Conflicting sources for the same normalized scope make the claim `disputed`, with the positions kept in its notes. A reviewer disagreement leaves the review `pending`.
  - Disagreements are never closed by deleting a side.
  - Conflict records, including what must be normalized before a conflict is declared, belong to APP-F03.02.T02.
- **Corrections keep the value.** A correction request never nulls or unpublishes a claim by itself.
  - The claim stays `evidence_state: active` until a reviewer triages the request.
  - A request the reviewer finds plausible moves the claim to `recheck_required`. Publication pauses and the value is kept until the recheck decides.
  - A request the reviewer does not accept is closed with its reason, and the claim stays active.
  - The correction lifecycle itself belongs to APP-F04.03.T02, and the re-review paths to APP-F01.04.
- **Structural checks are not acceptance.** Passing validators and tests is reported separately from factual review.

## Disclosure and conflicts of interest

Contributors and reviewers disclose **material affiliations** with any product or vendor in the change:
- employment or contracting;
- investment or sponsorship;
- a referral or affiliate arrangement;
- a direct competitor relationship.

A disclosure names the kind of relationship and the affected record or product IDs from the change, which are already public. Personal data, contract terms and amounts are never required or recorded. Someone who would rather not name the affected records recuses from the whole change instead.

| Situation | Rule |
| --- | --- |
| Contributor is affiliated with a product in the change | Allowed. The PR names the affiliation's kind and the affected IDs, and someone without an affiliation reviews those records. |
| Reviewer is affiliated with a product in the change, or with a direct competitor | The reviewer recuses from the affected records, or from the whole change if they don't name them; another non-author reviews. |
| A vendor submits or corrects its own record | The submission is not itself a source or a verification. Each claim cites public sources and is graded per claim like any other contribution, and it never counts as independent verification. |
| Sponsored or paid placement is offered | Declined for research records. Sponsorship never affects inclusion, field values or ordering. |
| A correction request disputes an admitted claim | Reviewed under the same rules, as "Corrections keep the value" says. The original claim and the correction both stay in history. |
| A model helped write or review the change | The PR or review says so. When the change concerns products of that model's vendor, it names the vendor, and a reviewer who did not use that vendor's models reviews the affected records. |

Contributors and reviewers state their affiliations, or that they have none, in the PR description or in their own review. Undisclosed material affiliations found later trigger a re-review of the affected records, which the disclosure's IDs identify.

## Enforcement status

Read back on 2026-11-03 by a repository admin, so the bypass actors are visible:
- `GET /repos/Pick-Your-AI/pick-your-ai-applications/rulesets` for the list;
- `GET /repos/Pick-Your-AI/pick-your-ai-applications/rulesets/{id}` for each ruleset's rules and bypass actors;
- the GraphQL `bypassActors` field for the role names.

The empty result recorded on #66 was observed before these rulesets were created on 2026-10-23.

| Ruleset (ID, last updated) | Applies to | Enforces | Bypass |
| --- | --- | --- | --- |
| Review required: default branch (25725543, 2026-10-23T09:33:04-04:00) | `main` | One approving review; approval of the most recent push by someone other than its pusher; the required `validate` check (GitHub Actions); no deletion and no force-push. Stale approvals are not dismissed on push, so the latest-push rule is what makes a later push need a new approval. Code-owner review is not required | **None.** The organization's documented pattern lets organization admins bypass this ruleset; here nobody can |
| Contributor boundary: default branch (25725675, 2026-10-23T09:34:44-04:00) | `main` | Only bypass actors can update it, so merges are made by them | Organization admins and the maintain and admin repository roles |
| Contributor boundary: branches (25725679, 2026-10-23T09:34:45-04:00) | Every branch except `main`, `contrib/**` and `dependabot/**` | No creation, update, deletion or force-push | Organization admins and the maintain and admin repository roles |
| Contributor boundary: tags (25725680, 2026-10-23T09:34:46-04:00) | Every tag | No creation, update or deletion | Organization admins and the maintain and admin repository roles |

**Checked structurally.** The required `validate` check enforces part of the evidence-grade rules:
- `verified` needs checked provenance and an independent verification receipt: a pinned protocol for a reproduced test, or a cited independent source for a second-source check;
- a displayed grade equals the claim's grade;
- a `disputed` claim carries no value and stays out of eligible manifests.

**Policy only, not enforced:**
- whether a grade truthfully reflects its source;
- review by each affected receiving owner;
- affiliation disclosure and recusal;
- the application research reviewer role;
- research #40 review of shared-contract changes;
- code-owner approval.

The `validate` check comes from `.github/workflows/validate.yml`, which #136 adds. Until #136 merges, a pull request based on `main` cannot produce it. Rulesets enforce who may merge and that the structure validates. Whether a review actually checked the evidence still depends on the reviewer following this policy.

## Receiving owners for this policy

None required. This policy governs review inside this repository and changes no interface that another repository consumes. #66's only dependency is information-only (`planning/foundation-backlog.json`). A later change that alters a handoff routes through the decision-record row above.
