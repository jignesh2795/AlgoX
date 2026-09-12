# 2024 Contradiction Analysis

## Status
PROVISIONAL — historical synthesis gate.

## Purpose
This document tests whether the 2024 findings can be treated as durable architecture lessons rather than conclusions produced by project popularity or current documentation.

## Contradiction matrix

| Topic | Evidence A | Evidence B / counterpoint | AlgoX resolution |
|---|---|---|---|
| End-to-end frameworks | Qlib, LEAN and FinRL expose broad workflows | Broad workflow does not imply equal maturity of research, simulation, execution and production capabilities | QUALIFY: evaluate capabilities independently |
| Agent autonomy | Coding-agent systems increased tool/environment access | More autonomy increases the need for permissions, tests, sandboxing and verification | VALIDATED: controlled autonomy |
| Retrieval | RAG systems make retrieval a reusable subsystem | Retrieval relevance does not establish truth, provenance or temporal validity | VALIDATED: evidence system > RAG |
| Vector storage | Vector search is useful for semantic candidate generation | Semantic similarity cannot represent authoritative truth, contradiction or temporal state by itself | REJECT: vector DB as institutional memory |
| Research/live parity | Shared abstractions reduce divergence | Live systems contain venue, transport, timing, persistence and reconciliation behavior absent from ordinary backtests | QUALIFIED: share semantics where possible, not assumptions |
| Provider abstraction | Common interfaces reduce coupling | Over-normalization can erase broker/exchange-specific semantics | QUALIFIED: stable canonical contract + explicit venue escape hatch |
| Data quality | Market-data systems emphasize accuracy, completeness, timeliness and lineage | Quality rules are domain-specific and may require human review | VALIDATED: data quality is a first-class capability |
| Operational resilience | Trading venues and regulators emphasize monitoring, shutdown and continuity | Resilience claims are not equivalent to independently demonstrated recovery | VALIDATED: require failure/recovery evidence |
| AI in execution | AI can assist research and development | Evidence does not establish that an unconstrained AI agent should control irreversible execution | REJECT for direct autonomous execution without strong safety evidence |
| Popularity | Widely used projects provide useful evidence | Popularity is not proof of correctness, production maturity or suitability | REJECT as quality proxy |

## Major contradiction
A recurring apparent contradiction is that one framework may support research, backtesting and live trading while the individual capabilities have very different evidence maturity.

Therefore AlgoX must preserve capability-level evaluation.

```text
Project
  ├── research
  ├── simulation
  ├── execution
  ├── reliability
  ├── reproducibility
  └── governance
```

A project-level score must not collapse these dimensions.

## Temporal qualification
Some evidence available today describes systems that evolved after 2024. Such evidence may validate a principle but must not automatically be backdated as proof of 2024 implementation behavior.

AlgoX therefore distinguishes:

- historical evidence — directly attributable to the period;
- retrospective evidence — later evidence that evaluates an earlier design;
- current evidence — useful for architecture but not historical proof.

## Reliability contradiction
Operational resilience requirements are stronger than ordinary software correctness. A system can produce correct outputs under normal conditions and still fail dangerously during:

- broker disconnects;
- stale market data;
- duplicate events;
- out-of-order events;
- process restart;
- partial fills;
- database failure;
- network partition;
- exchange halt;
- manual intervention;
- corrupted state.

This means unit-test coverage or backtest accuracy cannot be used as substitutes for recovery evidence.

## Resolution
The 2024 evidence supports the following high-confidence principles:

1. Data provenance and quality are part of trading correctness.
2. Research, decision and execution capabilities should remain separable.
3. Simulation and live execution share useful semantics but not identical operational behavior.
4. Reconciliation is a runtime capability, not merely maintenance tooling.
5. Operational resilience requires explicit failure and recovery testing.
6. AI should be bounded by deterministic policy and verification at irreversible boundaries.
7. Institutional knowledge must preserve evidence, time and contradiction state.

## Remaining uncertainty
The following remain insufficiently evidenced for unconditional adoption:

- superiority of any particular event bus;
- superiority of microservices over a modular monolith for AlgoX's eventual target systems;
- necessity of a dedicated graph database;
- superiority of a particular vector database;
- autonomous AI execution as a production architecture;
- universal research/live code sharing strategy.

These remain experiment or technology-radar questions.
