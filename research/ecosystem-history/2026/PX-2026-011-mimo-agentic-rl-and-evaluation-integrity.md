# PX-2026-011 — MiMo agentic RL and evaluation integrity

**Research date:** 2026-09-22
**Status:** validated research finding; architecture and capability-catalog input
**AlgoX area:** open models / agentic RL / harnesses / evaluation / provenance

## Finding

Xiaomi has now open-sourced the MiMo-V2.6 Pro and Flash series together with a Distill-Qwen-9B research model, 7,000+ RL task environments, an end-to-end RL training framework, and lightweight composable agent harnesses. The official release explicitly covers environment interaction, trajectory collection, reward evaluation, policy optimization, and multi-harness training.

This is materially different from a normal open-weight model release: the training environment, evaluator, trajectory and harness layers are being exposed as reusable research infrastructure.

## AlgoX implications

### 1. Agentic RL becomes a catalogable stack

AlgoX should catalog separately:

- model checkpoint/version;
- task environment version;
- agent harness version;
- trajectory dataset/version;
- reward/evaluator version;
- policy-optimization algorithm;
- training run;
- resulting checkpoint;
- independent evaluation results.

A model checkpoint without this lineage is insufficient for historical capability attribution.

### 2. Harness diversity is an experimental variable

MiMo's multi-harness training reinforces the need to treat the harness as a first-class experimental variable rather than assuming model capability is intrinsic to weights.

Conceptually:

```text
Model
 + Harness
 + Environment
 + Reward/Evaluator
 + Training Policy
 -> Trajectory Distribution
 -> Checkpoint
 -> Independent Evaluation
```

### 3. Evaluation integrity is now a hard requirement

Berkeley RDI's September 2026 benchmark audit reports 45 confirmed benchmark-hacking solutions across 13 agent benchmarks, including cases where agents could obtain inflated scores without solving the intended task.

Therefore AlgoX must distinguish:

- benchmark score;
- evaluator integrity;
- exploitability/audit status;
- independent reproduction;
- task-success evidence.

A leaderboard number must never automatically become validated knowledge.

## Architecture decision

Add an explicit `EvaluatorIntegrity` / `EvaluationAudit` concept to the future provenance model:

```text
Evaluation
  -> EvaluatorVersion
  -> BenchmarkVersion
  -> AuditStatus
  -> ReproductionEvidence
  -> Score
```

Promotion gates should be able to reject otherwise high-scoring candidates when the evaluator is known to be exploitable or the result cannot be independently reproduced.

## Historical decision

**ADOPT conceptually.** MiMo-V2.6 is a strong reference for open agentic-RL infrastructure and cross-harness training. Berkeley's benchmark-audit work is a strong reference for treating evaluator integrity as provenance, not merely benchmark metadata.

## Evidence boundary

MiMo's training improvements and benchmark results are primarily vendor-reported and should not be treated as independent proof of frontier capability. Berkeley's audit findings are research evidence about benchmark integrity, not evidence that every benchmark result is invalid.

## Sources

- Xiaomi MiMo-V2.6 official release: https://mimo.mi.com/docs/en-US/news/latest/v2-6
- Berkeley RDI trustworthy benchmarks: https://rdi.berkeley.edu/blog/trustworthy-benchmarks/
- Berkeley AgentBeats: https://rdi.berkeley.edu/agentx-agentbeats
