# PX-2023-018 — AutoGen

## Historical role
AutoGen was introduced publicly in 2023 as an open-source framework for building LLM applications from multiple conversable agents. The 2023 paper describes agents combining LLMs, human inputs, and tools, with programmable interaction patterns using natural language and code. citeturn1academia73turn1search8

## Architecture observations
- Agent behavior is represented as configurable conversation patterns.
- Human input and tools can participate in the same interaction model as LLM agents.
- Multi-agent coordination is treated as infrastructure rather than hard-coded into one application.
- The abstraction makes interaction topology a design variable: agents can be composed differently for different tasks.

## Research value
High for orchestration, human-in-the-loop boundaries, tool integration, and comparing conversational coordination against direct workflow/state-machine execution.

## AlgoX extraction
**Potential capability:** configurable agent interaction graphs.

**Lesson:** orchestration should expose interaction policy explicitly. A system should be able to constrain turns, tools, permissions, termination, and human intervention instead of relying on an unconstrained conversation loop.

## Evidence
- AutoGen 2023 paper and abstract. citeturn1academia73
- AutoGen research documentation identifies the work as an arXiv 2023 framework. citeturn1search8

## Decision status
ASSESS — useful as a historical architecture pattern; later versions must be evaluated separately rather than back-projected into 2023.

## Evidence maturity
C2 — published research and project documentation; no AlgoX reproduction yet.
