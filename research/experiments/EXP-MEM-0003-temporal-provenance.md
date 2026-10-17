# EXP-MEM-0003 — Temporal Provenance Gate

Status: **IMPLEMENTED — NOT EXECUTED IN THIS SESSION**

## Objective

Ensure that an institutional decision reconstructed as of time `T` cannot depend on evidence observed after `T`.

## Required invariants

- every evidence reference resolves to an authoritative evidence record
- future evidence is excluded from historical reconstruction
- missing evidence fails validation
- causal links remain explicit
- counter-evidence remains visible

## Promotion gate

The temporal/provenance layer may be promoted beyond the reference implementation only after executable tests demonstrate these invariants across multiple timestamps, supersession chains, contradictory findings, and missing-link cases.
