import pytest

from algox.memory.entities import ResearchEntity, ResearchEntityStore


def test_first_class_chain_entities_and_edges():
    store = ResearchEntityStore()
    for entity in (
        ResearchEntity("C-001", "Claim", "Method X may outperform Y", ("E-004",)),
        ResearchEntity("F-001", "Finding", "Reproduction was negative", ("E-006",)),
        ResearchEntity("EXP-017", "Experiment", "Reproduce method X"),
        ResearchEntity("R-017", "Result", "Advantage not reproduced"),
        ResearchEntity("D-001", "Decision", "Do not adopt without validation"),
        ResearchEntity("CAP-001", "Capability", "Strategy validation"),
    ):
        store.add(entity)
    store.link("C-001", "tested_by", "EXP-017")
    store.link("EXP-017", "produced", "R-017")
    store.link("R-017", "supports", "F-001")
    store.link("F-001", "informs", "D-001")
    store.link("D-001", "affects", "CAP-001")

    assert store.neighbors("D-001", "affects")[0].id == "CAP-001"
    assert store.evidence_for("C-001") == ("E-004",)


def test_invalid_entity_type_is_rejected():
    with pytest.raises(ValueError):
        ResearchEntity("X", "Unknown", "bad")


def test_duplicate_edges_are_idempotent():
    store = ResearchEntityStore()
    store.add(ResearchEntity("A", "Claim", "a"))
    store.add(ResearchEntity("B", "Finding", "b"))
    store.link("A", "supports", "B")
    store.link("A", "supports", "B")
    assert len(store.edges) == 1
