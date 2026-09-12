# PX-2023-063 — AlphaGen

## Classification
- Year: 2023
- Domain: Quantitative finance / alpha research / reinforcement learning
- Type: Research implementation
- Primary capability: formulaic alpha generation
- Evidence status: C1 — primary repository/paper inspected
- AlgoX status: RESEARCHED — benchmark reproduction required

## Historical significance
AlphaGen was presented at KDD 2023 and provides an implementation for generating synergistic formulaic alpha collections using reinforcement learning. The repository also includes Qlib-specific integration and modified symbolic-regression baselines.

## Architecture
```text
Market / research data
        ↓
Alpha representation / operators
        ↓
RL or symbolic search
        ↓
Candidate alpha factors
        ↓
Collection-level evaluation
        ↓
Backtest / trading experiment
```

## Key extraction
- automated factor discovery;
- reinforcement-learning search over formulaic alpha space;
- explicit baseline comparison against GP/deep symbolic regression approaches;
- integration boundary between generic alpha mining and Qlib-specific data/backtesting.

## AlgoX relevance
High. AlphaGen provides a concrete example of separating **research search** from downstream quantitative infrastructure. It is particularly relevant to AlgoX's research-to-experiment pipeline.

## Validation questions
- How robust are discovered factors outside the training regime?
- How is multiple-testing / data-mining bias controlled?
- Are alpha collections evaluated with realistic costs and turnover constraints?
- Does RL outperform strong symbolic-search baselines consistently across markets and periods?

## Decision
**ADAPT** the research-search separation and benchmark structure. Do not treat discovered alpha as production-ready without independent out-of-sample and execution validation.

## Primary evidence
- AlphaGen repository: https://github.com/ICT-FinD-Lab/AlphaGen
- KDD 2023 paper: “Generating Synergistic Formulaic Alpha Collections via Reinforcement Learning”

## Notes
Research performance is not production evidence. Reproducibility and regime robustness remain to be established.
