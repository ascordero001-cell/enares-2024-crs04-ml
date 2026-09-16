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
    matches: list[tuple[int, int, CatalogLocator]] = []
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
        semantic_haystack = _search_text(semantic_fields)
        visible_haystack = _search_text(f"{row.label} {row.category}")
        if all(token in visible_haystack for token in tokens):
            semantic_token_count = sum(
                token in semantic_haystack for token in tokens
            )
            semantic_phrase_match = int(
                bool(tokens) and _search_text(query) in semantic_haystack
            )
            matches.append((semantic_phrase_match, semantic_token_count, row))
    return tuple(
        item[2]
        for item in sorted(
            matches,
            key=lambda item: (
                -item[0],
                -item[1],
                item[2].focus,
                item[2].population,
                item[2].period,
                item[2].context,
                item[2].label,
                item[2].indicator_id,
            ),
        )
    )
