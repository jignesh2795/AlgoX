# PX-2023-086 — Indian-market cost and margin modeling

## Classification
- Year: 2023 ecosystem evidence
- Domain: Execution / risk
- Capability: Brokerage, exchange charges, taxes, margin and buying-power constraints
- Evidence maturity: C1

## Finding
A backtest or execution simulator that ignores Indian transaction costs and margin semantics can produce materially misleading results. Brokerage, exchange transaction charges, STT, GST, SEBI charges, stamp duty and segment-specific margin/buying-power rules must be modeled as time/versioned inputs rather than hard-coded universal constants.

## Evidence note
Current broker documentation demonstrates that these dimensions are broker- and segment-specific. Historical values must be sourced from dated broker/exchange/regulatory evidence before being used in a 2023 experiment.

## Decision
ADOPT as a capability requirement. Do not freeze current charges as historical truth.
