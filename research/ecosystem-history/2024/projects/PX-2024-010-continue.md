# PX-2024-010 — Continue

**Repository:** https://github.com/continuedev/continue
**Historical category:** AI-development / developer tooling
**Domain:** AI-assisted software engineering

## 2024 signal
Continue represents the shift from simple code completion toward configurable AI development infrastructure embedded in the developer workflow. The important historical capability is not one model but an extensible boundary around models, repository context, code actions, and developer interaction.

## Capability observed
Developer AI can be structured as a configurable system where model choice, context retrieval, tools, and editor interaction are replaceable components.

## Architectural lesson
Developer tooling benefits from explicit extension points. Model providers, context sources, prompts/instructions, tools, and UI surfaces should not be inseparably coupled.

## AlgoX extraction
- Configurable model providers
- Repository/context integration
- Tool and workflow extensibility
- Developer-facing feedback loop
- Model/application separation
- Local and hosted model compatibility

## Relevance to AlgoX
Supports a plugin-style architecture for future AlgoX research capabilities. Source connectors, retrieval systems, model runtimes, experiment runners, and evaluators should be independently replaceable.

## Evidence
Project repository: https://github.com/continuedev/continue

**Evidence maturity:** C1
**Status:** RESEARCHED
