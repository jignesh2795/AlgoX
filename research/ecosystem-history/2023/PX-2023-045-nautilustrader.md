# PX-2023-045 — NautilusTrader

## Historical role
NautilusTrader is a useful reference for the 2023 trading-engine research because it treats research, deterministic simulation, and live execution as parts of one event-driven trading architecture. Its current documentation describes a Rust-native core, Python control plane, modular venue adapters, and common execution semantics across research and live environments. citeturn0search0turn0search3

## Historical caution
Current documentation is evidence of the architecture that exists today, not proof that every current feature existed in 2023. AlgoX therefore records the durable architectural pattern separately from later implementation evolution.

## Architecture observations
- Event-driven runtime rather than a purely vectorized research abstraction.
- Research and live execution share execution semantics and a deterministic time model.
- Venue/data-provider integration is isolated through adapters.
- DDD, messaging patterns, ports-and-adapters, and crash-only design are explicit architectural techniques in the current system. citeturn0search11
- The architecture explicitly recognizes that live execution introduces venue, transport, timing, persistence, external-activity, and reconciliation effects that simulation may not reproduce. citeturn0search7

## AlgoX extraction
**Capability:** research-to-live execution parity.

**Finding:** reducing backtest/live divergence is a first-class architectural capability, not merely a testing concern.

**Decision:** ADOPT as a capability requirement; ASSESS NautilusTrader's implementation as one candidate rather than copying the complete platform.

## Evidence maturity
C2 — primary project documentation and architecture evidence; historical feature dating and AlgoX reproduction require separate validation.
