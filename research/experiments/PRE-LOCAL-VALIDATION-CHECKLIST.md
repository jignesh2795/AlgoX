# AlgoX Pre-Local-Validation Checklist

## Purpose

Track everything that can be completed before the local execution session. Runtime measurements remain deliberately unclaimed until executed locally.

## P0

- [x] EXP-ALG-001 persistence adapter implemented
- [x] EXP-ALG-001 benchmark harness implemented
- [x] EXP-ALG-001 restart/provenance/temporal tests implemented
- [x] EXP-ALG-002 retrieval design and benchmark fixtures present
- [x] EXP-ALG-003 memory-ablation design present
- [x] EXP-ALG-004 consolidation, governance and audit path implemented
- [x] EXP-ALG-004 failure/approval fixtures documented
- [x] EXP-ALG-005 research-agent reliability fixture design present
- [ ] Run full pytest suite locally
- [ ] Run persistence benchmark locally
- [ ] Record actual measurements
- [ ] Decide persistence boundary from measurements

## P1

- [x] EXP-ALG-008 temporal/contradiction architecture present
- [x] EXP-ALG-009 decision-chain reconstruction implementation present
- [x] EXP-ALG-010 Indian execution capability research present
- [ ] Build deterministic Indian execution fixture suite
- [ ] Build reproducible experiment replay harness
- [ ] Benchmark single-agent vs multi-agent execution

## Rules

1. A test file is not experimental evidence until executed.
2. A benchmark implementation is not a benchmark result until executed.
3. A literature claim is not a local capability decision unless the evidence maturity is recorded.
4. Do not introduce PostgreSQL, a dedicated graph database, a vector database or Redis before the relevant workload gate.
5. Do not turn AlgoX into an OMS/EMS; downstream execution capabilities remain research targets for QuantumTrade.
6. Preserve failed and contradictory results; they are evidence, not noise.
