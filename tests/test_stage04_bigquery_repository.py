from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pytest

from enares.stage04.repository import (
    BIGQUERY_MAXIMUM_BYTES_BILLED,
    BigQueryRepository,
    RepositoryContractError,
    is_verified_authorized_estimate,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app" / "data"
FULL_EXTRACT = DATA / "v0_authorized_full_indicator_estimates.csv"
FULL_MANIFEST = DATA / "v0_authorized_full_indicator_estimates.manifest.json"
APPROVAL_REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
TABLE_FQN = "project-id.stage04_shadow_published.indicator_estimates"


class _FakeJob:
    def __init__(self, rows: list[dict[str, str]]) -> None:
        self.rows = rows

    def result(self) -> list[dict[str, str]]:
        return self.rows


class _FakeClient:
    def __init__(self, rows: list[dict[str, str]]) -> None:
        self.rows = rows
        self.queries: list[tuple[str, Any]] = []

    def query(self, query: str, *, job_config: Any) -> _FakeJob:
        self.queries.append((query, job_config))
        return _FakeJob(self.rows)


def _module_rows(module_id: str) -> list[dict[str, str]]:
    with FULL_EXTRACT.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["module_id"] == module_id]
    for row in rows:
        row.pop("synthetic")
    return rows


def _repository(client: _FakeClient) -> BigQueryRepository:
    return BigQueryRepository(
        table_fqn=TABLE_FQN,
        release_id="enares2024-crs04-v0-shadow-001",
        run_id="pr-b-full-v0-authorized-20260916",
        manifest_path=FULL_MANIFEST,
        approval_registry_path=APPROVAL_REGISTRY,
        client=client,
    )


def test_bigquery_repository_uses_parameters_cap_and_verified_provenance() -> None:
    client = _FakeClient(_module_rows("3.2"))

    rows = _repository(client).list_estimates("3.2")

    assert len(rows) == 389
    assert all(is_verified_authorized_estimate(row) for row in rows)
    assert all(row.synthetic is False for row in rows)
    assert len(client.queries) == 1
    query, job_config = client.queries[0]
    assert f"FROM `{TABLE_FQN}`" in query
    assert "module_id = @module_id" in query
    assert "source_hash = @source_hash" in query
    assert job_config.maximum_bytes_billed == BIGQUERY_MAXIMUM_BYTES_BILLED
    assert job_config.use_query_cache is True
    parameters = {parameter.name: parameter.value for parameter in job_config.query_parameters}
    assert parameters["module_id"] == "3.2"
    assert parameters["release_id"] == "enares2024-crs04-v0-shadow-001"
    assert parameters["run_id"] == "pr-b-full-v0-authorized-20260916"
    assert parameters["source_hash"] == rows[0].source_hash


def test_bigquery_repository_fails_closed_on_partial_module() -> None:
    rows = _module_rows("3.2")[:-1]

    with pytest.raises(RepositoryContractError):
        _repository(_FakeClient(rows)).list_estimates("3.2")


def test_bigquery_repository_rejects_identifier_injection() -> None:
    with pytest.raises(RepositoryContractError):
        BigQueryRepository(
            table_fqn="project.dataset.table` WHERE TRUE --",
            release_id="release",
            run_id="run",
            manifest_path=FULL_MANIFEST,
            approval_registry_path=APPROVAL_REGISTRY,
            client=_FakeClient([]),
        )


def test_bigquery_repository_rejects_unknown_module_without_query() -> None:
    client = _FakeClient([])

    with pytest.raises(RepositoryContractError):
        _repository(client).list_estimates("3.7")

    assert client.queries == []
