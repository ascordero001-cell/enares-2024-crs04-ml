"""Redacted, metadata-only preflight for the approved Stage 04 resource."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any

from google.api_core.exceptions import GoogleAPICallError
from google.auth.exceptions import DefaultCredentialsError

_SAFE_FAILURE_CLASSES = {
    "BadRequest",
    "DeadlineExceeded",
    "DefaultCredentialsError",
    "Forbidden",
    "NotFound",
    "ServiceUnavailable",
    "TooManyRequests",
    "Unauthorized",
}


@dataclass(frozen=True)
class MetadataCheck:
    """One redacted existence/access result."""

    accessible: bool
    failure_class: str | None = None


@dataclass(frozen=True)
class MetadataPreflightEvidence:
    """Boolean/redacted evidence with no principal, path, row or provider detail."""

    status: str
    mode: str
    project: MetadataCheck
    dataset: MetadataCheck
    table: MetadataCheck
    rows_read: int = 0
    ddl_dml_executed: bool = False

    def as_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


def _safe_failure_class(exc: BaseException) -> str:
    name = type(exc).__name__
    return name if name in _SAFE_FAILURE_CLASSES else "GoogleCloudError"


def _check(call: Callable[[], Any]) -> MetadataCheck:
    try:
        call()
    except (GoogleAPICallError, DefaultCredentialsError, OSError) as exc:
        return MetadataCheck(False, _safe_failure_class(exc))
    return MetadataCheck(True)


def preflight_bigquery_metadata(
    *,
    client: Any,
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> MetadataPreflightEvidence:
    """Check project, dataset and table metadata separately without querying rows."""

    project = _check(
        lambda: next(iter(client.list_datasets(project=project_id, max_results=1)), None)
    )
    dataset = (
        _check(lambda: client.get_dataset(f"{project_id}.{dataset_id}"))
        if project.accessible
        else MetadataCheck(False, "NOT_CHECKED")
    )
    table = (
        _check(lambda: client.get_table(f"{project_id}.{dataset_id}.{table_id}"))
        if dataset.accessible
        else MetadataCheck(False, "NOT_CHECKED")
    )
    passed = project.accessible and dataset.accessible and table.accessible
    return MetadataPreflightEvidence(
        status="PASS" if passed else "HOLD",
        mode="METADATA_ONLY",
        project=project,
        dataset=dataset,
        table=table,
    )
