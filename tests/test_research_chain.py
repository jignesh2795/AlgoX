from algox.memory.research_chain import ResearchChainResolver
from tests.test_memory_benchmark import build_store


def test_trace_reconstructs_evidence_chain():
    resolver = ResearchChainResolver(build_store())
    chain = resolver.trace("M-004")
    assert {node.id for node in chain.nodes} == {"M-004", "M-005", "M-006"}
    assert "E-004" in resolver.evidence_ids("M-004")
    assert "E-006" in resolver.evidence_ids("M-004")


def test_explanation_is_auditable():
    resolver = ResearchChainResolver(build_store())
    explanation = resolver.explain("M-004")
    assert "M-004 --contradicts--> M-005" in explanation
    assert "M-004 --tested_by--> M-006" in explanation
    assert "E-004" in explanation
