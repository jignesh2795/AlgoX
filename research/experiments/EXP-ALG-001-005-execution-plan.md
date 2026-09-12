# EXP-ALG-001 → EXP-ALG-005: Local Validation Execution Plan

## Purpose

Move AlgoX from externally informed architecture decisions to locally measured evidence. These experiments are deliberately runnable without GitHub Actions.

## EXP-ALG-001 — Persistence workload

**Question:** Does the current logical memory model justify PostgreSQL as the first durable store?

Measure:
- insert/update throughput
- retrieval latency
- relationship traversal latency
- batch ingestion
- concurrent readers/writers
- restart/reload correctness

Baselines:
- current InMemoryStore
- minimal SQLite/local relational prototype if available
- PostgreSQL only when a local instance is available

Gate:
- select persistence only from measured workload requirements.

## EXP-ALG-002 — Evidence retrieval

**Question:** Does retrieval return the evidence needed to support a decision, rather than merely semantically similar text?

Dataset:
- existing memory benchmark dataset
- research-chain fixtures
- contradictory/temporal fixtures

Metrics:
- evidence recall
- support completeness
- false-support rate
- contradiction exposure
- ranking latency

Gate:
- retrieval is a candidate generator; no result becomes institutional truth without evidence validation.

## EXP-ALG-003 — Memory usefulness / ablation

**Question:** Does institutional memory measurably improve research-agent decisions?

Compare:
1. no memory
2. semantic retrieval only
3. graph retrieval only
4. evidence + graph + temporal metadata

Metrics:
- decision accuracy
- unsupported-claim rate
- repeated-work rate
- context size/token cost
- retrieval latency

Gate:
- retain a memory mechanism only when it produces measurable improvement on the benchmark.

## EXP-ALG-004 — Durable learning governance

**Question:** Can an agent learn from experience without silently corrupting institutional memory?

Test:
- AgentTrace → Evaluation → Experience → Consolidation Proposal
- proposal rejection
- proposal approval
- evidence attachment
- audit event creation
- disputed/refuted knowledge
- supersession

Gate:
- every truth-changing durable update is auditable and evidence-backed.

## EXP-ALG-005 — Research-agent reliability

**Question:** Can AlgoX's research loop reproduce an experiment and correctly distinguish successful execution from trustworthy evidence?

Pipeline:
- source/paper
- hypothesis
- experiment plan
- implementation
- sandbox execution
- result capture
- verification
- finding proposal
- governance

Metrics:
- execution success
- reproduction correctness
- unsupported-result rate
- verifier catch rate
- retry success
- human intervention count

External rationale:
Current research-agent benchmarks show sharp degradation as autonomous implementation becomes harder, and multi-trial execution can substantially outperform single-shot execution; this supports explicit verification and retry rather than trusting first-pass output. See AutoExperiment and RExBench.

## Local execution policy

Run locally with:

```bash
python tools/local_verify.py
python tools/local_verify.py --pytest
```

Experiment-specific scripts should remain ordinary local Python/pytest programs. GitHub Actions is not required.

## Evidence policy

Do not mark an experiment `PASSED` merely because code runs. Record:
- execution environment
- inputs
- outputs
- expected result
- observed result
- reproducibility
- evidence IDs
- anomalies
- conclusion
- decision

## Status

Plan only. No experiment is claimed to have passed until it has actually been executed and its result recorded.
