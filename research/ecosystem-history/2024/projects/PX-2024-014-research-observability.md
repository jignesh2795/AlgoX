# PX-2024-014 — Research-Agent Observability

**Historical category:** AI-agent engineering
**Domain:** Observability, tracing, reproducibility

## Historical signal

As agent workflows became multi-step systems, output quality alone became insufficient for debugging and evaluation. A research agent can fail through retrieval, planning, tool invocation, memory selection, evidence interpretation, or synthesis even when its final response appears plausible.

## Architectural lesson

Agent execution should produce an inspectable trace.

```text
Run
├── task
├── configuration
├── model/runtime
├── retrieved sources
├── memory reads/writes
├── plans
├── tool calls
├── intermediate observations
├── decisions
├── verification
├── final output
└── metrics
```

## AlgoX extraction

- immutable research-run identifier
- step-level trace
- source provenance
- tool-call logging
- evidence-to-claim links
- cost and latency metrics
- failure classification
- reproducibility metadata
- replayable experiments

## Relevance to AlgoX

Very high. Evidence-backed research cannot be audited if the system records only the final generated report. AlgoX should preserve the chain from source acquisition through extraction, synthesis, experiment, and decision.

**Evidence maturity:** C2
**Status:** RESEARCHED
