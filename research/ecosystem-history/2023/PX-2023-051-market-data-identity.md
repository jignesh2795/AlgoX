# PX-2023-051 — Market Data Identity Is a First-Class Capability

**Period:** 2023
**Domain:** Market data / broker infrastructure
**Status:** Historical research record

## Observation

Broker APIs commonly expose instruments through provider-specific identifiers and stream subscriptions. Kite Connect, for example, uses numerical instrument tokens for WebSocket subscriptions and exposes instrument metadata separately from quote streaming.

## Finding

A trading platform cannot safely treat a ticker string as the complete identity of a tradable instrument. Canonical identity needs exchange, segment/product context, provider identifiers, effective dates, and lifecycle information.

## Required canonical concepts

- canonical instrument ID
- exchange
- segment/venue
- symbol/name
- provider instrument ID
- asset/product type
- expiry where applicable
- strike/option type where applicable
- currency
- effective-from/effective-to
- corporate-action lineage
- source/provenance

## AlgoX implication

Instrument identity belongs in the Market Data capability and should be shared by research, portfolio, execution, reconciliation, and reporting rather than reimplemented inside each broker connector.

## Decision

**ADOPT:** canonical instrument identity boundary.

**ADAPT:** broker-specific identifiers as provider mappings, not as universal identifiers.

**Confidence:** High.
