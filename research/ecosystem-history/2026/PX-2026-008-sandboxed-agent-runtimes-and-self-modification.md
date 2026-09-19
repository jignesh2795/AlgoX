# PX-2026-008 — Sandboxed agent runtimes and self-modifying coding agents

**Research date:** 2026-09-19
**Status:** validated research finding; architecture/security/evaluation input
**AlgoX area:** agent runtime / capabilities / effect provenance / continual improvement

## Finding

Two developments materially sharpen the boundary between an agent harness and the control plane beneath it.

### NVIDIA OpenShell

OpenShell is an open-source runtime for autonomous agents that moves security controls into the execution environment rather than relying on the model or application layer. Its current design uses sandboxed containers, declarative YAML policies, policy-enforced egress routing, provider-managed credentials, and SDKs for Python, TypeScript, Go and Rust. It supports multiple coding/agent runtimes and experimental GPU passthrough for local inference workloads.

Repository: https://github.com/NVIDIA/OpenShell

**AlgoX implication:** capability authorization and effect provenance should remain external to the model/harness. AlgoX should record the policy and capability context under which an execution occurred, while allowing OpenShell-like runtimes to enforce the actual boundary.

### Ouroboros

Ouroboros is an open-source self-developing coding/agent system whose reviewed commits can change its tools, prompts, context assembly, architecture and dependencies. Its technical report describes both recursive evolution and experience-driven core evolution, with frozen benchmark snapshots separated from a long-running live lineage.

Repository: https://github.com/razzant/ouroboros
Report: https://arxiv.org/abs/2608.08311

**AlgoX implication:** agent self-modification requires stronger lineage semantics. An AgentVersion cannot be identified only by model/prompt/skill versions; the runtime implementation, dependency set, capability policy and parent lineage must also be attributable. Benchmark results must remain attached to immutable snapshots even while a live agent continues evolving.

## Combined architecture lesson

The control-plane boundary should now be explicit:

```text
Agent / Harness
      |
      v
AgentVersion + Lineage
      |
      v
Capability Policy -----> External Sandbox / Runtime
      |                         |
      |                         v
      |                    External Effect
      |                         |
      +-----------> Execution / Provenance <-----+
                            |
                            v
                         Evidence
                            |
                            v
                       Evaluation
                            |
                            v
                    Promotion / Reject
```

AlgoX should not implement another sandbox runtime. It should capture the identity, policy, execution receipt and resulting effects from compatible runtimes.

## Evaluation consequence

Self-modifying agents strengthen the need for two distinct evaluation modes:

1. **Frozen snapshot evaluation** — reproducible benchmark evidence for a precise agent version.
2. **Live lineage evaluation** — longitudinal evidence showing how an evolving agent changes capability, cost, regressions and safety over time.

A live agent's current score must never silently overwrite the evidence belonging to an earlier version.

## Decision

**ADOPT as an architecture constraint; do not copy implementation.** OpenShell is a reference for externalized runtime enforcement. Ouroboros is a reference for persistent self-modifying agent lineage. AlgoX should remain the provenance/evaluation/control plane connecting such runtimes rather than becoming the runtime itself.

## Evidence maturity

C2 — primary project repositories and published technical report; AlgoX integration not yet implemented.
