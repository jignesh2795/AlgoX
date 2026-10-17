# PX-2023-056 — CrewAI

Status: DISCOVERY / INITIAL RESEARCH
Year: 2023
Repository: crewAIInc/crewAI

## Why it belongs in the 2023 corpus

CrewAI is a significant 2023 multi-agent framework centered on role-based agents,
tasks and crews. It provides a useful counterpoint to AutoGen, CAMEL, MetaGPT and
ChatDev because its abstraction emphasizes explicit roles and workflow/task
decomposition.

## Research targets

- role/task/crew abstractions
- sequential and hierarchical execution
- tool integration
- delegation
- memory
- process control
- agent boundaries
- observability
- failure handling
- human-in-the-loop controls

## AlgoX questions

1. When does role separation improve reliability versus merely adding complexity?
2. Which workflow semantics are deterministic enough to benchmark?
3. How are agent outputs validated before downstream use?
4. What can be reused as research orchestration rather than execution authority?

## Initial classification

Agent Architecture; Workflow Orchestration; AI Engineering.

Evidence maturity: C1 — initial repository discovery; detailed historical extraction pending.
Decision: ASSESS.
