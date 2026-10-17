# PX-2024-011 — Agent Memory Research

**Historical category:** AI-agent infrastructure / memory
**Domain:** Agent architecture, long-horizon research systems

## Historical signal

2024 research increasingly treated memory as a distinct subsystem of LLM-agent architectures rather than assuming that a larger context window solved persistence. Surveys organized memory around sources, forms, operations, design, and evaluation.

## Evidence

The 2024 survey by Zhang et al. reviews memory mechanisms for LLM-based agents and emphasizes that memory supports long-term agent-environment interaction. It also distinguishes memory design from its evaluation. citeturn0academia24

The LoCoMo benchmark demonstrated that very long-term conversational memory remains difficult: its evaluation spans up to 32 sessions and roughly 600 turns, and found that long-context models and RAG improve performance but still leave substantial gaps. citeturn0search1

## Architectural lesson

Memory should be treated as a governed subsystem with explicit write, storage, retrieval, relevance, provenance, contradiction, and evaluation policies.

## AlgoX extraction

- persistent institutional memory
- evidence-linked memory
- episodic research memory
- semantic knowledge
- source provenance
- retrieval policy
- memory evaluation
- contradiction handling
- temporal validity
- controlled memory writes

## Critical distinction

AlgoX should not equate:

```text
conversation history = memory
RAG index = memory
vector database = memory
```

Instead:

```text
Memory
├── source observations
├── research episodes
├── findings
├── decisions
├── capabilities
├── experiments
├── provenance
├── temporal validity
└── retrieval policy
```

## Relevance to AlgoX

Very high. AlgoX is intended to preserve institutional research knowledge and prevent repeated research. Memory therefore becomes part of the core architecture, not an optional agent feature.

**Evidence maturity:** C2
**Status:** RESEARCHED
