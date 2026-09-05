"""Pure presentation helpers for the safe local 3.2 application shell."""

from __future__ import annotations

from dataclasses import asdict

from app.config import QUALITY_LABELS
from enares.stage04.privacy import PROTECTED_FIELDS, apply_published_suppression
from enares.stage04.repository import IndicatorEstimate, IndicatorRepository
from enares.stage04.view_model import to_card_view_model


EXPORT_ENABLED = False


def filter_estimates(
    repository: IndicatorRepository,
    module_id: str,
    disaggregation: str,
    category: str,
) -> list[IndicatorEstimate]:
    """Return only combinations present in the repository; never synthesize missing results."""
    return [
        row
        for row in repository.list_estimates(module_id)
        if row.disaggregation == disaggregation and row.category == category
    ]


def build_numeric_card(row: IndicatorEstimate) -> dict:
    """Extend the approved card view model with details required by the local UI."""
    card = to_card_view_model(row)
    card.update(
        {
            "standard_error_text": f"EE {row.standard_error:.4f}",
            "quality_label": QUALITY_LABELS[row.quality_status],
            "denominator": row.denominator,
            "created_at": row.created_at,
            "protected_values_visible": True,
        }
    )
    return card


def build_suppressed_card(row: IndicatorEstimate) -> dict:
    """Materialize suppression before constructing a non-numeric interface state."""
    if not row.suppress_flag:
        raise ValueError("Only a suppressed row can build a suppressed card")
    safe = apply_published_suppression([asdict(row)])[0]
    if any(safe[field] is not None for field in PROTECTED_FIELDS):
        raise ValueError("Suppressed card exposes a protected field")
    return {
        "indicator_id": row.indicator_id,
        "indicator_name": row.indicator_name,
        "module_label": "3.2 Violencia en el hogar",
        "disaggregation": row.disaggregation,
        "category": row.category,
        "quality_status": row.quality_status,
        "quality_label": QUALITY_LABELS[row.quality_status],
        "release_id": row.release_id,
        "state": "SHADOW",
        "universe_text": row.universe,
        "denominator_text": f"Denominador: {row.denominator}",
        "protected_values_visible": False,
        **{field: safe[field] for field in PROTECTED_FIELDS},
    }


def build_state_cards(repository: IndicatorRepository) -> list[dict]:
    """Build the three documented demo states through the Repository interface."""
    cards = []
    for row in repository.list_estimates("3.2"):
        cards.append(build_suppressed_card(row) if row.suppress_flag else build_numeric_card(row))
    return cards
