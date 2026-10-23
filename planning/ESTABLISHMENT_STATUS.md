# Establishment status

Observed October 23, 2026. **The repository and native backlog are live; the foundation is submitted for review, not merged. Full establishment remains incomplete.**

## Actual resources

- [Public repository](https://github.com/Pick-Your-AI/pick-your-ai-applications), with `main` still at the initial README commit `a30d8579b9228dc692bf47fd0404443ad363a2c0` during the completed import.
- [Program issue #1](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/1): 135 open planned issues, comprising one program, 14 epics, 72 work packages and 48 independently reviewable tasks.
- All 134 internal native parent relationships were read back against the authored plan. Small steps remain 192 checklist task groups and 768 subtasks, not additional issues.
- [Foundation PR #136](https://github.com/Pick-Your-AI/pick-your-ai-applications/pull/136), from `contrib/CompleteDotTech/applications-foundation` to `main`. No non-author approval or merge is claimed.
- [Organization Project #10](https://github.com/orgs/Pick-Your-AI/projects/10), created public in the prior setup session with this repository as its default. Seven research fields and seven saved views were configured. Item population and field values are not verified complete.

## Reproducible execution evidence

[Import run 39901787188](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39901787188) completed successfully. It reconciled all issue titles, bodies, type labels and internal native parents without duplicating records or replacing existing parents. It verified the source bundle and regenerated scaffold hashes before writing the contributor branch.

The immutable run [artifact 12479710416](https://github.com/Pick-Your-AI/pick-your-ai-applications/actions/runs/39901787188/artifacts/12479710416) includes the final execution receipt and confirms that `main` remained unchanged. Its ZIP SHA-256 is `bb1624f01d396abd3aba917f3acedff6e4fac45665ceaddde6c0d30674f7fa39`. Artifacts have retention limits; the committed [issue/relationship receipt](GITHUB_ESTABLISHMENT_RECEIPT.json) preserves the canonical IDs and mapping.

Receipt commit: `a45877b5a905a50e2c2c6730a2a6b5d5e3b05bb2`. The receipt's `validation_workflow` field records the bootstrap's scope boundary, not the current absence of a workflow: `.github/workflows/validate.yml` was separately committed using the authenticated connector. Python 3.12 CI at `7832b15cc6792ea5d207f999ec2f2402a9565c8a` passed. The PR checks must pass again on its final head before merge.

The first import created the records and parent relationships but failed its final index check because the marker parser omitted dots used in work-package/task IDs. The corrected, serialized run recognized all 135 stable IDs, reused the records and passed final readback. The failed first run is not counted as a successful verification.

Local and CI validation:

```sh
python scripts/validate_applications.py
python scripts/validate_planning.py
python -m unittest discover -s tests -v
```

Both validators and all 60 tests passed. Application and price schemas also passed JSON Schema meta-validation. These checks establish structure and specified invariants, not source truth, rights, independent product reproduction or current remote state indefinitely.

## Exact remaining setup gates

| Gate | Observed state | Canonical tracking |
| --- | --- | --- |
| Project item/field reconciliation | All 135 item placements and 945 intended initial values remain to be reconciled against Project #10. Do not overwrite later human triage. | Program #1; `docs/PROVISIONING.md` |
| Cross-repository native parent | Program #1 links research #509 in its body but has not been attached as its native child. | Program #1; research #509 |
| Team-based access and policy enforcement | No team grant was performed. The repository rulesets endpoint, including parent rulesets, returned an empty list. Enforcement is not claimed from the presence of CONTRIBUTING/CODEOWNERS. | [APP-F01.02 / #65](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/65) |
| Independent review and merge | PR #136 remains open. A qualified non-author must approve after the final push, with required checks and organization boundaries satisfied. | PR #136 |
| Default-branch verification | Full scaffold validation on `main` must follow an authorized reviewed merge. | PR #136 |

The active connector does not expose organization Project mutations, native cross-repository parent mutations or repository-access/ruleset configuration. Its browser connection is unavailable for completing those UI operations. The repository-scoped import deliberately does not obtain broader credentials, change access or bypass approval requirements. An already-authorized connection with the required capabilities is needed for those remaining operations.

## Research is a separate delivery stage

The taxonomy has eight domains, 48 categories, 288 subcategories and 15 facets. These are a declared research scope, not a claim of an exhaustive product census. There are zero real application or pricing records and no verified product capabilities or publication-approved records.

`planning/backlog.json` remains the immutable authored plan with `prepared_not_provisioned` metadata. Actual GitHub IDs are in `GITHUB_ESTABLISHMENT_RECEIPT.json`; live issue assignees and Project triage remain authoritative. Neither a successful import nor a scaffold merge closes the research program or parent research #509.
