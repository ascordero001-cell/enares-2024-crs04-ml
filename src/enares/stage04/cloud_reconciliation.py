"""Fail-closed reconciliation of an existing Stage 04 BigQuery snapshot."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

from .repository import (
    BIGQUERY_MAXIMUM_BYTES_BILLED,
    AuthorizedAggregateRepository,
    BigQueryRepository,
    IndicatorEstimate,
)
from .shadow_pipeline import (
    MODULE_IDS,
    PipelineInputContract,
    prepare_authorized_aggregate,
)
from .validation import validate_estimates

_FLOAT_FIELDS = {
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "weighted_population",
}


@dataclass(frozen=True)
class CloudReconciliationEvidence:
    """Redacted evidence; job identifiers and principals are intentionally absent."""

    status: str
    mode: str
    release_id: str
    run_id: str
    row_count: int
    indicator_count: int
    module_row_counts: dict[str, int]
    total_bytes_processed: int
    expected_total_bytes_processed: int
    cache_hits: int
    gates: dict[str, str]

    def as_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def as_markdown(self) -> str:
        gates = "\n".join(f"- {name}: `{value}`" for name, value in self.gates.items())
        return (
            "# Reconciliación automatizada Stage 04\n\n"
            f"- Estado: `{self.status}`\n"
            f"- Modo: `{self.mode}`\n"
            f"- Release/run: `{self.release_id}` / `{self.run_id}`\n"
            f"- Filas/indicadores: {self.row_count} / {self.indicator_count}\n"
            f"- Bytes procesados: {self.total_bytes_processed}\n"
            f"- Bytes esperados: {self.expected_total_bytes_processed}\n"
            f"- Cache hits: {self.cache_hits}\n\n"
            "## Gates\n\n"
            f"{gates}\n\n"
            "No se cargaron filas ni se ejecutaron promoción, rollback, IAM, tráfico o "
            "publicación. La evidencia omite datos, rutas privadas, principals y job IDs.\n"
        )


class TrackingBigQueryClient:
    """Delegate queries while retaining only non-sensitive billing metadata."""

    def __init__(self, client: Any) -> None:
        self._client = client
        self.queries: list[tuple[Any, Any]] = []

    def query(self, query: str, *, job_config: Any) -> Any:
        job = self._client.query(query, job_config=job_config)
        self.queries.append((job, job_config))
        return job


def _row_key(row: IndicatorEstimate) -> tuple[str, str, str, str]:
    return row.module_id, row.indicator_id, row.disaggregation, row.category


def _rows_match(
    expected: IndicatorEstimate,
    actual: IndicatorEstimate,
    *,
    tolerance: float,
) -> bool:
    for field in fields(IndicatorEstimate):
        expected_value = getattr(expected, field.name)
        actual_value = getattr(actual, field.name)
        if field.name in _FLOAT_FIELDS and expected_value is not None and actual_value is not None:
            if abs(float(expected_value) - float(actual_value)) > tolerance:
                return False
        elif expected_value != actual_value:
            return False
    return True


def reconcile_existing_snapshot(
    contract: PipelineInputContract,
    *,
    aggregate_path: Path,
    manifest_path: Path,
    approval_registry_path: Path,
    table_fqn: str,
    expected_total_bytes_processed: int,
    client: Any,
    tolerance: float = 1e-9,
) -> CloudReconciliationEvidence:
    """Compare the approved aggregate with cloud without writing cloud state."""
    contract.validate()
    if expected_total_bytes_processed <= 0:
        raise ValueError("expected_total_bytes_processed must be positive")

    prepare_authorized_aggregate(
        contract,
        aggregate_path=aggregate_path,
        manifest_path=manifest_path,
        approval_registry_path=approval_registry_path,
    )

    local_repository = AuthorizedAggregateRepository(
        aggregate_path,
        manifest_path,
        approval_registry_path,
    )
    tracking_client = TrackingBigQueryClient(client)
    cloud_repository = BigQueryRepository(
        table_fqn=table_fqn,
        release_id=contract.release_id,
        run_id=contract.run_id,
        manifest_path=manifest_path,
        approval_registry_path=approval_registry_path,
        client=tracking_client,
        use_query_cache=False,
    )

    local_rows: list[IndicatorEstimate] = []
    cloud_rows: list[IndicatorEstimate] = []
    module_row_counts: dict[str, int] = {}
    for module_id in MODULE_IDS:
        expected_rows = local_repository.list_estimates(module_id)
        actual_rows = cloud_repository.list_estimates(module_id)
        module_row_counts[module_id] = len(actual_rows)
        local_rows.extend(expected_rows)
        cloud_rows.extend(actual_rows)

    validate_estimates(cloud_rows)
    local_rows.sort(key=_row_key)
    cloud_rows.sort(key=_row_key)
    parity = len(local_rows) == len(cloud_rows) and all(
        _rows_match(expected, actual, tolerance=tolerance)
        for expected, actual in zip(local_rows, cloud_rows, strict=True)
    )
    cache_hits = sum(
        bool(getattr(job, "cache_hit", False)) for job, _ in tracking_client.queries
    )
    total_bytes = sum(
        int(getattr(job, "total_bytes_processed", 0) or 0)
        for job, _ in tracking_client.queries
    )
    gates = {
        "technical": "PASS",
        "v0_parity": "PASS" if parity else "HOLD",
        "privacy": "PASS"
        if all(not row.synthetic and not row.suppress_flag for row in cloud_rows)
        else "HOLD",
        "release_consistency": "PASS"
        if {row.release_id for row in cloud_rows} == {contract.release_id}
        and {row.run_id for row in cloud_rows} == {contract.run_id}
        else "HOLD",
        "query_cost_cap": "PASS"
        if tracking_client.queries
        and all(
            config.maximum_bytes_billed == BIGQUERY_MAXIMUM_BYTES_BILLED
            and config.use_query_cache is False
            for _, config in tracking_client.queries
        )
        and cache_hits == 0
        else "HOLD",
    }
    if total_bytes != expected_total_bytes_processed:
        gates["query_cost_cap"] = "HOLD"
    status = "PASS_RECONCILE_EXISTING" if set(gates.values()) == {"PASS"} else "HOLD"
    return CloudReconciliationEvidence(
        status=status,
        mode="RECONCILE_EXISTING",
        release_id=contract.release_id,
        run_id=contract.run_id,
        row_count=len(cloud_rows),
        indicator_count=len({row.indicator_id for row in cloud_rows}),
        module_row_counts=module_row_counts,
        total_bytes_processed=total_bytes,
        expected_total_bytes_processed=expected_total_bytes_processed,
        cache_hits=cache_hits,
        gates=gates,
    )
