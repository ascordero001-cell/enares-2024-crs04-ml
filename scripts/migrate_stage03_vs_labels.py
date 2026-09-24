"""Create a new, label-only Stage 03 V0 derivative without overwriting V0.

The input is the approved private aggregate CSV, never microdata. This tool
does not publish or connect its output to Stage 04.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = "15b845da4a886fdcf54a96d8b8471b6f6be618ae18b43024488c6bd6b23d0bb4"
MATRICES = frozenset({"Solap_VS_12M", "Solap_VS_VIDA"})
SUFFIX = " [referencial]"
NUMERIC_FIELDS = (
    "pct",
    "es",
    "ci_low",
    "ci_high",
    "cv",
    "n_unw",
    "target_unw",
    "base_unw",
    "local_critical",
    "cell_critical",
)


def is_referential_cv(cv: str) -> bool:
    """The Stage 03 CV column is a proportion, not a percentage."""
    return float(cv) > 0.15


def migrate_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Remove only the eight legacy markers, preserving every other field."""
    migrated: list[dict[str, str]] = []
    source_markers = {indicator: 0 for indicator in MATRICES}
    cv_referential = {indicator: 0 for indicator in MATRICES}
    matrix_rows = {indicator: 0 for indicator in MATRICES}
    for row in rows:
        new_row = row.copy()
        indicator = row["indicator_id"]
        marker = row["categoria"].endswith(SUFFIX)
        if indicator in MATRICES:
            matrix_rows[indicator] += 1
            cv_referential[indicator] += is_referential_cv(row["cv"])
            if marker:
                if row["dimension"] != "3×3":
                    raise ValueError("Legacy marker outside a 3×3 VS matrix")
                source_markers[indicator] += 1
                new_row["categoria"] = row["categoria"].removesuffix(SUFFIX)
        elif marker:
            raise ValueError("Unexpected legacy marker outside D06/D07")
        for field in NUMERIC_FIELDS:
            if new_row[field] != row[field]:
                raise AssertionError(f"Numeric field changed: {field}")
        migrated.append(new_row)

    if len(rows) != 3014 or matrix_rows != dict.fromkeys(MATRICES, 8):
        raise ValueError("Source is not the approved 3,014-row V0 matrix inventory")
    if source_markers != dict.fromkeys(MATRICES, 4):
        raise ValueError(
            "Source does not contain exactly four legacy labels per matrix"
        )
    if cv_referential != {"Solap_VS_12M": 4, "Solap_VS_VIDA": 0}:
        raise ValueError("CV classification differs from approved V0 evidence")
    return migrated, {
        "source_marker_rows": sum(source_markers.values()),
        "cv_referential_rows": sum(cv_referential.values()),
        "rows": len(rows),
    }


def create_version(source: Path, destination: Path) -> dict[str, object]:
    source_bytes = source.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    if source_hash != SOURCE_SHA256:
        raise ValueError("Input SHA-256 is not the frozen approved V0 baseline")
    if source.resolve() == destination.resolve() or destination.exists():
        raise FileExistsError("A new destination is required; V0 cannot be overwritten")

    # The approved source is UTF-8 CSV. Numeric values are retained as strings.
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if fields is None or not {
            "indicator_id",
            "dimension",
            "categoria",
            *NUMERIC_FIELDS,
        } <= set(fields):
            raise ValueError("Unexpected V0 CSV columns")
        rows = list(reader)
    migrated, counts = migrate_rows(rows)
    with destination.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(migrated)
    result = {
        "source_sha256": source_hash,
        "output_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "output_name": destination.name,
        **counts,
        "scope": "Stage 03 label-only derivative; not promoted or published",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="private approved V0 aggregate CSV")
    parser.add_argument("destination", type=Path, help="new versioned CSV path")
    args = parser.parse_args()
    print(
        json.dumps(
            create_version(args.source, args.destination), ensure_ascii=False, indent=2
        )
    )


if __name__ == "__main__":
    main()
