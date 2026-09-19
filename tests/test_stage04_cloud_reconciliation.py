from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any

from google.api_core.exceptions import Forbidden

from enares.stage04.cloud_reconciliation import reconcile_existing_snapshot
from enares.stage04.shadow_pipeline import PipelineInputContract

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app" / "data"
AGGREGATE = DATA / "v0_authorized_full_indicator_estimates.csv"
MANIFEST = DATA / "v0_authorized_full_indicator_estimates.manifest.json"
REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
WORKFLOW = ROOT / ".github" / "workflows" / "stage04-shadow-reconcile.yml"
EXPECTED_BYTES = 3_308_972


class _FakeJob:
    def __init__(
        self,
        rows: list[dict[str, str]],
        processed_bytes: int,
        *,
        fail: bool = False,
    ) -> None:
        self._rows = rows
        self.total_bytes_processed = processed_bytes
        self.cache_hit = False
        self._fail = fail

    def result(self) -> list[dict[str, str]]:
        if self._fail:
            raise Forbidden("sensitive provider detail must not be emitted")
        return self._rows


class _FakeClient:
    def __init__(self, *, alter_first_row: bool = False, fail: bool = False) -> None:
        with AGGREGATE.open(encoding="utf-8", newline="") as handle:
            self.rows = list(csv.DictReader(handle))
        self.alter_first_row = alter_first_row
        self.fail = fail
        self.configs: list[Any] = []

    def query(self, query: str, *, job_config: Any) -> _FakeJob:
        del query
        self.configs.append(job_config)
        parameters = {item.name: item.value for item in job_config.query_parameters}
        module_rows = [
            {key: value for key, value in row.items() if key != "synthetic"}
            for row in self.rows
            if row["module_id"] == parameters["module_id"]
        ]
        if self.alter_first_row and not any(
            row.get("indicator_name") == "changed" for row in module_rows
        ):
            module_rows[0]["indicator_name"] = "changed"
            self.alter_first_row = False
        index = len(self.configs) - 1
        processed_bytes = 551_495 + (1 if index < 2 else 0)
        return _FakeJob(module_rows, processed_bytes, fail=self.fail)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _contract() -> PipelineInputContract:
    return PipelineInputContract(
        release_id="enares2024-crs04-v0-shadow-001",
        run_id="pr-b-full-v0-authorized-20260916",
        aggregate_sha256=_sha256(AGGREGATE),
        manifest_sha256=_sha256(MANIFEST),
        parent_sha256="15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4",
        expected_row_count=3014,
        expected_indicator_count=516,
        decision_reference="https://github.com/example/repository/issues/43#issuecomment-1",
        decision_commit="a" * 40,
    )


def test_reconcile_existing_snapshot_passes_with_exact_parity_and_bytes() -> None:
    client = _FakeClient()

    evidence = reconcile_existing_snapshot(
        _contract(),
        aggregate_path=AGGREGATE,
        manifest_path=MANIFEST,
        approval_registry_path=REGISTRY,
        table_fqn=(
            "enares-2024-crs04."
            "enares2024_crs04_stage04_shadow_outputs.indicator_estimates"
        ),
        expected_total_bytes_processed=EXPECTED_BYTES,
        client=client,
    )

    assert evidence.status == "PASS_RECONCILE_EXISTING"
    assert evidence.row_count == 3014
    assert evidence.indicator_count == 516
    assert set(evidence.gates.values()) == {"PASS"}
    assert len(client.configs) == 6
    assert all(config.use_query_cache is False for config in client.configs)


def test_reconcile_existing_snapshot_holds_on_content_difference() -> None:
    evidence = reconcile_existing_snapshot(
        _contract(),
        aggregate_path=AGGREGATE,
        manifest_path=MANIFEST,
        approval_registry_path=REGISTRY,
        table_fqn=(
            "enares-2024-crs04."
            "enares2024_crs04_stage04_shadow_outputs.indicator_estimates"
        ),
        expected_total_bytes_processed=EXPECTED_BYTES,
        client=_FakeClient(alter_first_row=True),
    )

    assert evidence.status == "HOLD"
    assert evidence.gates["v0_parity"] == "HOLD"


def test_reconciliation_job_is_main_only_and_environment_protected() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "if: github.ref == 'refs/heads/main'" in workflow
    assert "name: stage04-shadow-mutation" in workflow
    assert "reconcile_stage04_shadow_existing.py" in workflow
    assert (
        "--table-fqn enares-2024-crs04."
        "enares2024_crs04_stage04_shadow_outputs.indicator_estimates"
    ) in workflow
    assert "if: always()" in workflow
    assert "load_table_from_file" not in workflow
    assert "bq load" not in workflow


def test_reconcile_existing_snapshot_emits_redacted_hold_on_provider_failure() -> None:
    evidence = reconcile_existing_snapshot(
        _contract(),
        aggregate_path=AGGREGATE,
        manifest_path=MANIFEST,
        approval_registry_path=REGISTRY,
        table_fqn=(
            "enares-2024-crs04."
            "enares2024_crs04_stage04_shadow_outputs.indicator_estimates"
        ),
        expected_total_bytes_processed=EXPECTED_BYTES,
        client=_FakeClient(fail=True),
    )

    assert evidence.status == "HOLD"
    assert evidence.gates["technical"] == "HOLD"
    assert evidence.failure_class == "Forbidden"
    assert "sensitive provider detail" not in evidence.as_json()
    assert "sensitive provider detail" not in evidence.as_markdown()
