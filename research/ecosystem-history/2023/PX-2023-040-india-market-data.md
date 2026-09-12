# PX-2023-040 — India-market architecture lessons

## Scope
This record captures architectural lessons from the India-market integrations visible in open trading infrastructure, rather than claiming that a single project represents the Indian ecosystem.

## Observations
- India equity support requires explicit market identity and exchange-aware data handling.
- Brokerage integrations expose account/product/order semantics that differ from generic exchange abstractions.
- Corporate-action normalization can materially affect historical research. LEAN documents multiple India-equity normalization modes for splits and dividends. citeturn0search1
- Zerodha integration exposes Indian product types such as MIS, CNC and NRML and trading segments such as equity and commodity. citeturn0search4
- Brokerage integration therefore needs more than an endpoint wrapper: it needs an explicit capability model and a mapping between canonical order intent and venue-specific order semantics.

## AlgoX extraction
**Capability:** market/broker capability matrix.

**Lesson:** future India-focused research must treat instrument master, exchange calendar, corporate actions, order types, product types, margin, fees and broker-specific behavior as first-class evidence objects.

## Decision status
ADOPT as a research requirement for all future India-market architecture comparisons.

## Evidence maturity
C2 — official India-market and brokerage integration documentation.
