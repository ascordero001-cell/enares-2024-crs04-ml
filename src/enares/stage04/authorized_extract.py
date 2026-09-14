"""Deterministic rederivation of a manifest-bound Stage 04 V0 extract."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from .authorized_scopes import D09_PAIRS
from .indicator_semantics import C3P213_DISPLAY_LABEL, D01_TASKS
from .quality_rules import derive_statistical_quality

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
OUTPUT_FIELDS = (
    "release_id",
    "run_id",
    "source_version",
    "source_hash",
    "git_commit_sha",
    "container_image_digest",
    "dataform_release",
    "engine_version",
    "scale",
    "indicator_id",
    "indicator_name",
    "module_id",
    "disaggregation",
    "category",
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "n_unweighted",
    "weighted_population",
    "cv_flag",
    "n_flag",
    "suppress_flag",
    "quality_note",
    "validation_status",
    "created_at",
    "universe",
    "denominator",
    "quality_status",
    "synthetic",
)
ETAPA1_INDICATORS = frozenset(
    {
        "Componentes",
        "CONS_ATENCION_SALUD",
        "C3P223_10_1",
        "Agresor_VS_12M__AG_01",
        "C3P213",
    }
)
MODULE_BY_INDICATOR = {
    "Componentes": "3.1",
    "C3P223_10_1": "3.3",
    "Agresor_VS_12M__AG_01": "3.4",
    "CONS_ATENCION_SALUD": "3.5",
    "C3P213": "3.6",
}
DISPLAY_NAME_BY_D11_INDICATOR = {
    "C3P223_10_1": (
        "Ha recibido mensajes de texto que le hacen sentir mal en forma virtual o escritos"
    ),
    "Agresor_VS_12M__AG_01": "Familiares",
    "C3P213": C3P213_DISPLAY_LABEL,
}
UNIVERSE_BY_INDICATOR = {
    "Componentes": (
        "Adolescentes de 12 a 17 años con respuesta válida al ítem C3P302 correspondiente"
    ),
    "C3P223_10_1": "Adolescentes de 12 a 17 años con VP_ESCUELA = 1",
    "Agresor_VS_12M__AG_01": "Adolescentes de 12 a 17 años con VS_12M = 1",
    "CONS_ATENCION_SALUD": (
        "Adolescentes de 12 a 17 años con CONS_ALGUNA = 1 y respuesta válida"
    ),
    "C3P213": "Adolescentes de 12 a 17 años con dom_no_recibio_hogar = 1",
}
DENOMINATOR_BY_INDICATOR = {
    "Componentes": "Casos con respuesta válida al ítem C3P302 correspondiente",
    "C3P223_10_1": "Casos con VP_ESCUELA = 1 y respuesta válida",
    "Agresor_VS_12M__AG_01": "Casos con VS_12M = 1 y respuesta válida",
    "CONS_ATENCION_SALUD": (
        "Respuestas válidas de CONS_ATENCION_SALUD dentro de CONS_ALGUNA = 1"
    ),
    "C3P213": "Casos con dom_no_recibio_hogar = 1 y respuesta válida",
}


def _selected_etapa1_parent_rows(parent_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    task_categories = {item.task for item in D01_TASKS}
    selected = []
    for row in parent_rows:
        indicator = row["indicator_id"]
        if indicator == "Componentes" and (
            row["dimension"] == "Tareas del hogar"
            and row["categoria"] in task_categories
        ):
            selected.append(row)
        elif indicator == "CONS_ATENCION_SALUD":
            display_dimension = {
                "Área y sexo": "Área × sexo",
                "Lengua materna": "Idioma del hogar",
            }.get(row["dimension"], row["dimension"])
            if (display_dimension, row["categoria"]) in D09_PAIRS:
                selected.append(row)
        elif indicator in DISPLAY_NAME_BY_D11_INDICATOR and (
            row["dimension"], row["categoria"]
        ) == ("Nacional", "Total"):
            selected.append(row)
    return selected


def build_etapa1_authorized_extract(
    parent_path: Path,
    output_path: Path,
    manifest_path: Path,
    *,
    expected_parent_sha256: str,
    git_commit_sha: str,
    generated_at_utc: str | None = None,
) -> dict[str, object]:
    """Build the exact 35-row Etapa 1 extract from the approved parent aggregate."""
    parent_path = Path(parent_path)
    output_path = Path(output_path)
    manifest_path = Path(manifest_path)
    actual_parent_sha = hashlib.sha256(parent_path.read_bytes()).hexdigest().upper()
    if actual_parent_sha != expected_parent_sha256.upper():
        raise ValueError("Parent aggregate SHA-256 does not match the approved baseline")
    with parent_path.open(encoding="utf-8", newline="") as handle:
        selected = _selected_etapa1_parent_rows(list(csv.DictReader(handle)))
    if len(selected) != 35:
        raise ValueError(f"Etapa 1 scope must contain exactly 35 rows, found {len(selected)}")

    task_names = {item.task: item.display_label for item in D01_TASKS}
    generated_at = generated_at_utc or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    output_rows: list[dict[str, object]] = []
    for source in selected:
        indicator = source["indicator_id"]
        dimension = {"Área y sexo": "Área × sexo", "Lengua materna": "Idioma del hogar"}.get(
            source["dimension"], source["dimension"]
        )
        quality = derive_statistical_quality(
            estimate=float(source["pct"]),
            cv=float(source["cv"]),
            cv_unit="proportion",
            n_unweighted=int(source["base_unw"]),
        )
        if indicator == "Componentes":
            indicator_name = task_names[source["categoria"]]
        elif indicator == "CONS_ATENCION_SALUD":
            indicator_name = "CONS_ATENCION_SALUD"
        else:
            indicator_name = DISPLAY_NAME_BY_D11_INDICATOR[indicator]
        output_rows.append(
            {
                "release_id": "enares2024-crs04-v0-shadow-etapa1-001",
                "run_id": "etapa1-authorized-extract-20260914",
                "source_version": "v0_official_drive_baseline",
                "source_hash": actual_parent_sha,
                "git_commit_sha": git_commit_sha,
                "container_image_digest": "BLOCKED_BY_CLOUD_GATE",
                "dataform_release": "BLOCKED_BY_CLOUD_GATE",
                "engine_version": "v0_csv",
                "scale": "0_100",
                "indicator_id": indicator,
                "indicator_name": indicator_name,
                "module_id": MODULE_BY_INDICATOR[indicator],
                "disaggregation": dimension,
                "category": source["categoria"],
                "estimate": source["pct"],
                "standard_error": source["es"],
                "ci95_lower": source["ci_low"],
                "ci95_upper": source["ci_high"],
                "cv": source["cv"],
                "n_unweighted": source["base_unw"],
                "weighted_population": "",
                "cv_flag": str(quality.cv_flag).lower(),
                "n_flag": str(quality.n_flag).lower(),
                "suppress_flag": "false",
                "quality_note": " ".join(quality.quality_notes)
                or "Sin alerta de precisión.",
                "validation_status": "APPROVED",
                "created_at": generated_at,
                "universe": UNIVERSE_BY_INDICATOR[indicator],
                "denominator": DENOMINATOR_BY_INDICATOR[indicator],
                "quality_status": quality.quality_status,
                "synthetic": "false",
            }
        )
    output_rows.sort(
        key=lambda row: (
            str(row["module_id"]),
            str(row["indicator_id"]),
            str(row["disaggregation"]),
            str(row["category"]),
        )
    )
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    extract_sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
    manifest: dict[str, object] = {
        "file_name": output_path.name,
        "generated_at_utc": generated_at,
        "row_count": len(output_rows),
        "schema_version": "stage04-v0-authorized-aggregate-v1",
        "sha256": extract_sha,
        "synthetic": False,
        "data_classification": "AUTHORIZED_AGGREGATE_ONLY",
        "source_kind": "AUTHORIZED_V0_EXTRACT",
        "source_hash": actual_parent_sha,
        "parent_sha256": actual_parent_sha,
        "source_version": "v0_official_drive_baseline",
        "scope": {"D01": 10, "D09": 22, "D11": 3, "D12": "aliases_applied"},
        "purpose": "Etapa 1 local shadow authorized aggregate",
        "prohibition": "no microdata / no institutional publication",
        "approval_reference": "PR #63 and acta D01-D12",
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


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
