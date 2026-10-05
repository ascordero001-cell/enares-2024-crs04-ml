"""Presentation-only aliases for approved V0 disaggregations and categories.

Source identifiers remain untouched in the repository and in export source_* fields.
"""

from __future__ import annotations

from collections.abc import Iterable

STANDARD_DIMENSIONS = (
    "Departamento",
    "Área",
    "Sexo",
    "Área × sexo",
    "Idioma del hogar",
    "Etnicidad",
    "Tipo de hogar",
    "Discapacidad",
)
DISPLAY_NAMES = {
    "Departamento": "Departamento",
    "Área": "Ámbito de la IIEE",
    "Sexo": "Sexo",
    "Área × sexo": "Sexo × ámbito de la IIEE",
    "Idioma del hogar": "Idioma del hogar",
    "Etnicidad": "Autoidentificación étnica",
    "Tipo de hogar": "Vive con padres",
    "Discapacidad": "Discapacidad",
}
OTHER_CHARACTERISTICS = "Otras características"
CATEGORY_LABELS = {
    "Área": {"1": "Urbano", "2": "Rural"},
    "Sexo": {"1": "Mujer", "2": "Hombre"},
    "Área × sexo": {
        "Urbano Hombre": "Urbano Hombre",
        "Urbano Mujer": "Urbano Mujer",
        "Rural Hombre": "Rural Hombre",
        "Rural Mujer": "Rural Mujer",
    },
    "Idioma del hogar": {
        "1": "Castellano",
        "3": "Lengua originaria de los Andes: Quechua/Aymara",
        "4": "Lengua originaria de la Amazonía: Otra lengua nativa",
        "5": "Idioma extranjero / No sabe",
    },
    "Etnicidad": {
        "1": "Población indígena u originaria de los Andes: Quechua/Aymara",
        "3": "Población indígena u originaria de la Amazonía: Nativo o indígena de la Amazonía / otro pueblo indígena u originario",
        "5": "Población afroperuana: Negro, moreno, zambo, mulato / pueblo afroperuano o afrodescendiente",
        "6": "Blanco/Mestizo",
        "9": "Otro / No sabe",
    },
    "Tipo de hogar": {"1": "Ambos", "2": "Uno", "3": "Ninguno"},
    "Discapacidad": {"0": "No", "1": "Sí"},
}


def display_dimension(source: str) -> str:
    """Show the approved human label while preserving the source key."""
    return DISPLAY_NAMES.get(source, source)


def display_category(source: str, category: str) -> str:
    """Reject unmapped standard codes; render binary contextual cuts legibly."""
    if source in CATEGORY_LABELS:
        try:
            return CATEGORY_LABELS[source][category]
        except KeyError as error:
            raise ValueError(f"Unmapped V0 category for {source}") from error
    if source not in STANDARD_DIMENSIONS and category in {"0", "1"}:
        return "No" if category == "0" else "Sí"
    return category


def category_sort_key(source: str, category: str) -> tuple[int, str]:
    """Use editorial order, never a numeric source-code sort."""
    if source in CATEGORY_LABELS:
        order = tuple(CATEGORY_LABELS[source])
        try:
            return order.index(category), ""
        except ValueError as error:
            raise ValueError(f"Unmapped V0 category for {source}") from error
    return 0, display_category(source, category).casefold()


def assert_standard_category_coverage(
    pairs: Iterable[tuple[str, str]],
) -> None:
    """Fail before rendering if V0 adds an unlabeled standard category."""
    for source, category in pairs:
        if source in CATEGORY_LABELS:
            display_category(source, category)
