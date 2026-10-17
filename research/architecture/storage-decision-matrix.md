# AlgoX Storage Decision Matrix

**Status:** Architecture decision for research implementation
**Scope:** institutional memory, evidence, knowledge graph, semantic retrieval, source artifacts

## Executive decision

AlgoX should evolve as a **hybrid evidence-and-memory system**, but it should not start as a collection of specialized databases.

### Initial architecture

```text
                         ALGOX MEMORY
                              │
             ┌────────────────┼────────────────┐
             │                │                │
       OBJECT STORE      POSTGRESQL        DERIVED INDEXES
       raw artifacts     system of record   ┌──────┴──────┐
                                            │             │
                                        pgvector       full-text
                                            │
                                      semantic search
```

The knowledge graph is a **logical model from day one**, represented initially with relational entities and relationship tables. A dedicated graph database is a later projection if experiments demonstrate a real advantage.

## Decision matrix

| Technology | Authoritative data | Temporal/provenance | Semantic retrieval | Multi-hop graph | Operational complexity | AlgoX decision |
|---|---:|---:|---:|---:|---:|---|
| PostgreSQL | Excellent | Excellent | Good with extension | Good for bounded joins | Low | **ADOPT first** |
| pgvector | No | Inherits host DB | Excellent | Poor | Low | **ADOPT as derived index** |
| Dedicated graph DB | Good | Good to excellent | Varies | Excellent | Medium-high | **ASSESS later** |
| Vector DB | Poor | Usually application-managed | Excellent | Poor | Medium | **DO NOT use as source of truth** |
| Document DB | Good | Good | Good | Weak-medium | Medium | **ASSESS only if workload requires** |
| Search engine | No | Good | Excellent lexical/hybrid | Limited | Medium | **ASSESS later** |
| Object/blob store | Excellent for raw artifacts | Excellent via metadata | No | No | Low | **ADOPT** |
| Redis/cache | No | Weak as authority | Fast retrieval/cache | Weak | Low-medium | **LATER / derived** |

## What each layer stores

### Object store — source archive

Store immutable or content-addressed source artifacts:

- downloaded papers;
- repository snapshots where licensing permits;
- documentation snapshots;
- benchmark datasets/results;
- source captures;
- experiment artifacts;
- generated reports.

The database stores metadata and hashes, not the assumption that a web URL will remain unchanged.

### PostgreSQL — institutional system of record

Store:

- projects;
- sources;
- source versions;
- evidence;
- claims;
- findings;
- capabilities;
- algorithms;
- requirements;
- architecture/design records;
- experiments;
- benchmarks;
- decisions;
- ADRs;
- failures;
- dependencies;
- graph nodes and edges;
- temporal validity;
- provenance links;
- review status;
- confidence and maturity.

Use transactions and constraints to protect knowledge integrity.

### pgvector — semantic retrieval projection

Store embeddings for selected knowledge/evidence units:

- claims;
- findings;
- source chunks;
- experiment summaries;
- decisions;
- project/capability descriptions.

Embeddings are disposable. They must be rebuildable from authoritative records.

### Dedicated graph database — future projection

Introduce only when benchmark evidence shows that graph workloads justify it. Candidate workloads include:

- deep multi-hop dependency analysis;
- large-scale contradiction traversal;
- capability convergence analysis;
- temporal path queries;
- graph algorithms over large relationship networks.

The graph must remain reconstructable from authoritative knowledge/evidence records.

## Why PostgreSQL first

AlgoX is not primarily a graph traversal product or a semantic-search product. It is a **research governance and institutional-memory system**. Its most dangerous failure is losing provenance, temporal state, evidence integrity, or decision history.

A transactional relational system is therefore the safer initial authority. The graph and vector views should be projections optimized for particular reasoning/retrieval workloads.

## Non-negotiable rule

> Never let an embedding, vector hit, generated summary, or graph projection become the only surviving representation of a research fact.

Every derived memory item must be traceable to authoritative evidence.

## Evolution path

```text
Phase 1
PostgreSQL + object store
        ↓
Phase 2
PostgreSQL + pgvector
        ↓
Phase 3
retrieval fusion: lexical + semantic + metadata + temporal
        ↓
Phase 4
graph workload benchmark
        ↓
Phase 5 (only if justified)
PostgreSQL authority + dedicated graph projection
        ↓
Phase 6
specialized search/cache projections where measurements justify them
```

## Technology Radar

| Technology/pattern | Ring | Rationale |
|---|---|---|
| PostgreSQL | ADOPT | transactional authority and rich metadata |
| Object storage | ADOPT | durable source/artifact archive |
| pgvector | TRIAL | strong fit for early semantic retrieval without a second authority |
| Temporal/provenance data model | ADOPT | core institutional-memory requirement |
| Hybrid lexical + semantic retrieval | TRIAL | avoids single-retriever blind spots |
| Logical knowledge graph in relational tables | ADOPT | captures graph semantics without premature infrastructure |
| Dedicated graph database | ASSESS | valuable only after graph workload benchmark |
| Standalone vector database | HOLD | duplicates authority and adds operational surface |
| Document database as primary authority | HOLD | not required by current knowledge model |
| Search engine as primary authority | HOLD | retrieval optimization, not institutional truth |
| Redis as memory authority | HOLD | cache/working-state role, not durable knowledge |

## Acceptance criteria for a future graph database

Do not add one because the architecture diagram looks better. Add it only if an experiment demonstrates material improvement in at least one of:

- query latency;
- query complexity reduction;
- multi-hop retrieval quality;
- temporal traversal quality;
- graph analytics capability;
- operational cost at realistic scale.

The experiment must compare the same workloads against the PostgreSQL representation.
