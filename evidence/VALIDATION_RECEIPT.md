# Local scaffold validation receipt

Date: 2026-10-22. Scope: authored repository foundation and planned delivery hierarchy. This is not a GitHub approval, source-truth assessment, legal review or product-capability verification.

The integrated application validator reports zero real application records and zero pricing records. The planning validator reconciles 48 categories, 288 subcategories, 135 native issue definitions, 134 internal parent edges, 192 checklist task groups and 768 small subtasks. The external program-to-research-#509 edge is specified separately and has not yet been created.

The initial integrated regression suite passed 43 tests. An independent local review confirmed matching taxonomy/foundation/backlog content, current schema copies, generated issue bodies, empty product intake and honest zero-start coverage. It identified a future regeneration risk: the renderer could reset remote identifiers. A guard now refuses regeneration after provisioning state exists or live identifiers/status have been recorded; two regression cases cover that correction.

Final commands:

```sh
python scripts/validate_applications.py
python scripts/validate_planning.py
python -m unittest discover -s tests -v
```

These checks cover offline structure, field prerequisites, scoped evidence/review/rights declarations, taxonomy references, exact price identities, non-finite/unknown values, parentage/cycles, truthful coverage, Project option alignment and preservation of remote state. They cannot confirm actual source access, independent experiments, rights interpretations, reviewer identity or website use.

GitHub provisioning and CI results must be appended as actual readback evidence, not inferred from these local checks. The program and all future research outcomes remain unfinished.

## Resumable provisioning helper

The offline helper dry run matches all 135 planned issues, 135 total native relationships (including the external parent), seven Project fields, 945 initial values and four type labels. Its 15 no-network regression tests cover duplicate protection, preservation of existing human changes and parentage, JSON stdin transport, timeout/rate-limit checkpoints, read-only behavior and batched Project values. The combined suite contains 60 tests. The helper has not been used to create or modify any GitHub resource.
