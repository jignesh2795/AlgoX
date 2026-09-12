# PX-2023-083 — Execution simulation gap

## Finding
Traditional backtesting often compresses execution into a final PnL result. Execution-aware research requires explicit order lifecycle, latency, queue position, liquidity, partial fills, cancellations, and venue-specific assumptions.

## Historical status
Execution-simulation projects found in the current ecosystem are useful discovery leads, but current repositories must not be backdated into 2023 without release/commit evidence.

## Capability taxonomy
- order intent
- order lifecycle
- market replay
- latency model
- fill model
- queue-position model
- partial-fill model
- cancellation model
- execution-cost model
- reproducible replay

## AlgoX relevance
High. This should become a dedicated benchmark family for future trading-system research.

## Decision
ADOPT capability requirement; RESEARCH historical implementations before assigning a 2023 project record.
