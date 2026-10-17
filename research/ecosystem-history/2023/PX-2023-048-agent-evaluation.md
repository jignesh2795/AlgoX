# PX-2023-048 — 2023 Agent Evaluation

## Scope
The 2023 agent literature established that tool use, reasoning loops, memory, and autonomy require evaluation under realistic environments. The major research line includes Toolformer, Reflexion, Generative Agents, Voyager, AgentBench, WebArena, and the broader 2023 agent survey literature. citeturn0search8

## Key finding
Agent capability cannot be inferred from a successful demonstration. Evaluation must test the complete loop:

```text
reason
  ↓
choose action/tool
  ↓
execute
  ↓
observe environment
  ↓
update state/memory
  ↓
verify outcome
```

WebArena is particularly important because it evaluates agents in realistic web environments rather than only text-only tasks. SWE-bench applies a similar principle to software engineering by requiring changes to real repositories and evaluation through repository tests. citeturn0search14turn0academia48

## AlgoX extraction
**Capability:** environment-grounded agent evaluation.

**Decision:** ADOPT the evaluation principle. Reject any future AlgoX claim of agent capability based solely on a demo or model benchmark that omits the execution environment and verification loop.

## Research implication
AlgoX experiments should record:
- task definition
- environment
- available tools
- permissions
- model/version
- prompts/policies
- intermediate actions
- final result
- verification method
- failure mode
- cost/latency where relevant

## Evidence maturity
C2 — published benchmark/research evidence; AlgoX has not independently reproduced the external benchmarks.
