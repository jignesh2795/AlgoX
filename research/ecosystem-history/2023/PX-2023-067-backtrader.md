# PX-2023-067 — Backtrader

## Classification
- Year: 2023
- Domain: backtesting / trading framework
- Research status: discovery record
- Evidence maturity: C1

## Historical relevance
Backtrader is an influential Python trading/backtesting framework whose architecture provides a useful historical baseline for strategy objects, data feeds, indicators, analyzers and broker simulation.

## Capability extraction
- strategy/data-feed separation
- indicator composition
- broker simulation
- analyzers
- event-driven backtesting
- extensible strategy APIs

## AlgoX relevance
Important comparison point for understanding how older backtesting architectures differ from newer event-driven production engines. Research should explicitly test where simulation abstractions diverge from real venue behavior.

## Decision
ASSESS — retain as historical architecture evidence and benchmark candidate.
