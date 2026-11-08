# PX-2026-039 — Point-in-time security universe and index membership reconstruction

**Research date:** 2026-11-08  
**Status:** NSE Indices methodology, historical-level archives, reconstitution calendar, press-release archive and index-data product/rights disclosure reviewed; no constituent dataset downloaded  
**AlgoX area:** historical universe / point-in-time index membership / constituent weights / index corporate actions / survivorship and lookahead controls  
**Scope:** NSE/NSE Indices equity indices, listed-equity history and index reconstitution events  
**Inputs:** PX-025 R-001–R-197; PX-028/029 corporate-action and settlement evidence; PX-034/035 reference-data ingestion; PX-036 canonical identity; PX-038 historical price and backtest integrity  
**Mode:** research and requirements specification only  
**Non-goals:** no index constituent-data subscription, no paid/member data access, no historical constituent file download, no broker/API connection, no backtest execution, no code implementation, PR or merge to main

## Executive finding

A historical index-level time series and a historical constituent universe are not the same dataset.

NSE makes historical index levels and Total Returns Index values available through its historical-report pages. Its FAQ says the NIFTY 50 historical series is available from 3 July 1990 and that the historical index set evolves through time. That statement explains the construction of the historical index series; it does not, by itself, provide the complete constituent list, weights, investible weight factors or point-in-time eligibility state for every historical date.

NSE Indices separately describes constituent data as a product containing company names, identifiers, market capitalisation, weights and prices, and directs customers to licensing opportunities. It also states that it retains proprietary rights over index compilation, composition and changes. This is an important acquisition boundary: a public historical index level does not prove that an exact constituent-and-weight history is available as a free public file.

The official reconstitution calendar and press-release archive do provide valuable event-level evidence:
- a current schedule by index family;
- index-specific announcements, inclusions, exclusions and changes;
- announcement dates and exact effective dates;
- reasons, selection thresholds and parent-index dependencies in many notices;
- ad-hoc events for corporate actions, suspension, delisting, schemes of arrangement and other exceptional conditions.

A point-in-time index universe can therefore be reconstructed from a verified starting constituent snapshot plus a complete chronological series of effective inclusion/exclusion/weight events and the correct methodology versions. A press-release event archive alone is not enough if the seed membership, historical weights, share/IWF updates or complete event set is missing.

**Decision:** AlgoX must model index membership, constituent weights, index methodology, security eligibility and the historical listed/tradable universe as separate effective-dated datasets. It must never use today's constituents retrospectively or infer exact constituent history from the index level alone. If a complete point-in-time baseline and event chain cannot be established, the backtest's constituent universe is UNKNOWN and cannot be labelled survivorship-bias-free.

## 1. Official historical-index and constituent-data surfaces

### 1.1 Public historical index-level data

NSE's Historical Reports catalogue lists separate products for:
- Historical Index Data;
- archives of daily/monthly reports for indices;
- Price/Earnings, Price/Book and dividend-yield values;
- Total Returns Index values;
- historical India VIX data.

NSE's Historical Index Data page provides an index selector, date range and CSV download for index OHLC, shares traded and turnover. Nifty Indices' Historical Data page separately offers historical index data, daily/monthly reports, valuation data and Total Returns Index values.

The NSE Indices FAQ says NIFTY 50 historical data is available from 3 July 1990 and that the historical index series evolves its index set through older periods. This is evidence that the published index level series represents a changing historical composition over time. It is not evidence that the same page exposes every underlying member, weight and investible weight factor for each date.

Sources:
- https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives
- https://www.nseindia.com/reports-indices-historical-index-data
- https://niftyindices.com/reports/historical-data
- https://www.nseindia.com/static/products-services/indices-faqs

### 1.2 Index constituent data is a separate product surface

NSE Indices' Index Data Subscription page says its products include constituent data with:
- company names;
- identifiers;
- market capitalisation;
- weights;
- prices.

It identifies uses such as quantitative research, portfolio construction, risk monitoring, performance attribution and benchmarking. It directs customers to NSE Indices for licensing opportunities. It also explicitly reserves proprietary rights over index names, trademarks, compilation, composition and changes.

This establishes that constituent-level data is an identifiable commercial/rights-controlled product. The public historical-level selector and the constituent-data product must not be treated as equivalent. The research pass did not subscribe to or download any constituent-data package and does not assert that complete historical member/weight files are available without entitlement.

Sources:
- https://www.nseindia.com/static/nse-indices/index-data-subscription
- https://www.nseindia.com/static/nse-indices/index-licensing

### 1.3 Index reconstitution calendar

Nifty Indices publishes an index reconstitution calendar with the effective frequency/date of changes for many individual indices. Examples from the current calendar include semi-annual reconstitution on the last working day of March and September for broad-market indices such as Nifty 50, Nifty Next 50, Nifty 100, Nifty 200 and Nifty 500. Other indices use quarterly, monthly, June/December or special schedules.

The calendar itself states that:
- NSE Indices may issue a separate notification if the schedule changes;
- additional reviews may be conducted for replacement following schemes of arrangement, suspension or delisting.

Therefore the calendar is a schedule baseline, not the event-of-record for every actual constituent change. Store the calendar version and the individual notice that supersedes or modifies the schedule.

Source:
- https://niftyindices.com/resources/index-rebalancing-schedule

### 1.4 Press-release archive provides dated constituent events

Nifty Indices maintains a searchable Press Release archive with dated event notices. The archive includes:
- replacements in indices effective on a future date;
- inclusion/exclusion from specific indices;
- corporate-action adjustments;
- revisions to index criteria;
- ad-hoc exclusions and reconstitution changes;
- postponements/deferments or revised effective dates.

A representative example is the 10 August 2026 “Replacements in indices” press release, which says changes become effective from 30 September 2026 (close of 29 September 2026). It explicitly records:
- Wipro Ltd. (WIPRO) excluded from Nifty 50;
- BSE Ltd. (BSE) included in Nifty 50;
- the selection rationale based on the six-month average free-float market capitalisation threshold relative to the smallest constituent;
- the F&O trading-availability eligibility requirement;
- linked impacts to Nifty 50 Equal Weight and other parent/child indices.

This gives a precise event date, announcement date, affected index and security-level inclusion/exclusion. It is useful for an append-only membership event ledger, but it does not alone provide all daily constituent weights and investible-weight-factor history.

Sources:
- https://www.niftyindices.com/press-release
- https://www.niftyindices.com/Press_Release/ind_prs10082026.pdf

## 2. Current methodology example: Nifty 50

The May 2026 NSE Indices Methodology Document for Equity Indices describes index-specific membership and review rules. The following is the Nifty 50 example only; it must not be copied as a universal rule for all Nifty indices.

### 2.1 Scheduled review and effective date

The May 2026 methodology states:
- the Nifty 50 review is semi-annual using six-month data ending January and July;
- changes take effect from the last trading day of March and September;
- four weeks' prior notice is given for scheduled replacements.

The public reconstitution calendar similarly lists Nifty 50 as semi-annual, last working day of March and September.

### 2.2 Eligibility and selection data

The May 2026 Nifty 50 methodology describes eligibility conditions including:
- constituent eligibility from the Nifty 100 universe;
- availability for trading in NSE's F&O segment;
- 100% trading frequency in the last six months;
- average impact cost of 0.50% or less for 90% of observations for a portfolio of ₹10 crore;
- average free-float market capitalisation at least 1.5 times that of the smallest existing constituent.

This illustrates that a backtest attempting to reconstruct index membership from raw daily prices alone is incomplete. The methodology depends on data and statuses such as parent-index composition, historical F&O availability, six-month trading frequency, impact cost and free-float market capitalisation.

### 2.3 Maximum changes and exceptions

The methodology says a maximum of five companies may be added in a calendar year in the scheduled semi-annual reconstitution of Nifty 50. It also lists exclusions from this cap for specified cases, including non-compliance with eligibility, F&O unavailability, impact cost/trading frequency failures, merger/demerger/delisting/capital restructuring, movement to BZ series, trading suspension and certain adverse regulatory findings.

Do not use the “five additions” limit as a cap on every possible exclusion or ad-hoc event. The exact scope and exclusions in the effective methodology version must be applied.

### 2.4 Ad-hoc changes and corporate events

The methodology permits additional index reconstitution for events such as:
- merger or demerger;
- delisting;
- capital restructuring;
- movement to BZ series;
- withdrawal of F&O trading permission where applicable;
- suspension of trading in the Capital Market segment;
- adverse regulatory findings/orders requiring removal.

It distinguishes scheduled periodic review from event-driven reconstitution. The index event ledger must capture which rule caused the event and when the change actually became effective.

Sources:
- May 2026 methodology document: https://archives.nseindia.com/content/indices/Method_NIFTY_Equity_Indices.pdf
- Index reconstitution calendar: https://niftyindices.com/resources/index-rebalancing-schedule
- 10 August 2026 Nifty 50 replacements notice: https://www.niftyindices.com/Press_Release/ind_prs10082026.pdf

## 3. Parent/child index dependencies and methodology versioning

The May 2026 methodology document explains that certain indices inherit their constituents from parent indices. For such child indices, the latest parent-index composition, including the most recent changes whether announced or yet to be announced under the relevant process, can be considered during reconstitution.

This creates two different time questions:
1. what membership is legally/effectively active in the index on date T;
2. what membership or proposed parent change was known to the index committee while reviewing the child index on its own decision date.

A backtest must not leak an announced-but-not-effective parent change into the child index's actual membership too early. Conversely, it must not use a stale parent membership if the index methodology and effective event record define a newer parent composition for the child review.

Methodology documents are versioned documents. The May 2026 rules cannot be applied to every historical reconstitution back to 1990 unless an archival version demonstrates that the relevant provision was then in force. Store the methodology version/effective date and the individual index product it governs.

A parent/child relation is also not a general assertion that every child index always has identical membership to its parent; it is an index-specific rule that must be read from the applicable methodology.

## 4. Historical membership reconstruction model

### 4.1 Required source chain

To reconstruct membership at historical point T, a future data pipeline needs:
1. a verified seed constituent snapshot effective immediately before the reconstruction window;
2. all scheduled reconstitution announcements and their effective dates;
3. all ad-hoc additions/exclusions;
4. all revised, postponed, withdrawn and superseding notices;
5. point-in-time methodology versions for each affected index;
6. corporate-action/scheme-of-arrangement and suspension/delisting event links;
7. constituent identifiers and predecessor/successor security mapping;
8. dated weight/IWF/shares-outstanding snapshots if exact portfolio weights are required;
9. parent-index membership and event chain for child indices;
10. source archive completeness/entitlement proof.

A sequence of current constituents plus a few sampled press releases is not a complete historical universe. If the starting snapshot or an event notice is missing, the membership chain becomes incomplete from that point.

### 4.2 Event ledger

A constituent-change event should preserve:
- index identifier and methodology version;
- source event ID/document hash;
- announcement publication timestamp;
- committee/press-release date;
- old and new constituent identifiers;
- action type (add, delete, replace, suspend, weight update, IWF/share update, parent propagation, defer, revoke);
- reason/rule clause;
- announced effective date and actual effective session boundary;
- source version, correction/supersession chain;
- parent/child affected indexes;
- old and new weights/IWF/shares where supplied;
- data completeness and validation result.

Never overwrite an earlier event because a later notice changes the effective date or reverses the prior decision. Keep both the original and revision, and derive the active state as-of the chosen knowledge time.

### 4.3 Membership state and weights are different

A security can remain an index constituent while its weight changes because of price drift, shares outstanding, free float/IWF or a quarterly weight alignment. Conversely, an addition/deletion changes membership itself.

The system must distinguish:
- membership start/end;
- effective weight;
- shares outstanding;
- free-float market capitalisation;
- investible weight factor (IWF);
- cap/weight adjustments;
- divisor adjustments and index-level continuity.

Do not treat a weight change as an add/delete event. Do not derive actual constituent weights solely by dividing today's company market capitalisation by a historical index total.

### 4.4 As-known versus as-effective views

Maintain two time axes:
- **effective time:** when the constituent/weight change applies to index calculation;
- **knowledge time:** when the notice/data was published and could have been known by a simulated strategy.

For a strategy acting before the effective close, the published future membership may be known as an announcement but is not yet active membership. The same announcement may be a valid signal for a pre-positioning strategy, but the active index portfolio still uses the pre-change membership until the source-defined effective boundary.

### 4.5 Missing history must remain explicit

If historical constituent data is not licensed/available for a period, or press-release events do not reconstruct a complete chain, do not:
- fill in today's members backwards;
- infer missing historical members from names in an index-level chart;
- assume the press-release archive contains every weight/IWF file;
- treat the historical index close as proof of the constituent list;
- silently use a current index file as a substitute.

Mark exact membership/weight reconstruction UNKNOWN for the affected period. Backtests can still run with an explicitly different universe definition (e.g. current universe or separately archived event-only approximation), but must label the methodology and bias risk; they cannot claim point-in-time index replication.

## 5. Backtest and research controls

For every index-based or constituent-screening strategy:
- pin index ID and methodology version;
- pin the historical constituent snapshot and the event chain used;
- pin announcement/knowledge timestamps and effective sessions;
- pin constituent weights/IWF/share snapshots if portfolio replication is claimed;
- use historical eligibility universe and historical parent index membership;
- include deleted, suspended, merged, delisted and excluded companies as they existed at the historical date;
- distinguish the official index calculation/continuity from a simple equal/market-cap weighted reconstruction;
- apply constituent weights and divisor/ corporate-action changes at their correct effective dates;
- label a test with incomplete member data as an approximation or UNKNOWN for exact index replication.

The Nifty 50 example demonstrates that even a fixed 50-stock index has specific selection filters, review data windows, notice periods, max-addition constraints and event-driven exceptions. Small/midcap, sectoral, thematic, strategy and fixed-income indexes may use different criteria and cadences; there is no safe universal semi-annual schedule.

## 6. Additional requirements for PX-025

### R-198 — Index levels and constituent membership are separate datasets

The system MUST model historical index OHLC/returns and point-in-time constituent membership as distinct datasets. A continuous index-level series MUST NOT be treated as proof of the constituent identifiers, weights or eligibility state for every historical date.

### R-199 — Index methodology is versioned and effective-dated

Every index reconstruction MUST pin the exact index methodology document/version, publication date, effective interval, index product and relevant rule clauses. The May 2026 methodology MUST NOT be applied retrospectively unless an archived effective version supports that historical rule.

### R-200 — Reconstitution calendar is a schedule, not the actual event record

The system MUST preserve the published index reconstitution calendar separately from each event-specific press release/notification and actual effective date. A changed schedule or ad-hoc notice MUST supersede the applicable planned date without deleting the original schedule evidence.

### R-201 — Index change events preserve announcement and effective timestamps

Every addition, deletion, replacement, weight change, deferment or cancellation MUST retain announcement/publication time, decision/notice date, effective session boundary and source document. A known future change MUST NOT be applied to active membership before its stated effective time.

### R-202 — Historical constituent event ledger is append-only

The system MUST preserve each source notice and its membership actions as immutable events, including revised, postponed, nullified and withdrawn changes. A later notice MUST NOT overwrite the earlier announcement; the as-known and as-effective state must be derivable independently.

### R-203 — Membership reconstruction requires a complete seed and event chain

The system MUST require a verified seed constituent snapshot plus complete additions/deletions and ad-hoc event chain for the reconstruction period. If any period/event is missing or unverified, exact membership MUST remain UNKNOWN from the point where completeness is lost.

### R-204 — Constituents, weights, IWF and shares are separate effective-dated facts

The system MUST preserve membership status, constituent weight, free-float/IWF, shares outstanding, market capitalisation, capping and divisor adjustments independently. A weight change MUST NOT be represented as an add/delete unless the source explicitly states membership changed.

### R-205 — Index-specific methodology cannot be generalized across products

Scheduled review cadence, eligibility, buffers, cap limits, data windows, parent-index dependencies and ad-hoc triggers MUST be evaluated from the correct index-specific methodology. The Nifty 50 semi-annual schedule MUST NOT be applied to all broad-market, sectoral, thematic, strategy or fixed-income indexes.

### R-206 — Eligibility metrics use historical point-in-time inputs

Where an index rule uses free-float market capitalisation, market capitalisation, trading frequency, F&O eligibility, impact cost or turnover, reconstruction MUST use the exact historical observation window, cut-off date, classification and source vintage applicable to that review. Current eligibility values MUST NOT be backfilled.

### R-207 — Parent/child index dependency is versioned and time-aware

Where an index draws its eligible universe or composition from a parent index, the system MUST pin the parent index methodology, membership version, announced changes and effective state used for the child review. An announced-but-not-effective parent change MUST NOT be silently treated as active child membership.

### R-208 — Ad-hoc index reconstitution is event-driven

The event pipeline MUST support additional reconstitution due to merger, demerger, scheme of arrangement, delisting, suspension, F&O trading-eligibility loss, BZ-series movement or other methodology-defined exceptional events. It MUST NOT wait for the next scheduled review when the source requires an ad-hoc change.

### R-209 — Suspension, delisting and removal end tradability without deleting history

A security removed/suspended/delisted from the index or exchange MUST retain its historical identity, membership interval, final available price and relevant event/consideration/settlement data. The system MUST mark it non-tradable for the applicable date without deleting it from historical universes.

### R-210 — Reconstitution limits and exceptions are applied literally

Any maximum additions/replacements or buffer rule MUST be bound to the correct index and review type. Explicit exceptions for forced exclusions and corporate events MUST be applied only where the applicable methodology says so; a cap on scheduled additions MUST NOT block a mandatory ad-hoc exclusion.

### R-211 — Actual effective boundary is session-specific

A constituent change announced as effective on a date or at a close boundary MUST be applied using the stated exchange session boundary and holiday calendar. The system MUST preserve pre-change membership through the last valid old-composition session and activate the new composition at the source-defined effective point.

### R-212 — Index divisor continuity is separate from portfolio return/accounting

Index divisor adjustments used to maintain index-level continuity MUST be stored separately from security portfolio cash flows, dividends, shares and actual historical execution prices. A divisor adjustment MUST NOT be booked as a client cash flow or used to rewrite raw security price history.

### R-213 — Press-release archives are event evidence, not a complete weight history by default

The system MUST treat press releases as source-backed membership-change events and reasons. It MUST NOT assume that event notices provide full daily constituent weights, IWF, shares outstanding or all intermediate weight changes. Exact weight history requires the corresponding complete authoritative data source.

### R-214 — Constituent data licensing and entitlement are recorded

Every historical index constituent/weight dataset MUST record its source product, acquisition/entitlement basis, redistribution/use constraints, coverage interval and file provenance. Public access to index levels MUST NOT be treated as permission or proof of access to proprietary constituent compilation/composition data.

### R-215 — Current methodology/calendar snapshots are not historical truth

Each backtest MUST use the methodology and schedule effective for the historical review date. A current reconstitution calendar or current eligibility criteria MUST NOT be retroactively applied to historical index membership without dated evidence.

### R-216 — Point-in-time universe completeness is an explicit backtest gate

A backtest claiming survivorship-bias-free index/member screening MUST demonstrate a complete historical universe and constituent/event chain for the entire tested period. If the data product/coverage does not prove completeness, the result MUST be labelled approximate/UNKNOWN and MUST NOT claim exact historical index replication.

## 7. Deterministic acceptance scenarios

These extend AT-001 through AT-370. Use synthetic index methodology versions, seed membership snapshots, press-release event records and fake constituent data files only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-371 | Historical index level series exists from 1990 but no constituent file is supplied | Permit index-level research only; exact constituent membership remains UNKNOWN |
| AT-372 | Current Nifty 50 constituents are supplied for a backtest beginning in 2005 | Reject point-in-time membership claim; do not backfill current members |
| AT-373 | Verified seed membership and complete event notices are supplied | Reconstruct membership intervals and preserve each source event/provenance |
| AT-374 | An index press release is announced on one date and effective at a later close | Keep announced membership separate from active membership until the correct effective boundary |
| AT-375 | Reconstitution calendar lists last working day of March/September but a separate notice changes the schedule | Preserve calendar and notice; use the operative revised date without deleting planned schedule |
| AT-376 | Nifty 50 scheduled review uses January/July six-month data and March/September implementation | Apply the Nifty 50-specific data window and effective date; do not generalize it to other indexes |
| AT-377 | Methodology revision becomes effective after the historical review being tested | Use the earlier effective methodology; do not apply the later threshold/cadence retrospectively |
| AT-378 | A child index review sees a parent-index change announced but not yet effective | Preserve the methodology's parent-review knowledge scope while keeping actual membership as-of effective time distinct |
| AT-379 | Parent index composition is missing for one historical review | Child-index membership becomes UNKNOWN; do not infer from current parent membership |
| AT-380 | Nifty 50 addition fails the current F&O availability or trading-frequency criterion | Do not include it based solely on market-cap ranking |
| AT-381 | Six-month impact-cost or free-float market-cap input is missing | Eligibility decision UNKNOWN; do not approximate the threshold from current values |
| AT-382 | Candidate stock meets the market-cap threshold but the index replacement cap has been reached | Apply the exact index/review addition cap and applicable exceptions; preserve deferred candidate status |
| AT-383 | Existing constituent is removed due to suspension/delisting during scheduled review window | Apply the methodology's ad-hoc/forced-exclusion path; do not wait for the next periodic review if rule requires earlier action |
| AT-384 | A merger or scheme of arrangement changes the constituent identity | Preserve predecessor/successor security identities, action date, consideration and index replacement event |
| AT-385 | An F&O-eligibility change triggers an ad-hoc index exclusion | Record loss of eligibility and exact effective date; do not leave a stale constituent as tradable |
| AT-386 | A company moves to BZ series and the index methodology treats it as an ad-hoc removal trigger | Trigger the applicable index event; preserve source notification and resulting constituent state |
| AT-387 | A reconstitution notice is postponed and later nullified | Preserve all versions; derive the membership state effective after the final valid notice |
| AT-388 | Two index notices overlap or conflict on the same constituent/effective date | Resolve using explicit issuer/supersession authority; otherwise membership status UNKNOWN |
| AT-389 | One constituent remains in index but its IWF/weight is revised | Record a weight/IWF change, not a membership add/delete |
| AT-390 | Index weight drifts daily because of market-price changes between rebalances | Recompute/observe weight as-of date if source permits; do not misclassify natural drift as a constituent event |
| AT-391 | Quarterly weight alignment and semiannual membership reconstitution occur at different boundaries | Preserve each event class and effective date independently |
| AT-392 | Press-release archive supplies additions/deletions but no full weight or IWF file | Event ledger may be complete for membership if event chain is sufficient; exact portfolio-weight replication remains UNKNOWN |
| AT-393 | Index divisor changes to maintain continuity after constituent/corporate action event | Preserve divisor event separately from portfolio cash/units and raw security price history |
| AT-394 | Index methodology PDF changes version but parser still uses old criteria | Invalidate affected point-in-time membership reconstruction and rebuild with correct effective methodology |
| AT-395 | NSE Indices constituent data is available only under separate entitlement and local test has no entitlement evidence | Block claim of full constituent-history coverage; public index-level data does not grant constituent-data rights |
| AT-396 | Nifty 50 methodology states max five additions per calendar year but an eligibility/forced-exclusion exception applies | Apply the exact stated exception; do not turn the addition limit into a universal no-change cap |
| AT-397 | Index reconstitution calendar changes after a methodology-specific notice | Reconcile current calendar to the effective official notice; preserve prior schedule vintage |
| AT-398 | A backtest universe includes only securities with surviving/current tickers | Flag survivorship bias; require historical identity and delisted/merged security evidence |
| AT-399 | Current index methodology contains a selection threshold not present in the historical version | Use historical version or return UNKNOWN; no retrospective rule substitution |
| AT-400 | Backtest claims exact historical index replication but lacks a seed membership snapshot, event chain or weight/IWF data | Fail reproducibility/completeness gate; label approximate/UNKNOWN rather than PASS |

PX-025 now contains **216 normative requirements (R-001–R-216) and 400 proposed acceptance scenarios (AT-001–AT-400)**. These are proposed tests only; no constituent files or historical index data products were downloaded and no index backtest was executed.

## 8. Evidence limitations and open questions

1. The public historical-index selector provides index-level history, but the exact date range and completeness of per-date constituent/weight history available without a separate product entitlement were not established.
2. NSE Indices' subscription page identifies constituent data as a separate product and reserves proprietary rights in index compilation/composition. Applicable license terms, pricing, permitted local research use, retention and redistribution rights must be checked before operational acquisition.
3. The public press-release archive provides event notices but may not provide a complete event chain for every index from inception. Archive completeness and machine-readable bulk access were not tested.
4. The May 2026 methodology document is a current version snapshot. Prior methodology versions for the entire backtest period must be archived and verified before historical membership reconstruction.
5. Current reconstitution calendar entries can be superseded by separate notifications. The calendar is not a replacement for event-specific notices.
6. The exact historical constituent weights, IWF, shares outstanding and divisor adjustments require their own dated authoritative files; press releases generally cannot be assumed to contain all such data.
7. Non-index historical listed universe reconstruction also requires archived exchange security masters, listing/delisting/suspension notices and source-valid historical security identities. This phase focuses on Nifty indices and does not close the complete NSE/BSE listed-universe archive.
8. Index-specific methodology varies materially; the Nifty 50 thresholds and semi-annual schedule in this report are examples, not universal defaults for all indices.

## 9. Research decisions and non-authorization

- **ACCEPT:** separate index-level historical values from constituent membership and constituent weights.
- **ACCEPT:** reconstruct membership only from a verified seed snapshot and complete, versioned, effective-dated event chain.
- **ACCEPT:** preserve announcement/knowledge time separately from effective membership time.
- **ACCEPT:** pin methodology, reconstitution calendar and individual event notices for each index/review.
- **ACCEPT:** model parent/child index dependencies, ad-hoc exclusions, corporate actions, suspension and delisting.
- **ACCEPT:** require explicit constituent-data entitlement and provenance for exact weight history; public index levels do not prove constituent-data access.
- **DEFER:** exact historical constituent/weight archive acquisition, index membership reconstruction engine and licensed data ingestion until source coverage, entitlement and historical methodology versions are verified.
- **NOT AUTHORIZED:** paid subscription, member portal access, broker/API access, live orders, code changes, PR or merge to main.

**Final status:** PX-039 point-in-time universe and index membership reconstruction audit documented. PX-025 expanded to 216 requirements and 400 proposed acceptance scenarios. No licensed constituent data, historical index file, code or backtest was executed.
