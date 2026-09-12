# PX-2023-079 — Data Correctness and Reconciliation as First-Class Capabilities

## Classification
- Year: 2023 evidence window
- Domain: Financial data / execution infrastructure
- Type: cross-project architectural finding
- Status: provisional finding

## Finding
The 2023 ecosystem evidence reinforces that market-data acquisition, reference-data identity, execution state and reconciliation should not be collapsed into a single broker or strategy abstraction.

NautilusTrader's March 2023 release explicitly included execution reconciliation comparisons and backtest/live execution behavior. Indian-market projects active in 2023 concentrated heavily on acquiring NSE data, historical prices, indices and bhavcopy information. These are different correctness problems.

## Separation of concerns
1. Raw market-data acquisition
2. Normalization and timestamp semantics
3. Instrument/security identity
4. Historical data storage
5. Strategy data consumption
6. Order intent
7. Broker/exchange acknowledgement
8. Fill and position state
9. Reconciliation

## Why this matters
A system can have correct strategy logic while producing incorrect trading results because of stale instruments, missing corporate actions, duplicated ticks, incorrect order-state transitions, incomplete fills or divergence between broker state and internal state.

## Evidence
- NautilusTrader v1.171.0 (30 March 2023) references reconciliation comparisons in its execution engine and fixes around cache persistence and order-event publishing.
- 2023 Indian-market repositories demonstrate separate data acquisition tooling for NSE data, historical prices and exchange reports.

## AlgoX decision implication
Future trading-system architecture should model reconciliation and data correctness as capabilities in their own right. They should not be treated as incidental implementation details of a broker adapter.

## Confidence
High for the architectural distinction; medium for the strength of production evidence because many 2023 open-source Indian projects were small research utilities rather than institutional systems.