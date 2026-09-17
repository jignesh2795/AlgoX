# PX-2026-006 — Paper-to-agent knowledge packaging

**Research date:** 2026-09-17
**Status:** validated research finding; architecture/capability input
**AlgoX area:** knowledge representation / retrieval / tool interfaces / provenance / research automation

## Finding

Paper2Agent, published in Nature on 2026-09-16, demonstrates a significant shift from treating research artifacts as documents to packaging them as executable, validated agent capabilities. The system analyzes a research paper and its associated code/data/workflows, constructs an MCP server exposing tools, resources and prompts, and iteratively generates tests to validate the resulting tools against reference behavior.

Repository: https://github.com/jmiao24/Paper2Agent

## Why this matters for AlgoX

AlgoX's evidence model should not assume that institutional knowledge is always best represented as text chunks in a retrieval index. Some high-value knowledge is better represented as a validated executable capability:

```text
Research Artifact
  -> Source / Code / Data
  -> Agentification
  -> Tool / Resource / Prompt
  -> Validation
  -> Provenance
  -> Versioned Knowledge Capability
```

This complements, rather than replaces, trajectory-aware retrieval. Retrieval can select an appropriate validated capability instead of merely retrieving descriptive text.

## Architecture implication

Introduce a conceptual distinction between:

- **Document Evidence** — text, papers, specifications, reports.
- **Executable Evidence** — code, notebooks, APIs, tools, reproducible workflows.
- **Validated Knowledge Capability** — an executable artifact whose behavior has been independently tested and whose provenance is recorded.

A future AlgoX knowledge record should therefore be able to reference both content and executable capability forms:

```text
KnowledgeItem
  -> EvidenceRefs[]
  -> CapabilityRef?
  -> ValidationRefs[]
  -> SourceVersion
  -> ProvenanceGraph
```

## Important limitation

Successful reproduction against reference outputs demonstrates faithful execution, not necessarily scientific validity. AlgoX should preserve this distinction: **execution validation != domain truth validation**.

## Decision

**ADOPT conceptually.** Add executable/agentified knowledge as a first-class future capability, but do not implement a Paper2Agent-style framework inside AlgoX yet. AlgoX should provide the provenance, validation, versioning and promotion layer that can govern such capabilities regardless of how they are generated.

## Historical significance

Paper2Agent is an important 2026 ecosystem marker because it shows MCP evolving beyond simple tool integration toward a packaging layer for reusable research knowledge and executable methods. This strengthens AlgoX's role as a provenance and validation substrate across both retrieved information and executable knowledge.
