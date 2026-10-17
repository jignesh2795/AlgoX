# PX-2023-061 — PIXIU / FinMA

## Classification
- Year: 2023
- Domain: Financial AI / LLM / evaluation
- Type: Research + open-source resource
- Primary capability: domain-specific financial LLM, instruction tuning, benchmark
- Evidence status: C1 — primary repository/paper inspected
- AlgoX status: RESEARCHED — decision pending reproduction

## Historical significance
PIXIU was introduced in 2023 as an open financial-LLM resource combining a financial model (FinMA), instruction-tuning data, and evaluation benchmarks. The paper describes 136K instruction samples and a benchmark spanning financial tasks and datasets.

## Architecture / capability map
```text
Financial sources / datasets
        ↓
Instruction dataset (FIT)
        ↓
Fine-tuned financial model (FinMA)
        ↓
Standardized evaluation (FinBen / task suite)
```

Important capability boundaries:
- domain adaptation through instruction tuning;
- benchmark/evaluation as a first-class artifact;
- mixed financial modalities including text and time-series inputs;
- open model/data/evaluation resources.

## AlgoX extraction
**Capability:** domain-specific model + dataset + evaluator packaged as one research stack.

**Lesson:** a financial AI capability should not be evaluated solely through the model. Dataset construction, task definitions, benchmark protocol and model results must remain linked through provenance.

## Relevance to AlgoX
High. PIXIU reinforces the existing AlgoX principle that **evaluation is part of the capability**, not an afterthought. It also provides a historical reference for financial-domain LLM research before the later finance-agent wave.

## Validation questions
- Can benchmark results be reproduced from the published data/protocol?
- How sensitive are results to model/checkpoint choice?
- Are financial prediction tasks temporally leakage-safe?
- How much of the reported advantage comes from domain adaptation versus task formulation?
- Can the benchmark be used as a regression suite for future AlgoX financial reasoning systems?

## Decision
**ADAPT** the architectural lesson: retain explicit dataset → task → evaluator → result provenance in AlgoX. Do not adopt the model itself as a system dependency without a separate benchmark and licensing review.

## Primary evidence
- PIXIU GitHub repository: https://github.com/The-FinAI/PIXIU
- PIXIU paper: arXiv:2306.05443

## Notes
This record deliberately does not treat reported model performance as production evidence. Production readiness remains unverified.
