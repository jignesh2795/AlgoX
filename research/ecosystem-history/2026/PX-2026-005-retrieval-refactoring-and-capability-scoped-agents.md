# PX-2026-005 — Retrieval, refactoring evaluation, and capability-scoped agents

**Research date:** 2026-09-16  
**Status:** validated research finding; architecture input  
**AlgoX area:** coding-agent evaluation / retrieval / security / provenance

## 1. RefactorPlatform — controlled repository-scale evaluation

RefactorPlatform is an open-source evaluation harness for repository-scale coding-agent refactoring. It fixes the environment and varies model, retrieval regime, prompt specificity, and multi-agent execution. Runs use isolated workspaces and retain terminal bytes, agent events, diffs, evaluation logs, and machine-readable results. The project was accepted to EMNLP 2026 System Demonstrations. citeturn2academia36turn27file0

The reported experiments provide a particularly useful warning for AlgoX: retrieval is not automatically beneficial. AST-aware chunking improved results, while naive line-window retrieval could underperform no retrieval; the tested lean retrieval-augmented single-agent configuration also outperformed the tested sub-agent configuration. The platform therefore isolates design variables instead of attributing every gain to the model or to "agents" generally. citeturn2academia36

### AlgoX implication

Add **controlled ablation** as a first-class experiment property. A retrieval experiment should identify exactly what changed:

- model;
- prompt;
- chunker;
- retriever;
- reranker;
- context budget;
- agent topology;
- evaluator;
- environment.

AlgoX should also preserve the principle that a benchmark verdict and the mechanism that produced it are separate evidence. RefactorPlatform's plugin boundary and fixed setup semantics are a strong reference for this separation. fileciteturn56file0

## 2. ExecRetrieval — retrieval must be tested against functional counterfactuals

ExecRetrieval introduces an execution-verified code-retrieval benchmark containing canonical implementations alongside near-clone buggy variants. On 939 Python tasks and 23 dense embedding configurations plus BM25, the leading hosted system reached exec@10 = 1.00 but only exec@1 = 0.331; rank-1 misses were overwhelmingly paired buggy variants. citeturn2academia38

### AlgoX implication

This materially strengthens the existing LRAT/ARB direction. Retrieval quality should not be defined as semantic similarity or even ordinary relevance alone. For coding/research workflows, AlgoX should eventually test:

```text
semantic relevance
      +
workflow usefulness
      +
functional correctness
      +
authority
      +
selective abstention
```

The benchmark also supports keeping **retrieval evidence** separate from **validated knowledge**: retrieving a plausible but functionally wrong implementation is not successful evidence.

## 3. CapScope — authorization should be capability-scoped and outside model context

CapScope proposes a harness-level authorization mechanism for coding agents. It derives an authority ceiling from trusted task input, assigns typed capabilities to agents, and checks every tool call against those capabilities outside the model's context. In its reported 300-run repair evaluation, the injected effect occurred in 3/75 runs under CapScope versus 33–47/75 under ambient-authority/global-policy baselines, while repair completion remained comparable. citeturn2academia37

### AlgoX implication

This is a concrete design refinement to `PX-2026-004`. The provenance layer should not merely record that an action was allowed. It should record the **capability decision that made the action possible**.

Recommended conceptual chain:

```text
Task intent
   -> Authority ceiling
   -> Agent capability set
   -> Tool request
   -> Policy decision
   -> External effect
   -> Observation
   -> Evaluation
```

Capabilities should be typed and versioned, with permissions maintained outside model-visible context. This is stronger than a single global "agent allowed" flag and fits the existing AlgoX requirement for effect provenance. fileciteturn60file0

## 4. Architecture decisions

1. **ADOPT:** controlled ablation and reproducible experiment environments as mandatory metadata for important AlgoX evaluations.
2. **ADOPT:** functional-counterfactual retrieval evaluation for coding/research retrieval.
3. **ADOPT:** capability-scoped authorization as the preferred security model for future agent adapters.
4. **ADOPT:** record authorization decisions as provenance events, without storing secrets.
5. **DO NOT COPY:** any benchmark or harness wholesale; extract contracts and evaluation methodology.

## 5. Historical significance

The 2026 ecosystem is converging on a more rigorous view of agent systems: capability is not just model intelligence. It depends on **context selection, execution regime, authorization boundaries, independent evaluation, and reproducible evidence**. This directly supports AlgoX's decision to remain a provenance/evaluation substrate rather than another monolithic agent runtime.

## Sources

- RefactorPlatform: https://github.com/PiSchool/refactor-platform
- RefactorPlatform paper: https://arxiv.org/abs/2609.04898
- CapScope paper: https://arxiv.org/abs/2609.08371
- ExecRetrieval paper: https://arxiv.org/abs/2609.01865
