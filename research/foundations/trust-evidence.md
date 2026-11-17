# APP-F03.04 — Trust disclosures and evidence method (proposal)

Refs: #75 (work package), #110 (documentary intake), #111 (presentation limits). This is a **research method**, not an assessment of any application, an accepted policy, a security certification, or authority to publish third-party material. Consumer decisions remain pending.

## User decision and scope

For a specific application product and offering, what does a supplier **actually document** about privacy, security, assurance and use rights, under which conditions and as of which check date? The result must let a reader distinguish a supplier statement, a dated independent examination, a reproducible test, and an unresolved question. It must not generate safety, legal suitability or compliance scores.

Apply the existing [application contract](../../docs/APPLICATION_CONTRACT.md), [research workflow](../../docs/RESEARCH_WORKFLOW.md), [review rules](../../docs/REVIEW_POLICY.md), [rights policy](../../THIRD_PARTY_RIGHTS.md) and [security policy](../../SECURITY.md). Shared research #41 owns canonical source-use policy; research #35 is background guardrail research, **not** a product assurance decision.

## Bounded trust evidence matrix

Each row represents a separate scoped question; one generic trust page is not enough to answer the entire matrix. Record applicability for the exact product, release/channel, plan, geographic deployment, contractual tier and observation date. An enterprise-only control does not apply to a free consumer tier by inference.

| Question | Evidence to seek and exact scope to record | Do not infer |
| --- | --- | --- |
| Training and reuse of input/output | Supplier's documented default, consent/opt-out, enterprise exception, model-improvement use and effective terms | "No training" from confidentiality wording or an unspecified plan |
| Collection, retention and access | Prompts, files, outputs, logs, support/admin access, backup retention, configurable limits and exceptions | No retention from a delete button or a short default period |
| Deletion, export and portability | Initiator, data classes, production/backup timelines, policy/version, effective guarantees and exclusions | Immediate irreversible deletion or full export from a UI label |
| Subprocessors and onward transfer | Published vendor/subprocessor list, purpose, date, region, optional vendors and contractual terms | No subprocessors from an incomplete list |
| Region and residency | Storage and processing locations, support access, data transfer, plan and service boundaries | End-to-end residency from a regional cloud setting |
| Encryption and key management | At-rest/in-transit statements, protocols, provider-managed versus customer-managed keys, scope and exceptions | Independently tested protection from a product badge |
| Identity, access and audit | SSO, MFA, roles, tenant isolation, audit logging, export and relevant subscription tier | Universal support or effectiveness from "enterprise-grade" |
| Incident and vulnerability process | Public notification commitment, disclosure channel, scope, publication date and exceptions | Zero incidents from silence, or a safe system from a bug bounty |
| Assurance reports and certifications | Issuing body, report/standard type, audited entity, covered service, period, exclusions, exceptions, expiration, permitted summary | Every product or control is covered; a report is a product-wide guarantee |
| Content/IP terms and commercial reuse | Terms for input/output ownership, licenses, confidentiality, training reuse, indemnity, commercial use and account/region exceptions | Legal ownership or unrestricted rights from marketing text |

A single source may answer several questions, but each answer retains its own source ID, exact field, conditions and limitations. If no permitted evidence is found, the answer remains **Unknown** or **Not disclosed**; untested is never "Unsupported".

## Intake sequence and evidence distinctions

1. **Identify the subject.** Record canonical application ID, product display name (pending identity evidence when necessary), offering, version, account entitlements, region and the user's precise decision. A trust statement about the operator, parent company, model, infrastructure host or another service is not automatically a statement about the product.
2. **Log the source check.** For each claim record a public canonical HTTP(S) URL without credentials/query tokens, publisher/authority, document title and version if known, the *actual* check date, and an access outcome: public/readable, gated/not inspected, unavailable, or conflicting. Gated/failed inspection has no checked factual content. Avoid copying full restricted reports, customer contracts or screenshots into public Git; use original summaries and permitted references only.
3. **Capture the claim without promoting it.** Preserve the narrow source language in an original paraphrase, the claim field, applicable product/plan/version/region conditions, actual as-of date, and exceptions. Distinguish documentation of a publisher-controlled term (**primary_documentation**) from an untested security/performance assertion (**vendor_claim**).
4. **Classify independent evidence separately.** An auditor report is an independent documentary examination of its *stated* subject, period and controls, not a direct reproduction of every claim. A researcher-controlled test requires a permitted offline/synthetic protocol with inputs, version, result, limitations and a separately linked receipt. An estimate stays **estimate**. Never claim that a report was read when only its public title or seal was seen.
5. **Handle disagreement and time.** Keep both conflicting statements, periods and caveats in the research note; mark the normalized claim **disputed** pending review. Changed terms or disclosed defects trigger **recheck_required**, not silent historical erasure. Older documents are not automatically false, and no universal TTL is invented.
6. **Separate decisions.** Independent verification, non-author review of the exact revision, field/source/intended-use rights and downstream publication acceptance are independent decisions. A passing validator proves only the encoded structure. Record missing decisions as pending.

### Evidence-state crosswalk

| Observation | Source check | Evidence grade | Verification | Presentation state |
| --- | --- | --- | --- | --- |
| Search result or inaccessible gated report | unchecked / failed access | none assigned | unverified | Unknown; candidate only |
| Supplier terms or documentation inspected | checked | primary_documentation (supplier-controlled terms) | unverified | Documented, dated, attributed |
| Supplier claim of security or performance | checked | vendor_claim | unverified | Supplier-reported, not tested |
| Auditor's report read within authorized terms | checked | grade appropriate to the exact report claim; do not relabel a vendor's broader claim | unverified absent qualifying independent evidence for that exact claim | Independently reported examination, tightly scoped |
| Independently repeated permitted test | checked | independent_measurement when the protocol and receipt qualify | verified **only** with the contract's verifier/receipt requirements | Exercised only under the measured conditions |
| No inspected explicit negative evidence | unchecked or checked other sources | none for negative claim | unverified | Unknown, never Unsupported |

An independent audit may corroborate a narrow control; it does not automatically change an unrelated vendor claim to verified. For an explicit Unsupported finding, retain affirmative negative evidence and its completeness/conditions. A marketing omission cannot justify it.

## Presentation and review gates — #111

- **No blanket trust badges.** Do not generate "secure", "safe", "compliant", "certified", "HIPAA-ready", "GDPR-compliant", "zero data retention", "no training" or similar product-wide badges from incomplete pages, uninspected reports, or a supplier's logo. Avoid a composite security/compliance ranking or endorsement.
- **Allowed factual language is attributable and bounded.** For example, "Supplier documents [control] for [named plan] as of [actual date], subject to [exception]" only after checking and recording the exact cited source. Describe a report as "supplier links a [report type] covering [entity/service and period]" unless the report itself was lawfully inspected and reviewed.
- **Report the uncertainty.** Show Unknown/Not disclosed/Disputed distinctly, the source-check date, coverage gaps, gated material, expired or withdrawn statements, and the difference between documented and independently exercised evidence. Never map Unknown to false, no cost, or no risk.
- **Rights before reuse.** Publishing a security claim, quote, logo, report excerpt, certification mark or screenshot has a separate source/field/use decision. A permissible original factual summary does not grant reuse rights to brand assets or restricted reports. Withhold an otherwise reviewed fact if the specific intended use is not allowed.
- **No legal determination.** Regulatory applicability, certifications and contract suitability require situation-specific review by the user's appropriate advisers. This repository records documentary statements, not legal, clinical or security assurance.

The reviewer of a proposed trust assessment examines the exact linked sources and subject conditions; checks that researcher and independent reviewer are different, that material affiliations are disclosed/recused under [review policy](../../docs/REVIEW_POLICY.md), and that no unverified statement became an absolute claim. The receiving owner must separately accept display phrasing and field eligibility at an immutable revision; until then there is **no** approved public trust presentation.

## Corrections, vulnerabilities and responsible disclosure

For ordinary factual changes, use the repository correction template and [review/correction process](../../docs/REVIEW_POLICY.md); preserve the original claim and source history, recheck changed terms, and notify affected consumers through their accepted receiving procedure *only when such a procedure exists and messaging is authorized*. No automated notifications are enabled by this proposal.

For suspected vulnerabilities, accidental credentials, exploit details, private reports or customer data, **do not** place details in public issues, PRs, files, examples or logs. Follow [SECURITY.md](../../SECURITY.md) and the established private disclosure route; freeze publication of sensitive material pending authorized handling. This method authorizes no live scans, adversarial testing or contacts.

## Handoff and acceptance state

Intake and presentation method: **proposed** at this revision. Real product assessments, source visits, non-author approval, rights decisions and receiving-owner acceptance: **not performed by this document**. Research #41 owns shared rights policy; website and catalog-pipeline owners decide their own bounded display/ingestion interfaces as in [HANDOFFS](../../docs/HANDOFFS.md). Do not mark #75, #110 or #111 complete from file existence or CI alone.
