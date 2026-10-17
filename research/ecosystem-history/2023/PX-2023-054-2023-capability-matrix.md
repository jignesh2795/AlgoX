# PX-2023-054 — Provisional 2023 Capability Matrix

**Status:** PROVISIONAL — historical synthesis continues

This matrix converts the 2023 project research into capability-level conclusions. It deliberately separates research capability from production evidence.

| Capability | Evidence sources | 2023 lesson | AlgoX disposition |
|---|---|---|---|
| Model/provider abstraction | LLaMA, Code Llama, vLLM | model choice is replaceable | ADOPT |
| Tool/agent orchestration | ReAct, CAMEL, AutoGen | explicit interaction policy matters | ADOPT |
| Memory | MemGPT, Reflexion, Generative Agents, Voyager | memory types and feedback differ | ADOPT |
| Agent evaluation | AgentBench, WebArena, SWE-bench | real environments expose capability gaps | ADOPT |
| Repository-aware coding | Aider, GPT Engineer, SWE-bench | code generation needs repository context + tests | ADOPT |
| Retrieval | Qdrant, Weaviate, Milvus, Chroma | retrieval is infrastructure, not truth | ADAPT |
| Financial research | Qlib, FinRL, FinGPT, BloombergGPT | domain-specific data/evaluation matter | ADAPT |
| High-throughput research | vectorbt | vectorization accelerates idea exploration | ADAPT |
| Trading bot lifecycle | Freqtrade | backtest and forward/live modes must be separated | ADAPT |
| Trading engine | LEAN | strategy/portfolio/risk/execution can be modular | ADAPT |
| Exchange connectivity | CCXT, Hummingbot, broker APIs | connector boundary is fundamental | ADAPT |
| Broker event handling | Kite, Upstox and other APIs | commands and asynchronous events differ | ADOPT |
| Instrument identity | broker instrument masters | ticker strings are insufficient identity | ADOPT |
| Order reconciliation | broker APIs + trading engines | observed state requires reconciliation | ADOPT |
| Backtest validation | vectorbt, Freqtrade, LEAN | speed is not fidelity | ADOPT |
| Execution simulation | LEAN / event-driven engines | fill/latency assumptions must be explicit | ADAPT |
| Data provenance | exchange/broker infrastructure | source and effective time matter | ADOPT |
| Knowledge governance | AlgoX research | model proposal must not become truth automatically | ADOPT |

## Cross-project contradiction themes

### 1. More autonomy vs more reliability
Agent projects often increase autonomy; evaluation projects show that autonomy without verification can remain unreliable.

**Resolution:** optimize controlled capability, not autonomy as an isolated metric.

### 2. Normalization vs venue fidelity
Unified APIs reduce integration cost; venue-specific semantics remain material.

**Resolution:** canonical interface plus explicit native capability escape hatch.

### 3. Backtest speed vs execution realism
Vectorized systems maximize research throughput; event-driven systems model richer execution behavior.

**Resolution:** maintain separate research-speed and execution-fidelity benchmarks.

### 4. Retrieval vs institutional truth
Vector databases improve retrieval but do not establish provenance, temporal validity, or contradiction state.

**Resolution:** evidence-backed canonical knowledge; retrieval is derived.

### 5. Research abstraction vs live behavior
Research platforms can simplify market interaction; brokers/exchanges impose operational semantics.

**Resolution:** shared canonical contracts with explicit simulation/live boundaries.

## Highest-priority 2023 capabilities

1. Evidence/provenance
2. Canonical instrument identity
3. Canonical order/event contracts
4. Reconciliation
5. Explicit simulation assumptions
6. Research/live parity controls
7. Capability-based provider abstraction
8. Evaluation/benchmark harnesses
9. Typed institutional memory
10. Deterministic, reproducible experiments

## Important non-conclusion

This matrix does **not** select a database, broker, vector store, LLM, graph database, or execution framework. Those choices require later experiments and technology-radar evaluation.
