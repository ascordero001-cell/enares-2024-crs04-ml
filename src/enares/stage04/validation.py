"""Local validation rules for aggregate Stage 04 contracts."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .authorized_scopes import (
    VS_MATRIX_CROSS_BY_DIMENSION,
    VS_MATRIX_PAIRS,
    VS_MATRIX_V0_CROSSES,
)
from .modules import get_module
from .privacy import assert_v0_granularity_boundary
from .repository import IndicatorEstimate
from .v0_catalog_registry import V0_MODULE_BY_INDICATOR

VALID_QUALITY_STATES = {
    "CONTEXT_ONLY",
    "EXACT_ZERO_CV_UNDEFINED",
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
        if not row.synthetic and V0_MODULE_BY_INDICATOR.get(row.indicator_id) != row.module_id:
            raise ValueError("indicator_id is not registered for its module")
        matrix_indicator = row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
        if (
            matrix_indicator
            and (row.disaggregation, row.category) not in VS_MATRIX_PAIRS
        ):
            raise ValueError("D06/D07 row is outside the approved V0 matrix")
        requested_crosses = (
            {VS_MATRIX_CROSS_BY_DIMENSION[row.disaggregation]}
            if matrix_indicator and row.disaggregation in VS_MATRIX_CROSS_BY_DIMENSION
            else set()
        )
        assert_v0_granularity_boundary(
            requested_dimensions={row.disaggregation},
            v0_dimensions=set(module.available_dimensions),
            requested_crosses=requested_crosses,
            v0_crosses=set(VS_MATRIX_V0_CROSSES),
            synthetic=row.synthetic,
        )
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
            if any(
                getattr(row, field) is not None for field in SUPPRESSED_PROTECTED_FIELDS
            ):
                raise ValueError("Suppressed rows must not expose protected statistics")
            if row.quality_status != "SUPPRESSED_EXERCISE":
                raise ValueError("suppress_flag requires the suppressed quality state")
            continue

        if row.quality_status == "CONTEXT_ONLY":
            if row.estimate is None or row.n_unweighted is None:
                raise ValueError("Context rows require the V0 estimate and base")
            if any(
                value is not None
                for value in (
                    row.standard_error,
                    row.ci95_lower,
                    row.ci95_upper,
                    row.cv,
                )
            ):
                raise ValueError("Context rows must preserve absent inferential statistics")
            continue

        exact_zero_cv_undefined = (
            row.quality_status == "EXACT_ZERO_CV_UNDEFINED"
            and row.estimate == 0
            and row.standard_error == 0
            and row.ci95_lower == 0
            and row.ci95_upper == 0
            and row.cv is None
            and row.n_unweighted is not None
        )
        missing = [
            field
            for field in REQUIRED_STATISTICAL_FIELDS
            if getattr(row, field) is None
        ]
        if missing and not (missing == ["cv"] and exact_zero_cv_undefined):
            raise ValueError("Non-suppressed rows require complete statistics")
        estimate = row.estimate
        standard_error = row.standard_error
        ci95_lower = row.ci95_lower
        ci95_upper = row.ci95_upper
        n_unweighted = row.n_unweighted
        if (
            estimate is None
            or standard_error is None
            or ci95_lower is None
            or ci95_upper is None
            or n_unweighted is None
        ):
            raise ValueError("Non-suppressed rows require complete statistics")
        upper = 1 if row.scale == "0_1" else 100 if row.scale == "0_100" else None
        if upper is None or not 0 <= estimate <= upper:
            raise ValueError("estimate is outside its declared scale")
        if (
            standard_error < 0
            or (row.cv is not None and row.cv < 0)
            or n_unweighted < 0
        ):
            raise ValueError("SE, CV and N must be non-negative")
        if row.weighted_population is not None and row.weighted_population < 0:
            raise ValueError("weighted_population must be non-negative when present")
        if not ci95_lower <= estimate <= ci95_upper:
            raise ValueError("The confidence interval must contain the estimate")

    if len({row.release_id for row in materialized}) != 1:
        raise ValueError("A catalog cannot mix releases")
    if len({row.source_hash for row in materialized}) != 1:
        raise ValueError("A catalog cannot mix source hashes")
