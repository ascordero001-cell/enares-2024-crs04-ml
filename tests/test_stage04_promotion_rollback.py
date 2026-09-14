from pathlib import Path

import pytest

from enares.stage04.release_lifecycle import (
    AUTOMATED_GATES,
    InMemoryReleaseBackend,
    ReleaseKey,
    ReleaseRecord,
    ReleaseStatus,
)


def candidate(name: str) -> ReleaseRecord:
    return ReleaseRecord(
        key=ReleaseKey(name, f"run-{name}"),
        source_version="v0_official_drive_baseline",
        source_hash="a" * 64,
    )


def pass_and_approve(backend: InMemoryReleaseBackend, record: ReleaseRecord) -> None:
    backend.register(record)
    for check in sorted(AUTOMATED_GATES):
        backend.record_validation(record.key, check, True)
    backend.approve(record.key, "supervisory-review")


def test_success_is_not_recorded_before_every_validation_finishes():
    backend = InMemoryReleaseBackend("V0")
    record = candidate("candidate-1")
    backend.register(record)
    final_check = max(AUTOMATED_GATES)
    for check in AUTOMATED_GATES - {final_check}:
        backend.record_validation(record.key, check, True)
        assert backend.history[0].status is ReleaseStatus.PENDING
    backend.record_validation(record.key, final_check, True)
    assert backend.history[0].status is ReleaseStatus.PASSED


def test_history_cannot_be_overwritten():
    backend = InMemoryReleaseBackend("V0")
    record = candidate("candidate-1")
    backend.register(record)
    with pytest.raises(ValueError, match="append-only"):
        backend.register(record)
    backend.record_validation(record.key, "technical", True)
    with pytest.raises(ValueError, match="cannot be overwritten"):
        backend.record_validation(record.key, "technical", False)


def test_only_approved_run_can_be_selected():
    backend = InMemoryReleaseBackend("V0")
    record = candidate("candidate-1")
    backend.register(record)
    with pytest.raises(ValueError, match="Only an APPROVED"):
        backend.promote(record.key, actor="ana", reason="practice")
    for check in AUTOMATED_GATES:
        backend.record_validation(record.key, check, True)
    with pytest.raises(ValueError, match="Only an APPROVED"):
        backend.promote(record.key, actor="ana", reason="practice")
    backend.approve(record.key, "review")
    backend.promote(record.key, actor="ana", reason="practice")
    assert backend.visible_record() == backend.history[0]


def test_rollback_changes_pointer_and_restores_previous_view():
    backend = InMemoryReleaseBackend("V0")
    first = candidate("candidate-1")
    second = candidate("candidate-2")
    pass_and_approve(backend, first)
    pass_and_approve(backend, second)
    backend.promote(first.key, actor="ana", reason="initial")
    backend.promote(second.key, actor="ana", reason="practice")
    backend.rollback(actor="ana", reason="smoke failure")
    assert backend.current == first.key
    assert backend.visible_record().key == first.key
    assert backend.pointer_events[-1].action == "ROLLBACK"
    assert backend.pointer_events[-1].previous == second.key


def test_v0_official_pointer_is_immutable_during_promotion_and_rollback():
    backend = InMemoryReleaseBackend("V0-OFFICIAL")
    first = candidate("candidate-1")
    second = candidate("candidate-2")
    pass_and_approve(backend, first)
    pass_and_approve(backend, second)
    backend.promote(first.key, actor="ana", reason="initial")
    backend.promote(second.key, actor="ana", reason="practice")
    backend.rollback(actor="ana", reason="practice")
    assert backend.official_v0_release_id == "V0-OFFICIAL"
    assert {record.key for record in backend.history} == {first.key, second.key}


def test_failed_validation_is_terminal_and_never_promotable():
    backend = InMemoryReleaseBackend("V0")
    record = candidate("candidate-failed")
    backend.register(record)
    backend.record_validation(record.key, "privacy", False)
    assert backend.history[0].status is ReleaseStatus.FAILED
    with pytest.raises(ValueError, match="Finalized"):
        backend.record_validation(record.key, "technical", True)
    with pytest.raises(ValueError, match="Only an APPROVED"):
        backend.promote(record.key, actor="ana", reason="must fail")


def test_dataform_release_tables_and_safe_current_view_are_declared():
    root = Path(__file__).resolve().parents[1]
    registry = (root / "dataform/definitions/ops/release_registry.sqlx").read_text()
    current = (root / "dataform/definitions/ops/current_release.sqlx").read_text()
    published = (
        root / "dataform/definitions/published/v_dashboard_current.sqlx"
    ).read_text()

    assert "CREATE TABLE IF NOT EXISTS" in registry
    assert "release_id STRING NOT NULL" in registry
    assert "approval_reference STRING" in registry
    assert "CREATE TABLE IF NOT EXISTS" in current
    assert "previous_release_id STRING" in current
    assert 'dependencies: ["current_release"]' in published
    assert 'estimates.validation_status = "APPROVED"' in published
    for field in (
        "estimate",
        "standard_error",
        "ci95_lower",
        "ci95_upper",
        "cv",
        "n_unweighted",
        "weighted_population",
    ):
        assert f"IF(estimates.suppress_flag, NULL, estimates.{field})" in published
    assert "survey_input" not in published
