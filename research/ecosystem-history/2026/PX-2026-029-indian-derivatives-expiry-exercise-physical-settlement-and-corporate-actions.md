# PX-2026-029 — Indian equity-derivatives expiry, exercise, physical delivery and settlement lifecycle

**Research date:** 2026-11-08  
**Status:** primary-source review completed with explicit source conflicts; current date-specific implementation contract remains to be closed  
**AlgoX area:** Indian-market contract lifecycle / derivatives domain / settlement accounting / risk and reconciliation  
**Exchange/regulator scope:** NSE / NSE Clearing / SEBI  
**Inputs:** PX-023 market-data/contract-master research and PX-028 accounting-reconciliation research  
**Mode:** research and requirements specification only  
**Non-goals:** no broker connection, account access, sandbox/production call, order, code implementation, paid service, legal opinion, PR or merge to `main`

## Executive finding

Indian equity derivatives cannot be modelled as an ordinary order becoming a final cash P&L at expiry. The lifecycle depends on contract family and the effective settlement rules:

- **Index derivatives:** the index itself is not a deliverable security. Final settlement is a cash obligation based on the applicable index final-settlement reference. The older NSE settlement-mechanism page describes cash final settlement and automatic European-style exercise for index options.
- **Individual-stock derivatives:** SEBI made physical settlement mandatory for all stock derivatives through a phased transition completed by the October 2019 expiry. This covers stock futures and stock options. A stock derivative position at expiry can create securities and funds obligations, not merely a cash MTM entry.
- **Stock options:** the NSE settlement page describes automatic final exercise for in-the-money positions at expiry and random allocation of long in-the-money positions to short positions in the same series. In a physically settled stock option, this can create delivery/receipt obligations.
- **Settlement netting:** SEBI introduced net settlement between cash-market and physical F&O obligations on stock-derivative expiry from the March 2023 expiry. Eligibility is restricted; it is not blanket netting across brokers, clearing members, institutional accounts or all client positions.
- **Expiry and corporate actions:** NSE's current contract-specification page gives Tuesday expiry with previous-trading-day fallback for the listed index and individual-security contracts. Corporate actions can adjust contract strikes, market lots, positions and futures base prices; mergers can cause compulsory closeout and cancellation of GTC/GTD orders.

A critical documentation conflict remains: NSE's settlement-mechanism HTML page, last updated 3 January 2023, says final exercise settlement for both index and individual-security options is cash-settled. That statement for individual-security options conflicts with SEBI's mandatory physical-settlement circulars, NSE's individual-securities F&O page, and NSE Clearing's March 2024 PFMI disclosure distinguishing delivery-settled contracts. A second NSE page, “Clearing Members”, last updated 7 January 2023, still says only funds settlement is allowed for index and stock futures/options. These older pages must not be used as a blanket current stock-derivative settlement rule.

**Research verdict:** the domain model must carry explicit, date-effective `settlement_mode`, product family, expiry calendar, exercise/assignment result, delivery/funds obligations, settlement netting eligibility and settlement evidence. If the effective contract/rule set cannot be established for the contract date, the result is UNKNOWN and the expiry/settlement process must fail closed.

## 1. Evidence set and source hierarchy

### 1.1 Primary regulatory decisions

**SEBI Circular SEBI/HO/MRD/DOPI/CIR/P/2018/161, 31 December 2018 — Physical settlement of stock derivatives**

The circular states that physical settlement shall be mandatory for all stock derivatives, with the phased move from cash settlement to physical settlement:
- bottom 50 stocks from April 2019 expiry;
- next 50 from July 2019 expiry;
- remaining stocks from October 2019 expiry;
- new derivatives on qualifying new stocks also physically settled.

The 2019 SEBI physical-settlement circular (SEBI/HO/MRD/DOP1/CIR/P/2019/28) is another part of this policy sequence. The 2018/161 circular is the clearest primary statement of the complete mandatory transition.

Sources:
- https://www.sebi.gov.in/legal/circulars/dec-2018/physical-settlement-of-stock-derivatives_41482.html
- https://www.sebi.gov.in/sebi_data/attachdocs/dec-2018/1546255335099.pdf
- https://www.sebi.gov.in/legal/circulars/feb-2019/physical-settlement-of-stock-derivatives_42021.html

**SEBI Circular SEBI/HO/MRD2_DCAP/P/CIR/2022/165, 30 November 2022 — Net settlement upon expiry of stock derivatives**

The circular confirms physical settlement of stock derivatives and introduces net settlement of cash-segment settlement obligations and physical F&O obligations arising upon stock-derivative expiry. Its eligibility and exclusions are important:
- investors receive the benefit where the same trading member clears both cash and F&O through the same clearing member (same TM-CM combination);
- institutions, including all categories of FPI, are excluded;
- non-institutional custodial participants may qualify through the same entity registered as custodian in cash and CM in F&O, subject to the stated exclusions;
- netting is for delivery obligations for settlement; STT and stamp duty remain computed, levied and reported segment-wise;
- clearing corporations continue to net at clearing-member level and retain segment-wise default waterfalls;
- effective from March 2023 F&O expiry.

Source:
- https://www.sebi.gov.in/legal/circulars/nov-2022/net-settlement-of-cash-segment-and-futures-and-options-fando-segment-upon-expiry-of-stock-derivatives_65667.html
- https://www.sebi.gov.in/sebi_data/attachdocs/nov-2022/1669806407982.pdf

### 1.2 NSE contract specification and expiry

NSE's current equity-derivatives contract-specification page lists the relevant index and individual-security products and states:
- Nifty 50, Nifty Bank, Nifty Financial Services, Nifty Midcap Select and Nifty Next 50 expiry: Tuesday of the expiry period;
- individual-security contracts: Tuesday of the expiry period;
- when the Tuesday is a trading holiday, expiry is the previous trading day.

The page is marked updated 10 February 2026. A date-specific circular and exchange holiday calendar remain the final reference for a given contract/expiry. Do not hard-code Tuesday for every derivative family, historical period or exchange.

Sources:
- https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- https://www.nseindia.com/resources/exchange-communication-holidays?apiversion=v2
- NSE expiry-change circular linked from contract specification: https://nsearchives.nseindia.com/content/circulars/NSE_FAOP_68747.pdf

### 1.3 NSE exercise and settlement documentation

The NSE Settlement Mechanism page describes:
- options as European-style;
- automatic final exercise at expiry;
- exercise for in-the-money option positions at the close of trading hours on expiry;
- long in-the-money positions assigned to short positions of the same series on a random basis;
- exercised option contracts allocated to clearing members at the client level;
- futures daily MTM and final-settlement concepts.

The page is marked updated 3 January 2023. It also says final exercise settlement for both index and individual-security options is cash-settled. That statement for individual-security options conflicts with the SEBI physical-settlement mandate and the later NSE Clearing disclosure. Treat its cash-settlement statement as stale/contradictory for stock derivatives; do not use it to override the SEBI requirement.

Sources:
- https://www.nseindia.com/static/products-services/equity-derivatives-settlement-mechanism
- https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price

### 1.4 NSE Clearing disclosure separates delivery and cash settlement

NSE Clearing's March 2024 PFMI disclosure says:
- cash-settled futures final settlement occurs before market hours on the following day;
- delivery-settled futures final settlement occurs on Expiry+1;
- cash-settled options final exercise settlement occurs before market hours on the following day;
- delivery-settled options final exercise settlement occurs on Expiry+1;
- delivery-settled futures/options obligations are netted with cash-market obligations to arrive at final netted delivery/funds obligations for cash-market settlement.

This source demonstrates that the clearing corporation distinguishes delivery-settled from cash-settled contracts. The exact date, pay-in, payout and holiday handling must still be resolved against the applicable settlement schedule and clearing circular for the contract.

Source:
- https://www.nseclearing.in/sites/default/files/disclosure-doc/2024-07/NCL%20PFMI%20Disclosure_March%202024.pdf

### 1.5 Current NSE product and risk documentation

NSE's individual-securities F&O page describes stock options as European-style and physically settled. NSE Clearing's current margin page (updated 9 March 2026) includes delivery margins and assignment margins in its reporting and current initial-margin framework. The actual rates/parameters are time-sensitive and must come from the applicable date's clearing files/circulars, not constants copied from this research note.

Sources:
- https://www.nseindia.com/static/products-services/equity-derivatives-individual-securities
- https://www.nseclearing.in/risk-management/equity-derivatives/margins

### 1.6 NSE physical-settlement client communication

NSE Circular NSE/INSP/38376, 20 July 2018, clarifies:
- the original contract note is issued at trade time and, where applicable, remarks indicate that the open position is to be physically settled;
- no new contract note is required on the final settlement date, but the member must communicate the final settlement in writing with a reference to the original trade, including contract description, date and trade number;
- delivery margin applies from expiry through settlement or early pay-in and is included in the daily margin statement's total-upfront-margin column.

This is a historical clarification; current applicable margin and client communication obligations still need date-effective circular/rule validation.

Source:
- https://nsearchives.nseindia.com/content/circulars/INSP38376.pdf

## 2. Settlement mode by product family

### 2.1 Index futures and options

An index is not a deliverable security. Index futures and options are therefore financially/cash settled rather than resulting in delivery of constituent shares to an investor.

- Index futures have daily MTM during the contract and a final settlement against the applicable underlying index final-settlement value.
- Index options use premium settlement while open and automatic European-style final exercise for in-the-money positions at expiry; the final result is a cash obligation.
- The NSE settlement-price page identifies the index final-settlement reference as the closing value of the relevant underlying index in the Capital Market segment on the last trading day of the contract.

The 2023 NSE Settlement Mechanism cash-settlement description is consistent for index products. Its simultaneous application of cash settlement to individual-stock options is the contradictory portion and must not be projected to stock options.

### 2.2 Individual-stock futures and options

SEBI's mandatory-physical-settlement decision applies to all stock derivatives. It is not limited to stock options:
- a long stock future has a buy/delivery-receipt obligation;
- a short stock future has a sell/delivery-give obligation;
- a physically settled in-the-money stock call: long call receives the underlying shares and pays the strike-value funds; short call delivers shares and receives funds;
- a physically settled in-the-money stock put: long put delivers shares and receives strike-value funds; short put receives shares and pays funds.

The exact quantity, lot, security identity and settlement value must come from the effective contract master, final exercise/assignment and clearing obligation files. The simple directional descriptions above are domain explanations, not a substitute for exchange-generated obligations.

### 2.3 Contract-family mode is data, not a global constant

A future implementation MUST NOT use one global `cash_settled=true` or `physical_settled=true` setting for the entire equity-derivatives segment.

The mode must be derived from:
- exchange and segment;
- product family (index vs individual security);
- instrument type (future vs option);
- underlying/security;
- contract specification and effective date;
- applicable SEBI/exchange/clearing circular versions;
- special corporate-action or exceptional settlement instructions.

An unresolved mode is UNKNOWN. Do not infer physical/cash mode from symbol spelling, instrument token, broker display text or a generic segment flag alone.

## 3. Expiry calendar and contract identity

Every derivative contract should be keyed by an immutable/effective-dated contract identity, not just a ticker:
- exchange and segment;
- instrument/product family;
- underlying index/security identity;
- contract symbol and exchange instrument/security ID;
- expiry date and expiry period/type;
- option type and strike (where relevant);
- lot/multiplier and quantity units;
- tick size and price step;
- settlement mode and exercise style;
- contract master version/effective date;
- circular/policy references controlling expiry and settlement.

NSE's current listed equity-derivatives expiry day is Tuesday for the named index and individual-security contracts, with previous trading-day fallback for a Tuesday holiday. The expiry scheduler must use the published calendar for that year and the specific contract circular. A holiday can move the expiry earlier; it must not be assumed to move later automatically.

A historical backtest must use the contract master and calendar version applicable to the historical session. Applying the current Tuesday rule to a pre-change contract or another segment is invalid.

## 4. Exercise, assignment and physical obligation

### 4.1 Automatic exercise

The NSE settlement mechanism page states European-style exercise and automatic final exercise on expiry. In-the-money open option positions at close are exercised; long ITM positions are randomly assigned to short positions in the same series. The clearing member receives client-level allocation of exercised positions.

A future design must preserve:
- original option contract ID and series;
- long/short side and client position;
- close/expiry reference and ITM decision evidence;
- exercise quantity and assignment result;
- random assignment/clearing allocation evidence if exposed in exchange files;
- resulting cash or securities obligation;
- relationship to the original trade(s) and option position.

Do not synthesize assignment from the fact that an option closed in-the-money alone if the actual exchange/clearing allocation file is not available. For a short option, random assignment is a source-controlled allocation, not a deterministic “all short positions exercise” rule.

### 4.2 Stock futures and option delivery direction

For physical stock derivatives, the domain needs separate buy/receive and sell/give legs.

| Expiring position | Client's physical obligation | Client's funds obligation |
|---|---|---|
| Long stock future | Receive/buy underlying shares | Pay settlement value |
| Short stock future | Deliver/sell underlying shares | Receive settlement value |
| Long ITM stock call | Receive underlying shares | Pay strike value |
| Short ITM stock call | Deliver underlying shares | Receive strike value |
| Long ITM stock put | Deliver underlying shares | Receive strike value |
| Short ITM stock put | Receive underlying shares | Pay strike value |

This table explains the contractual direction; exchange files determine actual client quantities, netting, funds and settlement dates.

### 4.3 Daily futures MTM versus expiry delivery

Daily MTM cash flows on stock futures remain a separate lifecycle from the physical delivery obligation created at expiry. The system must not replace daily MTM history with the final delivery event or add final settlement value again as if it were another daily MTM.

Index futures final cash settlement and stock futures physical delivery are different outcome types. The original futures trade remains in the execution ledger; the expiry creates one or more linked settlement events.

## 5. Delivery margin, early pay-in and clearing schedule

NSE's physical-settlement FAQ states delivery margin applies from expiry until settlement or early pay-in. The daily margin statement must show the delivery margin in the total upfront margin field. NSE Clearing's current margin page includes delivery margin and assignment margin in margin reporting.

Requirements:
- record delivery margin as a time-bounded risk/margin obligation, not as a trade or permanent expense;
- preserve margin type, amount, rate/parameter source, valuation reference, effective time, release condition and actual release evidence;
- distinguish an early pay-in instruction from confirmed delivery/pay-in;
- do not release delivery margin merely because the client requested early pay-in; release only after authoritative confirmation and applicable margin recomputation;
- do not hard-code 2018 rates or current page examples across historical dates/contracts.

NSE Clearing's March 2024 PFMI disclosure states delivery-settled futures/options final settlement occurs on Expiry+1; the actual settlement calendar and time must be read from the applicable clearing schedule/circular. Use working-day/holiday logic from the dated settlement calendar; do not simply add 24 hours to the expiry timestamp.

Sources:
- https://nsearchives.nseindia.com/content/circulars/INSP38376.pdf
- https://www.nseclearing.in/risk-management/equity-derivatives/margins
- https://www.nseclearing.in/sites/default/files/disclosure-doc/2024-07/NCL%20PFMI%20Disclosure_March%202024.pdf

## 6. Net settlement across cash and F&O on stock expiry

SEBI Circular 2022/165 introduced a merged cash/F&O settlement for eligible stock-derivative expiry obligations.

The documented criteria require:
- same trading member clears cash and F&O through the same clearing member (same TM-CM combination);
- institutional investors, including all categories of FPI, are excluded;
- non-institutional custodial participants can qualify through the same registered custodian/CM combination, subject to specified exclusions;
- the permitted set-off is for delivery obligations for settlement; STT and stamp duty remain segment-wise;
- clearing corporations continue netting at CM level and maintain segment-wise default waterfalls.

A future design must not treat this as:
- a global cross-broker netting privilege;
- netting between two different clearing members or clearing corporations;
- permission to offset institutional deliveries;
- permission to erase the original cash-market and F&O obligations;
- netting of taxes/charges into one untraceable amount;
- permission to use clearing-member net positions as the client's own deliverable position.

Store at least three levels separately:
1. **Client-level obligation:** original F&O exercise/expiry position and cash-market trades for that client.
2. **Eligibility/grouping decision:** account/TM/CM/custodian/participant classification and applicable SEBI netting rule.
3. **Clearing-member settlement result:** the official net delivery/funds obligation, with segment-wise tax/default-waterfall evidence preserved.

The exact netting algorithm, exchange file schema and treatment of all special participant categories must come from current implementation circulars and clearing data, not be invented from the policy summary.

Source:
- https://www.sebi.gov.in/sebi_data/attachdocs/nov-2022/1669806407982.pdf

## 7. Corporate actions and contract transformations

NSE says equity-derivative corporate-action adjustments are carried out on the last day the underlying is traded on a cum basis, after market close, and can change open positions and contract specifications including strike price, position and market lot/multiplier.

Examples from the NSE methodology page (updated 14 March 2023):

### 7.1 Bonus, splits and consolidations

NSE's method defines an adjustment factor:
- bonus ratio A:B: (A+B)/B;
- split/consolidation ratio A:B: A/B.

For bonus/split/consolidation, the published methodology divides the old strike price and futures base price by the factor and multiplies market lot/multiplier and position by the factor. Rounding of strike and lot can be necessary; NSE describes a process intended to minimize fraction settlement and preserve position value, with further adjustment decided by the relevant authority.

Do not compute an approximate strike/lot/position adjustment without the official dated adjustment factor and rounded contract master.

### 7.2 Rights issue

The rights adjustment uses the rights ratio, issue price, rights entitlement and underlying close on the last cum date to calculate an adjustment factor. The new strike, lot/multiplier, futures base price and position are adjusted. Prices are rounded to tick size and lot size to the nearest integer as stated in the methodology.

This is date/event-driven; the exact factor must be stored alongside the source circular/calculation version.

### 7.3 Dividends

NSE's page says ordinary dividends below 2% of underlying market value do not lead to strike adjustment. Extraordinary dividends at or above 2% trigger the stated adjustment; total dividend is deducted from cum-dividend option strikes, and the futures base price is adjusted using the reference rate less aggregate dividend. Revised strike prices apply from the exchange-specified ex-dividend date.

This threshold/method must be applied only under the version of the NSE policy effective for the event date; do not assume every cash dividend adjusts the derivative contract.

### 7.4 Mergers

The NSE page states:
- after the merger record date announcement, the last cum-date/early expiry is informed to members;
- no fresh futures/options contracts are introduced on the underlying that will cease to exist;
- unexpired contracts outstanding on last cum-date are compulsorily settled at the closing price of the underlying on that last cum-date;
- GTC/GTD orders outstanding at close on last cum-date are cancelled by the Exchange.

This is an explicit non-trade forced closeout/cancellation event; it must not be represented as a normal client-initiated order fill.

Sources:
- https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments

## 8. Settlement event model and PX-028 accounting links

This is a candidate event decomposition, not a final code enum or schema.

`ContractSpecificationObserved` → `ExpiryScheduled` → `PreExpiryRiskCheck` → `ExpiryObservationCaptured` → one of:
- `CashFinalSettlementCalculated` (index derivatives);
- `OptionExerciseEligible` → `ExerciseAssignmentObserved` → `CashExerciseObligation` (cash-settled contract);
- `PhysicalDeliveryObligationCreated` (stock derivative);
- `CorporateActionAdjusted` / `ForcedCloseoutCreated`.

For physical stock derivatives:
`DeliveryMarginAssessed` → `EarlyPayInInitiated` (optional) → `EarlyPayInConfirmed` (only after source evidence) → `SettlementObligationFinalized` → `SecuritiesPayInDue` and/or `FundsPayInDue` → `PayoutDue` → `SettlementConfirmed` → `MarginReleaseObserved`.

Exception paths include:
- `DeliveryShortage`;
- `AuctionInitiated`;
- `AuctionAllocated`;
- `AuctionFailed`;
- `CloseoutApplied`;
- `DefaultOrPenaltyRecorded`;
- `SettlementUnknown`.

Each event must retain source, account, contract, trading date, expiry date, settlement date, original trade/position reference, currency/quantity units, obligation side, policy/version, event time, capture time and raw evidence reference.

PX-028 provides the downstream reconciliation layers:
- original derivative trades and option assignments;
- resulting stock holdings/deliveries (DP/T+1/available/collateral buckets);
- funds and cash ledger debits/credits;
- delivery/assignment margin and release;
- STT/stamp duty/other charges;
- original contract note and written expiry-settlement communication.

A settlement event is not itself proof of successful pay-in/payout. Reconcile the generated obligation, the actual settlement result and the account-level records independently.

## 9. Source conflict register and confidence

| Source | Publication/update date | Claim | Assessment |
|---|---|---|---|
| SEBI Circular 2018/161 | 31 Dec 2018 | Mandatory physical settlement for all stock derivatives, phased through Oct 2019 | Controlling regulatory source for stock-derivative mode |
| SEBI Circular 2022/165 | 30 Nov 2022, effective Mar 2023 expiry | Eligible cash/F&O stock-expiry obligations netted; restrictions and segment-wise taxes | Regulatory source for netting framework |
| NSE contract specification | Updated 10 Feb 2026 | Tuesday expiry; previous trading day if Tuesday holiday | Current exchange contract-calendar source, subject to specific circular/master |
| NSE individual securities F&O page | Current page | Stock options European and physically settled | Supports stock-option physical mode |
| NSE Settlement Mechanism page | Updated 3 Jan 2023 | Cash final settlement for index and individual-stock options | **CONFLICT:** the stock-option cash statement conflicts with SEBI 2018/161 and later NSE Clearing PFMI; do not rely on it for current stock derivatives |
| NSE Clearing “Clearing Members” page | Updated 7 Jan 2023 | Only funds settlement allowed in index and stock futures/options | **CONFLICT / STALE:** inconsistent with mandatory physical stock settlement and later PFMI delivery-settlement description |
| NSE Clearing PFMI disclosure | 31 Mar 2024 | Delivery-settled futures/options on Expiry+1; cash-settled contracts separately; delivery obligations net with cash market | Later clearing-corporation disclosure; supports dual cash/delivery settlement modes |
| NSE margin page | Updated 9 Mar 2026 | Current margin framework/reports include delivery and assignment margins | Current risk-management reference; parameters remain date-effective |
| NSE corporate-action page | Updated 14 Mar 2023 | Adjustment methods and merger closeout | Exchange methodology; use the policy version effective on each corporate-action date |
| NSE physical-settlement FAQ | 20 Jul 2018 | Client communication and delivery-margin window | Historical implementation clarification; current circulars may supersede details |

The source conflict remains explicit in this research record. It must be resolved against the current effective exchange/clearing rulebook and circulars before implementation. A newer disclosure is evidence of the later distinction; it is not permission to ignore an applicable subsequent circular that may have changed the process after March 2024.

## 10. Research conclusions

- **ACCEPT:** settlement mode is product/underlying/effective-date specific; index and stock derivatives must not share one settlement flag.
- **ACCEPT:** stock derivatives are physically settled under the mandatory SEBI transition; the phased change was completed by October 2019 expiry.
- **ACCEPT:** stock options need automatic exercise/assignment evidence and share/funds obligations; random assignment must not be fabricated.
- **ACCEPT:** expiry calendar, holiday fallback, lot/multiplier and corporate actions must be date-versioned.
- **ACCEPT:** physical delivery margin, early pay-in, cash/F&O netting eligibility, clearing-member obligations, actual securities/funds settlement and account reconciliation are separate lifecycle stages.
- **ACCEPT:** SEBI cross-segment netting is restricted to eligible same TM-CM combinations; institutions including FPIs are excluded and taxes remain segment-wise.
- **ACCEPT:** a merger forced closeout or corporate-action contract adjustment is an exchange-originated event, not a normal client trade.
- **DEFER:** final settlement state enum, delivery-obligation formulas/rounding for each product, netting file parser, client/CM allocation algorithm and shortfall closeout calculation.
- **NOT AUTHORIZED:** broker access, live/sandbox order, execution configuration, code change, paid data, publication/PR or merge to `main`.

## 11. Open contract questions

1. Which current NSE Clearing UDiFF/report formats carry the authoritative client-level stock-derivative physical delivery obligations, exercise assignment and net-settlement outcome?
2. Which current effective circulars define exact delivery quantity/value rounding, settlement holidays, pay-in/payout cutoff and early pay-in treatment by product?
3. What current risk parameters and delivery-margin schedules apply to each stock derivative and expiry date?
4. What current exchange circulars govern shortage, auction, closeout price, penalties and default handling specifically for physical stock-derivative settlement?
5. How are exercise/assignment outcomes exposed in broker order/trade/ledger/contract-note channels and reconciled to the original option trade?
6. How are non-institutional custodial participants, PMS and other delivery-only client classes represented in clearing eligibility data?
7. Which versioned corporate-action adjustment files and adjustment calculators are authoritative for each date?
8. Have any post-March-2024 circulars changed the settlement modes, netting eligibility, settlement cutoffs or reporting process reflected in the PFMI disclosure?
9. Which exact index product families remain cash-settled and what are the current expiry/final-settlement schedules of each special/long-dated index series?
10. How should the platform represent an expiry obligation when the broker's margin/position snapshot and the exchange/clearing obligation file disagree?

All remain OPEN or UNKNOWN unless a source/version-specific answer is obtained. No broker or clearing API was called to test them.

## Source register

**SEBI**
- Physical settlement of stock derivatives, Circular SEBI/HO/MRD/DOPI/CIR/P/2018/161 (31 Dec 2018): https://www.sebi.gov.in/sebi_data/attachdocs/dec-2018/1546255335099.pdf
- SEBI legal circular page: https://www.sebi.gov.in/legal/circulars/dec-2018/physical-settlement-of-stock-derivatives_41482.html
- Net Settlement of Cash and F&O upon expiry of stock derivatives, Circular SEBI/HO/MRD2_DCAP/P/CIR/2022/165 (30 Nov 2022): https://www.sebi.gov.in/sebi_data/attachdocs/nov-2022/1669806407982.pdf
- SEBI legal circular page: https://www.sebi.gov.in/legal/circulars/nov-2022/net-settlement-of-cash-segment-and-futures-and-options-fando-segment-upon-expiry-of-stock-derivatives_65667.html

**NSE / NSE Clearing**
- Contract Specifications: https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- Settlement Mechanism: https://www.nseindia.com/static/products-services/equity-derivatives-settlement-mechanism
- Settlement Price: https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price
- Individual Securities F&O: https://www.nseindia.com/static/products-services/equity-derivatives-individual-securities
- Corporate Action Adjustments: https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments
- NSE Clearing PFMI Disclosure (31 Mar 2024): https://www.nseclearing.in/sites/default/files/disclosure-doc/2024-07/NCL%20PFMI%20Disclosure_March%202024.pdf
- NSE Clearing margins: https://www.nseclearing.in/risk-management/equity-derivatives/margins
- NSE Clearing STT: https://www.nseclearing.in/clearing-settlement/equity-derivatives/securities-transaction-tax
- Physical settlement FAQ / Circular NSE/INSP/38376 (20 Jul 2018): https://nsearchives.nseindia.com/content/circulars/INSP38376.pdf

**Final status:** PX-029 expiry, exercise, stock physical settlement, cash/F&O netting and corporate-action research documented with explicit conflicts and open contract questions. No broker/clearing API, account, sandbox, real order, implementation or paid service was used.
