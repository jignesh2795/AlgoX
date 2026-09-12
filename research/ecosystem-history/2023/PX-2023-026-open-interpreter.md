# PX-2023-026 — Open Interpreter

## Historical role
Open Interpreter emerged in 2023 as a local natural-language interface that allowed language models to execute code on a user's computer. Its architecture exposed an execution primitive and included explicit user approval before running code. citeturn1search1turn1search7

## Architecture observations
- Tool use became actual environment execution rather than text-only API simulation.
- A coding agent needs an execution boundary, not merely model output.
- Approval/permission is part of agent architecture, not an afterthought.
- Local execution changes the security model because the agent can affect files, processes, network resources, and system state.

## Research value
Very high for AI-assisted engineering, agent security, sandboxing, and human-in-the-loop design.

## AlgoX extraction
**Potential capability:** controlled execution environment with explicit permissions.

**Lesson:** agent autonomy must be bounded by capabilities, approvals, isolation, and auditability. Execution should never be treated as equivalent to reasoning.

## Evidence
- Historical Open Interpreter repository documentation describes local code execution and user confirmation. citeturn1search1turn1search7

## Decision status
ADOPT as an architectural principle: execution capabilities require explicit policy and safety boundaries. Evaluate implementation choices separately.

## Evidence maturity
C2 — project documentation; no AlgoX reproduction or security benchmark yet.
