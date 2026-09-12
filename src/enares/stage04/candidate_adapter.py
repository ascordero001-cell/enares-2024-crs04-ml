"""Disconnected candidate contract for the Stage 04 numeric gate.

This module deliberately has no application or repository integration. It lets
the team test proposed mappings with synthetic rows while numeric authorization
remains open.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

StatisticType = Literal["prevalence", "distribution", "special", "incomplete"]
Scale = Literal["0_1", "0_100"]
CvUnit = Literal["proportion", "percent"]


@dataclass(frozen=True)
class CandidateScope:
    indicator_id: str
    dimensions: frozenset[str]
    categories: frozenset[str]
    dictionary_type: StatisticType
    output_type: StatisticType
    scale: Scale = "0_100"
    cv_unit: CvUnit = "proportion"
    adapter_id: str | None = None


@dataclass(frozen=True)
class CandidateAggregate:
    indicator_id: str
    dimension: str
    category: str
    statistic_type: StatisticType
    estimate: float | None
    standard_error: float | None
    ci95_lower: float | None
    ci95_upper: float | None
    cv: float | None
    n_unweighted: int
    target_unweighted: int | None
    scale: Scale
    cv_unit: CvUnit
    cv_flag: None = None
    n_flag: None = None
    suppress_flag: None = None
    quality_status: str = "PENDING_METHODOLOGICAL_DECISION"


REQUIRED_COMPLETE_FIELDS = ("estimate", "standard_error", "ci95_lower", "ci95_upper", "cv")


def _count(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def adapt_candidate_row(raw: Mapping[str, object], scope: CandidateScope) -> CandidateAggregate:
    """Validate one synthetic proposal without authorizing or connecting it."""
    if raw.get("indicator_id") != scope.indicator_id:
        raise ValueError("indicator is outside the candidate authorization scope")
    if raw.get("dimension") not in scope.dimensions:
        raise ValueError("dimension is outside the candidate authorization scope")
    if raw.get("category") not in scope.categories:
        raise ValueError("category is outside the candidate authorization scope")

    output_type = raw.get("statistic_type")
    if output_type != scope.output_type:
        raise ValueError("statistic type does not match the candidate contract")
    if scope.dictionary_type != scope.output_type and not scope.adapter_id:
        raise ValueError("dictionary/output type mismatch requires an explicit adapter")

    # N is exclusively base_unw. target_unw is retained only as a separate numerator count.
    n_unweighted = _count(raw.get("base_unw"), "base_unw")
    target_value = raw.get("target_unw")
    target_unweighted = None if target_value is None else _count(target_value, "target_unw")
    if target_unweighted is not None and target_unweighted > n_unweighted:
        raise ValueError("target_unw cannot exceed base_unw")

    statistics = {field: raw.get(field) for field in REQUIRED_COMPLETE_FIELDS}
    missing = [field for field, value in statistics.items() if value is None]
    if scope.output_type == "incomplete":
        if not missing:
            raise ValueError("incomplete output must preserve at least one missing statistic")
    elif missing:
        raise ValueError("complete output requires all statistical fields")

    estimate = statistics["estimate"]
    standard_error = statistics["standard_error"]
    ci95_lower = statistics["ci95_lower"]
    ci95_upper = statistics["ci95_upper"]
    cv = statistics["cv"]
    upper = 1 if scope.scale == "0_1" else 100
    if estimate is not None and not 0 <= float(estimate) <= upper:
        raise ValueError("estimate is outside its declared scale")
    if standard_error is not None and float(standard_error) < 0:
        raise ValueError("standard_error must be non-negative")
    if cv is not None and float(cv) < 0:
        raise ValueError("cv must be non-negative")
    if None not in (estimate, ci95_lower, ci95_upper) and not (
        float(ci95_lower) <= float(estimate) <= float(ci95_upper)
    ):
        raise ValueError("confidence interval must contain estimate")

    for flag in ("cv_flag", "n_flag", "suppress_flag"):
        if raw.get(flag) is not None:
            raise ValueError(f"{flag} must remain pending until supervisory approval")

    return CandidateAggregate(
        indicator_id=scope.indicator_id,
        dimension=str(raw["dimension"]),
        category=str(raw["category"]),
        statistic_type=scope.output_type,
        estimate=None if estimate is None else float(estimate),
        standard_error=None if standard_error is None else float(standard_error),
        ci95_lower=None if ci95_lower is None else float(ci95_lower),
        ci95_upper=None if ci95_upper is None else float(ci95_upper),
        cv=None if cv is None else float(cv),
        n_unweighted=n_unweighted,
        target_unweighted=target_unweighted,
        scale=scope.scale,
        cv_unit=scope.cv_unit,
    )


def candidate_view_model(row: CandidateAggregate) -> dict[str, object]:
    """Return a non-numeric state for incomplete or still-pending candidates."""
    return {
        "indicator_id": row.indicator_id,
        "dimension": row.dimension,
        "category": row.category,
        "state": row.quality_status,
        "numeric_visible": False,
        "estimate": None,
        "standard_error": None,
        "ci95_lower": None,
        "ci95_upper": None,
        "cv": None,
        "n_unweighted": None,
    }
