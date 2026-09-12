from datetime import datetime, timezone

from algox.memory.benchmark import benchmark_decision_chain, benchmark_governance
from algox.memory.entities import ResearchEntity, ResearchEntityStore
from algox.memory.store import Evidence, InMemoryStore


def build_chain():
    evidence = InMemoryStore()
    evidence.add_evidence(Evidence("E-CHAIN", "benchmark", "claim", datetime(2026, 1, 1, tzinfo=timezone.utc), "C2"))
    entities = ResearchEntityStore()
    for entity in (
        ResearchEntity("C-CHAIN", "Claim", "method X may outperform baseline", ("E-CHAIN",)),
        ResearchEntity("EXP-CHAIN", "Experiment", "reproduction"),
        ResearchEntity("R-CHAIN", "Result", "advantage not reproduced"),
        ResearchEntity("F-CHAIN", "Finding", "reported advantage is not robust"),
        ResearchEntity("D-CHAIN", "Decision", "do not adopt without validation"),
        ResearchEntity("CAP-CHAIN", "Capability", "strategy validation"),
    ):
        entities.add(entity)
    entities.link("C-CHAIN", "tested_by", "EXP-CHAIN")
    entities.link("EXP-CHAIN", "produced", "R-CHAIN")
    entities.link("R-CHAIN", "supports", "F-CHAIN")
    entities.link("F-CHAIN", "informs", "D-CHAIN")
    entities.link("D-CHAIN", "affects", "CAP-CHAIN")
    return entities, evidence


def test_decision_chain_benchmarks_pass():
    entities, evidence = build_chain()
    results = benchmark_decision_chain(entities, evidence, "D-CHAIN")
    ratio_results = [r for r in results if r.unit == "ratio"]
    assert {r.workload for r in ratio_results} == {
        "W8 decision-chain reconstruction",
        "W9 experiment-to-decision tracing",
    }
    assert all(r.passed for r in ratio_results)


def test_governance_benchmarks_pass():
    entities, evidence = build_chain()
    results = benchmark_governance(entities, evidence)
    ratio_results = [r for r in results if r.unit == "ratio"]
    assert {r.workload for r in ratio_results} == {"G1 governance review", "G2 audit append"}
    assert all(r.passed for r in ratio_results)
