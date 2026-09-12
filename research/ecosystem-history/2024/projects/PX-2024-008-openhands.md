# PX-2024-008 — OpenHands

**Repository:** https://github.com/All-Hands-AI/OpenHands
**Historical category:** AI-development / software-engineering platform
**Domain:** Agentic software engineering

## 2024 signal
OpenHands (originally OpenDevin) pushed software-engineering agents toward executable, sandboxed environments. In 2024 its evaluation work emphasized reproducible execution and isolated runtimes for agents that write, run, and test code.

## Capability observed
The runtime separates agent actions from environment observations and executes risky operations inside a sandbox. This enables arbitrary developer-like actions while protecting the host environment.

## Architectural lesson
For agents that can execute code, the runtime is a security and reliability boundary. The agent loop should not have unrestricted access to the host simply because the model needs developer capabilities.

## AlgoX extraction
- Sandboxed execution
- Agent action/observation protocol
- Runtime isolation
- Reproducible evaluation environments
- Code execution and testing
- Agent evaluation infrastructure
- Separation of policy from execution environment

## Relevance to AlgoX
High relevance for future research agents that may execute experiments, clone repositories, run tests, build artifacts, or reproduce claims. Experiment execution should be isolated from the primary research environment.

## Evidence
OpenHands 2024 evaluation and runtime description: https://www.openhands.dev/blog/evaluation-of-llms-as-coding-agents-on-swe-bench-at-30x-speed
OpenHands repository: https://github.com/All-Hands-AI/OpenHands

**Evidence maturity:** C2
**Status:** RESEARCHED
