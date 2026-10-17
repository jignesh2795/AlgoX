from datetime import datetime, timezone

from algox.memory.audit import AuditLog
from algox.memory.consolidation import ConsolidationProposal
from algox.memory.entities import ResearchEntityStore
from algox.memory.governance import KnowledgeGovernance
from algox.memory.store import Evidence, InMemoryStore
from algox.memory.governed_learning import govern_proposal


def build_governance():
    evidence = InMemoryStore()
    evidence.add_evidence(
        Evidence("E-1", "S-1", "fixture://learning", datetime(2026, 1, 1, tzinfo=timezone.utc))
    )
    return KnowledgeGovernance(ResearchEntityStore(), evidence)


def proposal():
    return ConsolidationProposal(
        id="CP-1",
        experience_id="EX-1",
        memory_type="procedural",
        content="Preserve provenance.",
        evidence_ids=("E-1",),
        reason="verified reusable experience",
        confidence="high",
    )


def test_governed_learning_records_proposal_and_review():
    governance = build_governance()
    audit = AuditLog()
    outcome = govern_proposal(
        proposal(), governance, audit,
        actor="learning-loop",
        reviewed_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
    )

    assert outcome.review.approved is True
    assert outcome.review.status == "approved"
    assert outcome.audit_event_ids == ("AUD-CP-1-PROPOSED", "AUD-CP-1-APPROVED")
    assert [event.event_type for event in audit.history("CP-1")] == ["PROPOSED", "APPROVED"]
    assert "CP-1" not in governance.entities.entities


def test_governed_learning_rejects_missing_evidence_and_audits_it():
    governance = build_governance()
    audit = AuditLog()
    bad = ConsolidationProposal(
        id="CP-2",
        experience_id="EX-2",
        memory_type="procedural",
        content="Unsupported lesson.",
        evidence_ids=("E-MISSING",),
        reason="missing evidence",
        confidence="unknown",
    )
    outcome = govern_proposal(bad, governance, audit)

    assert outcome.review.approved is False
    assert outcome.review.status == "rejected"
    assert [event.event_type for event in audit.history("CP-2")] == ["PROPOSED", "REJECTED"]
    assert "E-MISSING" in outcome.review.errors[0]
