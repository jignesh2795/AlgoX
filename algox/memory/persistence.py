"""Persistence adapter contract for AlgoX memory.

The adapter mirrors the reference InMemoryStore semantics without forcing a
specific database on callers. The first implementation is an in-process
SQLite adapter, useful for local experiments and restart/durability checks.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from .store import Evidence, KnowledgeDelta, MemoryRecord


class SQLiteMemoryStore:
    """Small durable adapter implementing the core memory persistence contract."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                locator TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                maturity TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                confidence TEXT NOT NULL,
                valid_from TEXT,
                valid_to TEXT,
                status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memory_evidence (
                memory_id TEXT NOT NULL REFERENCES memories(id),
                evidence_id TEXT NOT NULL REFERENCES evidence(id),
                PRIMARY KEY(memory_id, evidence_id)
            );
            CREATE TABLE IF NOT EXISTS memory_relations (
                source_id TEXT NOT NULL REFERENCES memories(id),
                relation TEXT NOT NULL,
                target_id TEXT NOT NULL REFERENCES memories(id),
                PRIMARY KEY(source_id, relation, target_id)
            );
            CREATE TABLE IF NOT EXISTS deltas (
                id TEXT PRIMARY KEY,
                operation TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                evidence_ids TEXT NOT NULL,
                reason TEXT NOT NULL,
                confidence TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    @staticmethod
    def _dt(value: str | None) -> datetime | None:
        return datetime.fromisoformat(value) if value else None

    def add_evidence(self, evidence: Evidence) -> None:
        self.db.execute(
            "INSERT INTO evidence VALUES (?, ?, ?, ?, ?)",
            (
                evidence.id,
                evidence.source_id,
                evidence.locator,
                evidence.observed_at.isoformat(),
                evidence.maturity,
            ),
        )
        self.db.commit()

    def add_memory(self, memory: MemoryRecord) -> None:
        missing = [
            eid
            for eid in memory.evidence_ids
            if self.db.execute(
                "SELECT 1 FROM evidence WHERE id=?", (eid,)
            ).fetchone()
            is None
        ]
        if missing:
            raise ValueError(f"missing evidence: {sorted(missing)}")

        missing_targets = [
            target_id
            for _, target_id in memory.relations
            if self.db.execute(
                "SELECT 1 FROM memories WHERE id=?", (target_id,)
            ).fetchone()
            is None
        ]
        if missing_targets:
            raise ValueError(
                f"missing relation targets: {sorted(set(missing_targets))}"
            )

        try:
            self.db.execute(
                "INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    memory.id,
                    memory.memory_type,
                    memory.content,
                    memory.created_at.isoformat(),
                    memory.confidence,
                    memory.valid_from.isoformat() if memory.valid_from else None,
                    memory.valid_to.isoformat() if memory.valid_to else None,
                    memory.status,
                ),
            )
            self.db.executemany(
                "INSERT INTO memory_evidence VALUES (?, ?)",
                [(memory.id, eid) for eid in memory.evidence_ids],
            )
            self.db.executemany(
                "INSERT INTO memory_relations VALUES (?, ?, ?)",
                [
                    (memory.id, relation, target_id)
                    for relation, target_id in memory.relations
                ],
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def link_memory(self, source_id: str, relation: str, target_id: str) -> None:
        for memory_id in (source_id, target_id):
            if self.db.execute(
                "SELECT 1 FROM memories WHERE id=?", (memory_id,)
            ).fetchone() is None:
                raise KeyError("both memory endpoints must exist")
        self.db.execute(
            "INSERT OR IGNORE INTO memory_relations VALUES (?, ?, ?)",
            (source_id, relation, target_id),
        )
        self.db.commit()

    def get_memory(self, memory_id: str) -> MemoryRecord:
        row = self.db.execute(
            "SELECT id, memory_type, content, created_at, confidence, valid_from, valid_to, status "
            "FROM memories WHERE id=?",
            (memory_id,),
        ).fetchone()
        if row is None:
            raise KeyError(memory_id)

        evidence_ids = [
            r[0]
            for r in self.db.execute(
                "SELECT evidence_id FROM memory_evidence "
                "WHERE memory_id=? ORDER BY evidence_id",
                (memory_id,),
            )
        ]
        relations = [
            (r[0], r[1])
            for r in self.db.execute(
                "SELECT relation, target_id FROM memory_relations "
                "WHERE source_id=? ORDER BY relation, target_id",
                (memory_id,),
            )
        ]
        return MemoryRecord(
            id=row[0],
            memory_type=row[1],
            content=row[2],
            created_at=datetime.fromisoformat(row[3]),
            confidence=row[4],
            valid_from=self._dt(row[5]),
            valid_to=self._dt(row[6]),
            evidence_ids=evidence_ids,
            status=row[7],
            relations=relations,
        )

    def reconstruct_as_of(self, as_of: datetime) -> list[MemoryRecord]:
        rows = self.db.execute("SELECT id FROM memories ORDER BY id").fetchall()
        result = []
        for (memory_id,) in rows:
            memory = self.get_memory(memory_id)
            if (
                (memory.valid_from is None or memory.valid_from <= as_of)
                and (memory.valid_to is None or as_of < memory.valid_to)
            ):
                result.append(memory)
        return result

    def add_delta(self, delta: KnowledgeDelta) -> None:
        self.db.execute(
            "INSERT INTO deltas VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                delta.id,
                delta.operation,
                delta.entity_type,
                delta.entity_id,
                json.dumps(delta.evidence_ids),
                delta.reason,
                delta.confidence,
            ),
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()
