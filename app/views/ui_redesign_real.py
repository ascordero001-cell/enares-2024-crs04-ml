"""Authorized view models for the Stage 04 UI redesign."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, replace
from functools import partial

from app.views.stage04_dashboard import build_numeric_card, load_validated_estimates
from enares.stage04.display_taxonomy import display_category, display_dimension
from enares.stage04.indicator_labels import indicator_display_name
from enares.stage04.report_topics import (
    AssignmentIndex,
    ReportTopic,
    TopicAssignment,
    TopicCatalogError,
    resolve_assignment,
)
from enares.stage04.repository import (
    IndicatorEstimate,
    IndicatorRepository,
    RepositoryContractError,
    is_verified_authorized_estimate,
)

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")


class ModuleIsolationError(RuntimeError):
    """A visible module was about to receive another module's aggregate."""


def enforce_module_isolation(
    rows: Iterable[AuthorizedRedesignResult],
    *,
    active_module_id: str,
    assignment: AssignmentIndex,
) -> list[AuthorizedRedesignResult]:
    if active_module_id not in MODULE_IDS:
        raise ModuleIsolationError(f"Invalid active module: {active_module_id}")
    materialized = list(rows)
    foreign: set[str] = set()
    for result in materialized:
        try:
            item = resolve_assignment(assignment, result.row)
        except TopicCatalogError as error:
            raise ModuleIsolationError(str(error)) from error
        if item.module_id != active_module_id:
            foreign.add(item.module_id)
    if foreign:
        raise ModuleIsolationError(
            f"Module {active_module_id} received foreign rows from {sorted(foreign)}"
        )
    return materialized


def rows_for_topic(
    results: Iterable[AuthorizedRedesignResult],
    *,
    active_module_id: str,
    topic: ReportTopic,
    assignment: AssignmentIndex,
) -> list[AuthorizedRedesignResult]:
    if topic.module_id != active_module_id:
        raise ModuleIsolationError(
            f"Topic {topic.topic_id} does not belong to {active_module_id}"
        )
    selected = [
        result
        for result in results
        if resolve_assignment(assignment, result.row).topic_id == topic.topic_id
    ]
    return enforce_module_isolation(
        selected,
        active_module_id=active_module_id,
        assignment=assignment,
    )


@dataclass(frozen=True)
class AuthorizedRedesignResult:
    """One provenance-verified aggregate prepared for the redesigned UI."""

    row: IndicatorEstimate
    state: str

    @property
    def display_name(self) -> str:
        """Return the presentation label without mutating release metadata."""
        return indicator_display_name(self.row.indicator_id, self.row.module_id)


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
            results.append(
                AuthorizedRedesignResult(row=row, state=authorized_state(row))
            )
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
        "Indicador": result.display_name,
        "Código": row.indicator_id,
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
        "label": f"{result.display_name} — {row.category}",
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


def format_percentage(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}%"


def format_cv(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%"


def format_n(value: int | None) -> str:
    return "—" if value is None else f"{value:,}".replace(",", " ")


VISIBLE_TECHNICAL_CODE = re.compile(
    r"(?:_|\bC\d+P\d+\b|\b(?:AG|CP|D)\s*\d+\b|\bICVAC\s*\d+\b)",
    re.IGNORECASE,
)

METADATA_CODE_LABELS = {
    "CONS_ATENCION_SALUD": "atención de salud por consecuencias físicas",
    "CONS_ALGUNA": "alguna consecuencia física",
    "VF_ESCUELA": "violencia física en la escuela",
    "VF_HOGAR": "violencia física en el hogar",
    "VP_ESCUELA": "violencia psicológica en la escuela",
    "VP_HOGAR": "violencia psicológica en el hogar",
    "VP_o_VF_ESCUELA": "violencia psicológica o física en la escuela",
    "VP_o_VF_HOGAR": "violencia psicológica o física en el hogar",
    "VP_o_VF_E": "violencia psicológica o física en la escuela",
    "VS_12M": "violencia sexual en los últimos 12 meses",
    "VS_VIDA": "violencia sexual alguna vez en la vida",
    "VS_E_1": "violencia sexual en la escuela alguna vez en la vida",
    "VS_H_1": "violencia sexual en el hogar alguna vez en la vida",
    "VS_E": "violencia sexual en la escuela",
    "VS_H": "violencia sexual en el hogar",
    "C3P302": "pregunta correspondiente sobre violencia sexual",
    "dom_no_recibio_hogar": "quienes no recibieron ayuda por violencia en el hogar",
    "dom_no_recibio_escuela": "quienes no recibieron ayuda por violencia en la escuela",
    "dom_no_recibio_vs": "quienes no recibieron ayuda por violencia sexual",
    "dom_busco_hogar": "quienes buscaron ayuda por violencia en el hogar",
    "dom_busco_escuela": "quienes buscaron ayuda por violencia en la escuela",
    "dom_busco_vs": "quienes buscaron ayuda por violencia sexual",
    "dom_recibio_hogar": "quienes recibieron ayuda por violencia en el hogar",
    "dom_recibio_escuela": "quienes recibieron ayuda por violencia en la escuela",
    "dom_recibio_vs": "quienes recibieron ayuda por violencia sexual",
    "dom_victima_hogar": "víctimas de violencia en el hogar",
    "dom_victima_escuela": "víctimas de violencia en la escuela",
    "dom_victima_vs": "víctimas de violencia sexual",
    "dom_institucion_hogar": "quienes acudieron a una institución por violencia en el hogar",
    "dom_institucion_escuela": "quienes acudieron a una institución por violencia en la escuela",
    "dom_institucion_vs": "quienes acudieron a una institución por violencia sexual",
    "dom_ayuda_inst_vs": "quienes recibieron ayuda institucional por violencia sexual",
}


def _condition_label(match: re.Match[str], *, label: str) -> str:
    return label if match.group(1) == "1" else f"sin {label}"


def safe_metadata_text(value: str) -> str:
    """Translate known V0 domain variables without mutating their source fields."""
    visible = value or "—"
    condition = re.fullmatch(r"\s*([A-Za-z0-9_]+)\s*={1,2}\s*([012])\s*", visible)
    if condition:
        code, answer = condition.groups()
        if code == "SEXO":
            sex_label = display_category("Sexo", answer)
            return {"Mujer": "Mujeres", "Hombre": "Hombres"}[sex_label]
        if code not in METADATA_CODE_LABELS or answer not in {"0", "1"}:
            raise ModuleIsolationError("Untranslated V0 domain condition")
        label = METADATA_CODE_LABELS[code]
        if answer == "0":
            return f"sin {label}"
        return label
    for code in sorted(METADATA_CODE_LABELS, key=len, reverse=True):
        visible = re.sub(
            rf"(?<!\w){re.escape(code)}\s*={{1,2}}\s*([01])(?!\w)",
            partial(_condition_label, label=METADATA_CODE_LABELS[code]),
            visible,
        )
        visible = re.sub(
            rf"(?<!\w){re.escape(code)}(?!\w)",
            METADATA_CODE_LABELS[code],
            visible,
        )
    if "_" in visible or "=" in visible or VISIBLE_TECHNICAL_CODE.search(visible):
        raise ModuleIsolationError("Untranslated technical code in V0 metadata")
    return visible


def safe_indicator_display_name(
    indicator_id: str,
    *,
    presentation_module_id: str,
    topic_title: str,
    display_label_override: str = "",
) -> str:
    label = (
        display_label_override.strip()
        or indicator_display_name(indicator_id, presentation_module_id).strip()
    )
    if (
        not label
        or label.casefold() == indicator_id.casefold()
        or indicator_id.casefold() in label.casefold()
        or VISIBLE_TECHNICAL_CODE.search(label)
    ):
        return topic_title
    return label


def visible_indicator_name(
    result: AuthorizedRedesignResult,
    *,
    topic: ReportTopic,
    topic_assignment: TopicAssignment,
) -> str:
    return safe_indicator_display_name(
        result.row.indicator_id,
        presentation_module_id=topic.module_id,
        topic_title=topic.title,
        display_label_override=topic_assignment.display_label_override,
    )


def numeric_values_are_visible(result: AuthorizedRedesignResult) -> bool:
    return result.state not in {"SUPPRESSED", "CONTEXT_ONLY"} and not bool(
        getattr(result.row, "suppress_flag", False)
    )


def protected_percentage(result: AuthorizedRedesignResult, value: float | None) -> str:
    return format_percentage(value if numeric_values_are_visible(result) else None)


def protected_interval(result: AuthorizedRedesignResult) -> str:
    if not numeric_values_are_visible(result):
        return "—"
    return (
        f"{format_percentage(result.row.ci95_lower)} – "
        f"{format_percentage(result.row.ci95_upper)}"
    )


_OVERLAP_PAIR = re.compile(r"^P\((.+?) \| (.+?)\):")
_OVERLAP_FORMS = {
    "con contacto (301 o 302)": ("Con contacto", "violencia sexual con contacto"),
    "no física (303)": ("Sin contacto físico", "violencia sexual sin contacto físico"),
    "agresión con contacto (302)": ("Agresión con contacto", "agresión sexual con contacto"),
    "violación (301)": ("Violación", "violación"),
}


def visible_overlap_labels(category: str) -> tuple[str, str, str]:
    """Translate an approved V0 directed pair for display, not for export."""
    match = _OVERLAP_PAIR.match(category)
    if match is None or any(form not in _OVERLAP_FORMS for form in match.groups()):
        raise ModuleIsolationError("Unknown V0 sexual-overlap category")
    target, given = match.groups()
    target_short, target_name = _OVERLAP_FORMS[target]
    given_short, given_name = _OVERLAP_FORMS[given]
    description = (
        f"Entre quienes sufrieron {given_name}: % que también sufrió {target_name}"
    )
    return target_short, given_short, description


def visible_cut(result: AuthorizedRedesignResult) -> str:
    row = result.row
    if row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}:
        return f"Matriz {row.disaggregation} · {visible_overlap_labels(row.category)[2]}"
    if row.disaggregation == "Nacional":
        if row.category.casefold() in {"total", "nacional (total)"}:
            return "Nacional"
        return f"Nacional · {row.category}"
    return f"{display_dimension(row.disaggregation)} · {display_category(row.disaggregation, row.category)}"


def visible_table_record(
    result: AuthorizedRedesignResult,
    *,
    topic: ReportTopic,
    topic_assignment: TopicAssignment,
) -> dict[str, str]:
    row = result.row
    visible = numeric_values_are_visible(result)
    return {
        "Indicador": visible_indicator_name(
            result, topic=topic, topic_assignment=topic_assignment
        ),
        "Período": topic_assignment.period_label,
        "Corte": visible_cut(result),
        "Estimación": protected_percentage(result, row.estimate),
        "IC95%": protected_interval(result),
        "CV": format_cv(row.cv if visible else None),
        "N": format_n(row.n_unweighted if visible else None),
        "Estado y notas": STATE_LABELS[result.state],
    }


def protected_export_row(result: AuthorizedRedesignResult) -> IndicatorEstimate:
    if numeric_values_are_visible(result):
        return result.row
    return replace(
        result.row,
        estimate=None,
        standard_error=None,
        ci95_lower=None,
        ci95_upper=None,
        cv=None,
        n_unweighted=None,
    )
