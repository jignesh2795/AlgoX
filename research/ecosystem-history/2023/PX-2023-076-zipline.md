# PX-2023-076 — Zipline 3.7 / v4 Evolution

## Historical relevance
Zipline is important to AlgoX not only as a backtesting framework but as an example of architectural evolution and maintenance pressure in a mature research codebase.

## 2023 evidence
A June 19, 2023 maintainer discussion for Zipline announced a planned major v4 rewrite. The maintainer stated that development would focus on fixing bugs in 3.7.0 while the rewrite proceeded, with no further minor releases planned during that transition.

## AlgoX classification
- Domain: quantitative research / backtesting
- Type: backtest engine
- Historical year: 2023
- Evidence maturity: C2 — maintainer discussion / release evidence
- Research maturity: M2 — understood provisionally

## Architectural lessons
1. A mature research engine can reach a point where incremental maintenance is insufficient and a major rewrite becomes necessary.
2. Backtesting infrastructure is itself a long-lived software system with compatibility, correctness and maintenance constraints.
3. A rewrite should be recorded as architectural evidence, including what problems motivated it, rather than treated merely as a new version.

## AlgoX caution
The 2023 evidence is strongest for the transition/rewrite decision. AlgoX should not infer the eventual quality of v4 without separate implementation and benchmark evidence.

## Sources
- https://github.com/diced/zipline/discussions/433
