# PX-2026-031 — Clearing margin reports, short allocation and risk enforcement

**Research date:** 2026-11-08  
**Status:** official-reporting and risk-control page audit completed; UDiFF field-level workbook not inspected  
**AlgoX area:** margin evidence ingestion / client collateral allocation / shortfall reporting / member risk enforcement  
**Scope:** NSE Clearing equity-derivatives UDiFF catalogue, client margin reporting, PRISM/violations and payment-of-margin pages  
**Inputs:** PX-025 requirements baseline, PX-030 margin collection/risk-controls audit  
**Mode:** research and requirements refinement only  
**Non-goals:** no member portal login, clearing-file download requiring membership, broker/clearing API call, sandbox/production interaction, order, code implementation, paid service, PR or merge to `main`

## Executive finding

PX-030 established the margin components and client-collection rules. PX-031 examines how those obligations are represented in clearing reports, allocated as collateral, tested for short allocation and enforced at Trading Member/Clearing Member level.

The official NSE Clearing sources add several concrete controls:

1. **UDiFF is the standardized report-format family.** NSE Clearing states that the format standardizes Trade, STT, CTT, Stamp Duty, Position, Obligation, Margin, Penalty and Settlement Master reports across relevant segments.
2. **Client margin reporting is a separate clearing control.** The client-reporting page specifies minimum four randomly selected intraday snapshots using fixed BOD parameters, with SPAN, ELM and net option premium payable at snapshot/EOD. It separately specifies EOD and peak margin collection reporting.
3. **Collateral allocation is attributable to client/TM/CP and segment.** Clearing Members must ensure sufficient collateral is allocated to the relevant TM Prop/CP/client. Where the allocation is insufficient, Clearing Member/Trading Member proprietary collateral may be blocked and deemed allocated under the published rules.
4. **Short allocation is not identical to a generic margin shortfall.** The published formula compares minimum upfront client collection requirement with client collateral value in that segment, and excludes margins that may be collected by T+1/T+2 for that particular short-allocation calculation.
5. **Penalty comparison uses multiple views.** The page compares EOD shortfall, peak margin shortfall across snapshots and the highest intraday/EOD short allocation after allowed cross-segment excess/valid reason codes; the higher shortfall is used for penalty.
6. **Non-reporting is itself a severe compliance condition.** Missing client-margin reporting is treated similarly to 100% short reporting.
7. **PRISM risk enforcement is member-level.** NSE Clearing's violations page describes real-time monitoring, 70%/80%/90% effective-collateral usage warnings and withdrawal of a Trading Member's trading facility at 100% utilization. These are TM-level clearing controls, not universal client/broker RMS thresholds.

**Data-access limitation:** NSE Clearing's current UDiFF page links an Annexure B XLSX file-format catalogue and sample ZIP files. The web connector could not parse the XLSX content type; related ZIP retrieval attempts returned unsupported/forbidden/cache-miss responses. This audit therefore verifies the official catalogue, named report families and circular revision history, but it does **not** claim that the detailed workbook fields, code lists or actual sample rows were parsed.

## 1. UDiFF catalogue and version provenance

NSE Clearing's UDiFF page explains that standardized/harmonized file formats are intended for clearing and settlement information exchanged among market infrastructure institutions. It states that:
- Annexure A contains the UDiFF standards/guidance;
- Annexure B is the report/file-format workbook;
- Annexure C contains sample reports;
- standardized report families include Trade, STT, CTT, Stamp Duty, Position, Obligation, Margin, Penalty and Settlement Master;
- the report formats span Capital Market, Equity Derivatives, Commodity Derivatives, Electronic Gold Receipt and Currency Derivatives.

The same page lists updates relevant to schema/version control:
- **NCL/CMPT/59707 (11 Dec 2023):** original standardization circular with Annexures A/B/C;
- **NCL/CMPT/60764 (19 Feb 2024):** mapping of older/non-standard/standard phase-one/UDiFF files, revised Annexure B and change log;
- **NCL/CMPT/62079 (17 May 2024):** CC-to-member UDiFF update and trade-file remark changes;
- **NCL/CMPT/65315 (29 Nov 2024):** upfront collection of option premium; UDiFF page explicitly marks an update to the margin file;
- **NCL/CMPT/67345 (28 Mar 2025):** standardization of reports relating to T+0 settlement;
- UDiFF page last updated **14 May 2026**.

This is enough to establish that a margin-report parser must be versioned and date-effective. It is **not** enough to infer the exact fields or backward-compatible behavior of every file until the Annexure B workbook and applicable circular attachments are inspected.

Sources:
- https://www.nseclearing.in/udiff
- https://www.nseclearing.in/sites/default/files/2026-05/Annexure%20B_1.xlsx (link was not parseable by the web connector)
- https://nsearchives.nseindia.com/content/circulars/INSP67739.pdf

### 1.1 Margin and penalty file families

PX-030 recorded the NSE Clearing margin-report names:
- MG09 — CM margin summary;
- MG10 — TM/CP margin summary;
- MG11 — CM margin payable statement;
- MG12 — detailed CM file;
- MG13 — client-level margin file;
- MG14/MG15 — cross-margin benefit files.

PX-031 adds the need to treat these as different evidence levels:
- **MG09/MG11:** clearing-member summary, member payable/deposit context;
- **MG10:** Trading Member/Custodial Participant summary across its clients;
- **MG12:** detailed member/CP-level components and peak margin;
- **MG13:** client-level requirements and Client/Proprietary flag;
- **MG14/MG15:** cross-margin benefit at CM/TM or client scope;
- **UDiFF Margin/Penalty/Obligation files:** exact versioned records for the corresponding standardized report purpose.

Do not substitute an MG09 CM aggregate for a client's margin obligation. Do not treat MG15 cross-margin benefit as proof that every position or client qualifies. Do not assume the downloadable legacy MG naming and current UDiFF file names are interchangeable without the official mapping/circular.

## 2. Client margin snapshots, EOD reporting and short allocation

NSE Clearing's current Client Margin/Short Allocation Reporting page says:

### 2.1 Intraday snapshots

- Clearing Corporation sends a minimum of four client-wise margin snapshots per day.
- The snapshots are randomly selected from predefined time windows.
- The calculation for intraday snapshots uses fixed Beginning-of-Day (BOD) margin parameters.
- The minimum margin includes BOD SPAN, BOD ELM and net options premium payable at the time of the snapshot.

The source describes the snapshot requirement used for verification/reporting. The live clearing-margin obligation remains subject to the distinction documented by SEBI and PX-030: actual clearing parameters continue to update intraday/EOD.

### 2.2 EOD and peak collection reporting

The same page says:
- EOD margin is based on EOD positions and BOD margin parameters;
- clearing/trading members report margin collected from each TM/CP/client at EOD and the peak margin collected during the day.

A future parser must preserve both the EOD figure and the peak-across-snapshots figure with each snapshot and reporting period. It must not collapse them to one field called “margin collected”.

### 2.3 Client collateral allocation

The page requires Clearing Members to ensure sufficient collateral is allocated to TM Prop/CP/clients. If the Clearing Corporation margin applicable to a TM Prop/CP/client exceeds collateral allocated to that party plus its securities collateral re-pledged to the Clearing Corporation, member proprietary collateral can be blocked and deemed allocated to that party under the published process.

Consequences:
- the source client allocation and the deemed member-proprietary allocation are distinct;
- deemed allocation is not proof that the client independently funded the same value;
- collateral must remain scoped to the member/CP/client and segment;
- a Clearing Member's own collateral block cannot be silently recorded as a client cash receipt;
- the system must preserve which member supplied the backstop and which account/segment it supports.

### 2.4 Short allocation definition

NSE Clearing defines short allocation as minimum client margin collection requirement less client collateral value in the segment, where minimum collection exceeds collateral value.

For this purpose:
- minimum client margin collection means upfront margins (BOD SPAN/ELM and net option premium at the snapshot/EOD);
- margins which are permitted to be collected by T+1/T+2 are excluded from this specific minimum upfront short-allocation requirement;
- client collateral value is the relevant collateral allocated by the CM to the client in the segment plus securities collateral re-pledged at the Clearing Corporation for that client, using the stated valuation basis.

This is a specific reporting/penalty definition. It must not be substituted for:
- the complete client margin liability;
- all delivery/CCO collection obligations;
- the broker's available-funds value;
- a client cash ledger;
- CM aggregate deposit/shortfall.

### 2.5 Shortage comparison and penalty basis

The page describes three comparisons:
1. EOD client/TM/CP margin obligation vs the respective margin available at EOD;
2. peak margin obligation across snapshots vs the peak margin available during the day;
3. highest intraday/EOD short-allocation amount after eligible excess cross-segment collateral and valid reason codes.

The higher shortfall among these is considered for penalty.

The page further says:
- non-reporting/non-submission of client margins is treated similarly to 100% short reporting;
- short/non-reporting/short-allocation penalties are levied as prescribed by Clearing Corporation from time to time;
- members/TMs/CMs/custodians have a reporting upload window up to T+5 working days and sign-off on the sixth working day.

**Critical distinction:** the T+5 upload/sign-off window is a reporting procedure. It does not defer the requirement to collect upfront margin before trade or convert a reporting deadline into a client payment grace period.

Source:
- https://www.nseclearing.in/risk-management/equity-derivatives/client-margin-reporting

## 3. PRISM, effective collateral usage and member-level enforcement

NSE Clearing's current Violations page describes PRISM (Parallel Risk Management System) as its real-time position monitoring and risk-management system for Futures and Options. It monitors trading and clearing members and generates alerts/disablement messages when set limits are breached.

### 3.1 Trading Member margin-utilization monitoring

For TM positions, the page states:
- total initial and ELM margin is computed in real time;
- this is compared with TM effective collateral;
- warning messages are issued at 70%, 80% and 90% effective-collateral utilization;
- at 100% utilization, the Trading Member's trading facility is withdrawn.

These levels describe NSE Clearing's **Trading Member** control. They MUST NOT be copied as generic retail-client RMS thresholds or asserted as Zerodha/Upstox/Dhan client-specific square-off thresholds.

### 3.2 Clearing Member and TM margin violations

The same page defines a Clearing Member margin violation where:
- CM margin liability exceeds effective deposit less minimum liquid net worth; or
- a TM's margin liability exceeds the limit specified by its Clearing Member;
- the condition may occur at any time, including during trading hours.

NSE Clearing's broader violation text states that members may reduce positions by closeout or bring additional cash/collateral, and that a CM must set limits for enablement when a TM has a margin violation. The separate Payment of Margins page says non-fulfillment of whole or part of margin obligations attracts penalty and may trigger withdrawal of trading/clearing facilities or closeout of outstanding positions.

The Payment of Margins page itself is marked updated 16 November 2021. Its disciplinary examples are treated as a general enforcement disclosure, not as a complete current operational rulebook. Any actual enforcement rule must be tied to the current applicable circular and member agreement.

Sources:
- https://www.nseclearing.in/risk-management/equity-derivatives/violations
- https://www.nseclearing.in/risk-management/equity-derivatives/payment-of-margins

## 4. Important boundaries and non-claims

- The UDiFF catalogue is verified; the Annexure B XLSX field-level schema was not inspected because the connector rejected the Excel content type. Sample ZIPs were also inaccessible in this research session. No claim is made about actual row layouts, field offsets or exact current filename patterns.
- UDiFF circular history proves report schemas are versioned and changed, including an option-premium update to margin files; exact mappings must be read from the applicable workbook/circular attachment before parser implementation.
- MG09–MG15 are different report scopes; totals must not be confused across CM/TM/client levels.
- Client margin short allocation is a special minimum-upfront-collection test, not every form of margin liability or settlement obligation.
- Deemed allocation from member proprietary collateral must not be mislabeled as client-collected margin.
- Four snapshots is a minimum described by the page; their times are randomly selected from predefined windows, so a test cannot expect a fixed clock schedule.
- T+5 report upload/sign-off is not a grace period for upfront collection.
- PRISM 70/80/90/100 thresholds are stated for Trading Member effective-collateral usage; they are not retail-client risk thresholds.
- Member violation / position-limit violation / client short allocation are separate control categories.

## 5. Additional requirements for PX-025

### R-077 — Clearing-report parser is UDiFF-versioned

A future report-ingestion component MUST pin the UDiFF standard/workbook version, applicable circular, report name, segment and effective date for every parsed file. It MUST preserve the original file/hash and parser version. It MUST NOT infer field positions, codes or semantics from an older report or from a filename alone.

### R-078 — Intraday margin snapshots are individually preserved

Every client-wise snapshot MUST retain its original report identity, snapshot time/window, client/TM/CP/member scope, segment, parameter version and raw margin components. The implementation MUST support the minimum-four-random-snapshot framework without assuming fixed snapshot times.

### R-079 — EOD, peak and short-allocation measures remain distinct

The system MUST preserve EOD requirement, each intraday snapshot requirement, peak-across-snapshots requirement, reported collection, available margin and short allocation separately. It MUST NOT replace them with one daily total or assume that agreement in one comparison proves all other comparisons pass.

### R-080 — Collateral allocation is explicitly scoped

Collateral allocation MUST be tracked by Clearing Member, Trading Member, Custodial Participant, client/proprietary flag, segment and collateral source. Allocated collateral and securities re-pledged to the Clearing Corporation MUST be separately identifiable and must not be attributed to the wrong client or segment.

### R-081 — Deemed member-proprietary allocation is not client collection

Where member proprietary collateral is blocked/deemed allocated to cover a TM Prop/CP/client margin requirement, the system MUST preserve the provider-deemed allocation, supplying member, supported beneficiary and segment as a separate evidence event. It MUST NOT represent the blocked member collateral as cash or collateral actually paid by the client.

### R-082 — Short allocation uses the published minimum-upfront definition

The short-allocation calculation MUST use the applicable published minimum client upfront collection requirement (including BOD SPAN/ELM and net option premium where effective) less the defined eligible client collateral value in that segment. It MUST respect the source's specific exclusions for margins permitted to be collected by T+1/T+2. The resulting short-allocation metric MUST NOT be substituted for total margin liability.

### R-083 — Shortfall penalty comparison preserves all three tests

The calculation MUST preserve the separate EOD shortfall, peak-across-snapshots shortfall and highest intraday/EOD short-allocation amount after permitted excess collateral/reason codes. Where the applicable rule uses the higher amount, the source inputs and selected maximum MUST remain reproducible.

### R-084 — Report upload/sign-off deadlines are distinct from collection deadlines

The system MUST record report upload and sign-off status against the applicable reporting calendar (including the published T+5 upload/sixth-working-day sign-off procedure where effective). It MUST NOT interpret this reporting window as permission to delay upfront client collection.

### R-085 — Non-reporting is an explicit full short-reporting exception

Missing or incomplete client-margin reporting MUST be recorded as a separate non-reporting exception and processed according to the applicable rule (the reviewed page treats it similarly to 100% short reporting). An absent file MUST NOT be treated as a zero-margin/zero-shortfall report.

### R-086 — Member-level risk utilization thresholds remain scoped to the member

Any implementation of the published PRISM 70%/80%/90% warnings and 100% Trading Member facility withdrawal MUST bind them to the TM effective-collateral scope and effective rule version. It MUST NOT apply those values as universal retail-client RMS thresholds or automatically square off a client solely from this member-level page.

### R-087 — CM/TM violations and client short allocation remain distinct

The system MUST separately classify client short allocation, TM effective-collateral utilization/limit violation, CM effective-deposit/liquid-net-worth violation and position-limit violation. A violation at one layer MUST NOT be misreported as a client shortfall at another layer without source-supported allocation.

### R-088 — Risk-enforcement response is evidence-backed

A member-level margin violation response (additional collateral, member limit change, facility disablement, closeout or other action) MUST retain the triggering requirement, effective collateral, utilization, threshold, member scope, source event/time and observed enforcement result. A warning message alone MUST NOT be recorded as a completed closeout or as proof that collateral was deposited.

## 6. Additional deterministic acceptance scenarios

These extend AT-001 through AT-130. All use deterministic synthetic UDiFF/report/clearing fixtures; no membership portal or live clearing file is needed.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-131 | Margin report is parsed without a known UDiFF version/circular | Reject semantic parsing or return UNKNOWN; preserve original file/hash and do not guess fields |
| AT-132 | UDiFF margin file changes to include net option premium under NCL/CMPT/65315 | Apply only the date-effective schema; retain premium as a separate component |
| AT-133 | T+0 settlement report schema revision is encountered | Select the applicable report/version/segment; do not parse it as an unchanged prior UDiFF file |
| AT-134 | Only three intraday snapshots are present where the effective framework requires at least four | Snapshot-set completeness exception; no peak-verification PASS |
| AT-135 | Four snapshots have different client SPAN/ELM/net-premium values | Preserve each timestamp and calculate peak across the actual provided snapshots |
| AT-136 | EOD margin file uses EOD positions and BOD parameters | Retain both effective parameter purpose and EOD position scope; do not compare it as live intraday clearing margin |
| AT-137 | MG09/10 CM/TM totals and MG13 client details are ingested together | Preserve report scope and reconcile aggregates without substituting CM totals for a client amount |
| AT-138 | Same instrument/client appears in two segments with separately allocated collateral | Maintain segment-specific collateral allocation; no silent cross-segment or cross-client reuse |
| AT-139 | Client allocated collateral is short and CM proprietary collateral is blocked as deemed allocation | Record the deemed allocation and supplying member separately; do not mark client-paid collateral as increased |
| AT-140 | Re-pledged securities collateral is part of client collateral value | Apply the source-defined segment/client scope and collateral value basis; preserve raw and eligible values |
| AT-141 | Short-allocation calculation has upfront SPAN/ELM/net premium plus other T+1 collection items | Include the prescribed upfront components and exclude only the margins the short-allocation definition permits to be collected later |
| AT-142 | One client's collateral exceeds requirement while another client is short | No cross-client offset; short allocation remains client-specific |
| AT-143 | Report file is uploaded on T+5 and signed off on sixth working day | Record as reporting timeliness only; upfront collection deadline remains unchanged |
| AT-144 | Client margin report is not submitted | NON_REPORTING exception with the published 100%-short-reporting treatment; no zero-filled file |
| AT-145 | EOD shortfall, peak shortfall and short-allocation metrics differ | Preserve all three and select the rule-defined higher amount for penalty; keep calculation trace |
| AT-146 | TM effective collateral reaches 70% utilization in PRISM | Record TM-level warning only; do not apply an automatic retail-client square-off |
| AT-147 | TM effective collateral reaches 80% utilization | Record the correct TM-level warning and utilization evidence |
| AT-148 | TM effective collateral reaches 90% utilization | Record the correct TM-level warning and utilization evidence |
| AT-149 | TM effective collateral reaches 100% utilization | Record facility withdrawal for the TM scope; do not assume every client account has been individually disabled unless separately evidenced |
| AT-150 | CM liability exceeds effective deposit less minimum liquid net worth, or TM liability exceeds CM-set limit | Record member-level margin violation and enforcement evidence separately from client short allocation |

PX-025 now contains **88 normative requirements (R-001–R-088) and 150 proposed acceptance scenarios (AT-001–AT-150)**. These scenarios are proposed; no parser, margin report integration, fake provider or risk-enforcement implementation exists in this research work.

## 7. Research decisions and non-authorization

- **ACCEPT:** UDiFF version and report type must be part of the source contract; preserve originals and parser provenance.
- **ACCEPT:** retain four-or-more randomly timed client snapshot observations, EOD, peak, allocation, short allocation and reported collection as separate evidence.
- **ACCEPT:** deemed member collateral allocation is not client payment.
- **ACCEPT:** short-allocation/penalty comparison is not interchangeable with total margin liability or a cash-ledger balance.
- **ACCEPT:** non-reporting, late/missing evidence and member-level PRISM violations are explicit exceptions.
- **DEFER:** parsing Annexure B fields and sample rows until the official workbook/ZIP can be inspected; no field-level schema is claimed by this record.
- **DEFER:** automatic client RMS action/auto square-off; PRISM's published thresholds are member-level and do not establish broker retail RMS policies.
- **NOT AUTHORIZED:** member portal access, clearing/broker API calls, sandbox/production interaction, real orders, code changes, paid services, PR or merge to `main`.

**Final status:** PX-031 clearing margin-report, client short-allocation and member-level risk-enforcement audit documented. PX-025 expanded to 88 requirements and 150 proposed acceptance scenarios. UDiFF format workbook/sample files were not inspected; no broker/clearing endpoint was used.
