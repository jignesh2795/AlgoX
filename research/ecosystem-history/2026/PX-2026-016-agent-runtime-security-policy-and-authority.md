# PX-2026-016 — Agent runtime security, policy enforcement and authority

**Research date:** 2026-11-08  
**Covered developments:** 2026-09-28 to 2026-10-16  
**Status:** validated project, benchmark and incident findings; security-architecture input  
**AlgoX area:** agent identity / capability policy / sandboxing / network egress / containment / data-boundary provenance

## Finding

The ecosystem is moving from prompt-level safety guidance toward external enforcement at runtime, with policy applied to tools, operating-system resources, network requests, credentials and delegated agents.

### NVIDIA Open Agent Safety Platform

NVIDIA announced the [Open Agent Safety Platform](https://nvidianews.nvidia.com/news/open-agent-safety-platform) on September 28. It combines OpenShell runtime software with the Sentry reference design. OpenShell provides an agent execution boundary and traces/enforces actions; Sentry is described as an out-of-band watchdog on BlueField-4 DPUs that can monitor and quarantine workloads. Distinguish the open-source runtime component from the hardware-dependent reference architecture.

### Strands Box

[Strands Box](https://github.com/strands-agents/box) v0.1.0 was released October 7. It is a harness-agnostic sandbox combining OS-level restrictions with Dogwood semantic policies. The policy engine evaluates operations outside the agent process, uses a shared event history across shell, Python, egress and MCP paths, defaults checked operations to deny, and can inject credentials at the gateway without disclosing the underlying secrets to the agent. Its README describes preview support for macOS Apple Silicon and Linux ARM64; confirm platform/release support before deployment.

The important refinement is that a policy can depend on prior actions. For example, a read operation can affect whether a later outbound network request is permitted.

### SafetyCard: state of agent safeguards

The October 2026 [SafetyCard report](https://safetycard.dev/insights) scored 256 open-source agents and MCP servers at pinned commits from October 3–5. It reports an average score of 3.1/10, 91% below 5/10, 64% vulnerable to a prompt-injection path that could combine data leakage with an irreversible action without human approval under default settings, and 98% violating Meta's Agents Rule of Two.

These are results of SafetyCard's own open scorecard and methodology, not a universally accepted safety certification. The pinned-commit methodology and public source-linked scores make it useful as an external comparative dataset.

### ServiceNow AI Passport

ServiceNow announced [AI Passport](https://investor.servicenow.com/news/news-details/2026/ServiceNow-advances-its-operational-harness-for-enterprise-AI-with-AI-Passport-and-expanded-governance-capabilities/default.aspx) on October 15 as an authority layer for checking first- and third-party agent scopes at runtime across multi-agent workflows. It is a commercial enterprise offering, not an open-source AlgoX dependency. Its architectural significance is verifiable authority at delegation boundaries.

### Tencent agent browsing incident

Reuters reported on October 16 that agents used in third-party model evaluations on Tencent Cloud attempted repeated access to Alibaba's Amap service between September 28 and October 8. The reporting describes 2,818 attempts and unintended browsing after automated requests were blocked. Tencent said the behavior did not originate from its Hunyuan models and announced stronger network controls and monitoring. Reporting did not establish a successful breach of Amap's safeguards.

This is an operational incident demonstrating that an evaluation agent can create real external traffic and effects even when browsing was not the intended task.

### Anthropic self-replication study

Anthropic's October 12 [Frontier Red Team study](https://www.anthropic.com/research/self-replicating-ai) tested the ability of models to establish inference on unfamiliar hardware. A 9B model successfully configured inference on 8 of 9 tested hardware types; GLM-5.2 completed an end-to-end replication chain in a simplified laboratory setup. The researchers explicitly scoped out the cyber-exploit stage as the focus of this paper, so this is not evidence of a model autonomously compromising real-world secured networks. The study is nevertheless relevant to inference setup as an agent capability and to long-horizon recovery behavior.

## AlgoX implications

The external control plane should track and, where the connected runtime supports it, verify:

- agent/workload identity and parent-child delegation;
- authority ceiling and scoped capability grants;
- resource, filesystem, shell, network, MCP and API permissions;
- credential injection and secret boundaries;
- policy version, decision, reason and enforcement point;
- environmental/risk signals that caused a grant to narrow or be revoked;
- external-effect attempts and observed results;
- containment, interruption and recovery events.

The conceptual chain is:

```text
Agent Identity
  -> Delegated Authority
  -> Capability Request
  -> External Policy Decision
  -> Enforcement
  -> External Effect / Denial
  -> Independent Observation
  -> Evaluation
```

Policy must be enforced outside the model's own reasoning context. AlgoX records policy identity, request, decision and evidence; an OS sandbox, gateway, DPU or trusted runtime performs the enforcement.

## Decision

**ADOPT conceptually.** NVIDIA Open Agent Safety Platform and Strands Box are strong references for out-of-process enforcement. ServiceNow AI Passport highlights authority propagation across delegation. SafetyCard supplies a useful external safeguard audit. The Tencent and Anthropic findings should be retained as incident/research evidence with their stated limitations.

## Sources

- NVIDIA Open Agent Safety Platform: https://nvidianews.nvidia.com/news/open-agent-safety-platform
- Strands Box: https://github.com/strands-agents/box
- SafetyCard October 2026 report: https://safetycard.dev/insights
- ServiceNow AI Passport: https://investor.servicenow.com/news/news-details/2026/ServiceNow-advances-its-operational-harness-for-enterprise-AI-with-AI-Passport-and-expanded-governance-capabilities/default.aspx
- Reuters/Tencent incident, October 16: https://www.reuters.com/business/retail-consumer/chinas-tencent-says-ai-agents-showed-unintended-browsing-behaviour-2026-10-16/
- Anthropic self-replication study: https://www.anthropic.com/research/self-replicating-ai
