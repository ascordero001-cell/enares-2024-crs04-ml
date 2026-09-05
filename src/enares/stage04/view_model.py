"""Transform aggregate contract rows into safe local view models."""

from __future__ import annotations

from .repository import IndicatorEstimate


def to_indicator_contract(row: IndicatorEstimate) -> dict:
    """Project a repository row into the golden aggregate contract."""
    return {
        "indicator_id": row.indicator_id,
        "indicator_name": row.indicator_name,
        "module_id": row.module_id,
        "disaggregation": row.disaggregation,
        "category": row.category,
        "estimate": row.estimate,
        "standard_error": row.standard_error,
        "ci95_lower": row.ci95_lower,
        "ci95_upper": row.ci95_upper,
        "cv": row.cv,
        "n_unweighted": row.n_unweighted,
        "scale": row.scale,
        "universe": row.universe,
        "denominator": row.denominator,
        "state": "SHADOW",
        "quality_status": row.quality_status,
        "validation_status": row.validation_status,
        "engine_version": row.engine_version,
        "release_id": row.release_id,
        "source_hash": row.source_hash,
    }


def to_card_view_model(row: IndicatorEstimate) -> dict:
    """Build the view model consumed by the local 3.2 wireframe."""
    if row.suppress_flag:
        raise ValueError("A suppressed row cannot build a numeric card")
    return {
        "category": row.category,
        "cv_text": f"CV {row.cv:.5f}",
        "denominator_text": f"Denominador: {row.denominator}",
        "disaggregation": row.disaggregation,
        "estimate_text": f"{row.estimate:.2f} %",
        "indicator_id": row.indicator_id,
        "indicator_name": row.indicator_name,
        "interval_text": f"IC95 %: {row.ci95_lower:.2f} %–{row.ci95_upper:.2f} %",
        "module_label": "3.2 Violencia en el hogar",
        "n_text": f"N no ponderado: {row.n_unweighted:,}",
        "quality_status": row.quality_status,
        "release_id": row.release_id,
        "source_version": row.source_version,
        "state": "SHADOW",
        "universe_text": row.universe,
    }
