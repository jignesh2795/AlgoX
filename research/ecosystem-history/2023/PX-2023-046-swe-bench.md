# PX-2023-046 — SWE-bench

## Historical role
SWE-bench was released in October 2023 as an evaluation framework built from real GitHub issues and corresponding pull requests. The initial dataset contained 2,294 software-engineering problems across 12 Python repositories. The task requires an AI system to modify a real codebase and pass repository tests, making environment interaction and multi-file reasoning part of the evaluation rather than evaluating isolated code snippets. citeturn0academia48turn0search14

## 2023 finding
The original results were extremely low: the strongest reported model, Claude 2, solved 1.96% of the issues. This is direct evidence that strong language generation did not imply strong real-world software-engineering autonomy. citeturn0academia48

## Architecture / evaluation observations
- Real repositories are substantially harder than isolated coding prompts.
- Agent evaluation must include the execution environment, tests, repository context, and regression safety.
- A benchmark should preserve realistic task distribution rather than optimize for synthetic examples.
- Later SWE-agent work belongs to the 2024 research evolution and should not be backdated into the original 2023 record. citeturn0search14

## AlgoX extraction
**Capability:** repository-level engineering evaluation.

**Finding:** AI-assisted development requires environment-aware evaluation, not merely code-generation benchmarks.

**Decision:** ADOPT the principle; build AlgoX's coding-agent research around reproducible repository-level tasks and explicit pass/fail evidence.

## Evidence maturity
C2 — published benchmark methodology and reported results; AlgoX has not reproduced the benchmark.
