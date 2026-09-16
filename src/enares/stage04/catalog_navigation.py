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
) -> tuple[CatalogLocator, ...]:
    """Apply the C0 staged path: module, dimension, then token search."""
    tokens = _search_text(query).split()
    matches = []
    for row in rows:
        if row.synthetic is not True:
            raise ValueError("C0 accepts only explicit synthetic=true locators")
        if row.module_id != module_id or row.dimension != dimension:
            continue
        haystack = _search_text(f"{row.indicator_id} {row.label} {row.category}")
        if all(token in haystack for token in tokens):
            matches.append(row)
    return tuple(sorted(matches, key=lambda row: (row.label, row.indicator_id)))
