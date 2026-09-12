# Surviving Patterns — 2023 → 2024

Patterns that survived the transition and became stronger architectural primitives:

| Pattern | 2023 form | 2024 form | AlgoX implication |
|---|---|---|---|
| Model abstraction | provider wrappers | runtime/provider abstraction | model layer must be replaceable |
| Retrieval | RAG feature | data/context subsystem | retrieval needs provenance and evaluation |
| Tools | agent actions | explicit tool interfaces | tools need schemas, permissions, and auditability |
| Memory/state | conversation memory | persistent state/workflow state | state must be explicit and inspectable |
| Agent loop | autonomous loop | bounded workflow | control policy becomes first-class |
| Coding AI | code generation | repository engineering | context + execution + verification are required |
| Evaluation | qualitative demo | benchmark + tests | claims need measurable acceptance criteria |
| Local AI | local model experimentation | deployment/runtime ecosystem | local inference is a replaceable backend |
| Human feedback | prompt approval | permission/checkpoint boundary | high-impact actions require explicit controls |
| Observability | logs/debugging | evaluation + traces + outcomes | evidence must survive the run |

## Strongest durable principle

> A useful AI system is an engineered loop around a model, not merely a model wrapped in a prompt.
