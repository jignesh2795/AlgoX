# AlgoX Technology Radar — Memory, Knowledge and Retrieval

**Status:** Initial radar
**Scope:** technologies and architectural patterns relevant to evolving AlgoX institutional memory

## The direction

AlgoX should evolve its memory in the same direction that stronger agent-memory systems have been moving: from raw conversation/context retention toward **structured, temporal, provenance-aware, retrievable knowledge**.

2024 research highlighted that long-term agent memory requires explicit memory management and that vector databases were only one implementation pattern. citeturn0search0turn0academia61

By 2024–2025, systems such as Zep/Graphiti demonstrated a stronger pattern: continuously construct a temporal knowledge graph from episodes and structured data, preserve historical relationships, and retrieve a compact context rather than repeatedly replaying entire histories. citeturn0search4turn0search7

AlgoX should learn from this evolution without copying any single vendor architecture.

## Radar rings

### ADOPT

**1. Evidence-first memory**

Memory entries must point to evidence. Generated summaries are views, not truth.

**2. Typed memory**

Separate episodic, semantic, procedural, decision, evidence, failure, and temporal memory.

**3. Temporal memory**

Represent both when a fact was valid and when AlgoX learned/observed it where the distinction matters.

**4. Provenance**

A finding must be traceable through evidence to its source/version/locator.

**5. Supersession instead of destructive overwrite**

When knowledge changes, preserve the old state and record the new state and relationship.

**6. PostgreSQL as initial authority**

Use a transactional store for institutional truth.

**7. Object storage for source artifacts**

Keep raw source material independently from derived knowledge.

### TRIAL

**8. pgvector semantic index**

Use embeddings to retrieve candidate evidence/knowledge, while keeping canonical records relational.

**9. Hybrid retrieval**

Fuse lexical, semantic, metadata, temporal, provenance, and eventually graph signals.

**10. Memory consolidation pipeline**

```text
Experience
  ↓
Extract candidate facts
  ↓
Resolve entities
  ↓
Check existing memory
  ↓
Detect contradiction/supersession
  ↓
Attach provenance + time
  ↓
Validate
  ↓
Commit knowledge delta
```

**11. Memory evaluation suite**

Test retrieval with point-in-time, contradiction, provenance, multi-session, and cross-project questions—not only nearest-neighbor similarity.

### ASSESS

**12. Dedicated graph database**

Evaluate only after graph-heavy workloads are measurable.

**13. Search engine**

Evaluate if lexical/hybrid retrieval scale or document-search requirements exceed the relational index.

**14. Specialized agent-memory frameworks**

Study systems such as MemGPT/Letta and Zep/Graphiti as research subjects and reusable patterns, not as mandatory dependencies.

### HOLD

**15. Vector DB as system of record**

Rejected as an authority model because embeddings do not preserve the full structured/provenance/temporal semantics required by AlgoX.

**16. Graph DB because "memory needs graphs"**

Premature. The data model should be graph-compatible; the storage engine should be evidence-driven.

**17. Generic chat-history memory**

Insufficient for institutional research. Chat is an episode source, not the final knowledge model.

## The AlgoX memory loop

```text
                    ┌──────────────────┐
                    │  WORLD / SOURCES │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │     EPISODES     │
                    │ sources, runs,   │
                    │ experiments      │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    EXTRACTOR     │
                    │ claims/entities/ │
                    │ relationships    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ MEMORY GOVERNOR  │
                    │ provenance/time/ │
                    │ contradiction    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ KNOWLEDGE STORE  │
                    └────────┬─────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          semantic       lexical        graph
          projection     projection     projection
              └──────────────┼──────────────┘
                             ↓
                    ┌──────────────────┐
                    │ MEMORY RETRIEVER │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ EVIDENCE BUNDLE  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ RESEARCH/AGENT   │
                    └────────┬─────────┘
                             ↓
                    new experience / evidence
                             ↺
```

## The important evolution

The goal is not to make AlgoX remember everything.

The goal is to make it **remember the right things, know why it believes them, know when they were true, detect when they changed, retrieve the evidence, and learn from the result**.

That is the foundation for institutional intelligence rather than simple agent memory.
