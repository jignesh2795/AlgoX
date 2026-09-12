# AlgoX Memory Evolution Roadmap

## Decision

AlgoX will evolve through **memory generations**, not by committing prematurely to a single database or agent-memory framework.

The target is an institutional research brain with progressively stronger memory, reasoning, validation, and self-improvement loops.

## Generation 0 — Context

```text
conversation → prompt → answer
```

Useful for immediate work, but no durable institutional memory.

**Status:** historical baseline.

## Generation 1 — Persistent Research Records

```text
sources + projects + findings + decisions
              ↓
        structured files
```

Capabilities:

- reproducible research records
- explicit provenance
- schemas
- evidence maturity
- decisions
- experiments

**AlgoX status:** already established.

## Generation 2 — Evidence Memory

```text
raw source
   ↓
evidence
   ↓
claim
   ↓
finding
   ↓
decision
```

Add:

- evidence registry
- source versions
- claim identity
- contradiction tracking
- temporal validity
- supersession
- confidence evolution

**Target:** current phase.

## Generation 3 — Multi-layer Institutional Memory

```text
                 MEMORY
                    │
      ┌─────────────┼─────────────┐
      ↓             ↓             ↓
   episodic      semantic     procedural
      ↓             ↓             ↓
 experiments     knowledge     methods
 decisions       claims       playbooks
```

Add a persistent database authority while retaining source artifacts as immutable evidence.

Recommended initial topology:

```text
Object storage
      │
      ↓
PostgreSQL ← authoritative metadata/knowledge/evidence
      │
      ├── pgvector → semantic retrieval
      └── relational graph → relationship traversal
```

**Decision:** PostgreSQL-first.

## Generation 4 — Temporal Knowledge Brain

Introduce a first-class temporal graph projection.

```text
Episode
  ↓
Entity
  ↓
Claim / Edge
  ↓
valid_at / invalid_at
  ↓
provenance
```

This follows the important direction demonstrated by Zep/Graphiti: incrementally updated temporal knowledge, historical relationships, and hybrid retrieval rather than treating retrieved documents as timeless truth. citeturn0academia24turn0search0

Only introduce a dedicated graph database if AlgoX benchmarks show that relational graph traversal is insufficient.

## Generation 5 — Learning Brain

The system begins learning from its own research history.

```text
Research question
       ↓
Plan
       ↓
Research
       ↓
Evidence
       ↓
Experiment
       ↓
Result
       ↓
Decision
       ↓
Outcome
       ↓
Meta-learning
       ↺
```

It should learn:

- which sources are reliable for which questions;
- which retrieval strategies work;
- which experiments are informative;
- which architectures repeatedly fail;
- which capabilities are reusable;
- which decisions later proved wrong;
- which research methods reduce wasted work.

## Generation 6 — Self-improving Research Organization

AlgoX becomes capable of proposing improvements to its own research process.

```text
                    ALGOX
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
     DOMAIN MEMORY          PROCESS MEMORY
          ↓                       ↓
   what we know           how we research
          └───────────┬───────────┘
                      ↓
               META-RESEARCH
                      ↓
              METHOD IMPROVEMENT
                      ↓
                BETTER RESEARCH
```

Examples:

- identify that a source class is systematically stale;
- discover that benchmark results are not reproducible;
- learn that certain claims require multiple independent sources;
- improve research prioritization from historical research cost/value;
- identify recurring engineering failure modes;
- improve experiment design from previous failed experiments.

## Generation 7 — Institutional Intelligence

The final target is not an autonomous chatbot. It is a durable research organization encoded as software.

```text
                WORLD
                  ↓
             OBSERVATION
                  ↓
               MEMORY
                  ↓
              KNOWLEDGE
                  ↓
               REASONING
                  ↓
             EXPERIMENT
                  ↓
              EVIDENCE
                  ↓
              DECISION
                  ↓
             IMPLEMENTATION
                  ↓
               OUTCOME
                  ↓
              LEARNING
                  ↺
```

The system should preserve organizational memory even when the underlying model changes.

## Memory implementation rules

### Rule 1 — Model-independent memory

The database must not depend on a specific LLM provider.

### Rule 2 — Evidence before synthesis

Derived knowledge must always point back to evidence.

### Rule 3 — History is preserved

Changing a fact creates a new version or invalidates the old relation. It does not erase history.

### Rule 4 — Retrieval is policy-driven

The system chooses lexical, semantic, graph, temporal, or combined retrieval according to the question.

### Rule 5 — Memory writes are governed

Models propose changes. Validators and policy decide whether those changes become institutional memory.

### Rule 6 — Memory must be testable

Every memory subsystem gets evaluation datasets and regression tests.

### Rule 7 — Memory must be useful, not merely large

A larger memory that increases irrelevant retrieval or contradiction is a regression.

## Evaluation dimensions

Every memory generation should be benchmarked on:

- recall
- precision
- temporal correctness
- provenance correctness
- contradiction detection
- entity resolution
- retrieval latency
- write latency
- memory growth
- token reduction
- research-task success
- reproducibility
- cost

## Technology evolution rule

Do not choose technology because it is fashionable.

```text
Requirement
   ↓
Workload
   ↓
Benchmark
   ↓
Evidence
   ↓
Technology decision
```

The current ecosystem shows multiple viable patterns: hierarchical/self-editing memory in Letta, semantic/episodic/procedural memory in LangMem, graph-temporal memory in Graphiti/Zep, and graph-enhanced long-term memory in Mem0. citeturn1search5turn1search6turn0academia24turn0academia25

AlgoX should learn from all of them without becoming coupled to any of them.
