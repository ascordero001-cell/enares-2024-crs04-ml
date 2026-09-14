"""Local promotion and rollback state machine with an append-only memory backend."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum

AUTOMATED_GATES = frozenset(
    {"technical", "v0_parity", "privacy", "release_consistency"}
)


class ReleaseStatus(StrEnum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    APPROVED = "APPROVED"


@dataclass(frozen=True)
class ReleaseKey:
    release_id: str
    run_id: str


@dataclass(frozen=True)
class ReleaseRecord:
    key: ReleaseKey
    source_version: str
    source_hash: str
    status: ReleaseStatus = ReleaseStatus.PENDING
    approval_reference: str | None = None


@dataclass(frozen=True)
class PointerEvent:
    action: str
    selected: ReleaseKey
    previous: ReleaseKey | None
    actor: str
    reason: str
    occurred_at: str


class InMemoryReleaseBackend:
    """Exercise lifecycle rules without DDL, credentials or cloud access."""

    def __init__(self, official_v0_release_id: str) -> None:
        self._official_v0_release_id = official_v0_release_id
        self._records: dict[ReleaseKey, ReleaseRecord] = {}
        self._checks: dict[ReleaseKey, dict[str, bool]] = {}
        self._current: ReleaseKey | None = None
        self._events: list[PointerEvent] = []

    @property
    def official_v0_release_id(self) -> str:
        return self._official_v0_release_id

    @property
    def current(self) -> ReleaseKey | None:
        return self._current

    @property
    def history(self) -> tuple[ReleaseRecord, ...]:
        return tuple(self._records.values())

    @property
    def pointer_events(self) -> tuple[PointerEvent, ...]:
        return tuple(self._events)

    def register(self, record: ReleaseRecord) -> None:
        if record.key in self._records:
            raise ValueError("Release history is append-only; duplicate run rejected")
        if record.status is not ReleaseStatus.PENDING:
            raise ValueError("A new release must be registered as PENDING")
        self._records[record.key] = record
        self._checks[record.key] = {}

    def record_validation(self, key: ReleaseKey, check: str, passed: bool) -> None:
        if check not in AUTOMATED_GATES:
            raise ValueError("Unknown blocking validation")
        record = self._require_record(key)
        if record.status in {ReleaseStatus.FAILED, ReleaseStatus.APPROVED}:
            raise ValueError("Finalized validation state cannot be overwritten")
        checks = self._checks[key]
        if check in checks:
            raise ValueError("Validation history cannot be overwritten")
        checks[check] = passed
        if not passed:
            self._records[key] = replace(record, status=ReleaseStatus.FAILED)
        elif checks.keys() == AUTOMATED_GATES and all(checks.values()):
            self._records[key] = replace(record, status=ReleaseStatus.PASSED)

    def approve(self, key: ReleaseKey, approval_reference: str) -> None:
        record = self._require_record(key)
        if record.status is not ReleaseStatus.PASSED:
            raise ValueError("Only a fully validated PASSED release can be approved")
        if not approval_reference.strip():
            raise ValueError("Approval requires a review reference")
        self._records[key] = replace(
            record,
            status=ReleaseStatus.APPROVED,
            approval_reference=approval_reference,
        )

    def promote(self, key: ReleaseKey, *, actor: str, reason: str) -> None:
        record = self._require_record(key)
        if record.status is not ReleaseStatus.APPROVED:
            raise ValueError("Only an APPROVED release can be promoted")
        self._move_pointer("PROMOTE", key, actor, reason)

    def rollback(self, *, actor: str, reason: str) -> None:
        if self._current is None:
            raise ValueError("Rollback requires a current release")
        target = next(
            (
                event.previous
                for event in reversed(self._events)
                if event.action == "PROMOTE"
                and event.selected == self._current
                and event.previous is not None
            ),
            None,
        )
        if target is None:
            raise ValueError("No previous approved release is available")
        if self._require_record(target).status is not ReleaseStatus.APPROVED:
            raise ValueError("Rollback target is no longer approved")
        self._move_pointer("ROLLBACK", target, actor, reason)

    def visible_record(self) -> ReleaseRecord | None:
        return self._records.get(self._current) if self._current else None

    def _move_pointer(
        self, action: str, selected: ReleaseKey, actor: str, reason: str
    ) -> None:
        if not actor.strip() or not reason.strip():
            raise ValueError("Pointer changes require actor and reason")
        previous = self._current
        self._current = selected
        self._events.append(
            PointerEvent(
                action=action,
                selected=selected,
                previous=previous,
                actor=actor,
                reason=reason,
                occurred_at=datetime.now(UTC).isoformat(),
            )
        )

    def _require_record(self, key: ReleaseKey) -> ReleaseRecord:
        try:
            return self._records[key]
        except KeyError as exc:
            raise ValueError("Release run is not registered") from exc
