# MemGPT

- **Period:** 2023
- **Category:** Agent memory / context management
- **Historical signal:** Treated memory as a systems problem rather than assuming the entire useful history fits in the model context window.
- **Core idea:** Manage multiple memory tiers and selectively move information between them.
- **Architecture lesson:** Agent memory can be separated from the model's immediate context and managed explicitly.
- **AlgoX extraction:** Memory hierarchy; context paging; durable memory versus working context; explicit memory-management policy.
- **Relevance to AlgoX:** Institutional memory is a core requirement, so this is a foundational historical precedent for later memory architectures.
- **Validation needed:** Compare memory architectures for retrieval quality, cost, latency, stale information, and provenance preservation.
- **Evidence:** 2023 ecosystem references describe MemGPT as managing different memory tiers for extended context, including vector databases, SQL, and documents. citeturn0search5
