# 2023 → 2024 — Ecosystem Transition

**Status:** PROVISIONAL

## Central transition
2023 established the basic application patterns around foundation models: model abstraction, prompting, retrieval, memory, tools, agent loops, and AI-assisted coding.

2024 increasingly turned those patterns into infrastructure and controlled engineering systems.

```text
2023                                  2024
────────────────────────────────────────────────────────
LLM application                 →     model/runtime layer
Agent loop                      →     workflow + state + tools
RAG feature                     →     retrieval/data subsystem
Local model experiment          →     local inference platform
Code completion                 →     repository-level coding agent
Prompt-only evaluation         →     task + test + benchmark evaluation
Autonomous demo                 →     permissions + sandbox + verification
```

## Coding-agent transition
The most important software-engineering shift was from generating code snippets to operating on real repositories. SWE-bench formalized the task; SWE-agent added an engineered agent/environment interface; Aider demonstrated that pragmatic editing, static analysis, and test/lint feedback could produce strong results without requiring a highly autonomous architecture; OpenHands emphasized sandboxed execution and reproducible evaluation.

## AlgoX interpretation
The durable abstraction is not "autonomous agent". It is:

```text
MODEL
  ↓
CONTEXT
  ↓
TOOLS
  ↓
CONTROL POLICY / WORKFLOW
  ↓
EXECUTION ENVIRONMENT
  ↓
OBSERVATIONS
  ↓
VERIFICATION / EVALUATION
  ↓
EVIDENCE
```

This is directly applicable to AlgoX research agents.

## Strategic consequence
AlgoX should build its research architecture around replaceable capabilities and explicit evidence boundaries rather than one monolithic autonomous agent.

**Evidence maturity:** C2
