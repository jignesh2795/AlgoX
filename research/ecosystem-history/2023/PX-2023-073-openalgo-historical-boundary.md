# PX-2023-073 — OpenAlgo Historical Boundary

## Discovery result

OpenAlgo is highly relevant to AlgoX's Indian-market research, but current evidence does **not** justify placing its present architecture into the 2023 project inventory.

Its official documentation records the initial OpenAlgo 1.0.0.0 launch on 8 April 2024, initially supporting Angel, Upstox, Zerodha, 5Paisa, Fyers, Kotak, Dhan and ICICI Direct.

## Why this matters

The current OpenAlgo architecture is useful evidence for studying the evolution of Indian broker abstraction, but using today's architecture as if it existed in 2023 would create temporal contamination.

## AlgoX classification

- Historical 2023: **not established**
- Historical 2024: **confirmed candidate**
- Current architecture: **separate current-state evidence**
- Research value: High

## Research rule demonstrated

```text
Current project
     ↓
Historical release evidence
     ↓
Determine earliest supported year
     ↓
Assign to historical year
     ↓
Keep current architecture as a later evolution state
```

## Decision

**QUALIFY** the 2023 Indian-market synthesis: modern unified broker platforms must be studied historically, but they must not be back-projected into 2023 without primary release evidence.

## Sources

- https://docs.openalgo.in/change-log/release/version-1.0.0.0-launched
- https://github.com/marketcalls/openalgo
