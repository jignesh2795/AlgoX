# PX-2026-013 — Agent evaluation infrastructure and long-horizon benchmarks

**Research date:** 2026-11-08  
**Covered releases:** 2026-09-17 to 2026-09-30  
**Status:** validated ecosystem findings; evaluation-architecture input  
**AlgoX area:** evaluation / benchmarks / harnesses / environments / reproducibility

## Finding

Three developments make evaluation infrastructure more composable and more representative of sustained engineering work.

### AgentCompass

[AgentCompass](https://github.com/open-compass/AgentCompass) is an open-source evaluation framework that deliberately separates **Model, Benchmark, Harness, and Environment** behind reusable interfaces. Its execution pipeline includes task scheduling, isolated execution, evaluation, persistence, trajectory analysis, failure analysis, retries and resumable runs. The project announced its first PyPI release, v1.0.0, on September 30, 2026; its repository describes 30+ benchmarks and 10+ harness integrations.

This is a strong reference implementation for AlgoX's separation of evaluation subject from the model that happens to power it.

### Android Bench 2.0

Google's [Android Bench 2.0 announcement](https://developer.android.com/blog/posts/android-bench-2-0-pushing-the-frontier-with-challenging-long-horizon-tasks) on September 17, 2026 introduced long-horizon tasks intended to require days or up to a week of engineering work, together with agentic evaluation. The benchmark methodology is aligned with Harbor. This moves evaluation beyond localized issue completion toward complex, ambiguous, multi-stage work.

### NVIDIA SWE-Serve

[NVIDIA SWE-Serve](https://github.com/NVIDIA/swe-serve) packages 53 production inference-engineering tasks derived from merged SGLang pull requests. Tasks cover model integration, public APIs, cache systems and GPU kernels. Each task has a behavior verifier, isolated from the agent, and provenance linking it to upstream engineering work.

SWE-Serve evaluates whether an agent can perform real inference-engineering work, not merely call an inference server or answer questions about it.

## AlgoX implications

1. Treat `Model`, `Harness`, `BenchmarkVersion`, `EnvironmentVersion`, and `EvaluatorVersion` as separately versioned entities.
2. Persist the exact task set, execution environment, verifier, harness configuration, runtime limits, retries and raw trajectories for each run.
3. Support long-running and resumable evaluations; preserve checkpoints and interrupted/failed attempts instead of reporting only terminal scores.
4. Distinguish domain-specific engineering benchmarks (Android, inference-serving, repository repair) rather than collapsing them into one generic agent score.
5. Keep verifier isolation explicit. The agent must not be able to inspect private tests, reference solutions or evaluator secrets.

## Decision

**ADOPT conceptually.** AgentCompass is the most direct external reference for a composable evaluation control plane. Android Bench 2.0 and SWE-Serve demonstrate why benchmark task duration, domain, verifier and environment must be explicit. Do not implement a competing benchmark runner before testing the minimal interfaces against existing frameworks.

## Evidence boundary

Project capabilities and release metadata are verified from project/maintainer sources. Benchmark scores from any individual model or provider remain configuration-specific and should not be promoted without independent reproduction.

## Sources

- AgentCompass: https://github.com/open-compass/AgentCompass
- Android Bench 2.0: https://developer.android.com/blog/posts/android-bench-2-0-pushing-the-frontier-with-challenging-long-horizon-tasks
- SWE-Serve: https://research.nvidia.com/benchmarks/swe-serve
- SWE-Serve task repository: https://github.com/NVIDIA/swe-serve
