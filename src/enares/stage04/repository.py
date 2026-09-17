"""Safe local repository contract for aggregate Stage 04 results."""

from __future__ import annotations

import csv
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

REPOSITORY_UNAVAILABLE_MESSAGE: Final = "Repository data is unavailable"
REPOSITORY_CONTRACT_MESSAGE: Final = "Repository data violates the aggregate contract"
RELEASE_NOT_FOUND_MESSAGE: Final = "Requested release run is unavailable"

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


class RepositoryError(RuntimeError):
    """Base class for safe repository failures exposed to consumers."""


class RepositoryUnavailableError(RepositoryError):
    """The configured repository cannot currently be reached or read."""


class RepositoryContractError(RepositoryError, ValueError):
    """Repository content violates the approved aggregate contract."""


class ReleaseNotFoundError(RepositoryError, LookupError):
    """A requested release/run pair does not exist in the repository or cache."""


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
    cv_flag: bool | None
    n_flag: bool
    suppress_flag: bool
    quality_note: str
    validation_status: str
    created_at: str
    universe: str
    denominator: str
    quality_status: str
    synthetic: bool


@dataclass(frozen=True)
class _ProvenanceVerifiedIndicatorEstimate(IndicatorEstimate):
    """Internal type emitted only after the institutional provenance gate."""


class IndicatorRepository(ABC):
    """Read-only interface consumed by the future local view."""

    @abstractmethod
    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        """Return safe aggregate estimates for one module."""


class CompositeRepository(IndicatorRepository):
    """Expose several independently verified aggregate catalogs as one source."""

    def __init__(self, *repositories: IndicatorRepository) -> None:
        if not repositories:
            raise ValueError("CompositeRepository requires at least one source")
        self.repositories: tuple[IndicatorRepository, ...] = repositories

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        rows: list[IndicatorEstimate] = []
        for repository in self.repositories:
            rows.extend(repository.list_estimates(module_id))
        return rows


def _optional_float(value: str) -> float | None:
    return None if value == "" else float(value)


def _bool(value: str) -> bool:
    if value.lower() not in {"true", "false"}:
        raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
    return value.lower() == "true"


def _optional_bool(value: str) -> bool | None:
    return None if value == "" else _bool(value)


class _VerifiedSourceClassification(Enum):
    SYNTHETIC_TEST = True
    AUTHORIZED_INSTITUTIONAL_AGGREGATE = False


def _to_estimate(
    row: dict[str, str],
    *,
    source_classification: _VerifiedSourceClassification,
) -> IndicatorEstimate:
    estimate_type = (
        _ProvenanceVerifiedIndicatorEstimate
        if source_classification
        is _VerifiedSourceClassification.AUTHORIZED_INSTITUTIONAL_AGGREGATE
        else IndicatorEstimate
    )
    return estimate_type(
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
        cv_flag=_optional_bool(row["cv_flag"]),
        n_flag=_bool(row["n_flag"]),
        suppress_flag=_bool(row["suppress_flag"]),
        quality_note=row["quality_note"],
        validation_status=row["validation_status"],
        created_at=row["created_at"],
        universe=row["universe"],
        denominator=row["denominator"],
        quality_status=row["quality_status"],
        # This flag is provenance output. It is never copied from a CSV field.
        synthetic=source_classification.value,
    )


def is_verified_authorized_estimate(row: IndicatorEstimate) -> bool:
    """Return true only for rows classified by the authorized repository gate."""
    return row.synthetic is False and isinstance(
        row, _ProvenanceVerifiedIndicatorEstimate
    )


class DemoRepository(IndicatorRepository):
    """Read a checked synthetic fixture without accessing private sources."""

    def __init__(self, fixture_path: Path) -> None:
        self.fixture_path: Path = Path(fixture_path)

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        try:
            with self.fixture_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                columns = set(reader.fieldnames or ())
                if columns & SENSITIVE_COLUMNS:
                    raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
                raw_rows = list(reader)
            if any(not _bool(row.get("synthetic", "")) for row in raw_rows):
                raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
            return [
                _to_estimate(
                    row,
                    source_classification=_VerifiedSourceClassification.SYNTHETIC_TEST,
                )
                for row in raw_rows
                if row["module_id"] == module_id
            ]
        except OSError:
            raise RepositoryUnavailableError(REPOSITORY_UNAVAILABLE_MESSAGE) from None
        except RepositoryError:
            raise
        except (KeyError, TypeError, ValueError):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE) from None


class AuthorizedAggregateRepository(IndicatorRepository):
    """Read a manifest-bound authorized V0 extract for local shadow use."""

    def __init__(
        self,
        fixture_path: Path,
        manifest_path: Path,
        approval_registry_path: Path,
    ) -> None:
        self.fixture_path: Path = Path(fixture_path)
        self.manifest_path: Path = Path(manifest_path)
        self.approval_registry_path: Path = Path(approval_registry_path)

    def _verify_provenance(
        self,
    ) -> tuple[dict[str, object], _VerifiedSourceClassification]:
        try:
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            digest = hashlib.sha256(self.fixture_path.read_bytes()).hexdigest()
            approval_registry = self.approval_registry_path.read_text(encoding="utf-8")
        except OSError:
            raise RepositoryUnavailableError(REPOSITORY_UNAVAILABLE_MESSAGE) from None
        except (json.JSONDecodeError, TypeError):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE) from None
        if (
            manifest.get("file_name") != self.fixture_path.name
            or manifest.get("sha256") != digest
        ):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        if manifest.get("synthetic") is not False:
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        if manifest.get("data_classification") != "AUTHORIZED_AGGREGATE_ONLY":
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        if manifest.get("source_kind") != "AUTHORIZED_V0_EXTRACT":
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        source_hash = manifest.get("source_hash")
        if not isinstance(source_hash, str) or manifest.get("parent_sha256") != source_hash:
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        if (
            "APPROVED_FOR_STAGE04_BASELINE" not in approval_registry
            or source_hash not in approval_registry
        ):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        return (
            manifest,
            _VerifiedSourceClassification.AUTHORIZED_INSTITUTIONAL_AGGREGATE,
        )

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        manifest, source_classification = self._verify_provenance()
        source_hash = manifest["source_hash"]

        try:
            with self.fixture_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                columns = set(reader.fieldnames or ())
                if columns & SENSITIVE_COLUMNS:
                    raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
                raw_rows = list(reader)
        except OSError:
            raise RepositoryUnavailableError(REPOSITORY_UNAVAILABLE_MESSAGE) from None
        if manifest.get("row_count") != len(raw_rows):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        if any(row.get("source_hash") != source_hash for row in raw_rows):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE)
        try:
            return [
                _to_estimate(row, source_classification=source_classification)
                for row in raw_rows
                if row["module_id"] == module_id
            ]
        except RepositoryError:
            raise
        except (KeyError, TypeError, ValueError):
            raise RepositoryContractError(REPOSITORY_CONTRACT_MESSAGE) from None


class BigQueryRepository(IndicatorRepository):
    """Non-connected design placeholder; cloud access is not authorized."""

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        raise RepositoryUnavailableError(REPOSITORY_UNAVAILABLE_MESSAGE)
