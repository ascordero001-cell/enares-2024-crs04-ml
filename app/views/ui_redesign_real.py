"""Authorized view models for the Stage 04 UI redesign."""

from __future__ import annotations

from dataclasses import dataclass

from app.views.stage04_dashboard import build_numeric_card, load_validated_estimates
from enares.stage04.repository import (
    IndicatorEstimate,
    IndicatorRepository,
    RepositoryContractError,
    is_verified_authorized_estimate,
)

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")


@dataclass(frozen=True)
class AuthorizedRedesignResult:
    """One provenance-verified aggregate prepared for the redesigned UI."""

    row: IndicatorEstimate
    state: str


STATE_LABELS = {
    "PUBLISHABLE_SHADOW": "Sin alerta",
    "REFERENCE_HIGH_CV": "Referencial por CV",
    "SMALL_N": "Alerta de N reducido",
    "REFERENCE_HIGH_CV_AND_SMALL_N": "Referencial por CV + alerta de N reducido",
    "CONTEXT_ONLY": "Contexto no numérico",
    "SUPPRESSED": "Suprimido por confidencialidad",
}


def authorized_state(row: IndicatorEstimate) -> str:
    """Derive display state from independent, already-validated row signals."""
    if row.suppress_flag:
        return "SUPPRESSED"
    if row.quality_status == "CONTEXT_ONLY":
        return "CONTEXT_ONLY"
    if row.cv_flag and row.n_flag:
        return "REFERENCE_HIGH_CV_AND_SMALL_N"
    if row.cv_flag:
        return "REFERENCE_HIGH_CV"
    if row.n_flag:
        return "SMALL_N"
    return "PUBLISHABLE_SHADOW"


def load_authorized_results(
    repository: IndicatorRepository,
) -> list[AuthorizedRedesignResult]:
    """Load every approved module through the existing repository and validation gates."""
    results: list[AuthorizedRedesignResult] = []
    for module_id in MODULE_IDS:
        for row in load_validated_estimates(repository, module_id):
            if not is_verified_authorized_estimate(row):
                raise RepositoryContractError(
                    "UI redesign received an aggregate without verified provenance"
                )
            results.append(AuthorizedRedesignResult(row=row, state=authorized_state(row)))
    return results


def filter_authorized_results(
    results: list[AuthorizedRedesignResult],
    *,
    module_id: str,
    dimension: str,
    indicator_id: str,
    states: tuple[str, ...],
    category: str | None = None,
) -> list[AuthorizedRedesignResult]:
    """Select only combinations that already exist in the authorized catalog."""
    return [
        result
        for result in results
        if result.row.module_id == module_id
        and result.row.disaggregation == dimension
        and result.row.indicator_id == indicator_id
        and result.state in states
        and (category is None or result.row.category == category)
    ]


def table_record(result: AuthorizedRedesignResult) -> dict[str, object]:
    """Return a safe table row; protected or non-numeric states never expose statistics."""
    row = result.row
    show_numeric = result.state not in {"SUPPRESSED", "CONTEXT_ONLY"}
    return {
        "Indicador": row.indicator_id,
        "Dimensión": row.disaggregation,
        "Categoría": row.category,
        "Estimación (%)": row.estimate if show_numeric else None,
        "IC95 % inferior": row.ci95_lower if show_numeric else None,
        "IC95 % superior": row.ci95_upper if show_numeric else None,
        "N no ponderado": row.n_unweighted if show_numeric else None,
        "Estado": STATE_LABELS[result.state],
    }


def forest_record(result: AuthorizedRedesignResult) -> dict[str, object] | None:
    """Return one validated numeric point without recalculating its interval."""
    row = result.row
    if result.state in {"SUPPRESSED", "CONTEXT_ONLY"}:
        return None
    if row.estimate is None or row.ci95_lower is None or row.ci95_upper is None:
        return None
    return {
        "label": row.category,
        "estimate": row.estimate,
        "lower": row.ci95_lower,
        "upper": row.ci95_upper,
        "state": STATE_LABELS[result.state],
    }


def numeric_card(result: AuthorizedRedesignResult) -> dict[str, object] | None:
    """Reuse the approved card adapter for a visible numeric aggregate."""
    if result.state in {"SUPPRESSED", "CONTEXT_ONLY"}:
        return None
    return build_numeric_card(result.row)
