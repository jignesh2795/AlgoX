# PX-2026-030 — Equity-derivatives margin calculation, collection and risk controls

**Research date:** 2026-11-08  
**Status:** official-source review completed; implementation contract remains open  
**AlgoX area:** Indian derivatives risk / margin engine / client collection / clearing reconciliation  
**Scope:** NSE Clearing equity derivatives, SEBI margin-verification and collection framework, Kite/Upstox/Dhan margin APIs  
**Inputs:** PX-025 requirements baseline, PX-028 account reconciliation, PX-029 expiry/physical-settlement lifecycle  
**Mode:** research and requirements specification only  
**Non-goals:** no broker account/API access, sandbox/production request, order, code implementation, paid service, legal advice, PR or merge to `main`

## Executive finding

Indian equity-derivatives margin is not one static percentage or one broker “available margin” number. It is a time-varying, portfolio-based requirement with distinct calculation, collection, reporting and settlement layers.

The reviewed official sources establish the following:

1. **SPAN / initial margin is portfolio-based.** NSE Clearing performs online intraday margining using SPAN. Its published methodology describes 99% VaR over a one-day horizon, with a two-day horizon for futures where the MTM settlement value may not be collected before the next market opens.
2. **ELM is separate and parameterized.** It has product- and position-sensitive rules, including deep-OTM, long-dated and expiry-day adjustments. Current published percentages are a parameter snapshot, not constants to hard-code into an historical or future margin engine.
3. **Upfront client collection includes SPAN/IM and ELM before trade.** From 1 February 2025, equity-derivatives upfront collection also includes net option premium payable at client level.
4. **Peak-margin verification is not the same as live clearing margin computation.** SEBI's fixed Beginning-of-Day (BOD) parameter rule is specifically for verifying client upfront collection. Clearing-corporation margin parameters continue to update intraday and at EOD for actual clearing obligations.
5. **Margins are netted within the individual client, not across clients.** Client positions are netted per client and grossed across clients at TM/CM level with no cross-client set-off. Proprietary positions are separate from client positions.
6. **Delivery and consolidated crystallized obligation margins have their own lifecycle.** NSE Clearing's equity-derivatives margin page expresses initial margin as Total SPAN + Delivery Margins + margins on consolidated crystallized obligations. ELM and the post-2025 upfront net-option-premium collection requirement must also be represented separately in the total risk/collection view.
7. **F&O client collection timing is distinct from the April 2025 cash-segment change.** NSE's current F&O member FAQ states SPAN/ELM are collected before trade and delivery margin plus consolidated crystallized obligation collected by T+1. SEBI Circular 2025/57 changes the timeline for non-upfront margins in the cash segment to settlement day. Do not generalize the cash-segment circular into a replacement F&O collection rule.
8. **Margin must be reconciled as required, available, collected, reported, utilized and released.** A calculator output or funds snapshot does not prove that the corresponding client margin was actually collected. NSE explicitly describes reporting uncollected/short-collected margin as collected as false reporting.

**Research decision:** any future AlgoX margin service must keep the clearing requirement, client-level upfront/peak verification obligation, broker calculator estimate, actual collateral/cash collected, margin shortfall, member-level collateral and settlement-triggered release as distinct values with their own source, timestamp and effective rule version.

## 1. Official evidence and regulatory scope

### 1.1 NSE Clearing's equity-derivatives margin framework

NSE Clearing states that:
- actual margining is performed online on an intraday basis using the SPAN portfolio-based system;
- initial margin is collected upfront on open positions through the clearing-member → trading-member → client chain;
- initial margin is based on 99% VaR over one day, except the stated two-day futures horizon where MTM settlement may not be collected before the next day's market;
- client positions are netted at individual-client level and grossed across clients, without set-offs between clients;
- proprietary positions are netted at TM/CM level separately, without client/proprietary set-offs;
- SPAN parameters are specified from time to time;
- the page expresses initial margin as total SPAN + delivery margin + margin on consolidated crystallized obligations;
- the ELM schedule varies by product and position characteristics;
- consolidated crystallized obligation (CCO) is calculated intraday and at EOD from different inputs;
- MG09–MG15 reports expose different CM, TM, client and cross-margin views.

Source:
- https://www.nseclearing.in/risk-management/equity-derivatives/margins

### 1.2 SEBI upfront collection and peak-margin verification

The SEBI Exchange Traded Derivatives chapter in the December 2024 master-circular document, at clauses 14.3–14.4, establishes:
- upfront margin must be collected in advance of trade;
- Clearing Corporations send a minimum of four client-wise snapshots per day in randomly selected time windows;
- reports include EOD client margin requirement and peak obligation across the intraday snapshots;
- EOD and intraday client margin collection verification in derivatives uses fixed BOD margin parameters;
- this BOD rule is **only for verification of upfront collection**; Clearing Corporation margin parameters for actual collection obligations continue to update intraday and EOD;
- in the equity-derivatives segment, from 1 February 2025, upfront collection includes net options premium payable at client level in addition to IM and ELM.

Source:
- https://www.sebi.gov.in/sebi_data/commondocs/dec-2024/RE_Chapter%205%20-%20Exchange%20Traded%20Derivatives%20FINAL_1_p.pdf

The source describes both the client verification methodology and the actual Clearing Corporation calculation process. Those purposes must not be conflated. A BOD-parameter client-verification snapshot is not a statement that the live clearing margin remained fixed at the BOD parameter set.

### 1.3 F&O client collection timelines and false reporting

NSE's current FAQ for Margin Collection and Reporting says:
- F&O SPAN and ELM are to be collected from respective clients upfront, before trade;
- delivery margin and margin on consolidated crystallized obligation are to be collected from clients by T+1 day;
- where margin (including upfront and consolidated crystallized obligation/MTM) has not actually been collected or has been short-collected but reported as collected, this is false reporting to the Clearing Corporation.

Source:
- https://www.nseindia.com/static/trade/members-faqs-margin-collection-and-reporting

**Important scope boundary — SEBI Circular 2025/57:** this circular is titled “Timelines for collection of Margins other than Upfront Margins – Alignment to settlement cycle” and modifies the cash-segment collection timeline in the Stock Brokers Master Circular. It requires non-upfront cash-segment margins by settlement day in light of T+1 cash settlement. It does not replace the separate F&O T+1 client collection statement in the NSE F&O FAQ.

Sources:
- SEBI Circular 2025/57 (28 April 2025): https://www.sebi.gov.in/legal/circulars/apr-2025/timelines-for-collection-of-margins-other-than-upfront-margins-alignment-to-settlement-cycle_93685.html
- NSE Circular NSE/INSP/67739 (29 April 2025): https://nsearchives.nseindia.com/content/circulars/INSP67739.pdf

### 1.4 ELM and other additional risk parameters are time-sensitive

The NSE Clearing margin page, updated 9 March 2026, publishes a current ELM schedule. Its displayed values include 2% of notional for index derivatives and 3.5% for stock derivatives, with stated exceptions/adjustments including:
- 3% for specified deep-OTM short index options;
- 5% for short index options with residual maturity over nine months;
- 5.25% for specified deep-OTM short single-stock options;
- additional 2% ELM on short index options due to expire that day;
- additional margins for certain highly volatile stocks;
- calendar-spread and near-expiry treatment that differs between index and individual-security futures.

These rates and conditions are evidence of a parameterized rule set, not fixed source-code constants. The effective-date source and applicable SPAN/ELM parameter files must be pinned for each valuation/snapshot.

Source:
- https://www.nseclearing.in/risk-management/equity-derivatives/margins

### 1.5 Margin reports and clearing-member liquidity

NSE Clearing documents:
- **MG09:** CM margin summary, including initial, premium, intraday crystallized MTM, delivery, total and assignment margin;
- **MG10:** TM/CP margin summary;
- **MG11:** CM margin payable statement and deposits;
- **MG12:** detailed CM file with TM/CP, SPAN, ELM, delivery, CCO, total and peak intraday margin;
- **MG13:** client-level file with SPAN, ELM, delivery, CCO, total, peak intraday margin and client/proprietary flag;
- **MG14/MG15:** CM/TM cross-margin benefit reports.

The MG12/MG13 descriptions state that the margin values are based on EOD positions and BOD margin parameters. The files therefore must be interpreted according to their reporting purpose and not substituted for every intraday clearing obligation.

The same page says that at least 50% of Clearing Members' effective deposits must be in the defined cash component. This is a **Clearing Member collateral/liquidity rule**, not a blanket instruction that every retail client must maintain 50% of their own margin as cash. Preserve CM-level collateral requirements separately from client collection requirements.

Source:
- https://www.nseclearing.in/risk-management/equity-derivatives/margins

## 2. Margin components and lifecycle

The following is a taxonomy of separately sourced obligations. It is not a universal additive formula; the applicable Clearing Corporation/broker statement defines which components apply and how recognized benefits are applied.

| Component | Meaning in the reviewed sources | Lifecycle / key caution |
|---|---|---|
| SPAN / initial margin | Portfolio risk requirement on open positions, based on SPAN scenarios/parameters | Recompute on portfolio changes and refreshed clearing parameters; not a fixed per-order percentage |
| ELM | Additional loss coverage under exchange/clearing rules | Parameterized by product, position, maturity, moneyness, expiry and volatility rules |
| Net options premium payable | Net client-level premium payable from option purchases after eligible premium offsets | Included in equity-derivatives upfront collection from 1 Feb 2025 |
| Delivery margin | Margin for physical delivery exposure approaching/at expiry | Time-bounded expiry-to-settlement/early-pay-in lifecycle; link to PX-029 |
| Tender margin | Broker/API field used for applicable near-expiry futures contracts | Preserve provider-specific meaning and effective rules; do not universalize from one broker field |
| Margin on consolidated crystallized obligation | Intraday/EOD payable obligation at client level | Intraday: closed-futures crystallized P&L plus net premium; EOD adds futures MTM, options premium, exercise/assignment and futures final settlement |
| Assignment margin | Reported separately in CM margin summaries and relevant option-expiry risk | Link to exercise/assignment outcome and the relevant settlement evidence |
| Additional/special margin | Volatility, concentration or other exchange/broker prescribed add-on | Source, instrument, period and rule must be stored; not inferred from a generic “additional” field |
| Cross-margin / hedge benefit | Recognized offset benefit under a defined exchange rule | Must be tied to eligible positions, account/client scope, expiry rules and applicable parameter set |
| Margin release | Release of a previously required/collected obligation | Must follow source-confirmed settlement/closeout/release condition; order cancellation alone is insufficient |

### 2.1 SPAN is portfolio-based, not order-isolated

NSE Clearing describes SPAN as portfolio-based. It calculates client margin after netting positions within the same individual client. The requirement is then grossed across clients at member level without offsetting one client's risk with another client's excess margin. Proprietary positions are netted separately.

The practical implication is that a new order's incremental margin depends on:
- existing positions;
- open orders;
- all eligible legs of the same client's portfolio;
- contract/expiry and product identity;
- effective SPAN/ELM parameters;
- current cross-margin/hedge eligibility;
- whether a hedge leg is being closed, expired or converted into delivery exposure.

A calculation made for each leg independently can overstate or understate the basket's actual incremental requirement. A gross member-level total must not be allocated to a client without the client-level source report.

### 2.2 Margin on consolidated crystallized obligation (CCO)

NSE Clearing describes CCO separately at intraday and EOD:

- **Intraday:** calculate net client-level payable/receivable from premium payable/receivable and futures crystallized profit/loss on closed-out futures, using weighted-average trade prices. A net payable amount becomes intraday CCO margin.
- **EOD:** calculate the payable/receivable amount from futures MTM, options premiums, option exercise/assignment for expired contracts and futures final settlement. A net payable becomes EOD CCO margin.
- CCO margin is released on completion of settlement.

This is not the same as SPAN/ELM, not the same as total broker funds utilization, and not an order fee.

### 2.3 Hedge breaks, expiry and calendar-spread changes

Margin can rise sharply without a new order when:
- a client closes one leg of a spread;
- a hedge expires or ceases to qualify;
- expiry-day calendar-spread benefits are withdrawn under the effective rule;
- a portfolio moves into physical delivery/assignment exposure;
- volatility or an ELM/additional-margin parameter changes.

The NSE member FAQ explicitly discusses short/non-collection penalty cases attributable to a client when a hedge breaks or one leg expires, provided the broker has informed clients of such potential situations in its risk-management policy.

The SEBI Circular 2024/132 also removed calendar-spread treatment on expiry day for contracts expiring that day, effective 1 February 2025. The exact present rule and correlated-index/cross-margin interaction must remain date-effective rather than being inferred from a generic “spread benefit” field.

Sources:
- https://www.nseindia.com/static/trade/members-faqs-margin-collection-and-reporting
- https://www.sebi.gov.in/sebi_data/commondocs/dec-2024/RE_Chapter%205%20-%20Exchange%20Traded%20Derivatives%20FINAL_1_p.pdf

## 3. Collection, verification, reporting and available funds are different facts

A future AlgoX account/margin ledger must distinguish:

1. **Required margin:** sourced from the applicable Clearing Corporation/broker calculation for a particular account/portfolio and parameter timestamp.
2. **Client upfront collection requirement:** the amount that must be available before trade under the effective rules (including net option premium payable from 1 February 2025).
3. **Peak/EOD verification requirement:** the amount used to verify client collection and report a shortfall, using the prescribed BOD snapshot parameters where applicable.
4. **Actual collected margin:** cash/collateral actually received/blocked from that client and held in the broker's records.
5. **Available collateral/funds:** eligible assets and cash after applicable haircut, encumbrance and source-specific limits.
6. **Margin utilized/blocked:** the amount currently allocated to open positions, open orders or crystallized obligations.
7. **Shortfall:** required collection minus verified eligible amount actually available/collected, according to the applicable rule.
8. **Reported collection:** the amount the member reports to the Clearing Corporation. This is an assertion that must be supported by the actual books/ledger.
9. **Release:** the amount returned/unblocked once the relevant obligation has been settled or released under the applicable rule.

A margin calculator saying “sufficient balance” does not establish that funds were collected and reported correctly. A funds endpoint showing an available balance does not prove that it was reserved for the required client obligation. A reported collection amount must never be generated from the required margin number itself.

## 4. Broker margin API comparison

These are broker API calculation/availability surfaces, not replacements for authoritative NSE Clearing parameter files, client margin statements, actual collected-collateral evidence or settlement records.

### 4.1 Zerodha Kite Connect

Kite documents:
- `POST /margins/orders`: returns margin fields for each order considering existing positions and open orders;
- `POST /margins/basket`: calculates spread/basket margins, with a `consider_positions` option;
- response components include SPAN, exposure, option premium, additional, BO, cash, VAR, P&L and charges.

The API is useful for pre-trade and incremental basket estimation. Its results are still broker API calculations for the request/context; they are not a Clearing Corporation MG13 file or proof of client margin collection.

Sources:
- https://kite.trade/docs/connect/v3/margins/

### 4.2 Upstox

Upstox's `POST /charges/margin` accepts instrument keys, quantity, transaction side and product; the page documents a maximum of 20 instruments per request.

The response can include:
- `span_margin`;
- `exposure_margin`;
- `equity_margin`;
- `net_buy_premium`;
- `additional_margin`;
- `tender_margin`;
- `total_margin`, `required_margin` and `final_margin`.

The documented field descriptions identify tender margin as applying as a futures contract approaches expiry, and net buy premium as option premium required. This is a broker API calculation for the supplied request; it does not itself prove the final exchange-clearing obligation or actual client collection.

Source:
- https://upstox.com/developer/api-documentation/margin/

### 4.3 DhanHQ

Dhan publishes:
- `POST /margincalculator`: margin requirement for an order, with SPAN, exposure, variable margin, available balance, insufficient balance and brokerage fields in the documented example;
- `POST /margincalculator/multi`: multi-order margin calculation, with flags to include existing positions and open orders;
- `GET /fundlimit`: available balance, SOD limit, collateral, receivable, utilized amount, blocked payout and withdrawable balance.

The multi-order calculator can return total, SPAN, exposure, equity/F&O margin and hedge-benefit fields. These are broker API values with provider-specific semantics. They must not be equated with the exchange's official margin statement, actual collection ledger or released collateral.

Source:
- https://dhanhq.co/docs/v2/funds/

## 5. Proposed margin event and evidence model

This is a requirements-level decomposition, not a finalized schema or state enum.

A margin obligation should preserve:
- broker/account/client identity;
- proprietary/client flag and TM/CM/CP mapping where relevant;
- exchange, segment and contract/instrument identity;
- portfolio/position/open-order set used in calculation;
- component type (SPAN, ELM, net premium, CCO, delivery, assignment, tender, additional, cross-margin benefit);
- gross requirement, eligible offset/benefit and net requirement as separate values;
- amount, currency and raw numeric precision;
- parameter-set name/version, effective time and source file/reference;
- BOD, intraday snapshot, EOD or settlement context;
- calculation timestamp and the position/market-data watermark;
- client collection deadline and relevant settlement calendar;
- actual collected funds/collateral evidence, haircut and encumbrance;
- shortfall/reporting status and the submitted report reference;
- release condition, release event and actual return/unblock evidence.

Candidate event lifecycle:
`MarginParametersPublished` → `MarginRequirementCalculated` → `ClientUpfrontCollectionRequired` → `FundsOrCollateralCollected` → `MarginBlockedOrAllocated` → `MarginSnapshotObserved` → `IntradayRecalculation` / `EODReconciliation` → `SettlementObligationFinalized` → `MarginReleaseConfirmed`.

Exception paths include:
- `MarginParameterMissing`;
- `MarginCalculationStale`;
- `PortfolioScopeIncomplete`;
- `HedgeBenefitRevoked`;
- `MarginShortfall`;
- `CollectionEvidenceMissing`;
- `FalseCollectionReportingConflict`;
- `CollateralHaircutOrEligibilityConflict`;
- `MarginReleaseUnconfirmed`.

No negative/zero fallback is permitted when the applicable margin parameter, portfolio component or client collection evidence is missing.

## 6. Requirements refinements to PX-025

The existing PX-025 requirements R-025 (fail-closed exposure), R-039/R-041/R-044 (positions, cash and funds), R-049–R-061 (expiry and delivery) remain in force. PX-030 adds:

### R-062 — Margin parameters are source-versioned and effective-dated

Every margin calculation MUST retain the exact exchange/clearing parameter-set identity, source/reference file, effective timestamp/date, market snapshot and applicable contract-master version. A current SPAN/ELM rate MUST NOT be applied retrospectively to historical positions.

### R-063 — Portfolio-based margin is not per-order isolation

Margin calculation MUST account for all in-scope positions and eligible open orders of the same client, product and account. It MUST preserve per-client netting and the resulting member-level gross total separately. A standalone per-order estimate MUST NOT be represented as the client's complete portfolio margin unless the source calculation explicitly includes the relevant portfolio.

### R-064 — Upfront collection includes applicable client net option premium

For equity-derivatives trades on and after 1 February 2025, the upfront collection/verification requirement MUST include net options premium payable at client level in addition to IM and ELM, using the effective SEBI/exchange definition. Historical trades MUST use the rule effective on their date.

### R-065 — BOD verification parameters differ from live clearing parameters

The system MUST distinguish the fixed BOD parameters used for client upfront-margin verification/shortfall assessment from the refreshed intraday/EOD parameters used by Clearing Corporations for actual clearing obligations. It MUST NOT treat a BOD verification snapshot as the live clearing requirement or assume clearing requirements remain static during the day.

### R-066 — No cross-client or client/proprietary margin set-off

The margin core MUST net positions only within the permitted individual-client scope and MUST NOT offset one client's excess margin against another client's requirement. Proprietary positions MUST remain separate from client positions. Any cross-margin benefit MUST be traceable to the applicable approved framework, client and eligible position set.

### R-067 — Margin components remain separately attributable

SPAN/initial, ELM, net option premium, CCO, delivery, assignment, tender, additional/special, cross-margin benefit, collected collateral, utilization, shortfall and release MUST be represented separately. A single total may be derived, but the component inputs and source rules MUST remain auditable.

### R-068 — Basket/hedge benefits are conditional and revocable

A spread or hedge benefit MUST be calculated from the complete eligible portfolio using the effective exchange rules. Closing, expiry, exercise, corporate action or other loss of a hedge leg MUST trigger a fresh margin evaluation. The previous basket result MUST NOT be carried forward after its supporting position set changes.

### R-069 — Expiry and delivery margin link to settlement lifecycle

Delivery, tender and assignment margin MUST retain the expiry/settlement date, applicable contract family, delivery mode, assessment/release period and source rule. Margin must be recalculated when a contract enters the tender/delivery/assignment window. This requirement links to PX-029 physical-settlement obligations.

### R-070 — CCO is distinct intraday and EOD evidence

Intraday CCO MUST use the documented client-level closed-futures crystallized P&L and payable/receivable premium inputs. EOD CCO MUST preserve the additional futures MTM, options premium, option exercise/assignment and futures final-settlement inputs. The two calculations MUST NOT be collapsed into an unexplained daily total.

### R-071 — F&O collection deadline is segment-specific

For the reviewed NSE F&O member FAQ, SPAN/ELM MUST be collected before trade; delivery margin and CCO MUST be collected by T+1 day. The cash-segment settlement-day change in SEBI Circular 2025/57 MUST NOT be generalized into an F&O collection rule. The exact current effective rule and trading/settlement calendar must be checked for the relevant segment and date.

### R-072 — Required margin and actual collected margin are separate records

The system MUST retain the amount required, amount available, amount actually collected/blocked, amount reported, collection timestamp, collection instrument/source and any shortfall separately. It MUST NOT derive “collected” from “required” or a margin calculator response.

### R-073 — Peak-margin snapshots are preserved with purpose and parameters

Every intraday snapshot MUST retain its capture window/time, client scope, reported component values and verification parameter set. The system MUST preserve EOD and peak-across-snapshot values separately. Snapshot count/selection and reporting rules must be date-versioned.

### R-074 — Margin release follows confirmed obligation settlement

Delivery/CCO/assignment/other margin MUST remain allocated until the effective release condition has been met and confirmed by authoritative settlement/clearing/broker evidence. Order cancellation, position flattening, early-pay-in initiation or a broker display change alone MUST NOT prove the corresponding margin release.

### R-075 — Collateral eligibility and member-level liquidity remain distinct

Collateral type, ownership/client allocation, encumbrance, applicable haircut, eligible value and liquid-cash classification MUST be preserved independently. Clearing-member deposit composition requirements (including the published 50% cash-component rule) MUST NOT be misapplied as a universal client cash percentage. Client collateral segregation/eligibility must follow its own effective rules.

### R-076 — Margin shortfall and reporting conflict fail closed

An unmet upfront requirement, a T+1 shortfall, unavailable collateral, missing client allocation, stale calculation or mismatch between actual collections and reported collections MUST remain an explicit risk exception. The system MUST NOT permit a new position on the assumption that an uncollected or unverified amount is available, and MUST NOT fabricate a collection record to satisfy reporting.

## 7. Additional deterministic acceptance scenarios

The following extend AT-001 through AT-100. Use deterministic synthetic portfolio, BOD/ intraday/EOD parameter and fake clearing/broker evidence only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-101 | SPAN/ELM input parameter set is missing or stale | Margin result UNKNOWN; no zero/default margin or order clearance |
| AT-102 | Existing same-client positions and open orders affect a new order's SPAN | Compute against the complete supplied portfolio context; record exactly which positions/orders were included |
| AT-103 | A two-leg spread receives a documented eligible hedge benefit | Record gross leg margins, eligible benefit and net requirement separately with the rule version |
| AT-104 | One hedge leg is closed, expired or becomes ineligible | Recompute the remaining portfolio margin; revoke unsupported prior hedge benefit |
| AT-105 | Client submits an order without upfront SPAN/IM and ELM collected | Block/reject pre-trade authorization; do not rely on post-trade collection |
| AT-106 | Equity-derivatives option buyer has net premium payable on/after 1 February 2025 | Include client-level net option premium in upfront collection and verification |
| AT-107 | Multiple option trades create offsetting premiums within one client | Calculate net payable premium at the client scope under the effective rule; do not sum all gross buy premiums |
| AT-108 | Client verification snapshot uses fixed BOD parameters while Clearing Corporation updates live parameters intraday | Preserve both values with purpose; do not label them contradictory or substitute one for the other |
| AT-109 | Four or more randomly selected intraday snapshots and an EOD margin report are supplied | Preserve each timestamped snapshot and independently derive peak and EOD verification requirements |
| AT-110 | Two clients have opposite/surplus margin positions | Do not set off one client's surplus against the other's requirement |
| AT-111 | Proprietary positions hedge client positions at member level | Keep proprietary and client risk/offset ledgers separate; no proprietary-to-client set-off |
| AT-112 | Basket margin estimate changes after a position or open order is added | Recalculate complete portfolio margin; preserve request context and before/after deltas |
| AT-113 | Kite margin API order response considers existing positions/open orders and basket API evaluates a spread | Preserve broker estimate and input scope; do not treat it as Clearing Corporation or collection evidence |
| AT-114 | Upstox margin response contains SPAN, ELM/exposure, net buy premium and tender-margin fields | Preserve each field separately; apply tender margin only according to its provider/effective contract definition |
| AT-115 | Dhan multi-order margin request includes existing positions and open orders | Record inclusion flags and complete scrip list; do not compare with a calculation that omits these inputs |
| AT-116 | Contract approaches expiry and delivery/tender/assignment margin becomes applicable | Recompute with date-effective expiry rules and link margin to settlement obligation |
| AT-117 | F&O upfront and T+1 collection timelines are evaluated | Require SPAN/ELM before trade; enforce current F&O T+1 collection for delivery/CCO; do not apply cash-segment 2025/57 settlement-day rule to F&O |
| AT-118 | Cash-segment non-upfront margin falls under SEBI Circular 2025/57 | Use settlement-day rule for the cash segment only; retain segment scope in the rule reference |
| AT-119 | Intraday CCO contains premium payable and crystallized futures loss | Compute/record intraday payable CCO at client level from the two documented inputs |
| AT-120 | EOD CCO includes futures MTM, premiums, expired option exercise/assignment and futures final settlement | Reconcile each component before classifying EOD CCO payable/receivable |
| AT-121 | Short index option due to expire incurs additional expiry-day ELM under the effective parameter set | Apply the dated rule to all eligible open and newly initiated due-to-expire positions; never hard-code it across all historical dates |
| AT-122 | Member reports required margin as collected but collection ledger has no matching client cash/collateral evidence | FALSE_COLLECTION_REPORTING_CONFLICT; block PASS and preserve the missing/short collection evidence |
| AT-123 | Approved collateral is present but after haircut/encumbrance its eligible value is below requirement | Calculate eligible value using dated haircut/eligibility; record shortfall rather than nominal face value |
| AT-124 | Delivery/CCO margin remains blocked after order cancellation but settlement is not complete | Keep margin allocated until the documented settlement/release condition is evidenced |
| AT-125 | Clearing member satisfies its 50% cash-component effective-deposit rule using CM-level deposits | Validate at CM level only; do not translate it into a blanket 50% retail-client cash requirement |
| AT-126 | SPAN parameters update intraday while a broker calculator returns a value from an earlier timestamp | Store both parameter timestamps; classify stale estimate and recalculate before risk clearance |
| AT-127 | Current published ELM rates differ from the rate applicable to a historical trade date | Use the historical effective parameter file; never back-apply the current website table |
| AT-128 | Expiry-day calendar-spread benefit is withdrawn under the applicable rule | Recalculate margin without the expired benefit and preserve the triggering expiry/rule evidence |
| AT-129 | A margin shortfall is detected but the collection/reporting API is unavailable | Keep shortfall unresolved and fail closed; do not assume collection or emit a synthetic success |
| AT-130 | Settlement is completed and clearing/broker evidence confirms margin release | Release only the confirmed amount; retain the release event, linked obligation, timestamp and source reference |

PX-025 now contains **76 normative requirements (R-001–R-076) and 130 proposed acceptance scenarios (AT-001–AT-130)**. These new scenarios are proposed for future fake-provider/fake-clearing tests only; no test or broker API was run.

## 8. Open questions

1. Which current NSE Clearing SPAN risk-parameter and ELM files should be the canonical inputs for each segment/date, and how are effective timestamps and intraday revisions identified?
2. What precise UDiFF/MG report versions and fields expose SPAN, ELM, net option premium, delivery, assignment, CCO, peak margin, actual collected client margin and release for each member role?
3. How do current broker APIs map every exchange component (especially CCO, assignment, expiry-day ELM and special/additional margin) into their own calculator response?
4. What exact collection modes, haircut/encumbrance rules and client-level segregation evidence are accepted for each collateral type under the current framework?
5. Which exact risk state causes a broker's RMS to block new orders, square off, or restrict positions when a client misses upfront/T+1 margin?
6. How do margin obligations/release behave during physical settlement, auction, corporate action, special expiry or holiday extensions?
7. How are client-level net option premium and spread/cross-margin offsets calculated where multiple products, expiries or correlated indices are involved?
8. Do provider calculator APIs expose the parameter version/timestamp and a complete portfolio snapshot ID? If not, how can a result be marked stale or incomplete?
9. What are the current amendments after the 2024 master-circular chapter and 2025/57 that affect F&O upfront, client verification, collection timing or collateral segregation?
10. What is the exact current interpretation of F&O T+1 client collection timing for exceptional settlement calendars and payment instruments?

All remain OPEN/UNKNOWN unless answered by the applicable circular, current clearing specification or provider contract. No broker API experiment is authorized or required by this research record.

## 9. Research decisions and non-authorization

- **ACCEPT:** SPAN, ELM, net option premium, CCO, delivery, assignment, tender, additional margin, cross-margin benefit, actual collection, shortfall and release are distinct auditable dimensions.
- **ACCEPT:** BOD client-verification parameters and refreshed live clearing parameters are different views with different purposes.
- **ACCEPT:** client margin is netted within the individual client; no cross-client or client/proprietary set-off is inferred.
- **ACCEPT:** SPAN/ELM and applicable net option premium are upfront; F&O delivery/CCO collection follows its separate T+1 client rule in the current NSE FAQ.
- **ACCEPT:** the cash-segment 2025/57 settlement-day change is not generalized to F&O.
- **ACCEPT:** false reporting of uncollected/short-collected margin as collected is a separate compliance exception.
- **DEFER:** production margin formula, exact parameter ingestion, cross-margin engine, client collateral ledger, collection orchestration, risk action thresholds and clearing report parser.
- **NOT AUTHORIZED:** broker/clearing connections, sandbox/production calls, real orders, code changes, paid data/services, credential/IP changes, PR or merge to `main`.

**Final status:** PX-030 margin calculation, client collection, peak verification and risk-control research documented. PX-025 expanded to 76 requirements and 130 proposed acceptance scenarios. No broker endpoint, account, sandbox or implementation was used.
