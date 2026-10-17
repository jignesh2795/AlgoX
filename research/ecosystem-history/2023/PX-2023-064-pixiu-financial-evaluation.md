# PX-2023-064 — PIXIU Evaluation Capability

## Classification
- Year: 2023
- Domain: Financial AI evaluation
- Type: Benchmark capability record
- Evidence status: C1

## Why this is separate from PX-2023-061
PIXIU is important not only as a financial LLM project but as an early attempt to package **model + instruction data + standardized evaluation**. AlgoX should preserve that benchmark capability independently from the model implementation.

## Capability
```text
Financial task definitions
        ↓
Curated datasets
        ↓
Standard evaluation protocol
        ↓
Comparable model results
        ↓
Failure / strength analysis
```

## AlgoX extraction
Benchmark artifacts should be first-class research objects with:
- dataset version;
- task definition;
- evaluation metric;
- model/checkpoint;
- prompt/configuration;
- result;
- provenance;
- temporal validity;
- reproducibility status.

## Decision
**ADOPT** the benchmark-as-first-class-object principle. This complements AlgoX's existing Experiment and Benchmark schemas.

## Primary evidence
PIXIU paper and repository, 2023.
