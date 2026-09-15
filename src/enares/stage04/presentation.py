"""Approved presentation aliases that preserve source metadata."""

from __future__ import annotations

from dataclasses import dataclass

PRESENTATION_SURFACES = frozenset(
    {"card", "table", "chart", "tooltip", "print", "export"}
)
AREA_SEX_DISPLAY_NAME = "Área × sexo"
HOME_LANGUAGE_DISPLAY_NAME = "Idioma del hogar"


@dataclass(frozen=True)
class DimensionPresentation:
    """Keep an approved display label separate from its source identifiers."""

    display_name: str
    source_name: str
    source_code: str


DIMENSION_PRESENTATIONS = {
    "Área y sexo": DimensionPresentation(
        display_name=AREA_SEX_DISPLAY_NAME,
        source_name="Área y sexo",
        source_code="AREA BY SEXO",
    ),
    "Lengua materna": DimensionPresentation(
        display_name=HOME_LANGUAGE_DISPLAY_NAME,
        source_name="Lengua materna",
        source_code="idiomaHogar",
    ),
}


def resolve_dimension_presentation(source_name: str) -> DimensionPresentation:
    """Resolve an approved alias without discarding the original metadata."""
    try:
        return DIMENSION_PRESENTATIONS[source_name]
    except KeyError as error:
        raise ValueError(f"Unregistered source dimension: {source_name}") from error


def dimension_label_for_surface(source_name: str, surface: str) -> str:
    """Return one consistent label for every approved presentation surface."""
    if surface not in PRESENTATION_SURFACES:
        raise ValueError(f"Unknown presentation surface: {surface}")
    return resolve_dimension_presentation(source_name).display_name
