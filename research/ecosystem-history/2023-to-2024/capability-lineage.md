# Capability Lineage — 2023 → 2024

This map tracks how important AI/software-engineering capabilities evolved rather than treating yearly projects as isolated artifacts.

```text
Foundation-model access
  └─ 2023 model abstraction
       └─ 2024 provider/runtime abstraction
            └─ model-serving infrastructure

Retrieval
  └─ 2023 RAG libraries
       └─ 2024 ingestion/index/retrieval subsystems
            └─ context engineering + evaluation

Agent loop
  └─ 2023 autonomous prototypes
       └─ 2024 tools + workflow/state
            └─ controlled agent runtimes

Local models
  └─ 2023 llama.cpp
       └─ 2024 GPT4All + Ollama ecosystem
            └─ local/private inference as deployment option

AI coding
  └─ 2023 GPT Engineer / Aider / early coding agents
       └─ 2024 SWE-bench + SWE-agent + Cline + OpenHands
            └─ repository-level engineering agents

Evaluation
  └─ qualitative demos
       └─ task benchmarks
            └─ reproducible containers + acceptance/regression tests
```

## AlgoX architectural deduction
The lineage suggests six reusable research-agent layers:

1. **Model layer** — interchangeable providers/runtimes.
2. **Context layer** — source retrieval, repository inspection, historical context.
3. **Tool layer** — search, GitHub, files, code execution, experiment runners.
4. **Control layer** — planning, state machines, budgets, permissions, checkpoints.
5. **Execution layer** — isolated environments for reproduction and experiments.
6. **Evidence layer** — provenance, tests, benchmarks, findings, decisions.

These layers should remain independently replaceable.
