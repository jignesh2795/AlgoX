# PX-2023-031 — vectorbt

## Historical role
vectorbt is a Python quantitative-analysis/backtesting framework built around vectorized numerical computation. It is an important 2023 reference because it demonstrates a different scaling strategy from event-by-event trading engines: represent large numbers of strategy configurations and historical computations as array operations.

## Architecture observations
- Research throughput can be increased by vectorized computation rather than increasing agent/model complexity.
- Parameter sweeps and large experiment spaces benefit from array-oriented representations.
- Vectorized backtesting is powerful for research but does not automatically reproduce every event-driven execution behavior.

## AlgoX extraction
**Capability:** high-throughput research/backtest experimentation.

**Lesson:** AlgoX should maintain separate benchmarks for research throughput and execution fidelity. A fast vectorized simulation and a realistic event-driven simulator solve different problems.

## Decision
ASSESS — benchmark against event-driven backtesting systems before selecting it for any capability.

## Evidence maturity
C1 — project architecture; reproduction and benchmark pending.
