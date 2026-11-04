# Resume the GitHub bootstrap

`scripts/provision_github.py` provisions only `Pick-Your-AI/pick-your-ai-applications`, its dedicated organization Project, and the program's native parent relationship to research issue #509. It reads the prepared backlog, issue bodies and Project configuration without rewriting those authored artifacts.

## Current checkpoint: October 23, 2026

The repository, Project #10, all 135 planned issues and all 134 internal native parent relationships already exist. The foundation is in PR #136, not `main`. Do not restart from an assumption that these resources are absent. See [establishment status](../planning/ESTABLISHMENT_STATUS.md) and [the live mapping](../planning/GITHUB_ESTABLISHMENT_RECEIPT.json).

A separate repository-scoped Actions import completed the internal backlog. The later [October 23 establishment checkpoint](../planning/ESTABLISHMENT_STATUS.md) records Project population and fields, the native root-to-research-#509 edge, team access and review-policy readbacks. The general CLI helper below did not perform those later steps; its earlier gaps are historical, not a request to recreate resources. Use readback and conflict protections to reconcile current state. The reviewed merge and research acceptance remain separate gates.

The committed authored plan intentionally retains `prepared_not_provisioned` as its snapshot state. It is not the live resource inventory. The receipt provides the actual GitHub IDs; do not regenerate a competing plan or erase live triage.

Project discovery uses the recorded Project number or checkpoint ID before names. A rename of the recorded Project is reported without rewriting it; an inaccessible recorded Project fails closed and never authorizes creating a replacement. The prepared Project title remains historical input for a genuinely new bootstrap, not the identity of the established Project #10.

## Before executing

Use an authorized GitHub CLI session on Linux or macOS. Authentication remains owned by `gh`; this script never reads or prints a token. It creates no credentials, grants no access, changes no teams or rulesets, submits no reviews and merges no pull requests. Repository and Project creation require the corresponding existing account permissions. Do not broaden credentials or bypass organization rules to make a failed request pass.

Run the repository's normal validation first. The helper's default mode is an **offline dry run** and requires neither `gh` nor authentication:

```bash
python scripts/provision_github.py
```

The current plan resolves to 135 issues, 134 internal native parent relationships plus the program's external research #509 parent, four type labels, seven Project fields and 945 initial field values. Labels describe issue type; Status, Priority, Readiness and other Project semantics are not duplicated as labels.

To perform the already authorized resource creation:

```bash
python scripts/provision_github.py --apply
```

The script initializes a missing public repository with a README only, creates or reconciles the dedicated Project and its repository link, creates missing labels/issues, establishes native parents and populates Project items/fields. A repository initialized with a README is **not the completed scaffold**. Deliver the actual repository files through the organization's normal independent review and merge workflow.

All writes are sequential and paced by at least one second. Seven independent field updates are batched into one GraphQL request per item. A secondary or primary rate limit stops the run with its checkpoint intact; the script does not repeatedly retry, reset a rate limit or silently switch credentials. Resume the same command after GitHub permits requests again. An optional local budget allows deliberately bounded batches:

```bash
python scripts/provision_github.py --apply --max-mutations 100
```

The budget counts mutation requests, not individual aliased fields. It is a local work limit, not a claim about GitHub's rate-limit accounting.

## Checkpoint and conflict behavior

The durable `.bootstrap-state.json` contains only resource IDs, URLs, pending operation metadata and verification results. Keep this file between runs and exclude it, its temporary file and its lock file from Git. A POSIX advisory lock prevents two local instances from operating on the same checkpoint.

Before creating an issue, the helper re-reads the repository's issues across all pages and matches the exact `<!-- plan-id: APP-ID -->` marker. Duplicate markers stop execution. Existing issues are reused only when their prepared title/body/state and required labels match. Changed human-authored content or progress is preserved and reported; the script does not overwrite it to force an old plan to pass. Extra unrelated labels and live assignees are preserved.

Project IDs and option IDs are discovered from live GraphQL readback. Missing options are appended while retaining existing option IDs and values; existing fields are not deleted or renamed. The script refreshes an item's values immediately before mutation and fills only empty values. Any nonempty value that differs from the prepared initial value stops execution rather than resetting triage or work already done. Archived Project items are read and preserved; the helper never unarchives them to force initial planning state. Status options supplied by GitHub, such as its initial Todo option, may remain alongside the configured research options.

A preexisting native parent is never replaced. The helper omits authorization to move children between parents and verifies the resulting parent by readback. A timeout or GraphQL partial error leaves an uncertain operation checkpoint; the next run reconciles live resources before attempting creation again. GitHub offers no transaction across all resources, so confirmed changes remain in place after a later failure.

The prepared Project is public. A Project newly created by this bootstrap is configured accordingly. A preexisting Project with different visibility is left unchanged and reported for owner reconciliation. No preexisting repository visibility is changed.

## Verification and accurate completion

Read-only verification makes no remote changes:

```bash
python scripts/provision_github.py --verify
```

After the scaffold has actually been reviewed and delivered, verify its exact commit:

```bash
python scripts/provision_github.py --verify --scaffold-commit EXACT_40_CHARACTER_COMMIT_SHA
```

The commit must be reachable from the default branch. Local scaffold file bytes are compared to Git blob hashes at that immutable commit. Checkpoints, Git internals, virtual environments and bytecode caches are excluded. A differing or missing file, truncated tree or symlink causes an incomplete result; do not substitute a random existing SHA. Keep optional output reports outside the scaffold directory if they are not intended repository files.

Exit status 2 means incomplete, a conflict or an access/rate-limit failure. A successful provisioned-resource readback without a committed scaffold still exits 2. Exit status 0 after live verification means the provisioned resources and exact supplied scaffold passed the helper's checks; it is **not** independent review approval, product research completion or public directory publication.

The final JSON always leaves `mission_complete` false. This helper does not configure the proposed UI views, change organization access, certify review-policy enforcement or perform the research backlog. Its report lists those remaining boundaries. The authored backlog remains `prepared_not_provisioned`; actual observed IDs and results live in the checkpoint until a separately reviewed reconciliation updates planning records.

## API references

The implementation was checked against current official documentation on 2026-10-22:

- [REST sub-issue endpoints](https://docs.github.com/en/rest/issues/sub-issues): parent readback and native child creation using numeric `sub_issue_id`, with `replace_parent: false`.
- [GraphQL Projects reference](https://docs.github.com/en/graphql/reference/projects): Project, field, item and single-select mutations; existing option IDs are retained when appending options.
- [Using the API to manage Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects): item creation and separate field updates.
- [Sub-issue nesting limits](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues): the local plan is checked for native depth and direct-child bounds.

The general CLI helper was prepared with mocked tests; the later repository-scoped import has a separate successful live receipt. The CLI helper's organization-Project and cross-repository paths remain unverified live. Mocked tests cover duplicate protection, existing human changes, native-parent conflicts, Project-value preservation, JSON stdin transport, rate-limit/timeout checkpoints, partial GraphQL errors and batched field readback. They do not certify actual account permission or live GitHub API compatibility.
