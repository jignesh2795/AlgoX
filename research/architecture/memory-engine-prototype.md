# AlgoX Memory Engine Prototype

Status: **Design-ready / implementation next**

## Objective

Create a storage-independent memory engine whose authoritative unit is a provenance-bearing memory record, not an embedding.

## Canonical flow

```text
Observation / Source
        ↓
Evidence
        ↓
Memory Record
        ↓
Relations + temporal metadata
        ↓
Retrieval projections
        ↓
Evidence Bundle
        ↓
Reasoning
        ↓
Knowledge Delta
        ↓
Validation
        ↓
Commit / Reject
```

## Memory types

- **working** — short-lived context for the current research task.
- **episodic** — what AlgoX experienced: research runs, experiments, observations, failures, decisions.
- **semantic** — normalized knowledge: projects, algorithms, capabilities, claims and findings.
- **procedural** — repeatable methods, playbooks, research protocols and engineering procedures.
- **source** — durable identity and version information for external artifacts.
- **meta** — information about confidence, provenance, conflicts, retrieval quality and memory itself.

## Authority rules

1. No semantic memory without provenance.
2. No high-confidence claim without evidence meeting the applicable evidence standard.
3. New information does not silently overwrite old information.
4. Temporal changes create a new state or supersession relation.
5. Contradictory evidence remains retrievable and is explicitly classified.
6. Embeddings are derived indexes and may be rebuilt.
7. Graph projections are derived indexes and may be rebuilt.
8. A model may propose a knowledge delta but cannot make an unvalidated institutional-memory mutation.

## Initial storage implementation

The first prototype should use a relational schema because it gives AlgoX transactions, constraints, temporal fields, provenance joins and JSON extensibility without prematurely committing to a specialized graph database.

Suggested logical tables:

```text
sources
source_versions
evidence
memory_records
memory_relations
claims
findings
experiments
experiment_results
decisions
knowledge_deltas
retrieval_events
```

Optional derived indexes:

```text
pgvector embeddings
full-text index
materialized graph projection
```

## Retrieval contract

A retriever must return an **Evidence Bundle**, not only text chunks:

```yaml
query: "Why did AlgoX choose event-driven order state?"
items:
  - memory_id: MEM-001
    content: "..."
    evidence_ids: [E-001, E-014]
    confidence: high
    valid_from: "2026-01-01T00:00:00Z"
    relations: ["supports ADR-0042"]
counter_evidence: []
constraints:
  as_of: "2026-09-12T00:00:00Z"
```

## First implementation milestone

Build a minimal in-process repository with the following operations:

```text
add_source()
add_evidence()
add_memory()
link_memory()
retrieve()
find_conflicts()
propose_delta()
validate_delta()
commit_delta()
reconstruct_as_of()
```

The implementation must have no dependency on a specific LLM, vector database or graph database.

## Evaluation workloads

The first benchmark should test:

1. exact source lookup
2. semantic recall
3. multi-hop relationship retrieval
4. contradiction detection
5. historical `as_of` reconstruction
6. provenance reconstruction
7. supersession handling
8. decision reconstruction
9. experiment-to-decision tracing
10. rebuildability of derived indexes

## Exit criterion

Do not promote a specialized graph/vector database to an authoritative role merely because it improves retrieval in one benchmark. It must improve the overall evidence lifecycle without weakening provenance, temporal correctness, transactions, explainability or rebuildability.
