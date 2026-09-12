# PX-2023-007 — FastChat

**Repository:** https://github.com/lm-sys/FastChat
**Historical category:** SUSTAINED
**Domain:** LLM serving / evaluation / open models

## 2023 signal
FastChat became an important 2023 project around open chat models, serving, and evaluation. Its 2023 release history includes Vicuna, Chatbot Arena, MT-Bench, long-context work, and real-world conversation datasets.

## Capability observed
Training, serving, evaluation, user-facing interaction, and human preference data were treated as related but distinct components.

## Architectural lesson
Model quality cannot be evaluated only by offline benchmark scores. Serving infrastructure and human evaluation can be part of the system's evidence loop.

## AlgoX extraction
- Multi-model serving
- OpenAI-compatible API boundary
- Evaluation infrastructure
- Human preference evaluation
- Dataset generation from real usage
- Separation of training/serving/evaluation concerns

## Evidence
Repository and 2023 release history: https://github.com/lm-sys/FastChat
GitHub 2023 ecosystem report: https://github.blog/news-insights/research/the-state-of-open-source-and-ai/

**Evidence maturity:** C1
**Status:** RESEARCHED
