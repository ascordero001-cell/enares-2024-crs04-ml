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


def _semantic_relevance(
    row: CatalogLocator,
    *,
    normalized_query: str,
    tokens: tuple[str, ...],
) -> int:
    """Score query evidence in meaningful fields without arbitrary text tie-breaks."""
    weighted_fields = (
        (row.focus, 5),
        (row.population, 4),
        (row.context, 3),
        (row.period, 3),
        (row.category, 1),
    )
    score = 0
    for value, weight in weighted_fields:
        normalized_value = _search_text(value)
        score += weight * sum(token in normalized_value for token in tokens)
        if normalized_query and normalized_query in normalized_value:
            score += weight * max(len(tokens), 1) * 2
        if normalized_query and normalized_query == normalized_value:
            score += weight * max(len(tokens), 1) * 4
    return score


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
    normalized_query = _search_text(query)
    tokens = tuple(normalized_query.split())
    matches: list[tuple[int, CatalogLocator]] = []
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
        visible_haystack = _search_text(f"{row.label} {row.category}")
        if all(token in visible_haystack for token in tokens):
            matches.append(
                (
                    _semantic_relevance(
                        row,
                        normalized_query=normalized_query,
                        tokens=tokens,
                    ),
                    row,
                )
            )
    # sorted() is stable: equally relevant candidates retain canonical catalog order.
    # In particular, population text is never used as an arbitrary tie-breaker.
    return tuple(
        item[1]
        for item in sorted(
            matches,
            key=lambda item: -item[0],
        )
    )
