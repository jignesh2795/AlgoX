# AlgoX Brain Evolution Roadmap

## Principle

AlgoX should evolve from a research archive into an institutional intelligence system. Each generation adds a capability while preserving the evidence and history of previous generations.

## Generations

### G0 — Context

Current task context and transient working state.

### G1 — Persistent Research Memory

Structured project, source, finding, experiment and decision records.

### G2 — Evidence Memory

Every important claim is connected to evidence, source version, locator, observation time and confidence.

### G3 — Multi-layer Memory

Working, episodic, semantic, procedural, source and meta memory with explicit consolidation rules.

### G4 — Temporal Knowledge Brain

The system can answer both:

- what is believed now?
- what did AlgoX know/believe at time T?

Supersession, contradiction and validity intervals become first-class.

### G5 — Learning Loop

```text
research → experiment → result → confidence change → decision → outcome
                                      ↑                    │
                                      └────────────────────┘
```

AlgoX learns from outcomes rather than merely accumulating documents.

### G6 — Research Organization

The system prioritizes research questions, selects evidence-gathering strategies, identifies knowledge gaps and proposes experiments.

Human review remains required for consequential institutional decisions.

### G7 — Institutional Intelligence

AlgoX can reconstruct the reasoning behind major architectural and research decisions, identify recurring failure modes, transfer knowledge between domains and detect when old knowledge has become stale.

## Memory consolidation

Not every observation becomes permanent semantic knowledge.

```text
Observation
   ↓
Candidate memory
   ↓
Evidence check
   ↓
Deduplicate / relate
   ↓
Confidence assessment
   ↓
Consolidate
   ↓
Semantic / procedural knowledge
```

Working memories can expire. Episodic records should remain durable. Semantic memories can be superseded but should not be silently deleted.

## Anti-patterns

- Treating chat history as institutional memory.
- Treating embeddings as truth.
- Allowing an LLM to silently rewrite facts.
- Deleting contradictory evidence.
- Losing source versions after an update.
- Conflating popularity with evidence quality.
- Making a specialized database authoritative before workload validation.
- Optimizing retrieval latency while degrading provenance.

## Success condition

AlgoX becomes more capable over time **without becoming less auditable**.

The brain must be able to explain not only its answer, but the evidence, temporal context, uncertainty and chain of reasoning that produced it.
