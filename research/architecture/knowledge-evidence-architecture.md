# AlgoX Knowledge + Evidence Architecture

**Status:** PROPOSED
**Purpose:** Convert research outputs into auditable institutional knowledge without coupling the system to a specific LLM, vector database, or graph database.

## 1. Design objective

AlgoX needs two related but distinct systems:

1. **Evidence System** — preserves source material, provenance, versions, retrieval context, verification, and reproducibility.
2. **Knowledge System** — represents durable entities, claims, findings, relationships, decisions, and capability state.

Neither system should be implemented as an LLM memory buffer.

## 2. Logical architecture

```text
                    RESEARCH ENGINE
                          │
                  ┌───────┴───────┐
                  │               │
             Query Planner    Memory Policy
                  │               │
                  └───────┬───────┘
                          ↓
                 RETRIEVAL ORCHESTRATOR
                          │
          ┌───────────────┼────────────────┐
          ↓               ↓                ↓
   Document Search   Knowledge Graph   Metadata Search
          │               │                │
          └───────────────┼────────────────┘
                          ↓
                  Evidence Ranker
                          ↓
                   Evidence Bundle
                          ↓
                    LLM Reasoning
                          ↓
                  Claim Extraction
                          ↓
                Verification / Review
                          ↓
                 Knowledge Commit
                          ↓
             Knowledge + Evidence Stores
```

## 3. Storage responsibilities

### Source store
Raw or normalized source artifacts:
- papers
- repository snapshots
- README files
- API documentation
- standards
- exchange/regulatory documents
- benchmark datasets
- experiment artifacts

### Evidence store
Evidence-level metadata:
- source reference
- locator
- retrieved timestamp
- publication timestamp
- version/commit
- excerpt or structured observation
- provenance
- evidence maturity
- verification status

### Knowledge store
Durable entities and relations:
- Project
- Capability
- Algorithm
- Architecture
- Technology
- Requirement
- Claim
- Finding
- Experiment
- Benchmark
- Decision
- Failure
- SourceVersion

### Search index
Optimized retrieval representations. It is derived state and may be rebuilt.

## 4. Claim lifecycle

```text
OBSERVED
   ↓
CLAIMED
   ↓
SUPPORTED
   ↓
VERIFIED
   ↓
VALIDATED
   ↓
DECISION-RELEVANT
```

A claim can move backwards when contradictory evidence appears. Historical states should remain recoverable.

## 5. Knowledge commit

LLM output should not directly mutate durable knowledge.

Instead:

```text
LLM proposes change
       ↓
Structured knowledge delta
       ↓
Schema validation
       ↓
Provenance validation
       ↓
Contradiction detection
       ↓
Policy / confidence checks
       ↓
Human or automated approval
       ↓
Knowledge commit
```

This is analogous to source control for institutional knowledge.

## 6. Knowledge delta

```yaml
operation: ADD | UPDATE | SUPERSEDE | REFUTE | QUALIFY
entity_type: Claim
entity_id: C-001
changes:
  status: verified
provenance:
  evidence_ids:
    - E-001
    - E-002
reason: reproduced by EXP-014
confidence: high
```

## 7. Temporal semantics

Every mutable knowledge entity should support:

- valid time
- observation time
- transaction/commit time
- supersession relationship
- source version

This enables historical queries without rewriting history.

## 8. Contradiction engine

The contradiction engine should compare claims using:

- subject/entity
- predicate
- object/value
- valid time
- source type
- source authority
- assumptions
- dataset
- metric
- implementation version
- experimental conditions

Output categories:

```text
CONTRADICTS
QUALIFIES
SUPERSEDES
TIME-SCOPED
CONDITIONALLY-COMPATIBLE
UNRESOLVED
```

## 9. Evidence bundle

A research agent should receive a bounded evidence bundle rather than an unfiltered knowledge dump.

```yaml
question: ...
claims:
  - claim_id: C-001
    statement: ...
    confidence: medium
evidence:
  - evidence_id: E-001
    source: ...
    locator: ...
    relevance: 0.94
    authority: high
counter_evidence:
  - evidence_id: E-017
    reason: contradicts claim C-001
constraints:
  valid_at: 2024-10-01
```

## 10. Retrieval strategy

Use hybrid retrieval:

- lexical/exact search
- semantic retrieval
- graph traversal
- metadata filtering
- temporal filtering
- provenance filtering
- source authority ranking
- freshness ranking

The retrieval system should be replaceable. AlgoX must not depend on one vector database or embedding model.

## 11. Institutional-memory rule

The system should preserve:

> what was known, why it was believed, when it was believed, what contradicted it, what experiment changed confidence, and what decision followed.

## 12. Financial-system rule

Research knowledge about market infrastructure must carry effective dates whenever applicable. This includes:

- exchange rules
- broker API behavior
- fees
- taxes
- order types
- instrument metadata
- market hours
- regulatory requirements
- corporate-action handling

A current answer without a historical validity boundary is insufficient for serious financial research.

## 13. Non-goals

This architecture does not prescribe:

- Neo4j
- PostgreSQL
- a specific vector database
- a specific embedding model
- a specific LLM
- a specific agent framework

Those are implementation choices to be evaluated through AlgoX experiments and technology-radar decisions.

## 14. Architectural principle

> **Evidence is the source of institutional truth; the knowledge graph is the structured projection of that evidence.**
