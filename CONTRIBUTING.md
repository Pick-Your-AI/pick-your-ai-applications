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
