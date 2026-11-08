# PX-2026-028 — Portfolio, cash-ledger, charge and contract-note reconciliation

**Research date:** 2026-11-08  
**Status:** official-documentation comparison completed; end-to-end accounting reconciliation contract remains open  
**AlgoX area:** broker adapters / portfolio accounting / execution ledger / settlement evidence  
**Providers:** Zerodha Kite Connect, Upstox Developer API, DhanHQ API v2  
**External evidence:** NSE investor advisory and broker-issued statements/contract notes  
**Inputs:** PX-2026-024 through PX-2026-027  
**Mode:** research and requirements specification only  
**Non-goals:** no broker account/API access, sandbox/production call, order, code implementation, paid service, PR or merge to `main`

## Executive finding

Order recovery and trade reconciliation do not establish that the broker account's economic state is correct. A complete account reconciliation needs several distinct views:

1. **Order lifecycle:** what the broker accepted, rejected, modified or cancelled.
2. **Execution ledger:** each individual fill, with trade identity, quantity and price.
3. **Position snapshot:** the broker's current open/net position by instrument and product.
4. **Demat holdings and settlement:** settled, T+1, available, collateral/pledged and other delivery quantities.
5. **Cash ledger:** signed debits/credits, vouchers, pay-ins, payouts and running balance.
6. **Charges and taxes:** brokerage, STT, GST, stamp duty, exchange/SEBI/clearing/depository and other applicable charges.
7. **Contract note / broker statement:** the issued transaction statement and the broker's reported charges.
8. **Funds and margin availability:** available-to-trade, blocked/used margin, collateral and withdrawable balances.
9. **Independent external evidence:** depository statement and exchange messages/verification.

These sources answer different questions. An orderbook is not an execution ledger; a tradebook is not a cash ledger; positions are not demat holdings; available margin is not withdrawable cash; and a charge calculator is not the same object as an issued contract note.

**Core decision:** AlgoX must implement accounting reconciliation as separate, linked evidence checks. It must not derive account truth from one P&L number or force different provider views to agree by overwriting the source data.

## 1. Official-source findings

### 1.1 Zerodha Kite Connect

The Portfolio API provides:
- holdings for long-term equity delivery stocks;
- short-term positions;
- separate `net` and `day` position sets.

Kite explicitly defines `net` as the actual current net position portfolio and `day` as that day's buying/selling activity snapshot. It also says overnight equity positions move to the holdings portfolio on the next trading day. Holdings contain separate fields such as `t1_quantity`, `realised_quantity`, `quantity`, `used_quantity`, `authorised_quantity`, `opening_quantity`, collateral quantities and average price.

This means the following must not be treated as interchangeable:
- intraday day activity;
- current net positions;
- delivery holdings;
- T+1 quantities;
- quantities realised/settled in demat;
- quantities used/authorised for sale;
- pledged/collateral quantities.

Kite's Margin Calculation page exposes `POST /charges/orders`, described as a **Virtual contract note**. It calculates an order-wise breakdown using supplied order details and executed quantity/average price, including brokerage, transaction tax, exchange turnover charge, SEBI turnover charge, stamp duty and GST. The documentation allows an arbitrary `order_id` for an imaginary order in this calculator. Therefore this output is a calculation/estimate from input values, not evidence that an actual contract note was issued or that the broker finally posted those exact charges.

The reviewed Kite Connect pages do not establish a general cash-ledger or bank pay-in/payout statement endpoint. This is a documented-surface gap in this audit, not proof that Kite's other client reports or non-Connect channels do not provide statements.

Sources:
- https://kite.trade/docs/connect/v3/portfolio/
- https://kite.trade/docs/connect/v3/margins/

### 1.2 Upstox

The reviewed Upstox developer API exposes separate:
- short-term positions;
- holdings;
- historical trade records;
- trade-wise realised P&L report;
- charges report by segment and financial year;
- pay-in and payout transaction records.

The positions API describes current short-term positions and says overnight equity positions shift to holdings the following trading day. The historical trade API:
- can query the last three financial years;
- is paginated;
- supports EQ, FO, COM, CD and MF segments;
- exposes exchange trade ID, trade date, quantity, amount, side, price and instrument details in the examples.

One important data-quality detail: the published Mutual Fund example has an empty `trade_id`. Therefore a trade ID field must be treated as nullable and segment-scoped, not assumed to be universally populated or globally unique.

The P&L data API returns trade-wise realised P&L for a selected segment and financial year. The separate charges API returns a segment/financial-year charges breakdown with total brokerage, GST, STT, stamp duty, transaction, clearing, IPFT, other, SEBI turnover and demat transaction charges. Its published example is an **aggregate breakdown**, not a per-trade charge mapping. An aggregate total MUST NOT be spread across individual fills without a broker-documented allocation rule.

The pay-in API exposes amount, mode, status, last-update time, bank, transaction ID and payment charges. The account/payment transaction is separate from order/trade execution and must be reconciled as a cash movement.

Sources:
- https://upstox.com/developer/api-documentation/get-positions/
- https://upstox.com/developer/api-documentation/get-holdings/
- https://upstox.com/developer/api-documentation/get-historical-trades/
- https://upstox.com/developer/api-documentation/get-profit-and-loss-report/
- https://upstox.com/developer/api-documentation/get-trade-charges/
- https://upstox.com/developer/api-documentation/get-user-payins/
- https://upstox.com/developer/api-documentation/get-user-payouts/

### 1.3 DhanHQ

Dhan publishes distinct APIs for:
- holdings and current day open positions;
- funds/margin limits;
- account ledger;
- historical trade history.

The Portfolio API's holding records distinguish `totalQty`, `dpQty`, `t1Qty`, `availableQty` and `collateralQty`, together with instrument identity fields such as exchange, security ID and ISIN. The Positions endpoint covers open positions for the day, including F&O carry-forward positions.

The Statement API provides:
- a date-filtered ledger report with narration, voucher date, exchange, voucher description/number, debit, credit and running balance;
- paginated historical trade data with Dhan order ID, exchange order ID, exchange trade ID, segment, product, symbol/security IDs, traded quantity/price, timestamps and charge/tax fields.

The documented trade sample includes SEBI tax, STT, brokerage, service-tax-labelled field, exchange transaction charges and stamp duty. The adapter must preserve the raw provider field name and value. It must not silently relabel a field such as `serviceTax` as GST without a provider schema/revision clarification.

The Funds & Margin API exposes a `/fundlimit` snapshot with start-of-day limit, available balance, collateral, receivable amount, utilised amount, blocked payout and withdrawable balance. These are available-funds/margin fields; they are not a substitute for the dated debit/credit ledger.

Dhan's multi-order margin calculator documentation says returned margin values are indicative and valid only for the current trading session. A margin calculation must not be used as final accounting evidence.

Sources:
- https://dhanhq.co/docs/v2/portfolio/
- https://dhanhq.co/docs/v2/statements/
- https://dhanhq.co/docs/v2/funds/

### 1.4 NSE investor-facing evidence expectations

NSE's investor advisory tells investors to:
- receive contract notes within 24 hours of trades;
- receive a statement of account at least once per quarter;
- verify balances and the demat statement;
- check exchange messages about reported funds and securities balances;
- raise discrepancies with the broker and, where needed, the Exchange/Depositories.

This is used here as an external evidence checklist. PX-028 does not provide legal advice or replace the applicable SEBI/exchange rules and broker agreements.

Source:
- https://www.nseindia.com/static/invest/advisory-for-investors

## 2. Reconciliation layers and source precedence

| Layer | Primary evidence | What it establishes | What it does not establish by itself |
|---|---|---|---|
| Order lifecycle | Order book / order history / postbacks | Broker order state and order identity | Every fill, final position or final cash charge |
| Executions | Individual tradebook/history records | Trade ID, price, quantity, side, order link | Complete account cash/settlement ledger |
| Current positions | Broker net/open positions | Current broker-reported open quantity and product | Demat settled quantity or original trade evidence |
| Holdings | Broker holdings + depository statement | Delivery quantities, T+1, settled/available/collateral distinctions | Current F&O open positions |
| Cash ledger | Dated debit/credit entries and running balance | Account cash movements and balances | Execution causality unless linked to trades/orders |
| Charges | Actual contract note/statement + broker charges reports | Broker-reported fee/tax amounts | Market position or execution completeness |
| Funds/margin | Fund-limit and margin endpoints | Available/blocked/used/withdrawable figures at query time | Final ledger balance or issued charges |
| External confirmation | Contract note, depository statement, exchange messages | Independent cross-check against API observations | Automatic proof that the internal AlgoX ledger has no missing records |

The system should record which source is authoritative for each assertion. It must not declare one global source “the truth” for all accounting layers.

### Required precedence rules

1. **Execution facts:** preserve the provider/exchange trade record and the corresponding issued contract-note evidence. An order status or current position cannot replace individual fill records.
2. **Position quantity:** preserve broker current position snapshot as a broker observation; independently recompute from prior snapshot, executions and documented non-trade adjustments.
3. **Demat quantity:** compare broker holdings with depository evidence and retain T+1/settled/available/collateral categories separately.
4. **Cash balance:** use the broker's actual dated ledger/statement and corroborating bank/pay-in/payout evidence. Do not infer the final cash balance from trade turnover or margin usage.
5. **Charges:** use the issued contract note/broker statement for the posted amount. Use API calculators/indicative charges for pre-trade estimation or diagnostic comparison only.
6. **P&L:** separate realised, unrealised, MTM, brokerage/charges and cash ledger effects. Do not assume a broker P&L summary is the same as net settled cash.

## 3. Required roll-forward controls

### 3.1 Position quantity

For a single broker account, exchange/segment, stable instrument/contract identity, product and effective session:

`closing quantity = opening quantity + signed executions + documented non-trade adjustments`

The non-trade adjustments must be represented as explicit linked events, for example:
- corporate action;
- settlement/delivery movement;
- pledge/unpledge or collateral movement;
- exercise/assignment;
- expiry/physical settlement;
- conversion between margin products;
- broker correction or manual adjustment.

Do not use an unexplained balancing adjustment to force the computed quantity to match the broker snapshot.

### 3.2 Cash ledger

For each currency and statement period:

`closing ledger balance = opening ledger balance + sum(signed posted credits and debits)`

Every ledger line must preserve voucher/transaction identity, date, narration, debit/credit, running balance, source, and any link to a trade, charge, pay-in, payout or settlement event.

A pending pay-in, failed payout or blocked margin is not a posted ledger credit/debit unless the broker ledger shows it. A funds snapshot can differ from ledger cash due to margin, collateral, receivable and blocked-payout components.

### 3.3 Charges

Reconcile actual charges across:
- brokerage;
- STT/CTT as applicable;
- stamp duty;
- GST;
- exchange transaction charges;
- SEBI turnover charges;
- clearing charges;
- investor protection fund charges;
- DP/demat transaction charges;
- other broker-documented levies.

Preserve each component, currency, calculation basis, trade/contract note reference, applicable segment, side, trade date, effective tariff version and rounding. No single fixed fee formula should be applied retrospectively across all dates/segments.

### 3.4 P&L

Keep these components separate:
- realised trading P&L;
- unrealised/open-position P&L;
- intraday/day P&L;
- carry-forward/overnight P&L;
- mark-to-market or settlement adjustments;
- execution charges/taxes;
- ledger/cash movements.

A P&L API summary, broker net position value and cash ledger balance answer different questions. Any derived net result must show the formula and its inputs.

## 4. Instrument, settlement and unit identity

The reconciliation key must not rely on a trading symbol alone. Preserve:
- broker/account ID;
- exchange and segment;
- stable security/instrument ID;
- ISIN where applicable;
- symbol as observed on the trade date;
- expiry, strike and option type for derivatives;
- product/margin type;
- trading date and settlement date where supplied;
- quantity unit and effective lot-size/contract-master version.

Equity delivery holdings have a settlement lifecycle that differs from intraday position views. The APIs explicitly distinguish T+1 and delivered quantities or say overnight equity positions move between positions and holdings. Do not assume one universal settlement-cycle constant across all effective dates, segments and instruments; use the applicable date/version-specific exchange/depository evidence.

For derivatives, preserve raw quantity units and conversion separately. Do not normalize a source quantity to contracts or underlying shares without the applicable historical contract master and an explicitly verified source-unit definition. This connects directly to the quantity-unit issue in PX-023.

## 5. Contract note and actual-charge handling

A contract note is a separate evidence artifact from:
- orderbook;
- tradebook;
- API margin calculator;
- virtual/estimated contract note;
- P&L dashboard;
- cash ledger.

The NSE investor advisory says investors should receive contract notes within 24 hours of trades. The system should therefore preserve the broker-issued note/report as an original artifact, with:
- broker and client identity references (sensitive fields redacted in project logs);
- exchange/segment and trade date;
- order/trade identifiers and individual execution details where present;
- turnover and charge/tax breakdown;
- document issue/generation time;
- original file/content hash and retrieval provenance.

Kite's `/charges/orders` is explicitly titled a virtual contract note and accepts supplied order attributes including an arbitrary order ID for imaginary-order charge calculation. Treat it as a diagnostic charge calculator, not as proof of the actual contract note. Upstox's charges API returns a segment/financial-year charges breakdown in aggregate form; do not allocate it to individual trade IDs without a documented allocation rule. Dhan's historical trade records contain per-trade charge fields, but those API fields still need comparison against the issued contract note and account ledger.

A missing contract note after the applicable delivery window, a contract-note total that does not reconcile to trade/charge records, or a missing segment/trade line is a reconciliation exception—not something to patch with an estimated fee.

## 6. Funds and margin are separate views

Funds/margin APIs are snapshots useful for risk and pre-trade checks:
- Dhan `fundlimit` includes available balance, start-of-day limit, collateral, receivables, utilised amount, blocked payout and withdrawable balance.
- Dhan's margin calculator says multi-order values are indicative and valid for the current session.
- Kite exposes margin calculation against orders and positions.
- Upstox exposes account payments and margin endpoints.

The available-to-trade balance is not necessarily the same as ledger cash or withdrawable bank balance. Differences must be explained by explicit components (open-order margin, position margin, collateral, receivables, blocked payouts, unsettled funds and other provider-specific buckets), not flagged as cash ledger corruption merely because two differently defined figures differ.

No implementation should sum every margin/funds field together; they may overlap or represent alternative views of the same funds.

## 7. Reconciliation workflow

1. **Capture period boundaries.** Pin broker, account, date range, segment, trading date, settlement date, timezone and source document/API versions.
2. **Load opening state.** Capture prior closing/net position, settled holdings/T+1 quantities and opening ledger balance from provider/external evidence.
3. **Collect all orders and trades.** Retrieve paginated order/trade records; retain raw payloads, pagination metadata, API version and capture times.
4. **Reconcile fills.** Match unique trade IDs to broker orders; compare total fill quantities/prices with final order observations. Preserve trade corrections/UNKNOWN from PX-027.
5. **Roll positions.** Apply signed executions to opening quantity and append explicit settlement/corporate/non-trade adjustments. Compare derived quantity with current broker positions.
6. **Reconcile delivery holdings.** Compare broker holdings T+1/delivered/available/collateral buckets with depository statement/settlement records. Do not collapse them into one integer.
7. **Reconcile cash.** Collect dated ledger entries, pay-ins/payouts and settlement debits/credits. Verify running-balance arithmetic and closing balance.
8. **Reconcile fees and taxes.** Compare trade-level charges, aggregate charge reports and contract-note itemization. Record any source-level granularity mismatch instead of inventing an allocation.
9. **Compare P&L views.** Recompute realised and unrealised components where data supports it; identify broker-specific definition differences.
10. **Compare funds/margin.** Reconcile available/used/blocked/withdrawable values against explicit components; do not use as a substitute for ledger cash.
11. **Classify exceptions.** Assign unmatched trade, quantity variance, settlement variance, cash variance, charge variance, missing note, identity/unit issue or UNKNOWN.
12. **Persist reconciliation evidence.** Store source references, raw observations, hashes, page totals, exact software/policy version, calculated values, variance and resolution status.
13. **Keep unresolved state visible.** Do not force a zero variance, round away a meaningful difference, or declare PASS when source pages are missing or inconsistent.

## 8. Proposed reconciliation exception taxonomy

- `ORDER_WITHOUT_TRADE`
- `TRADE_WITHOUT_ORDER`
- `DUPLICATE_TRADE_ID`
- `TRADE_QUANTITY_VARIANCE`
- `POSITION_ROLL_FORWARD_VARIANCE`
- `UNEXPLAINED_POSITION_ADJUSTMENT`
- `HOLDINGS_SETTLEMENT_VARIANCE`
- `T1_DELIVERED_QUANTITY_VARIANCE`
- `COLLATERAL_OR_PLEDGE_VARIANCE`
- `LEDGER_RUNNING_BALANCE_VARIANCE`
- `CASH_EXTERNAL_TRANSFER_UNMATCHED`
- `CHARGE_COMPONENT_VARIANCE`
- `AGGREGATE_CHARGE_ALLOCATION_UNKNOWN`
- `CONTRACT_NOTE_MISSING`
- `CONTRACT_NOTE_TRADE_LINE_MISMATCH`
- `CONTRACT_NOTE_CHARGE_TOTAL_VARIANCE`
- `FUNDS_SNAPSHOT_COMPONENT_VARIANCE`
- `PNL_DEFINITION_MISMATCH`
- `INSTRUMENT_OR_UNIT_MISMATCH`
- `SETTLEMENT_DATE_OR_STATUS_UNKNOWN`
- `SOURCE_PAGINATION_INCOMPLETE`
- `SOURCE_PERIOD_OR_RETENTION_INCOMPLETE`

These are descriptive research classifications, not implemented enums.

## 9. Additional requirements for PX-025

### R-037 — Accounting layers remain distinct

The system MUST model orders, executions, current positions, demat holdings, cash ledger, charges/contract notes, funds/margin and external evidence as distinct but linkable accounting layers. One layer MUST NOT be substituted for another merely because it returns a total P&L or balance.

### R-038 — Stable instrument and account scope

Every accounting record MUST be scoped by broker, account, exchange, segment, stable instrument/security identity, product, trading date and settlement date where applicable. Symbols alone MUST NOT be used as the durable cross-period key.

### R-039 — Position roll-forward must be explicit

A position reconciliation MUST compare opening quantity plus signed executions plus documented non-trade adjustments with the broker closing position. Any unexplained adjustment or quantity mismatch MUST remain an exception; no plug/balancing entry may be invented.

### R-040 — Demat and broker holdings buckets remain separate

The system MUST preserve settled/DP quantity, T+1 quantity, available/sellable quantity, used/authorised quantity and collateral/pledged quantity independently when the source provides them. It MUST NOT equate broker derivative/intraday positions with demat delivery holdings.

### R-041 — Cash ledger is transaction-based

Where a ledger source exists, every debit/credit MUST retain voucher/transaction identity, date, narration, amount, running balance and source. Closing balance MUST be reconciled from opening balance plus signed posted entries. Pending or blocked amounts MUST NOT be silently booked as posted credits/debits.

### R-042 — Actual contract note outranks charge estimates for posted amounts

The system MUST preserve broker-issued contract notes/statements as original evidence. A virtual contract note, pre-trade calculator or indicative charge report MUST NOT be presented as the actual posted charge without explicit provider documentation establishing equivalence.

### R-043 — Charge components are date/segment/version aware

Charge reconciliation MUST preserve separate charge/tax components, applicable segment, side, trade date, calculation basis, tariff/source version, currency and rounding. An aggregate charge report MUST NOT be allocated to individual trades without an authoritative allocation rule.

### R-044 — Available funds and withdrawable cash are not interchangeable

Funds/margin snapshots MUST preserve their individual fields and query time. Available-to-trade, blocked/used margin, collateral, receivable, blocked payout, ledger cash and withdrawable balance MUST NOT be added or equated unless their provider definitions establish non-overlapping accounting meaning.

### R-045 — P&L dimensions remain separate

The system MUST distinguish realised P&L, unrealised P&L, intraday/day P&L, carry-forward P&L, MTM/settlement adjustments, charges and cash movements. It MUST NOT treat broker P&L summaries as cash ledger balances.

### R-046 — Pagination and period completeness are mandatory

Historical trade, charge, ledger and other paginated/date-filtered reports MUST retain the requested date/segment/financial-year scope, page count, total-record metadata and completion status. Missing pages, inaccessible history or provider retention limits MUST leave the reconciliation period incomplete/UNKNOWN.

### R-047 — Settlement and demat evidence are external cross-checks

Where delivery holdings or cash settlement are in scope, the system SHOULD cross-check broker holdings and ledger against depository and exchange/bank evidence available to the account. T+1/settled/collateral and trade/settlement dates MUST remain distinct and date-valid. A broker API response alone MUST NOT be labelled independent external verification.

### R-048 — Raw source numerics must be preserved

The adapter MUST preserve original numeric strings/JSON representations and source units for trade quantities, prices, taxes, fees and balances. Derived money MUST use exact decimal arithmetic; binary floating-point parsing MUST NOT silently become the financial source of truth. Rounding rules and source precision MUST be explicit.

## 10. Additional deterministic acceptance scenarios

These extend PX-025 AT-001 through AT-049. The following use deterministic synthetic provider/statement fixtures only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-050 | Opening position plus signed trades matches broker closing net position | Reconciliation PASS for that instrument/product/session with all source references retained |
| AT-051 | Broker position differs from computed roll-forward with no adjustment evidence | POSITION_ROLL_FORWARD_VARIANCE; no balancing event fabricated |
| AT-052 | Overnight equity moves from positions view to holdings view | Model the provider's documented portfolio transition; do not interpret it as a missing sell or zero quantity |
| AT-053 | Holdings show T+1, delivered/DP, available and collateral quantities | Preserve separate buckets; do not collapse into one settled/available quantity |
| AT-054 | Derivatives carry forward while day activity is flat/closed | Keep opening/overnight position and day activity distinct |
| AT-055 | Dhan ledger has debit/credit entries and voucher numbers | Verify per-entry signed amounts and running-balance arithmetic; retain voucher identity |
| AT-056 | Dhan trade record includes per-trade tax/charge fields | Preserve raw fields separately and reconcile against actual statement/contract note |
| AT-057 | A pay-in is PENDING or FAILED | Do not count it as posted cash credit; retain transaction ID/status |
| AT-058 | Funds snapshot has available, collateral, utilised and withdrawable values that differ | Preserve each provider-defined component; do not flag a mismatch by comparing unlike buckets |
| AT-059 | Kite virtual contract-note calculator produces a charge total | Label as calculated/virtual estimate; do not substitute for an issued contract note |
| AT-060 | Upstox charge report returns aggregate charges without per-trade allocation | Reconcile at its documented aggregate scope; do not invent per-trade charge splits |
| AT-061 | Actual contract note arrives with a charge total different from the earlier calculator estimate | Keep the issued note as posted-charge evidence; retain estimate and record the variance |
| AT-062 | Contract note is missing after the applicable delivery window | CONTRACT_NOTE_MISSING; no synthetic note generated |
| AT-063 | Contract note total agrees but one individual execution line is missing/mismatched | CONTRACT_NOTE_TRADE_LINE_MISMATCH; total agreement does not close line-level completeness |
| AT-064 | Upstox historical trades have a nullable/empty trade ID for a segment | Preserve record; use a separately validated composite/statement identity or remain UNKNOWN; do not use empty ID as dedupe key |
| AT-065 | Historical trade endpoint uses multiple pages and a middle page is unavailable | SOURCE_PAGINATION_INCOMPLETE; no period-level PASS |
| AT-066 | Trade date and settlement date straddle a calendar/session boundary | Apply date-valid settlement rules and keep both dates; no blanket same-day settlement assumption |
| AT-067 | Corporate action, exercise/assignment, expiry, pledge or settlement changes position without an ordinary trade | Require explicit non-trade adjustment evidence; otherwise UNEXPLAINED_POSITION_ADJUSTMENT |
| AT-068 | Cash ledger running balance does not equal opening plus signed posted entries | LEDGER_RUNNING_BALANCE_VARIANCE; preserve original amounts and source evidence |
| AT-069 | Same trade appears in tradebook, P&L report and contract note | Deduplicate economic execution by validated identity while retaining all source observations |
| AT-070 | API numerics arrive as binary floating values or decimal strings with different scale | Preserve raw input/scale and exact decimal result; no binary-float contamination |
| AT-071 | Broker P&L, trade charges, cash ledger and margin snapshot show different totals because scopes differ | Keep each measure separately typed and explain scope; do not force one total to equal another |
| AT-072 | Depository statement or exchange balance message conflicts with broker holdings/ledger | Raise external-evidence variance; retain both versions and require review |
| AT-073 | Funds snapshot is fetched at a different time from ledger/position data | Store each capture timestamp; do not treat snapshots as one atomic account state |
| AT-074 | Charge tariff/rate changes across effective dates or segments | Calculate using the applicable dated schedule; do not back-apply current rate to historical trades |
| AT-075 | Unresolved order from PX-024/025 later creates a fill that changes the account position/ledger | Link the recovered fill into execution, position and cash reconciliation; preserve the original UNKNOWN interval and resolution provenance |

PX-025 now has **48 normative requirements and 75 proposed acceptance scenarios** (AT-001 through AT-075). These are proposed tests and were not executed.

## 11. Open questions and limits

- The reviewed Kite Connect docs expose a virtual charge calculator but no general cash-ledger statement endpoint; other broker reports or non-Connect channels may exist.
- Upstox historical trades are documented for the last three financial years; longer retention/export and contract-note delivery mechanism were not established here.
- Upstox's documented charges endpoint returns an aggregate breakdown; no authoritative trade-level allocation mapping was established by this review.
- Dhan's ledger/trade history is exposed through APIs, but the reviewed page does not itself state that this output is identical to the issued contract note.
- Exact trade correction/bust/charge adjustment and post-trade contract-note revision semantics remain open from PX-027.
- Settlement and depository records depend on effective dates, product, security and exchange rules; no universal settlement-cycle constant is adopted.
- Cash balance, available margin, withdrawable balance, collateral and unsettled receivables require provider-specific definitions; no common arithmetic is assumed.

## 12. Research decisions and non-authorization

- **ACCEPT:** separate order, trade, position, holdings, ledger, charge/contract-note, funds/margin and external-verification layers.
- **ACCEPT:** explicit roll-forward and cash-ledger arithmetic with source-linked non-trade adjustments.
- **ACCEPT:** actual contract notes/statements are distinct from estimated charge calculators.
- **ACCEPT:** preserve T+1/DP/available/collateral quantity buckets and date-valid settlement evidence.
- **ACCEPT:** preserve raw numeric representations and use exact-decimal derived accounting.
- **DEFER:** final accounting schema, charge allocation algorithm, settlement policy registry and exact source-of-truth implementation.
- **NOT AUTHORIZED:** broker connections, sandbox/production calls, real orders, code changes, paid data/services, credential/IP changes, PR creation or merge to `main`.

**Final status:** PX-028 economic account reconciliation audit documented. PX-025 refined to 48 requirements and 75 proposed acceptance scenarios. No broker API, account, sandbox, real order, or implementation was used.
