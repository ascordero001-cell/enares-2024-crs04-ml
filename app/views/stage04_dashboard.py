"""Pure presentation helpers for the safe local 3.2 application shell."""

from __future__ import annotations

from dataclasses import asdict
from html import escape

from app.config import QUALITY_LABELS, get_module
from enares.stage04.authorized_scopes import D09_CATEGORY_LABELS
from enares.stage04.indicator_semantics import (
    D01_RELATIONSHIP_GROUP,
    D01_TASK_EXECUTION_GROUP,
)
from enares.stage04.privacy import PROTECTED_FIELDS, apply_published_suppression
from enares.stage04.repository import IndicatorEstimate, IndicatorRepository
from enares.stage04.validation import validate_estimates
from enares.stage04.view_model import to_card_view_model

EXPORT_ENABLED = False


def escape_dynamic_text(value: object) -> str:
    """Return repository-provided text as inert display content."""
    return escape(str(value), quote=True)


def precision_category_label(category: str, cv_flag: bool) -> str:
    """Derive the visible precision marker from the statistical flag only."""
    clean_category = category.removesuffix(" [referencial]")
    return f"{clean_category} [referencial]" if cv_flag else clean_category


def load_validated_estimates(
    repository: IndicatorRepository,
    module_id: str,
) -> list[IndicatorEstimate]:
    """Load a catalog and enforce its statistical contract before UI use."""
    rows = repository.list_estimates(module_id)
    if rows:
        validate_estimates(rows)
    return rows


def filter_estimates(
    repository: IndicatorRepository,
    module_id: str,
    disaggregation: str,
    category: str,
) -> list[IndicatorEstimate]:
    """Return only combinations present in the repository; never synthesize missing results."""
    return [
        row
        for row in load_validated_estimates(repository, module_id)
        if row.disaggregation == disaggregation and row.category == category
    ]


def build_numeric_card(row: IndicatorEstimate) -> dict:
    """Extend the approved card view model with details required by the local UI."""
    if row.suppress_flag:
        raise ValueError("A suppressed row cannot build a numeric card")
    validate_estimates([row])
    card = to_card_view_model(row)
    for field in (
        "category",
        "denominator_text",
        "disaggregation",
        "indicator_id",
        "indicator_name",
        "release_id",
        "source_version",
        "universe_text",
    ):
        card[field] = escape_dynamic_text(card[field])
    card.update(
        {
            "category_display": escape_dynamic_text(
                precision_category_label(row.category, row.cv_flag)
            ),
            "cv_flag": row.cv_flag,
            "standard_error_text": f"EE {row.standard_error:.4f}",
            "quality_label": escape_dynamic_text(
                "Aprobado para shadow — sin alerta"
                if row.validation_status == "APPROVED"
                and row.quality_status == "PUBLISHABLE_CANDIDATE"
                else QUALITY_LABELS[row.quality_status]
            ),
            "quality_note": escape_dynamic_text(row.quality_note),
            "denominator": escape_dynamic_text(row.denominator),
            "created_at": escape_dynamic_text(row.created_at),
            "protected_values_visible": True,
        }
    )
    return card


def build_suppressed_card(row: IndicatorEstimate) -> dict:
    """Materialize suppression before constructing a non-numeric interface state."""
    if not row.suppress_flag:
        raise ValueError("Only a suppressed row can build a suppressed card")
    validate_estimates([row])
    safe = apply_published_suppression([asdict(row)])[0]
    if any(safe[field] is not None for field in PROTECTED_FIELDS):
        raise ValueError("Suppressed card exposes a protected field")
    return {
        "indicator_id": escape_dynamic_text(row.indicator_id),
        "indicator_name": escape_dynamic_text(row.indicator_name),
        "module_label": get_module(row.module_id).full_label,
        "disaggregation": escape_dynamic_text(row.disaggregation),
        "category": escape_dynamic_text(row.category),
        "quality_status": row.quality_status,
        "quality_label": escape_dynamic_text(QUALITY_LABELS[row.quality_status]),
        "quality_note": escape_dynamic_text(row.quality_note),
        "release_id": escape_dynamic_text(row.release_id),
        "state": "SHADOW",
        "universe_text": escape_dynamic_text(row.universe),
        "denominator_text": escape_dynamic_text(f"Denominador: {row.denominator}"),
        "protected_values_visible": False,
        **{field: safe[field] for field in PROTECTED_FIELDS},
    }


def build_state_cards(
    repository: IndicatorRepository,
    module_id: str = "3.2",
) -> list[dict]:
    """Build the three documented demo states through the Repository interface."""
    cards = []
    for row in load_validated_estimates(repository, module_id):
        cards.append(
            build_suppressed_card(row) if row.suppress_flag else build_numeric_card(row)
        )
    return cards


def build_d01_task_groups(
    repository: IndicatorRepository,
) -> tuple[list[dict], list[dict]]:
    """Build the two approved D01 groups without conflating their questions."""
    rows = load_validated_estimates(repository, "3.1")
    by_category = {
        row.category: row
        for row in rows
        if row.indicator_id == "Componentes"
        and row.disaggregation == "Tareas del hogar"
    }
    expected = {
        item.task for item in (*D01_TASK_EXECUTION_GROUP, *D01_RELATIONSHIP_GROUP)
    }
    if set(by_category) != expected or len(rows) != len(expected):
        raise ValueError(
            "D01 authorized task scope is incomplete or contains extra rows"
        )

    def cards_for(group) -> list[dict]:
        return [build_numeric_card(by_category[item.task]) for item in group]

    return cards_for(D01_TASK_EXECUTION_GROUP), cards_for(D01_RELATIONSHIP_GROUP)


def d09_category_label(disaggregation: str, category: str) -> str:
    """Resolve approved D09 labels while preserving uncoded source categories."""
    return D09_CATEGORY_LABELS.get((disaggregation, category), category)
