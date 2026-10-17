# Replaced or Constrained Patterns — 2023 → 2024

These patterns did not disappear, but their naive forms became less strategically useful.

| Early pattern | Why constrained | More mature form |
|---|---|---|
| Fully autonomous agent loop | unreliable, difficult to reproduce, costly | bounded workflows with checkpoints |
| Prompt as architecture | hidden coupling and weak guarantees | explicit state, tools, contracts |
| Single-model dependency | model capability and economics change | provider/runtime abstraction |
| RAG as a vector database feature | retrieval quality depends on ingestion, ranking, evaluation | complete context/data subsystem |
| Code generation without execution | syntax correctness is insufficient | edit → run → observe → test → repair |
| Unrestricted shell access | security and reproducibility risk | sandboxed runtime + permissions |
| Demo-based agent evaluation | success criteria are ambiguous | task benchmarks + acceptance tests |
| Popularity as quality | adoption does not prove correctness | evidence + benchmark + maintenance analysis |

## AlgoX rule

Never promote a pattern into the capability catalog merely because it is popular. Record the evidence level, operating assumptions, failure modes, and measured trade-offs.
