"""Pure catalog filtering used by the synthetic C0 navigation checkpoint."""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogLocator:
    module_id: str
    indicator_id: str
    label: str
    dimension: str
    category: str
    synthetic: bool = True
    focus: str = ""
    population: str = ""
    context: str = ""
    period: str = ""


def _search_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return " ".join(
        "".join(char for char in decomposed if not unicodedata.combining(char)).split()
    )


def filter_catalog(
    rows: Iterable[CatalogLocator],
    *,
    module_id: str,
    dimension: str,
    query: str,
    focus: str | None = None,
    population: str | None = None,
    context: str | None = None,
    period: str | None = None,
) -> tuple[CatalogLocator, ...]:
    """Apply module/scope, semantic search and optional human-readable facets."""
    tokens = _search_text(query).split()
    matches = []
    for row in rows:
        if row.synthetic is not True:
            raise ValueError("C0 accepts only explicit synthetic=true locators")
        if row.module_id != module_id or row.dimension != dimension:
            continue
        if focus is not None and row.focus != focus:
            continue
        if population is not None and row.population != population:
            continue
        if context is not None and row.context != context:
            continue
        if period is not None and row.period != period:
            continue
        semantic_fields = " ".join(
            value
            for value in (
                row.focus,
                row.population,
                row.context,
                row.period,
                row.category,
            )
            if value
        )
        # The module and scope are already selected controls. Searching only the
        # distinguishing fields prevents a word repeated in a module title from
        # making every row look relevant (the root cause of C0-01).
        haystack = _search_text(semantic_fields or f"{row.label} {row.category}")
        if all(token in haystack for token in tokens):
            matches.append(row)
    return tuple(
        sorted(
            matches,
            key=lambda row: (
                row.focus,
                row.population,
                row.period,
                row.context,
                row.label,
                row.indicator_id,
            ),
        )
    )
