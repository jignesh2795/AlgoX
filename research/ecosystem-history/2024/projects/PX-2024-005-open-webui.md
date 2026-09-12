# PX-2024-005 — Open WebUI

**Repository:** https://github.com/open-webui/open-webui
**Historical category:** APPLICATION PLATFORM / integration layer
**Domain:** Self-hosted AI applications

## Historical signal
Open WebUI represents the maturation of local and provider-agnostic AI into a complete application platform rather than a single model interface.

## Capability observed
The platform combines multiple model providers, local runtimes, retrieval, tools, plugins, persistent state, authentication, observability, evaluation, and deployment options behind one application boundary.

## Architectural lesson
Once model infrastructure becomes interchangeable, the application layer increasingly becomes an orchestration and governance boundary: identity, permissions, tools, knowledge, persistence, observability, and user workflows matter as much as the model itself.

## AlgoX extraction
- Provider-agnostic model boundary
- Plugin/tool architecture
- Persistent application state
- Retrieval subsystem
- Authentication/RBAC
- Observability
- Evaluation and model comparison
- Horizontal deployment patterns

## Relevance to AlgoX
Strong precedent for treating knowledge, tools, evaluation, and governance as first-class platform capabilities rather than features buried inside an agent prompt.

## Evidence
Repository documentation: https://github.com/open-webui/open-webui

**Evidence maturity:** C1
**Status:** RESEARCHED
