from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/"
    "pilot_33_school_v0_5.sqlx"
)

QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/"
    "pilot_33_school_quality.sqlx"
)

PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/"
    "pilot_33_school_v0_parity.sqlx"
)


def detail_condition(index: int) -> str:
    return f"""CASE
      WHEN
        C3P223_{index} = 1
        AND C3P225 = 1
        AND (
          C3P223A_{index} = 1
          OR C3P223C_{index} = 1
          OR C3P223E_{index} = 1
        )
      THEN 1
      ELSE 0
    END"""


detail_names = [
    f"C3P223_{index}_1"
    for index in range(1, 15)
]

detail_selects = ",\n".join(
    f"    {detail_condition(index)} AS `{detail_names[index - 1]}`"
    for index in range(1, 15)
)

detail_output_columns = ",\n".join(
    f"  `{name}`"
    for name in detail_names
)

any_detail = "\n    OR ".join(
    f"`{name}` = 1"
    for name in detail_names
)

model = f"""config {{
  type: "table",
  schema: dataform.projectConfig.vars.analyticalDataset,
  name: "analytical_crs04_pilot_33_school_v0_5",
  description: "Stage 03 shadow pilot for SPSS VP_ESCUELA.",
  tags: ["stage03", "analytical", "pilot_33", "shadow"]
}}

WITH details AS (
  SELECT
    ID,
    COLEGIAL_ID,
    FACTOR_ALUMNOS,
    CCDD,
    SEXO,
    AREA,
    C3P225,
{detail_selects}
  FROM ${{ref("cleaned_crs04_merged_adolescents_v0_5")}}
)

SELECT
  ID,
  COLEGIAL_ID,
  FACTOR_ALUMNOS,
  CCDD,
  SEXO,
  AREA,
  C3P225,
{detail_output_columns},

  CASE
    WHEN
      {any_detail}
    THEN 1
    ELSE 0
  END AS VP_ESCUELA

FROM details
"""

quality = """config {
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "pilot_33"]
}

WITH
candidate AS (
  SELECT *
  FROM ${ref("analytical_crs04_pilot_33_school_v0_5")}
),

duplicate_keys AS (
  SELECT ID, COLEGIAL_ID
  FROM candidate
  GROUP BY ID, COLEGIAL_ID
  HAVING COUNT(*) > 1
),

checks AS (
  SELECT
    "row_count" AS check_name,
    ABS(COUNT(*) - 18807) AS violation_count
  FROM candidate
  HAVING COUNT(*) != 18807

  UNION ALL

  SELECT
    "null_keys",
    COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate
  HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0

  UNION ALL

  SELECT
    "duplicate_key_groups",
    COUNT(*)
  FROM duplicate_keys
  HAVING COUNT(*) > 0

  UNION ALL

  SELECT
    "indicator_domain_or_null",
    COUNTIF(VP_ESCUELA NOT IN (0, 1) OR VP_ESCUELA IS NULL)
  FROM candidate
  HAVING COUNTIF(
    VP_ESCUELA NOT IN (0, 1) OR VP_ESCUELA IS NULL
  ) > 0
)

SELECT *
FROM checks
"""

parity = """config {
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "pilot_33", "parity"]
}

WITH
reference AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
    CAST(VP_ESCUELA AS INT64) AS reference_value
  FROM ${ref("analytical_crs04_adolescents")}
),

candidate AS (
  SELECT
    ID,
    COLEGIAL_ID,
    VP_ESCUELA AS candidate_value
  FROM ${ref("analytical_crs04_pilot_33_school_v0_5")}
)

SELECT
  COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(
    candidate.COLEGIAL_ID,
    reference.COLEGIAL_ID
  ) AS COLEGIAL_ID,
  candidate.candidate_value,
  reference.reference_value

FROM candidate
FULL OUTER JOIN reference
  USING (ID, COLEGIAL_ID)

WHERE
  candidate.ID IS NULL
  OR reference.ID IS NULL
  OR candidate.candidate_value
     IS DISTINCT FROM reference.reference_value
"""

for output, content in [
    (MODEL_OUTPUT, model),
    (QUALITY_OUTPUT, quality),
    (PARITY_OUTPUT, parity),
]:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        content.strip() + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated: {output}")

print(f"Detail indicators generated: {len(detail_names)}")