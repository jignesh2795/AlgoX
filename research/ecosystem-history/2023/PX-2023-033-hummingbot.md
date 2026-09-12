# PX-2023-033 — Hummingbot

## Historical role
Hummingbot entered 2023 as a mature open-source trading framework rather than a new AI project. Its 2023 roadmap described a transition from a bot toward a framework, with dozens of exchange connectors, multiple strategies, reusable scripts and support for external modules. The 2023 retrospective records connector standardization, market-order support, gateway separation and a scripts framework. citeturn1search3turn1search6

## Architecture observations
- Exchange connectivity is isolated behind connectors.
- Strategy logic is separated from exchange-specific APIs.
- Gateway/connector boundaries can be independently evolved.
- Community-built external modules become part of the architecture, creating extension and compatibility requirements.

## AlgoX extraction
**Capability:** exchange/broker connector abstraction.

**Lesson:** connector boundaries are foundational to trading-system portability. The canonical internal order/data model must not inherit every exchange's quirks directly.

## Decision
ADOPT as a reference architecture for connector boundaries; benchmark individual design choices before reuse.

## Evidence maturity
C2 — official 2023 roadmap and retrospective; no AlgoX reproduction yet.
