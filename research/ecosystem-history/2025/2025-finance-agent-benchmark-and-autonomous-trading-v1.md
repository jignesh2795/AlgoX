# 2025 Finance-Agent Benchmarks and Autonomous Trading

## Purpose
Record 2025 evidence on financial research agents, autonomous trading agents, and the evaluation requirements they expose. This is historical evidence for AlgoX, not an endorsement of autonomous live trading.

## Evidence

### Finance Agent Benchmark
The 2025 Finance Agent Benchmark evaluates 537 expert-authored questions across nine financial task categories using recent SEC filings and an agentic tool harness. Its reported best-model result was 46.8% accuracy at an average cost of $3.79/query. This demonstrates that strong general-purpose models were still materially unreliable on realistic financial research tasks.

### InvestorBench
InvestorBench provides a broader financial decision-making evaluation spanning stocks, cryptocurrencies, ETFs, multiple environments, and multiple LLM backbones. The important capability is the move from static financial QA toward decision-making in task environments.

### StockBench
StockBench evaluates LLM agents in multi-month stock-trading environments with sequential buy/hold/sell decisions and financial metrics such as cumulative return, maximum drawdown, and Sortino ratio. Static financial knowledge is therefore treated as insufficient evidence for trading capability.

### Agent Market Arena / live trading evaluation
2025 work on live multi-market evaluation introduced continuous environments using verified market data and expert-checked news. Results indicate that agent architecture and risk style can materially affect behavior, and that model backbone alone is not a sufficient explanation for outcomes.

### AI-Trader
AI-Trader extends evaluation to live, data-uncontaminated decision-making across U.S. stocks, Chinese A-shares, and cryptocurrency markets. Its reported results emphasize that general intelligence does not automatically produce effective trading and that risk control is central to cross-market robustness.

## AlgoX findings

1. **Financial research capability and trading capability are separate capabilities.** A system can answer financial questions without demonstrating profitable or risk-controlled sequential decision-making.
2. **Static benchmark success is insufficient.** Evaluation must include environment interaction, temporal sequencing, tool use, and consequences.
3. **Risk must be a first-class evaluation dimension.** Return alone is inadequate; drawdown, volatility, risk-adjusted return, exposure, and failure behavior matter.
4. **Agent architecture is an experimental variable.** Do not attribute outcomes only to the underlying model.
5. **Point-in-time correctness is essential.** Financial agents must operate on information actually available at the decision timestamp.
6. **Live evaluation is qualitatively different from historical backtesting.** Data contamination, information leakage, execution assumptions, and changing environments must be controlled.
7. **Autonomous trading should remain downstream of evidence and governance.** AlgoX should research and validate capabilities; it should not infer production readiness from a benchmark return.

## Capability implications

ADOPT as research requirements:
- environment-based evaluation
- point-in-time datasets
- sequential decision evaluation
- risk-aware metrics
- agent-trace capture
- reproducible evaluation environments
- model/agent architecture separation

ADAPT:
- financial-agent benchmarks into an AlgoX capability benchmark layer
- trading environments into reproducible experiment fixtures

DO NOT infer:
- benchmark profitability => production readiness
- LLM intelligence => trading skill
- one market's result => general financial capability

## Evidence maturity
The benchmark evidence supports architectural requirements and evaluation methodology. It does not by itself establish production readiness for autonomous trading.

## Sources
- Finance Agent Benchmark, 2025: arXiv:2508.00828.
- InvestorBench, ACL 2025: ACL Anthology 2025.acl-long.126.
- StockBench, 2025: arXiv:2510.02209.
- When Agents Trade / Agent Market Arena, 2025: arXiv:2510.11695.
- AI-Trader, 2025: arXiv:2512.10971.
