# 2023 Contradiction Analysis

Status: PROVISIONAL HISTORICAL SYNTHESIS

## Purpose

This document records disagreements and trade-offs found across the 2023 research set. A contradiction is not automatically an error: it may arise from different workloads, datasets, market regimes, implementation choices, or definitions.

## 1. Research speed vs execution fidelity

Vectorized research systems such as vectorbt optimize for high-throughput exploration. Event-driven engines such as LEAN, Freqtrade, and related systems expose more execution semantics.

Finding: neither is universally superior.

Decision implication: separate **research throughput** from **execution fidelity**. AlgoX should benchmark both rather than selecting a single backtesting architecture by popularity.

## 2. Unified broker API vs venue fidelity

CCXT demonstrates the value of a common exchange interface. Broker and exchange APIs simultaneously expose venue-specific order, market-data, authentication, and event semantics.

Finding: normalization is valuable only when the normalized contract does not erase information required for correctness.

Decision implication: use a canonical interface with an explicit venue-specific escape hatch.

## 3. Backtest/live parity vs realistic simulation

A shared strategy/execution model reduces research-to-production translation risk. However, historical simulation cannot automatically reproduce latency, queue position, liquidity, outages, exchange behavior, or broker-specific semantics.

Finding: code-path parity is useful but is not evidence that simulation is realistic.

Decision implication: require explicit simulation assumptions and a fidelity report alongside backtest results.

## 4. Autonomous agents vs controlled agents

2023 agent projects demonstrated planning, tools, memory, and multi-agent coordination. Evaluation work showed substantial gaps between demonstrations and reliable environment-level task completion.

Finding: autonomy is a capability dimension, not a quality metric.

Decision implication: prefer bounded execution, permissions, checkpoints, verification, and reproducible environments over maximum autonomy.

## 5. More agents vs better outcomes

CAMEL, AutoGen, MetaGPT, and ChatDev explored role specialization and multi-agent interaction. The existence of multiple roles does not establish that additional agents improve outcomes.

Finding: coordination overhead and error propagation are first-class costs.

Decision implication: multi-agent architectures require controlled experiments against a single-agent baseline.

## 6. Vector retrieval vs institutional memory

2023 retrieval/vector systems made semantic search practical, but a vector representation does not preserve all temporal, provenance, contradiction, or governance semantics.

Finding: retrieval representation and authoritative knowledge are different layers.

Decision implication: AlgoX must preserve canonical evidence and structured relationships independently of semantic indexes.

## 7. Model size vs capability

LLaMA, Code Llama, local inference projects, and serving systems demonstrated that smaller or specialized models can be useful under appropriate workloads.

Finding: parameter count is not a sufficient architecture-selection criterion.

Decision implication: model choice should be task-, cost-, latency-, privacy-, and quality-dependent, with replaceable model interfaces.

## 8. AI-generated software vs verified software

GPT Engineer, Aider, SWE-bench-related work, and coding-agent research established that code generation can accelerate development while still requiring repository context, tests, iteration, and human verification.

Finding: generated code is an implementation proposal until validated.

Decision implication: AlgoX treats AI-assisted development as an engineering workflow with evidence gates, not as an autonomous source of truth.

## 9. Broker event stream vs broker state

Order updates are observations about an external system. Connection loss, retries, duplicates, partial fills, and out-of-order events can make a local event stream incomplete.

Finding: the event stream alone cannot always be treated as authoritative state.

Decision implication: reconciliation must be a first-class execution capability.

## 10. Market-data normalization vs identity preservation

Research systems benefit from normalized OHLCV/tick schemas. Trading systems also need venue/security identity, contract specifications, corporate actions, timestamps, and source provenance.

Finding: normalized values without canonical identity can produce silent research and execution errors.

Decision implication: instrument identity and provenance belong in the canonical market-data model.

## 11. Popularity vs engineering quality

Projects with large communities are useful evidence sources, but popularity can reflect timing, marketing, ecosystem effects, or ease of adoption.

Finding: stars, forks, and attention are ecosystem signals, not technical-quality measurements.

Decision implication: evaluate architecture, evidence maturity, tests, maintenance, reproducibility, and production characteristics separately.

## Contradiction resolution protocol

When AlgoX detects conflicting claims, it should classify the conflict before selecting a winner:

1. different time period
2. different implementation/version
3. different dataset
4. different market regime
5. different metric definition
6. different assumptions
7. incomplete evidence
8. source-quality difference
9. genuine unresolved disagreement

Only after classification should AlgoX issue a decision. If the conflict remains unresolved, preserve both claims with their evidence and assumptions.

## Provisional 2023 meta-finding

The strongest common lesson across the 2023 ecosystem is not a particular framework. It is the emergence of **explicit boundaries**:

- model vs application
- retrieval vs knowledge
- command vs observation
- event vs state
- research vs execution
- normalization vs venue semantics
- generation vs verification
- proposal vs institutional truth

These boundaries are stronger architectural evidence than individual project popularity.
