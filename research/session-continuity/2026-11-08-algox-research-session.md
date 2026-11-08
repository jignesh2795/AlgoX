# AlgoX research session continuity — 2026-11-08

**Record type:** session continuity / research-state consolidation  
**Research branch:** `research/px-2026-022-indian-fill-realism-2026-11-08`  
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
- The present continuation branch is `research/px-2026-022-indian-fill-realism-2026-11-08`.
- This branch contains PX-2026-022 and this continuity record. It is intentionally not merged.
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
