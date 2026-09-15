"""Explicit denominator mapping for a future approved V0 aggregate adapter."""

import re
from collections.abc import Mapping


def denominator_count(row: Mapping[str, str]) -> int:
    """Read base_unw only; never substitute target_unw or legacy n_unw."""
    value = row.get("base_unw")
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+", value):
        raise ValueError("base_unw must be a non-negative integer count")
    return int(value)
