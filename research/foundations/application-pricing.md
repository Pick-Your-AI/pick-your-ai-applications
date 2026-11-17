# APP-F03.03 — application pricing and conditional total cost (proposal)

Issue: [#74](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/74); children [#108](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/108) (offer/meter) and [#109](https://github.com/Pick-Your-AI/pick-your-ai-applications/issues/109) (comparisons). Recorded 2026-11-17. **Status: proposed research method, not accepted product pricing, a verified market survey or a production cost engine.** Research #39 remains the shared cost-semantics owner; do not alter research's frozen builder `contracts/v1`.

## Decision and existing contracts

The consumer asks: *what would I pay for a particular application offering, under my actual seat, usage, region, commitment and BYOK/BYOM conditions, and which components cannot be priced from the available evidence?*

The authoritative local `0.1.0` structures are [`schemas/pricing.schema.json`](../../schemas/pricing.schema.json), [`schemas/pricing-record.schema.json`](../../schemas/pricing-record.schema.json) and [`docs/APPLICATION_CONTRACT.md`](../../docs/APPLICATION_CONTRACT.md). A standalone `data/pricing/*.json` observation is tied to an existing `app:` identity and exactly one declared `offering:`, contains an evidence-bearing pricing claim, rights decisions and a separate publication manifest. An embedded application pricing claim is an alternative; do not count the same observation twice. All claims and terms are scoped to their documented product/plan/version/region/platform/currency and actual checked/effective dates.

The existing pricing value captures `offering_id`, `plan_name`, `amount_status`, `amount`, `currency`, `regions`, `billing_period`, `meter`, `commitment`, `tax_treatment`, `minimum_seats`, `included_allowance`, `overage_terms`, `promotion_conditions` and `effective_on`. An amount is a decimal **string**, not a float. `amount_status: known` with `amount: "0"` represents only a *sourced, scoped zero charge*; `unknown`, `contact_sales` or `custom` require `amount: null`. Missing currency, an unpublished quote or unreported tax is not zero. An Enterprise label is not an entitlement or a price.

## Pricing observation types and what cannot be inferred

| Commercial form | Minimum observation | Critical unknowns to preserve |
| --- | --- | --- |
| Subscription | Charge, currency, time basis, billed/renewal period, applicable seats and plan scope | Whether billed annually, prepaid, commitment length, mid-term cancellation and taxes |
| Per-seat / per-user | Seat definition, minimum seats, unit price and billed period | Active vs named seats, annual true-up, guest charges and volume bands |
| Credits / pooled capacity | Purchased credits, currency, validity, included allowance and exact **source-defined** debit units | Conversion of one credit to tokens, messages or requests, per-feature debits, shared-pool exhaustion, rollover and refunds |
| Metered consumption | Unit, rate, billing increment, allowance, overage/tiers and measurement scope | Overages, burst/peak rules, min spend and vendor vs underlying model meter |
| Outcome / transaction | Precisely defined billable event, charge, eligibility and dispute/return rules | Refund/reversal treatment, attribution, minimum billing and invalid-event handling |
| Trial / promotional | Trial length, eligible population, start/end trigger, promotional price and subsequent ordinary price | Card requirement, auto-conversion, renewal, cancellation timing and access after expiry |
| Bundle / add-on | Product/feature inclusions, independent fee and whether charges stack | Which features or limits are excluded, license/seat bundling and upgrade or downgrade impacts |
| Enterprise quote / custom | Exact offering identity, `contact_sales`/`custom`, source/check date and requested quote fields | **All unquoted monetary values**; never derive a number from plan name or comparable vendors |
| BYOK / BYOM or externally metered provider | Which encryption key, model endpoint or API key the customer brings and which party bills each unit | Separate provider/API usage, token/call volume, egress, hosting, support and vendor add-on charges |

A trial, temporary promotional tier, free allowance, free-to-start account, free software license and a permanently zero-priced paid-equivalent subscription are distinct propositions. Record each without turning one into another. Open-source license terms are not proof of zero operating or hosting cost.

If one provider includes credits that cover different modalities or models, log *each published conversion* separately. A product page saying "1,000 credits" without a conversion table does not support normalizing credits to dollars per request, tokens, images or minutes. A single shared meter cannot be converted from another product's model/runtime assumptions; keep its normalized cost **unknown** and flag a receiving question to research #39.

## Conditioned evidence checklist

A researcher must identify **actual** dated primary material for each populated fact, not a generic product homepage or secondhand aggregator. Log the source URL, publisher, checked date, effective date or version of the pricing terms, source access outcome and known update/correction history. Tie evidence to the exact offering, region, currency, applicable sales channel, price unit and tax/discount conditions. Validate the original source's permission for each intended display/cache/export/API/commercial use separately under [source-use and publication policy](../../docs/APPLICATION_CONTRACT.md); publicly accessible price pages do not grant bulk copying rights.

For each applicable offering, record these questions in its claim evidence or incomplete research notes:

- **Price and terms:** Is the charge base, seat minimum, invoice period, commitment, renewal type, promotion eligibility and upgrade/downgrade treatment stated? Are charges pre- or post-tax and is a region/currency exchange assumed?
- **Quota and usage:** Are included units, usage window, resets, pooled/individual credits, add-ons, overage tiers, burst behavior and expiry/rollover/refunds stated? Identify who publishes the meter and whether product usage differs from provider usage.
- **Trial and cancellation:** How is trial start triggered; is a card required; does it auto-convert; what are cancellation deadlines, renewal terms, refundable balances or charges, and access/deletion at expiry? **Unknown** is an acceptable outcome when these terms are not available.
- **External dependencies:** When an app uses a separately priced model/API, does a user pay the app, the model provider, a cloud host or several parties? Mark BYOK/BYOM external costs unquantified unless applicable, source-linked rates and compatible units are actually observed.
- **Risk and change:** Note potential transfer fees, data egress, hosting, seat true-ups, minimum bills, taxes and third-party support; date the observation and identify conditions that would trigger a new check. An old price is a dated price, not a forecast or a current guarantee.

For source access failures, missing rates, restricted or individualized quotes, note the **attempt and limitation**, not a fictional check date or a false `unsupported` status. A verified, actually read primary source is `source_status: checked` but still `verification_status: unverified` absent independent evidence. Independent price testing is distinct from documenting a vendor's rate sheet. No actual vendor pricing has been checked for this proposal.

## Calculation contract for comparisons (proposed, not yet an implemented validator)

Make assumptions first; do not silently compute a universal "monthly cost" from unrelated plans. Each comparison scenario declares:

1. **Workload and eligibility:** user role, region, currency, platform, seat count/type, term length, model/provider choice, expected usage by *original published meter*, and plan eligibility.
2. **Input price observation IDs and dates:** source IDs, actual check/effective dates, relevant offering IDs and exact unit prices with rate tier/billing treatment; explicitly flag a quote requirement.
3. **Arithmetic:** use decimal arithmetic for money. For a seat-based subscription with a source-supported minimum, `billable_seats = max(requested_seats, minimum_seats)`; `base = unit_price_per_billing_period × billable_seats × number_of_billing_periods`. An annual discount is an alternative plan rate, not twelve times an unverified monthly rate.
4. **Usage:** calculate overage **only** if allowance, conversion, rate schedule and time-window semantics are sourced and in compatible units. For a simple published flat meter, `overage = max(0, billable_units - included_units) × observed_overage_rate`. Tiered/pooled meters require the documented actual allocation and tier rules instead of this shortcut.
5. **Separated cost buckets:** identify base subscription, minimum/seat true-up, vendor usage, vendor add-ons, external model/provider/API fees, deployment/hosting, egress, support and tax. An absent bucket is **Unknown**, not `0`, unless actual evidence establishes no charge.
6. **Scenario result:** show subtotal of *priced buckets*, unpriced buckets, calculation date, each source condition, eligibility caveats, any estimates and assumptions. Do not label a partial subtotal "total cost". If a required bucket is unknown, a comprehensive TCO is **not calculable**; it is not a point estimate, a zero or a comparable score.
7. **Review and receiving:** require a non-author exact-revision calculation review; the research #39 cost owner and actual downstream consumers must resolve shared normalization or projections before accepted cross-repository semantics are claimed.

**Synthetic arithmetic illustration, not product data or source evidence:** suppose a fictitious offering requires 3 seats at 20 fictitious currency units per seat per month for 12 months. It documents 500 included requests per month and 0.02 units per additional request, with a steady 1,000 requests each month. In that *invented test scenario* the base is `3 × 20 × 12 = 720`, the overage is `(1,000 - 500) × 0.02 × 12 = 120`, and the **priced-bucket subtotal** is `840` units for the 12 months. Taxes, provider API usage, add-ons, refunds and hosting remain **Unknown**, so a full TCO and a market price are **not** established. If the published allowance were per user rather than per workspace, the arithmetic would change; do not apply this calculation without that distinction.

**Additional synthetic seat/term contrast:** 2 requested seats under a fictitious minimum of 5 seats at an independently sourced-in-the-hypothetical annual charge of 18 units per billable seat per month gives `5 × 18 × 12 = 1,080` units, *not* 2 × 18 × 12. It is invalid to compare that amount directly with an offer whose usage, features, eligibility and taxes are unknown. Both numbers are purely invented to exercise the comparison method; neither is an observation of a real seller.

## Limitations, schema follow-ups and receiving questions

The live local `0.1.0` pricing schema is an **observation**, not a complete billing engine. In particular it has no typed fields for trial auto-conversion, recurring renewal/cancellation/refund terms, credit unit conversions and rollover, tier schedules, seat definitions, BYOK/BYOM pass-through charges or multiple external-billing parties. Do not stuff invented uniform units into `meter` or invent a zero rate to make this shape pass. Keep actual source language in scoped notes until a separately reviewed and versioned schema/validator extension is accepted. Do **not** change this application's `0.1.0` pricing schema or the frozen research builder contract in this documentation PR.

Explicit decisions required before adopting a shared normalized bill/price schema:

- **research #39:** canonical price/currency/unit/term semantics, conversion and meter ownership, precision and rounding, promotion/discount precedence, external provider double-counting and the meaning of unknown partial TCO;
- **APP-F03.01 / rights owner:** permissions for exact price/source fields and intended uses, including copies of terms or tables;
- **catalog-pipeline and website owners:** acceptance of the application-specific `pricing-record.schema.json` envelope, conditional display and unavailable-quote/Unknown presentation; a technical readback is not an acceptance receipt.

## Acceptance accounting

This document proposes the missing APP-F03.03 method and **partially addresses #108/#109**. The two `0.1.0` schemas already exist on the baseline; no schema/version/validator modification, checked market rate, actual external price access, numerical product claim, consumer acceptance, rights grant or implementation runtime test is included. The synthetic arithmetic is explicitly hypothetical and does not increase product counts. Keep #74, #108 and #109 **open** until a non-author exact-revision review and each issue's full acceptance and genuinely required receiving decisions are documented.

Relevant local policies: [contributor instructions](../../CONTRIBUTING.md), [research workflow](../../docs/RESEARCH_WORKFLOW.md), [review/admission policy](../../docs/ADMISSION_POLICY.md), [source rights](../../THIRD_PARTY_RIGHTS.md), [research identity/evidence](../../docs/APPLICATION_CONTRACT.md).
