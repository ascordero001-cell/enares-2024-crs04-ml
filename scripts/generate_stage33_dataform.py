"""Generate the complete Stage 03 section 3.3 shadow model and assertions.

The formulas directly transcribe the ordered SPSS-authority implementation in
notebook 02. The generator makes the SQLX reproducible and exposes a contract
that unit tests can inspect independently of BigQuery.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage33_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage33_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage33_shadow_v0_parity.sqlx"
)

KEY_DESIGN_COLUMNS = [
    "ID",
    "COLEGIAL_ID",
    "FACTOR_ALUMNOS",
    "CCDD",
    "SEXO",
    "AREA",
]


def any_one(names: Iterable[str]) -> str:
    return "(" + " OR ".join(f"`{name}` = 1" for name in names) + ")"


def school_aggressor_expressions(
    stem: str, item_count: int, gateway: str, kind: str
) -> dict[str, str]:
    """Return the nine published school aggressor groups."""

    specifications: dict[int, tuple[str, int | None]] = {
        1: ("A", None),
        2: ("A", 1),
        3: ("A", 2),
        4: ("A", 3),
        5: ("C", None),
        6: ("C", 1),
        7: ("C", 2),
        8: ("C", 3),
        9: ("E", None),
    }
    expressions: dict[str, str] = {}
    for group, (person_suffix, age) in specifications.items():
        hits = []
        for index in range(1, item_count + 1):
            person = f"{stem}{person_suffix}_{index}"
            condition = (
                f"{stem}_{index} = 1 AND {gateway} = 1 AND {person} = 1"
            )
            if age is not None:
                age_suffix = "B" if person_suffix == "A" else "D"
                condition += f" AND {stem}{age_suffix}_{index} = {age}"
            hits.append(f"({condition})")
        expressions[f"AG_{kind}_E_{group:02d}"] = (
            "CASE WHEN " + " OR ".join(hits) + " THEN 1 ELSE 0 END"
        )
    return expressions


def build_stage33_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the three ordered SPSS 3.3 expression blocks."""

    raw_inputs = {"C3P225", "C3P229"}
    school_forms: dict[str, str] = {}
    for stem, item_count, gateway in [
        ("C3P223", 14, "C3P225"),
        ("C3P227", 10, "C3P229"),
    ]:
        for index in range(1, item_count + 1):
            item = f"{stem}_{index}"
            first_person = f"{stem}A_{index}"
            first_age = f"{stem}B_{index}"
            second_person = f"{stem}C_{index}"
            second_age = f"{stem}D_{index}"
            other_person = f"{stem}E_{index}"
            raw_inputs.update(
                {
                    item,
                    first_person,
                    first_age,
                    second_person,
                    second_age,
                    other_person,
                }
            )
            school_forms[f"{stem}_{index}_1"] = (
                f"CASE WHEN {item} = 1 AND {gateway} = 1 "
                f"AND ({first_person} = 1 OR {second_person} = 1 "
                f"OR {other_person} = 1) THEN 1 ELSE 0 END"
            )

    main_indicators = {
        "VP_ESCUELA": (
            "CASE WHEN "
            + any_one(f"C3P223_{index}_1" for index in range(1, 15))
            + " THEN 1 ELSE 0 END"
        ),
        "VF_ESCUELA": (
            "CASE WHEN "
            + any_one(f"C3P227_{index}_1" for index in range(1, 11))
            + " THEN 1 ELSE 0 END"
        ),
        "VPE_ICVAC_401_ATERRORIZAR": (
            "CASE WHEN "
            + any_one(["C3P223_12_1", "C3P223_13_1"])
            + " THEN 1 ELSE 0 END"
        ),
        "VPE_ICVAC_402_HOSTIGAR_HUMILLAR": (
            "CASE WHEN "
            + any_one(f"C3P223_{index}_1" for index in range(1, 11))
            + " THEN 1 ELSE 0 END"
        ),
        "VPE_ICVAC_203_AISLAMIENTO": (
            "CASE WHEN C3P223_11_1 = 1 THEN 1 ELSE 0 END"
        ),
        "VPE_ICVAC_409_OTROS": (
            "CASE WHEN C3P223_14_1 = 1 THEN 1 ELSE 0 END"
        ),
        "VFE_ICVAC_201_AGRESION_GRAVE": (
            "CASE WHEN "
            + any_one(f"C3P227_{index}_1" for index in [5, 7, 8, 9])
            + " THEN 1 ELSE 0 END"
        ),
        "VFE_ICVAC_202_AGRESION_LEVE": (
            "CASE WHEN "
            + any_one(f"C3P227_{index}_1" for index in [1, 2, 3, 4, 6])
            + " THEN 1 ELSE 0 END"
        ),
        "VFE_ICVAC_209_OTROS": (
            "CASE WHEN C3P227_10_1 = 1 THEN 1 ELSE 0 END"
        ),
    }

    aggressors = {
        **school_aggressor_expressions("C3P223", 14, "C3P225", "VP"),
        **school_aggressor_expressions("C3P227", 10, "C3P229", "VF"),
    }

    blocks = [
        ("33_escuela_formas", school_forms),
        ("33_escuela_principales", main_indicators),
        ("331_escuela_agresores", aggressors),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def render_model() -> str:
    raw_inputs, blocks = build_stage33_contract()
    raw_only = sorted(set(raw_inputs) - set(KEY_DESIGN_COLUMNS))
    base_columns = KEY_DESIGN_COLUMNS + raw_only
    base_select = ",\n".join(f"    `{column}`" for column in base_columns)

    ctes = [
        "base AS (\n"
        "  SELECT\n"
        f"{base_select}\n"
        '  FROM ${ref("cleaned_crs04_merged_adolescents_v0_5")}\n'
        ")"
    ]
    previous = "base"
    for index, (block_name, expressions) in enumerate(blocks, start=1):
        cte_name = f"block_{index:02d}_{block_name}"
        derived = ",\n".join(
            f"    {expression} AS `{column}`"
            for column, expression in expressions.items()
        )
        ctes.append(
            f"{cte_name} AS (\n"
            "  SELECT\n"
            "    *,\n"
            f"{derived}\n"
            f"  FROM {previous}\n"
            ")"
        )
        previous = cte_name

    final_columns = KEY_DESIGN_COLUMNS + output_columns(blocks)
    final_select = ",\n".join(f"  `{column}`" for column in final_columns)
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.analyticalDataset,
  name: "analytical_crs04_stage33_v0_5",
  description: "Stage 03 section 3.3 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage33", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    _, blocks = build_stage33_contract()
    binary_condition = "\n    OR ".join(
        f"`{column}` NOT IN (0, 1) OR `{column}` IS NULL"
        for column in output_columns(blocks)
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage33", "quality"]
}}

WITH
candidate AS (
  SELECT *
  FROM ${{ref("analytical_crs04_stage33_v0_5")}}
),

duplicate_keys AS (
  SELECT ID, COLEGIAL_ID
  FROM candidate
  GROUP BY ID, COLEGIAL_ID
  HAVING COUNT(*) > 1
),

checks AS (
  SELECT "row_count" AS check_name, ABS(COUNT(*) - 18807) AS violation_count
  FROM candidate
  HAVING COUNT(*) != 18807

  UNION ALL

  SELECT "null_keys", COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate
  HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0

  UNION ALL

  SELECT "duplicate_key_groups", COUNT(*)
  FROM duplicate_keys
  HAVING COUNT(*) > 0

  UNION ALL

  SELECT "survey_design_fields", COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL
  )
  FROM candidate
  HAVING COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL
  ) > 0

  UNION ALL

  SELECT "binary_outputs", COUNTIF(
    {binary_condition}
  )
  FROM candidate
  HAVING COUNTIF(
    {binary_condition}
  ) > 0
)

SELECT *
FROM checks
'''


def render_parity_assertion() -> str:
    _, blocks = build_stage33_contract()
    columns = output_columns(blocks)
    reference_select = ",\n".join(f"    `{column}`" for column in columns)
    candidate_select = ",\n".join(f"    `{column}`" for column in columns)
    comparisons = "\n  OR ".join(
        f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
        for column in columns
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage33", "parity"]
}}

WITH
reference AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
{reference_select}
  FROM ${{ref("analytical_crs04_adolescents")}}
),

candidate AS (
  SELECT
    ID,
    COLEGIAL_ID,
{candidate_select}
  FROM ${{ref("analytical_crs04_stage33_v0_5")}}
)

SELECT
  COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(candidate.COLEGIAL_ID, reference.COLEGIAL_ID) AS COLEGIAL_ID
FROM candidate
FULL OUTER JOIN reference
  USING (ID, COLEGIAL_ID)
WHERE
  candidate.ID IS NULL
  OR reference.ID IS NULL
  OR {comparisons}
'''


def main() -> None:
    _, blocks = build_stage33_contract()
    outputs = [
        (MODEL_OUTPUT, render_model()),
        (QUALITY_OUTPUT, render_quality_assertion()),
        (PARITY_OUTPUT, render_parity_assertion()),
    ]
    for path, content in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")
        print(f"Generated: {path}")
    print(f"Blocks generated: {len(blocks)}")
    print(f"Derived columns generated: {len(output_columns(blocks))}")


if __name__ == "__main__":
    main()
