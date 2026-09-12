# PX-2023-055 — LiteLLM

Status: DISCOVERY / INITIAL RESEARCH
Year: 2023
Repository: BerriAI/litellm

## Why it belongs in the 2023 corpus

LiteLLM emerged in the 2023 ecosystem as a provider/model abstraction layer. It is
important to study because it represents a different architectural response to the
rapidly changing model-provider landscape: normalize heterogeneous model APIs
behind a common interface and centralize routing/configuration concerns.

## Research targets

- provider abstraction
- request/response normalization
- model routing
- retries and failure handling
- cost and usage tracking
- configuration boundaries
- proxy/gateway architecture
- observability
- fallback semantics
- provider-specific escape hatches

## AlgoX questions

1. Which semantics can safely be normalized across model providers?
2. Which provider differences must remain visible?
3. How should routing decisions be represented as evidence?
4. How should provider failure and fallback be audited?
5. What lessons apply to future broker/venue abstraction?

## Initial classification

Architecture Intelligence; AI Infrastructure; Provider Abstraction; Operations.

Evidence maturity: C1 — repository/source inspection pending deeper extraction.
Decision: ASSESS.
