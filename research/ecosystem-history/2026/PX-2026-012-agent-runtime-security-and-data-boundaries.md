# PX-2026-012 — Agent runtime security and data-boundary controls

**Research date:** 2026-09-23
**Status:** validated ecosystem finding; architecture/security input
**AlgoX area:** agent runtime / security / provenance / capability policy / coding-agent architecture

## Finding

Two developments materially strengthen the case for an external control plane around agent execution:

- **Prismor** is an open-source, self-hosted runtime control plane that intercepts agent tool calls, supports observe/warn/block/HITL policies, MCP gateway enforcement, network controls, secret protection, supply-chain checks and local audit/session records. Its current repository describes support for Claude Code, Codex, LangChain and many other agent harnesses. GitHub currently reports 363 stars. https://github.com/PrismorSec/prismor
- **Z.ai ZCode** published its coding-agent source after a September 2026 incident in which the Codebase Indexing / Repo Wiki workflow was reported to upload local repository data without clear user consent. Z.ai disabled the affected workflow and released ZCode 3.14.0 with the remediation; subsequent reporting notes that the public repository history is limited, so source publication does not by itself establish the full historical behavior. https://github.com/zai-org/ZCode

## AlgoX implications

### 1. Capability enforcement belongs outside the model

The runtime boundary should be explicit:

```text
Agent / Harness
    -> Capability Request
    -> External Policy Engine
    -> Allow / Warn / Human Approval / Block
    -> Tool / Network / Filesystem Effect
    -> Provenance Event
```

AlgoX should record the policy decision and effective capability set, but should not assume that its own model reasoning is the enforcement mechanism.

### 2. Data movement is an external effect

Repository indexing, retrieval uploads, telemetry, model-provider traffic and MCP responses should be represented as externally observable effects with provenance.

```text
Source Data
  -> Transformation / Packaging
  -> Destination
  -> Authorization Basis
  -> Policy Decision
  -> Effect
  -> Evidence / Audit Record
```

A statement such as “local repository” is therefore insufficient. The system must know whether data remained local, crossed a trust boundary, or was sent to a provider.

### 3. Agent identity and sub-agent visibility are first-class

A control plane must preserve parent/child agent identity, session identity, capability identity and policy identity so that spawned agents cannot become invisible provenance gaps.

### 4. Security evidence must be independently auditable

Local dashboards and runtime logs are useful evidence, but a runtime's own claim that data was deleted or an action was safe should not automatically become validated knowledge. AlgoX should distinguish:

- runtime assertion;
- observable telemetry;
- independent verification;
- validated claim.

## Architecture decision

**ADOPT conceptually.** AlgoX should remain runtime-agnostic and provide provenance/evaluation/promotion semantics above an external enforcement boundary. Prismor is a useful reference implementation for that boundary, while the ZCode incident is a concrete historical case for why data-boundary provenance must be explicit.

## Historical significance

This marks a transition from generic “agent security” toward **runtime policy + data-boundary provenance + independent verification** as a normal architectural layer of agent systems.

## Sources

- Prismor GitHub: https://github.com/PrismorSec/prismor
- Prismor documentation: https://www.prismor.dev/docs/prismor
- ZCode repository: https://github.com/zai-org/ZCode
- The Next Web, September 22, 2026: Z.ai open-sources ZCode after repository-upload incident.
- Reuters/other reporting on the ZCode incident and remediation.
