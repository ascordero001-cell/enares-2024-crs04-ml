"""Deterministic rederivation of a manifest-bound Stage 04 V0 extract."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

SOURCE_DIMENSION = {
    "Área × sexo": "Área y sexo",
    "Idioma del hogar": "Lengua materna",
}
STATISTIC_FIELDS = {
    "estimate": "pct",
    "standard_error": "es",
    "ci95_lower": "ci_low",
    "ci95_upper": "ci_high",
    "cv": "cv",
    "n_unweighted": "base_unw",
}


def rederive_authorized_extract(
    parent_path: Path,
    template_path: Path,
    output_path: Path,
    *,
    expected_parent_file_sha256: str,
    approved_parent_sha256: str,
) -> None:
    """Replace every template statistic with the exact matching parent value.

    The template owns presentation metadata and the closed row list. The parent
    owns every numeric field. Missing or duplicate parent keys fail closed.
    """
    parent_path = Path(parent_path)
    template_path = Path(template_path)
    output_path = Path(output_path)
    actual_parent_sha = hashlib.sha256(parent_path.read_bytes()).hexdigest()
    if actual_parent_sha.lower() != expected_parent_file_sha256.lower():
        raise ValueError("Parent aggregate SHA-256 does not match the expected file")

    with parent_path.open(encoding="utf-8-sig", newline="") as handle:
        parent_rows = list(csv.DictReader(handle))
    parent_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in parent_rows:
        key = (row["indicator_id"], row["dimension"], row["categoria"])
        if key in parent_by_key:
            raise ValueError(f"Duplicate parent aggregate key: {key}")
        parent_by_key[key] = row

    with template_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or ())
        template_rows = list(reader)

    derived_rows = []
    for template in template_rows:
        source_dimension = SOURCE_DIMENSION.get(
            template["disaggregation"], template["disaggregation"]
        )
        key = (template["indicator_id"], source_dimension, template["category"])
        try:
            parent = parent_by_key[key]
        except KeyError as exc:
            raise ValueError(f"Authorized row is absent from parent aggregate: {key}") from exc
        derived = dict(template)
        derived["source_hash"] = approved_parent_sha256.upper()
        for output_field, parent_field in STATISTIC_FIELDS.items():
            derived[output_field] = parent[parent_field]
        derived_rows.append(derived)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(derived_rows)
