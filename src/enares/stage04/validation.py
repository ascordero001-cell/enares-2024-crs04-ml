"""Local validation rules for aggregate Stage 04 contracts."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .modules import get_module
from .repository import IndicatorEstimate


VALID_QUALITY_STATES = {
    "PUBLISHABLE_CANDIDATE",
    "REFERENCE_HIGH_CV",
    "SUPPRESSED_EXERCISE",
}
VALID_VALIDATION_STATES = {"PENDING", "PASSED", "FAILED", "APPROVED"}
REQUIRED_STATISTICAL_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "n_unweighted",
)
SUPPRESSED_PROTECTED_FIELDS = (
    *REQUIRED_STATISTICAL_FIELDS,
    "weighted_population",
)


def validate_estimates(rows: Iterable[IndicatorEstimate]) -> None:
    materialized = list(rows)
    if not materialized:
        raise ValueError("The aggregate catalog must not be empty")

    keys: set[tuple[str, ...]] = set()
    for row in materialized:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}", row.release_id):
            raise ValueError("release_id is invalid")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}", row.run_id):
            raise ValueError("run_id is invalid")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", row.git_commit_sha):
            raise ValueError("git_commit_sha must be a 40-character hexadecimal SHA")
        if not row.source_version:
            raise ValueError("source_version is required")
        module = get_module(row.module_id)
        if not row.synthetic and row.indicator_id not in module.indicator_ids:
            raise ValueError("indicator_id is not registered for its module")
        if not row.synthetic and row.disaggregation not in module.available_dimensions:
            raise ValueError("disaggregation is not available for its module")
        if not row.synthetic and row.disaggregation not in module.authorized_dimensions:
            raise ValueError("disaggregation is not authorized for its module")
        if not row.category:
            raise ValueError("category is required")
        key = (
            row.release_id,
            row.run_id,
            row.indicator_id,
            row.disaggregation,
            row.category,
        )
        if key in keys:
            raise ValueError(f"Duplicate aggregate key: {key}")
        keys.add(key)

        if row.validation_status not in VALID_VALIDATION_STATES:
            raise ValueError("Unknown validation status")
        if row.validation_status == "FAILED":
            raise ValueError("FAILED rows cannot enter a candidate catalog")
        if row.quality_status not in VALID_QUALITY_STATES:
            raise ValueError("Unknown quality status")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", row.source_hash):
            raise ValueError("source_hash must be a SHA-256")
        if row.quality_status == "SUPPRESSED_EXERCISE" and not row.suppress_flag:
            raise ValueError("Suppressed quality state requires suppress_flag")
        if row.suppress_flag:
            if any(getattr(row, field) is not None for field in SUPPRESSED_PROTECTED_FIELDS):
                raise ValueError("Suppressed rows must not expose protected statistics")
            if row.quality_status != "SUPPRESSED_EXERCISE":
                raise ValueError("suppress_flag requires the suppressed quality state")
            continue

        if any(getattr(row, field) is None for field in REQUIRED_STATISTICAL_FIELDS):
            raise ValueError("Non-suppressed rows require complete statistics")
        upper = 1 if row.scale == "0_1" else 100 if row.scale == "0_100" else None
        if upper is None or not 0 <= row.estimate <= upper:
            raise ValueError("estimate is outside its declared scale")
        if (
            row.standard_error < 0
            or row.cv < 0
            or row.n_unweighted < 0
        ):
            raise ValueError("SE, CV and N must be non-negative")
        if row.weighted_population is not None and row.weighted_population < 0:
            raise ValueError("weighted_population must be non-negative when present")
        if not row.ci95_lower <= row.estimate <= row.ci95_upper:
            raise ValueError("The confidence interval must contain the estimate")

    if len({row.release_id for row in materialized}) != 1:
        raise ValueError("A catalog cannot mix releases")
    if len({row.source_hash for row in materialized}) != 1:
        raise ValueError("A catalog cannot mix source hashes")
