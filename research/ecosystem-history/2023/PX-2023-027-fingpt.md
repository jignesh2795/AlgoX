# PX-2023-027 — FinGPT

## Historical role
FinGPT is a 2023 open-source financial LLM effort focused on making financial-language models accessible through open data, instruction tuning and parameter-efficient fine-tuning. Its public benchmark material compares financial tasks and reports the cost implications of training/fine-tuning different model families. citeturn0search7

## Architecture observations
- Financial AI benefits from domain-specific data and evaluation rather than generic language benchmarks alone.
- Parameter-efficient fine-tuning makes domain specialization materially cheaper than training a foundation model from scratch.
- Reproducibility requires recording datasets, base models, tuning method, compute assumptions and evaluation tasks.

## AlgoX extraction
**Capability:** domain-specific model adaptation and financial-language evaluation.

**Lesson:** AlgoX should distinguish generic model capability from finance-domain capability and preserve the exact dataset/model/evaluation lineage behind each finding.

## Decision
ASSESS — financial-domain AI benchmark/reference; useful for later finance-agent research.

## Evidence maturity
C2 — public project and benchmark evidence; AlgoX reproduction pending.
