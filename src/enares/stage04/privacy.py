"""Complementary suppression controls for synthetic aggregate tables."""

from __future__ import annotations

from copy import deepcopy


PROTECTED_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "n_unweighted",
)


def apply_published_suppression(rows: list[dict]) -> list[dict]:
    """Materialize suppression before rows reach a view or export."""
    published = deepcopy(rows)
    for row in published:
        if row.get("suppress_flag"):
            for field in PROTECTED_FIELDS:
                row[field] = None
    return published


def assert_no_unique_additive_reconstruction(rows: list[dict]) -> None:
    """Reject a visible total with exactly one suppressed additive child."""
    by_id = {row["cell_id"]: row for row in rows}
    child_ids: dict[str, list[str]] = {}
    for row in rows:
        parent = row.get("parent_total_id")
        if parent:
            child_ids.setdefault(parent, []).append(row["cell_id"])

    for total_id, children in child_ids.items():
        total = by_id[total_id]
        if total.get("suppress_flag"):
            continue
        hidden = [by_id[cell_id] for cell_id in children if by_id[cell_id].get("suppress_flag")]
        visible = [by_id[cell_id] for cell_id in children if not by_id[cell_id].get("suppress_flag")]
        if len(hidden) == 1 and total.get("estimate") is not None and all(
            row.get("estimate") is not None for row in visible
        ):
            raise ValueError("Primary cell can be uniquely reconstructed from total and margins")


def assert_suppressed_fields_are_null(rows: list[dict]) -> None:
    for row in rows:
        if row.get("suppress_flag") and any(row.get(field) is not None for field in PROTECTED_FIELDS):
            raise ValueError("Suppressed published cell exposes a protected statistic")
