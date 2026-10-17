# AlgoX Capability Matrix v1

## Purpose

Convert the 2023-2025 ecosystem research into actionable capability decisions. A project is evidence; a capability is the reusable unit. Decisions remain provisional until supported by experiments and governance.

## Decision vocabulary

- **ADOPT** — use the demonstrated concept with minimal conceptual change.
- **ADAPT** — reuse the capability but modify it for AlgoX/Indian-finance constraints.
- **WRAP** — isolate an external implementation behind a stable interface.
- **BUILD** — implement the capability ourselves because provenance, control, integration, or domain requirements make direct reuse unsuitable.
- **HOLD** — valuable but premature; defer until a concrete requirement or benchmark justifies it.
- **REJECT** — evidence does not justify inclusion or risk/cost is unacceptable.

## Matrix

| Capability | Evidence direction | Maturity target | AlgoX decision | Experiment / gate | Destination |
|---|---|---:|---|---|---|
| Source provenance | GitHub/papers/regulatory/engineering evidence | M5 | ADOPT | provenance validation | AlgoX core |
| Evidence records | Research-memory architecture + evidence chain | M5 | ADOPT | schema + chain validation | AlgoX core |
| Temporal validity | temporal-memory research + historical source lifecycle | M4 | ADAPT | temporal contradiction tests | AlgoX core |
| Knowledge graph | graph projection + research-chain work | M4 | ADOPT | invariant/rebuild tests | AlgoX core |
| Semantic retrieval | RAG/vector ecosystem | M3 | ADAPT | retrieval benchmark | AlgoX retrieval |
| Dedicated vector DB | ecosystem evidence | M2 | HOLD | scale benchmark first | Later |
| Dedicated graph DB | ecosystem evidence | M2 | HOLD | graph workload benchmark first | Later |
| Agent traces | coding/research-agent systems | M4 | ADOPT | trace completeness | AlgoX core |
| Experiment registry | quant + research-agent systems | M4 | ADOPT | reproducibility test | AlgoX core |
| Benchmark registry | finance/agent benchmarks | M4 | ADOPT | metric/provenance audit | AlgoX core |
| Knowledge governance | evidence-governed memory | M4 | ADOPT | approval/audit tests | AlgoX core |
| Consolidation learning loop | 2025 research-agent/memory evidence | M3 | ADAPT | accepted-proposal audit | AlgoX core |
| Autonomous research loop | 2025 R&D-agent evidence | M3 | ADAPT | sandbox + reproducibility gate | AlgoX research engine |
| Multi-agent orchestration | AutoGen/LangGraph/financial agents | M3 | ADAPT | compare single vs multi-agent | AlgoX research engine |
| Agent-computer interface | OpenHands/SWE-agent direction | M3 | ADAPT | action/recovery benchmark | AlgoX execution layer |
| Sandboxed execution | coding-agent ecosystem | M3 | ADOPT | isolation/recovery test | AlgoX execution layer |
| Financial research agent | FinRobot/financial-agent ecosystem | M3 | ADAPT | finance benchmark | AlgoX finance research |
| Trading agent | trading-agent benchmarks | M2 | HOLD | out-of-sample/risk gate | Future systems |
| Autonomous production trading | benchmark evidence remains insufficient | M0-M1 | REJECT | requires separate safety case | Not AlgoX |
| Event-driven market data | LEAN/Nautilus/Indian broker ecosystem | M4 | ADOPT | deterministic event tests | Future trading platform |
| Execution state machine | LEAN/Nautilus/Indian broker evidence | M4 | ADOPT | partial-fill/recovery tests | Future trading platform |
| Execution reconciliation | Nautilus/financial execution evidence | M4 | ADOPT | disconnect/replay tests | Future trading platform |
| Canonical instrument identity | Indian broker/data evidence | M3 | ADAPT | cross-provider identity tests | Future trading platform |
| F&O contract lifecycle | Indian market evidence + LEAN/Nautilus | M3 | ADAPT | expiry/roll/assignment tests | Future trading platform |
| Corporate-action correctness | financial data ecosystem | M2 | ADAPT | raw/adjusted reconciliation | Future trading platform |
| Realistic fill simulation | quant/trading ecosystem | M2 | BUILD | market replay benchmark | Future trading platform |
| Deterministic tick/order-book replay | event-driven trading ecosystem | M2 | BUILD | replay determinism benchmark | Future trading platform |
| Broker abstraction | Indian broker APIs + trading engines | M3 | ADAPT | contract conformance suite | Future trading platform |
| Broker recovery/idempotency | execution/reconciliation evidence | M2 | BUILD | failure-injection tests | Future trading platform |
| Indian cost/margin model | broker/exchange evidence | M2 | ADAPT | historical charge/margin fixtures | Future trading platform |
| PostgreSQL persistence | architecture assessment | M2 | ADOPT FIRST | persistence benchmark | AlgoX core |
| Object storage | research artifact requirements | M2 | ADOPT | artifact integrity test | AlgoX core |
| Redis | generic infrastructure | M1 | HOLD | measured latency/use case | Later |
| Search engine | generic infrastructure | M1 | HOLD | scale benchmark | Later |

## Guardrails

1. Popularity is discovery evidence, never quality evidence.
2. Current implementation must not be backdated into historical evidence.
3. A model proposal is not institutional truth.
4. A benchmark result is not production readiness.
5. A capability does not become durable memory without provenance and governance.
6. Reusable external code requires license/provenance review.
7. Financial capabilities require market-specific validation, especially for India.
8. Infrastructure choices must be justified by workload measurements rather than fashion.

## Immediate implementation order

1. Finish AlgoX research/evidence interfaces.
2. Integrate accepted consolidation proposals with governance and audit.
3. Establish reproducible local experiment/benchmark execution.
4. Add capability-level evidence and decision records.
5. Build PostgreSQL persistence only after the persistence benchmark/gate.
6. Keep trading-platform implementation downstream of AlgoX decisions.

## Status

This is a decision projection of the 2023-2025 research, not final truth. Decisions can be superseded by stronger evidence, experiments, or requirements.
