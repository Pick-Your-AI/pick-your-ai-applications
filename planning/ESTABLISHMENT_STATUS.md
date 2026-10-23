# Establishment status

Observed October 23, 2026. **The repository and native backlog are live. Foundation PR #136 is a draft, not merged; full establishment remains incomplete.**

## Actual resources

- [Public repository](https://github.com/Pick-Your-AI/pick-your-ai-applications). The latest default-branch readback remains the initial README commit `a30d8579b9228dc692bf47fd0404443ad363a2c0`, not the complete scaffold.
- [Program issue #1](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/1): the completed import established 135 planned issues, comprising one program, 14 epics, 72 work packages and 48 independently reviewable tasks.
- All 134 internal native parent relationships were read back against the authored plan by that import. Small steps remain 192 checklist task groups and 768 subtasks, not additional issues. The review-hardening patch changes neither the authored backlog nor these live issues.
- [Foundation PR #136](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/136), from `contrib/CompleteDotTech/applications-foundation` to `main`. It is deliberately a draft while setup gates and non-author review remain outstanding.
- [Organization Project #10](https://github.com/orgs/Pick-Your-AI/projects/10), created public in the prior browser session with this repository as its default. Seven research fields and seven saved views were configured. The current session cannot read or control that browser; issue placement and field population are not claimed complete.

## Original establishment evidence

[Import run 39901787188](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39901787188) successfully reconciled all 135 authored issue identities, bodies, labels and 134 internal native parents without duplicate issues or parent replacement. The committed [issue/relationship receipt](GITHUB_ESTABLISHMENT_RECEIPT.json) preserves the actual IDs.

The original [artifact 12479710416](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39901787188/artifacts/12479710416) has ZIP SHA-256 `bb1624f01d396abd3aba917f3acedff6e4fac45665ceaddde6c0d30674f7fa39`. Artifact retention is limited. Receipt commit: `a45877b5a905a50e2c2c6730a2a6b5d5e3b05bb2`.

The first import created the records and parent relationships but failed its final index check because its marker parser omitted dots in work-package/task IDs. The corrected serialized run reused those records and passed readback. The historical receipt's `validation_workflow` field describes that bootstrap's boundary; the validation workflow was separately committed and has run successfully. These historical observations are not an indefinitely current remote inventory.

## Review hardening completed in the contributor branch

Commit `5fea2fec1a701b29c38edd6307076526c65566f7` implements fixes for 13 reported validation/provisioning defects. The earlier stale-status finding was already corrected. The eight-file patch adds 42 regression tests, taking the suite from 60 to **102 tests**; both metadata and planning validators pass. No real application/pricing records, authored issues, taxonomy counts, assignees, permissions or default-branch content were changed by that patch.

Covered invariants include offering resolution; normalized independent-review identities; duplicate JSON keys and non-finite numbers; duplicate price observations; independent-measurement evidence; review dates; explicit unsupported values; relationship target types; name/alias collision decisions; bounded coverage percentages and scoped acceptance receipts; public-host syntax; and protection against regeneration after external-checkpoint provisioning.

See [validation hardening](../docs/VALIDATION_HARDENING.md), [regression tests](../tests/test_review_regressions.py), and the [hardening receipt](REVIEW_HARDENING_RECEIPT.json). The new regression suite fails against the original code and passes with the patch. The scoped [preparation run 39926501046](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39926501046) applied a hash-pinned patch to the exact original head, checked all eight output blob hashes, passed both validators and 102 tests, and created commit objects without moving refs. Its [artifact 12489717205](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39926501046/artifacts/12489717205) has ZIP SHA-256 `3ec2835189f8f671bc7da3630d3d8ef3f4fb5a836f8fde62cfda454007555931`.

The authenticated connector subsequently fast-forwarded only the foundation contributor branch with an expected-head check. [PR CI 39926733943](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39926733943) passed on the exact hardening commit. Further receipt/documentation commits must also pass final-head CI before merge.

```sh
python scripts/validate_applications.py
python scripts/validate_planning.py
python -m unittest discover -s tests -v
```

Structural checks do not authenticate sources, authors, review receipts, rights, independent measurements or actual website publication. Valid metadata is not proof of the represented event. No independent approval is inferred from automated review comments or these tests.

## Exact remaining setup gates

| Gate | Observed state | Canonical tracking |
| --- | --- | --- |
| Project reconciliation | All 135 placements and 945 intended initial values remain to be reconciled against Project #10. Preserve later human triage. | Program #1; `docs/PROVISIONING.md` |
| External native parent | Program #1 still has no native parent. A single repository-scoped attachment attempt returned HTTP 403; no replacement, credential expansion or permission change was attempted. | Program #1; research #509 |
| Team access and policy enforcement | No team grants were performed. Latest repository ruleset readback, including parents, remains an empty list. Policy files alone do not enforce review or branch restrictions. | [APP-F01.03 / #66](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/66) |
| Independent review and merge | PR #136 is a draft. BunsDev's review request remains outstanding; there is no qualifying non-author approval. Final-head approval and organization policy gates are required. | PR #136 |
| Default-branch verification | Full scaffold validation on `main` follows an authorized reviewed merge. | PR #136 |

The parent-link attempt is preserved in research [run 39927009375](https://github.com/Pick-Your-AI/pick-your-ai-research/actions/runs/39927009375), with result timestamp `2026-10-23T08:46:19.587980+00:00` and artifact `12489727021`. The subsequent applications parent endpoint still returned `No parent issue found`. The attempt only permitted the native attachment of applications #1 beneath research #509 with `replace_parent: false`; it did not edit issue text, assignments or acceptance criteria.

The active connector lacks Project, cross-repository-parent and repository-settings mutation operations. The connected-browser attempt returned that it requires the originating browser context. Completing the remaining UI operations requires the already-authorized connected browser in Work mode or an equivalent authorized capability. GitHub repository authentication itself is working; repeated reauthentication does not supply a missing browser capability. Do not expand credentials or bypass review to force completion.

## Research remains a separate stage

The taxonomy defines eight domains, 48 categories, 288 subcategories and 15 facets. These describe planned research scope, not an exhaustive product census. There are zero real application/pricing records and no verified product capabilities or publication-approved records.

`planning/backlog.json` remains the immutable authored snapshot with `prepared_not_provisioned` metadata; actual IDs live in `GITHUB_ESTABLISHMENT_RECEIPT.json`. Live assignees and Project triage remain authoritative. Successful setup or a scaffold merge does not close the applications research program or research #509.
