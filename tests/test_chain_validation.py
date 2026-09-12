from datetime import datetime, timezone

from algox.memory.chain_validation import validate_decision_chain
from algox.memory.entities import ResearchEntity, ResearchEntityStore
from algox.memory.store import Evidence, InMemoryStore


def build_chain():
    evidence = InMemoryStore()
    evidence.add_evidence(Evidence("E-1", "S-1", "claim", datetime(2026, 1, 1, tzinfo=timezone.utc)))
    evidence.add_evidence(Evidence("E-2", "S-2", "result", datetime(2026, 1, 2, tzinfo=timezone.utc)))
    entities = ResearchEntityStore()
    entities.add(ResearchEntity("C", "Claim", "claim", ("E-1",)))
    entities.add(ResearchEntity("X", "Experiment", "experiment"))
    entities.add(ResearchEntity("R", "Result", "result", ("E-2",)))
    entities.add(ResearchEntity("F", "Finding", "finding"))
    entities.add(ResearchEntity("D", "Decision", "decision"))
    entities.add(ResearchEntity("K", "Capability", "capability"))
    entities.link("C", "tested_by", "X")
    entities.link("X", "produced", "R")
    entities.link("R", "supports", "F")
    entities.link("F", "informs", "D")
    entities.link("D", "affects", "K")
    return entities, evidence


def test_complete_decision_chain_is_valid():
    entities, evidence = build_chain()
    assert validate_decision_chain(entities, evidence, "D") == []


def test_missing_experiment_link_is_reported():
    entities, evidence = build_chain()
    entities.edges = [edge for edge in entities.edges if edge.source_id != "C"]
    errors = validate_decision_chain(entities, evidence, "D")
    assert any("C" in error and "tested_by" in error for error in errors)
