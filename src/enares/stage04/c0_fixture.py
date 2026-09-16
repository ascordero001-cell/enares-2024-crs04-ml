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
    prompt: str


@dataclass(frozen=True)
class AutomatedNavigationCase:
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

FOCUSES = (
    "apoyo y acompañamiento",
    "respuesta institucional",
    "barreras para pedir ayuda",
    "experiencias reportadas",
    "redes de confianza",
    "consecuencias percibidas",
    "protección y cuidado",
    "corresponsabilidad cotidiana",
)
POPULATIONS = (
    "niñas y niños de 9 a 11 años",
    "adolescentes de 12 a 17 años",
    "estudiantes que buscaron ayuda",
    "estudiantes que no buscaron ayuda",
    "hogares con persona adulta de referencia",
    "comunidad educativa entrevistada",
)
CONTEXTS = ("ámbito urbano", "ámbito rural", "total del ámbito observado")
PERIODS = ("alguna vez", "últimos 12 meses")


def _descriptor(sequence: int) -> tuple[str, str, str, str]:
    """Return a unique semantic combination without relying on its sequence number."""
    offset = sequence - 1
    period = PERIODS[offset % len(PERIODS)]
    focus = FOCUSES[(offset // len(PERIODS)) % len(FOCUSES)]
    population = POPULATIONS[
        (offset // (len(PERIODS) * len(FOCUSES))) % len(POPULATIONS)
    ]
    context = CONTEXTS[offset % len(CONTEXTS)]
    return focus, population, context, period


def build_synthetic_catalog() -> tuple[CatalogLocator, ...]:
    """Build exactly 516 synthetic locators with deliberately difficult labels."""
    rows: list[CatalogLocator] = []
    for module_id, theme in MODULE_THEMES.items():
        module_number = module_id.replace(".", "")
        for sequence in range(1, PER_MODULE + 1):
            dimension = "Departamento" if sequence > 80 else "Nacional"
            focus, population, context, period = _descriptor(sequence)
            label = (
                f"{theme} — {focus} en {population} "
                f"(periodo sintético ({period}); {context}) — resultado sintético comparable"
            )
            rows.append(
                CatalogLocator(
                    module_id=module_id,
                    indicator_id=f"SYN_C0_{module_number}_{sequence:03d}",
                    label=label,
                    dimension=dimension,
                    category=f"{focus.capitalize()} · {population} · {context} · {period}",
                )
            )
    return tuple(rows)


C0_TASKS = (
    NavigationTask(
        "C0-01",
        "En el módulo 3.1 y alcance nacional, localiza el indicador sobre "
        "corresponsabilidad cotidiana en adolescentes de 12 a 17 años, alguna vez, "
        "para el ámbito urbano.",
    ),
    NavigationTask(
        "C0-02",
        "En el módulo 3.2 y alcance nacional, localiza el indicador sobre "
        "corresponsabilidad cotidiana en adolescentes de 12 a 17 años durante los "
        "últimos 12 meses, para el ámbito rural.",
    ),
    NavigationTask(
        "C0-03",
        "En el módulo 3.3 y alcance nacional, localiza el indicador sobre apoyo y "
        "acompañamiento entre estudiantes que buscaron ayuda, alguna vez, para el "
        "total del ámbito observado.",
    ),
    NavigationTask(
        "C0-04",
        "En el módulo 3.4 y alcance nacional, localiza el indicador sobre apoyo y "
        "acompañamiento entre estudiantes que buscaron ayuda durante los últimos "
        "12 meses, para el ámbito urbano.",
    ),
    NavigationTask(
        "C0-05",
        "En el módulo 3.5 y alcance nacional, localiza el indicador sobre respuesta "
        "institucional entre estudiantes que buscaron ayuda, alguna vez, para el "
        "ámbito rural.",
    ),
    NavigationTask(
        "C0-06",
        "En el módulo 3.6 y alcance nacional, localiza el indicador sobre respuesta "
        "institucional entre estudiantes que buscaron ayuda durante los últimos "
        "12 meses, para el total del ámbito observado.",
    ),
    NavigationTask(
        "C0-07",
        "En el módulo 3.2 y alcance departamental, localiza el indicador sobre "
        "barreras para pedir ayuda en comunidad educativa entrevistada durante los "
        "últimos 12 meses, para el ámbito rural.",
    ),
)

C0_AUTOMATION_CASES = (
    AutomatedNavigationCase("C0-01", "3.1", "Nacional", "corresponsabilidad", "SYN_C0_31_031"),
    AutomatedNavigationCase("C0-02", "3.2", "Nacional", "corresponsabilidad", "SYN_C0_32_032"),
    AutomatedNavigationCase("C0-03", "3.3", "Nacional", "acompañamiento", "SYN_C0_33_033"),
    AutomatedNavigationCase("C0-04", "3.4", "Nacional", "acompañamiento", "SYN_C0_34_034"),
    AutomatedNavigationCase("C0-05", "3.5", "Nacional", "respuesta", "SYN_C0_35_035"),
    AutomatedNavigationCase("C0-06", "3.6", "Nacional", "respuesta", "SYN_C0_36_036"),
    AutomatedNavigationCase("C0-07", "3.2", "Departamento", "barreras", "SYN_C0_32_086"),
)
