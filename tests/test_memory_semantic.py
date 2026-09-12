from algox.memory.semantic import SemanticRetriever
from tests.test_memory_benchmark import build_store


def test_semantic_baseline_handles_related_terms():
    retriever = SemanticRetriever(build_store())
    matches = retriever.search("asynchronous broker order", limit=3)
    assert matches
    assert matches[0].memory.id in {"M-001", "M-002", "M-003"}


def test_semantic_results_are_deterministic():
    retriever = SemanticRetriever(build_store())
    first = [(m.memory.id, m.score) for m in retriever.search("method X", limit=10)]
    second = [(m.memory.id, m.score) for m in retriever.search("method X", limit=10)]
    assert first == second
