# PX-2023-028 — BloombergGPT

## Historical role
BloombergGPT was announced in March 2023 as a large language model trained on a mixed corpus of financial documents and general-purpose text, with evaluation on both finance-specific and general NLP tasks. The project is an important counterpoint to smaller open financial-model efforts because it demonstrates the data, compute and specialization trade-offs of a large proprietary finance model. citeturn0search7

## Architecture observations
- Domain specialization can require substantial high-quality domain data.
- Financial performance should be evaluated separately from general-language performance.
- Model quality must be considered alongside training cost and infrastructure requirements.

## AlgoX extraction
**Capability:** domain-specific foundation-model benchmarking.

**Lesson:** when evaluating finance AI, record domain performance, general performance, compute cost, data provenance and reproducibility separately. A higher benchmark score does not automatically justify a larger or more expensive model.

## Decision
ASSESS — historical finance-AI reference point; compare against open and parameter-efficient approaches rather than treating scale as the default answer.

## Evidence maturity
C2 — published project/reporting and public comparative data; AlgoX reproduction pending.
