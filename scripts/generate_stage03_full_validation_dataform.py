"""Generate the consolidated Stage 03 V0.5 shadow and full parity gates."""

from __future__ import annotations

import re
from pathlib import Path

try:
    from scripts.generate_stage31_dataform import (
        build_stage31_contract,
        output_columns as stage31_columns,
    )
    from scripts.generate_stage32_dataform import (
        build_stage32_contract,
        output_columns as stage32_columns,
    )
    from scripts.generate_stage33_dataform import (
        build_stage33_contract,
        output_columns as stage33_columns,
    )
    from scripts.generate_stage34_dataform import (
        build_stage34_contract,
        output_columns as stage34_columns,
    )
    from scripts.generate_stage35_dataform import (
        build_stage35_contract,
        output_columns as stage35_columns,
    )
    from scripts.generate_stage36_dataform import (
        build_stage36_contract,
        output_columns as stage36_columns,
    )
except ModuleNotFoundError:
    from generate_stage31_dataform import (
        build_stage31_contract,
        output_columns as stage31_columns,
    )
    from generate_stage32_dataform import (
        build_stage32_contract,
        output_columns as stage32_columns,
    )
    from generate_stage33_dataform import (
        build_stage33_contract,
        output_columns as stage33_columns,
    )
    from generate_stage34_dataform import (
        build_stage34_contract,
        output_columns as stage34_columns,
    )
    from generate_stage35_dataform import (
        build_stage35_contract,
        output_columns as stage35_columns,
    )
    from generate_stage36_dataform import (
        build_stage36_contract,
        output_columns as stage36_columns,
    )


CLEANED_SQLX = Path(
    "dataform/definitions/cleaned/cleaned_crs04_merged_adolescents_v0_5.sqlx"
)
MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_full_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage03_full_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage03_full_shadow_v0_parity.sqlx"
)

EXPECTED_ROWS = 18_807
EXPECTED_CLEANED_COLUMNS = 1_206
EXPECTED_DERIVED_COLUMNS = 730
EXPECTED_FULL_COLUMNS = 1_937
KEY_COLUMNS = ["ID", "COLEGIAL_ID"]


def cleaned_columns() -> list[str]:
    """Read the explicit cleaned model projection in its canonical order."""

    text = CLEANED_SQLX.read_text(encoding="utf-8")
    columns = re.findall(r" AS `([^`]+)`", text)
    if len(columns) != EXPECTED_CLEANED_COLUMNS:
        raise ValueError(
            f"Expected {EXPECTED_CLEANED_COLUMNS} cleaned columns, "
            f"found {len(columns)}"
        )
    if len(columns) != len(set(columns)):
        raise ValueError("Cleaned projection contains duplicate columns")
    return columns


def section_columns() -> list[tuple[str, list[str]]]:
    """Return each validated section table and its ordered outputs."""

    return [
        (
            "analytical_crs04_stage31_v0_5",
            stage31_columns(build_stage31_contract()[1]),
        ),
        (
            "analytical_crs04_stage32_v0_5",
            stage32_columns(build_stage32_contract()[1]),
        ),
        (
            "analytical_crs04_stage33_v0_5",
            stage33_columns(build_stage33_contract()[1]),
        ),
        (
            "analytical_crs04_stage34_v0_5",
            stage34_columns(build_stage34_contract()[1]),
        ),
        (
            "analytical_crs04_stage35_v0_5",
            stage35_columns(build_stage35_contract()[1]),
        ),
        (
            "analytical_crs04_stage36_v0_5",
            stage36_columns(build_stage36_contract()[1]),
        ),
    ]


def derived_columns() -> list[str]:
    columns = [column for _, group in section_columns() for column in group]
    if len(columns) != EXPECTED_DERIVED_COLUMNS:
        raise ValueError(
            f"Expected {EXPECTED_DERIVED_COLUMNS} derived columns, "
            f"found {len(columns)}"
        )
    if len(columns) != len(set(columns)):
        raise ValueError("Derived sections contain duplicate columns")
    overlap = set(columns) & set(cleaned_columns())
    if overlap:
        raise ValueError(f"Derived/cleaned collisions: {sorted(overlap)}")
    return columns


def full_columns() -> list[str]:
    columns = cleaned_columns() + ["ID_AULA"] + derived_columns()
    if len(columns) != EXPECTED_FULL_COLUMNS:
        raise ValueError(
            f"Expected {EXPECTED_FULL_COLUMNS} full columns, found {len(columns)}"
        )
    if len(columns) != len(set(columns)):
        raise ValueError("Full projection contains duplicate columns")
    return columns


def render_model() -> str:
    stage_aliases = [f"stage{section}" for section in range(31, 37)]
    derived_select = []
    joins = []
    for alias, (table_name, columns) in zip(
        stage_aliases, section_columns(), strict=True
    ):
        derived_select.extend(
            f"  {alias}.`{column}` AS `{column}`" for column in columns
        )
        joins.append(
            f'LEFT JOIN ${{ref("{table_name}")}} AS {alias}\n'
            "  USING (ID, COLEGIAL_ID)"
        )
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.analyticalDataset,
  name: "analytical_crs04_full_v0_5",
  description: "Consolidated Stage 03 V0.5 shadow with all SPSS-derived columns.",
  tags: ["stage03", "analytical", "full", "shadow", "validation"]
}}

SELECT
  cleaned.*,
  CONCAT(
    CAST(cleaned.ID AS STRING), "_",
    CAST(cleaned.C3ANIO AS STRING), "_",
    CAST(cleaned.TURNO AS STRING), "_",
    UPPER(TRIM(CAST(cleaned.C3SECC AS STRING)))
  ) AS ID_AULA,
{",\n".join(derived_select)}
FROM ${{ref("cleaned_crs04_merged_adolescents_v0_5")}} AS cleaned
{"\n".join(joins)}
'''


def normalized_select(source: str) -> str:
    """Render the full projection with normalized respondent-key types."""

    columns = full_columns()
    projection = []
    for column in columns:
        if column in KEY_COLUMNS:
            projection.append(f"    CAST({source}.`{column}` AS INT64) AS `{column}`")
        else:
            projection.append(f"    {source}.`{column}` AS `{column}`")
    return ",\n".join(projection)


def render_quality_assertion() -> str:
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "full", "quality"]
}}

WITH
candidate AS (
  SELECT * FROM ${{ref("analytical_crs04_full_v0_5")}}
),
duplicate_keys AS (
  SELECT ID, COLEGIAL_ID FROM candidate
  GROUP BY ID, COLEGIAL_ID HAVING COUNT(*) > 1
),
schema_count AS (
  SELECT COUNT(*) AS column_count
  FROM `enares-2024-crs04.enares2024_crs04_analytical.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = "analytical_crs04_full_v0_5"
),
checks AS (
  SELECT "row_count" AS check_name, ABS(COUNT(*) - {EXPECTED_ROWS}) AS violation_count
  FROM candidate HAVING COUNT(*) != {EXPECTED_ROWS}
  UNION ALL
  SELECT "null_keys", COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0
  UNION ALL
  SELECT "duplicate_key_groups", COUNT(*) FROM duplicate_keys HAVING COUNT(*) > 0
  UNION ALL
  SELECT "null_id_aula", COUNTIF(ID_AULA IS NULL)
  FROM candidate HAVING COUNTIF(ID_AULA IS NULL) > 0
  UNION ALL
  SELECT "schema_column_count", ABS(column_count - {EXPECTED_FULL_COLUMNS})
  FROM schema_count WHERE column_count != {EXPECTED_FULL_COLUMNS}
)
SELECT * FROM checks
'''


def render_parity_assertion() -> str:
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "full", "parity"]
}}

WITH
reference AS (
  SELECT
{normalized_select("reference_source")}
  FROM ${{ref("analytical_crs04_adolescents")}} AS reference_source
),
candidate AS (
  SELECT
{normalized_select("candidate_source")}
  FROM ${{ref("analytical_crs04_full_v0_5")}} AS candidate_source
)
SELECT
  COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(candidate.COLEGIAL_ID, reference.COLEGIAL_ID) AS COLEGIAL_ID
FROM candidate
FULL OUTER JOIN reference USING (ID, COLEGIAL_ID)
WHERE
  candidate.ID IS NULL
  OR reference.ID IS NULL
  OR TO_JSON_STRING(candidate) IS DISTINCT FROM TO_JSON_STRING(reference)
'''


def main() -> None:
    columns = full_columns()
    for path, content in [
        (MODEL_OUTPUT, render_model()),
        (QUALITY_OUTPUT, render_quality_assertion()),
        (PARITY_OUTPUT, render_parity_assertion()),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")
        print(f"Generated: {path}")
    print(f"Cleaned columns: {len(cleaned_columns())}")
    print(f"Derived columns: {len(derived_columns())}")
    print(f"Full columns: {len(columns)}")


if __name__ == "__main__":
    main()
