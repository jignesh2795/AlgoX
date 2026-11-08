# PX-2026-023 — NSE feed protocol, historical order data and deterministic replay feasibility

**Research date:** 2026-11-08  
**Status:** primary-source audit substantially advanced; historical version and entitlement closure still open  
**AlgoX area:** Indian market data / event sourcing / deterministic replay / research data access  
**Scope:** NSE CM and F&O, focusing on 2023 public evidence and current 2026 access routes  
**Decision boundary:** research only; no parser, broker integration, purchase, data application or execution change authorized.

## Executive finding

NSE's January 2023 public market-data circular confirms that tick-by-tick order and trade multicast (MTBT) was provisioned for both Capital Market (CM) and Futures & Options (FO), with segment-specific stream masters. It documents TCP recovery for missed ticks and an order-book snapshot recovery service refreshed every 30 seconds. This establishes that exchange-level order/trade event infrastructure existed in 2023 for both segments.

The circular does not identify the exact in-force protocol revision for every segment or publish sufficient snapshot-message detail to certify a 2023 snapshot as a sequence-aligned replay checkpoint. A separate archived FO MTBT document is version 6.1 (January 2019); a CM/CD document is version 6.2 (September 2021) and its revision history records an FAO feed discontinuation in that document's lineage. Since the 2023 circular still lists FO MTBT streams, these documents must not be collapsed into a single protocol story. The exact 2023 FO protocol/version and snapshot schema remain open pending an authorized, date-pinned source.

A second important route is now evidenced: NSE's non-confidential Historical Order & Trade specification v1.18 (18 May 2026) describes full historical order-book-event and trade datasets for CM and F&O. It states that full orders are made available after 90 calendar days and full trades after 30 days, in fixed-length records with consistent sequencing and timestamps suitable for historical reconstruction. This is a stronger candidate for offline replay than trying to reconstruct history from retail broker WebSockets. It is a subscription product, not a free public dump.

A possible non-commercial research route exists under the SEBI/NSE research-data framework and the NSE Data Room, but eligibility and the treatment of the TBT subset must be clarified. No application has been submitted and no data has been purchased.

## 1. What the 2023 public record establishes

NSE Circular 03/2023, dated 23 January 2023, consolidates market-data broadcast arrangements and explicitly lists tick-by-tick order/trade multicast for CM and FO, with separate segment-specific contract/stream master files.

The circular documents:
- MTBT stream and contract-master mapping for the CM and FO segments;
- primary and delayed multicast channels;
- missed-tick recovery over TCP;
- a non-persistent TCP recovery connection for each request, with recovered data potentially lagging the direct multicast feed;
- an order-book snapshot recovery service constructed from MTBT, refreshed every 30 seconds, returning outstanding orders through the last refresh point for a stream.

This is sufficient to confirm the existence of 2023 CM and FO MTBT service and a documented recovery facility. It is not enough, by itself, to establish exact packet schema/version, historical message completeness, or the sequence-watermark contract for the 2023 snapshot service.

No member connection parameters, authentication material or restricted protocol payloads are reproduced in this public research record.

## 2. Protocol versioning: do not infer the missing 2023 FO schema

The source trail contains distinct documents:
- Archived FO MTBT API specification version 6.1, dated 30 January 2019.
- Archived CM/CD MTBT API specification version 6.2, dated 1 September 2021; its revision history records an FAO-feed discontinuation in that document's lineage.
- The 2023 Circular 03/2023 nevertheless lists active FO MTBT multicast streams.
- The current NSE member protocol catalogue lists separate MTBT documentation for CM and FO. Current protocol documents are explicitly marked confidential/proprietary.

These are not enough to assert that FO used the archived 2019 v6.1 schema throughout 2023, nor that the CM/CD v6.2 document describes FO. The appropriate conclusion is:

**2023 FO MTBT service: evidenced. Exact in-force FO schema/revision on a given 2023 date: unresolved.**

Any eventual parser or replay benchmark must pin the exact segment, date, protocol revision and entitlement. The public repository will record this conclusion and the official catalogue link, but will not reproduce member-confidential schemas.

## 3. Current market-data products are not identical to member feed facilities

NSE's current member protocol catalogue lists MTBT protocol documents by segment. Its paid real-time subscriber catalogue presents a different product matrix: CM/CD tick-by-tick products and separate F&O depth products are listed. The two catalogues serve different access routes.

Therefore:
- a member-facing protocol's existence does not prove ordinary retail-subscriber access to that protocol;
- a broker's aggregated depth API is not equivalent to exchange MTBT;
- an API's depth level count does not prove order-by-order identities or FIFO queue observability;
- access, usage, persistence, retention and redistribution terms must be checked independently.

## 4. Historical Order & Trade data: strongest offline replay candidate

NSE Historical Order & Trade specification version 1.18, dated 18 May 2026, describes:
- a full version of order and trade messages representing the order-book events and executed trades captured during the trading day;
- supported CM and F&O order/trade data layouts, as well as other market segments;
- fixed-length record formats and consistent sequencing;
- timestamps and identifiers needed for historical event reconstruction;
- full order files made available after 90 calendar days;
- full trade files made available after 30 calendar days.

This is strong evidence that NSE offers a structured, deterministic-parsing-oriented historical order/trade dataset for offline research. It is still a subscription product; the current NSE EOD/historical-data page directs prospective customers to the data subscription channel. This record does not assume historical 2023 files are included in any particular subscription, nor infer the exact coverage period or price.

**Research implication:** compare the historical full-data product with MTBT multicast before designing a replay pipeline. The historical file product may avoid the need to capture and recover live UDP sessions, while retaining per-order event history. Availability windows, segment coverage, corrections, identifier semantics and licensed use still require confirmation.

## 5. Research-data and lower-cost access routes

### 5.1 SEBI research-data policy

SEBI Circular SEBI/HO/DEPA-II/DEPA-II_SRG/P/CIR/2024/178 dated 20 December 2024 establishes a data-sharing framework for research/research publications undertaken by accredited academic institutions. It distinguishes shareable first-basket data from restricted data. For qualifying voluminous data, it calls for a reasonable amount to be supplied free of charge up to 2 GB per researcher per year when no additional computation is required; very high volume or additional processing/value addition may be charged on a cost basis.

### 5.2 NSE's published data list

NSE's published research-data list places tick-by-tick historical trades and orders without client and broker information in its voluminous-data category. The same list identifies a separate restricted category for more sensitive client/member-linked information. Its footnote describes the TBT research-data period as six months before the request, although the wording in the published PDF is incomplete and requires clarification.

There is a practical ambiguity to resolve before planning around the free allowance: NSE's list labels the TBT dataset as voluminous/chargeable, while SEBI's circular provides a 2 GB/year free allowance for qualifying first-basket voluminous data without extra computation. The request form and NSE's data team must clarify whether a small TBT sample fits that allowance, which exact six-month window applies, and whether the requester meets the academic-institution requirement.

NSE's Data for Research page says that research-provided data is limited to academic and non-commercial use and provides a request route. AlgoX must not assume that a private or potentially commercial project is eligible.

### 5.3 NSE Data Room

NSE describes a cloud-based Data Room for granular historical order/trade research. Access is proposal-based, reviewed by an independent external committee, and offered as a time-bound research grant without monetary consideration. The current page refers to researchers from academia and beyond; the original 2021 press release also describes time-bound access through the EPR research proposal route.

This is a potentially useful no-purchase route, but it is approval-dependent, cloud-hosted rather than local-first, and subject to the Data Dissemination and Operational Guidelines. Whether an independent AlgoX project qualifies, what exact datasets are available, and whether outputs can be exported or published are not verified.

**No data application has been prepared or submitted. No vendor, exchange or broker has been contacted. No subscription or paid dataset has been approved.**

## 6. Deterministic replay model: research requirements

The findings support a stream-aware event-sourcing design as a research candidate, not yet a final architecture decision.

1. Preserve raw source messages/files immutably with capture provenance, segment, trading date, protocol/schema version, stream, event time, receipt time and integrity checksum.
2. Load the contract/security master applicable to the exact trading date before interpreting tokens. Preserve historical mappings; do not resolve old tokens using today's instrument master.
3. Reconstruct each stream in its own ordered event domain. Do not invent a global sequence across independent streams.
4. Detect duplicates and sequence gaps explicitly. A gap puts the affected book into an uncertain state until recovery is proven.
5. Apply recovered records in the correct sequence and retain the distinction between live-feed and recovery-feed provenance.
6. Use an order-book snapshot as a replay rebase only when its as-of boundary/watermark is verified against the corresponding event sequence. The public 2023 circular establishes the 30-second snapshot service but does not publish enough schema to establish this boundary for the 2023 implementation.
7. Do not silently repair unknown order references, missing amendments, unobserved order classes or trade/cancel corrections. Preserve an explicit unknown/degraded state.
8. Keep cross-stream event ordering uncertainty explicit. Stream-local sequence is not a universal cross-market clock.
9. Make replay deterministic by pinning data, schema, master files, parser version, event-order policy and recovery policy. Compare reconstructed book states at known checkpoints.
10. Record any missing/corrected data and the impact on downstream fill/queue experiments; a replay with unresolved gaps cannot be labelled fully verified.

## 7. Proposed acceptance tests (not implemented or run)

- Complete stream: replay a known session twice and compare state hashes at fixed sequence checkpoints.
- Duplicate packet: replaying a duplicate must not change the reconstructed state twice.
- Missing sequence: the stream must be marked degraded and must not silently continue as a verified book.
- Successful tick recovery: recovered interval is inserted in the right location and the resulting book matches a clean capture.
- Failed/incomplete recovery: the book remains uncertain; no synthetic events are invented.
- Snapshot restore: accepted only when its as-of watermark and stream identity are verified.
- DR/session reset: sequence resets must be distinguished from duplicates and ordinary gaps using the authorized version-specific protocol and feed metadata.
- Historical masters: replay uses the master file for the historical trading date, not a current contract master.
- Segment/schema variation: CM and FO use the correct pinned protocol/data layout.
- Full historical file replay: compare resulting order/trade state and fill outputs with the source dataset's documented event semantics.

These acceptance tests are proposed research gates. No code, fixtures or benchmark results have been produced.

## 8. Research decisions and unresolved questions

- **ACCEPT:** the January 2023 public circular confirms MTBT stream infrastructure for both CM and FO.
- **ACCEPT:** tick recovery and order-book snapshot recovery existed in 2023; they must be modeled as distinct recovery mechanisms.
- **ACCEPT:** full historical Order & Trade data is a strong candidate for offline deterministic replay and is more promising than trying to backfill years of history from retail WebSockets.
- **ACCEPT WITH LIMITATION:** public 2023 information does not establish the exact F&O protocol revision or snapshot-watermark semantics.
- **ACCEPT WITH LIMITATION:** the current historical order/trade product is not assumed free; no purchase is approved.
- **INVESTIGATE:** whether an independent AlgoX research proposal can be accepted by NSE's Data Room / EPR route.
- **INVESTIGATE:** whether a small first-basket TBT dataset can be supplied inside the SEBI 2 GB/year free allowance and what the six-month restriction means in practice.
- **INVESTIGATE:** exact 2023 FO protocol revision and authorized snapshot message semantics.
- **DEFER:** parser design, event-replay implementation, matching-engine integration and any execution changes until authorized sample data and exact schemas are available.

## 9. Next research sequence

1. Audit the public sample files and non-confidential historical Order & Trade spec for CM and FO. Record which fields and event types are sufficient to rebuild each book.
2. Determine whether sample data is freely downloadable and whether its usage terms permit local research fixtures.
3. Compare a small historical full-file replay with the event semantics described in the 2023 member circular. Do not require a paid subscription for this investigation.
4. Clarify the research-data 2 GB allowance and six-month window from NSE's official request process; screen Data Room eligibility without submitting an application.
5. Only then define the deterministic replay experiment and its gap-recovery tests.
6. Continue the historical 2023 Indian-market gap audit with broker disconnect/reconnect, ambiguous submission outcomes and reconciliation.

## Sources

### NSE public 2023 feed evidence
- NSE Circular 03/2023, 23 January 2023 — Market Data Consolidated Circular: https://archives.nseindia.com/content/circulars/MSD55333.pdf
- Archived FO MTBT API Specification v6.1, 30 January 2019: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/MTBT_FO_NNF_PROTOCOL_6.1_0.pdf
- Archived CM/CD MTBT API Specification v6.2, 1 September 2021: https://nsearchives.nseindia.com/content/press/Realtime_CM_CD_TBT.pdf
- NSE current member Trading Protocols catalogue: https://www.nseindia.com/static/trade/platform-services-neat-trading-system-protocols

### NSE historical data
- NSE Historical Order & Trade Specification v1.18, 18 May 2026 (Non-Confidential): https://nsearchives.nseindia.com/web/mediaattachment/2026-05/NSE_Hist_Order_Trade_Data_1.18_20260518122214.pdf
- NSE Paid EOD / Historical Data page: https://www.nseindia.com/static/market-data/eod-historical-data-subscription
- NSE Paid Real-Time Data page: https://www.nseindia.com/static/market-data/real-time-data-subscription

### Research access
- SEBI Circular 2024/178, 20 December 2024 — Policy for Sharing Data for Research/Analysis: https://www.sebi.gov.in/sebi_data/attachdocs/dec-2024/1734693561713.pdf
- NSE Data List Under the NSE Data Sharing Policy for Research and Analysis (2025-07-28 PDF): https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Data%20list%20under%20NSE%20Data%20Sharing%20Policy%20for%20Research%20and%20Analysis_20250728.pdf
- NSE Data for Research: https://www.nseindia.com/static/research/initiatives-data-for-research
- NSE Data for Analytics / Data Room: https://www.nse.in/static/research/initiatives-data-for-analytics
- NSE Data Room launch press release, 13 April 2021: https://nsearchives.nseindia.com/web/sites/default/files/2021-04/PR_cc_13042021.pdf

## Evidence and confidentiality discipline

This is a research synthesis, not a source-closed reverse-engineering report. The exact 2023 FO member protocol and detailed member-only packet/snapshot schemas remain unverified in an authorized, date-pinned source. Current member protocol documents are marked confidential/proprietary; this public record does not reproduce their schemas, connection details or access material. Historical claims must be tied to the correct segment, publication date and protocol revision.

No code was written, no broker/feed connection was initiated, no paid data was ordered, no application was sent, no live/paper execution behavior was changed, and main was not modified.
