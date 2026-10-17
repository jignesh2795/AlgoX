from algox.memory.graph import MemoryGraph
from tests.test_memory_benchmark import build_store


def test_graph_projection_rebuilds_from_store():
    graph = MemoryGraph(build_store())
    assert ("M-004", "contradicts", "M-005") in {
        (edge.source, edge.relation, edge.target) for edge in graph.edges()
    }


def test_graph_finds_research_path():
    graph = MemoryGraph(build_store())
    assert graph.path("M-004", "M-006") == ["M-004", "M-006"]


def test_graph_is_bounded():
    graph = MemoryGraph(build_store())
    assert graph.path("M-004", "M-002", max_depth=1) is None
