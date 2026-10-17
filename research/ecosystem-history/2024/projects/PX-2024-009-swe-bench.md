# PX-2024-009 — SWE-bench

**Project:** https://www.swebench.com/
**Historical category:** benchmark / evaluation infrastructure
**Domain:** AI-assisted software engineering

## 2024 signal
SWE-bench established repository-level software engineering as a concrete evaluation problem: given a real issue and a real codebase, an agent must produce a patch that resolves the issue without breaking unrelated functionality. In 2024 the ecosystem added SWE-bench Lite, containerized evaluation, and SWE-bench Verified.

## Capability observed
The benchmark evaluates complete task outcomes rather than judging generated code in isolation. It uses failing tests to establish whether the requested behavior was fixed and passing regression tests to detect collateral breakage.

## Architectural lesson
A research system needs task-level evaluation, not only component-level metrics. The evaluator must define the environment, baseline, success criteria, regression criteria, and reproducibility conditions.

## AlgoX extraction
- Real-world task benchmark
- Acceptance-test evaluation
- Regression protection
- Containerized/reproducible evaluation
- Standardized task instances
- Baseline comparison
- Agent evaluation harness

## Relevance to AlgoX
This is a foundational pattern for AlgoX experiments. Research claims should be converted into explicit hypotheses, reproducible environments, success/failure criteria, and benchmarkable outcomes wherever feasible.

## Evidence
ICLR 2024 SWE-bench paper: https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html
SWE-bench history: https://www.swebench.com/original.html
SWE-bench Verified: https://openai.com/index/introducing-swe-bench-verified/

**Evidence maturity:** C2
**Status:** RESEARCHED
