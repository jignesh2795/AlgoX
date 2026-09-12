# PX-2023-062 — FinMem

## Classification
- Year: 2023
- Domain: Financial AI / LLM agents / trading research
- Type: Research implementation
- Primary capability: layered financial memory + LLM decision agent
- Evidence status: C1 — primary repository/paper inspected
- AlgoX status: RESEARCHED — reproduction required

## Historical significance
FinMem, published in 2023, is an early financial LLM trading-agent implementation explicitly centered on layered memory. It separates profiling, memory processing and decision-making, making it especially relevant to AlgoX's later memory architecture.

## Architecture
```text
Market / external information
        ↓
Layered memory
(short / medium / long-term style processing)
        ↓
Agent profile / character
        ↓
Decision-making
        ↓
Investment action
```

## Key extraction
**Capability:** structured, layered memory for an LLM financial agent.

**Important distinction:** memory is treated as an active processing layer rather than merely a vector retrieval store.

## AlgoX relevance
Very high. This is direct historical evidence supporting the direction AlgoX later reached independently: memory should have explicit types, lifecycle and consolidation semantics.

However, FinMem's trading results must not be interpreted as evidence that LLM agents are production-safe trading authorities. The experimental environment, assumptions, costs, execution model and data regime require independent validation.

## Validation questions
- Does layered memory improve out-of-sample decision quality versus equivalent no-memory baselines?
- Which memory layer contributes the improvement?
- Does memory create stale-information or confirmation-bias failure modes?
- How does performance change under regime shifts?
- Are transaction costs, slippage and execution constraints realistic?

## Decision
**ADAPT** the layered-memory concept for AlgoX's research brain. Keep financial execution behind deterministic policy, risk and reconciliation boundaries.

## Primary evidence
- FinMem GitHub: https://github.com/pipiku915/FinMem-LLM-StockTrading
- Paper: arXiv:2311.13743

## Notes
Reported trading performance is research evidence only. Production readiness is unverified.
