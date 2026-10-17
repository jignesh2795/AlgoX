# Temporal Decision Memory

AlgoX treats time as part of research truth, not merely metadata.

For a decision reconstructed at time `T`, the admissible evidence set is constrained by what was observed by `T`. Later evidence may change the present decision but must not retroactively alter the historical reconstruction.

```text
Current knowledge
      │
      ├── evidence observed ≤ T → admissible for historical view
      └── evidence observed > T → future knowledge; excluded
```

## Consequences

- exchange and broker API changes require observation/effective dates
- superseded claims remain recoverable
- experiments are attached to the evidence available at their execution time
- contradictions are preserved rather than overwritten
- decisions can be audited against their historical information set

The reference implementation exposes this through `ValidatedResearchGraph.path_is_valid_as_of()` and the authoritative evidence registry.
