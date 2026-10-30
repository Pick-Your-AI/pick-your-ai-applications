# Contributing

The [organization policy](https://github.com/Pick-Your-AI/.github/blob/main/CONTRIBUTING.md) governs access, branches, reviews and merges. Use `contrib/<login>/<topic>` for early contributor branches. A PR to the default branch needs a non-author approval, approval of the latest push by someone other than the person who pushed it, and any required checks. Access is managed through authorized teams; CODEOWNERS alone is not an access grant or enforcement mechanism.

## Workflow

1. Read the current issue, live ownership, comments, existing research and [workflow](docs/RESEARCH_WORKFLOW.md). Keep the specified deliverable path.
2. Add candidates and unresolved findings to a research note using [the template](templates/research-note.md). Record the actual date and source of each checked assertion.
3. Add complete structured research records only when the contract's required facts are available. Keep unknowns explicit. Every product/plan/version identity and claim needs appropriate provenance.
4. Record evidence class, independent reproduction/corroboration and review separately. Record source/field/intended-use rights separately from all three.
5. Run `python scripts/validate_applications.py`, `python scripts/validate_planning.py` and `python -m unittest discover -s tests -v`.
6. Open a focused PR. Use `Refs #N` for partial progress and `Closes #N` only when the entire issue acceptance and receiving handoffs are met. Include source-check dates, evidence limitations, exact validation and consumer impact.
7. Obtain the required review. Publication-eligible metadata still needs an accepted consumer handoff before it is called published.

## Research acceptance

A completed package identifies the user decision, bounded discovery method, deduplicated candidates, comparison fields, claim-level evidence, scoped negatives/unknowns, source-use decisions or unresolved rights, and an accountable next action. It has a merged decision record and confirmed required handoffs. Empty tables, a generated file, a merged partial PR or a vendor page are not proof of completion.

Do not copy paid or restricted sources into public Git. Use sanitized evidence manifests for external material. Do not commit secrets, customer data, datasets, weights, large downloads or raw browsing captures containing private information.

## Routing decisions

For an unresolved decision, first read the existing issue, its assignees, relevant
decision record and related pull requests. Preserve accepted ownership and local
review, evidence, security and release requirements. Routing identifies a contact;
it does not grant access, appoint an owner, authorize publication or waive a gate.

Use the canonical [escalation guide](https://github.com/Pick-Your-AI/.github/blob/main/docs/governance/ESCALATION.md) and
[versioned routing policy](https://github.com/Pick-Your-AI/.github/blob/main/governance/escalation-policy.json). These links depend on the organization
governance change merging; until then, use its reviewed checkout and describe the
route as provisional. Do not claim the central tooling is installed or active.

The order is repository team → repository maintainer → repository lead maintainer
→ applicable parent teams → CompleteDotTech. Record a disposition at each level,
including unresolved, vacant, pending-acceptance or inaccessible roles; membership,
team-management status and repository permissions do not establish accepted
operational ownership. Keep owner placeholders for the final fallback. Do not
silently skip an unresolved role or treat a proposed mapping as accepted.

An operator with read access must refresh the private snapshot before resolving:

```sh
python /path/to/org-checkout/governance/router.py refresh --policy /path/to/org-checkout/governance/escalation-policy.json --snapshot /private/path/routing-snapshot.json --status /private/path/routing-status.json
python /path/to/org-checkout/governance/router.py resolve --policy /path/to/org-checkout/governance/escalation-policy.json --snapshot /private/path/routing-snapshot.json --repo Pick-Your-AI/pick-your-ai-applications --max-age-seconds 86400 --status /private/path/routing-status.json
```

Here `86400` is an **operator-selected example**, not an approved default. Select
an appropriate explicit maximum age; a proposed policy value does not supply one.
Check that refresh succeeded. If refresh fails, stop recipient selection and
report the failure; the last successful snapshot is retained for diagnosis, not
as a current route. Report stale or incomplete coverage explicitly. Keep snapshots,
raw API responses, rosters and private
identities outside public Git and public issues. Share only the necessary public
team destination and a sanitized decision summary.

When escalation is needed, include the decision needed, current responsible role,
prior disposition and proposed next recipient. Reuse information already in the
issue or PR; routine contributions need no full escalation history. Send nothing
and change no assignment automatically. For security concerns, follow the
[existing security policy](SECURITY.md), including its conditional reporting routes.
This routing guidance establishes no additional or verified private destination.

The owner-selected scope of [organization issue #14](https://github.com/Pick-Your-AI/.github/issues/14)
is all changes in Research, Sustainability, Applications, Papers, Catalog Pipeline
and Datasets. This records scope only: current independent-review and branch/check
requirements remain in force. Any proposed enforcement change requires separate
approval; no review exception or CODEOWNERS change is established here.
