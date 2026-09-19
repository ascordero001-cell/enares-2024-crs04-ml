from __future__ import annotations

from pathlib import Path
from typing import Any

from google.api_core.exceptions import Forbidden, NotFound

from enares.stage04.cloud_metadata_preflight import preflight_bigquery_metadata

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "stage04-metadata-preflight.yml"


class _FakeClient:
    def __init__(self, failures: dict[str, BaseException] | None = None) -> None:
        self.failures = failures or {}
        self.calls: list[tuple[str, str]] = []

    def _call(self, kind: str, identity: str) -> list[Any]:
        self.calls.append((kind, identity))
        if kind in self.failures:
            raise self.failures[kind]
        return []

    def list_datasets(self, *, project: str, max_results: int) -> list[Any]:
        assert max_results == 1
        return self._call("project", project)

    def get_dataset(self, identity: str) -> object:
        self._call("dataset", identity)
        return object()

    def get_table(self, identity: str) -> object:
        self._call("table", identity)
        return object()


def test_metadata_preflight_checks_each_resource_without_querying_rows() -> None:
    client = _FakeClient()

    evidence = preflight_bigquery_metadata(
        client=client,
        project_id="enares-2024-crs04",
        dataset_id="enares2024_crs04_stage04_shadow_outputs",
        table_id="indicator_estimates",
    )

    assert evidence.status == "PASS"
    assert evidence.rows_read == 0
    assert evidence.ddl_dml_executed is False
    assert client.calls == [
        ("project", "enares-2024-crs04"),
        (
            "dataset",
            "enares-2024-crs04.enares2024_crs04_stage04_shadow_outputs",
        ),
        (
            "table",
            "enares-2024-crs04.enares2024_crs04_stage04_shadow_outputs.indicator_estimates",
        ),
    ]
    assert not hasattr(client, "query")


def test_metadata_preflight_stops_after_project_failure_and_redacts_detail() -> None:
    client = _FakeClient(
        {"project": Forbidden("principal and provider details must stay private")}
    )

    evidence = preflight_bigquery_metadata(
        client=client,
        project_id="enares-2024-crs04",
        dataset_id="enares2024_crs04_stage04_shadow_outputs",
        table_id="indicator_estimates",
    )

    assert evidence.status == "HOLD"
    assert evidence.project.failure_class == "Forbidden"
    assert evidence.dataset.failure_class == "NOT_CHECKED"
    assert evidence.table.failure_class == "NOT_CHECKED"
    assert "principal" not in evidence.as_json()


def test_metadata_preflight_distinguishes_missing_table_without_leaking_detail() -> None:
    client = _FakeClient({"table": NotFound("sensitive provider response")})

    evidence = preflight_bigquery_metadata(
        client=client,
        project_id="enares-2024-crs04",
        dataset_id="enares2024_crs04_stage04_shadow_outputs",
        table_id="indicator_estimates",
    )

    assert evidence.status == "HOLD"
    assert evidence.project.accessible
    assert evidence.dataset.accessible
    assert evidence.table.failure_class == "NotFound"
    assert "sensitive provider response" not in evidence.as_json()


def test_metadata_preflight_workflow_is_protected_and_contains_no_data_operations() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "if: github.ref == 'refs/heads/main'" in workflow
    assert "name: stage04-shadow-mutation" in workflow
    assert "enares-2024-crs04" in workflow
    assert "enares2024_crs04_stage04_shadow_outputs" in workflow
    assert "indicator_estimates" in workflow
    assert "preflight_stage04_bigquery_metadata.py" in workflow
    for forbidden in ("query(", "SELECT ", "INSERT ", "UPDATE ", "DELETE ", "bq load"):
        assert forbidden not in workflow
