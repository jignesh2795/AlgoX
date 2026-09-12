# PX-2023-081 — Event-driven financial data infrastructure

## Status
Discovery lead; historical year requires verification before 2023 classification.

## Finding
Event-driven market-data infrastructure should be evaluated separately from trading strategy code. Important capabilities include canonical instrument identity, normalized event envelopes, timestamps, replay, storage, schema evolution, and downstream analytics.

## AlgoX relevance
This capability family is directly relevant to the market-data and evidence boundaries of future trading systems. It should not be collapsed into a broker adapter or strategy engine.

## Evidence rule
The currently observed `fincore` repository is useful as an architectural reference, but current repository state alone does not establish 2023 historical relevance. It therefore remains a discovery lead rather than confirmed 2023 evidence.

## Decision
ASSESS — historical provenance first; architecture extraction second.
