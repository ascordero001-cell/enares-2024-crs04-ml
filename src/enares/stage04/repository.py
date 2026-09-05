"""Safe local repository contract for aggregate Stage 04 results."""

from __future__ import annotations

import csv
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


SENSITIVE_COLUMNS = {
    "respondent_id",
    "person_id",
    "child_id",
    "nna_id",
    "name",
    "birth_date",
    "address",
    "phone",
    "email",
    "latitude",
    "longitude",
    "raw_record",
}
@dataclass(frozen=True)
class IndicatorEstimate:
    release_id: str
    run_id: str
    source_version: str
    source_hash: str
    git_commit_sha: str
    container_image_digest: str
    dataform_release: str
    engine_version: str
    scale: str
    indicator_id: str
    indicator_name: str
    module_id: str
    disaggregation: str
    category: str
    estimate: float | None
    standard_error: float | None
    ci95_lower: float | None
    ci95_upper: float | None
    cv: float | None
    n_unweighted: int | None
    weighted_population: float | None
    cv_flag: bool
    n_flag: bool
    suppress_flag: bool
    quality_note: str
    validation_status: str
    created_at: str
    universe: str
    denominator: str
    quality_status: str
    synthetic: bool


class IndicatorRepository(ABC):
    """Read-only interface consumed by the future local view."""

    @abstractmethod
    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        """Return safe aggregate estimates for one module."""


def _optional_float(value: str) -> float | None:
    return None if value == "" else float(value)


def _bool(value: str) -> bool:
    if value.lower() not in {"true", "false"}:
        raise ValueError(f"Invalid boolean: {value}")
    return value.lower() == "true"


def _to_estimate(row: dict[str, str]) -> IndicatorEstimate:
    return IndicatorEstimate(
        release_id=row["release_id"],
        run_id=row["run_id"],
        source_version=row["source_version"],
        source_hash=row["source_hash"],
        git_commit_sha=row["git_commit_sha"],
        container_image_digest=row["container_image_digest"],
        dataform_release=row["dataform_release"],
        engine_version=row["engine_version"],
        scale=row["scale"],
        indicator_id=row["indicator_id"],
        indicator_name=row["indicator_name"],
        module_id=row["module_id"],
        disaggregation=row["disaggregation"],
        category=row["category"],
        estimate=_optional_float(row["estimate"]),
        standard_error=_optional_float(row["standard_error"]),
        ci95_lower=_optional_float(row["ci95_lower"]),
        ci95_upper=_optional_float(row["ci95_upper"]),
        cv=_optional_float(row["cv"]),
        n_unweighted=None if row["n_unweighted"] == "" else int(row["n_unweighted"]),
        weighted_population=_optional_float(row["weighted_population"]),
        cv_flag=_bool(row["cv_flag"]),
        n_flag=_bool(row["n_flag"]),
        suppress_flag=_bool(row["suppress_flag"]),
        quality_note=row["quality_note"],
        validation_status=row["validation_status"],
        created_at=row["created_at"],
        universe=row["universe"],
        denominator=row["denominator"],
        quality_status=row["quality_status"],
        synthetic=_bool(row.get("synthetic", "")),
    )


class DemoRepository(IndicatorRepository):
    """Read a checked synthetic fixture without accessing private sources."""

    def __init__(self, fixture_path: Path) -> None:
        self.fixture_path = Path(fixture_path)

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        with self.fixture_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = set(reader.fieldnames or ())
            exposed = columns & SENSITIVE_COLUMNS
            if exposed:
                raise ValueError(f"Sensitive columns are forbidden: {sorted(exposed)}")
            raw_rows = list(reader)
            if any(not _bool(row.get("synthetic", "")) for row in raw_rows):
                raise ValueError("DemoRepository accepts only synthetic=true rows")
            rows = [_to_estimate(row) for row in raw_rows if row["module_id"] == module_id]
        return rows

class AuthorizedAggregateRepository(IndicatorRepository):
    """Read one manifest-bound, authorized aggregate input for local golden tests."""

    def __init__(
        self,
        fixture_path: Path,
        manifest_path: Path,
        approval_registry_path: Path,
    ) -> None:
        self.fixture_path = Path(fixture_path)
        self.manifest_path = Path(manifest_path)
        self.approval_registry_path = Path(approval_registry_path)

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(self.fixture_path.read_bytes()).hexdigest()
        if manifest.get("file_name") != self.fixture_path.name or manifest.get("sha256") != digest:
            raise ValueError("Authorized aggregate manifest does not match its CSV")
        if manifest.get("synthetic") is not False:
            raise ValueError("Authorized aggregate manifest must declare synthetic=false")
        if manifest.get("data_classification") != "AUTHORIZED_AGGREGATE_ONLY":
            raise ValueError("Authorized aggregate classification is required")
        source_hash = manifest.get("source_hash")
        approval_registry = self.approval_registry_path.read_text(encoding="utf-8")
        if (
            "APPROVED_FOR_STAGE04_BASELINE" not in approval_registry
            or source_hash not in approval_registry
        ):
            raise ValueError("Manifest source_hash is not in the approved V0 registry")

        with self.fixture_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = set(reader.fieldnames or ())
            exposed = columns & SENSITIVE_COLUMNS
            if exposed:
                raise ValueError(f"Sensitive columns are forbidden: {sorted(exposed)}")
            raw_rows = list(reader)
        if manifest.get("row_count") != len(raw_rows):
            raise ValueError("Authorized aggregate row_count does not match its CSV")
        if any(_bool(row.get("synthetic", "")) for row in raw_rows):
            raise ValueError("Authorized aggregate rows must declare synthetic=false")
        if any(row.get("source_hash") != source_hash for row in raw_rows):
            raise ValueError("Authorized aggregate row source_hash does not match the manifest")
        return [_to_estimate(row) for row in raw_rows if row["module_id"] == module_id]


class BigQueryRepository(IndicatorRepository):
    """Non-connected design placeholder; cloud access is not authorized."""

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        raise RuntimeError("BLOCKED_BY_CLOUD_GATE: BigQuery access is not authorized")
