# PX-2023-047 — 2023 Agent Memory and Learning Patterns

## Scope
This record groups several independent 2023 research lines that materially shaped the later memory architecture: Reflexion, Generative Agents, and Voyager. They are kept together for capability analysis, while individual papers remain the authoritative evidence objects.

## Reflexion
Reflexion introduced verbal reinforcement learning in which an agent reflects on task outcomes using language and stores the resulting reflections for subsequent trials. The 2023 work demonstrates a separation between task execution and textual experience that can influence later behavior. citeturn0search8

**AlgoX lesson:** experience should be representable as durable, inspectable records rather than disappearing inside model context.

## Generative Agents
Generative Agents modeled memory, reflection, planning, and interaction in a simulated social environment. The work is important because it treats memory retrieval and reflection as explicit mechanisms supporting future behavior rather than treating a conversation transcript as the entire memory system. citeturn0search18

**AlgoX lesson:** memory can contain observations, derived reflections, and plans with different roles; these should not be collapsed into one undifferentiated vector store.

## Voyager
Voyager explored an open-ended embodied agent using an iterative skill-acquisition loop and an expanding skill library. The 2023 paper is evidence for treating acquired procedures/skills as reusable artifacts rather than requiring the model to rediscover them each time. citeturn0search18

**AlgoX lesson:** procedural memory should be a first-class memory type, linked to the evidence, experiment, or outcome that justified the procedure.

## Cross-project finding
These 2023 lines support a multi-type memory model:

```text
Observation / Episode
        ↓
Reflection / Finding
        ↓
Procedure / Skill
        ↓
Future task execution
```

This directly supports AlgoX's later separation of episodic, semantic, procedural, source, and meta memory.

## Decision status
ADOPT as a conceptual capability pattern; implementation requires provenance, temporal validity, confidence, and governance rather than unconstrained self-editing.

## Evidence maturity
C2 — published research evidence; AlgoX has not independently reproduced these systems.
