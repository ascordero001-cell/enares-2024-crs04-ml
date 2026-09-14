"""Complementary suppression controls for synthetic aggregate tables."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction

PROTECTED_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "n_unweighted",
    "weighted_population",
)
PUBLICATION_CHANNELS = ("ui", "export", "cache", "log")
PRIMARY_SUPPRESSION_ACTIVE = False
PRODUCER_DOMINANCE_SIGNAL_AVAILABLE = False


def requires_primary_suppression_controls(
    *,
    authorized_finer_than_department: bool,
    authorized_non_v0_cross: bool,
) -> bool:
    """Activate dormant controls only for an explicitly authorized scope expansion."""
    if not isinstance(authorized_finer_than_department, bool) or not isinstance(
        authorized_non_v0_cross, bool
    ):
        raise TypeError("Granularity activation inputs must be boolean")
    return authorized_finer_than_department or authorized_non_v0_cross


def assert_v0_granularity_boundary(
    *,
    requested_dimensions: set[str],
    v0_dimensions: set[str],
    requested_crosses: set[tuple[str, ...]],
    v0_crosses: set[tuple[str, ...]],
    synthetic: bool = False,
) -> None:
    """Block dimensions and crosses that do not already exist in official V0."""
    if not isinstance(synthetic, bool):
        raise TypeError("synthetic must be boolean")
    if synthetic:
        return
    extra_dimensions = requested_dimensions - v0_dimensions
    extra_crosses = requested_crosses - v0_crosses
    if extra_dimensions or extra_crosses:
        raise ValueError(
            "Requested output exceeds the approved V0 granularity boundary"
        )


def apply_published_suppression(rows: list[dict]) -> list[dict]:
    """Materialize suppression before rows reach a view or export."""
    published = deepcopy(rows)
    for row in published:
        if row.get("suppress_flag"):
            for field in PROTECTED_FIELDS:
                row[field] = None
    return published


def materialize_safe_channel_payloads(rows: list[dict]) -> dict[str, list[dict]]:
    """Create every outward payload from one already-nullified publication boundary."""
    published = apply_published_suppression(rows)
    assert_suppressed_fields_are_null(published)
    return {channel: deepcopy(published) for channel in PUBLICATION_CHANNELS}


def assert_consistent_suppression_within_release(rows: list[dict]) -> None:
    """A stable cell cannot be hidden in one table and visible in another."""
    decisions: dict[tuple[str, str], set[bool]] = {}
    for row in rows:
        key = (row["release_id"], row["cell_id"])
        decisions.setdefault(key, set()).add(bool(row.get("suppress_flag")))
    if any(len(flags) != 1 for flags in decisions.values()):
        raise ValueError("A cell has inconsistent suppression within one release")


def assert_no_retroactive_suppression(
    candidate_rows: list[dict],
    all_published_history_rows: list[dict],
) -> None:
    """Block attempts to hide a stable cell after any prior publication."""
    historically_visible = {
        row["cell_id"]
        for row in all_published_history_rows
        if not row.get("suppress_flag")
    }
    newly_hidden = {
        row["cell_id"] for row in candidate_rows if row.get("suppress_flag")
    }
    exposed = historically_visible & newly_hidden
    if exposed:
        raise ValueError(
            "A previously visible cell cannot be protected by later suppression"
        )


def _matrix_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix if any(row)]
    if not work:
        return 0
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for index, row in enumerate(work):
            if index != rank and row[column]:
                factor = row[column]
                work[index] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(row, work[rank], strict=True)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def uniquely_reconstructable_primary_cells(
    rows: list[dict],
    equations: list[dict],
) -> set[str]:
    """Return primary cells uniquely determined by the combined equation system."""
    hidden = {row["cell_id"] for row in rows if row.get("suppress_flag")}
    primary = {
        row["cell_id"]
        for row in rows
        if row.get("suppress_flag") and row.get("suppression_type") == "PRIMARY"
    }
    columns = sorted(hidden)
    matrix = [
        [Fraction(equation["terms"].get(cell_id, 0)) for cell_id in columns]
        for equation in equations
    ]
    full_rank = _matrix_rank(matrix)
    unique = set()
    for cell_id in primary:
        if cell_id not in columns:
            continue
        position = columns.index(cell_id)
        without_cell = [row[:position] + row[position + 1 :] for row in matrix]
        if full_rank > _matrix_rank(without_cell):
            unique.add(cell_id)
    return unique


def assert_no_reconstructable_primary(
    rows: list[dict],
    equations: list[dict],
) -> None:
    """Fail when any primary cell is solvable from all available equations."""
    assert_consistent_suppression_within_release(rows)
    reconstructable = uniquely_reconstructable_primary_cells(rows, equations)
    if reconstructable:
        raise ValueError(
            "Primary cells are reconstructable from the combined equation system: "
            + ", ".join(sorted(reconstructable))
        )


def plan_complementary_suppression(
    rows: list[dict],
    equations: list[dict],
) -> list[dict]:
    """Add deterministic complementaries until no primary is uniquely solvable."""
    planned = deepcopy(rows)
    while uniquely_reconstructable_primary_cells(planned, equations):
        candidates = sorted(
            (
                row
                for row in planned
                if not row.get("suppress_flag")
                and row.get("eligible_for_complementary", False)
                and any(
                    equation["terms"].get(row["cell_id"], 0) for equation in equations
                )
            ),
            key=lambda row: (row["base_unw"], row["cell_id"]),
        )
        if not candidates:
            raise ValueError("No safe complementary suppression plan is available")
        selected = candidates[0]
        selected["suppress_flag"] = True
        selected["suppression_type"] = "COMPLEMENTARY"
        selected["suppression_reason"] = "PROTECT_PRIMARY_FROM_RECONSTRUCTION"

    assert_no_reconstructable_primary(planned, equations)
    return planned


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
        hidden = [
            by_id[cell_id]
            for cell_id in children
            if by_id[cell_id].get("suppress_flag")
        ]
        visible = [
            by_id[cell_id]
            for cell_id in children
            if not by_id[cell_id].get("suppress_flag")
        ]
        if (
            len(hidden) == 1
            and total.get("estimate") is not None
            and all(row.get("estimate") is not None for row in visible)
        ):
            raise ValueError(
                "Primary cell can be uniquely reconstructed from total and margins"
            )


def assert_suppressed_fields_are_null(rows: list[dict]) -> None:
    for row in rows:
        if row.get("suppress_flag") and any(
            row.get(field) is not None for field in PROTECTED_FIELDS
        ):
            raise ValueError("Suppressed published cell exposes a protected statistic")
