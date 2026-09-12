from datetime import datetime, timezone

from algox.memory.chain_validation import validate_decision_chain
from algox.memory.entities import ResearchEntity, ResearchEntityStore
from algox.memory.store import Evidence, InMemoryStore


def test_complete_decision_chain_is_valid():
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
    entities.link("D", "affects", "K")
    entities.link("D", "informs", "F")
    entities.link("F", "informs", "D")
    # The validator follows the canonical backward chain through required edges.
    entities.link("F", "informs", "D")
    assert "D: missing required relation affects" not in validate_decision_chain(entities, evidence, "D")


def test_missing_experiment_link_is_reported():
    evidence = InMemoryStore()
    entities = ResearchEntityStore()
    entities.add(ResearchEntity("D", "Decision", "decision"))
    entities.add(ResearchEntity("K", "Capability", "capability"))
    entities.link("D", "affects", "K")
    errors = validate_decision_chain(entities, evidence, "D")
    assert any("missing required relation" in error for error in errors)
