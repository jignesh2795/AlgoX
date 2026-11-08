# AlgoX research session continuity — 2026-11-08

**Record type:** session continuity / research-state consolidation  
**Research branch:** `research/px-2026-023-nse-replay-data-audit-2026-11-08` (branched from the PX-2026-022 research branch)  
**Base:** `main` (research-only branch; no merge performed)  
**Status:** consolidated from the available conversation transcript, repository records and prior project context; source closure remains incomplete  
**Scope:** preserve the research work and decisions from this conversation so the next session can resume without relying on chat history alone.

## 1. AlgoX identity and governing purpose

AlgoX is an open-source, reusable research lab and algo-trading ecosystem—not merely a personal trading bot, a broker wrapper, or a UI. Its research scope includes open-source trading systems, architecture, strategies, market data, brokers, backtesting, execution, risk, AI/agents, failures, Indian-market infrastructure, and reusable/adaptable/rejected components.

The broader intended lifecycle is **Research → Validate → Simulate → Execute → Recover → Learn**, with deterministic trading-engine boundaries and an evidence/provenance/evaluation layer. The modular philosophy is kernel → adapters → capabilities → agents → UI → integrations. Research must distinguish observed behavior, documented capability, vendor/paper claims, local reproduction and architectural inference.

**Current task boundary:** this workstream is research and documentation. Do not implement a matching engine, alter broker/execution behavior, connect to a broker, purchase data, or merge research into `main` merely because a research record recommends further investigation.

## 2. Repository and continuity state

- Public repository: https://github.com/jignesh2795/AlgoX
- Default branch: `main`.
- Historical research/prototype branch previously identified: `research/algo-trading-github`, at `4dbc9f4c5f7052a1a25e398cc0ba64178019547f`; draft PR #1 remains unmerged.
- The 2026 ecosystem archive on `main` contains records PX-2026-001 through PX-2026-021.
- The prior continuation branch is `research/px-2026-022-indian-fill-realism-2026-11-08`.
- The current continuation branch is `research/px-2026-023-nse-replay-data-audit-2026-11-08`, branched from the PX-022 branch.
- The current branch contains PX-2026-022, PX-2026-023 and this updated continuity record. It is intentionally not merged.
- During this session, GitHub issue search returned no open issues; PR #1 was found as a draft research PR. This is a point-in-time connector result, not a permanent repository guarantee.

## 3. Research completed or substantially advanced in this conversation

### 3.1 Historical ecosystem research (2023–2025)

The earlier audit recovered substantial historical research, but the year-level summaries and status labels were stale or incomplete. Findings are provisional until each period's primary-source coverage, dates, project versions, architecture claims and contradictions are reconciled.

- **2023:** Indian-market execution, data and trading-engine gaps were identified. The current follow-up priority is realistic fills, deterministic replay, recovery, broker normalization, F&O lifecycle and dated cost/tax/margin assumptions.
- **2024:** reliability, agent-memory and financial-agent research was expanded. Historical reliability evidence and finance-agent comparisons still need closure.
- **2025:** finance-agent benchmarks, retrieval, sequential decision evaluation, and evolving-memory research were compared. These are different evaluation layers and must not be collapsed into one score.
- The year-level research records should be status-corrected only after evidence reconciliation; do not mark a period complete just because a synthesis exists.

### 3.2 Financial-agent and benchmark comparison

The conversation compared:
- Finance Agent Benchmark — financial research/knowledge questions;
- InvestorBench — sequential portfolio decisions;
- FinGAIA — multi-step financial tasks across domains;
- FinAgentBench — financial document and passage retrieval;
- FLAG-Trader — learned sequential trading policy;
- Agent Market Arena and AI-Trader — agent behavior in market simulations/evaluations.

**Key conclusion:** retrieval correctness, financial reasoning, portfolio decisions, trading performance and execution reliability are distinct capabilities. Their metrics are not directly interchangeable. Reported benchmark results require pinned datasets, evaluator, harness, model, environment, market assumptions and independent reproduction.

Memory research examined MemoryAgentBench (retrieval, test-time learning, long-range understanding, conflict resolution) and Evo-Memory (sequential task streams and reuse of prior experience). These provide better dimensions for AlgoX's memory experiments but do not prove that AlgoX memory improves decisions.

### 3.3 India-specific benchmark gap

- FABRIC was identified as a multilingual Indian-finance QA candidate (204 questions across six languages and several financial/regulatory domains). Its evaluation script and sample answer quality raised concerns: response collection is not equivalent to independently verified scoring, and unsupported answer claims must not be treated as trusted ground truth.
- AlphaAudit was identified as a promising Indian-equity strategy-audit research lead, including claims about survivorship-free data, costs, leakage and statistical validation. Reproducible public implementation and independent validation were not established in this session.
- India-specific financial knowledge, regulatory accuracy, historical market-data correctness, strategy validity and execution realism need separate benchmarks.

### 3.4 2026 agent-system research

The 2026 archive currently indexes PX-2026-001 through PX-2026-021. It covers agent evolution, retrieval evaluation, protocol boundaries, security/provenance, paper-to-agent knowledge, multimodal perception, sandboxed runtimes, inference architecture, recursive improvement, benchmark integrity, agent runtime authority, long-horizon evaluation, model catalogs and related infrastructure.

These are ecosystem research records and candidate patterns, not authorization to implement every project or adopt vendor claims. Preserve open-source vs open-weight vs hosted/API-only status, preview vs general availability, primary-source evidence and independent evaluation status.

## 4. Recovered experiment queue — not closed

The following original experiment identifiers remain pending until execution evidence is recorded:

| ID | Objective | Status |
|---|---|---|
| EXP-ALG-001 | Persistence baseline and workload measurements | Pending controlled execution |
| EXP-ALG-002 | Evidence retrieval quality | Pending controlled execution |
| EXP-ALG-003 | Memory effect on research decisions | Pending controlled ablation |
| EXP-ALG-004 | Governed learning gate | Pending validation |
| EXP-ALG-005 | Research-agent reliability fixtures | Pending validation |
| EXP-ALG-006 | Single-agent vs multi-agent comparison | Pending controlled comparison |
| EXP-ALG-007 | Reproducible experiment replay | Pending validation |
| EXP-ALG-008 | Temporal contradiction benchmark | Pending validation |
| EXP-ALG-009 | Evidence-to-decision reconstruction | Pending validation |
| EXP-ALG-010 | Indian-market execution semantics | Pending validation |

Designs, fixtures, literature coverage or a repository record do not constitute completed experiments.

## 5. 2023 Indian-market execution gap — current active workstream

The most recent research phase studied fill realism, queue reconstruction and market impact. Its dedicated record is [PX-2026-022](PX-2026-022-indian-market-fill-realism-and-market-impact.md).

The central result is an execution-fidelity ladder:

- **L0:** OHLCV/bar approximation.
- **L1:** trades/quotes and best bid/ask.
- **L2:** aggregated market-by-price depth; supports book-walking and coarse queue proxies.
- **L3:** sequenced order add/modify/cancel/trade events plus exchange rules; can support displayed queue reconstruction if feed completeness, identifiers, timestamps and recovery semantics are adequate.
- **L4:** calibrated execution model with uncertainty intervals and out-of-sample validation.

Separate the following cost/effect components to avoid double counting:
1. spread crossing;
2. displayed-depth consumption/book-walking;
3. latency drift between decision, submission and exchange arrival;
4. residual market impact not already represented by displayed depth;
5. brokerage, exchange charges, taxes and other statutory costs.

For aggressive orders, model multi-level fills, partial residuals and limit-price protection. For passive orders, model quantity ahead, trade/cancellation queue depletion and exchange priority rules. Aggregated broker depth does not establish exact order-level queue position.

### NSE feed qualification

The session found 2023 NSE materials referring to tick-by-tick/order-and-trade feed capabilities across segments. However, archived protocol revisions, segment scope, later feed offerings, historical availability, entitlement and licensing were not fully reconciled. In particular, exact F&O packet mapping and protocol continuity remain unresolved. A historical circular is not proof of current entitlement or free access. Treat L3 feasibility as conditional until exact document IDs, packet schemas, segment rules and legal access are verified.

### Simulator acceptance criteria

Future validation must cover:
- partial fills across multiple price levels and insufficient depth;
- unfilled residual quantity and marketable-limit price protection;
- passive queue depletion by trades;
- amendment/cancellation priority changes under pinned segment rules;
- sequence gaps, duplicates, out-of-order events, snapshot recovery and stale-book rejection;
- latency injection;
- independent reporting of spread, depth, latency, residual impact, fees and taxes;
- calibration/test separation, out-of-sample checks and uncertainty reporting.

Measure fill ratio, time-to-fill, adverse selection, implementation shortfall, price improvement, residual quantity and calibration error by instrument, liquidity, volatility, order type, size and regime.

## 6. Decisions and non-decisions

**Accepted research principles**
- Use an explicit execution-fidelity ladder; do not use a binary "partial fill supported" label.
- Separate book-walking, latency drift, residual impact and statutory costs.
- Treat aggregated depth as adequate for L2 book-walking/coarse estimates, not exact queue reconstruction.
- Keep financial QA, retrieval, portfolio decisions, trading performance and execution reliability as separate evaluation domains.
- Maintain evidence provenance, temporal validity, contradiction tracking and reproducible experiment configuration.

**Still unresolved**
- Exact NSE 2023 segment-specific circulars, protocol revisions and F&O payload mapping.
- Historical data availability, entitlements, licensing, retention and costs.
- Reproducible 2023-version behavior of NautilusTrader, LEAN and Backtrader; the earlier comparison is a research lead that must be checked against pinned source revisions.
- A legally usable Indian-market dataset at each fidelity level, including a lower-fidelity free-data fallback.
- Controlled results for passive fill probability, queue estimation and residual impact.
- Closure of the broader 2023–2025 historical research and EXP-ALG-001 through EXP-ALG-010.

**Not authorized by this research record:** implementation, broker connection/submission, live trading, paid data procurement, production actions, or merging to `main`.

## 7. Recommended next sequence

1. **Close the source register for NSE feed claims:** exact circular/document IDs, dates, segment, protocol revision, packet fields, sequence/recovery behavior, entitlement and license.
2. **Pin and verify framework evidence:** NautilusTrader, LEAN and Backtrader commits/tags corresponding to the historical period; record exact tests, skipped tests and fill-model behavior.
3. **Map data availability by fidelity level:** identify a lawful historical dataset and a clearly qualified free fallback.
4. **Specify deterministic order-book replay and integrity tests:** sequence gaps, snapshots, duplicates, stale state and recovery.
5. **Only then design controlled fill experiments:** aggressive fills, passive fills, latency and residual impact as separate experiments.
6. Continue closing the remaining 2023 gaps, then reconcile 2024 and 2025, then complete the six newer agent-system research comparisons.
7. Consolidate architecture only after the evidence and experiment gates are satisfied.

## 8. Session provenance and limitations

This record consolidates information available in the conversation transcript, current repository records and prior AlgoX project context as of 2026-11-08. The original chat contained many web searches and summaries, but the transcript does not preserve every source URL, exact circular number, version pin or complete bibliography. This record therefore preserves conclusions and uncertainty; it does not falsely claim that every underlying source has been independently re-audited here.

No application code, broker integration or execution behavior was changed. The continuity record and PX-2026-022 are research documentation only.


## 9. Follow-up research update — NSE feed protocol and deterministic replay (2026-11-08)

A follow-up primary-source audit was completed and saved as [PX-2026-023 — NSE feed protocol, historical order data and deterministic replay feasibility](../ecosystem-history/2026/PX-2026-023-nse-feed-protocol-and-deterministic-replay.md).

### New verified findings

- NSE Circular 03/2023, dated 23 January 2023, explicitly lists MTBT order/trade multicast infrastructure for both CM and FO, with segment-specific stream masters.
- The same circular documents missed-tick TCP recovery and a 30-second order-book snapshot-recovery service. Recovered ticks can lag the direct multicast feed. The circular alone does not pin the exact 2023 FO schema or snapshot watermark contract.
- Historical protocol documents are segment/version-specific. An archived FO v6.1 document and a CM/CD v6.2 document are not sufficient to infer the exact FO version in force on every 2023 date. The current member protocol catalogue is separate from the ordinary subscriber product catalogue.
- NSE Historical Order & Trade specification v1.18 (18 May 2026) describes full order-book-event and trade datasets for CM/F&O. Full orders are available after 90 calendar days; full trades after 30 days. The dataset is a subscription product, not assumed free.
- SEBI Circular 2024/178 sets a first-basket voluminous-data free allowance of up to 2 GB per researcher per year where no extra computation is required, while NSE's research list classifies historical TBT order/trade data without client and broker information as voluminous and includes a six-month-window footnote. Eligibility, exact lookback and whether a sample qualifies under the free allowance remain unresolved.
- NSE's Data Room is a time-bound, approval-based research route with no monetary consideration; it is cloud-hosted and eligibility/export conditions remain unverified for AlgoX.

### Replay research boundary

The candidate replay approach is stream-aware and fail-closed: preserve immutable source records, use historical contract masters, detect duplicates and gaps, keep recovery provenance, and mark books uncertain where continuity cannot be proven. A snapshot may only be used as a replay rebase when its as-of boundary is verified for the applicable historical schema. These are research requirements, not an approved architecture or implementation.

### Next task

Audit public sample files and the non-confidential historical Order & Trade specification for CM and FO. Determine whether the sample files are freely downloadable and usable for local research fixtures. Then compare a small file-based replay feasibility study with the 2023 MTBT semantics. Do not purchase data, submit an NSE application, connect to a broker, implement a parser or change execution behavior without a separate authorization.

### Source register additions

- NSE Circular 03/2023: https://archives.nseindia.com/content/circulars/MSD55333.pdf
- NSE Historical Order & Trade Specification v1.18: https://nsearchives.nseindia.com/web/mediaattachment/2026-05/NSE_Hist_Order_Trade_Data_1.18_20260518122214.pdf
- SEBI Circular 2024/178: https://www.sebi.gov.in/sebi_data/attachdocs/dec-2024/1734693561713.pdf
- NSE research-data list: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Data%20list%20under%20NSE%20Data%20Sharing%20Policy%20for%20Research%20and%20Analysis_20250728.pdf
- NSE Data Room / Data for Analytics: https://www.nse.in/static/research/initiatives-data-for-analytics


## 10. Historical research-file schema and replay-integrity follow-up (2026-11-08)

The PX-2026-023 research record has been expanded with the exact archived 2023 NSE Research Data layout and two important limitations.

### Exact format lineage

- NSE Historical Research Data Layout v1.10 is dated 27 July 2022.
- NSE Historical Research Data Layout v1.11 is dated 15 December 2023; its revision history identifies the v1.10 to v1.11 boundary.
- This makes v1.10 the documented layout before 15 December 2023 and v1.11 the documented layout from that date. Pin the full file URL and date, not just the label: an older separate document also carries a v1.11 label with a different date and content.
- The 2023 v1.11 Research Data format includes all order/trade ticks, order identifiers, jiffy timestamps, entry/cancel/modify activity, and buy/sell order references in trade records.

### Replay limits now evidenced

- The reviewed v1.11 and v1.18 file layouts have no documented per-event sequence-number field or explicit equal-timestamp tie-order guarantee.
- The v1.11 trigger files provide MD5 and byte size per file. This validates file delivery integrity, not exchange-event completeness or ordering.
- FAO files are split across stream files with non-overlapping contracts; preserve each file identity and do not create a global event sequence.
- In 2023 v1.11, FAO quantities are described as underlying shares. v1.12 (2024), v1.14 and v1.15 (2025) repeat this; v1.18 (2026) instead says derivative volumes are in contract units and need lot-size conversion. The exact point/meaning of this discrepancy is unresolved and needs sample/official confirmation.

### Public sample status

NSE links CM and FO sample ZIPs from its current historical-data product page. The current research environment could not fetch ZIP contents, so the samples have not been inspected. They must not be treated as a validated 2023 research-data fixture or as proof of data entitlement.

### Updated next action

Continue with the no-purchase route: establish whether a limited NSE Research Data TBT sample is eligible under the SEBI 2 GB/year allowance or the NSE Data Room research grant, and determine the exact historical row-order/tie semantics. Do not submit an application or contact NSE without explicit authorization. If data access is unavailable, the replay study must remain a specification-feasibility study with its uncertainty clearly recorded.

Source references added to PX-2026-023:
- v1.10: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Hist_Order_data_layout_1.10_0.pdf
- v1.11: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Hist_Order_data_layout_1.11_0.pdf
- v1.12: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Hist_Order_data_layout_1.12.pdf
- v1.14: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Hist_Order_Trade_Data_1.14.pdf
- v1.15: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/NSE_Hist_Order_Trade_Data_1.15.pdf
- CM sample: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Sample_CMsegment.zip
- FO sample: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Sample_FOsegment.zip


## 11. Replay feasibility verdict and documentation correction (2026-11-08)

**Current status: order-event reconstruction is feasible in principle; exact deterministic replay remains unproven.**

The v1.11 historical research files contain per-order lifecycle events and trade records with buy/sell order references. However, the reviewed public layouts do not expose a per-event sequence number or an explicit guarantee for ordering equal-jiffy events across separate order/trade files. Trigger files provide MD5 and byte-size checks, which prove delivered-file integrity but not event-level completeness/order.

The historical research-data format is versioned: v1.10 is dated 27 July 2022; v1.11 is dated 15 December 2023. A separate archived document also labelled v1.11 is dated 20 June 2022 and has different content. Always pin the full URL, document date and segment, not just the version number.

There is also an F&O quantity-unit discrepancy:
- v1.11 (2023), v1.12 (2024), v1.14 and v1.15 (2025) describe FAO quantities as underlying shares.
- v1.18 (2026) states that derivative volumes are in contract units requiring lot-size conversion.

This is unresolved as a specification change or correction. 2023 research must use the date-specific v1.11 specification as its initial interpretation, with actual sample rows/lot-size checks required before any numeric replay claim.

The current NSE CM/FO sample ZIP links were found on the official page but could not be downloaded in the research environment; they have not been inspected. Do not claim that a sample parser or replay was validated.

The next task is to test whether the file-order contract and quantity units can be verified from authorized sample data or NSE research access. Until then, report an event-order ambiguity state rather than a deterministic result. After that, continue with broker disconnect/reconnect, ambiguous submission outcomes and reconciliation.

The earlier wording that described historical data as having "consistent sequencing" was corrected in PX-2026-023. The research note now distinguishes file integrity, order-event reconstruction, trade linkage, event-ordering confidence and unit validation.


## 12. Broker disconnect, ambiguous outcomes and reconciliation (2026-11-08)

A new provider-documentation comparison has been recorded in [PX-2026-024 — Broker disconnect, ambiguous order outcomes and reconciliation](../ecosystem-history/2026/PX-2026-024-broker-disconnect-order-recovery-and-reconciliation.md).

### Verified findings

- **Zerodha Kite:** a broker OMS order ID does not prove exchange receipt or execution; `exchange_order_id` may be null. The API exposes order history and tradebook endpoints, an optional tag, and WebSocket order postbacks. The order history is day-scoped. The documented `guid` is not a usable client-supplied idempotency token.
- **Upstox:** order history can be looked up by tag and may return all matching orders; order details/history are day-scoped. Daily and per-order trade endpoints expose individual executions. The Portfolio Stream Feed includes updates across Upstox platforms. SDK auto-reconnect is documented, but no missed-event replay cursor was established in the reviewed pages.
- **DhanHQ:** the user/partner-generated `correlationId` can be used with `GET /orders/external/{correlation-id}`, explicitly documented for a missed order ID. Dhan also exposes order/trade books and live order updates; static-IP and rate-limit constraints apply.
- For all three providers, the reviewed public documentation does not establish exactly-once submission or safe duplicate suppression when repeating a placement with the same tag/correlation value.
- Live update streams are useful low-latency evidence, but the reviewed pages do not establish a common durable sequence cursor or missed-event replay guarantee. Reconciliation via order and trade read APIs is required after disconnect.

### Recovery boundary

If an order command may have reached the broker but the response is uncertain, keep the result in `SUBMISSION_UNKNOWN` / `RECONCILIATION_REQUIRED`. Do not automatically resubmit. Recover using provider-specific correlation/tag lookup, order history/book and trade records. Apply the same uncertainty treatment to modification and cancellation timeouts.

### Status and next step

Research and documentation only. No broker account, sandbox/production API, real order, code implementation, paid service or merge to `main` was used or authorized. The next research step is to turn PX-024 into a provider-neutral requirements and acceptance-test specification, while keeping external broker interactions closed unless separately authorized.


## 13. Broker-neutral recovery requirements and acceptance tests (2026-11-08)

PX-2026-025 has translated the provider comparison in PX-024 into a proposed requirements baseline and a deterministic fake-provider test matrix.

### Scope and deliverables

- 33 normative requirements cover durable intent/attempt evidence, unknown command outcomes, no blind retry, identity separation, order/trade reconciliation, event provenance, stream recovery, conflicts, child orders, session retention, risk gating, exact units, concurrency fencing and reproducibility.
- 43 deterministic acceptance scenarios cover lost acknowledgements, proven non-dispatch, delayed visibility, zero/one/multiple correlation matches, partial fills, duplicate trades, cancel/modify races, reconnect gaps, session rollover, process crashes, multi-worker races, manual orders, sliced orders, unit discrepancies and unknown statuses.
- The document defines candidate reconciliation outcomes and algorithm phases, while explicitly deferring final enums, schema, storage technology and adapter interfaces. PX-026 adds provider-specific slicing/batch/compound-order semantics and extends PX-025 with R-031 through R-033 and AT-036 through AT-043.
- Tests are specified only; no implementation exists in this workstream and no tests were executed.

### Requirements decision

The core rule remains: once a command may have reached the provider, missing acknowledgement means UNKNOWN. No automatic retry, replacement or false rejection is allowed before adequate reconciliation evidence is available. Order and trade observations must be reconciled independently, and unresolved exposure must not be treated as zero.

### Architecture relationship

PX-025 is proposed as a requirements input to the existing `ALG-ARCH-001` provenance baseline: intents/commands/attempts and provider observations must remain attributable; reconciliation is a derived claim that cites the evidence and policy/parser version used. This does not authorize architecture implementation or revise the architecture baseline itself.

### Status and boundaries

Research specification completed. Provider contract gaps remain open; all 10 future implementation gates in PX-025 remain OPEN, PARTIAL or PROPOSED. No broker API, account, sandbox, real order, code change, paid service, PR or merge to `main` was used or authorized.


## 14. Provider idempotency, slicing and compound-order recovery audit (2026-11-08)

PX-2026-026 records an official-documentation audit of provider idempotency, per-request correlation semantics, auto-slicing, multi-order batches and compound/super-order hierarchies.

### Provider-specific findings

- **Kite:** optional `tag` is an identification/filter value, not a documented idempotency token. The response `guid` is described as unusable. Auto-slicing can return independent successful order IDs and per-slice errors in one response, up to the documented maximum of 10 slices.
- **Upstox:** V3 single-order slicing returns multiple `order_ids`; optional tag length is 40 characters. The distinct V2 multi-order endpoint has required per-line `correlation_id` values unique within that payload (1–20 characters), and supports HTTP 207 / `partial_success` with per-line success/error results. This uniqueness rule is not a repeated-request idempotency guarantee.
- **DhanHQ:** `correlationId` is a tracking field and the published correlation lookup returns one order object. The order-slicing endpoint is documented, but its response structure is not supplied in the reviewed page. Super Orders have a top-level order ID and nested entry/target/stop-loss legs.

### Requirements and test amendments

PX-025 has been amended with R-031 (per-child group outcome), R-032 (provider-scoped correlation uniqueness) and R-033 (independent child-set completeness), plus AT-036 through AT-043. Totals are now 33 requirements and 43 proposed fake-provider acceptance scenarios. None has been executed.

### Current decision

No reviewed provider documentation establishes safe cross-request deduplication for repeated placement after a lost acknowledgement. Continue to treat a possibly dispatched request as UNKNOWN and do not retry based only on a repeated tag/correlation value. Compound and sliced results require per-child reconciliation; incomplete child sets remain unresolved.

No broker account, API, sandbox, real order, code implementation, paid service, PR or merge to `main` was used or authorized.


## 15. Broker observation consistency, stream recovery and trade-revision audit (2026-11-08)

PX-2026-027 records the provider-documentation audit of order-update stream continuity, REST observation consistency and trade correction semantics.

### Findings

- **Kite:** daily orders/order histories and trades/per-order trades are separate REST reads. WebSocket and HTTP postbacks provide order observations; the HTTP checksum verifies a received payload but does not prove complete delivery. The reviewed docs do not define an event cursor, missed-window replay or atomic order/trade snapshot.
- **Upstox:** the Portfolio Stream Feed starts updates after a successful connection. `order_request_id` is documented as request-count metadata and `order_ref_id` as an internal order identifier, not a stream sequence/cursor. SDK auto-reconnect controls reconnection but the reviewed docs do not promise replay of missed updates. Order and trade reads are separate.
- **DhanHQ:** Live Order Update messages carry order/exchange IDs and timestamps such as `LastUpdatedTime`; the reviewed schema does not define a sequence/replay cursor. Orderbook and tradebook are separate reads.
- The reviewed official trade API pages do not define a common trade-bust/correction/reversal contract. This is a documentation gap, not proof that corrections cannot occur.

### Requirements amendment

PX-025 now contains **36 normative requirements and 49 proposed acceptance scenarios**:
- R-034 requires event-history completeness to remain UNKNOWN without a documented stream continuity/replay contract.
- R-035 treats separate REST responses as independently timed observations unless a provider guarantees a shared atomic snapshot/watermark.
- R-036 requires original trades and corrections to be preserved append-only, with economic reversal only under authoritative provider semantics.
- AT-044 through AT-049 test these cases using synthetic fixtures only.

### Current result

Current order/trade state reconciliation and historical event-stream completeness are distinct outputs. Current state may be reconstructed without proving every missed transition was replayed. Conflicting or non-atomic observations remain visible; no last-arrival-wins balancing.

No broker endpoint, account, sandbox, real order, code implementation, paid service, PR or merge to `main` was used.


## 16. Portfolio, cash-ledger, charge and contract-note reconciliation audit (2026-11-08)

PX-2026-028 expands broker recovery into account-level economic reconciliation: portfolio positions, delivery holdings, cash ledger, charges, contract notes, funds/margin and external evidence.

### Provider evidence

- **Kite:** `net` and `day` positions are distinct; overnight equity moves from positions to holdings. Holdings include T+1, realised/settled, used/authorised and collateral quantities. The charges endpoint is labelled a virtual contract note and is not proof of the actual issued note.
- **Upstox:** exposes short-term positions, holdings, historical trades (documented for the last three financial years), trade-wise realised P&L, aggregate charges by segment/financial year and payment transactions. Historical trade examples include a blank trade_id for an MF record, so the identifier is not universally populated.
- **DhanHQ:** exposes holdings buckets (total, DP, T+1, available, collateral), open positions, a dated cash ledger with voucher/debit/credit/running-balance fields, paginated historical trades with exchangeTradeId and charge fields, and a separate fund-limit snapshot.
- **NSE investor advisory:** instructs investors to receive contract notes within 24 hours, account statements at least quarterly, and verify demat and exchange-reported balance records.

### Requirements amendment

PX-025 now contains **48 normative requirements and 75 proposed acceptance scenarios**:
- R-037–R-048 distinguish accounting layers, stable identity scope, explicit position/cash roll-forwards, holdings buckets, actual contract notes, dated charges, funds vs withdrawable cash, P&L dimensions, pagination completeness, external evidence and raw exact-decimal numerics.
- AT-050–AT-075 cover these cases through synthetic fixtures, including ledger running balance, unsettled holdings, missing notes, aggregate charges, cross-source duplicates, corporate actions, data pagination and exact-decimal preservation.

### Reconciliation rule

A tradebook does not establish cash balance; positions do not establish demat holdings; available margin does not establish withdrawable cash; and a charge calculator does not establish the issued contract-note amount. These dimensions must be reconciled independently and linked by evidence.

No broker endpoint, account, sandbox, real order, code implementation, paid service, PR or merge to `main` was used.


## 17. Indian derivatives expiry, exercise, physical settlement and corporate actions (2026-11-08)

PX-2026-029 documents NSE/SEBI requirements for expiry calendars, automatic option exercise and assignment, stock-derivative physical settlement, eligible cash/F&O netting, delivery margin, settlement obligations and contract adjustments.

### Key findings

- NSE's current equity-derivatives contract-specification page (updated 10 February 2026) says Tuesday expiry for the named index families and individual-security contracts, with previous-trading-day fallback if Tuesday is a trading holiday. A date-specific calendar and contract master remain mandatory.
- SEBI Circular SEBI/HO/MRD/DOPI/CIR/P/2018/161 mandated physical settlement for all stock derivatives, phased to completion by October 2019 expiry. Index derivatives are not share-delivery contracts; stock futures and stock options can create physical delivery/funds obligations.
- NSE's 3 January 2023 Settlement Mechanism page still says individual-security options are cash-settled; the 7 January 2023 Clearing Members page says only funds settlement for index/stock derivatives. These are explicitly recorded as stale/contradictory against the SEBI stock-derivative physical-settlement requirement and NSE Clearing's 31 March 2024 PFMI disclosure that distinguishes delivery-settled contracts and Expiry+1 settlement.
- NSE describes automatic European-style exercise at expiry for ITM options and random assignment of long ITM positions to short positions in the same series. Actual assignment/allocation evidence is required.
- SEBI Circular 2022/165 permits cash/F&O expiry netting only under specific eligibility, including the same TM-CM combination; institutional investors including FPIs are excluded; STT and stamp duty remain segment-wise.
- Delivery margin applies from expiry until settlement or early pay-in under the NSE physical-settlement FAQ. Initiated early pay-in is not confirmed settlement.
- NSE corporate actions can adjust strike/position/lot/futures base price; a merger can force-settle outstanding contracts on last cum-date and cancel GTC/GTD orders.

### Requirements and test amendments

PX-025 now contains **61 normative requirements and 100 proposed acceptance scenarios**:
- R-049–R-061 add contract-calendar versioning, settlement-mode classification, automatic exercise/assignment evidence, physical delivery direction, lifecycle stages, delivery margin/early pay-in, netting eligibility, client/CM layering, append-only settlement events, corporate-action adjustments, merger closeout, segment-specific taxes and shortage/default states.
- AT-076–AT-100 cover holiday expiry, historical calendar changes, index cash vs stock delivery, stock future/call/put obligations, ITM assignment, margin/early-pay-in, netting restrictions, taxes, client/CM aggregation, bonus/split/rights/dividend/merger actions and delivery shortfall.

All are proposed acceptance tests and remain unexecuted.

### Source conflict decision

The older NSE Settlement Mechanism/“Clearing Members” pages are not treated as the controlling current stock-derivative settlement rule where they conflict with the SEBI mandatory-physical-settlement circular and later NSE Clearing PFMI disclosure. The contradiction remains recorded and must be closed against the effective clearing circulars/rulebook before implementation.

No broker/clearing endpoint, account, sandbox, real order, code implementation, paid service, PR or merge to `main` was used.


## 18. Equity-derivatives margin calculation, collection and risk controls (2026-11-08)

PX-2026-030 records the NSE Clearing/SEBI margin framework and the broker margin-calculator surfaces for Kite, Upstox and Dhan. The full research record is [PX-2026-030 — Equity-derivatives margin calculation, collection and risk controls](../ecosystem-history/2026/PX-2026-030-equity-derivatives-margin-calculation-collection-and-risk-controls.md).

### Source-derived findings

- **SPAN:** NSE Clearing performs online intraday portfolio-based SPAN margining. Its public methodology describes 99% VaR over a one-day horizon, with a two-day horizon for futures where MTM may not be collected before the next market opens.
- **ELM:** separate and parameterized, with dated product/position exceptions. Current published rates are a parameter snapshot, not constants for a historical model.
- **Upfront collection:** F&O SPAN/ELM is collected before trade. From 1 February 2025, equity-derivatives upfront verification also includes net options premium payable at client level.
- **BOD vs live clearing:** fixed BOD parameters apply to client upfront-margin verification/shortfall assessment; actual Clearing Corporation margin parameters continue to update intraday and EOD.
- **Netting:** client positions are netted at individual-client level and grossed across clients without cross-client offset. Proprietary positions are separate.
- **CCO:** intraday CCO uses closed futures crystallized P&L and premium payable/receivable; EOD includes futures MTM, option premiums, expiry exercise/assignment and futures final settlement. CCO margin releases after settlement completion.
- **Collection timing:** NSE's current F&O FAQ says SPAN/ELM before trade and delivery/CCO by T+1. SEBI Circular 2025/57 aligns non-upfront margin collection to settlement day for the cash segment; that cash-segment rule is not generalized to F&O.
- **False reporting:** NSE treats uncollected/short-collected margin reported as collected as false reporting.
- **Broker APIs:** Kite returns per-order and basket margin calculations, Upstox exposes SPAN/exposure/net-buy-premium/tender fields, and Dhan exposes single/multi-order calculators plus fund-limit data. These are not proof of final Clearing Corporation obligation or actual client collection.

### Requirements and test amendments

PX-025 now contains **76 normative requirements and 130 proposed acceptance scenarios**:
- R-062–R-076 add dated margin parameters, portfolio context, net option premium, fixed BOD verification vs live clearing parameters, client-only netting, component attribution, hedge revocation, delivery/tender/assignment, CCO, segment-specific T+1 collection, actual collection evidence, peak snapshots, confirmed release, collateral segregation and shortfall fail-closed rules.
- AT-101–AT-130 cover parameter staleness, same-client portfolios, spreads, hedge breaks, upfront collection, premium, BOD/live distinction, snapshots, no cross-client/proprietary netting, provider APIs, expiry margin, collection timelines, CCO, ELM, false reporting, collateral haircuts, release and shortfall.

All are proposed acceptance scenarios; no tests or broker API calls were made.

### Critical modelling distinction

Required margin, client upfront/peak verification requirement, actual collected collateral, available funds, reported collection, utilized margin, shortfall and settlement-confirmed release are separate facts. A calculator or available-balance response does not prove actual collection.

No broker/clearing endpoint, account, sandbox, real order, code change, paid service, PR or merge to `main` was used.


## 19. Clearing margin reports, short allocation and PRISM risk enforcement (2026-11-08)

PX-2026-031 reviews NSE Clearing's current UDiFF catalogue, client margin/short allocation page, PRISM/violations page and payment-of-margin page.

### Key findings

- UDiFF standardizes Trade, STT, CTT, Stamp Duty, Position, Obligation, Margin, Penalty and Settlement Master report families. The catalogue shows versioned circular updates, including an option-premium margin-file update in NCL/CMPT/65315 (29 Nov 2024).
- The current client-margin reporting page specifies at least four randomly selected intraday snapshots, fixed BOD parameters for those verification snapshots, and SPAN/ELM plus net option premium payable at the snapshot.
- EOD margin, peak margin across snapshots, reported collection and collateral available must remain independent values.
- Clearing Members allocate collateral at TM Prop/CP/client and segment scope. Where client allocated/re-pledged collateral is insufficient, member proprietary collateral may be blocked and deemed allocated; that is not client-paid collateral.
- Short allocation compares the minimum upfront client collection requirement against the defined client collateral value; T+1/T+2 collectible margins are excluded from this particular short-allocation metric.
- Penalty comparison preserves EOD shortfall, peak shortfall and highest intraday/EOD short allocation. Non-reporting is treated similarly to 100% short reporting.
- Reporting upload may be allowed to T+5 working days with sign-off on the sixth working day; this is a reporting window, not an upfront-collection grace period.
- PRISM reports 70%, 80%, 90% TM effective-collateral utilization warnings and 100% Trading Member facility withdrawal. These are member-level controls, not universal retail-client RMS thresholds.

### Requirements and test amendments

PX-025 now contains **88 normative requirements and 150 proposed acceptance scenarios**:
- R-077–R-088 add UDiFF parser versioning, snapshot evidence, EOD/peak/short-allocation separation, collateral allocation, deemed member allocation, short-allocation definition, three-part penalty comparison, reporting deadline, non-reporting, member-level PRISM scope, CM/TM violation distinction and evidence-backed enforcement.
- AT-131–AT-150 cover unknown UDiFF version, option-premium file update, T+0 report versioning, snapshot completeness, MG report scope, collateral allocation, deemed allocation, short allocation, T+5 reporting, non-reporting penalty, peak/EOD comparison and PRISM threshold behaviour.

### Data limitation

The UDiFF catalogue page was reviewed. The Annexure B XLSX workbook could not be parsed by the connector and ZIP attachments were unavailable, so field-level layouts and sample rows were not inspected. Any future parser work must close this evidence gap before implementation.

No member portal, broker/clearing endpoint, sandbox, order, code implementation, paid service, PR or merge to `main` was used.


## 20. Position limits, MWPL ban period and intraday index risk monitoring (2026-11-08)

PX-2026-032 audits single-stock MWPL/ban controls, entity-level stock position limits and index-derivative intraday monitoring.

### Findings

- SEBI Circular 2025/79 moved single-stock market-wide OI to FutEq/delta-based measurement and changed MWPL calculation to the lower of 15% free float and 65x preceding-three-month ADDV in quantity, with 10% free-float floor; recalculated quarterly.
- The current FutEq stock-ban trigger is EOD >95% MWPL; ban starts next trading day. Trading resumes only when combined FutEq OI across exchanges is ≤80%.
- During a ban, Day 1 entity positions are stored as baseline. Subsequent comparisons use the prescribed 2 PM contract delta and EOD positions. Passive delta changes are distinguished from active position increases; sign-change rules and expiry-passive treatment are retained.
- NCL/CMPT/70271 (18 Sep 2025) defined entity scopes and the 2025 single-stock percentage limits. A secondary circular index surfaced NCL/CMPT/76459 as a later update (purportedly dated 21 Sep 2026, effective 1 Oct 2026), but the official NSE archive PDF was inaccessible; its metadata and Annexure I therefore remain unverified here. The 2025 percentage list is not treated as the current schedule.
- Index intraday monitoring uses at least four random snapshots. SEBI 2025/41 distinguished existing-limit intraday monitoring from penalty. NSE/SURV/71673 (5 Dec 2025) confirms expiry-day index-option ASD from 8 Dec 2025, held for one month, with intraday ASD at 1.5x computed ASD; it says non-expiry-day intraday ASD does not apply.
- Position-limit enforcement, MWPL ban penalties, index-option expiry ASD, margin shortfall and TM-level PRISM utilization are separate controls.

### Requirements and test amendments

PX-025 now contains **101 normative requirements and 180 proposed acceptance scenarios**:
- R-089–R-101 cover effective-dated limit schedules, cross-member client aggregation, FutEq/delta, quarterly MWPL, 95/80 ban thresholds, Day 1 base positions, passive delta movement, current entity categories, random intraday snapshots, expiry-only ASD, rule-version scoping, data completeness and separation from margin/PRISM.
- AT-151–AT-180 cover stale parameters, cross-member position aggregation, missing delta, MWPL formula, quarterly changes, 95/80 thresholds, ban baselines, sign-change rules, passive changes, expiry roll-off, 2026 schedule, category limits, intraday snapshots, expiry ASD and independent margin/position-limit outcomes.

### Current-data limitations

The NCL/CMPT/76459 reference came from a secondary circular index; the official archive PDF and Annexure I security-level table were not inspected. Exact 2025/122 PDF thresholds were also not retrieved. NSE's 19 Nov 2025 position-limits page lists a 60% OI alert every 10 minutes, but whether the alert was migrated to FutEq is not established. The research records the effective circular references and refuses to substitute stale 2025 values. A live control must fail closed when its current effective limit/delta/ban data is unavailable.

No broker/member portal, broker/clearing endpoint, sandbox, order, code implementation, paid service, PR or merge to `main` was used.


## 21. Order admission, exposure classification and independent risk gates (2026-11-08)

PX-2026-033 synthesizes PX-024 through PX-032 and the ALG-ARCH-001 provenance baseline into a proposed order-admission policy.

### Core conclusion

Order admission is the conjunction of independent mandatory gates. Margin sufficiency does not override a position limit; position-limit headroom does not prove upfront collection; a broker acknowledgement does not prove exchange receipt or execution; and an unresolved command may already have created exposure.

The projected portfolio must include current positions, unique trades, working-order residuals, partial fills, sliced/compound children and unresolved submissions. “Sell”, “close” or “reduce-only” labels do not prove an action is risk-reducing; classify the projected exposure vector under the effective contract, delta, position-limit, margin and settlement rules.

### Proposed gate composition

PX-033 proposes 11 gates covering identity/contract eligibility, command recovery, projected exposure, MWPL ban, entity limits, index intraday controls, margin/collection, expiry/settlement, provider validation and evidence freshness. A gate-level FAIL or required UNKNOWN blocks risk-increasing admission. Advisory warnings remain separate from hard restrictions.

PLACE, OFFSET, MODIFY, CANCEL, REPLACE and compound/sliced actions have distinct state/evidence rules. Admission approval is time-bounded and must be revalidated before dispatch if relevant inputs change.

### Requirements and tests

PX-025 now contains **118 normative requirements and 220 proposed acceptance scenarios**:
- R-102–R-118 cover independent gates, projected exposure, action classification, fail-closed UNKNOWN, command lifecycle, ban reduction proof, cross-member aggregation, actual margin collection, hedge invalidation, expiry/settlement admission, child-order gates, provider validation, advisory vs hard block, immutable decision snapshots, per-gate trace, distinct dispatch/ack/execution evidence and non-bypassable regulatory restrictions.
- AT-181–AT-220 cover gate conjunction, position/margin independence, unknown data, reduction labels, working orders, lost acknowledgements, cancel/modify/replace races, ban reductions, cross-member data, stale basket approval, physical delivery, compound orders, broker acknowledgement vs execution, warnings vs hard limits and override attempts.

These scenarios are proposed for a future deterministic fake-provider/fake-clearing harness and have not been run.

No order engine code, broker integration, sandbox/production request, live order, paid service, PR or merge to `main` was used.


## 22. Exchange contract master, freeze limits and broker order validation (2026-11-08)

PX-2026-034 audits the effective NSE contract master and separate broker request schemas for Kite, Upstox V3 and DhanHQ v2.

### Findings

- Exchange contract identity must include exchange/segment, underlying/security, instrument ID/token, contract family, expiry, strike, option type, trading status and effective contract-master version. Symbol-only or token-only matching is insufficient.
- NSE current specification has distinct tick rules for index futures, index options, stock futures and stock options; exchange operating/dynamic price ranges are distinct from broker market protection.
- NSE Circular NSE/FAOP/74469 (29 May 2026) gives index freeze limits effective 1 June 2026 (BANKNIFTY 900, NIFTY 1800, FINNIFTY 1800, MIDCPNIFTY 2800, NIFTYNXT50 600) and directs members to load the dated `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` files. The actual 8 Nov 2026 daily file was not downloaded, so those figures are not treated as evergreen constants.
- Kite supports provider-specific varieties/products/validity/market protection/autoslice fields; Upstox V3 has its own enums, DAY/IOC, session-inferred AMO, slicing and market-protection constraints; Dhan v2 has its own product/order/AMO fields and separate slicing endpoint. Do not normalize provider enums by silent coercion.
- Upstox documentation describes F&O/equity units and commodity lots but also says units are multiples of tick size; the wording is dimensionally inconsistent. Use the effective exchange lot/quantity file and do not treat price tick as a quantity conversion factor.
- Dhan's reviewed slicing endpoint does not publish a complete response schema; child-set recovery remains UNKNOWN until verified.

### Requirements and tests

PX-025 now contains **132 normative requirements and 250 proposed acceptance scenarios**:
- R-119–R-132 cover effective-dated contract data, derivative identity, quantity unit/lot conversions, exact tick validation, daily freeze quantity, exchange price range vs broker protection, versioned broker enums, conditional fields, AMO/session semantics, explicit slicing, child completeness, contract lifecycle invalidation, rejection evidence and fresh validation before dispatch.
- AT-221–AT-250 cover missing/stale contract file, identity mismatch, expiry/suspension, market lot, double conversion, product tick differences, dynamic price ranges, freeze edge conditions, malformed files, Kite/Upstox market protection, Dhan unsupported fields, Upstox lot units, provider enums, AMO, validity mapping, slicing, stale admission and unknown provider rejection codes.

The current daily contract master and provider schema gaps remain explicit; no parser, adapter or test implementation was performed.

No broker/exchange API, account, sandbox, production order, code change, paid service, PR or merge to `main` was used.


## 23. NSE contract-file ingestion, schema variants and integrity (2026-11-08)

PX-2026-035 audits NSE MII contract-file variants, dated FO contract CSVs, separate quantity-freeze/market-lot report chronology and Admission Type mappings.

### Findings

- NSE uses multiple contract-data variants, including NSE-exclusive MII contract files and NSE/BSE interoperability-related variants. They must remain separately scoped.
- NSE/FAOP/74469 (29 May 2026) directs members to load updated `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` files for revised index freeze limits effective 1 June 2026.
- The 2024 circular history records discontinuation of separate quantity-freeze/market-lot report distribution where the MII file contains the data, followed by a later circular re-announcing `Qtyfreeze.csv` and `fo_mktlots.csv` from 9 December 2024 EOD. The current source/report precedence must be verified at integration time.
- NSE/FAOP/73629 (April 2026) identifies Admission Type in different positions: field 13 for `contract.gz` and field 30 for the dated FO CSV. Field offsets must not be reused between schema variants; BSE-exclusive routing/admission remains a first-class eligibility check.
- Publication time, download time and effective time are separate. Raw bytes, hashes, source circular, parser version, row-level provenance, schema and completeness must be retained.
- The 8 November 2026 daily files and complete current field schemas were not retrieved or inspected; no parser was implemented or claimed as validated.

### Requirements and acceptance tests

PX-025 now contains **147 normative requirements and 280 proposed acceptance scenarios**:
- R-133–R-147 cover file variant, publication/effective time, schema profile, immutable raw artifacts, gzip completeness, unique contract keys, variant scope, Admission Type mapping, lot/unit/freeze distinctions, auxiliary report lifecycle, atomic promotion, cross-file conflict, status/expiry, venue routing and auditable invalidation.
- AT-251–AT-280 cover contract variants, field mappings, unknown Admission Type, route mismatch, duplicate keys, future-effective files, gzip truncation/hash change, missing artifacts, malformed identity, expired rows, stale/partial data, standalone freeze/lot report chronology, freeze discrepancies, parser upgrades, schema shifts, unknown enums and revalidation after correction.

All are proposed tests; no file parser or exchange integration was run.

No exchange/member portal access, broker/API call, sandbox, order, code change, paid service, PR or merge to `main` was used.


## 24. Cross-provider instrument identity and effective-dated contract mapping (2026-11-08)

PX-2026-036 separates immutable canonical underlying/contract identity from Kite, Upstox and Dhan provider aliases.

### Official provider-master findings

- **Kite:** daily gzipped CSV. The `last_price` field is not real-time. Kite expressly warns instrument tokens may be reused for different derivative instruments after expiry and recommends exchange + tradingsymbol rather than numeric token as the storage key.
- **Upstox:** current JSON BOD files are recommended over deprecated CSV. The docs identify `instrument_key` as unique, warn `exchange_token` can be reused after expiry, and publish separate suspended, MTF, MIS, mutual-fund and global instrument datasets. The daily refresh is around 6 AM with possible intraday refreshes; next-day BOD omits expired/delisted instruments.
- **Dhan:** publishes compact and detailed CSV scrip masters plus a segmentwise instrument endpoint. Detailed rows expose exchange/segment, ISIN, underlying security ID/symbol, series, lot, expiry, strike, option type, tick and additional eligibility flags. A global all-time uniqueness guarantee for the raw Dhan securityId was not established.

### Canonical mapping rule

Use immutable canonical identity for the economic underlying/contract, then map provider-scoped aliases with provider/API/schema, exchange segment and effective interval. Complete matching requires underlying identity, venue/segment, contract family, expiry, exact strike, option type and relevant contract attributes. No fuzzy symbol match or cross-provider token equality may authorize an order.

Daily provider files for 8 November 2026 were not downloaded or parsed; no row-level crosswalk was built.

### Requirements and tests

PX-025 now contains **162 normative requirements and 310 proposed acceptance scenarios**:
- R-148–R-162 cover canonical identity versus aliases, provider namespace, effective validity, authoritative underlying identity, complete contract terms, exact normalization, unique exact match, attribute cross-checking, separate provider-master versioning, venue route, corporate-action successor links, historical-only expired aliases, collision quarantine, atomic crosswalk and fail-closed UNKNOWN.
- AT-281–AT-310 cover token namespace, current/next expiry, strike/option type, ISIN/index handling, unmatched rows, lot/tick/unit conflicts, float/timezone errors, alias collisions and transitions, expired aliases, corporate actions, venue, provider schema, stale masters and incomplete promotion.

No provider file download, API call, parser, code change or order was performed.

## 25. Market-data identity, timestamp semantics, freshness and historical continuity (2026-11-08)

PX-2026-037 audits provider market-feed timestamps, session state, disconnect/reconnect semantics and historical candle continuity.

### Official feed findings

- **Kite:** REST quote `timestamp` is the exchange timestamp of the quote packet; `last_trade_time` is separate. WebSocket full quote packets include last-trade timestamp and exchange timestamp; index packets have a distinct shorter schema. Kite's continuous-history feature covers daily candles for expired NFO/MCX futures, not general intraday expired-contract history.
- **Upstox V3:** the first feed message is `market_info` with per-segment status and `currentTs`; the second is a market snapshot; subsequent updates are live feed. Per-instrument `ltpc.ltt` is last-trade time; `currentTs` is described as timestamp of the received tick, not exchange timestamp.
- **DhanHQ v2:** binary tick/quote/full packets carry LTT epoch time and market values; the reviewed packet schemas do not expose a separate exchange quote-update timestamp. Dhan sends ping every 10 seconds, closes after more than 40 seconds without pong, and provides a disconnect reason code.
- **Historical:** Kite's continuous option supports daily expired-futures candles; Dhan daily history is back to inception, intraday intervals 1/5/15/25/60 minutes for up to five years, and each intraday request is limited to 90 days.

### Core design decisions

Keep exchange event time, last-trade time, provider message time, local receive time, persistence time and candle bucket/session time separate. Trade freshness does not prove quote/depth freshness; ping/pong does not prove data completeness. Reconnect snapshot or historical bar backfill cannot recreate missing tick/depth events. Never synthesize missing bars or merge conflicting providers using last-arrival-wins.

### Requirements and tests

PX-025 now contains **177 normative requirements and 340 proposed acceptance scenarios**:
- R-163–R-177 cover distinct timestamp semantics, raw timestamp units, freshness by data component, local monotonic timing, provider schema semantics, canonical identity linkage, packet variants, session evidence, liveness vs completeness, explicit gaps, reconnect/backfill limits, use-case freshness, historical candle identity, continuous-series lineage and missing/source-conflict handling.
- AT-311–AT-340 cover Kite/Upstox/Dhan timestamps, packet schemas, market status, LTT-vs-currentTs, transport timeout, stale/no-trade distinctions, clock skew, timestamp units, reconnect gaps, historical backfill, Kite continuous daily scope, Dhan 90-day range and date inclusivity, candle source differences, roll lineage, holidays and cross-provider conflicts.

No live feed, historical API, broker account, code or order was used.

## 26. Historical data coverage, expired contracts and backtest provenance (2026-11-08)

PX-2026-038 compares historical candle and expired-contract coverage for Kite, Upstox and Dhan.

### Key findings

- **Kite:** standard historical candles include minute through daily intervals and optional OI. `continuous=1` applies to expired NFO/MCX futures **daily candles** only; expired contract tokens are not in the live master unless cached.
- **Upstox V3:** historical intervals include minutes 1–300, hours 1–5, day/week/month; minute/hour data is documented from Jan 2022, day/week/month from Jan 2000, with unit-specific maximum retrieval windows. Separate expired-instrument APIs list expired options/futures and retrieve exact expired-contract candles at 1m/3m/5m/15m/30m/day.
- **Dhan:** daily history is documented from instrument inception; active-instrument intraday 1/5/15/25/60m covers the last five years, maximum 90 days per call. Its expired-options API is rolling ATM-relative (up to five years, 30 days per call and bounded ATM±strike coverage), not a full fixed-strike archive.
- Provider date semantics differ: Upstox ranges are inclusive; Dhan's documented toDate is non-inclusive; Kite uses timestamp parameters.
- Preserve exact contract history, rolling moneyness history and continuous futures as distinct data coverage classes. Raw bars remain immutable; corporate-action-adjusted/continuous series are derived views with lineage.
- OHLC-only data cannot prove exact intrabar fills, queue position or order-book path. Backtests must state data resolution/fill model and enforce no-lookahead.

### Requirements and acceptance tests

PX-025 now contains **192 normative requirements and 370 proposed acceptance scenarios**:
- R-178–R-192 cover coverage classification, query date/range semantics, exact expired contract coverage, Upstox expired key resolution, Dhan rolling-moneyness limitation, Kite continuous scope, immutable retrieval manifests, candle boundary/finalization, nullable OI/IV/spot, explicit adjustment lineage, continuous futures construction, no fixed-contract inference from rolling data, chunk completeness, OHLC execution limits and as-of/no-lookahead replay.
- AT-341–AT-370 cover provider query windows, expired-contract data scope, Dhan ATM shifts/ranges, date inclusivity, missing OI, reversed/duplicate/gapped candles, corporate-action adjustment, roll lineage, lookahead and dataset revision reproducibility.

No historical API call, market data collection or backtest was executed.

## 27. Market-data rights, retention and distribution controls (2026-11-08)

PX-2026-039 reviews NSE data policy, public Kite Connect API terms, Upstox website/app terms and Dhan Data API subscription documentation.

### Findings

- **NSE Data policy:** subscriber Relevant Agreements define intended use, handling and dissemination. Ownership remains with NSE/NSE Data; redistribution is only as agreed. Custom/composite financial indices and financial instruments require separate licensing; offline removable media requires prior approval. Non-commercial research still requires documented restrictions and confidentiality.
- **Kite Connect:** public terms prohibit public display of live data, virtual/mock trading uses and redistribution. API content may not be permanently copied/cached with intent to redistribute. Kite requires usage trails/books/records/logs for at least five years or as required by law; this is not a five-year raw-data archive licence.
- **Upstox:** public website/app Terms of Use describe content ownership and restrict commercial/public use of website materials without consent. This is not treated as a complete API-feed licence; API account terms remain UNKNOWN.
- **Dhan:** public support docs show a separately subscribed Data API (₹499 plus taxes/month, auto-debited every 30 days); subscription confirms access mechanism, not redistribution/archive/commercial rights. Specific Data API terms remain UNKNOWN.
- Website/app terms are not generalized to separately licensed broker APIs, and a paid/free API credential does not grant rights by implication.
- SEBI retail API algo compliance is a separate deployment gate from data licensing.

### Requirements and tests

PX-025 now contains **205 normative requirements and 395 proposed acceptance scenarios**:
- R-193–R-205 cover source rights manifest, no inferred downstream rights, purpose-specific use, display/redistribution, storage vs archive, audit log vs data retention, derived-data lineage, separate exchange/broker/website terms, index licensing, non-commercial research terms, termination/deletion, tenant/credential protection and separate algo regulation gate.
- AT-371–AT-395 cover unknown agreements, Kite public display/mock trading/cache, five-year audit logs vs data archive, NSE licence/redistribution/offline media/research, Upstox API rights uncertainty, Dhan subscription vs downstream display, backtest storage, derived analytics, data termination, backups, public GitHub, tenant isolation, permitted end-user limits and separate SEBI algo deployment compliance.

No licence was accepted, no subscription purchased, no feed connected and no data payload downloaded.

### Open rights items

Before customer-facing display, archive, redistribution or commercial deployment, obtain the current signed terms for each broker/API account and any required exchange/data-vendor licence. The public Upstox and Dhan material reviewed here does not fully settle API-feed rights. UNKNOWN is not permission.
