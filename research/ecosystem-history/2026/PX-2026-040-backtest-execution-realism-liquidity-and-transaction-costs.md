# PX-2026-040 — Backtest execution realism, liquidity and transaction-cost controls

**Research date:** 2026-11-08  
**Status:** NSE execution-cost, price-range, settlement and statutory-charge sources reviewed; no order-book history, quote archive or backtest executed  
**AlgoX area:** backtest fill model / liquidity and market impact / price protections / fees and taxes / cash settlement and auction risk  
**Scope:** NSE cash equities and equity derivatives; broker/account-level cost inputs remain configurable  
**Inputs:** PX-025 R-001–R-216; PX-028 ledger/contract-note reconciliation; PX-029 physical settlement; PX-030 margin; PX-033 admission gates; PX-034 order validation; PX-037 market data; PX-038 historical price integrity; PX-039 point-in-time universe  
**Mode:** research and requirements specification only  
**Non-goals:** no live/depth market data request, no broker API call, no account/member portal access, no order, no backtest run, no implementation, no paid service, no PR or merge to main

## Executive finding

A realistic backtest cannot assume that every signal fills at the bar close, at LTP, or at one fixed slippage percentage. NSE's impact-cost definition is order-size-specific, side-specific and dependent on the outstanding order book. Exchange price protections can reject an otherwise risk-approved order. Actual statutory and exchange costs depend on segment, side, product, trade value/premium base and effective date. Cash-market delivery has settlement and possible auction/close-out consequences that do not occur in every intraday or derivatives trade.

The audit establishes five separate layers:

1. **Execution opportunity:** whether the order could have reached the market and traded during the relevant session, considering session state, price range, LPP, available quantity and time priority.
2. **Market execution cost:** bid/ask spread, depth consumption, impact cost, partial fills, residual quantity and market movement while working.
3. **Exchange/statutory charges:** exchange transaction charges, IPFT contribution, SEBI turnover fee, STT, stamp duty and applicable GST.
4. **Broker/account costs:** brokerage tariff, DP/depository charge, funding/interest, product-specific charges and account plan.
5. **Settlement tail costs:** funds/securities shortage, valuation debit, auction/close-out or other delivery-related outcome where the simulated position actually creates that risk.

These layers must be separately modelled and separately reported. A single flat slippage or all-in cost percentage hides the execution assumptions and makes historical results difficult to reproduce.

**Important source-derived current fee changes:**
- NSE Circular NSE/FA/73061 (27 February 2026) revises transaction charge/IPFT composition from **1 March 2026** while keeping aggregate Trading Member outflow unchanged: cash ₹307/crore each side; equity futures ₹183/crore each side; equity options ₹3,553/crore traded premium each side. The circular's figures are exchange/member-level schedule values, not a complete client invoice.
- NSE's current STT page reflects the Finance Act 2026 rates from **1 April 2026**: stock-option sale 0.15% on option premium (seller), option exercise 0.15% on intrinsic value (purchaser), and equity futures sale 0.05% (seller). The relevant taxable base and liable side differ by event.
- Stamp duty is separately collected from the buyer at the applicable product rate; SEBI turnover fee is separate again.

The exact broker invoice can only be reconciled against the selected broker/account tariff and issued contract note. A backtest must pin all effective rate schedules and its chosen fill model.

## 1. NSE impact cost and liquidity

### 1.1 Impact cost is an order-size-specific market cost

NSE describes impact cost as the transaction cost attributable to lack of liquidity, distinct from fixed costs such as brokerage, transaction charges and depository charges.

The NSE page states that:
- impact cost is computed for a specified stock and a predefined transaction size at a point in time;
- buying and selling are computed separately;
- it depends on transaction size and outstanding orders in the order book;
- it changes dynamically with the order book;
- a penal impact cost is applied where the stock is not sufficiently liquid.

The page's example compares an ideal price based on the best bid/offer midpoint with the average price required to execute a specified quantity through the available book. It illustrates that an order consuming multiple ask levels has an average buy price above the ideal midpoint.

This is a useful execution-cost concept, but it is not a universal cost rate. Index eligibility methodology may use an impact-cost statistic for a defined portfolio size and observation sample; that index eligibility statistic must not be copied as an execution-cost curve for every order, time or broker.

Source:
- https://www.nseindia.com/static/products-services/indices-impact-cost

### 1.2 Side and depth matter

A buy and a sell of the same size can have different impact because:
- the best bid/ask spread can be asymmetric;
- visible depth at successive price levels differs;
- depth can change between observation and order arrival;
- a large order can consume multiple levels;
- an order may be only partially executable at its limit price;
- other orders have priority ahead of the simulated order.

For a depth-based simulation, the model should preserve the book snapshot time, side, price levels, quantity available at each level, requested quantity, executed quantity and residual. A midpoint-to-book-VWAP impact measure can be reported as a diagnostic, but the actual fill simulation must also consider the order type, limit price, price-time priority and order lifetime.

Impact cost should not be added twice if the simulated fill price already consumes the bid/ask and depth. A model must identify whether it applies spread/impact through the fill price or as a separate cash cost.

### 1.3 Market volume is not order-book depth

Daily traded volume, intraday bar volume and visible quote depth are different observations:
- bar volume measures transactions over an interval;
- cumulative traded volume measures activity over the session;
- quote depth represents resting quantities at a snapshot;
- hidden/iceberg/reserve liquidity and subsequent cancellations can alter actual executable quantity.

A volume-participation limit is a backtest policy, not a fact inferred from the bar. It must be configured and reported. Where historical depth is unavailable, the backtest must use a declared bar-based approximation and must not claim queue-aware or order-book-accurate fills.

## 2. Exchange price protections and rejection effects

### 2.1 Price band, operating range and LPP are separate controls

NSE publishes distinct mechanisms:

- **Cash-market price bands:** daily bands for eligible securities, commonly 2%, 5%, 10% or 20% as assigned by the exchange. Securities with derivatives have a separate dynamic operating-range treatment under NSE's published framework; do not assume a standard cash-market circuit band applies identically to every derivative-eligible share.
- **Futures operating range:** NSE's derivatives page describes a 10% base operating range for index and individual-security futures, which can be flexed under the applicable process.
- **Options operating range:** NSE describes a contract-specific delta-based price range computed and updated daily.
- **Limit Price Protection (LPP):** an additional limit-price validation in the F&O segment, over and above the operating price range. The current NSE FAQ says an incoming limit order outside LPP is rejected.

A valid local strategy/risk admission does not mean the exchange will accept the price. Backtest execution must model the effective price constraint and rejection outcome separately from the strategy's desired limit price.

Sources:
- https://www.nseindia.com/static/products-services/equity-market-price-bands
- https://www.nseindia.com/static/products-services/equity-derivatives-price-bands
- https://www.nseindia.com/static/trade/price-band-operating-range-flex-faqs
- https://www.nseindia.com/static/trade/limit-price-protection-faqs

### 2.2 Dynamic LPP reference and stop-limit treatment

NSE's LPP FAQ describes:
- theoretical reference pricing at market open using the underlying cash pre-open price, benchmark interest rate and, for options, Black-Scholes with the appropriate volatility; if the underlying is unavailable, the contract base price is used;
- during trading, reference price based on the simple average of contract trade prices over the last 30 seconds, revised at 30-second intervals when there has been trading;
- if there is no trade for 30 seconds, the reference is not revised; if there is no trade for 15 minutes after the last update, theoretical price from the latest underlying/base price is used;
- LPP applies to permitted order types with a limit price;
- for SL-Limit, LPP validation is applied after the trigger when the order is released into the regular limit-order book;
- a modification outside LPP is rejected and the original pre-modification order remains in the book;
- passive outstanding orders remain in the order book when the LPP range flexes, retaining price-time priority.

The FAQ's numeric LPP parameter table is source-versioned and is not treated here as an evergreen constant. It explicitly says the Exchange may review and modify parameters through circulars. Operational use must load the current effective broadcast/circular values for the contract and time.

A backtest must model an LPP rejection as an unfilled order, not silently clamp its price into range. A rejected modification does not cancel the original order. A flexed range does not erase passive orders already resting in the book.

Source:
- https://www.nseindia.com/static/trade/limit-price-protection-faqs

## 3. Transaction charges, taxes and broker costs

### 3.1 NSE transaction charges and IPFT contribution

NSE Circular NSE/FA/73061, dated 27 February 2026, states that revised transaction charges and NSE IPFT contributions apply from **1 March 2026**. The circular says the exchange rolled back the IPFT contribution increase made in 2023 and revised transaction charges to preserve the same total Trading Member outflow.

| Segment | Transaction charge | NSE IPFT contribution | Total outflow in circular |
|---|---:|---:|---:|
| Cash market | ₹306.99/crore each side | ₹0.01/crore each side | ₹307/crore each side |
| Equity futures | ₹182.99/crore each side | ₹0.01/crore each side | ₹183/crore each side |
| Equity options | ₹3,552/crore traded premium each side | ₹0.01/crore traded premium each side | ₹3,553/crore traded premium each side |

These are the circular's Trading Member outflow rates. They are not the complete amount charged to every client; broker billing/pass-through and tax invoice presentation must be taken from the applicable broker/account tariff and actual contract note. For a backtest, preserve the exchange rate schedule and avoid charging both the total outflow and its transaction/IPFT components as separate totals.

Sources:
- NSE Circular NSE/FA/73061 (27 February 2026): https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies

### 3.2 STT is date-, side-, product- and event-specific

NSE's STT page reflects the Finance Act 2026 schedule from 1 April 2026. The reviewed table includes:
- sale of stock option: 0.15% on option premium, payable by seller;
- exercise of option: 0.15% on intrinsic value, payable by purchaser;
- sale of equity futures: 0.05%, payable by seller.

Prior rates appear separately for earlier effective periods. STT is not one generic percentage applied to every buy and sell cash flow. Option sale premium and option exercise intrinsic value are different tax bases.

The cost engine must use the event date, trade/settlement type, segment, side and applicable statutory schedule. Do not back-apply the 2026 rates to trades before their effective date.

Source:
- https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax

### 3.3 Stamp duty and SEBI turnover fees are separate

NSE's investor levy schedule lists buyer-side stamp duty separately by transaction type, including:
- equity delivery: 0.015%;
- equity non-delivery: 0.003%;
- equity futures: 0.002%;
- equity options: 0.003%.

NSE's levy page lists SEBI turnover fees of 0.0001% (₹10 per crore) for applicable purchase and sale transactions other than debt securities.

These rates must be interpreted against the applicable trade segment, transaction base and current government/exchange schedule. Stamp duty is not STT; SEBI turnover fees are not exchange transaction charges.

Sources:
- https://www.nseindia.com/static/invest/first-time-investor-stamp-duty-charges-taxes
- https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies

### 3.4 Brokerage, GST, DP/depository and funding

These costs cannot be safely hard-coded from one exchange table:
- brokerage varies by broker, account tariff, product, order type and date;
- GST applies under the relevant tax rules to the applicable taxable service/charge base, not as an arbitrary percentage on every debit;
- DP/depository transaction charges can depend on broker tariff, delivery sale and account plan;
- margin funding/interest depends on broker terms, financed balance and time;
- collateral haircuts and blocked margin have opportunity cost even if they are not a posted fee;
- borrow/SLB or other stock-borrow availability/cost must be explicit for a cash short strategy.

The backtest must either pin the real broker/account fee schedule or label the run as using a generic cost scenario. A generic fee model must not be presented as an actual client contract-note reproduction.

## 4. Cash settlement, short delivery and auction tail risk

NSE Clearing describes a T+1/T+0 rolling settlement cycle:
- for T+1, final obligations are generated by 8:30 a.m. on the next working day; settlement is on the T+1 working day, excluding intervening bank/exchange holidays, Saturdays and Sundays;
- for T+0 eligible securities, trading is described until 1:30 p.m.; obligations are determined by 2:30 p.m.; non-custodial sell pay-in is through early-pay-in block by 1:45 p.m.; securities pay-in cutoff at depositories is 3:30 p.m.; payout occurs later the same day;
- no T+0 trading occurs for T+0 securities on a settlement/bank holiday.

The T+0 scheme is optional/eligibility-specific; it must not be assumed for every cash equity. The current effective settlement calendar and eligible-security list must be pinned.

NSE shortage handling states:
- at settlement, securities shortages are identified and the member is debited a valuation amount for securities not delivered;
- a buy-in auction is conducted on T+1 after payout;
- if auction purchase price exceeds valuation price, the clearing member makes good the difference;
- shortages not bought in are closed out;
- for normal-market delivery shortfall, close-out is the higher of the highest price across exchanges from trade date through auction day or 20% above auction-day settlement price, subject to the applicable rule;
- corporate-action and deleted-security shortages can have special close-out handling.

This is a tail settlement cost, not the default cost of every sale. A backtest should invoke it only when its simulated settlement position creates a delivery shortage or the strategy's explicit short-delivery/default scenario requires it. It must not treat a normal successfully delivered sell as an auction.

Sources:
- https://www.nseindia.com/static/products-services/equity-market-settlement-cycle
- https://www.nseindia.com/static/products-services/equity-market-shortages-handling
- https://www.nseindia.com/static/products-services/equity-market-data-reports-download

## 5. Execution model requirements for research

### 5.1 Order types need different fill semantics

A future backtest engine should distinguish at least:
- marketable market/limit order that consumes visible liquidity;
- passive limit order that waits behind existing quantity at its price;
- stop-limit order that activates only after trigger and may then be rejected/unfilled;
- stop-market order whose execution price can gap beyond the trigger, subject to provider/exchange protection;
- iceberg/auto-sliced or multi-child order whose fills and failures are tracked per child;
- auction/pre-open orders with their own session and matching rules.

A bar high/low touching a limit is not proof of a fill. The data may not reveal whether the order arrived before or after the high/low, how much queue was ahead, whether sufficient opposing quantity traded at the limit, or whether a price range rejected the order. The engine must declare an execution model and its limitations.

### 5.2 Partial fills and residual orders

Each simulated order should track:
- submitted time/price/quantity;
- eligible session/order type;
- queue/priority assumptions;
- each fill time/price/quantity;
- unfilled residual quantity and remaining lifetime;
- cancel/modify/expiry/rejection;
- exchange price range/LPP state;
- cost and tax allocation to each fill;
- post-fill position and settlement obligation.

An order that cannot be filled fully must remain partially filled or unfilled. Do not force the full requested quantity into the portfolio because the strategy emitted a signal.

### 5.3 Participation and capacity

For a bar-only simulation, an explicit maximum participation policy can limit fills relative to the observed bar/session volume. This parameter is a simulation assumption, not an NSE default. It must be recorded with results and tested for sensitivity. If exact order-book/depth data is unavailable, the backtest must not claim depth-based impact accuracy.

### 5.4 Cost stack is componentized

The cost engine should return separate components:
- spread cost;
- market impact/slippage;
- brokerage;
- exchange transaction charges;
- IPFT contribution;
- SEBI turnover fee;
- STT;
- stamp duty;
- GST;
- DP/depository charges;
- borrow/funding/interest;
- margin opportunity cost (reported separately from posted fees);
- delivery-shortage/auction/close-out cost if triggered.

A net P&L report must show gross and net results and enough component detail to reproduce the net value. Never deduct a cost in the execution price and again as a separate fee.

## 6. Additional requirements for PX-025

### R-217 — Execution cost and fixed charges are separate

The system MUST distinguish spread, order-book impact and price slippage from brokerage, exchange transaction charge, IPFT, SEBI fee, STT, stamp duty, GST, DP/depository, funding and settlement-shortage costs. Impact cost MUST NOT be treated as a fixed statutory fee.

### R-218 — Impact cost is side-, size- and time-specific

Any impact-cost estimate MUST retain buy/sell side, reference price definition, requested order size, book/volume snapshot time and source, executable levels and average execution price. A single universal impact-cost percentage MUST NOT be treated as accurate across instruments or order sizes.

### R-219 — Execution simulation uses price and quantity availability

A depth-based fill MUST be limited to the available executable quantity at each relevant price level and the order's price constraint. A quote or LTP alone MUST NOT establish fillable quantity. The model MUST preserve book snapshot time and avoid assuming depth remains available indefinitely.

### R-220 — Candle bars do not prove order-book fills

A bar-based backtest MUST declare how it handles intrabar path, order arrival, price-time priority and liquidity. A candle high/low touching an order price MUST NOT by itself be treated as a guaranteed fill or full fill.

### R-221 — Partial fills and residual orders are first-class

The simulated order lifecycle MUST preserve each partial fill, remaining quantity, working lifetime, rejection, cancellation, modification and expiry. A strategy signal MUST NOT cause the engine to assume all requested quantity traded.

### R-222 — Volume participation is an explicit model parameter

A bar-volume participation cap MUST be configured, versioned and reported as a backtest assumption. It MUST NOT be represented as an exchange-mandated percentage or inferred automatically from the signal size. Historical coverage and zero-volume cases MUST be respected.

### R-223 — Exchange price bands and operating ranges are admission constraints

The execution model MUST retain the effective security price band or derivatives operating range for the contract/date/session. An order outside the effective permitted range MUST be rejected/unfilled rather than clamped silently to the nearest band.

### R-224 — LPP is a distinct dynamic F&O validation layer

For applicable F&O limit-price orders, the model MUST treat LPP as an additional validation above operating price range and use the effective time-specific LPP parameters/reference. The LPP parameter values MUST be versioned and MUST NOT be hard-coded from an old FAQ table.

### R-225 — Stop-limit LPP is checked at trigger release

A simulated SL-Limit order MUST be revalidated against prevailing LPP when its trigger activates and it is released to the regular book. A rejection MUST remain an unfilled/rejected order; it MUST NOT be converted into an execution at a clamped price.

### R-226 — Rejected modifications preserve the original order state

Where LPP or another exchange validation rejects a modification, the model MUST preserve the pre-modification order state if the exchange rule says the original order remains in the book. It MUST NOT assume that a rejected modify cancelled the original order.

### R-227 — Passive orders survive range flex under source rules

When the applicable LPP process flexes its range, the engine MUST preserve existing passive orders and their price-time priority where the exchange rule says they remain. It MUST NOT silently cancel/reprice them due solely to LPP range flex.

### R-228 — Exchange charges and IPFT are effective-dated and segment-specific

The cost model MUST preserve exchange transaction charge and IPFT components separately with their segment, rate base, side and effective date. It MUST apply the 1 March 2026 NSE/FA/73061 schedule for applicable later trades and historical rates before that date, without double-counting the combined outflow and its components.

### R-229 — Statutory charges use the correct taxable base and liable side

STT and stamp duty MUST be computed from the applicable dated statutory schedule, product/event type, taxable base and liable side. Option premium sale, option exercise intrinsic value, futures sale, equity delivery and non-delivery MUST NOT be treated as one generic turnover charge.

### R-230 — SEBI turnover fee and GST remain separate components

The model MUST preserve SEBI turnover fee and applicable GST as separate charge components with their respective dated base/rules. GST MUST NOT be applied indiscriminately to all taxes/levies or double-counted in an exchange/broker total.

### R-231 — Brokerage and account-level charges are tariff-versioned

Brokerage, DP/depository charges, other broker fees, margin funding and account-specific rates MUST be represented by broker/account/product tariff version and effective date. A generic cost scenario MUST be labelled as such and MUST NOT be described as an actual client invoice.

### R-232 — Cost calculations use exact decimal and component-level rounding

Fees and statutory charges MUST retain raw taxable base, rate, currency, calculation precision and applicable component-level rounding rule. The engine MUST NOT round a combined percentage once if the actual tariff requires separate rounding by order, fill, side, segment or charge component.

### R-233 — Settlement calendar and T+0 eligibility are modelled explicitly

Cash-equity backtests MUST use the effective T+1/T+0 eligible-security list and settlement calendar, including holidays, pay-in/payout cutoffs and T+0 time restrictions. T+0 MUST NOT be assumed for all securities or sessions.

### R-234 — Short-delivery auction/close-out is a conditional tail event

The engine MUST distinguish normal successful delivery from securities shortage, valuation debit, buy-in auction and failed-auction close-out. It MUST apply the dated exchange close-out/auction rule only when the simulated settlement scenario creates the relevant shortage; it MUST NOT apply auction cost to every cash-market sale.

### R-235 — Gross/net P&L and no-double-count cost provenance are mandatory

Every backtest MUST report gross P&L and net P&L with component cost totals, execution-price assumptions, cost-model version, rates/tariffs and settlement events. A cost already embedded in fill price MUST NOT be charged a second time as an explicit fee.

## 7. Deterministic acceptance scenarios

These extend AT-001 through AT-400. Use synthetic books, OHLC bars, price-range states, fee schedules, settlement calendars and fake order/settlement outcomes only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-401 | Same size buy and sell consume asymmetric bid/ask depth | Calculate side-specific impact and fill price; preserve midpoint, book levels and size |
| AT-402 | A marketable buy exceeds the quantity at best ask and consumes deeper levels | Produce depth-weighted partial/multi-level fill; do not fill entire quantity at best ask |
| AT-403 | Requested quantity exceeds all visible executable depth | Fill only supported quantity and keep residual unfilled; no fabricated liquidity |
| AT-404 | LTP is present but bid/ask depth is missing | Do not treat LTP as executable quantity; use explicit lower-fidelity model or UNKNOWN |
| AT-405 | Order size grows while the same book snapshot is held constant | Model greater depth consumption/impact; do not reuse the same fixed slippage percentage |
| AT-406 | Order book changes between signal and simulated arrival | Use the arrival-time observation if available; otherwise record timing assumption/uncertainty |
| AT-407 | Bar high touches a buy limit but no trade/queue evidence exists | Do not guarantee fill from high alone; apply declared conservative bar-fill policy |
| AT-408 | Strategy signal is produced at the end of a bar | Do not fill at that same closing price without an explicit valid closing-auction/arrival model; default to next eligible observation |
| AT-409 | Stop-limit triggers after a gap but the limit price is no longer marketable | Record triggered-but-unfilled order; do not force execution at trigger |
| AT-410 | Marketable order has only partial fill before session close | Preserve partial execution and residual expiry/cancel; P&L uses filled quantity only |
| AT-411 | Configured participation cap is exceeded by candidate order | Limit simulated execution to the configured participation quantity and retain residual |
| AT-412 | Bar volume is zero or missing | No volume-based fill; return unfilled/UNKNOWN according to source completeness |
| AT-413 | F&O limit order price is inside OPR but outside current LPP | Reject order on LPP; do not assume OPR PASS implies exchange acceptance |
| AT-414 | SL-Limit order triggers when current LPP has moved | Validate at trigger-release time; reject if outside prevailing range |
| AT-415 | LPP rejects an order modification | Retain the original order in its prior state; do not mark it cancelled |
| AT-416 | LPP range flexes while passive orders are resting | Keep existing orders and their time priority if the effective rule retains them |
| AT-417 | Price-range validation changes during the session | Use time-effective range for each order attempt; do not backfill current range to earlier time |
| AT-418 | Cash equity has an effective 2%, 5%, 10% or 20% band and order price exceeds it | Reject/unfilled using that security's dated band |
| AT-419 | F&O future uses operating range and option uses a daily delta-based range | Use product-specific range; do not apply the cash security price band to the derivative contract |
| AT-420 | Exchange transaction charges change on 1 March 2026 | Apply the effective NSE/FA/73061 segment schedule from its start date and prior schedule before it |
| AT-421 | Equity option transaction charges are calculated on premium turnover | Use traded premium value rather than option notional value as the transaction-charge base |
| AT-422 | STT on an equity option sale and option exercise occurs in separate events | Apply the relevant dated rates and bases to seller premium sale and purchaser intrinsic-value exercise respectively |
| AT-423 | Equity futures sale occurs after the 1 April 2026 STT revision | Use the effective seller-side futures STT schedule; do not apply the option premium base |
| AT-424 | Stamp duty is assessed for delivery, non-delivery, futures and options | Apply correct buyer-side product/event base and separate it from STT |
| AT-425 | SEBI turnover fee is charged on both sides of an applicable transaction | Preserve the correct rate/base independently from NSE transaction/IPFT charge |
| AT-426 | Broker tariff or DP charge changes across dates/account plans | Select dated broker/account tariff; do not use current account tariff for historical periods |
| AT-427 | Brokerage, exchange charges, STT, stamp duty and GST are combined into one number too early | Preserve each component, taxable base and rounding; prevent double tax/cost |
| AT-428 | Cash equity settles T+1 across an intervening holiday | Calculate working-day settlement date and retain separate trade/settlement date |
| AT-429 | Eligible T+0 security is sold after the T+0 early-pay-in cutoff or on settlement/bank holiday | Do not assume T+0 settlement; apply effective cutoff/eligibility and mark obligation accordingly |
| AT-430 | Cash-market sale results in a short securities delivery and failed buy-in auction | Record valuation debit and applicable close-out tail cost; do not charge auction cost to ordinary successfully delivered trades |

PX-025 now contains **235 normative requirements (R-001–R-235) and 430 proposed acceptance scenarios (AT-001–AT-430)**. These are proposed tests only; no historical depth, fee file, order book or backtest was run.

## 8. Source limitations and open questions

1. No historical order-book depth or quote-level market-impact dataset was acquired; the backtest fill model cannot claim calibrated depth impact from this research alone.
2. NSE impact-cost page defines the concept and order-size dependence but does not supply a full historical executable order-book archive through this review.
3. LPP FAQ lists current parameters but says NSE may change them through circulars; the exact live parameter broadcast and historical parameter archive must be obtained before operational simulation.
4. The cash price-band and derivatives operating-range values can be revised/flexed; the relevant dated file/broadcast must be pinned by instrument and session.
5. NSE/FA/73061 is the revised transaction-charge/IPFT schedule effective 1 March 2026; broker/client pass-through, brokerage and account fees still require the dated broker tariff and actual contract note.
6. STT schedule is subject to Finance Act amendments and event-specific tax bases; rates must be verified for the historical trade date.
7. Stamp duty, SEBI fee, GST, DP/depository and funding/interest all require their specific effective rules and bases; this report does not claim a complete tax computation engine.
8. Settlement cycle pages can be updated and T+0 eligible-security coverage is date-specific. Current settlement/holiday and security eligibility files must be used for a given historical date.
9. Shortage/auction/close-out is conditional on settlement failure and product/security-specific rules; no shortage or auction occurred in this research.
10. No fill calibration, transaction-cost sensitivity analysis or backtest execution was performed.

## 9. Research decisions and non-authorization

- **ACCEPT:** separate market impact from fixed exchange/statutory/broker charges.
- **ACCEPT:** impact cost is side-, size-, time- and depth-specific; not a universal slippage constant.
- **ACCEPT:** an OHLC touch does not prove a queue-aware fill; partial fill and residual order states must be represented.
- **ACCEPT:** cash price bands, F&O operating range and LPP are distinct admission constraints.
- **ACCEPT:** current/date-effective NSE charge schedules, statutory taxes and broker/account tariffs remain separate.
- **ACCEPT:** T+1/T+0 settlement calendars and shortage auction/close-out tail risk must be modelled only in the relevant scenario.
- **DEFER:** execution-cost calibration, historical depth archive, production fill engine, tax/fee calculator and broker-specific cost tables until dated files/tariffs and suitable samples are obtained.
- **NOT AUTHORIZED:** broker connections, market data subscription, live orders, code implementation, paid services, credentials/IP changes, PR or merge to main.

**Final status:** PX-040 execution realism, liquidity and transaction-cost requirements documented. PX-025 expanded to 235 normative requirements and 430 proposed acceptance scenarios. No depth data, order book, broker API, backtest or code implementation was executed.
