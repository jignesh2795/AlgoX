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
    entities.edges = [edge for edge in entities.edges if not (edge.source_id == "C" and edge.relation == "tested_by")]
    errors = validate_decision_chain(entities, evidence, "D")
    assert any("X" in error and "tested_by" in error for error in errors) or any("Experiment" in error for error in errors)


def test_missing_finding_is_reported_from_decision():
    entities, evidence = build_chain()
    entities.edges = [edge for edge in entities.edges if not (edge.source_id == "F" and edge.relation == "informs")]
    errors = validate_decision_chain(entities, evidence, "D")
    assert any("D" in error and "informs" in error for error in errors)


def test_missing_capability_target_is_reported():
    entities, evidence = build_chain()
    entities.edges = [edge for edge in entities.edges if not (edge.source_id == "D" and edge.relation == "affects")]
    errors = validate_decision_chain(entities, evidence, "D")
    assert any("D" in error and "affects" in error for error in errors)


def test_claim_without_evidence_is_reported():
    entities, evidence = build_chain()
    entities.entities["C"] = ResearchEntity("C", "Claim", "claim")
    errors = validate_decision_chain(entities, evidence, "D")
    assert "C: claim requires evidence" in errors
