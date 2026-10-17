# AlgoX Memory Model

Status: Proposed architecture

## Purpose

AlgoX memory is an institutional research memory, not a chat-history database. It must preserve evidence, claims, findings, experiments, decisions, and their evolution over time.

## Memory hierarchy

```text
WORKING MEMORY
  Current research question
  Active evidence bundle
  Current hypotheses
  Current task state

EPISODIC MEMORY
  Research sessions
  Experiments
  Benchmark runs
  Investigations
  Decisions made in context

SEMANTIC MEMORY
  Projects
  Algorithms
  Capabilities
  Architecture patterns
  Requirements
  Claims
  Findings
  Technologies
  Failures

PROCEDURAL MEMORY
  Research methods
  Evaluation procedures
  Engineering playbooks
  Decision policies
  Validation rules

SOURCE MEMORY
  Papers
  repositories
  documentation
  regulations
  exchange specifications
  articles
  datasets
  source versions

META-MEMORY
  confidence
  provenance
  freshness
  contradictions
  supersession
  reproducibility
  maintenance state
```

## Memory lifecycle

```text
OBSERVE
  ↓
CAPTURE EPISODE
  ↓
EXTRACT CANDIDATE MEMORY
  ↓
NORMALIZE
  ↓
RESOLVE ENTITY
  ↓
CHECK DUPLICATE / CONTRADICTION
  ↓
ATTACH PROVENANCE + TIME
  ↓
VALIDATE
  ↓
COMMIT
  ↓
INDEX / PROJECT
  ↓
RECALL
  ↓
USE IN RESEARCH
  ↓
EXPERIMENT / REVIEW
  ↓
UPDATE CONFIDENCE
```

## Memory types

| Type | What it stores | Authority |
|---|---|---|
| Source | Original external artifact and version | External evidence |
| Evidence | Precise support extracted from a source | Evidence layer |
| Claim | Atomic proposition | Derived |
| Finding | Interpreted research result | Research |
| Episode | What happened during research/experiment | Historical |
| Experiment | Controlled validation activity | Experimental |
| Result | Measured outcome | Experimental |
| Decision | Adopt/adapt/wrap/build/reject choice | Governance |
| Procedure | Repeatable way of doing research/engineering | Procedural |
| Capability | Reusable system ability | Architecture |
| Entity | Canonical project/technology/algorithm/etc. | Identity |

## Temporal model

Every important memory should distinguish:

- `valid_from`: when the fact became true
- `valid_to`: when the fact stopped being true
- `observed_at`: when AlgoX observed it
- `recorded_at`: when AlgoX stored it
- `superseded_at`: when a later memory replaced it
- `source_version`: version/commit/date of the supporting source

Never silently overwrite historical knowledge when a fact changes.

Example:

```text
Broker API supports order type X
valid_from: 2025-01-01
valid_to: 2026-04-30
observed_at: 2026-03-10

Broker API no longer supports order type X
valid_from: 2026-05-01
observed_at: 2026-05-03
```

## Confidence evolution

```text
CLAIM
  ↓
C0 unverified
  ↓ source inspection
C1 documented
  ↓ implementation inspection
C2 code-grounded
  ↓ reproduction
C3 reproduced
  ↓ benchmark
C4 benchmarked
  ↓ independent validation
C5 validated
  ↓ production evidence
C6 production-supported
```

Confidence is never increased merely because an LLM generated a plausible explanation.

## Consolidation

AlgoX should have a background consolidation process, inspired by the strongest patterns found in agent-memory systems: hierarchical memory, explicit memory editing, episodic learning, temporal knowledge, and periodic consolidation. MemGPT/Letta separates always-available working memory from external archival memory and has explored asynchronous memory-consolidation processes. citeturn1search0turn1search3 LangMem separately distinguishes semantic, episodic, and procedural memory. citeturn1search6turn1search8

Consolidation jobs should:

1. detect duplicate memories;
2. resolve aliases/entities;
3. identify contradictions;
4. mark obsolete facts as superseded rather than deleting history;
5. merge compatible claims;
6. extract durable findings from episodes;
7. update confidence from experiment results;
8. identify capability gaps;
9. propose decisions;
10. never commit high-impact decisions without required evidence.

## Recall

Recall is not one search.

```text
Query
 ↓
Query classification
 ↓
Temporal constraints
 ↓
Scope / capability filters
 ↓
Lexical retrieval ─┐
Semantic retrieval ─┼→ candidate memories
Graph retrieval ───┘
 ↓
Evidence / authority ranking
 ↓
Contradiction check
 ↓
Temporal validity check
 ↓
Bounded evidence bundle
```

pgvector supports exact and approximate vector search and can be combined with PostgreSQL full-text search for hybrid retrieval. citeturn0search8

## Memory governance

An LLM may propose a memory delta, but the storage layer owns truth.

```yaml
operation: ADD | UPDATE | SUPERSEDE | REFUTE | QUALIFY
entity_type: Claim
entity_id: C-001
changes: {}
provenance:
  evidence_ids: []
temporal: {}
confidence: {}
reason: ""
```

Before commit:

- schema validation
- provenance validation
- identity resolution
- temporal validation
- contradiction detection
- license/compliance checks where applicable
- confidence policy
- approval policy

## Design principle

> **Memory is not what the model remembers. Memory is what AlgoX can recover with provenance, temporal validity, confidence, and evidence.**
