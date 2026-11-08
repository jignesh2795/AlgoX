# PX-2026-019 — Coding-agent workflows and the governed software factory

**Research date:** 2026-11-08  
**Covered developments:** 2026-06-11 to 2026-10-31  
**Status:** validated project/product findings; workflow and software-architecture input  
**AlgoX area:** coding-agent orchestration / task lifecycle / identity / approvals / artifact provenance / enterprise workflow

## Finding

The ecosystem is extending coding agents from interactive sessions into persistent work systems that listen for authorized tasks, coordinate changes through repository and CI workflows, and preserve an organizational record.

### DeepSeek dsh-superagent prototype

[DeepSeek's dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) was published October 31, 2026. It is a MIT-licensed research prototype for a proactive coding agent scoped to one GitHub repository and packaged as a DeepSeek Harness bundle. Authorized requests create work items; the agent operates in its own session and directory, then reports back through the original channel, potentially with a pull request. It has explicit documentation for domain model, authorization, execution, deployment and operator interaction.

The repository is explicit that it is **reference/research code, not an official DeepSeek product**, and is not identical to the company's internal system or all concepts in the accompanying design article. Treat it as an architecture specimen, not production-ready software.

### GitHub Agentic Workflows

GitHub announced [Agentic Workflows public preview](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/) on June 11. It allows reasoning-based maintenance tasks such as issue triage, CI failure analysis and documentation updates to be described in Markdown and compiled into standard GitHub Actions workflows. The workflows inherit runner groups and policy constraints from Actions.

The key architectural property is that agent-generated work can remain within an existing CI/workflow governance envelope.

### GitLab Governed Software Factory

GitLab's October 6 [Governed Software Factory announcement](https://ir.gitlab.com/news/news-details/2026/GitLab-Announces-the-Foundation-for-the-Governed-Software-Factory/default.aspx) describes a connected workflow for orchestrating, assembling, securing and optimizing software delivery. Announced capabilities include agentic workflow progression, governed artifact management, dependency firewall controls, security standards and impact analytics. GitLab emphasizes consistent identity, policy and traceability from intent through production.

### Stack Overflow Stack Internal

Stack Overflow announced the next generation of [Stack Internal](https://stackoverflow.co/company/press/archive/stack-internal-trusted-enterprise-ai) on September 30. Its product direction is to convert fragmented enterprise knowledge into reusable, decision-grade knowledge with provenance, recency and human validation signals. This is relevant to AlgoX's distinction between mere relevance and evidence that is sufficiently authoritative and validated for reuse.

## AlgoX implications

Model the workflow around explicit task and control records, not just chat sessions:

```text
Trigger / Authorized Request
  -> WorkItem / Assignment
  -> AgentRun + Dedicated Workspace
  -> Delegation / Tool Actions
  -> Artifacts / Diff / Tests
  -> Review / Approval
  -> Merge / Release / Deployment
  -> Evidence + Audit Record
```

Useful conceptual entities include `WorkItem`, `Assignment`, `AgentRun`, `Workspace`, `Delegation`, `Approval`, `Artifact`, `WorkflowVersion` and `ExternalEffect`. Link these to the existing Interaction, ExecutionEvent, Evidence, Evaluation and PromotionDecision records.

The agent should not be able to redefine its own authorization or silently move from a requested task to an unbounded repository/CI workflow. Trigger identity, allowed operations, repository/workspace scope, review state and artifact lineage must remain independently inspectable.

## Decision

**ADOPT conceptually.** DeepSeek's prototype is a useful reference for persistent task/work-item lifecycles and dedicated agent workspaces. GitHub and GitLab demonstrate how agentic activity can be integrated with existing CI, security, identity and approval controls. Stack Internal reinforces the need to promote human-validated, provenance-rich knowledge rather than raw retrieved text.

## Sources

- DeepSeek dsh-superagent prototype: https://github.com/deepseek-ai/dsh-superagent-prototype
- GitHub Agentic Workflows: https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/
- GitLab Governed Software Factory: https://ir.gitlab.com/news/news-details/2026/GitLab-Announces-the-Foundation-for-the-Governed-Software-Factory/default.aspx
- Stack Overflow Stack Internal: https://stackoverflow.co/company/press/archive/stack-internal-trusted-enterprise-ai
