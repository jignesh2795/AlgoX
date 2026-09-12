# AlgoX

AlgoX is a research, capability-intelligence, and validation system for building better financial technology.

It studies projects, papers, algorithms, architectures, engineering practices, AI-agent workflows, market infrastructure, regulation, failures, and emerging technologies; converts evidence into reusable capabilities; validates promising ideas; and records decisions for future systems.

## Mission

Build institutional memory for financial technology R&D so future systems do not repeatedly reinvent existing capabilities or miss important ideas.

## Core lifecycle

`Discover → Classify → Research → Extract → Evaluate → Experiment → Benchmark → Decide → Catalog → Gap Analysis → Design → Implement → Learn`

## Scope

AlgoX is deliberately broader than GitHub and broader than algorithmic trading. Sources may include:

- Open-source repositories and package ecosystems
- Academic papers and research
- Exchange, broker, and regulatory documentation
- Engineering and production literature
- AI and agent research
- Practitioner communities
- Experiments and benchmarks

## AI-era historical research

AlgoX maintains an ecosystem-history program beginning in **January 2023** to study the evolution of open-source technology during the modern generative-AI era. It records not only projects that trended, but why they grew, what they introduced, what survived, what failed, and which capabilities remain valuable.

## Evidence discipline

AlgoX separates:

1. Observation / fact
2. Finding
3. Hypothesis
4. Decision

No unverified claim should silently become an architectural requirement.

## Decision vocabulary

- **ADOPT** — use an existing approach directly
- **ADAPT** — modify an existing approach where appropriate
- **WRAP** — isolate an external component behind an internal interface
- **BUILD** — create a missing capability
- **REJECT** — do not use the approach

## Research maturity

`UNVERIFIED → REPRODUCED → BENCHMARKED → VALIDATED`

## Local verification

AlgoX does **not require GitHub Actions** for verification. The repository includes a local runner:

```bash
python tools/local_verify.py
```

For the full pytest suite, when pytest is installed locally:

```bash
python tools/local_verify.py --pytest
```

GitHub is used for source control and research review; Python execution and benchmark evidence are generated locally.

See `research/experiments/EXP-MEM-0005-local-verification.md` for the verification protocol.

## Repository structure

- `research/` — research questions and source studies
- `knowledge/` — reusable capabilities, patterns, algorithms, and technology intelligence
- `evidence/` — provenance, claims, code references, benchmarks, and reproductions
- `extraction/` — extracted ideas, components, architectures, and workflows
- `experiments/` — hypotheses, proofs of concept, simulations, and results
- `decisions/` — adoption decisions and ADRs
- `planning/` — capability gaps, architecture alternatives, priorities, and roadmap
- `schemas/` — machine-readable record contracts
- `tools/` — local research and verification utilities
- `data/` — generated catalogs and indexes

## Status

AlgoX v0.1 is the foundation phase. The methodology and schemas are intentionally established before building autonomous research automation.
