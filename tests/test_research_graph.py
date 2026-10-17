from datetime import datetime, timezone

from algox.memory.entities import ResearchEntity, ResearchEntityStore
from algox.memory.research_graph import ValidatedResearchGraph
from algox.memory.store import Evidence, InMemoryStore


def build_graph():
    evidence = InMemoryStore()
    for item in (
        Evidence("E-1", "SRC-1", "claim.md", datetime(2026, 1, 1, tzinfo=timezone.utc)),
        Evidence("E-2", "SRC-2", "experiment.md", datetime(2026, 2, 1, tzinfo=timezone.utc)),
    ):
        evidence.add_evidence(item)
    entities = ResearchEntityStore()
    entities.add(ResearchEntity("C-1", "Claim", "claim", ("E-1",)))
    entities.add(ResearchEntity("F-1", "Finding", "finding", ("E-2",)))
    entities.add(ResearchEntity("D-1", "Decision", "decision"))
    entities.add(ResearchEntity("CAP-1", "Capability", "capability"))
    entities.link("C-1", "supports", "F-1")
    entities.link("F-1", "informs", "D-1")
    entities.link("D-1", "affects", "CAP-1")
    return ValidatedResearchGraph(entities, evidence)


def test_validation_and_full_path():
    graph = build_graph()
    assert graph.validate() == []
    path = graph.path("C-1", "CAP-1")
    assert path is not None
    assert path.node_ids == ("C-1", "F-1", "D-1", "CAP-1")
    assert path.evidence_ids == ("E-1", "E-2")


def test_temporal_validation_rejects_future_evidence():
    graph = build_graph()
    path = graph.path("C-1", "CAP-1")
    assert path is not None
    assert graph.path_is_valid_as_of(path, datetime(2026, 1, 15, tzinfo=timezone.utc)) is False
    assert graph.path_is_valid_as_of(path, datetime(2026, 3, 1, tzinfo=timezone.utc)) is True
