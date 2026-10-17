# ADR-0001 — Evolve AlgoX as an Evidence-Backed Institutional Memory

**Status:** Accepted for research architecture
**Date:** 2026-09-12

## Context

AlgoX needs memory that survives individual research runs and prevents repeated rediscovery. Agent-memory research has moved from simple context retention and vector retrieval toward typed memory, temporal knowledge, provenance, contradiction handling, and context assembly. 2024 survey/review work identifies persistent memory management as a central agent problem; Zep/Graphiti's 2024–2025 work demonstrates temporal graph memory as one concrete evolution. citeturn0search0turn0academia61turn0search7

AlgoX has a stricter requirement than a conversational assistant: its memory will contain research claims, source evidence, experiments, benchmarks, engineering decisions, financial-system constraints, and historical beliefs. Incorrect or decontextualized memory can therefore cause incorrect architecture or trading-system decisions.

## Decision

AlgoX will evolve as an **evidence-backed institutional memory system**.

The canonical model will represent:

- episodes;
- sources and source versions;
- evidence;
- claims;
- findings;
- capabilities;
- experiments and benchmarks;
- decisions and ADRs;
- failures;
- entities and relationships;
- temporal validity;
- provenance;
- confidence/evidence maturity;
- supersession and contradiction.

The first implementation will use:

1. **object storage** for raw source/artifact preservation;
2. **PostgreSQL** as the authoritative structured store;
3. **pgvector** as a derived semantic retrieval index when the first retrieval experiments justify it;
4. a **logical graph model** from day one, implemented initially in relational tables;
5. a **dedicated graph/search/cache system only after workload benchmarks justify the additional operational surface**.

## Rationale

The architectural target should follow the strongest pattern in the ecosystem without blindly adopting its infrastructure.

A vector index is excellent at approximate semantic retrieval but is not sufficient as the institutional authority. A graph is excellent at relationship traversal but does not by itself solve provenance, source preservation, experiment lineage, or transactional governance. A relational authority can preserve these semantics while allowing optimized projections to be rebuilt.

## Memory policy

### Write policy

No important memory is committed without:

- provenance;
- source/version reference;
- timestamps appropriate to the claim;
- schema validation;
- contradiction/supersession check;
- confidence/evidence state.

### Read policy

Research reasoning should prefer an evidence bundle containing:

- supporting evidence;
- counter-evidence;
- relevant temporal constraints;
- source authority;
- confidence/maturity;
- related decisions and experiments.

### Update policy

Do not silently overwrite historically meaningful knowledge. Prefer:

```text
old fact
  ↓
SUPERSEDED / REFUTED / QUALIFIED
  ↓
new fact
```

This allows AlgoX to reconstruct what it believed at a prior point in time.

## Evolution roadmap

### Stage 0 — Knowledge contract

Define schemas, provenance, temporal semantics, evidence maturity, decision records, and graph relations.

### Stage 1 — Durable memory

Implement PostgreSQL + object storage. Establish source ingestion, evidence records, claims, findings, experiments, decisions, and temporal metadata.

### Stage 2 — Retrieval memory

Add lexical and semantic retrieval. Use pgvector initially if experiments show adequate quality/latency.

### Stage 3 — Memory consolidation

Build automated candidate extraction and knowledge-delta generation. Require validation before commit.

### Stage 4 — Contradiction + temporal reasoning

Support supersession, qualification, refutation, as-of queries, and competing claims under different assumptions.

### Stage 5 — Memory evaluation

Create benchmark suites for:

- exact evidence retrieval;
- semantic retrieval;
- provenance tracing;
- temporal retrieval;
- contradiction resolution;
- multi-hop capability reasoning;
- decision reconstruction;
- research-regression detection.

### Stage 6 — Graph specialization

Benchmark the relational graph representation against one or more dedicated graph engines using real AlgoX workloads. Promote a graph database only if measured benefits justify it.

### Stage 7 — Self-improving research memory

Use research outcomes to update:

```text
source reliability
retrieval quality
research strategy
capability confidence
technology radar
experiment priorities
```

The memory system therefore learns not merely facts, but **how AlgoX learns**.

## Consequences

### Positive

- institutional memory survives individual sessions;
- evidence remains auditable;
- historical knowledge is preserved;
- derived indexes can be rebuilt;
- specialized databases can be added without changing the canonical model;
- research quality can improve through measured feedback.

### Negative

- more metadata must be maintained;
- ingestion and consolidation become engineering problems;
- temporal/contradiction handling adds complexity;
- memory evaluation becomes necessary;
- a graph database may eventually be required for some workloads.

## Rejected alternatives

### Vector database as primary memory

Rejected. Useful retrieval mechanism, insufficient institutional authority.

### Graph database as day-one primary store

Rejected. Strong conceptual fit, but infrastructure choice is premature without workload evidence.

### Chat transcript as memory

Rejected. Transcripts preserve experience but not normalized evidence, temporal facts, decisions, or reusable capabilities.

### One giant knowledge graph

Rejected. Raw sources, evidence, derived knowledge, and retrieval indexes have different lifecycle and integrity requirements.

## Success criterion

AlgoX should eventually be able to answer:

> **What do we currently believe, why do we believe it, what evidence supports or contradicts it, when was it true, what experiment changed our confidence, and what decision did we make because of it?**

That is the definition of the AlgoX "brain".
