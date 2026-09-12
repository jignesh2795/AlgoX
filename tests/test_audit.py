from datetime import datetime, timezone

import pytest

from algox.memory.audit import AuditLog, GovernanceEvent


def test_audit_log_is_append_only_and_ordered():
    log = AuditLog()
    first = GovernanceEvent("EV-1", "PROPOSED", "D-1", "model", datetime(2026, 1, 1, tzinfo=timezone.utc))
    second = GovernanceEvent("EV-2", "REVIEWED", "D-1", "reviewer", datetime(2026, 1, 2, tzinfo=timezone.utc))
    log.append(first)
    log.append(second)
    assert log.history("D-1") == (first, second)
    with pytest.raises(ValueError, match="already exists"):
        log.append(first)


def test_invalid_event_type_is_rejected():
    with pytest.raises(ValueError, match="unsupported governance event type"):
        GovernanceEvent("EV-1", "MUTATED", "D-1", "reviewer", datetime.now(timezone.utc))


def test_empty_actor_is_rejected():
    with pytest.raises(ValueError, match="actor"):
        GovernanceEvent("EV-1", "APPROVED", "D-1", " ", datetime.now(timezone.utc))
