"""Pure view models for the Stage 04 synthetic UI redesign."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SyntheticResult:
    module_id: str
    module_label: str
    indicator: str
    dimension: str
    category: str
    estimate: float | None
    lower: float | None
    upper: float | None
    cv_flag: bool = False
    n_flag: bool = False
    suppress_flag: bool = False
    context_only: bool = False
    authorized: bool = True


SYNTHETIC_RESULTS = (
    SyntheticResult("3.1", "Roles y tareas en el hogar", "SYN_31_A", "Nacional", "Total", 54.2, 51.1, 57.3),
    SyntheticResult("3.2", "Violencia en el hogar", "SYN_32_A", "Nacional", "Total", 16.7, 15.7, 17.7),
    SyntheticResult("3.2", "Violencia en el hogar", "SYN_32_B", "Área", "Rural", 8.4, 4.1, 12.7, cv_flag=True),
    SyntheticResult("3.3", "Violencia en la escuela", "SYN_33_A", "Sexo", "Mujer", 22.8, 19.4, 26.2, n_flag=True),
    SyntheticResult("3.4", "Violencia sexual", "SYN_34_A", "Área", "Urbano", 6.3, 2.4, 10.2, cv_flag=True, n_flag=True),
    SyntheticResult("3.5", "Acumulación y consecuencias", "SYN_35_CONTEXT", "Nacional", "Contexto", None, None, None, context_only=True),
    SyntheticResult("3.5", "Acumulación y consecuencias", "SYN_35_SUPPRESSED", "Nacional", "Ejercicio", None, None, None, suppress_flag=True),
    SyntheticResult("3.6", "Búsqueda de ayuda", "SYN_36_PENDING", "Nacional", "Combinación simulada", None, None, None, authorized=False),
)


def state_code(row: SyntheticResult) -> str:
    """Derive a display state without conflating statistical flags."""
    if row.suppress_flag:
        return "SUPPRESSED"
    if not row.authorized:
        return "PENDING_AUTHORIZATION"
    if row.context_only:
        return "CONTEXT_ONLY"
    if row.cv_flag and row.n_flag:
        return "REFERENCE_HIGH_CV_AND_SMALL_N"
    if row.cv_flag:
        return "REFERENCE_HIGH_CV"
    if row.n_flag:
        return "SMALL_N"
    return "PUBLISHABLE_SHADOW"


STATE_LABELS = {
    "PUBLISHABLE_SHADOW": "Sin alerta",
    "REFERENCE_HIGH_CV": "Referencial por CV",
    "SMALL_N": "Alerta de N reducido",
    "REFERENCE_HIGH_CV_AND_SMALL_N": "Referencial por CV + alerta de N reducido",
    "CONTEXT_ONLY": "Contexto no numérico",
    "PENDING_AUTHORIZATION": "Pendiente de autorización",
    "SUPPRESSED": "Suprimido por confidencialidad (ejercicio sintético)",
}


def filter_synthetic_results(
    *, module_id: str, dimension: str, states: tuple[str, ...]
) -> list[SyntheticResult]:
    """Filter only the in-memory synthetic fixture."""
    return [
        row
        for row in SYNTHETIC_RESULTS
        if (module_id == "Todos" or row.module_id == module_id)
        and (dimension == "Todas" or row.dimension == dimension)
        and state_code(row) in states
    ]


def effective_view_results(
    rows: list[SyntheticResult], *, active_view: str
) -> list[SyntheticResult]:
    """Apply the active module view to an already-filtered selection."""
    if not active_view.startswith("Módulo "):
        return list(rows)
    module_id = active_view.removeprefix("Módulo ")
    return [row for row in rows if row.module_id == module_id]


def table_record(row: SyntheticResult) -> dict[str, object]:
    """Build a table row, withholding numeric fields for protected/non-numeric states."""
    state = state_code(row)
    show_numeric = state not in {
        "SUPPRESSED",
        "CONTEXT_ONLY",
        "PENDING_AUTHORIZATION",
    }
    return {
        "Módulo": row.module_id,
        "Indicador": row.indicator,
        "Dimensión": row.dimension,
        "Categoría": row.category,
        "Estimación (%)": row.estimate if show_numeric else None,
        "IC95 % inferior": row.lower if show_numeric else None,
        "IC95 % superior": row.upper if show_numeric else None,
        "Estado": STATE_LABELS[state],
    }


def forest_record(row: SyntheticResult) -> dict[str, object] | None:
    """Return an already-authorized numeric point for the synthetic forest plot."""
    if row.estimate is None or row.lower is None or row.upper is None:
        return None
    if row.suppress_flag or row.context_only or not row.authorized:
        return None
    return {
        "label": f"{row.module_id} · {row.category}",
        "estimate": row.estimate,
        "lower": row.lower,
        "upper": row.upper,
        "state": STATE_LABELS[state_code(row)],
    }


def serialized_fixture() -> list[dict[str, object]]:
    """Expose a testable copy without sharing mutable fixture state."""
    return [asdict(row) for row in SYNTHETIC_RESULTS]
