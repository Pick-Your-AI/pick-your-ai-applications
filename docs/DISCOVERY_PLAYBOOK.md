# APP-F04.02 — Bounded application discovery and deduplication playbook (proposal)

Refs #77, #114 and #115. This is a repeatable **candidate discovery** method for the 48 authored categories in [taxonomy v0.1.0](../taxonomy/README.md), not an assertion of market completeness or a list of verified products. The first actual campaign must be logged with its own real dates, inspected sources and non-author review before any coverage count or product claim changes.

## 1. Declare a reproducible campaign before searching

For one category (APP-C01 through APP-C48) record: the user decision, subcategory boundaries, inclusion/exclusion tests, required fields, planned source frames, search terms with language and geography, actual start and cutoff dates, minimum sampling rationale, sources not available, and a stopping rule. Include hosted/local/open-source/non-generative AI and narrow regional/vertical products when in scope. Do not treat 48 categories or 288 subcategories as the world's total products; a product may belong to multiple categories.

Use the [discovery log](../templates/discovery-log.md) for each bounded campaign, with public references and actual inspection status. Prespecify a saturation rule, e.g. no new distinct leads in the last *documented* search frame, rather than changing the threshold after results are seen. Record time/budget constraints and exclusions instead of claiming exhaustive coverage.

The scope is **applications people use to perform a recognizable workflow**. Under the [application contract](APPLICATION_CONTRACT.md), an underlying model, provider, inference endpoint, infrastructure, toolkit or stand-alone integration is not a new application merely because it has a brand name. AI use may be predictive, classificatory, perceptual, recommendational, optimizing or generative.

## 2. Search multiple candidate frames without unauthorized access

| Frame | Reproducible lead strategy | Source of factual product claims |
| --- | --- | --- |
| Supplier-controlled public directories | Documented query/navigation of official product/service catalogs, release notes and product manuals, with region and edition filters | Official product documentation inspected at the recorded date |
| Official app stores and marketplaces | Store/category/search queries, supported platform, locale, storefront geography and listing date | Vendor-operated listing and linked official docs where permitted; a store's ranking is not capability evidence |
| Open-source software projects | Public repository/topic searches, README plus release/tag/distribution checks; separate libraries and client apps | Maintainer's public docs and release-specific materials, not stars/fork counts as verification |
| Enterprise suites and vendors | Product portfolio search and suite/module/edition comparison, including acquired/rebranded product lines | Versioned supplier docs for the actual module, plan and provisioned entitlement |
| Specialist and vertical software | Domain-specific public vendor lists, professional catalogs and industry directories; include predictive/optimization workflows | Inspect the application's own primary documentation; secondary directories create leads only |
| Non-English/regional offerings | Translate documented category concepts into selected local languages; search local vendor domains and storefront locales | Original-language official source, with language/translation uncertainty explicitly recorded |
| Existing Pick Your AI research | Crosswalk model/provider identities (T1), integration/framework identities (T4) and market research evidence | Preserve original record/reviewer/source and its limits; never silently copy a claim or reuse rights |

For each frame, log every **actual** query, query language, region, source class, public URL (no credentials, tracking or signed query strings), source-check date, access outcome, visible result bound, and known ranking/index bias. Search result snippets, SEO pages, media mentions and secondhand aggregators are candidate leads only.

Do not create paid accounts, accept new terms on behalf of others, bulk scrape, bypass robots/access gates, call paid APIs, contact vendors, deploy crawlers, or harvest customer/private data. A method may be designed offline; its live execution needs separate authorization. A failed page or gated report remains "not inspected" and must not become negative evidence or an Unsupported claim.

## 3. Candidate state transitions (no invented facts)

1. **Sighting:** assign a local discovery-log lead ID, preserve the result locator, query/frame/date and quoted *reason for checking* in original wording. The lead is not yet an admitted product. A search result can say only that a candidate was returned.
2. **Primary-source check:** inspect the exact official product documentation; record publisher, document version/release, actual checked date, access status and boundaries. A claim can be marked **Documented** with its vendor scope, but is not independently verified merely because the source was read.
3. **Identity comparison:** crosswalk the lead against existing canonical application IDs and the known T1/T4/market records; flag likely rebrands, aliases, suites, editions, regional white labels and integrations before suggesting a new product. Keep unresolved cases as leads with conflict notes.
4. **Research eligibility:** only a source-backed, deduplicated product with the application contract's required fields may become a structured proposal. Incomplete findings remain [research notes](../templates/research-note.md). Publication and verification do not follow from research eligibility.
5. **Independent acceptance:** a non-author reviewer checks the exact facts and revision, and any affected receiving owner accepts the handoff separately. Preserve source/field/intended-use rights decisions; no universal grant follows from public visibility.

Maintain the difference between: a search sighting, a distinct candidate, an admitted product, a checked claim, a reviewed product, an independently measured product and an eligible/published record. Do not modify [coverage counters](../coverage/README.md) from a generated list, static plan or uninspected candidate.

## 4. Identity and exception review — #115

Evaluate candidate matches using **multiple specific identifiers**, not name similarity as proof: normalized names and aliases; operator/vendor identity; canonical product URL; stable product IDs; documented version/edition; distribution ownership; release/rebrand history; published equivalence or migration statement; and independent review. Preserve a link between sibling products without flattening them into one record.

| Case | Required treatment |
| --- | --- |
| Same name, different operators or use cases | Keep separate pending identity evidence; do not merge by normalized name |
| Alias or explicit rebrand | Retain the historical name with sources and dates; distinguish same product from successor |
| Suite, module and purchased edition | Research the actual user workflow; an offering/feature is not automatically a separate product |
| White-label/OEM service | Check documented operating entity, edition and distinct workflow; flag uncertainty instead of collapsing brands |
| Fork, acquisition, split or merger | Require explicit reviewed identity-change decision before retiring or reusing IDs; preserve predecessors and receiving redirects |
| Integration, plugin, model/API vs full app | Link T4/T1 component where sourced, but do not turn it into a product-count duplicate |
| Uncertain match or inaccessible source | State competing hypotheses and missing evidence; keep it unresolved and excluded from deduplicated counts |

For any contested duplicate, record each candidate's evidence and opposing interpretation, an exact decision request, independent researcher/reviewer, and immutable review receipt when one actually exists. APP-F02.01 supplies the canonical identity decision vocabulary when accepted; this playbook does not preapprove or implement it. No unreviewed automatic merge, deletion or canonical ID reuse is allowed.

## 5. Reporting coverage, exclusions and stopping

Summarize actual frames attempted, searched terms, dates, regions/languages, source counts, lead sightings, deduplicated candidate proposals, reviewed products, rejected leads, unresolved matches, failed access, rights restrictions and saturation curve **only where evidenced**. Preserve cross-category overlap by canonical product ID; never add the same product to a global total twice.

A bounded numerator needs a real, enumerated denominator and survey cutoff. No inferred global coverage percentage is permitted without a defined closed survey. When the search was partial, label the surveyed set **partial**; unknown regions, inaccessible official pages, non-English markets and unobserved vendors remain explicit blind spots. An unused log is not evidence of research.

## 6. Review and downstream boundaries

A non-author reviewer checks that the intended category/scope, actual query/source details, primary evidence, deduplication exceptions and limitations are reproducible and not overstated. The received candidate log is **not** authority to show product capabilities, pricing, endorsements or logos publicly. Research #41 retains source-use rules, APP-F02.01 identity decisions remain independently reviewed, and application records/website/pipeline projections require their own separate approvals and rights. No scheduled discovery or outreach is activated by this document.

**State:** proposed method and blank template only. Product discovery sessions, receiving acceptances and evidence-based coverage updates have not been performed in this PR. Close #77/#114/#115 only after exact-revision review and required handoffs.
