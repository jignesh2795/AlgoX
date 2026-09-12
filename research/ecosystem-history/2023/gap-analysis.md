# 2023 Capability Gap Analysis

Status: PROVISIONAL

## Purpose

Identify capabilities that the 2023 ecosystem demonstrated well, partially demonstrated, or left insufficiently evidenced for the future AlgoX / target trading-platform architecture.

| Capability | 2023 evidence | Confidence | Gap |
|---|---|---|---|
| Model/provider abstraction | LLaMA, inference/serving ecosystem | High | Need policy-driven model selection |
| Tool execution | agent frameworks | High | Need sandboxing and approval |
| Agent memory | MemGPT, agent research | High | Need temporal/provenance governance |
| Retrieval | vector databases/RAG ecosystem | High | Need evidence-aware retrieval |
| Agent evaluation | WebArena, AgentBench, SWE-bench | High | Need domain-specific evaluation |
| Coding-agent workflow | Aider, GPT Engineer, SWE research | High | Need institutional code-change traceability |
| Financial research pipeline | Qlib, FinRL, vectorbt | High | Need unified evidence model |
| Backtesting | Freqtrade, LEAN, vectorbt | High | Need explicit fidelity metrics |
| Live/backtest continuity | LEAN and event-driven systems | Medium-High | Need quantified parity validation |
| Broker abstraction | CCXT and broker APIs | High | Need canonical contract + escape hatch |
| Order reconciliation | broker event/state patterns | Medium-High | Needs formal invariant suite |
| Market-data normalization | financial projects/broker APIs | High | Need canonical identity + provenance |
| Indian market semantics | broker/exchange evidence | Medium | Requires broader broker/exchange coverage |
| Corporate actions | financial-data ecosystem | Medium | Needs first-class temporal treatment |
| Fees/taxes/slippage | trading platforms | Medium | Needs India-specific cost model |
| Production reliability | selected mature systems | Medium | Need recovery/chaos benchmarks |
| Security boundaries | agent/code-execution systems | Medium | Need formal threat model |
| Knowledge governance | fragmented across projects | Low | Major AlgoX research gap |
| Temporal institutional memory | emerging research | Medium | Need durable implementation |
| Cross-project capability comparison | fragmented | Low | Major AlgoX differentiator |
| Decision provenance | fragmented | Low | Major AlgoX differentiator |

## Highest-priority gaps

### G1 — Evidence-backed institutional knowledge

Most systems optimize retrieval or execution, not preservation of why a technical decision was made.

### G2 — Temporal knowledge

Financial APIs, exchange rules, project versions, model capabilities, and claims change over time. Current truth and historical truth must be distinguishable.

### G3 — Reconciliation correctness

Execution systems require formal handling of partial fills, duplicate events, reconnects, rejected commands, and state drift.

### G4 — Research/live parity measurement

Shared abstractions are useful, but AlgoX needs experiments that quantify where simulation diverges from live behavior.

### G5 — Indian-market capability depth

The 2023 research identifies the architecture categories but does not yet provide enough independent evidence across Indian exchanges, brokers, data providers, product types, fees, corporate actions, and regulatory constraints.

### G6 — Agent engineering evaluation

General agent benchmarks are insufficient for finance. AlgoX needs task-specific evaluation around research correctness, evidence citation, code changes, data analysis, trading-system design, and operational safety.

## Gap prioritization

Priority should be determined by:

`Potential Value × Relevance × Evidence Potential × Reuse Potential / Research Cost`

The gaps above should not automatically become implementation tasks. They are research targets until sufficient evidence exists.
