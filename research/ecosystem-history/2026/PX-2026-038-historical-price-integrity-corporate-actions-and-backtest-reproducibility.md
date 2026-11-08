# PX-2026-038 — Historical price integrity, corporate actions and backtest reproducibility

**Research date:** 2026-11-08  
**Status:** official NSE historical-data catalogue, bhavcopy-format chronology, corporate-action disclosures and index total-return references reviewed; no historical files downloaded or reconciled  
**AlgoX area:** historical data lake / EOD prices / corporate actions / total returns / point-in-time backtesting / dataset provenance  
**Scope:** NSE Capital Market, Equity Derivatives and index historical data  
**Inputs:** PX-025 R-001–R-178; PX-028 accounting reconciliation; PX-029 derivatives corporate actions/settlement; PX-034/035 contract master ingestion; PX-036 instrument identity and PX-037 market-data timestamps  
**Mode:** research and requirements specification only  
**Non-goals:** no historical data download, no member/extranet login, no broker API or market feed, no backtest execution, no code implementation, paid service, PR or merge to main

## Executive finding

Backtest price integrity depends on more than receiving a sequence of OHLC candles. For NSE instruments, the public reporting catalogue exposes several different data products and historically changed its dissemination formats. Corporate actions create additional representations of a price series. Derivatives have close, last traded price and settlement-price values that answer different questions. Index Price Return and Total Return series are distinct. A strategy tested on the wrong representation can appear to generate returns that could not have been earned.

The source review supports these core decisions:

1. **Actual bhavcopy prices and adjusted reference prices are separate.** NSE explicitly states that adjusted 52-week high/low values are adjusted for bonus, consolidation, splits and rights, while actual unadjusted 52-week high/low prices should be taken from bhavcopy.
2. **Daily EOD report formats are effective-dated.** NSE states that legacy CM/F&O common/bhavcopy CSV reports were discontinued from 8 July 2024 in favour of the relevant UDiFF Common Bhavcopy Final ZIP. Later, NSE Circular NSE/MSD/74764 (18 June 2026) says website .DAT bhavcopies will also be made available through Extranet in a phased manner from July 2026; the older .MS/.MD Extranet reports and related NNF API broadcast formats are discontinued effective 12 October 2026.
3. **Cash-equity adjustment and derivative contract adjustment are not the same thing.** NSE's derivatives corporate-action methodology adjusts open derivative positions and contract specifications to preserve position value across cum/ex dates. It is not a blanket instruction to rewrite cash-market OHLC history.
4. **Price return and total return are different.** NSE explains that a Price Index reflects constituent price movements, while a Total Returns Index also includes dividend receipts and reinvests indexed dividends on ex-dates. Do not compare a price-only backtest against a total-return benchmark or double-count dividends.
5. **F&O close, LTP and daily settlement price must remain separate.** NSE's historical contract-wise price/volume archive displays Open/High/Low/Close, LTP, Settle Price, contracts, turnover, OI, change in OI and underlying value as separate fields. Futures MTM and backtest mark/exit pricing must use the appropriate field for the use case.
6. **Historical contract identity and data vintage are part of each observation.** Expiry-specific contracts, historical symbols, UDiFF format changes, corrected files and corporate-action successor instruments must be preserved. A current instrument master or current symbol cannot rewrite old market data.
7. **A backtest must be reproducible from a pinned data manifest.** Preserve source artifacts and hashes, schema versions, data vintage, corporate-action policy, roll policy, point-in-time universe, date/time calendar and adjustment-builder version.

**Limitation:** no NSE daily bhavcopy, UDiFF ZIP, .DAT file, contract-wise price/volume archive, corporate-action attachment or historical constituent file was downloaded or parsed in this pass. The findings establish source families and methodological distinctions, not a validated production dataset.

## 1. NSE daily market-data and historical archive inventory

### 1.1 Capital Market reports

NSE's All Reports page lists multiple distinct EOD products, including:
- CM-UDiFF Common Bhavcopy Final (ZIP);
- Bhavcopy File (DAT);
- Full Bhavcopy and Security Deliverable data;
- Security-wise delivery positions;
- security price-band and surveillance indicator reports;
- MII security files;
- 52-week high/low reports;
- close-out prices and other daily reports.

NSE explicitly says the legacy CM Bhavcopy CSV and CM Common Bhavcopy CSV reports were discontinued effective 8 July 2024, referring to Circular 62424 dated 12 June 2024 and directing users to CM-UDiFF Common Bhavcopy Final (ZIP).

The same page states that:
- adjusted 52-week high/low columns are adjusted for corporate actions (bonus, consolidation, splits and rights);
- actual unadjusted 52-week high/low prices should be taken from bhavcopy.

The public catalogue therefore distinguishes an unadjusted market-price source from corporate-action-adjusted reference statistics. The two must not be collapsed into one field called close or price.

Sources:
- https://www.nseindia.com/all-reports
- https://www.nseindia.com/historical/historical-reports-capital-market-daily-monthly-archives
- NSE Circular 62424 (12 June 2024), referenced on the All Reports page.

### 1.2 2026 EOD dissemination change — .DAT versus .MS/.MD

NSE Circular NSE/MSD/74764, dated 18 June 2026, titled “Streamlining EOD information dissemination related to Bhavcopy”, states:
- website .DAT bhavcopy reports will also be made available through Extranet in a phased manner from July 2026; segment-specific effective dates are to be communicated separately;
- report paths are segment-specific for CM, FO, CD and CO;
- .MS and .MD bhavcopy reports distributed on Extranet and the related NNF API broadcasts will be discontinued effective 12 October 2026 because they duplicate the .DAT reports.

This is a separate 2026 format/distribution transition from the 2024 UDiFF common-bhavcopy transition. A data loader must know which source family, delivery channel and segment schedule apply on the requested trade date. It must not continue ingesting a legacy broadcast after its discontinuation date merely because an old connector still receives it.

Source:
- https://nsearchives.nseindia.com/content/circulars/MSD74764.pdf

### 1.3 Equity Derivatives daily reports

NSE's All Reports–Derivatives page lists:
- F&O-UDiFF Common Bhavcopy Final (ZIP);
- F&O Daily Settlement Prices (CSV);
- Daily Volatility;
- F&O Market Activity Report;
- contract MII files (NSE-exclusive and NSE/BSE-exclusive variants);
- daily contract delta file;
- combined delta-equivalent OI across exchanges;
- security-in-ban-period and position-limit files;
- other daily risk and settlement reports.

The page states that old F&O Bhavcopy CSV/common-bhavcopy CSV formats were discontinued effective 8 July 2024 in favour of F&O-UDiFF Common Bhavcopy Final (ZIP).

Daily price/volume, daily settlement price and contract-master files are distinct artifacts even when they refer to the same contract and trade date.

Source:
- https://www.nseindia.com/all-reports-derivatives

### 1.4 Historical archives by instrument family

NSE's Historical Reports catalogue separately lists:
- security-wise price/volume archives for equities;
- daily/monthly Capital Market reports;
- historical index data and Total Returns Index values;
- equity-derivatives contract-wise price/volume data;
- F&O daily/monthly reports and monthly settlement statistics;
- other segment-specific contract-wise archives.

The F&O contract-wise price/volume report exposes separate fields such as trade date, symbol, expiry, Open, High, Low, Close, LTP, Settle Price, number of contracts, turnover, open interest, change in OI and underlying value.

NSE also distinguishes option premium turnover and notional turnover. Do not treat turnover as interchangeable with traded premium or the notional value of option contracts.

Sources:
- https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives
- https://www.nseindia.com/all-reports-derivatives
- https://www.nseindia.com/report-detail/fo_eq_security

## 2. Actual, adjusted, settlement and total-return price concepts

### 2.1 Actual unadjusted traded prices

A raw EOD bhavcopy record represents the exchange's reported market data for its trade date and source format. For a cash-equity historical record, preserve at least:
- open/high/low/close as supplied;
- last price where separately supplied;
- volume/traded quantity;
- turnover/value and its documented unit;
- number of trades where supplied;
- deliverable quantity/delivery percentage where supplied;
- security ID, symbol, series and exchange;
- trade date, settlement context and source artifact.

Do not rewrite raw historical OHLC when a later bonus, split, rights issue or dividend occurs. Raw exchange observations must remain immutable so a researcher can reproduce the actual price observed on each date.

### 2.2 Corporate-action-adjusted price series

NSE's report-page disclaimer specifically labels the 52-week adjusted high/low columns as corporate-action-adjusted for bonus, consolidation, splits and rights; it points to bhavcopy for actual unadjusted values.

A separate adjusted historical series may be useful for statistical analysis, return comparison and chart continuity. It is a **derived dataset**, not the original bhavcopy. It must retain:
- raw source series;
- action event and effective/ex-date;
- adjustment factor and method;
- whether the action changes shares/units, price, or both;
- whether the adjustment is backward, forward or point-in-time;
- rounding and precision;
- treatment of dividends, rights proceeds, cash-in-lieu, mergers and demergers;
- adjustment-engine version.

Do not assume NSE's adjusted 52-week high/low report means a full adjusted historical OHLCV history is publicly available with identical methodology. The page makes a specific 52-week adjustment statement.

### 2.3 Corporate actions and event time

NSE's Corporate Actions filing page exposes announcement date, record date, ex-date, series, purpose, face value and, where relevant, book-closure dates. These dates are distinct:
- announcement date: when the market was informed;
- ex-date: date from which the security trades without the entitlement;
- record date: date used to determine eligible holders;
- book-closure dates, if any.

A backtest must not apply an action before it was announced if the simulation is intended to represent information available to a trader at that historical point. It must also distinguish the ex-date price/quantity transition from the later corporate-action payment/allotment/credit event.

NSE's derivatives-specific corporate-action methodology says derivative adjustments occur after market close on the last cum-date and may change strike, position and market lot/multiplier. That methodology applies to open derivatives contracts; it must not be copied as a generic cash-equity historical OHLC adjustment formula.

Sources:
- https://www.nseindia.com/companies-listing/corporate-filings-actions
- https://www.nseindia.com/static/investor-relations/corporate-actions
- https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments

### 2.4 Dividend cash flows and Total Returns Index

NSE explains:
- a Price Index reflects constituent price changes and does not account for dividend receipts;
- a Total Returns Index includes price movements and dividends;
- dividend payouts are indexed on their ex-dates and reinvested into the Total Returns Index;
- investors should benchmark total investment returns using TRI rather than a price index when dividend income matters.

Therefore:
- use Price Index when the intended benchmark is price-only;
- use TRI for a dividend-inclusive index return comparison;
- when backtesting individual shares, model dividend entitlements/cash credits as cash-flow events or use a documented adjusted series—but not both for the same dividend;
- do not subtract dividends from raw bhavcopy OHLC and then also credit dividend cash to the portfolio;
- do not assume a split/bonus-adjusted price series includes dividend reinvestment.

Source:
- https://www.nseindia.com/static/products-services/indices-total-returns-index

## 3. Derivatives price and settlement data must remain separate

NSE's F&O historical contract-wise archive exposes Open, High, Low, Close, LTP and Settle Price separately, together with volume/contracts, turnover, OI, change in OI and underlying value.

These fields answer different questions:
- OHLC: trading prices over the session;
- LTP: last reported trade price in the source report;
- Settle Price: clearing/settlement reference used for the applicable daily settlement and MTM process;
- OI: outstanding contracts at the reporting point;
- Change in OI: change against the prior reference;
- Underlying Value: reference value of the underlying in the report;
- option premium turnover versus notional turnover: different measures.

For futures P&L and margin reconciliation, use the effective clearing settlement-price source and preserve its date/version. Do not replace settlement price with close or LTP because it appears more intuitive. For trade-execution simulation, do not pretend that daily settlement price was an executable market quote.

For options, retain actual contract expiry/strike/option type and the source price/settlement fields. Never treat a generic continuous option series as a listed contract.

## 4. Point-in-time corporate-action and backtest treatment

### 4.1 Use a dated corporate-action event ledger

For each event, preserve:
- canonical security/underlying identity and historical aliases;
- exchange/series;
- corporate-action type and announced terms;
- announcement timestamp/date and source filing reference;
- ex-date, record date and book-closure dates;
- entitlement ratio, face-value change, issue price, dividend amount or other parameters;
- status (announced, revised, withdrawn, effective, completed);
- source artifact hash and capture time;
- affected predecessor/successor securities/contracts;
- cash and share entitlements/adjustment outcomes.

An event may be amended or withdrawn. Do not overwrite the original announcement; retain each official version and the effective event state for the simulated date.

### 4.2 Separate three backtest accounting choices

A strategy/backtest must declare which return convention it uses:

1. **Raw-price trading:** use actual raw market prices and separately model cash dividends, bonus/split/rights entitlements, mergers and other non-trade corporate-action events.
2. **Price-adjusted research series:** use a documented adjusted price series for continuous statistical indicators while preserving raw prices and not double-booking the corporate action in the portfolio ledger.
3. **Total-return benchmarking:** use a TRI or a fully documented total-return portfolio accounting convention, including dividend reinvestment/cash treatment.

The strategy's trading prices, portfolio holdings/units, cash ledger and benchmark return convention must be internally consistent. A single adjusted-close column cannot represent all these dimensions.

### 4.3 Avoid lookahead and survivorship bias

A point-in-time test must use:
- the security universe actually listed and eligible on the historical date;
- historical instrument/contract masters and effective aliases;
- date-effective symbol/series/venue mappings;
- action announcements as known on that date;
- the source data vintage available under the chosen test policy;
- index constituents and methodology as of the historical rebalance period;
- historical trading status, price bands, suspensions and delistings where available;
- the actual futures/options contract expiry and settlement process.

If a current security list is used to select historical instruments, delisted/merged/suspended names can disappear from the sample and produce survivorship bias. If a current index constituent list is backfilled over earlier periods, index membership lookahead is introduced.

NSE's historical catalogue separately lists equity security-wise price/volume archives, historical index data, F&O contract-wise price/volume and Total Returns Index values. A future backtest data lake should ingest the relevant point-in-time files and preserve coverage gaps rather than imply that one current dataset covers all historical universes.

### 4.4 Historical file vintage and correction policy

EOD report files should be immutable by source artifact and version:
- original bytes/hash;
- report family (UDiFF, .DAT, legacy CSV, .MS/.MD where historically applicable);
- segment and trade date;
- publication/dissemination time and actual capture time;
- schema/circular version;
- parser version and validation result;
- supersedes/superseded-by relation if a corrected/reissued file is encountered.

A later replacement/correction must not silently rewrite the original. Store each vintage and choose which one a backtest uses through a declared data-vintage policy:
- first-available/as-published;
- latest-corrected;
- research snapshot pinned by hash.

Backtest results should state the policy. This is essential for reproducing an earlier result after exchange files or parsers change.

## 5. Dataset ingestion and validation model

A historical dataset should be promoted only after:
1. validating source family and segment (CM, FO, index, etc.);
2. validating the effective file format (UDiFF ZIP, .DAT, legacy format for historical dates);
3. verifying archive/date/file identity and cryptographic hash;
4. parsing with the exact schema profile;
5. checking required columns, unique keys and value domains;
6. checking the calendar for expected sessions/holidays;
7. reconciling row counts and key totals against official report metadata where available;
8. checking duplicates, missing securities/contracts and unexpected expired/suspended/removed instruments;
9. reconciling close/LTP/settle/OI/traded quantity fields without replacing one with another;
10. joining corporate-action events via stable canonical identity and effective date;
11. producing raw and adjusted datasets separately;
12. recording dataset manifest and adjustment policy before allowing backtest consumption.

A missing bar, zero-trade instrument, suspended instrument, newly listed security, expired option or holiday must be represented explicitly. A missing record must not be silently forward-filled as a real traded price. Any synthetic/derived fill must be labelled, reason-coded and excluded from order-execution claims unless a strategy-specific policy explicitly accepts it.

## 6. Data product types for AlgoX

The data lake should expose separately typed datasets:

| Dataset | Meaning | Primary consumers |
|---|---|---|
| raw_cash_eod | Unadjusted official cash-market EOD data | Historical execution, corporate action ledger, reconciliation |
| raw_fo_eod | Contract-level F&O EOD with close/LTP/settlement/OI | Futures/options research, settlement and margin reconciliation |
| raw_intraday_candles | Provider/exchange intraday OHLCV by actual instrument/contract | Backtesting with declared bar assumptions |
| raw_index_price | Price-return index series | Price benchmark and index research |
| raw_index_tri | Total-return index series | Dividend-inclusive benchmark |
| corporate_action_events | Point-in-time action announcements and effective terms | Portfolio cash/units, adjusted research data |
| adjusted_price_research | Derived price series under a named corporate-action method | Technical indicators and statistical analysis |
| continuous_futures_research | Derived contract-roll series with declared roll policy | Futures research and long-horizon indicators |
| historical_universe | Point-in-time listed/eligible security and index membership | Bias-controlled strategy tests |
| data_vintage_manifest | File hashes, schema, corrections, parser and policy versions | Reproducibility and audit |

No dataset should overload a single field called adjusted_close to represent raw close, corporate-action-adjusted close, total-return close and derivatives settlement.

## 7. Additional requirements for PX-025

### R-179 — Raw, adjusted, settlement and total-return prices are separate types

The system MUST distinguish actual raw exchange prices, corporate-action-adjusted research prices, derivative settlement prices, Price Index values and Total Returns Index values. These values MUST NOT be overwritten or substituted for one another.

### R-180 — EOD artifact family and segment are effective-dated

Every EOD dataset MUST identify the source report family, segment, file format, distribution channel, effective date, circular/schema version and parser profile. CM, FO and index reports MUST NOT share an assumed universal file schema.

### R-181 — Raw EOD artifacts are immutable and hashed

The original bhavcopy/UDiFF/DAT/contract-wise archive bytes MUST be preserved with source, trade date, segment, file hash, publication/capture time, file size and parser version. Parsed tables MUST remain traceable to the original artifact.

### R-182 — Bhavcopy format migrations are date-versioned

The loader MUST apply the 8 July 2024 transition from discontinued CM/F&O legacy bhavcopy CSV formats to the corresponding UDiFF Common Bhavcopy Final ZIP. It MUST also apply NSE/MSD/74764's 12 October 2026 discontinuation of the older .MS/.MD Extranet files and NNF API broadcast formats where the segment-specific effective notice applies. Old source formats may remain valid for historical dates but MUST NOT be treated as current.

### R-183 — Data corrections create new vintages

If a corrected/reissued EOD report is encountered, the system MUST preserve the original and replacement as separate vintages, capture their hashes/timestamps and record the supersession relationship. A backtest MUST declare whether it uses first-published or latest-corrected data; a new vintage MUST NOT silently overwrite the source of a prior result.

### R-184 — Corporate-action event dates and status are explicit

Every corporate action MUST preserve announcement date/time, ex-date, record date, book-closure dates where applicable, event terms, status/version, source reference and affected canonical security identity. Record date MUST NOT be substituted for ex-date or announcement date.

### R-185 — Cash-equity raw prices and adjusted research prices remain separate

Actual bhavcopy OHLC/volume MUST remain raw and immutable. Any adjusted price series MUST be a separate derived dataset with event, factor, adjustment direction, rounding and builder version. NSE's derivative contract adjustment formula MUST NOT be applied as a generic cash-equity OHLC adjustment method.

### R-186 — Price Return and Total Return series are separate

The system MUST preserve Price Index and Total Returns Index as distinct benchmark datasets. If a backtest includes dividends through TRI or an adjusted portfolio return, it MUST NOT credit/reinvest the same dividend a second time.

### R-187 — Dividend entitlements are not double-counted

For individual-equity portfolio backtests, a dividend MUST be represented either through an explicit portfolio cash-flow/reinvestment ledger or through a fully documented total-return/adjusted-series convention. The selected approach MUST be declared and the same dividend MUST NOT be counted in both price adjustment and cash credit.

### R-188 — Derivative Close, LTP and Settle Price are distinct

Historical F&O ingestion MUST retain the separate close, LTP and daily settlement price fields where supplied, along with volume/contracts, turnover, OI/change-in-OI and underlying value. Daily MTM/settlement calculations MUST use the applicable clearing settlement price; execution simulation MUST NOT treat settlement price as an executable trade quote.

### R-189 — Historical derivatives retain the actual dated contract identity

Each historical option/future row MUST retain exchange/segment, instrument/contract identity, underlying, expiry, strike, option type, lot/quantity unit and effective contract master. A continuous root symbol or current contract token MUST NOT replace the actual expired contract identity.

### R-190 — Point-in-time universe includes removed and restricted securities

Historical universe construction MUST retain securities/contracts listed, eligible, suspended, delisted, merged or otherwise restricted on the historical date where official evidence is available. A current-only universe MUST NOT be presented as survivorship-bias-free history.

### R-191 — Index membership and methodology are point-in-time

Index backtests MUST use constituent membership, weighting and methodology effective for each historical rebalance period. Current constituents MUST NOT be applied retrospectively to earlier dates. Price-index and TRI membership/methodology versions MUST be retained.

### R-192 — Corporate-action knowledge time prevents lookahead

A backtest that simulates decisions at historical time T MUST only use corporate-action terms/announcements available by T. Later revised terms or post-event files MUST not be exposed as if they were known earlier. Announcement, capture, ex-date, record date and effective timestamps MUST remain distinct.

### R-193 — Historical coverage and missing sessions are explicit

Every security/contract/date range MUST record expected trading sessions, observed rows, missing bars, suspensions, zero-trade sessions, expired instruments and source retention gaps. Missing records MUST NOT be silently filled with a prior close and treated as a real traded observation.

### R-194 — OHLCV, settlement, turnover and delivery units retain source semantics

Volume, contracts, shares, traded value, premium turnover, notional turnover, deliverable quantity, OI and settlement values MUST retain their source definitions, units and segment. Option premium turnover MUST NOT be equated with notional turnover or cash-equity traded value.

### R-195 — Adjustment factors are sourced and reproducible

Every corporate-action adjustment factor MUST retain the official event terms, calculation basis, rounding/tick/lot rules, effective date and source/policy version. An adjustment MUST NOT be inferred solely from a price jump or from a current adjusted-high/low statistic.

### R-196 — Adjusted-series builder has an explicit policy version

Any derived adjusted-price or continuous futures research series MUST record algorithm version, adjustment direction, event inclusion policy, roll policy, dividend treatment, price/volume/OI adjustment, rounding, source vintages and output hash. A derived series MUST be reproducible independently of raw source data.

### R-197 — Backtest results pin a complete data manifest

Every backtest/research result MUST pin the dataset manifest, source hashes/vintages, historical universe, index membership, contract identities, corporate-action policy, total-return convention, market calendar, adjustment/roll algorithm and data-gap report. A result without these inputs MUST NOT be labelled fully reproducible.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-340. Use synthetic EOD files, corporate-action fixtures, historical universe and backtest manifests only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-341 | Historical CM report date is before the 8 July 2024 UDiFF transition | Select the historical source format/schema effective on that date; preserve its vintage |
| AT-342 | CM/F&O legacy bhavcopy CSV is requested for a current date after the documented transition | Reject as a current source and select the effective UDiFF Common Bhavcopy Final ZIP |
| AT-343 | Extranet .MS/.MD or NNF bhavcopy broadcast arrives after 12 October 2026 | Mark legacy dissemination as discontinued for the applicable segment; do not silently promote it as current |
| AT-344 | .DAT bhavcopy and UDiFF common bhavcopy exist for the same segment/date | Keep distinct source artifacts and schemas; reconcile under an explicit source policy rather than assuming byte/row equality |
| AT-345 | Raw bhavcopy close differs from corporate-action-adjusted 52-week high/low reference | Preserve raw close and adjusted statistic as separate types; no overwrite |
| AT-346 | Corporate-action record has announcement, ex-date and record date | Preserve each date independently; apply entitlement/price transition on the correct effective date |
| AT-347 | Bonus or stock split changes share count and economic price basis | Preserve raw OHLC; produce a separate factor-versioned adjusted series and correct unit/share transition |
| AT-348 | Cash dividend is included in a TRI benchmark and also credited in the portfolio ledger | Detect dividend double count; choose one consistent total-return treatment |
| AT-349 | Rights issue has entitlement ratio, issue price and ex-date | Use event-specific source terms; do not apply a generic split/bonus factor |
| AT-350 | Merger/demerger changes security identity and consideration/share entitlement | Preserve predecessor/successor IDs, event ratio, cash/stock consideration and non-trade event; no symbol-only roll |
| AT-351 | Corporate-action announcement is revised or withdrawn after initial publication | Retain both versions and use the status known at the backtest as-of time |
| AT-352 | Equity daily file contains raw OHLC but adjusted 52-week reference fields | Keep actual bhavcopy prices and adjusted reference columns separate |
| AT-353 | Index Price Return and TRI have different performance due to dividends | Benchmark against the selected return convention; never claim price-only index equals total-return index |
| AT-354 | Historical F&O row has Close, LTP and Settle Price with different values | Preserve each field; use settlement price for applicable daily MTM and close/LTP only for their defined market-price use |
| AT-355 | NIFTY future expires and next expiry becomes active | Retain separate dated contract IDs; construct continuous root series only with explicit roll and adjustment policy |
| AT-356 | Option contract is expired and absent from the current contract master | Resolve via the historical contract/alias snapshot; never substitute a current expiry token |
| AT-357 | Index backtest uses today's constituents for a historical year | Flag survivorship/lookahead bias; require point-in-time historical constituent set |
| AT-358 | Security was suspended or delisted and has no ordinary price row for a period | Preserve non-tradable/missing state; do not forward-fill into a tradable execution signal |
| AT-359 | A corrected bhavcopy vintage is received after an earlier backtest | Preserve old/new hashes; prior result remains pinned to its original vintage or is explicitly rerun |
| AT-360 | Corporate action was announced after the simulated strategy decision time | Prevent use of the later announcement/terms in that earlier decision; no lookahead |
| AT-361 | Split/bonus causes an apparent raw price discontinuity across ex-date | Keep raw prices unchanged and verify a separate adjusted-series continuity calculation without changing historical trade prints |
| AT-362 | A cash dividend is modelled as cash in portfolio accounting and TRI is used as an additional portfolio credit | Prevent duplicate dividend return; document benchmark vs portfolio accounting treatment |
| AT-363 | Derivative corporate-action adjustment changes strike and lot, while cash-equity OHLC remains raw | Apply derivative-specific contract adjustment to derivative identity only; do not rewrite cash OHLC by that formula |
| AT-364 | F&O archive uses option premium turnover and notional turnover in separate displays | Preserve correct unit/definition and prohibit turnover-field substitution |
| AT-365 | Volume is zero but close/settlement price is carried in a report | Distinguish zero-trade/settlement-reference data from an actual executed trade; do not fabricate volume |
| AT-366 | Contract settlement price is revised or published separately from the market close | Preserve source, time and value of each; settlement reconciliation uses the effective clearing source |
| AT-367 | EOD parser sees an old schema/format after the 2024 or 2026 transition | Reject current semantic parsing; retain historical parser only for dates when that format applied |
| AT-368 | Two rows appear for the same security/contract/trade date with distinct source identifiers or report roles | Apply exact report key/source role; do not pick one row silently or double-count it |
| AT-369 | Historical dataset combines provider candles from different corporate-action or contract-master vintages | Mark mixed-vintage dataset incomplete/UNKNOWN until reconciled under one explicit policy |
| AT-370 | Backtest output is created without hashes, universe, action policy or return convention | Refuse reproducibility PASS; emit a manifest-completeness exception |

PX-025 now contains **197 normative requirements (R-001–R-197) and 370 proposed acceptance scenarios (AT-001–AT-370)**. These are proposed tests only; no historical dataset was downloaded, adjusted, backtested or executed.

## 9. Open questions and evidence limitations

1. No daily 2026 CM/FO UDiFF ZIP, .DAT bhavcopy or contract-wise historical archive was downloaded or parsed.
2. NSE/MSD/74764 states segment-specific effective dates for the new Extranet .DAT dissemination will be communicated separately; each segment's actual operational date and the latest format catalogue must be checked before integration.
3. The exact schema, record-key and correction/reissue semantics for each UDiFF/DAT report version require the corresponding official readme/circular/sample file. This report does not claim a validated parser.
4. NSE's adjusted 52-week values do not establish a full adjusted historical OHLCV dataset. The exact adjustment methodology for any third-party adjusted series must be separately documented.
5. NSE's derivatives corporate-action methodology is not a complete cash-equity total-return price-adjustment methodology.
6. The complete historical point-in-time index constituent/universe history, delisting archive and all corporate-action event revisions were not downloaded in this pass.
7. Historical contract-wise F&O query interfaces can impose their own date-range/retention constraints; the archive coverage must be measured by contract/expiry, not assumed complete from a successful query.
8. The report does not resolve data redistribution/licensing/entitlement terms for NSE files or vendor historical data; any operational acquisition must observe the relevant terms.

## 10. Research decisions and non-authorization

- **ACCEPT:** retain raw unadjusted EOD reports as immutable source artifacts.
- **ACCEPT:** preserve UDiFF ZIP, .DAT, legacy .MS/.MD and historical source schemas by effective date and segment.
- **ACCEPT:** keep cash OHLC, adjusted research prices, derivative settlement prices, Price Index and TRI separate.
- **ACCEPT:** maintain a point-in-time corporate-action event ledger and action-aware cash/quantity accounting.
- **ACCEPT:** keep actual dated derivatives contracts separate from continuous analytical series.
- **ACCEPT:** pin each backtest to immutable source files, correction vintage, historical universe, adjustment/roll policy and data-gap report.
- **DEFER:** production data lake/parser, adjusted-price builder, historical constituent loader, daily correction resolver and backtest manifest enforcement until official sample files and schema/readme are obtained and validated.
- **NOT AUTHORIZED:** market/broker data requests, account or member portal access, production orders, code implementation, paid services, PR or merge to main.

**Final status:** PX-038 historical price integrity, corporate-action handling and backtest reproducibility research documented. PX-025 expanded to 197 requirements and 370 proposed acceptance scenarios. No data files or backtest were executed; exact current report schemas and segment-specific .DAT Extranet dates remain open.
