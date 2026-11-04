# Application taxonomy and coverage method

Status: **proposed research structure**, prepared 2026-10-22. This file defines what the new applications corpus will investigate. It does not claim that any product has been researched, independently tested, approved for publication or deployed to the website.

The taxonomy contains **48 product-workflow categories in eight domains, 288 named subcategories and 15 cross-cutting facets**. Counts describe this authored structure. They are not the size of the AI market. The machine-readable authority for this version is `taxonomy/taxonomy.json`; the starting ledger is `coverage/ledger.json`.

## Scope and ownership

An application is identifiable software that offers a usable AI-assisted workflow to an individual or organization. Include standalone products, separately identifiable suite modules, client applications, extensions and software-delivered services. A product can be proprietary, open source, source available, local, customer hosted or vendor operated. Include predictive, classificatory, perceptual and optimization applications alongside generative and agentic ones. A marketing use of “AI” is a discovery lead, not sufficient evidence of a material AI workflow.

Models, inference routes, engines, hardware, SDKs, frameworks, integration connections, MCP servers, datasets and papers remain different entity kinds. Their canonical evidence stays with existing research owners. An application may **use** a model, **expose** an integration or **contain** a workflow; those relationships do not make the entities interchangeable. The website remains the owner of directory UI and public delivery. The catalog pipeline receives approved structured handoffs; it does not decide research truth or source rights merely by accepting JSON.

Generic consulting and implementation agencies without an identifiable software-delivered workflow are retained, if useful, as service-provider discovery notes outside product counts. A directory of other products is a discovery source unless it independently offers an AI-assisted application workflow. Announcements, inaccessible products, prototypes, waitlists and retired offerings can have explicit lifecycle records; none automatically qualifies as a currently available application.

## Identity rules

| Entity | Identity and decision rule | Do not infer |
| --- | --- | --- |
| Operator or publisher | A sourced organization/person/brand relationship with time and role; unresolved legal operator stays unresolved. | A domain name proves legal ownership. |
| Product | A durable product identity tied to canonical first-party documentation or distribution. Track aliases, renamed brands, acquisitions and predecessors. | A different marketing name always means a new product. |
| Suite | A product grouping related modules; count separately from modules only with explicit aggregate counting rules. | Every feature is a separately sellable product. |
| Module or extension | Separate only when independently discoverable and materially distinct in access, release, contract or workflow. Link its containing suite/host. | One entry per feature, language or category. |
| Offering or plan | Product × operator × plan/channel × region or tenant option, with effective dates and conditions. | A capability on one plan exists on every plan. |
| Release or version | Exact application release or documented observation of an unversioned service. Retain access date and source revision. | A floating brand or latest label is immutable. |
| Claim | One fact or bounded result with source, grade, conditions and applicability. | One reviewed claim verifies the whole product. |
| Price fact | Exact meter, amount/currency, billing period, quota and commercial conditions for the selected offering. | “Free,” “open source,” monthly equivalent or included credits establish zero total cost. |
| Underlying component | Reference existing T0–T6 identity and version where evidenced. | Listing a component proves the application actually uses it in the selected offering. |

Do not merge records solely by brand resemblance, shared domains or similar descriptions. Preserve a possible-duplicate relationship and the unresolved evidence instead. A fork or reseller can be a distinct product/operator offering, but requires an explicit relation and evidence. Retired identities remain available for historical citations and redirects. Source/code licenses, service terms, model licenses, input rights and output rights are separate materials.

## Classification and navigation

Pick one primary category for the product or module's main user workflow; attach any additional **evidenced** workflows as secondary category tags. Assign facet values at the offering or claim scope needed to make them true. A provider may sell several distinct products; a product may serve several audiences and industries. Neither situation should inflate the distinct-product count.

The category tree organizes research ownership and browse navigation. Facets carry orthogonal properties: audience, product form, access surface, deployment, AI role, input/output modalities, action scope, distribution rights, lifecycle availability, commercial model, language coverage, geography, accessibility and enterprise controls. A native mobile application is a surface, not a separate domain; a French interface is not evidence of French output quality. Accessibility is both a cross-cutting evaluation dimension and a primary category when assistive access is the product's central purpose.

The application deployment vocabulary is a proposed directory facet. It is not a silent replacement for the accepted T0 serving-component operator/capacity vocabulary. An application can combine hosted and local functionality without changing a linked component's canonical deployment classification.

## Category inventory

Each row has a separate research decision-record path, six subcategories, specific comparison fields, evidence questions and an independently reviewable work package. Small tasks and subtasks belong in that work package's checklist. Native issue children should represent independent deliverables, not every mechanical step.

| ID | Domain | Application category | Proposed research path |
| --- | --- | --- | --- |
| APP-C01 | Knowledge work and personal productivity | General assistants and answer search | `research/categories/general-assistants.md` |
| APP-C02 | Knowledge work and personal productivity | Enterprise search and knowledge work | `research/categories/enterprise-knowledge.md` |
| APP-C03 | Knowledge work and personal productivity | Writing, editing and editorial publishing | `research/categories/writing-editorial.md` |
| APP-C04 | Knowledge work and personal productivity | Translation and localization | `research/categories/translation-localization.md` |
| APP-C05 | Knowledge work and personal productivity | Document intelligence and extraction | `research/categories/document-intelligence.md` |
| APP-C06 | Knowledge work and personal productivity | Meeting, speech and communication assistance | `research/categories/meetings-communication.md` |
| APP-C07 | Knowledge work and personal productivity | Office suites, spreadsheets and presentations | `research/categories/office-authoring.md` |
| APP-C08 | Knowledge work and personal productivity | Personal productivity and planning | `research/categories/personal-productivity.md` |
| APP-C09 | Software, data and process tools | Coding assistants and engineering copilots | `research/categories/coding-assistants.md` |
| APP-C10 | Software, data and process tools | Application, website and low-code builders | `research/categories/application-builders.md` |
| APP-C11 | Software, data and process tools | Software testing, review and quality assurance | `research/categories/software-quality.md` |
| APP-C12 | Software, data and process tools | IT operations, service management and cloud assistance | `research/categories/it-operations.md` |
| APP-C13 | Software, data and process tools | Analytics, business intelligence and decision support | `research/categories/analytics-decision.md` |
| APP-C14 | Software, data and process tools | Workflow automation and enterprise agent applications | `research/categories/workflow-automation.md` |
| APP-C15 | Creative media and interactive products | Image, graphic and visual design | `research/categories/image-graphics.md` |
| APP-C16 | Creative media and interactive products | Video, animation and avatar creation | `research/categories/video-animation.md` |
| APP-C17 | Creative media and interactive products | Audio, voice and music creation | `research/categories/audio-voice-music.md` |
| APP-C18 | Creative media and interactive products | 3D, CAD and spatial design | `research/categories/spatial-design.md` |
| APP-C19 | Creative media and interactive products | Games and interactive entertainment | `research/categories/games-interactive.md` |
| APP-C20 | Creative media and interactive products | Browser, computer and device agents | `research/categories/computer-browser-agents.md` |
| APP-C21 | Customer and business operations | Sales, CRM and revenue operations | `research/categories/sales-revenue.md` |
| APP-C22 | Customer and business operations | Marketing, advertising and growth | `research/categories/marketing-growth.md` |
| APP-C23 | Customer and business operations | Customer support and contact centers | `research/categories/customer-support.md` |
| APP-C24 | Customer and business operations | Commerce, retail and merchandising | `research/categories/commerce-retail.md` |
| APP-C25 | Customer and business operations | Project, product and portfolio management | `research/categories/project-product-management.md` |
| APP-C26 | Enterprise functions and assurance | Finance, accounting and business planning | `research/categories/finance-accounting.md` |
| APP-C27 | Enterprise functions and assurance | People operations, recruitment and workforce | `research/categories/people-hr.md` |
| APP-C28 | Enterprise functions and assurance | Legal work, contracts and e-discovery | `research/categories/legal-contracts.md` |
| APP-C29 | Enterprise functions and assurance | Procurement, sourcing and supplier management | `research/categories/procurement-suppliers.md` |
| APP-C30 | Enterprise functions and assurance | Cybersecurity, identity and fraud operations | `research/categories/security-fraud.md` |
| APP-C31 | Enterprise functions and assurance | Governance, risk, compliance and assurance | `research/categories/governance-risk-compliance.md` |
| APP-C32 | Professional, scientific and public domains | Education, tutoring and training | `research/categories/education-training.md` |
| APP-C33 | Professional, scientific and public domains | Healthcare delivery and clinical administration | `research/categories/healthcare.md` |
| APP-C34 | Professional, scientific and public domains | Life sciences, pharmaceuticals and laboratory work | `research/categories/life-sciences.md` |
| APP-C35 | Professional, scientific and public domains | Scientific research, literature and discovery | `research/categories/science-research.md` |
| APP-C36 | Professional, scientific and public domains | Financial services, investing and insurance | `research/categories/financial-services.md` |
| APP-C37 | Professional, scientific and public domains | Government, civic and public-service applications | `research/categories/public-sector.md` |
| APP-C38 | Industry, infrastructure and environment | Manufacturing, engineering and industrial work | `research/categories/manufacturing-engineering.md` |
| APP-C39 | Industry, infrastructure and environment | Supply chain, logistics and transport operations | `research/categories/logistics-supply-chain.md` |
| APP-C40 | Industry, infrastructure and environment | Architecture, construction and real estate | `research/categories/built-environment.md` |
| APP-C41 | Industry, infrastructure and environment | Energy, utilities, climate and environment | `research/categories/energy-climate.md` |
| APP-C42 | Industry, infrastructure and environment | Agriculture, food and natural-resource operations | `research/categories/agriculture-food.md` |
| APP-C43 | Industry, infrastructure and environment | Geospatial, earth observation and surveying | `research/categories/geospatial-earth.md` |
| APP-C44 | Consumer, assistive and autonomous applications | Accessibility and assistive applications | `research/categories/accessibility-assistive.md` |
| APP-C45 | Consumer, assistive and autonomous applications | Personal wellness, fitness and sports | `research/categories/wellness-sports.md` |
| APP-C46 | Consumer, assistive and autonomous applications | Travel, hospitality, home and consumer services | `research/categories/travel-lifestyle.md` |
| APP-C47 | Consumer, assistive and autonomous applications | Social, companionship and community applications | `research/categories/social-companionship.md` |
| APP-C48 | Consumer, assistive and autonomous applications | Robotics, autonomy and physical-agent software | `research/categories/robotics-autonomy.md` |

## Evidence states and publication boundaries

Follow the upstream claim-level evidence grades: **Primary documentation**, **Vendor claim**, **Independent measurement**, and **Estimate**. Reading a publisher's capability statement supplies documentary evidence that it makes that statement. It does not independently establish the capability or its quality. A bounded exercised workflow supplies only the result, configuration, version, inputs, conditions and limitations actually observed. Unsupported needs eligible explicit negative evidence or the applicable documented complete-list rule; a missing page, failed load or absent marketing mention remains Unknown.

A research record can be valid while important questions remain unresolved. Review can accept an explicit Unknown finding. Review is not source-use clearance, a legal interpretation, production implementation or consumer acceptance. For prices and other current-state facts, keep the actual access date, effective date when known, region, plan, units and conditions. Version-pinned facts keep their exact scope; no universal expiry period is adopted. Trigger rechecks on relevant version changes, revised terms, corrected evidence, product retirement, conflicts or a new intended use.

Publish only the fields and material with an applicable source/use decision and review at a declared immutable revision. Display, caching, bulk export, API redistribution, screenshots/logos and internal research are distinct intended uses. An eligible product name/link does not permit redistributing the whole source page. Unknown rights or an inaccessible source must not be turned into a permissive default. This task does not authorize bulk collection, purchase, benchmark execution, participant outreach or use of customer data.

## Measuring coverage without inventing a market census

The initial ledger has **48 `not_started` category rows**. All counters start at zero because no products were recorded by this new corpus baseline. This is not a claim that those categories contain no products. `owner`, `reviewer`, source cutoff and last source check are intentionally unassigned in planning; future complete records must satisfy their own required-field rules. A planning null is not permission to invent a missing product fact.

For each category, declare the searched source families, language/region scope, query or selection protocol, cutoff, inclusions and exclusions before interpreting counts. A bounded source set can support a ratio such as “43 of 61 eligible identities in the declared survey have reviewed claims.” It cannot support “70% of all AI applications.” Preserve excluded and unresolved candidates, source failures and discovery channels so another researcher can reconstruct the denominator.

Report these measures separately:

1. **Breadth:** categories/subcategories examined, source families, languages and regions, with explicit unexamined gaps.
2. **Identity:** raw candidate sightings, deduplicated products, independent modules and offerings. Sum only the appropriate unique IDs across overlapping categories.
3. **Depth:** products with primary-linked claims, reviewed records and independent measurements. A record may contain a mixture of grades and Unknowns.
4. **Freshness:** actual dated checks of current-state claims, superseded evidence and event-triggered recheck queues. Counts of dates alone do not certify current truth.
5. **Rights:** permitted material/field/intended-use combinations, unresolved decisions, expired grants and restrictions.
6. **Delivery:** eligible immutable artifacts, receiving-owner acceptance, published versions and actual public readback. A merged Markdown note is not a published directory entry.

No arbitrary product count completes a category. Completion means the predeclared bounded survey and its literal acceptance criteria are satisfied, with omissions and next expansion actions documented. Near-exhaustiveness is a maintained process across explicit territories and discovery methods, not a permanent global percentage. New categories and splits require a versioned rationale, old-ID crosswalk and migration review.

## Existing-research overlap and receiving responsibilities

| Existing owner or artifact | Reuse | Applications boundary |
| --- | --- | --- |
| [Research AGENTS and workflow](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/AGENTS.md) | Evidence discipline, incomplete notes, claim conditions and review requirements | Use a separately versioned application proposal; do not mutate the frozen builder contract. |
| [T1 model taxonomy](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/T1-model-selection/model-taxonomy.md) | Model identity and task/output distinctions; model/component references | An application UI, branded service and underlying model are distinct. Retain original dates and grade when linking evidence. |
| [T4 agents and integrations](https://github.com/Pick-Your-AI/pick-your-ai-research/tree/main/research/T4-agents-integrations) | Framework/tool/integration/MCP/memory identities and bounded research | Research the application's actual user workflow, selected action scope and offering. Registry or connector presence proves no runtime authorization or safety. |
| [Market competitor catalog](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/market/competitors.json) | Discovery leads, prior identity resolutions, documented unknowns and source links | Do not bulk import competitors as verified applications. Check each entity kind and current offering; retain the market study's original scope. |
| [Market synthesis](https://github.com/Pick-Your-AI/pick-your-ai-research/blob/main/research/market/synthesis.md) | The bounded decision-record comparison and its accepted historical evidence | A broad reference taxonomy does not overturn its narrow commercial-validation decision or prove demand for the directory. |
| [Research #40](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/40) | Canonical builder schema/compatibility ownership and affected-owner review | Propose crosswalks and versioned handoffs; do not force applications into incompatible v1 kinds. |
| [Research #41](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/41) and [#60](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/60) | Evidence, source-use and publication policy | Rights decisions remain source/material/use-specific; new use needs actual review. |
| [Research #39](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/39) and [#36](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/36) | Cost/price and evaluation semantics | Document application seats, credits, tasks and outcome metrics without pretending they are supported frozen-schema meters. |
| [Website repository](https://github.com/Pick-Your-AI/pick-your-ai-website) | Search/browse/filter, citations, revisions, accessibility and public display requirements | Deliver versioned requirements and eligible data; the applications repository does not duplicate the frontend. |
| Catalog pipeline | Identity mapping, admitted record contract, publication/correction/withdrawal receipts | Pipeline existence and consumer support require actual readback; planned handoffs are not accepted handoffs. |

This map is a division of proposed delivery responsibility, not a reassignment of any existing person or issue. Live assignees, accepted contracts and current source-owner decisions remain authoritative.

## Per-category research protocol

The machine-readable work package provides four task groups: define the survey and permitted source plan; discover and reconcile identities; build the evidence-backed comparison; and independently review, reconcile coverage and hand off. Each group has small checklist subtasks. The suggested High/Medium priorities are qualitative planning judgments for sequencing the method and breadth. They are not empirical vendor scores, promises, estimates or authority to overwrite an existing Project field.

Start with a coherent user decision and compare products on the category-specific fields. Keep claim-to-source mappings reproducible, record unsuccessful retrieval and test attempts, and distinguish hypotheses from evidence. Submit a bounded slice with `Refs` while broader research remains incomplete. Close the category only when its acceptance criteria, independent review, merged revision and material handoffs have actual receipts. The domain/program parents additionally require their children and synthesis; creating the hierarchy cannot satisfy those criteria.

## Inspection provenance

`inspection-references.json` records the existing files and blob SHAs examined for this design. The T4 summary and market synthesis were read in bounded sections; they are not claimed as full line-by-line audits of those long files. This design pass read repository evidence and created research structure. It did not check vendor pages, exercise applications, run benchmarks, collect private data, assess legal terms afresh or award independent verification to any product claim.
