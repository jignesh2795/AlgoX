# EXP-MEM-0003 — Knowledge Governance Gate

Status: **IMPLEMENTED — NOT EXECUTED IN THIS SESSION**

## Hypothesis

A deterministic governance layer can prevent unsupported model-generated knowledge from entering durable institutional memory.

## Acceptance criteria

- unsupported ADD is rejected
- unknown evidence is rejected
- duplicate ADD is rejected
- known evidence can pass review
- explicit approval identity is required for entity commit
- historical review reports evidence observed after the requested time

## Architectural consequence

The LLM remains a proposer/reasoner, not the authority. Durable memory is admitted through structured policy and provenance checks.

## Next

Add contradiction-aware policy decisions and an append-only approval/audit event model before connecting this gate to PostgreSQL transactions.
