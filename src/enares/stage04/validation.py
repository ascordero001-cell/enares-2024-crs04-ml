"""Local validation rules for aggregate Stage 04 contracts."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .repository import IndicatorEstimate


VALID_QUALITY_STATES = {
    "PUBLISHABLE_CANDIDATE",
    "REFERENCE_HIGH_CV",
    "SUPPRESSED_EXERCISE",
}
VALID_VALIDATION_STATES = {"PENDING", "PASSED", "FAILED", "APPROVED"}
PROTECTED_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "n_unweighted",
    "weighted_population",
)


def validate_estimates(rows: Iterable[IndicatorEstimate]) -> None:
    materialized = list(rows)
    if not materialized:
        raise ValueError("The aggregate catalog must not be empty")

    keys: set[tuple[str, ...]] = set()
    quality_states: set[str] = set()
    for row in materialized:
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
        quality_states.add(row.quality_status)

        if row.quality_status == "SUPPRESSED_EXERCISE":
            if not row.suppress_flag:
                raise ValueError("Suppressed quality state requires suppress_flag")
            if any(getattr(row, field) is not None for field in PROTECTED_FIELDS):
                raise ValueError("Suppressed rows must not expose protected statistics")
            continue

        if any(getattr(row, field) is None for field in PROTECTED_FIELDS):
            raise ValueError("Non-suppressed rows require complete statistics")
        upper = 1 if row.scale == "0_1" else 100 if row.scale == "0_100" else None
        if upper is None or not 0 <= row.estimate <= upper:
            raise ValueError("estimate is outside its declared scale")
        if (
            row.standard_error < 0
            or row.cv < 0
            or row.n_unweighted < 0
            or row.weighted_population < 0
        ):
            raise ValueError("SE, CV and N must be non-negative")
        if not row.ci95_lower <= row.estimate <= row.ci95_upper:
            raise ValueError("The confidence interval must contain the estimate")

    if quality_states != VALID_QUALITY_STATES:
        raise ValueError("The demo catalog must cover all three visual quality states")
