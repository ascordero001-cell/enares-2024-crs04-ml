"""Boundaries and immutability for the Stage 03 D06/D07 label migration."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

import scripts.migrate_stage03_vs_labels as migration
from scripts.migrate_stage03_vs_labels import (
    MATRICES,
    SUFFIX,
    create_version,
    is_referential_cv,
    migrate_rows,
)


@pytest.mark.parametrize(
    ("cv", "expected"),
    [("0.149999", False), ("0.15", False), ("0.150001", True)],
)
def test_strict_cv_threshold_in_proportion_scale(cv: str, expected: bool) -> None:
    assert is_referential_cv(cv) is expected


def _rows() -> list[dict[str, str]]:
    rows = []
    for indicator in sorted(MATRICES):
        for i in range(8):
            category = f"pair {i}" + (SUFFIX if i in {3, 5, 6, 7} else "")
            rows.append(
                {
                    "indicator_id": indicator,
                    "dimension": "3×3" if i >= 2 else "2×2",
                    "categoria": category,
                    "cv": "0.16"
                    if indicator == "Solap_VS_12M" and i in {3, 5, 6, 7}
                    else "0.08",
                    "pct": str(i),
                    "es": "1.234567890123",
                    "ci_low": "0.1",
                    "ci_high": "9.9",
                    "n_unw": "43",
                    "target_unw": "43",
                    "base_unw": "112",
                    "local_critical": "1.96",
                    "cell_critical": "2.05",
                }
            )
    for i in range(3014 - len(rows)):
        rows.append({**rows[0], "indicator_id": f"OTHER_{i}", "categoria": "Total"})
    return rows


def test_only_eight_labels_change_and_all_numbers_remain_exact() -> None:
    source = _rows()
    migrated, counts = migrate_rows(source)
    assert counts == {"source_marker_rows": 8, "cv_referential_rows": 4, "rows": 3014}
    assert sum(left != right for left, right in zip(source, migrated)) == 8
    assert all(SUFFIX not in row["categoria"] for row in migrated)
    for left, right in zip(source, migrated):
        assert {k: v for k, v in left.items() if k != "categoria"} == {
            k: v for k, v in right.items() if k != "categoria"
        }


def test_unexpected_marker_is_rejected() -> None:
    rows = _rows()
    rows[-1]["categoria"] = "Total" + SUFFIX
    with pytest.raises(ValueError, match="outside D06/D07"):
        migrate_rows(rows)


def test_frozen_source_hash_and_existing_destination_are_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.csv"
    destination = tmp_path / "new-version.csv"
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=_rows()[0])
        writer.writeheader()
        writer.writerows(_rows())
    with pytest.raises(ValueError, match="SHA-256"):
        create_version(source, destination)
    assert not destination.exists()
    monkeypatch.setattr(
        migration, "SOURCE_SHA256", hashlib.sha256(source.read_bytes()).hexdigest()
    )
    result = create_version(source, destination)
    assert result["rows"] == 3014
    assert result["source_marker_rows"] == 8
    assert result["cv_referential_rows"] == 4
    with source.open("r", encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    with destination.open("r", encoding="utf-8", newline="") as handle:
        output_rows = list(csv.DictReader(handle))
    assert len(output_rows) == len(source_rows)
    assert (
        sum(
            left["categoria"] != right["categoria"]
            for left, right in zip(source_rows, output_rows)
        )
        == 8
    )
    assert all(
        {key: value for key, value in left.items() if key != "categoria"}
        == {key: value for key, value in right.items() if key != "categoria"}
        for left, right in zip(source_rows, output_rows)
    )
    with pytest.raises(FileExistsError, match="new destination"):
        create_version(source, destination)
