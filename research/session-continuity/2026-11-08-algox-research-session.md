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
