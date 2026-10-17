# PX-2024-015 — Agent Memory: From Context Buffers to Persistent Memory

**Status:** PROVISIONAL
**Research period:** 2024
**Domain:** AI agents / memory / knowledge systems

## Question
How did 2024 agent-memory research change the design target for AlgoX's institutional memory?

## Evidence

The 2024 survey literature treats memory as a core mechanism for long-running LLM agents and distinguishes memory design from simply keeping a larger conversation context. The literature identifies persistent memory, retrieval, memory management, and evaluation as separate concerns. citeturn0academia61turn0search0

A recurring early implementation pattern was vector storage and semantic retrieval. The 2024 AAAI symposium review explicitly notes that long-term agent memory was often implemented with vector databases, while identifying unresolved issues around separating memory types and managing memory across an agent's lifetime. citeturn0search0

## AlgoX interpretation

The useful abstraction is not "vector memory." It is **managed institutional memory**.

AlgoX must preserve:

1. raw experience / episodes;
2. extracted facts and claims;
3. source provenance;
4. temporal validity;
5. confidence and evidence maturity;
6. contradictions and supersession;
7. experiments and their results;
8. decisions and the evidence behind them;
9. reusable capabilities;
10. what was known at a particular point in time.

## Memory classes

| Memory class | Purpose | Example in AlgoX |
|---|---|---|
| Episodic | Preserve what happened | research run, source snapshot, experiment |
| Semantic | Preserve what is believed to be true | claim, capability, architecture fact |
| Procedural | Preserve how to do something | research workflow, benchmark recipe |
| Decision | Preserve what was chosen and why | ADR, adopt/adapt/reject |
| Evidence | Preserve why a claim is trusted | source locator, reproduction, benchmark |
| Temporal | Preserve when facts/decisions were valid | exchange rule as-of date |
| Failure | Preserve what did not work | rejected design, failed experiment |

## Design consequence

Do not model memory as one table or one vector index. Model it as a set of typed records connected by provenance and time.

Semantic retrieval is a **read optimization** over memory. It is not the authoritative memory itself.

## Research conclusion

**Decision:** ADAPT the strongest ideas from agent-memory systems, but build AlgoX around evidence-backed institutional memory rather than a generic chatbot memory layer.

**Confidence:** High for the architectural direction; implementation technology remains an experiment.

**Next validation:** compare PostgreSQL-first, graph-first, and hybrid implementations against representative AlgoX queries involving temporal facts, contradictions, provenance, semantic retrieval, and multi-hop capability relationships.
