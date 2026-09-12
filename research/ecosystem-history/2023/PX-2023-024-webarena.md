# PX-2023-024 — WebArena

## Historical role
WebArena was released in 2023 as a realistic, self-hostable environment for evaluating language-guided web agents. It uses functional websites across several domains and evaluates long-horizon task completion rather than isolated language-model outputs. The published results showed a large gap between agent and human performance, with the best reported GPT-4-based agent achieving 14.41% end-to-end success versus 78.24% for humans. citeturn0academia36turn0search0

## Architecture observations
- Agents need an executable environment, not only a prompt and answer pair.
- Evaluation should measure task completion and functional correctness.
- Reproducible environments are essential for comparing agent implementations.
- Long-horizon tasks expose failures that ordinary language benchmarks can hide.

## Research value
Very high for AlgoX's evaluation architecture and agent reliability research.

## AlgoX extraction
**Potential capability:** environment-backed agent evaluation harness.

**Lesson:** an agent's usefulness must be measured against realistic tasks, state changes, tools, and verification. Language-model benchmark scores alone are insufficient.

## Evidence
- WebArena paper, July 2023. citeturn0academia36
- Project repository documents its reproducible web environment and 2023 releases. citeturn0search0

## Decision status
ADOPT as a research principle: future AlgoX agent experiments should use reproducible environments and task-level success metrics where applicable.

## Evidence maturity
C2 — published benchmark and project evidence; AlgoX reproduction not yet performed.
