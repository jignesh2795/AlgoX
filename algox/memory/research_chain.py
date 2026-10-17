"""Research-chain reconstruction from the derived memory graph."""

from __future__ import annotations

from dataclasses import dataclass

from .graph import MemoryGraph
from .store import InMemoryStore, MemoryRecord


@dataclass(frozen=True)
class ResearchChain:
    root_id: str
    nodes: tuple[MemoryRecord, ...]
    relations: tuple[tuple[str, str, str], ...]


class ResearchChainResolver:
    """Reconstruct why a research conclusion exists without inventing links."""

    def __init__(self, store: InMemoryStore) -> None:
        self.store = store
        self.graph = MemoryGraph(store)

    def trace(self, root_id: str, *, max_depth: int = 6) -> ResearchChain:
        if root_id not in self.store.memories:
            raise KeyError(root_id)
        queue: list[tuple[str, int]] = [(root_id, 0)]
        seen = {root_id}
        nodes = [self.store.memories[root_id]]
        relations: list[tuple[str, str, str]] = []
        while queue:
            current, depth = queue.pop(0)
            if depth >= max_depth:
                continue
            for relation, target in self.store.memories[current].relations:
                if target not in self.store.memories:
                    continue
                relations.append((current, relation, target))
                if target not in seen:
                    seen.add(target)
                    nodes.append(self.store.memories[target])
                    queue.append((target, depth + 1))
        return ResearchChain(root_id, tuple(nodes), tuple(relations))

    def evidence_ids(self, root_id: str, *, max_depth: int = 6) -> list[str]:
        chain = self.trace(root_id, max_depth=max_depth)
        return list(dict.fromkeys(eid for node in chain.nodes for eid in node.evidence_ids))

    def explain(self, root_id: str, *, max_depth: int = 6) -> str:
        chain = self.trace(root_id, max_depth=max_depth)
        lines = [f"Root: {chain.root_id}"]
        for source, relation, target in chain.relations:
            lines.append(f"{source} --{relation}--> {target}")
        lines.append("Evidence: " + ", ".join(self.evidence_ids(root_id, max_depth=max_depth)))
        return "\n".join(lines)
