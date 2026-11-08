# PX-2026-032 — Position limits, MWPL ban period and intraday risk monitoring

**Research date:** 2026-11-08  
**Status:** source review completed; latest per-security Annexure I limit table not retrieved  
**AlgoX area:** equity-derivatives position limits / MWPL / entity exposure / ban-period controls / surveillance  
**Scope:** NSE Clearing, NSE, SEBI equity-derivatives circulars and current position-limit reporting  
**Inputs:** PX-025 requirements baseline, PX-029 expiry, PX-030 margin, PX-031 clearing reports  
**Mode:** research and requirements specification only  
**Non-goals:** no broker/member portal login, broker/clearing API call, sandbox/production access, order, code implementation, paid service, PR, or merge to `main`

## Executive finding

Position limits are a separate risk-control system from margin. A client can breach a position limit without a margin shortfall; a client may have sufficient margin and still be prohibited from increasing a position. Conversely, a margin shortfall or TM collateral-utilization warning does not prove that a position-limit breach occurred.

The audit identifies three separate monitoring/control domains:

1. **Single-stock MWPL / ban-period control.** Under the current FutEq framework, NSE Clearing tests aggregate market-wide delta-adjusted open interest across exchanges at EOD. A stock above 95% of MWPL enters ban from the next trading day. During ban, positions must reduce; normal trading resumes only after combined FutEq OI falls to 80% or below.
2. **Entity-level position limits.** Client, Trading Member, proprietary, FPI and Mutual Fund limits are separate scopes. The single-stock client limit applies across different trading members. Security-wise limits are versioned and disseminated for each effective period.
3. **Index-derivative intraday monitoring.** SEBI requires at least four randomly timed intraday snapshots for index-derivative position monitoring. The later 2025/122 framework and NSE's December 2025 implementation add an expiry-day index-option Additional Surveillance Deposit (ASD) process. That expiry-only ASD must not be generalized to non-expiry-day intraday alerts.

**Critical current-data issue:** NSE Clearing's public position-limit HTML page still displays category percentages last updated 19 November 2025. A later NCL circular, **NCL/CMPT/76459 dated 21 September 2026**, is identified as the applicable MWPL/entity-limit schedule from 1 October 2026, but its Annexure I could not be retrieved in this environment. Therefore this report does not claim that the 2025 stock-wise table is the current October–December 2026 schedule. Future implementation must use the exact effective-date circular/annexure and stock-level MWPL files. Missing or stale limits are UNKNOWN and block automated clearance.

## 1. Source set and chronology

### 1.1 SEBI Circular 2025/79 — FutEq and revised single-stock MWPL

SEBI Circular **SEBI/HO/MRD/TPD-1/P/CIR/2025/79**, dated 29 May 2025, changes the single-stock market-wide open-interest measurement to Future Equivalent (FutEq) and revises the MWPL methodology.

The revised stock MWPL is:
- the lower of **15% of free-float shares** and **65 times market-wide Average Daily Delivery Value (ADDV), expressed in quantity**;
- subject to a floor of **10% of free-float shares**;
- recomputed every three months using the rolling ADDV of the preceding three months;
- adjusted for relevant corporate actions using the applicable adjustment factor.

The EOD market-wide test uses combined FutEq open interest across exchanges against 95% of the applicable MWPL. The prior notional OI measure must not be substituted for the effective delta-based measure after the change takes effect.

Sources:
- https://www.sebi.gov.in/legal/circulars/may-2025/measures-for-enhancing-trading-convenience-and-strengthening-risk-monitoring-in-equity-derivatives_94293.html
- https://www.sebi.gov.in/sebi_data/attachdocs/may-2025/1748525395419.pdf (PDF attachment retrieval failed in this session)
- NSE Clearing FAQ updated 14 January 2026: https://www.nseclearing.in/sites/default/files/2026-01/Recent_changes_in_Equity_Derivative_segment_focusing_on_position_limits%2C_Limit_Monitoring%2C_and_Securities_in_Ban_Period.pdf

### 1.2 FutEq contract deltas and data files

NSE Clearing's January 2026 FAQ describes Futures Equivalent open interest as the portfolio-level net delta-adjusted exposure of futures and options on an underlying. Futures have delta 1; option exposure is scaled by the published contract delta factor. The FAQ points to:
- `Contract_Delta_DDMMYYYY.csv` for end-of-day delta factors;
- `Contract_Delta_DDMMYYYY_inn.csv` for intraday delta factors;
- member-specific `F_CM_DELOI_...` / `F_TM_DELOI_...` files;
- `nsccl.YYYYMMDD.i04.spn` for the scheduled 2 PM SPAN/delta snapshot used in the ban-period Day 2 comparison.

The FAQ shows fields including trade date, symbol, expiry, strike, option type and delta factor. The file's date, instrument, expiry and parameter snapshot are part of the calculation provenance.

**Research limitation:** the 8-page FAQ's official PDF text was searchable, but screenshot retrieval for pages 3–5 returned a cache-miss error. The field-level claims in this note are limited to the extracted official-page search text; no sample file was downloaded or parsed.

Source:
- https://www.nseclearing.in/sites/default/files/2026-01/Recent_changes_in_Equity_Derivative_segment_focusing_on_position_limits%2C_Limit_Monitoring%2C_and_Securities_in_Ban_Period.pdf

### 1.3 Market-wide ban threshold and resumption

Under the new FutEq method:
- NCL checks at EOD whether combined market-wide FutEq OI in a single stock exceeds **95% of MWPL**.
- If it does, the scrip is placed in ban **from the next trading day**.
- During ban, trading must reduce positions through offsetting activity; no new exposure may be added.
- Normal trading resumes only after combined FutEq OI across exchanges returns to **80% or below** MWPL.
- The ban-period security list continues to be published daily.

NSE Clearing's older public HTML position-limit page, updated 19 November 2025, still describes the 95%/80% thresholds and offset-only trading using generic aggregate OI language. The January 2026 FAQ gives the updated FutEq form and must be used for the post-migration calculation.

Sources:
- https://www.nseclearing.in/risk-management/equity-derivatives/position-limits
- https://www.nseclearing.in/sites/default/files/2026-01/Recent_changes_in_Equity_Derivative_segment_focusing_on_position_limits%2C_Limit_Monitoring%2C_and_Securities_in_Ban_Period.pdf

### 1.4 Ban-period entity baseline, passive delta movement and violation

The January 2026 FAQ describes the ban-period sequence:

1. On Day 1 (the day the security enters ban), the positions of each entity are stored as the base position.
2. On Day 2, the Day 1 positions are revalued to FutEq using the delta factors in the Clearing Corporation's SPAN file at the specified 2 PM snapshot; Day 2 EOD positions are also converted using that day's 2 PM delta.
3. If the current EOD FutEq position is less than or equal to the base-position FutEq without a change in sign, the movement is not treated as a violation.
4. Other cases are identified as violations and are subject to the applicable penalty.
5. Passive changes in FutEq resulting from delta movement are not automatically treated as position increases; the source comparison uses the prescribed Day 1 baseline and current-day delta.

The rule is not equivalent to simply comparing raw contract counts or option notional on two days. A future reconciler must preserve both the raw positions and the delta-adjusted comparisons used by the rule.

The FAQ also notes that expiry-day disappearance/roll-off of near-month positions may create a passive position-limit change that is not penalized under its stated treatment. This is an expiry-specific source rule; do not generalize it to an actively increased position.

Source:
- https://www.nseclearing.in/sites/default/files/2026-01/Recent_changes_in_Equity_Derivative_segment_focusing_on_position_limits%2C_Limit_Monitoring%2C_and_Securities_in_Ban_Period.pdf

### 1.5 Entity-level limits for single-stock derivatives

NCL Circular **NCL/CMPT/70271**, dated 18 September 2025, effective 1 October 2025, specified the entity categories and limits:
- Trading Member combined proprietary plus client positions: 30% of applicable MWPL;
- TM proprietary positions: 20%;
- FPI Category I and Mutual Funds: 30%;
- FPI Category II other than individuals/family offices/corporates: 20%;
- FPI Category II individuals/family offices/corporates: 10%;
- clients/NRI/schemes of Mutual Funds trading through different members: 10%.

The circular also says end-of-day positions are considered on a gross basis for those limits. It prescribes an entity-level penalty of 1% of the excess value or ₹1,00,000, whichever is lower, subject to a ₹5,000 minimum.

**Current-schedule qualification:** NCL later issued:
- NCL/CMPT/74811 dated 22 June 2026, effective 1 July 2026; and
- NCL/CMPT/76459 dated 21 September 2026, effective 1 October 2026.

The latter reference was located through a secondary circular index that reproduced the circular metadata/text. The expected official NSE archive URL was then attempted but was not accessible in this research environment. Accordingly, the circular number/date/effective date are a source lead rather than independently verified official-PDF evidence in this pass; the Annexure I security-level numbers and any effective-date changes in the 2026 table have not been inspected. Treat the 1 October 2026 schedule and all per-security values as UNKNOWN until the official circular/annexure or matching UDiFF/limit file is retrieved. The 2025 percentage table is retained as historical source context, not asserted as the current 1 October 2026 schedule.

Sources:
- NCL/CMPT/70271 (18 September 2025): https://www.archive.nseclearing.in/content/circulars/CMPT70271.pdf
- NCL/CMPT/74811 (22 June 2026): official circular reference and annexure retrieval not completed
- NCL/CMPT/76459 (21 September 2026): https://nsearchives.nseindia.com/content/circulars/CMPT76459.pdf (official archive URL not accessible in this session)
- NSE Clearing position limits page: https://www.nseclearing.in/risk-management/equity-derivatives/position-limits

### 1.6 Intraday index-derivative monitoring

SEBI Circular **SEBI/HO/MRD/TPD-1/P/CIR/2025/41**, dated 28 March 2025, requires:
- intraday monitoring of equity-index derivative position limits from 1 April 2025;
- at least four randomly selected position snapshots in predefined time windows;
- the exchanges to prepare and communicate an SOP for monitoring existing notional position limits.

The 2025/41 circular stated that intraday breaches of the then-existing position limits would not attract penalty and would not be considered violations until further directions. This statement must be read with the later 2025/122 framework; it is not a blanket exemption from expiry-day index-option ASD or from EOD position-limit rules.

SEBI Circular **SEBI/HO/MRD/TPD/CIR/P/2025/122**, dated 1 September 2025, establishes a further intraday framework for equity index derivatives. NSE's implementing circular **NSE/SURV/71673**, dated 5 December 2025, confirms that:
- the transitional glide path ended 5 December 2025 and ceased from 8 December 2025;
- entities taking large delta-based index-option positions are expected to maintain their own delta computation/monitoring;
- intraday position-limit breaches on the **day of expiry of options contracts** attract Additional Surveillance Deposit (ASD) from 8 December 2025;
- ASD remains blocked for one month;
- the intraday ASD amount is 1.5 times the computed ASD;
- the source example uses the higher of applicable intraday-expiry and EOD excess position values and recognizes cash/cash equivalents allocated by the Clearing Member in RPT reporting;
- the circular states ASD is not applicable for non-expiry-day intraday breaches.

The SEBI 2025/122 PDF itself was not retrievable by the web connector, but NSE/SURV/71673 explicitly references its clause 4.7 and sets out the implementation date and ASD treatment. The exact numerical entity limits and all other clause-level details from the 2025/122 PDF remain a source-closure item.

Sources:
- SEBI Circular 2025/41: https://www.sebi.gov.in/legal/circulars/mar-2025/intraday-monitoring-of-position-limits-for-index-derivatives_93123.html
- SEBI Circular 2025/122: https://www.sebi.gov.in/legal/circulars/sep-2025/framework-for-intraday-position-limits-monitoring-for-equity-index-derivatives_96376.html
- NSE Circular NSE/SURV/71673 (5 December 2025): https://nsearchives.nseindia.com/content/circulars/SURV71673.pdf

### 1.7 Current ban-period penalty and separate position-limit penalty

NCL Circular **NCL/CMPT/71501**, dated 27 November 2025, discontinues the interim ban-period penalty procedure from 6 December 2025 and says penalties for increases during ban follow NCL/CMPT/70085 (8 September 2025).

NSE Clearing's penalties page, updated 16 April 2026, separately states:
- **single-stock entity position-limit violation:** 1% of the excess quantity value at the underlying close or ₹1,00,000, whichever is lower, subject to a ₹5,000 minimum;
- **MWPL ban-period increase:** 1% of the value of the increased position at the underlying close, subject to ₹5,000 minimum and ₹1,00,000 maximum.

These are distinct penalty calculations. They must not be collapsed into one generic “position-limit penalty.” The page also describes different penalties for margin/disablement and client short-collection; those belong to PX-030/PX-031.

Sources:
- NCL/CMPT/71501: https://nsearchives.nseindia.com/content/circulars/CMPT71501.pdf
- NSE Clearing penalties (updated 16 April 2026): https://www.nseclearing.in/clearing-settlement/equity-derivatives/penalties

## 2. Three independent monitoring domains

| Control domain | Measurement scope | Trigger/monitoring | Primary control response |
|---|---|---|---|
| Single-stock MWPL ban | Aggregate market-wide FutEq OI across exchanges for one stock | EOD >95% MWPL; ban starts next trading day; resume at ≤80% | Reduce positions through offsets during ban; ban-period increase penalty |
| Entity-level stock position limit | Client/NRI/scheme, TM combined, TM proprietary, FPI category, MF | Effective security-wise MWPL and category table; cross-member aggregation where specified | Prevent/flag entity-level breach; applicable entity-position penalty |
| Index-derivative intraday limit | Entity positions in index futures/options on FutEq/delta and applicable intraday rules | Minimum four random snapshots; expiry-day index-option ASD rules from 8 Dec 2025 | Intraday surveillance; expiry-day ASD; separate EOD limit monitoring |

Do not substitute:
- margin utilisation for position limit;
- raw open-contract count for FutEq;
- NSE-only OI for cross-exchange market-wide OI;
- one client's broker account for the entity's cross-member total;
- the 60% warning threshold for the 95% ban trigger;
- an index-option intraday ASD for a single-stock MWPL penalty.

## 3. Source limitations and current-value handling

1. NSE Clearing's position-limit HTML page is updated 19 November 2025 and displays category values from the earlier schedule. It remains useful for the ban thresholds and category context but is not the controlling current security-wise schedule for October–December 2026.
2. NCL/CMPT/76459 (effective 1 October 2026) was identified through its circular reference and official archive URL, but Annexure I could not be retrieved. Per-stock limits are therefore UNKNOWN in this research environment.
3. The 2026 FAQ establishes the FutEq and ban-period method; the PDF screenshots for pages 3–5 returned cache-miss errors, and no example ZIP/data file was inspected.
4. The 2025/122 SEBI PDF retrieval failed; NSE's official SURV71673 implementation circular provides the December 2025 transition and ASD provisions. Exact clause-level entity limit thresholds from 2025/122 are not re-stated without the full source.
5. May 2026 SEBI materials that include consolidation/draft language are public consultation/draft content, not an operative replacement circular. They are not used as current binding rules in this record.
6. Position limits and MWPL are date/effective-period data, not hard-coded constants. A live trading control must refuse to clear a position where the effective schedule, category, delta source or current ban status is missing.

## 4. Additional requirements for PX-025

### R-089 — Position-limit sources are effective-dated and versioned

Every position-limit decision MUST retain the exchange/segment, underlying/security, entity category, member/client scope, applicable MWPL, individual/entity cap, source circular/annexure, effective period, retrieved file/hash and parameter version. A historical or stale HTML table MUST NOT be treated as the current limit schedule.

### R-090 — Client limits aggregate across relevant trading members

Where the applicable rule defines a client limit across different members, the calculation MUST aggregate all relevant positions for the same client/entity identity across those members and the applicable exchange/clearing scope. A broker-local account subtotal MUST NOT be represented as the full entity exposure. If client identity mapping or cross-member data is incomplete, the total is UNKNOWN.

### R-091 — FutEq uses contract-specific delta evidence

The system MUST preserve raw contracts/open positions and compute/ingest FutEq using the applicable contract delta factor for symbol, expiry, strike, option type and timestamp. The delta source file/version and parameter snapshot MUST be retained. Raw OI, notional OI and FutEq OI MUST remain distinct measures.

### R-092 — MWPL calculation is quarterly, source-based and corporate-action adjusted

For the rule introduced by SEBI 2025/79, the MWPL calculation MUST use the lower of 15% free float and 65 times market-wide ADDV in quantity, subject to the 10% free-float floor, and the preceding three-month ADDV window. It MUST preserve the calculation inputs, reference period and quarterly effective date. Applicable corporate-action factors MUST be applied only from the effective source; no stale monthly limit may be carried forward.

### R-093 — MWPL ban activation and resumption are cross-exchange EOD conditions

Under the current FutEq framework, the ban MUST be activated only after the EOD market-wide FutEq OI for the stock exceeds 95% of the applicable MWPL, with the ban effective from the next trading day. Normal trading MUST remain restricted until combined FutEq OI across exchanges is 80% or below MWPL. An intraday alert MUST NOT be converted into next-day ban status without the prescribed EOD test.

### R-094 — Ban-period Day 1 baseline is immutable

The system MUST preserve the entity's Day 1 baseline positions when a security enters ban and the exact delta snapshot used to create the base FutEq value. Subsequent daily comparisons MUST use the source-prescribed position and delta times (including the specified 2 PM snapshot) and must be reproducible from raw position and delta files.

### R-095 — Passive delta movement and expiry roll-off are not fabricated as active increases

The ban reconciler MUST distinguish actual position changes from FutEq changes caused only by a delta-factor movement. It MUST apply the official Day 1/current-day comparison and sign rule. An expiry-related passive change that the applicable exchange rule excludes MUST NOT be penalized as an active increase. The system MUST retain enough evidence to show why a change was active or passive.

### R-096 — Entity-level stock limits use the latest applicable category and security schedule

The implementation MUST distinguish client/NRI/scheme, TM combined, TM proprietary, FPI Category I/II and Mutual Fund scopes. It MUST load the latest applicable per-security MWPL and entity cap for the effective period (including the identified 1 October 2026 schedule once available). It MUST NOT hard-code category percentages from the September 2025 schedule as current October 2026 values without verifying the operative Annexure I.

### R-097 — Intraday index monitoring retains every required snapshot

For equity-index derivatives, the system MUST retain at least four randomly timed snapshots in the prescribed windows, with client/entity identity, raw positions, applicable limit, underlying price, delta/FutEq factor, snapshot time and source/report identity. It MUST NOT assume fixed snapshot times or use a daily bar to reconstruct an actual snapshot.

### R-098 — Index-option expiry ASD is limited to the effective expiry-day framework

For the applicable index-option expiry-day intraday breach framework effective from 8 December 2025, the system MUST preserve the breach snapshot, cure-period snapshot, EOD comparison, cash/cash-equivalent allocation and ASD calculation. It MUST apply the source-defined 1.5x intraday ASD and one-month block only where applicable. It MUST NOT apply this expiry-day ASD to non-expiry-day intraday alerts.

### R-099 — Existing-limit intraday monitoring and expiry-day ASD are separate rule states

The system MUST preserve the 2025/41 rule that existing notional-limit intraday breaches were not treated as violations/penalties until further directions, alongside the later 2025/122 and NSE implementation of expiry-day index-option ASD. It MUST apply the effective rule by product, entity, date and expiry status; it MUST NOT generalize either statement to every index intraday or stock MWPL case.

### R-100 — Ban files, delta files and violation files are completeness-gated inputs

A position-limit decision MUST retain and validate the daily ban-period security list, combined cross-exchange MWPL/OI data, contract delta file, member/entity FutEq files and any applicable violation report. Missing, stale, partial, corrupt or mismatched-date inputs MUST result in UNKNOWN, not a pass or zero exposure.

### R-101 — Position limits, margin and member PRISM controls remain distinct

The system MUST model position-limit utilization, MWPL ban state, margin requirement/shortfall, client collateral availability and member-level effective-collateral/PRISM utilization as separate risk dimensions. One dimension MUST NOT be inferred from another. Any automated block or warning MUST carry the scope and source rule that authorizes that control.

## 5. Additional deterministic acceptance scenarios

These extend AT-001 through AT-150. Use deterministic synthetic position, contract-master, delta, MWPL, ban-list and exchange-surveillance fixtures only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-151 | Position-limit parameter set is missing, stale or effective date does not cover the trade date | UNKNOWN; no position-limit clearance or invented default |
| AT-152 | Same client's stock-derivative position is split across two brokers/trading members | Aggregate under the applicable client identity/rule; do not assess each broker account independently |
| AT-153 | Client identity mapping across trading members is incomplete | Cross-member total remains UNKNOWN; do not assume broker-local exposure is the client total |
| AT-154 | Option contract delta file is missing for one expiry/strike | FutEq calculation UNKNOWN for affected positions; do not substitute delta 1 or stale delta |
| AT-155 | Futures and options on the same stock have different delta factors | Compute FutEq with the correct factor per contract and retain raw OI separately |
| AT-156 | MWPL inputs provide 15% free-float quantity and 65x ADDV quantity | Select the lower, enforce the 10% free-float floor and record the calculation trace |
| AT-157 | Quarter boundary changes the ADDV reference window and MWPL | Use the rolling preceding three-month period and the new effective date; do not apply monthly/stale limits |
| AT-158 | Corporate action changes the applicable MWPL from an ex-date | Apply only the published adjustment factor from that date and retain pre/post limits |
| AT-159 | Market-wide FutEq OI closes at 94.99% of MWPL | Do not activate ban; retain the EOD ratio and source inputs |
| AT-160 | Market-wide FutEq OI closes above 95% of MWPL | Mark stock for ban beginning the next trading day, not immediately during the current session |
| AT-161 | NSE-only OI exceeds a warning threshold but cross-exchange FutEq has not reached ban trigger | Preserve the warning and market-wide test separately; do not enter ban solely from the alert |
| AT-162 | Market-wide FutEq OI falls to 80% or below across exchanges | Resume normal trading only after the applicable source-confirmed EOD condition is met |
| AT-163 | Market-wide OI remains between 80% and 95% after ban | Keep ban active; do not resume early |
| AT-164 | Day 1 ban baseline is captured and Day 2 uses new delta factors | Recompute current FutEq using the prescribed 2 PM delta and EOD positions; retain raw positions and comparison values |
| AT-165 | Day 2 contract delta changes while raw entity positions are unchanged | Classify passive FutEq change according to the official baseline comparison; no false active-increase violation |
| AT-166 | Position reduction crosses through zero and changes FutEq sign | Apply the source sign rule; do not call it a valid reduction merely because absolute magnitude is lower |
| AT-167 | Entity increases raw contracts during ban but delta-weighted EOD FutEq remains at/below base without sign change | Apply the effective FutEq rule and source evidence; do not use raw contract count alone to decide |
| AT-168 | Near-month expiry causes passive open-interest/FutEq movement during ban | Apply the documented expiry-passive treatment; do not levy an active-increase penalty without the triggering evidence |
| AT-169 | Ban-period trade creates new exposure rather than offsetting an existing position | Flag violation and compute the applicable ban-increase penalty basis |
| AT-170 | Ban begins next day after EOD 95% trigger | Enforce offset-only trading for the next trade date; do not restrict the trigger day retrospectively |
| AT-171 | Security returns to normal only after combined all-exchange FutEq reaches 80% | Keep restriction until the cross-exchange condition is met; one exchange's local OI is insufficient |
| AT-172 | Current entity-limit annexure is the 1 October 2026 NCL/CMPT/76459 schedule | Require the actual applicable annexure/security row; if unavailable, return UNKNOWN instead of using 2025 category table |
| AT-173 | TM combined proprietary+client, TM proprietary-only and client limits are assessed together | Preserve each limit scope separately; do not substitute TM combined cap for client cap |
| AT-174 | FPI Category I, FPI Category II subcategories, MF scheme and NRI client have different applicable limits | Apply the correctly classified entity rule and date-specific schedule; ambiguous category remains UNKNOWN |
| AT-175 | Index-derivative intraday monitoring supplies four random snapshots | Preserve each snapshot and calculate applicable peak/breach state; do not assume snapshots occur at fixed times |
| AT-176 | Intraday index position snapshot has an underlying price different from EOD close | Use the price/time input prescribed for that snapshot; do not value the intraday exposure with stale close |
| AT-177 | Intraday breach occurs on a non-expiry day under the 2025/41 / 2025/122 framework | Preserve the intraday observation and applicable surveillance rule; do not apply the expiry-day ASD automatically |
| AT-178 | Intraday breach occurs on an index-option expiry day after 8 December 2025 | Apply the current expiry-day ASD process, including cure-period/EOD comparison, 1.5x intraday ASD and one-month block where the source conditions are met |
| AT-179 | Missing delta/ban file or incomplete exchange snapshot set prevents a reliable breach calculation | Position state UNKNOWN; do not clear order or manufacture a pass |
| AT-180 | Position-limit alert exists while SPAN margin is sufficient; or margin shortfall exists while position limit is within bounds | Preserve the two separate risk dimensions and trigger only the rule-specific control |
 
PX-025 now contains **101 normative requirements (R-001–R-101) and 180 proposed acceptance scenarios (AT-001–AT-180)**. These are proposed deterministic scenarios, not executed tests.

## 6. Research decisions and non-authorization

- **ACCEPT:** separate single-stock MWPL ban, entity-level stock position limits and index-derivative intraday monitoring into different control domains.
- **ACCEPT:** calculate post-May-2025 single-stock MWPL/OI using FutEq and date-versioned delta files, not raw option notional alone.
- **ACCEPT:** use 95% EOD to activate next-day ban and 80% combined cross-exchange FutEq for resumption.
- **ACCEPT:** preserve Day 1 ban baseline, current-day 2 PM delta and EOD position comparison; passive delta and expiry movements must not be fabricated as active increases.
- **ACCEPT:** preserve at least four random index-derivative intraday snapshots and expiry-day index-option ASD separately from non-expiry-day monitoring.
- **ACCEPT:** position-limit penalties, ban-period penalties, client margin shortfall and TM-level PRISM utilization are distinct.
- **DEFER:** exact October–December 2026 security-wise MWPL and entity-limit values until NCL/CMPT/76459 Annexure I and the applicable quarterly file can be inspected.
- **DEFER:** exact 2025/122 numerical thresholds/parameters not exposed by retrieved official sources; use the effective exchange implementation files and circular when designing the index-option intraday engine.
- **NOT AUTHORIZED:** broker/member portal login, broker/clearing API call, sandbox/production operation, real orders, code changes, paid data/services, credential/IP changes, PR or merge to `main`.

**Final status:** PX-032 position limits, MWPL ban period and intraday index-risk monitoring research documented. PX-025 expanded to 101 requirements and 180 proposed acceptance scenarios. Latest 1 October 2026 security-wise schedule and exact 2025/122 PDF-level parameters remain uninspected; no automated control or broker interaction was implemented.
