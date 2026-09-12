# 2023 Ecosystem Research — Remaining / Follow-up Candidates

These candidates are research targets, not endorsements. Completed items are retained below as historical coverage so the research program remains auditable.

## Agent systems

### Covered
- BabyAGI
- CAMEL — PX-2023-017
- Generative Agents
- AgentGPT
- SuperAGI
- MetaGPT
- ChatDev
- MemGPT
- AutoGen — PX-2023-018
- Open Interpreter — PX-2023-026

### Follow-up
- Voyager / embodied-agent research
- Toolformer / tool-use research
- Reflexion / self-improvement
- AgentBench / WebArena evaluation

## AI software engineering

### Covered
- Aider
- GPT Engineer
- GPT Migrate
- Continue
- Code Llama — PX-2023-022
- SWE-bench historical origin/evidence

### Follow-up
- repository-aware coding architectures
- code-agent verification patterns
- local coding models

## Model and inference infrastructure

### Covered
- LLaMA — PX-2023-021
- Code Llama — PX-2023-022
- llama.cpp
- text-generation-webui
- FastChat
- vLLM — PX-2023-025
- Hugging Face Transformers — PX-2023-061
- MLC LLM — PX-2023-064
- Axolotl — PX-2023-065
- Ray Serve / BentoML / DeepSpeed — PX-2023-069

### Follow-up
- LitGPT
- additional inference/runtime projects

## Generative media

### Follow-up
- AUTOMATIC1111 Stable Diffusion WebUI
- InvokeAI
- ComfyUI
- ControlNet
- Segment Anything
- Whisper / multimodal infrastructure

## Data / retrieval infrastructure

### Covered
- Qdrant — PX-2023-019
- Milvus — PX-2023-035
- Chroma — PX-2023-036
- Weaviate — PX-2023-029
- FAISS — PX-2023-062
- Haystack — PX-2023-063

### Follow-up
- retrieval/RAG architecture evolution
- hybrid lexical + semantic retrieval
- retrieval evaluation

## Financial / quantitative ecosystem — priority

### Covered
- Microsoft Qlib — PX-2023-020
- OpenBB Terminal — PX-2023-032
- FinGPT — PX-2023-027
- BloombergGPT — PX-2023-028
- FinRL — PX-2023-030
- vectorbt — PX-2023-031
- Hummingbot — PX-2023-033
- CCXT — PX-2023-034
- Freqtrade — PX-2023-066
- Backtrader — PX-2023-067
- Jesse — PX-2023-068
- QuantConnect LEAN — PX-2023-074
- NautilusTrader — PX-2023-075
- Zipline 3.7 / v4 transition — PX-2023-076
- Indian broker/API ecosystem — PX-2023-077

### Follow-up
- Voyager / Toolformer / Reflexion and agent-evaluation crossover with finance
- LitGPT and additional model/inference runtimes
- financial data infrastructure and data-quality systems
- instrument master / corporate-action infrastructure
- Indian-market historical broker/API projects at version-specific evidence level
- execution, reconciliation, fill simulation and risk architecture
- Indian-market open-source trading systems with demonstrable 2023 release/history evidence

## Historical boundary findings

### LEAN
LEAN is confirmed as a mature event-driven trading engine with modular data/brokerage/algorithm components. Its value for AlgoX is as a mature reference architecture, not as proof that its design should be copied wholesale.

### NautilusTrader
NautilusTrader has strong 2023 evidence and is especially valuable for event-driven domain modeling: market data types, order/execution events, risk limits, actors, data catalogs and Rust acceleration were all visible in 2023 releases.

### Zipline
Zipline's 2023 evidence is valuable primarily as an evolution/failure signal: the maintainer announced a major rewrite after the 3.7 line, demonstrating that mature backtesting infrastructure can accumulate architectural debt that eventually motivates a rewrite.

### Indian broker APIs
The Indian ecosystem already exposed the essential automation boundary by 2023, but each provider had its own authentication, instrument, order, WebSocket and state semantics. AlgoX should therefore research broker abstraction as a normalization problem with preserved provider-specific semantics, not as a simplistic common-interface problem.

### OpenAlgo temporal classification
OpenAlgo is intentionally **not classified as a 2023 project** in this index. Its documented 1.0 launch is April 8, 2024. It remains a high-priority 2024 Indian-market research target.

## Discovery note

The discovery pass has added additional infrastructure and trading-framework records, but this does not mean 2023 is closed. Historical year must be established from dated releases, repository history, papers, documentation or other contemporaneous evidence. Current popularity is only a discovery signal.

## Research rule

A project enters the permanent knowledge catalog only after its historical relevance, architecture, evidence, outcome, and provenance have been evaluated. Popularity is a discovery signal rather than a quality score. Historical year refers to the relevant ecosystem development/release/evidence year, not necessarily the project's original creation year.
