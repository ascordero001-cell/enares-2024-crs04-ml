"""Safe local repository contract for aggregate Stage 04 results."""

from __future__ import annotations

import csv
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
AUTHORIZED_AGGREGATE_HASHES = {
    "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"
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
            rows = [self._to_estimate(row) for row in reader if row["module_id"] == module_id]
        return rows

    @staticmethod
    def _optional_float(value: str) -> float | None:
        return None if value == "" else float(value)

    @staticmethod
    def _bool(value: str) -> bool:
        if value.lower() not in {"true", "false"}:
            raise ValueError(f"Invalid boolean: {value}")
        return value.lower() == "true"

    @classmethod
    def _to_estimate(cls, row: dict[str, str]) -> IndicatorEstimate:
        synthetic = cls._bool(row.get("synthetic", ""))
        if not synthetic and row["source_hash"] not in AUTHORIZED_AGGREGATE_HASHES:
            raise ValueError("Non-synthetic rows require an explicitly authorized aggregate hash")
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
            estimate=cls._optional_float(row["estimate"]),
            standard_error=cls._optional_float(row["standard_error"]),
            ci95_lower=cls._optional_float(row["ci95_lower"]),
            ci95_upper=cls._optional_float(row["ci95_upper"]),
            cv=cls._optional_float(row["cv"]),
            n_unweighted=None if row["n_unweighted"] == "" else int(row["n_unweighted"]),
            weighted_population=cls._optional_float(row["weighted_population"]),
            cv_flag=cls._bool(row["cv_flag"]),
            n_flag=cls._bool(row["n_flag"]),
            suppress_flag=cls._bool(row["suppress_flag"]),
            quality_note=row["quality_note"],
            validation_status=row["validation_status"],
            created_at=row["created_at"],
            universe=row["universe"],
            denominator=row["denominator"],
            quality_status=row["quality_status"],
            synthetic=synthetic,
        )


class BigQueryRepository(IndicatorRepository):
    """Non-connected design placeholder; cloud access is not authorized."""

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        raise RuntimeError("BLOCKED_BY_CLOUD_GATE: BigQuery access is not authorized")
