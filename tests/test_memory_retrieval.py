from datetime import datetime, timezone

from algox.memory.retrieval import EvidenceRetriever
from tests.test_memory_benchmark import build_store


def test_evidence_bundle_contains_provenance():
    retriever = EvidenceRetriever(build_store())
    bundle = retriever.retrieve("broker API asynchronous order", limit=5)
    assert "E-002" in bundle.supporting_evidence
    assert bundle.temporal_as_of is None


def test_evidence_bundle_preserves_counter_evidence():
    retriever = EvidenceRetriever(build_store())
    bundle = retriever.retrieve("method X", limit=10)
    assert "E-004" in bundle.supporting_evidence
    assert "E-005" in bundle.counter_evidence or "E-006" in bundle.counter_evidence


def test_temporal_retrieval_excludes_future_memory():
    retriever = EvidenceRetriever(build_store())
    as_of = datetime(2026, 3, 1, tzinfo=timezone.utc)
    bundle = retriever.retrieve("broker API", as_of=as_of)
    assert "M-002" not in {m.id for m in bundle.memories}
    assert "M-001" in {m.id for m in bundle.memories}


def test_related_traversal_is_bounded():
    retriever = EvidenceRetriever(build_store())
    related = retriever.related("M-004", depth=1)
    assert [memory.id for memory in related] == ["M-005", "M-006"]
