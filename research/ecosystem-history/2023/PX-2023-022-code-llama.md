# PX-2023-022 — Code Llama

## Historical role
Meta released Code Llama in August 2023 as a code-specialized family built on Llama 2. The release included base, Python-specialized, and instruction-following variants, with fill-in-the-middle support for some models and evaluation on code benchmarks. citeturn3search0turn3search1

## Architecture observations
- General foundation models were being specialized for software-engineering workloads.
- Model variants separated general code generation, language specialization, and instruction following.
- Fill-in-the-middle made repository-local code completion a distinct capability from unconstrained code generation.
- Model evaluation needed domain-specific benchmarks rather than relying only on general language benchmarks.

## Research value
Very high for AlgoX's AI-assisted engineering track and later coding-agent research.

## AlgoX extraction
**Potential capability:** code-specialized model layer with task-specific variants and code benchmarks.

**Lesson:** model selection should be task-specific. Coding quality, repository reasoning, latency, context length, safety, and cost must be benchmarked independently.

## Evidence
- Meta research publication, August 24, 2023. citeturn3search0
- Meta engineering announcement describing model variants, FIM, training, and code-specific evaluation. citeturn3search1

## Decision status
ASSESS — retain as a 2023 foundation for the coding-agent research line; later coding models must be compared against it historically rather than collapsing the timeline.

## Evidence maturity
C2 — primary research and engineering evidence; no AlgoX benchmark yet.
