"""Single synthetic catalog and frozen task protocol shared by C0 and C2."""

from __future__ import annotations

from dataclasses import dataclass

from .catalog_navigation import CatalogLocator

CATALOG_SIZE = 516
PER_MODULE = 86
HUMAN_TIME_LIMIT_SECONDS = 90.0
ALLOWED_HELP = "Solo el texto de la tarea; sin conocer el ID y sin ayuda externa."


@dataclass(frozen=True)
class NavigationTask:
    task_id: str
    module_id: str
    dimension: str
    query: str
    expected_indicator_id: str


MODULE_THEMES = {
    "3.1": "Roles, cuidado y corresponsabilidad en el hogar",
    "3.2": "Violencia física y psicológica en el hogar",
    "3.3": "Violencia física y psicológica en la escuela",
    "3.4": "Situaciones de violencia sexual en adolescentes",
    "3.5": "Acumulación, solapamiento y consecuencias de violencias",
    "3.6": "Búsqueda de ayuda, respuesta y barreras de acceso",
}


def build_synthetic_catalog() -> tuple[CatalogLocator, ...]:
    """Build exactly 516 synthetic locators with deliberately difficult labels."""
    rows: list[CatalogLocator] = []
    for module_id, theme in MODULE_THEMES.items():
        module_number = module_id.replace(".", "")
        for sequence in range(1, PER_MODULE + 1):
            dimension = "Departamento" if sequence == PER_MODULE else "Nacional"
            period = "12 meses" if sequence % 2 == 0 else "alguna vez"
            label = (
                f"{theme} — indicador sintético repetido {sequence:03d} "
                f"(periodo sintético ({period})) — resultado con prefijo casi duplicado"
            )
            rows.append(
                CatalogLocator(
                    module_id=module_id,
                    indicator_id=f"SYN_C0_{module_number}_{sequence:03d}",
                    label=label,
                    dimension=dimension,
                    category=f"Categoría sintética cercana {sequence:03d} ({period})",
                )
            )
    return tuple(rows)


C0_TASKS = (
    NavigationTask("C0-01", "3.1", "Nacional", "corresponsabilidad repetido 031", "SYN_C0_31_031"),
    NavigationTask("C0-02", "3.2", "Nacional", "hogar repetido 032 12 meses", "SYN_C0_32_032"),
    NavigationTask("C0-03", "3.3", "Nacional", "escuela repetido 033", "SYN_C0_33_033"),
    NavigationTask("C0-04", "3.4", "Nacional", "sexual repetido 034 12 meses", "SYN_C0_34_034"),
    NavigationTask("C0-05", "3.5", "Nacional", "solapamiento repetido 035", "SYN_C0_35_035"),
    NavigationTask("C0-06", "3.6", "Nacional", "barreras acceso repetido 036", "SYN_C0_36_036"),
    NavigationTask("C0-07", "3.2", "Departamento", "hogar repetido 086 12 meses", "SYN_C0_32_086"),
)
