# 2023 Discovery Gap Audit — v1

## Status
Provisional. This is a gap audit, not a final synthesis.

## Strongly covered
- Agent frameworks and agent evaluation
- LLM application/retrieval infrastructure
- Model/inference infrastructure
- AI coding/development systems
- Major quantitative research/trading frameworks
- Broker/API abstractions
- Indian-market data and broker discovery
- Execution/reconciliation architecture

## Capability gaps still requiring targeted evidence
1. Corporate actions and historical price adjustment
2. Canonical instrument/security-master design
3. Indian F&O contract lifecycle and expiry handling
4. Margin and buying-power semantics
5. Historical brokerage/tax/transaction-cost modeling
6. Fill simulation and partial-fill semantics
7. Market-data replay and deterministic execution tests
8. Tick/order-book storage and replay
9. Failure/recovery behavior under broker disconnects
10. Position/order reconciliation across multiple event sources

## Temporal caution
Current projects may expose these capabilities today, but that does not establish that the capability existed in the same form in 2023. AlgoX must preserve the distinction between:
- capability observed in 2023;
- capability reconstructed from later evolution;
- capability inferred from older documentation/code;
- current discovery lead with no historical classification.

## Current research conclusion
The 2023 research is mature enough to expose architectural boundaries, but not yet mature enough to freeze the final 2023 thesis. The remaining work should concentrate on evidence quality and missing capabilities rather than adding repositories indiscriminately.

## Proposed next gate
Before final synthesis, every high-value capability should have at least one dated source and preferably a code/test or reproducible experiment. Contradictions should be recorded explicitly rather than averaged away.
