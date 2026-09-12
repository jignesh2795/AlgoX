# Knowledge Governance Gate

AlgoX separates **model proposal** from **institutional truth**.

```text
LLM / researcher
      ↓
proposed knowledge delta
      ↓
schema validation
      ↓
provenance validation
      ↓
temporal validation
      ↓
contradiction detection
      ↓
policy / confidence gate
      ↓
explicit approval
      ↓
knowledge commit
```

## Non-negotiable rules

- A model cannot silently promote its own output to durable truth.
- Durable claims and decisions require evidence references.
- Unknown evidence is a rejection, not a low-confidence approval.
- Contradictions are retained and surfaced.
- Historical reconstruction cannot use evidence observed after the requested time.
- Approval is an explicit event and must identify the approving actor or policy.
- Search indexes, embeddings, and graph projections never become authoritative merely because retrieval ranks them highly.

The current implementation is intentionally storage-independent. It provides the policy boundary that a future PostgreSQL-backed transaction layer can enforce atomically.
