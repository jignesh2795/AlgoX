# 2025 Agent Memory and Reasoning

## Status
PROVISIONAL historical evidence.

## Research question
Did 2025 agent systems solve the memory and reasoning weaknesses identified in 2023–2024, or mainly make the same architectures more capable?

## Evidence
Zep's January 2025 paper introduced Graphiti, a temporally-aware knowledge graph memory layer that integrates conversational and structured business data while preserving historical relationships. Its reported evaluations showed gains over MemGPT on DMR and stronger temporal/enterprise evaluations on LongMemEval. These are research results, not proof of production superiority. [1]

The 2025 agent-memory literature increasingly treats memory as a first-class subsystem rather than a synonym for vector retrieval. Important dimensions include temporal state, entity relationships, consolidation, experience, and retrieval policy. [1]

Financial-agent surveys in 2025 identify numerical reasoning, prompt sensitivity, real-time adaptability, deployment constraints, and evaluation as continuing obstacles. They also distinguish financial functions such as data analysis, investment research, trading, investment management, and risk management. [2]

## 2023–2024 hypothesis check

| Earlier finding | 2025 status | Interpretation |
|---|---|---|
| Externalized memory is necessary | VALIDATED | Memory became a distinct architectural capability. |
| Vector retrieval alone is institutional memory | REJECTED | Temporal/relational memory architectures became increasingly explicit. |
| Evaluation belongs inside the development loop | VALIDATED | Agent research increasingly evaluates task success, retrieval, temporal correctness and workflow behavior. |
| More autonomy automatically improves reliability | REJECTED | Finance research still reports reliability and deployment limitations. |
| AI should directly control irreversible execution | UNVERIFIED / HIGH RISK | 2025 finance surveys still describe direct trading autonomy as an open research/deployment problem. |
| Temporal provenance matters | STRENGTHENED | Temporal graph memory directly addresses evolving facts and historical relationships. |

## AlgoX finding
The durable 2025 shift is from **retrieval-augmented agents** toward **stateful, evidence-aware agents**.

A useful model is:

```text
Experience / Sources
        ↓
Memory Formation
        ↓
Temporal + Relational State
        ↓
Evidence-Aware Retrieval
        ↓
Reasoning
        ↓
Action / Experiment
        ↓
Outcome
        ↓
Consolidation
        ↺
```

## Important qualification
Benchmark improvements do not establish that a memory architecture is universally superior. AlgoX must record benchmark dataset, task definition, temporal requirements, retrieval policy, model, latency, and evaluation protocol before treating a result as transferable.

## Implication for AlgoX brain
The existing AlgoX design is directionally correct but should evolve toward explicit **experience memory + semantic knowledge + procedural knowledge + temporal relations + outcome learning**. The authoritative layer remains evidence-backed canonical records; graph and semantic indexes remain projections.

## References
1. Rasmussen et al., “Zep: A Temporal Knowledge Graph Architecture for Agent Memory,” arXiv:2501.13956, 2025.
2. Dong et al., “Large Language Model Agents in Finance: A Survey Bridging Research, Practice, and Real-World Deployment,” Findings of EMNLP 2025.
