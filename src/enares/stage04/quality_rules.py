"""Pure, source-agnostic statistical quality rules for Stage 04."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CvUnit = Literal["proportion", "percent"]

CV_HIGH_NOTE = (
    "Estimación referencial por precisión reducida: CV superior al 15 %. "
    "Interpretar con cautela."
)
N_SMALL_NOTE = (
    "Estimación basada en menos de 30 observaciones no ponderadas. "
    "Interpretar con cautela."
)
EXACT_ZERO_CV_NOTE = (
    "Cero exacto observado: el CV es indefinido (0/0), no un estadístico faltante."
)


@dataclass(frozen=True)
class StatisticalQuality:
    cv_flag: bool | None
    n_flag: bool
    quality_status: str
    quality_notes: tuple[str, ...]


def derive_statistical_quality(
    *,
    estimate: float | None,
    cv: float | None,
    cv_unit: CvUnit,
    n_unweighted: int,
) -> StatisticalQuality:
    """Derive precision alerts without considering source or confidentiality."""
    if cv_unit not in {"proportion", "percent"}:
        raise ValueError("Unknown CV unit")
    exact_zero_cv_undefined = estimate == 0 and cv is None
    threshold = {"proportion": 0.15, "percent": 15.0}[cv_unit]
    cv_flag = None if cv is None else cv > threshold
    n_flag = n_unweighted < 30
    notes = tuple(
        note
        for active, note in (
            (cv_flag is True, CV_HIGH_NOTE),
            (n_flag, N_SMALL_NOTE),
            (exact_zero_cv_undefined, EXACT_ZERO_CV_NOTE),
        )
        if active
    )
    if cv_flag is True:
        status = "REFERENCE_HIGH_CV"
    elif exact_zero_cv_undefined:
        status = "EXACT_ZERO_CV_UNDEFINED"
    else:
        status = "PUBLISHABLE_CANDIDATE"
    return StatisticalQuality(cv_flag, n_flag, status, notes)
