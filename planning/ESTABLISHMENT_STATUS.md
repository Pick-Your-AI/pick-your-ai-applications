# Establishment status

Observed October 23, 2026. **Repository, native backlog, Project population, external parent linkage and repository controls are verified. Foundation PR #136 remains draft and unmerged pending qualified non-author approval.**

## Verified setup

- Public repository: https://github.com/Pick-Your-AI/pick-your-ai-applications .
- Native backlog: 135 issues (one program, 14 epics, 72 work packages and 48 tasks), with 134 internal native parent relationships verified by the original import. Smaller work remains 192 checklist groups and 768 subtasks.
- Applications program #1 is now a native child of research #509. The browser readback of research #509 showed the applications program in its sub-issue collection. The earlier repository-scoped HTTP 403 attempt is historical, not the current state.
- Project #10 contains all 135 unique planned issue identities and 945 populated values across seven fields. A full browser DOM readback across all 15 workstreams found no mismatches in the 810 non-status values against the authored plan. Status is Backlog for 134 issues and In Progress for the program; the live program status was preserved.
- Type labels are preserved. Additive topic labels identify the 15 existing domains/foundations; Project fields remain authoritative for status, priority and readiness.
- Existing team grants were read back: Maintainers and Research have Triage, Research Lead Maintainers has Admin, and Research Maintainers has Write. No team membership or repository grants were changed in this continuation.
- Four active rulesets were read back: Review required: default branch (25725543), Contributor boundary: default branch (25725675), Contributor boundary: branches (25725679), and Contributor boundary: tags (25725680).
- Default-branch review requires one approval, approval of the latest reviewable push, the GitHub Actions `validate` check, deletion restrictions and blocked force pushes. The contributor branch boundary includes all branches and excludes the default branch, `contrib/**`, `contrib/**/*`, `dependabot/**` and `dependabot/**/*`; creations, updates, deletions and force pushes are restricted. The tag boundary restricts tag creation, updates and deletion.
- Branch/tag boundary bypasses observed on the existing rulesets are Organization admin, Maintain and Repository admin roles. Review/check enforcement is a separate ruleset; passing tests is not approval.

The full issue-number/field readback and settings identifiers are preserved in [PROJECT_RECONCILIATION_RECEIPT.json](PROJECT_RECONCILIATION_RECEIPT.json). This is a dated observation, not a perpetual live inventory. The authored `planning/backlog.json` remains immutable; live assignments and later triage remain authoritative.

## Validation and original evidence

The implementation head before these receipt-only updates was `efa552a1dd7cd39184e89eeafac28b2aed3cb14b`. Its PR validation run [39927482836](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39927482836) was read back as successful. The prior hardening work passed both validators and all 102 tests, including 42 added regression tests; see [REVIEW_HARDENING_RECEIPT.json](REVIEW_HARDENING_RECEIPT.json) and [validation hardening](../docs/VALIDATION_HARDENING.md). New documentation commits must pass final-head CI before merge.

The original [import run 39901787188](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39901787188) reconciled the issue definitions and internal native relationships. Its dated IDs are in [GITHUB_ESTABLISHMENT_RECEIPT.json](GITHUB_ESTABLISHMENT_RECEIPT.json); its old incomplete-setup fields describe that earlier checkpoint and are superseded by the new Project receipt.

```sh
python scripts/validate_applications.py
python scripts/validate_planning.py
python -m unittest discover -s tests -v
```

## Remaining acceptance gates

1. Qualified non-author approval of the final PR head, with approval of the latest push by someone other than its pusher. BunsDev's existing request is not an approval; the latest review readback still contained comments only.
2. Required validation passing on the final submitted head, followed by a reviewed merge.
3. Default-branch scaffold and CI readback after that merge. The complete scaffold is still on the contributor branch; no merge is claimed.

Do not bypass the organization review policy. Keep program #1 and research #509 open after a scaffold merge: their product-research and receiving-handoff outcomes remain future work.

## Research remains separate

The taxonomy covers eight domains, 48 categories, 288 subcategories and 15 facets. There are zero real application or pricing records. Setup completion, passing validation or a future scaffold merge does not establish verified product capabilities, publication rights, completed product research or website delivery.
