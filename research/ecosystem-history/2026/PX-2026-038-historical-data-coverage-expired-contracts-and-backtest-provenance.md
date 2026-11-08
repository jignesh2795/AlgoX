# PX-2026-038 — Historical data coverage, expired contracts and backtest provenance

**Research date:** 2026-11-08  
**Status:** official provider historical-data and expired-instrument documentation reviewed; no historical API data was requested  
**AlgoX area:** historical market-data ingestion / expired-contract recovery / derivatives backtesting / adjustment lineage / deterministic replay  
**Providers:** Zerodha Kite Connect, Upstox V3 and expired-instrument APIs, DhanHQ v2 and expired-options API  
**Inputs:** PX-025, PX-029, PX-034–PX-037  
**Mode:** research and requirements specification only  
**Non-goals:** no broker/account access, historical API call, live feed, market subscription, sandbox/production interaction, order, code implementation, paid service, PR or merge to `main`

## Executive finding

Historical data availability, contract identity and data fidelity differ materially by provider. A backtest cannot treat every provider's historical candle endpoint as a common, complete history service.

The reviewed official documentation establishes:

- **Kite:** historical candles are available for several years at minute/3-minute/5-minute/10-minute/15-minute/30-minute/60-minute/day intervals. The optional OI field is separately requested. Its continuous-history option works for expired NFO/MCX **futures daily candles** using a live contract token; expired contract tokens are not available from the current instrument master unless previously cached. This is not a general expired-options or intraday continuous-history service.
- **Upstox V3:** supports custom minute (1–300), hour (1–5), daily, weekly and monthly intervals. Its documented availability starts January 2022 for minute/hour data and January 2000 for day/week/month data, with different maximum retrieval windows. Upstox also exposes expired futures/options contracts and a separate expired-contract candle route keyed by an expired instrument key; it documents 1-minute, 3-minute, 5-minute, 15-minute, 30-minute and daily expired-contract candles.
- **DhanHQ v2:** daily data is documented back to instrument inception; active-instrument intraday data supports 1/5/15/25/60-minute intervals over the last five years, with a maximum 90-day query window. Its expired-options API is a **rolling ATM-relative** dataset: last five years, up to 30 days per request, minute-level, and only the documented ATM±strike range. It is not equivalent to a complete historical archive of every fixed option contract and every strike.

The critical distinction is **exact expired-contract history versus rolling moneyness history**. Upstox's expired-instrument key represents an individual expired contract. Dhan's rolling-option endpoint selects strikes relative to ATM/spot at the time and returns the strike/spot series; the strike may therefore change through time. That is useful for a rolling-ATM strategy but cannot be treated as one fixed option-contract history.

**Decision:** every historical dataset must be classified by provider, source endpoint, exact contract or rolling selection rule, interval, date inclusivity, retention window, OI/IV availability, source capture time and response hash. A strategy/backtest must declare its required fidelity. Missing expired history, missing intervals or different provider coverage must remain visible; they must not be filled with zero/flat bars or silently spliced into another contract.

## 1. Provider historical-data capabilities

### 1.1 Zerodha Kite Connect

Kite's Historical Candle Data endpoint documents:
- intervals: minute, day, 3minute, 5minute, 10minute, 15minute, 30minute and 60minute;
- request start/end timestamps in `yyyy-mm-dd hh:mm:ss` format;
- candle records containing timestamp, OHLC and volume;
- `oi=1` to request open interest;
- `continuous=1` for a particular expired-futures history case.

Important expired-contract limitations:
- exchanges flush instrument tokens for futures/options contracts at every expiry;
- current Kite instrument master returns only live contract tokens;
- expired contract tokens are not retrievable from the live master unless the application regularly downloaded/cached them;
- `continuous=1` is documented for NFO and MCX futures and returns **day** candle records for expired contracts using a live contract token;
- this continuous mode must not be generalized to minute-level expired futures, options, equities or all exchanges.

Historical data is described as archived data up to date as of the time of access. The reviewed page does not establish a correction/revision feed or a universal corporate-action-adjustment guarantee for the returned OHLC history.

Sources:
- https://kite.trade/docs/connect/v3/historical/
- https://kite.trade/docs/connect/v3/market-quotes/

### 1.2 Upstox Historical Candle Data V3

Upstox V3 supports:
- minute intervals from 1 through 300;
- hour intervals from 1 through 5;
- daily, weekly and monthly interval units;
- history from January 2022 for minute and hour data;
- history from January 2000 for daily, weekly and monthly data.

The documented maximum retrieval windows are:
- minute intervals 1–15: one month;
- minute intervals greater than 15: one quarter;
- hourly intervals: one quarter;
- daily: one decade;
- weekly/monthly: no stated maximum window in the table.

V3 uses `instrument_key` and returns candle arrays with timestamp, OHLC, volume and OI. The documented timestamp indicates the start time of the candle. Start/end date parameters are documented as inclusive.

These are endpoint availability limits, not evidence that all instruments existed for the entire date range or that every interval contains a candle. Expiry, listing date, suspension and provider availability remain instrument-specific.

Source:
- https://upstox.com/developer/api-documentation/v3/get-historical-candle-data/

### 1.3 Upstox expired instrument history

Upstox documents separate APIs to:
- retrieve available expiries;
- list expired option contracts;
- list expired futures contracts;
- retrieve OHLC candles for an expired contract.

The expired candle route uses an `expired_instrument_key`, described as a combination of the normal instrument key and expiry date. It supports:
- 1minute;
- 3minute;
- 5minute;
- 15minute;
- 30minute;
- day.

The documented expired-candle start and end dates are inclusive. The page's response sample includes timestamp, OHLC, volume and OI. This is a contract-specific route and should be cross-referenced to PX-036's canonical contract ID before ingestion.

Do not mix the older general V2 historical-candle endpoint with V3 history as if its time coverage and retrieval limits were identical. The older Upstox historical candle page is marked deprecated; use the documented V3 route for supported active-contract history and the dedicated expired-instrument endpoint for expired-contract history, keeping their schemas/versioning separate.

Sources:
- https://upstox.com/developer/api-documentation/expired-instruments/
- https://upstox.com/developer/api-documentation/get-expired-historical-candle-data/
- https://upstox.com/developer/api-documentation/v3/get-historical-candle-data/
- https://upstox.com/developer/api-documentation/get-historical-candle-data/

### 1.4 DhanHQ v2 historical candles

Dhan's Historical Data APIs document:
- daily OHLCV data back to the date of instrument inception;
- daily data request through `/charts/historical`;
- daily `toDate` is non-inclusive;
- intraday `/charts/intraday` intervals of 1, 5, 15, 25 and 60 minutes;
- intraday history for the last five years for active instruments;
- maximum 90 days of intraday data in one request;
- timestamp as an epoch value;
- optional OI for derivative instruments.

This endpoint's coverage is described for active instruments. It must not be assumed to offer all expired-option/futures contract candles merely because a raw security ID once existed.

Source:
- https://dhanhq.co/docs/v2/historical-data/

### 1.5 DhanHQ expired-options rolling data

Dhan's `POST /charts/rollingoption` endpoint documents:
- up to five years of expired options data;
- minute-level data;
- a maximum 30-day date range per API call;
- index and stock options;
- OHLC, IV, volume, OI and spot information;
- expiry type/code and option side as request parameters;
- strike selection relative to ATM, including ATM±10 for index options near expiry and ATM±3 for other contracts.

The request uses a rolling moneyness selector such as `ATM`, not necessarily one immutable strike throughout the date range. The response includes a strike series and spot series alongside OHLC/IV/OI. A strategy that explicitly trades the ATM option each day may use this as a rolling selection dataset if the daily contract identity is reconstructed from the returned strike, expiry and contract master. A strategy that buys a particular fixed strike/expiry must not treat the rolling ATM series as that fixed contract's history.

The endpoint is not documented as a complete archive of every strike at every timestamp. Absence of an out-of-range strike is not proof that the option did not trade.

Source:
- https://dhanhq.co/docs/v2/expired-options-data/

## 2. Coverage comparison and required labels

| Source | Active-contract history | Expired-contract coverage | Key limit/meaning |
|---|---|---|---|
| Kite Historical | minute through daily documented intervals | continuous expired NFO/MCX futures daily candles only via `continuous=1`; expired tokens require prior cache for direct query | Not a general expired-option or expired-intraday archive |
| Upstox V3 Historical | minutes, hours, day, week, month | separate exact expired-instrument key candles at 1m/3m/5m/15m/30m/day | Date/interval limits differ by unit; expired endpoint is separate |
| Dhan Historical | daily from inception; active instrument intraday 1/5/15/25/60m, last 5 years | not established as full exact expired-contract history by this endpoint | Intraday query maximum 90 days |
| Dhan Expired Options | not an active-instrument endpoint | rolling ATM-relative index/stock option data, up to 5 years | Up to 30 days per call, ATM±bounded strike range; not a full fixed-strike archive |

A stored dataset must carry one of these coverage classes:
- `EXACT_CONTRACT_ACTIVE`;
- `EXACT_CONTRACT_EXPIRED`;
- `CONTINUOUS_FUTURES_DAILY`;
- `ROLLING_MONEYNESS_OPTIONS`;
- `UNDERLYING_DAILY`;
- `UNDERLYING_INTRADAY`;
- `UNKNOWN_COVERAGE`.

Do not blend coverage classes into one unlabeled “historical candles” table.

## 3. Historical retrieval manifest and reproducibility

Every historical retrieval should store:
- canonical instrument/contract ID;
- provider alias and exact historical API version/endpoint;
- coverage class (exact, continuous, rolling, underlying);
- source exchange/segment and instrument type;
- exact expired-instrument key or Dhan expiry/strike selector;
- interval/unit;
- request `from` and `to` parameters and inclusivity semantics;
- retrieval window limit and chunk sequence;
- request time and provider response time where available;
- source file/response bytes or canonical response hash;
- parser/schema version and response record count;
- first/last returned candle timestamps;
- missing/duplicate/out-of-order timestamp report;
- OI/IV/spot field availability;
- source correction/re-fetch version if later responses differ;
- corporate-action/continuous-series adjustment policy;
- backtest dataset snapshot ID.

A historical query manifest must permit the exact same retrieval scope and transformations to be reproduced. Since provider data can change between retrievals and the reviewed pages do not specify universal revision semantics, a backtest must pin the actual response snapshot rather than rely on a future query returning byte-identical values.

## 4. Date boundaries, pagination and request windows

Providers differ in date inclusivity:
- Upstox V3 standard and expired-candle pages describe `from_date` and `to_date` as inclusive;
- Dhan daily historical documentation explicitly says `toDate` is non-inclusive;
- Dhan expired rolling options also says `toDate` is non-inclusive;
- Kite takes timestamp `from`/`to` values but the reviewed page does not provide one universal inclusive/exclusive guarantee for every endpoint/interval.

A range planner must use a provider/version-specific boundary adapter. It must not copy one provider's date semantics to another. Adjacent chunks must be checked for overlap or gap; duplicate candles at a boundary must be reconciled by exact source key, while missing boundary candles remain visible.

Request windows must obey provider limits. Dhan intraday chunks must not exceed 90 days; Dhan rolling options chunks must not exceed 30 days; Upstox V3 chunks must obey per-unit/interval limits. The importer must assert requested coverage versus returned first/last timestamps and record all missing intervals.

## 5. Exact contract history versus continuous/rolling datasets

### 5.1 Exact contract history

An exact-contract history must use a canonical contract identity containing:
- exchange/segment/venue;
- underlying identity;
- future/option type;
- expiry;
- strike and option side for options;
- lot/multiplier and contract version.

The provider alias is resolved through PX-036 and its validity interval. Historical rows must not be remapped to a current contract simply because the provider's present instrument master has a similar symbol.

### 5.2 Continuous futures

A continuous futures series is a derived analytical object. It must identify:
- each constituent contract and its validity interval;
- roll schedule/rule (calendar, volume, OI or other);
- roll decision time and source data;
- whether prices are raw, ratio-adjusted, difference/back-adjusted or unadjusted;
- adjustment factor and exact effective boundary;
- volume/OI treatment at roll;
- whether the contract series is executable or research-only.

Never execute a live order against a continuous synthetic symbol. Order admission must resolve the actual listed contract.

### 5.3 Rolling ATM/relative-strike options

Dhan's rolling options dataset is moneyness-relative, not a static fixed-strike contract by default. It must be labelled with:
- underlying;
- expiry code/type;
- option side;
- moneyness selector/offset;
- actual strike for each returned observation;
- spot value and timestamp;
- contract master/lot/tick version for each actual strike;
- any change in contract identity as ATM migrates.

A backtest must decide whether its strategy truly selects a rolling ATM/relative strike at each decision point. If the strategy instead trades an exact fixed strike, a rolling series is the wrong dataset and cannot be substituted.

## 6. Corporate-action and adjustment provenance

The reviewed historical-data endpoint pages do not establish a common guarantee that raw OHLC data from all providers is adjusted identically for splits, bonuses, rights, dividends, mergers or derivative contract adjustments.

Therefore:
- preserve provider-returned raw OHLCV/OI/IV as the source observation;
- acquire applicable effective-dated corporate-action/contract-adjustment records separately;
- construct adjusted analytical series as a derived view with formula, adjustment factor, ex-date, source circular and policy version;
- never overwrite raw candles with adjusted values;
- keep cash dividends and contract adjustment semantics separate where their economic treatment differs;
- keep pre/post-adjustment price bases and resulting returns auditable.

PX-029 already establishes exchange-specific corporate-action adjustments for derivatives. PX-038 extends the data rule: historical-price adjustment must be explicit in the backtest dataset manifest, not assumed from provider name or endpoint.

## 7. Backtest execution fidelity and no-lookahead safeguards

Historical OHLC candles do not reveal the complete intrabar path, quote depth, queue position or exact sequence of trades. A candle-only backtest must not claim that a limit order would have filled merely because the candle range crossed its price.

A data/fill model must declare:
- source resolution (tick, quote/depth, minute candle, daily candle);
- whether order-book data exists;
- the fill model and its uncertainty;
- slippage/impact assumptions;
- bid/ask availability;
- market session, auction, halt and expiry handling;
- whether data is exact-contract, continuous futures or rolling moneyness;
- whether historical adjustments were applied.

For exact chronological replay:
- strategy decisions at time (t) may use only observations that would have been available by (t);
- a candle's final OHLC/volume/OI cannot be used before the candle closes;
- if the provider's candle timestamp denotes bucket start, use that boundary while preventing lookahead to final candle values;
- expired contract master/chain information and strike availability must be time-correct;
- future contract listings, later revisions and post-event adjustments must not leak into earlier decisions;
- incomplete/missing bars must remain incomplete, not be filled to make the strategy appear continuous.

The backtest result must separately report the amount of source data by fidelity class and the unresolved data gaps.

## 8. Additional requirements for PX-025

### R-178 — Historical datasets declare coverage class

Every historical dataset MUST be labeled as exact active contract, exact expired contract, continuous futures daily, rolling moneyness options, underlying daily/intraday or UNKNOWN. Coverage class MUST be retained at dataset and row level where relevant; different classes MUST NOT be blended into an unlabeled candle series.

### R-179 — Provider retrieval limits and date semantics are versioned

Every query adapter MUST encode provider/API-specific interval availability, maximum retrieval windows and date inclusivity. Dhan non-inclusive `toDate`, Upstox inclusive date ranges and Kite timestamp query parameters MUST remain distinct. Adjacent chunks MUST be checked for overlap/gaps.

### R-180 — Expired contract coverage is explicitly proven

An importer MUST use exact expired-instrument identifiers/keys or a provider-documented expired-contract endpoint before claiming exact expired-contract coverage. Kite continuous futures daily, Dhan rolling ATM-relative option history and active-contract historical candles MUST NOT be described as equivalent exact-contract archives.

### R-181 — Upstox expired contract keys are canonical-mapped

Upstox `expired_instrument_key` MUST be resolved to the PX-036 canonical contract using the underlying instrument key, expiry and complete contract terms. The key and expiry suffix MUST be preserved as source aliases, not parsed into a guessed symbol-only identity.

### R-182 — Dhan rolling options remain moneyness-relative

Dhan rolling-option records MUST preserve actual returned strike, spot, expiry selector, option side and time. They MUST be labeled ROLLING_MONEYNESS_OPTIONS and MUST NOT be used as fixed-strike exact-contract history unless each observation is individually reconciled to the exact listed contract.

### R-183 — Kite continuous data is restricted to its documented scope

Kite `continuous=1` MUST be used only under the documented NFO/MCX futures daily-candle semantics. It MUST NOT be treated as a general expired-option or expired-intraday data source. Any expired token not cached before expiry remains unresolved for direct token-based history.

### R-184 — Historical retrievals are immutable and reproducible

Every historical retrieval MUST persist query parameters, provider/API version, canonical/provider instrument identity, request/response times, response hash, parser version, record count, first/last timestamp and missing/duplicate-row report. A backtest MUST pin the actual dataset snapshot rather than re-fetching mutable history implicitly.

### R-185 — Candle timestamp and finalization semantics are respected

The importer MUST preserve provider candle timestamp, timezone/offset, interval and whether the timestamp denotes bucket start or another documented boundary. Strategies MUST NOT use final OHLCV/OI values before that candle would have closed.

### R-186 — OI/IV/spot fields remain nullable and source-scoped

Missing OI, IV, spot or option metadata MUST remain null/UNKNOWN, not zero. OI/IV/spot values from rolling options or one provider MUST NOT be attached to a different exact contract or time bucket without an authoritative mapping.

### R-187 — Historical data does not silently imply corporate-action adjustment

Raw provider candles MUST be preserved. Any split/bonus/rights/dividend/merger or derivative adjustment MUST be a separate effective-dated derived transformation with formula, factor, source circular and policy version. An undocumented provider adjustment must remain UNKNOWN.

### R-188 — Continuous futures construction is a versioned derived series

A continuous futures dataset MUST retain every constituent contract, roll trigger/date, price basis, adjustment method/factor, volume/OI policy and source history. It MUST never be represented as an executable contract identity.

### R-189 — Rolling moneyness is not a fixed contract

Any rolling ATM/relative-strike option series MUST retain the moneyness selector and actual strike/spot history. It MUST NOT be evaluated as a fixed-strike option strategy unless exact contract mapping is established per timestamp.

### R-190 — Query chunk coverage is verified

For any historical API with maximum date windows, the importer MUST split requests into compliant chunks and verify all expected boundaries, record counts and timestamp continuity. Missing or failed chunks MUST remain explicit; adjacent requests MUST not double-count overlap candles.

### R-191 — OHLC-only data cannot prove intrabar execution

A candle-only backtest MUST declare its execution/fill model and MUST NOT infer a guaranteed limit/stop fill or queue position solely from the bar's high/low. Tick/depth fidelity and candle fidelity MUST be reported separately.

### R-192 — Backtest replay is as-of and no-lookahead

Every strategy decision MUST use only data, contract listings, expiry/adjustment metadata and finalized bars available at that decision time. Dataset revision, future contract master, final candle values before close or later corporate-action knowledge MUST NOT leak into an earlier simulation.

## 9. Deterministic acceptance scenarios

These extend AT-001 through AT-340. Use synthetic historical responses, expired-contract keys, exact/rolling option fixtures and fake backtest datasets only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-341 | Kite minute/day historical query includes OI only when the OI parameter is enabled | Preserve absent OI as null; do not default to zero |
| AT-342 | Kite continuous=1 is requested for an expired NFO futures day series | Accept only the documented daily continuous-futures coverage class |
| AT-343 | Kite continuous=1 is requested for expired option minute candles | Reject/UNKNOWN; do not claim documented support |
| AT-344 | Kite expired token was not captured before expiry | Direct token-based historical retrieval remains UNKNOWN/unavailable |
| AT-345 | Upstox V3 requests 1-minute history for a period exceeding one month | Split into compliant windows and verify all requested timestamps |
| AT-346 | Upstox V3 requests 30-minute data over a period exceeding one quarter | Split according to documented maximum retrieval window |
| AT-347 | Upstox V3 requests hourly data over more than one quarter | Split by quarter and verify boundary candles |
| AT-348 | Upstox V3 requests daily data over more than one decade | Split into date windows without overlap or gaps |
| AT-349 | Upstox V3 minute history before January 2022 is requested | Return unsupported/UNKNOWN rather than padding missing history |
| AT-350 | Upstox expired instrument key includes a specific contract expiry | Resolve key to exact PX-036 contract identity and preserve expiry suffix |
| AT-351 | Upstox expired 1-minute/3-minute/5-minute/15-minute/30-minute/day candle request | Accept only documented interval set and store source version |
| AT-352 | Upstox expired date range start and end boundaries are inclusive | Respect inclusive range and deduplicate adjacent chunk boundaries by exact bar key |
| AT-353 | Dhan intraday active-instrument query spans more than 90 days | Split into <=90-day chunks; no lost days |
| AT-354 | Dhan daily historical query uses toDate as non-inclusive | Exclude toDate per source semantics; retain the query boundary |
| AT-355 | Dhan expired-option query spans more than 30 days | Split into <=30-day chunks and reconcile all date boundaries |
| AT-356 | Dhan rolling ATM option series changes actual strike as spot moves | Preserve each actual strike/spot and classify the dataset as rolling moneyness |
| AT-357 | Strategy requests a fixed 22,000-strike option but Dhan rolling ATM history shifts between strikes | Reject dataset as non-equivalent unless each timestamp is mapped to the requested fixed contract |
| AT-358 | Dhan rolling-option query requests ATM+10 for index options near expiry | Validate selector against documented near-expiry index strike range |
| AT-359 | Dhan rolling-option query requests ATM+4 for a non-index/other contract where maximum is ATM+3 | Reject unsupported selector; no extrapolation |
| AT-360 | Exact expired option history is absent from one provider but rolling ATM history exists from another | Keep coverage classes distinct; do not substitute rolling data for exact fixed-contract history |
| AT-361 | Historical provider returns no OI for some bars but OHLCV exists | Preserve OI as null for missing bars and flag completeness; do not forward-fill OI |
| AT-362 | Historical response returns candle timestamps in reverse chronological order | Normalize/order by timestamp only after validating uniqueness; preserve raw response order and report |
| AT-363 | Two adjacent chunks return one overlapping candle | Deduplicate by full source/bar key while retaining both response provenance records |
| AT-364 | Adjacent chunks omit a boundary candle | Record a coverage gap; do not synthesize a flat bar |
| AT-365 | Corporate action changes historical price basis after raw data retrieval | Keep raw bars unchanged and create a separate effective-dated adjusted view with factor/source provenance |
| AT-366 | Continuous futures roll switches from old to new contract | Retain each raw contract series and apply only the declared roll/adjustment policy |
| AT-367 | Backtest uses a final candle's high/low before its interval closes | Detect lookahead and fail the backtest validation |
| AT-368 | OHLC candle high/low crosses a limit price but no tick/depth evidence exists | Use the declared probabilistic/conservative fill model; do not claim a guaranteed fill |
| AT-369 | Historical contract is absent from current instrument master but existed at historical date | Resolve through historical contract/expired key snapshot, not current master or fuzzy symbol |
| AT-370 | Historical dataset is re-fetched and values differ from the pinned source snapshot | Preserve original backtest dataset hash; create a new data revision and do not silently rewrite prior result |

PX-025 now contains **192 normative requirements (R-001–R-192) and 370 proposed acceptance scenarios (AT-001–AT-370)**. These are deterministic proposed scenarios; no historical API request or backtest was executed.

## 10. Open questions and evidence limitations

1. Provider candle correction/revision semantics and any late correction window are not fully established by the reviewed public pages.
2. Kite's historical API date-range inclusivity/correction behaviour is not stated as one universal rule for every interval.
3. Upstox expired-contract history and its current API route use a V2 path while its active historical API has V3; both schemas must be versioned independently.
4. Dhan rolling-option data has moneyness-relative coverage and is not a complete archive of every exact strike; exact expired futures coverage was not established from the reviewed v2 pages.
5. None of the three reviewed historical-data pages establishes a common corporate-action-adjustment guarantee for all raw OHLC histories.
6. No real historical response samples were downloaded to measure row ordering, missing sessions, duplicate rows or provider revisions.
7. Backtest fill realism remains bounded by data fidelity. OHLC-only histories cannot establish queue position, bid/ask path or exact intrabar execution.

All remain open until source-specific response fixtures and versioned contract/adjustment records are acquired.

## 11. Research decisions and non-authorization

- **ACCEPT:** every historical source has an explicit coverage class and provider-specific request/date semantics.
- **ACCEPT:** use Upstox exact expired-instrument candles where available; map to canonical contract identity.
- **ACCEPT:** Dhan rolling-option history is only valid for rolling-moneyness strategies unless exact strike mapping is reconstructed per timestamp.
- **ACCEPT:** Kite continuous expired-futures history remains daily-only in the reviewed API.
- **ACCEPT:** preserve raw bars and derive adjusted/continuous series separately with lineage.
- **ACCEPT:** backtest datasets are immutable snapshots; re-fetch creates a new revision, not a silent overwrite.
- **ACCEPT:** no-lookahead and execution-fidelity declarations are mandatory.
- **DEFER:** provider correction/revision semantics, corporate-action adjustment parity and exact data availability at all historical dates until source fixtures and circulars are inspected.
- **NOT AUTHORIZED:** broker/history API calls, account/sandbox/production access, orders, code changes, paid data, credential/IP changes, PR or merge to `main`.

**Final status:** PX-2026-038 historical-data coverage, expired-contract retrieval and backtest provenance research documented. PX-025 expanded to 192 requirements and 370 proposed acceptance scenarios. No historical API or backtest was executed.
