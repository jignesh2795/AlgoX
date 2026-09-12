# AlgoX Capability Gaps and Experiment Queue v1

## Purpose

Turn the 2023-2025 capability matrix into a bounded implementation and research queue. The goal is not to build every capability immediately; it is to identify which uncertainties must be experimentally resolved before durable architecture decisions.

## Highest-priority gaps

### G1 — Evidence-backed persistence
**Question:** Is the current in-memory institutional-memory model sufficient for realistic AlgoX research workloads, and what persistence boundary is actually required?

**Gate:** persistence workload benchmark covering append/read, evidence lookup, temporal reconstruction, graph traversal, audit history, concurrent reads, and rebuild-from-evidence.

**Candidate:** PostgreSQL + object storage first.

**Do not decide yet:** pgvector, dedicated graph database, search engine, Redis.

### G2 — Retrieval quality
**Question:** When does semantic retrieval improve evidence discovery versus exact/metadata/graph retrieval?

**Gate:** benchmark on historical AlgoX research questions with recall, precision, temporal correctness, source diversity, latency and token cost.

**Decision:** semantic retrieval remains a candidate generator, never an authority.

### G3 — Research-agent reliability
**Question:** Can an agent reliably execute a research task without turning unsupported output into institutional knowledge?

**Gate:** task → trace → artifact → experiment → result → evidence → governance test, including intentional failure cases.

**Minimum requirement:** every durable claim must retain provenance and review state.

### G4 — Single-agent versus multi-agent
**Question:** When does decomposition into specialized agents outperform one stronger agent after coordination cost and failure propagation are included?

**Gate:** same task suite, same model/tool budget, single-agent baseline versus multi-agent candidates; measure correctness, latency, cost, recovery and trace complexity.

**Default:** single-agent baseline first.

### G5 — Memory usefulness
**Question:** Does institutional memory improve future research decisions rather than merely increasing retrieved context?

**Gate:** repeated research tasks with and without memory; measure decision quality, contradiction detection, evidence reuse, token cost and stale-memory errors.

### G6 — Experiment reproducibility
**Question:** Can AlgoX reproduce an experiment from stored evidence, code/version metadata, parameters and dataset references?

**Gate:** clean-environment replay with deterministic fixtures and explicit missing-input failures.

### G7 — Financial execution boundary
**Question:** What should be learned from financial execution systems before QuantumTrade implementation?

**Gate:** broker abstraction, order lifecycle, partial fills, disconnect/recovery, reconciliation, instrument identity, F&O lifecycle and deterministic replay fixtures.

**Boundary:** these are downstream trading-platform capabilities; AlgoX researches and validates them but does not become the OMS/EMS.

## Experiment queue

| ID | Experiment | Priority | Depends on |
|---|---|---|---|
| EXP-ALG-001 | Persistence workload benchmark | P0 | existing memory store |
| EXP-ALG-002 | Evidence retrieval benchmark | P0 | memory benchmark dataset |
| EXP-ALG-003 | Memory usefulness / ablation | P0 | retrieval + research fixtures |
| EXP-ALG-004 | Durable learning governance gate | P0 | consolidation + audit |
| EXP-ALG-005 | Research-agent reliability benchmark | P0 | trace/evaluation framework |
| EXP-ALG-006 | Single vs multi-agent cost/quality benchmark | P1 | agent harness |
| EXP-ALG-007 | Reproducible experiment replay | P1 | experiment registry |
| EXP-ALG-008 | Temporal contradiction benchmark | P1 | temporal evidence model |
| EXP-ALG-009 | Evidence-to-decision reconstruction | P1 | research graph |
| EXP-ALG-010 | Indian execution semantics fixture suite | P1 | downstream trading research |

## Exit criteria for the research phase

The ecosystem research phase is considered sufficiently mature when:

1. Major 2023-2025 capability families have evidence records.
2. Historical and current evidence are separated.
3. Contradictions and uncertainty are recorded rather than silently resolved.
4. Each high-value capability has an explicit decision status.
5. High-impact unknowns have experiments rather than additional open-ended browsing.
6. The AlgoX memory/research loop can preserve provenance from source to decision.
7. Downstream trading architecture requirements can be expressed as capability requests against this catalog.

## Principle

When a question can now be answered by an experiment on AlgoX itself, stop expanding the literature search and run the experiment locally. Research should transition from discovery to evidence generation.
