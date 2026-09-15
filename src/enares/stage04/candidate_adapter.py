"""Disconnected candidate contract for the Stage 04 numeric gate.

This module deliberately has no application or repository integration.  It lets
the team test proposed mappings with synthetic rows while numeric authorization
remains open.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Literal, cast

from . import quality_rules

CV_HIGH_NOTE = quality_rules.CV_HIGH_NOTE
N_SMALL_NOTE = quality_rules.N_SMALL_NOTE
EXACT_ZERO_CV_NOTE = quality_rules.EXACT_ZERO_CV_NOTE

StatisticType = Literal["prevalence", "distribution", "special", "incomplete"]
Scale = Literal["0_1", "0_100"]
CvUnit = Literal["proportion", "percent"]
MODULE_IDS = frozenset({"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"})
VALID_SCALES = frozenset({"0_1", "0_100"})
VALID_CV_UNITS = frozenset({"proportion", "percent"})
VALID_STATISTIC_TYPES = frozenset(
    {"prevalence", "distribution", "special", "incomplete"}
)


@dataclass(frozen=True)
class CandidateScope:
    module_id: str
    indicator_id: str
    allowed_pairs: frozenset[tuple[str, str]]
    dictionary_type: StatisticType
    output_type: StatisticType
    scale: Scale = "0_100"
    cv_unit: CvUnit = "proportion"
    adapter_id: str | None = None


@dataclass(frozen=True)
class CandidateAggregate:
    module_id: str
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
    adapter_id: str | None
    cv_flag: bool | None = None
    n_flag: bool = False
    suppress_flag: None = None
    quality_status: str = "PUBLISHABLE_CANDIDATE"
    quality_notes: tuple[str, ...] = ()
    authorization_state: str = "PENDING_NUMERIC_AUTHORIZATION"


REQUIRED_COMPLETE_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
)


def _count(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def _validate_scope(scope: CandidateScope, row_type: object) -> None:
    if scope.module_id not in MODULE_IDS:
        raise ValueError("Unknown module")
    if scope.scale not in VALID_SCALES:
        raise ValueError("Unknown scale")
    if scope.cv_unit not in VALID_CV_UNITS:
        raise ValueError("Unknown CV unit")
    if scope.dictionary_type not in VALID_STATISTIC_TYPES:
        raise ValueError("Unknown dictionary type")
    if scope.output_type not in VALID_STATISTIC_TYPES:
        raise ValueError("Unknown output type")
    if row_type not in VALID_STATISTIC_TYPES:
        raise ValueError("Unknown row statistic type")


def _finite_number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be a number")
    converted = float(value)
    if not isfinite(converted):
        raise ValueError(f"{field} must be finite")
    return converted


def adapt_candidate_row(
    raw: Mapping[str, object], scope: CandidateScope
) -> CandidateAggregate:
    """Validate one synthetic proposal without authorizing or connecting it."""
    if raw.get("synthetic") is not True:
        raise ValueError("Candidate adapter accepts only explicit synthetic=true rows")
    return _adapt_row_after_source_boundary(raw, scope)


def _adapt_row_after_source_boundary(
    raw: Mapping[str, object],
    scope: CandidateScope,
    *,
    authorization_state: str = "PENDING_NUMERIC_AUTHORIZATION",
) -> CandidateAggregate:
    """Apply shared validation after a source-specific boundary has succeeded."""
    output_type = raw.get("statistic_type")
    _validate_scope(scope, output_type)
    if raw.get("module_id") != scope.module_id:
        raise ValueError("module is outside the candidate authorization scope")
    if raw.get("indicator_id") != scope.indicator_id:
        raise ValueError("indicator is outside the candidate authorization scope")
    pair = (raw.get("dimension"), raw.get("category"))
    if pair not in scope.allowed_pairs:
        raise ValueError(
            "dimension/category pair is outside the candidate authorization scope"
        )

    if output_type != scope.output_type:
        raise ValueError("statistic type does not match the candidate contract")
    if scope.dictionary_type != scope.output_type and not scope.adapter_id:
        raise ValueError("dictionary/output type mismatch requires an explicit adapter")

    # N is exclusively base_unw. target_unw is retained only as a separate numerator count.
    n_unweighted = _count(raw.get("base_unw"), "base_unw")
    target_value = raw.get("target_unw")
    target_unweighted = (
        None if target_value is None else _count(target_value, "target_unw")
    )
    if target_unweighted is not None and target_unweighted > n_unweighted:
        raise ValueError("target_unw cannot exceed base_unw")

    statistics = {field: raw.get(field) for field in REQUIRED_COMPLETE_FIELDS}
    missing = [field for field, value in statistics.items() if value is None]
    exact_zero_with_undefined_cv = (
        statistics["estimate"] == 0
        and statistics["cv"] is None
        and all(
            statistics[field] is not None
            for field in REQUIRED_COMPLETE_FIELDS
            if field != "cv"
        )
    )
    if scope.output_type == "incomplete":
        if not missing:
            raise ValueError(
                "incomplete output must preserve at least one missing statistic"
            )
    elif missing and not (missing == ["cv"] and exact_zero_with_undefined_cv):
        raise ValueError("complete output requires all statistical fields")

    numeric = {
        field: None if value is None else _finite_number(value, field)
        for field, value in statistics.items()
    }
    estimate = cast(float | None, numeric["estimate"])
    standard_error = cast(float | None, numeric["standard_error"])
    ci95_lower = cast(float | None, numeric["ci95_lower"])
    ci95_upper = cast(float | None, numeric["ci95_upper"])
    cv = cast(float | None, numeric["cv"])
    upper = {"0_1": 1, "0_100": 100}[scope.scale]
    if estimate is not None and not 0 <= estimate <= upper:
        raise ValueError("estimate is outside its declared scale")
    if standard_error is not None and standard_error < 0:
        raise ValueError("standard_error must be non-negative")
    if cv is not None and cv < 0:
        raise ValueError("cv must be non-negative")
    if ci95_lower is not None and ci95_upper is not None and ci95_lower > ci95_upper:
        raise ValueError("confidence interval bounds are reversed")
    if (
        estimate is not None
        and ci95_lower is not None
        and ci95_upper is not None
        and not ci95_lower <= estimate <= ci95_upper
    ):
        raise ValueError("confidence interval must contain estimate")

    for flag in ("cv_flag", "n_flag", "suppress_flag"):
        if raw.get(flag) is not None:
            raise ValueError(f"{flag} is derived centrally and cannot be supplied")

    quality = quality_rules.derive_statistical_quality(
        estimate=estimate,
        cv=cv,
        cv_unit=scope.cv_unit,
        n_unweighted=n_unweighted,
    )

    return CandidateAggregate(
        module_id=scope.module_id,
        indicator_id=scope.indicator_id,
        dimension=str(raw["dimension"]),
        category=str(raw["category"]),
        statistic_type=scope.output_type,
        estimate=estimate,
        standard_error=standard_error,
        ci95_lower=ci95_lower,
        ci95_upper=ci95_upper,
        cv=cv,
        n_unweighted=n_unweighted,
        target_unweighted=target_unweighted,
        scale=scope.scale,
        cv_unit=scope.cv_unit,
        adapter_id=scope.adapter_id,
        cv_flag=quality.cv_flag,
        n_flag=quality.n_flag,
        quality_status=quality.quality_status,
        quality_notes=quality.quality_notes,
        authorization_state=authorization_state,
    )


def candidate_view_model(row: CandidateAggregate) -> dict[str, object]:
    """Render approved quality alerts for synthetic candidates only."""
    visible = row.statistic_type != "incomplete"
    return {
        "module_id": row.module_id,
        "indicator_id": row.indicator_id,
        "dimension": row.dimension,
        "category": row.category,
        "state": row.authorization_state,
        "quality_status": row.quality_status,
        "quality_notes": row.quality_notes,
        "cv_flag": row.cv_flag,
        "n_flag": row.n_flag,
        "suppress_flag": row.suppress_flag,
        "confidentiality_state": "PENDING_INDEPENDENT_POLICY",
        "numeric_visible": visible,
        "estimate": row.estimate if visible else None,
        "standard_error": row.standard_error if visible else None,
        "ci95_lower": row.ci95_lower if visible else None,
        "ci95_upper": row.ci95_upper if visible else None,
        "cv": row.cv if visible else None,
        "n_unweighted": row.n_unweighted if visible else None,
    }


def summarize_synthetic_health_care_domain(
    rows: list[Mapping[str, object]],
) -> tuple[int, int]:
    """Prove the D09 denominator rule with synthetic records, never production data."""
    base_unw = 0
    target_unw = 0
    for row in rows:
        if row.get("synthetic") is not True:
            raise ValueError("D09 domain evidence accepts only synthetic=true rows")
        domain = row.get("CONS_ALGUNA")
        care = row.get("CONS_ATENCION_SALUD")
        if domain not in (0, 1, None) or isinstance(domain, bool):
            raise ValueError("CONS_ALGUNA must be 0, 1 or null")
        if care not in (0, 1, None) or isinstance(care, bool):
            raise ValueError("CONS_ATENCION_SALUD must be 0, 1 or null")
        if domain != 1 and care is not None:
            raise ValueError("CONS_ATENCION_SALUD must be null outside CONS_ALGUNA = 1")
        if domain == 1 and care is not None:
            base_unw += 1
            target_unw += int(care == 1)
    return base_unw, target_unw
