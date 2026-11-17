# APP-F02.01 application identity: decisions and invariants

Issue: #68 (tasks #96 and #97) · Version 0.1.0 (proposed) · Status: proposed for review · Recorded: 2026-11-17
Schema: [schemas/application-identity.schema.json](../../schemas/application-identity.schema.json) · Validator: [scripts/validate_applications.py](../../scripts/validate_applications.py) · Tests: [tests/test_identity.py](../../tests/test_identity.py)

## User decision

Which records are the same product, and which are related editions, modules, features or services? When records turn out to be duplicates, or one record turns out to hold several products, how does the intake change without losing history or counting a product twice?

This record applies the existing rules; it does not replace them. Entity kinds and namespaces are in [docs/APPLICATION_CONTRACT.md](../../docs/APPLICATION_CONTRACT.md) (identity and scope), identity rules in [docs/TAXONOMY_AND_COVERAGE.md](../../docs/TAXONOMY_AND_COVERAGE.md) (identity rules) and boundary cases B1-B17 in [application-scope.md](application-scope.md). All worked cases below are synthetic. No real product, vendor or decision is recorded.

## Product, suite, module, feature, offering and release (T01.S02)

| Thing | Identity | Deciding test | Source rule |
| --- | --- | --- | --- |
| Product | One `app:` record | Durable identity tied to first-party documentation or distribution | Taxonomy identity rules, Product |
| Suite | One `app:` record (`product_form: suite`) | Sold or distributed as one product | B16 |
| Module or extension | Its own `app:` record, linked to its host or suite | Independently discoverable and materially distinct in access, release, contract or workflow | Module rule; B3b, B8 |
| AI feature | `feature:` entity on the product | Own `app:` only with an independent entry point, name **and** offering | S02 in application-scope.md; B7 |
| Edition, plan or channel | `offering:` entity on the product | A different plan, edition, region or channel of the same workflow | Taxonomy identity rules, Offering; B3a, B14 |
| Release | `release:` entity with a concrete version | A specific version | Contract, identity and scope |
| Family | `family:` grouping separate products | Separate products marketed together; never a suite's modules | B16 |
| Vendor | `vendor:` the publisher or responsible business | Evidenced by first-party documentation or distribution | Contract, identity and scope |

## Decisions (T01.S01)

1. **Rename.** A renamed product keeps its `app:` ID. The new name becomes `identity.name` and the old name stays in `identity.aliases`. A rename never creates a second record.
2. **Edition or plan.** An edition, plan, tier or channel is an `offering:` entity on the product, not another product, unless it meets the module rule (B8).
3. **Same name, different products.** Two products that share a normalized name or alias need an independently reviewed `distinct_products` decision in `data/identity-resolutions.json`. Without one the validator rejects the collision. The decision shape is unchanged from contract 0.1.0.
4. **Merge.** When two or more records turn out to describe one product, keep one record (the survivor) and record a reviewed `merged` decision naming the retired IDs. The survivor keeps the retired records' names as aliases and their evidence, where it still applies. A retired ID is never reused for a live record, so earlier citations and redirects keep pointing at the survivor.
5. **Split.** When one record turns out to hold several products, create one record per product and record a reviewed `split` decision naming the retired ID and at least two successors. A split ID has no single successor, so consumers must offer a choice rather than redirect.
6. **History.** A survivor or successor can later be retired by another decision. The chain is kept, not rewritten, and it must end at live records. Cycles are rejected. Each ID is retired by one decision only.
7. **Unknown operator.** A product whose publisher is unknown does not get a record. It stays a candidate note in `research/notes/` until first-party documentation or distribution evidences the vendor. A placeholder vendor (`vendor:unknown`, "Unknown", "TBD", "N/A" and similar) is rejected, because it would merge unrelated products under one invented operator. When the publisher or brand is evidenced but the legal operator behind it is not, the record uses the evidenced publisher and keeps the legal operator as a known unknown ("unresolved legal operator stays unresolved", taxonomy identity rules).
8. **No merge by resemblance.** Brand resemblance, a shared domain or a similar description is not enough to merge (taxonomy identity rules). Keep the records apart, note the possible duplicate and the missing evidence, and decide with sources.

Every `merged` and `split` decision needs a researcher, a different reviewer, a real past review date and a stable public decision URL, the same review metadata as `distinct_products`. A decision is a reviewed identity fact, not a cleanup step.

## Invariants the validator checks (T02)

| Invariant | Where | Subtask |
| --- | --- | --- |
| One record per product ID across the intake | `validate_directory` (existing) | S01 |
| One record per canonical URL | `validate_directory` (existing) | S01 |
| A name or alias shared between products needs a reviewed `distinct_products` decision | `validate_directory` (existing) | S01 |
| Aliases are distinct after normalization (case, spacing, Unicode form and invisible characters) | `validate_record` (new) | S01 |
| No alias repeats the product's own name | `validate_record` (new) | S01 |
| No placeholder vendor ID or vendor name | `validate_record` (new) | S02 |
| Decisions match `application-identity.schema.json` | `validate_directory` (new) | S01 |
| A retired ID is not a live record and is retired by one decision only | `identity_change_errors` (new) | S02 |
| A product is not merged or split into itself; a split has at least two successors | schema and `identity_change_errors` (new) | S02 |
| Merges and splits resolve to live records without a cycle | `identity_change_errors` (new) | S02 |
| Merges and splits carry independent, dated review with a public decision URL | `identity_change_errors` (new) | S02 |

## Worked synthetic cases

| Case | Outcome | Test |
| --- | --- | --- |
| Product renamed; old name kept | One record, old name as alias | `test_rename_keeps_one_product_and_the_old_name_as_alias` |
| Alias differs from the name only by case or spacing | Rejected | `test_alias_repeating_the_name_is_inconsistent` |
| Two aliases differ only by case, spacing or a zero-width character | Rejected | `test_aliases_differing_only_by_*` |
| Publisher unknown; placeholder vendor used | Rejected; keep a note | `test_unknown_operator_is_not_given_a_placeholder_vendor` |
| Two products share a name, with a reviewed decision | Accepted | `test_same_name_distinct_products_keep_the_existing_decision_shape` |
| Two products share an alias, no decision | Rejected | `test_alias_shared_with_another_product_needs_a_reviewed_decision` |
| Duplicate record merged into a survivor | Accepted; duplicate ID retired | `test_merge_retires_duplicates_into_a_live_survivor` |
| Merged record left in the intake | Rejected | `test_merged_id_cannot_stay_live_or_be_reused` |
| One record split into two products | Accepted | `test_split_retires_one_id_into_several_live_products` |
| Merge then merge again (A into B, B into C) | Accepted; resolves to C | `test_chained_changes_resolve_through_history` |
| A into B and B into A | Rejected | `test_cyclic_changes_are_rejected` |

## Not decided here

- Open boundary questions U1 (operating-system assistants) and U4 (customer-configured enterprise platforms) in [application-scope.md](application-scope.md) stay open with their consulted owners. The tests above apply to them, but this record does not classify either.
- `schemas/application.schema.json` is unchanged and the contract stays 0.1.0. Identity changes live in `data/identity-resolutions.json`, not in product records, so no record field was needed.
- How a consumer (catalog pipeline, website) shows a retired or split ID is a receiving decision for those owners ([docs/HANDOFFS.md](../../docs/HANDOFFS.md): "alias redirects", "retirement history").
- No real record, merge or split exists yet; the intake is empty.

## Acceptance

| Criterion (#96, #97) | State |
| --- | --- |
| Named outputs committed with scope, evidence references and retained unknowns | This record, the schema, the validator change and the tests |
| Reviewer assesses the exact revision | pending |
| Structural validation reported separately from factual acceptance | Validation is structure only; no product fact is asserted |
