from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.release_lifecycle import (
    AUTOMATED_GATES,
    InMemoryReleaseBackend,
    ReleaseKey,
    ReleaseRecord,
)
from enares.stage04.repository import (
    DemoRepository,
    RepositoryContractError,
)
from enares.stage04.repository_cache import ReleaseRunCache

ROOT = Path(__file__).resolve().parents[1]
DEMO_FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"


def _approve(backend: InMemoryReleaseBackend, key: ReleaseKey) -> None:
    backend.register(
        ReleaseRecord(
            key=key,
            source_version="synthetic-cache-test",
            source_hash="a" * 64,
        )
    )
    for check in AUTOMATED_GATES:
        backend.record_validation(key, check, True)
    backend.approve(key, "synthetic-review")


def test_cache_is_indexed_by_release_and_run() -> None:
    source_rows = DemoRepository(DEMO_FIXTURE).list_estimates("3.2")
    first = [replace(row, release_id="release-a", run_id="run-1") for row in source_rows]
    second = [replace(row, release_id="release-a", run_id="run-2") for row in source_rows]
    cache = ReleaseRunCache()

    first_key = cache.store(first)
    second_key = cache.store(second)

    assert first_key == ReleaseKey("release-a", "run-1")
    assert second_key == ReleaseKey("release-a", "run-2")
    assert {row.run_id for row in cache.get(first_key)} == {"run-1"}
    assert {row.run_id for row in cache.get(second_key)} == {"run-2"}


def test_cache_snapshot_is_immutable_and_cannot_be_overwritten() -> None:
    rows = DemoRepository(DEMO_FIXTURE).list_estimates("3.2")
    cache = ReleaseRunCache()
    key = cache.store(rows)

    with pytest.raises(RepositoryContractError, match="cannot be overwritten"):
        cache.store(rows)

    assert isinstance(cache.get(key), tuple)


def test_promotion_and_rollback_never_mix_cached_release_runs() -> None:
    source_rows = DemoRepository(DEMO_FIXTURE).list_estimates("3.2")
    first = [replace(row, release_id="release-1", run_id="run-1") for row in source_rows]
    second = [replace(row, release_id="release-2", run_id="run-2") for row in source_rows]
    cache = ReleaseRunCache()
    first_key = cache.store(first)
    second_key = cache.store(second)
    backend = InMemoryReleaseBackend("V0-OFFICIAL")
    _approve(backend, first_key)
    _approve(backend, second_key)

    backend.promote(first_key, actor="ana", reason="synthetic smoke")
    assert {row.release_id for row in cache.for_current(backend.current)} == {
        "release-1"
    }

    backend.promote(second_key, actor="ana", reason="synthetic smoke")
    assert {row.release_id for row in cache.for_current(backend.current)} == {
        "release-2"
    }

    backend.rollback(actor="ana", reason="synthetic rollback")
    restored = cache.for_current(backend.current)
    assert {row.release_id for row in restored} == {"release-1"}
    assert {row.run_id for row in restored} == {"run-1"}
