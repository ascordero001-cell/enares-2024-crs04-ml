from pathlib import Path


OUTPUT = Path(
    "sql/stage03/pilot_32_household_preflight.sql"
)

form_calls = []

for index in range(1, 12):
    form_calls.append(
        "household_form("
        f"SEXO, C3P201_{index}, C3P203, "
        f"C3P201A_{index}, C3P201E_{index}, "
        f"C3P201C_{index}, C3P201D_{index}, "
        f"C3P201F_{index}"
        ") = 1"
    )

any_form = "\n      OR ".join(form_calls)

query = f"""
CREATE TEMP FUNCTION household_form(
  p_sexo FLOAT64,
  p_item FLOAT64,
  p_gateway FLOAT64,
  p_perpetrator_a FLOAT64,
  p_perpetrator_e FLOAT64,
  p_confirm_c FLOAT64,
  p_confirm_d FLOAT64,
  p_confirm_f FLOAT64
)
RETURNS INT64
AS (
  CASE
    WHEN
      p_sexo IN (1, 2)
      AND p_item = 1
      AND p_gateway = 1
      AND (
        p_perpetrator_a IN (1, 2, 3, 4, 19)
        OR p_perpetrator_e IN (1, 2, 3, 4, 19)
        OR (
          p_perpetrator_a IS NOT NULL
          AND p_perpetrator_a NOT IN (1, 2, 3, 4, 19)
          AND p_confirm_c = 1
          AND p_confirm_d = 1
        )
        OR (
          p_perpetrator_e IS NOT NULL
          AND p_perpetrator_e NOT IN (1, 2, 3, 4, 19)
          AND p_confirm_f = 1
        )
      )
    THEN 1
    ELSE 0
  END
);

WITH
candidate AS (
  SELECT
    ID,
    COLEGIAL_ID,
    CASE
      WHEN
        {any_form}
      THEN 1
      ELSE 0
    END AS candidate_value
  FROM
    `enares-2024-crs04.enares2024_crs04_cleaned.cleaned_crs04_merged_adolescents_v0_5`
),

reference AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
    CAST(VP_HOGAR AS INT64) AS reference_value
  FROM
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_adolescents`
)

SELECT
  COUNTIF(
    candidate.ID IS NOT NULL
    AND reference.ID IS NOT NULL
  ) AS matched_rows,

  COUNTIF(candidate.ID IS NULL) AS reference_only_rows,
  COUNTIF(reference.ID IS NULL) AS candidate_only_rows,

  COUNTIF(
    candidate.ID IS NOT NULL
    AND reference.ID IS NOT NULL
    AND candidate.candidate_value
        IS DISTINCT FROM reference.reference_value
  ) AS rows_with_differences,

  COUNTIF(candidate.candidate_value = 1) AS candidate_positive_count,
  COUNTIF(candidate.candidate_value = 0) AS candidate_zero_count,
  COUNTIF(candidate.candidate_value IS NULL) AS candidate_null_count,

  COUNTIF(reference.reference_value = 1) AS reference_positive_count,
  COUNTIF(reference.reference_value = 0) AS reference_zero_count,
  COUNTIF(reference.reference_value IS NULL) AS reference_null_count

FROM candidate
FULL OUTER JOIN reference
  USING (ID, COLEGIAL_ID);
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    query.strip() + "\n",
    encoding="utf-8",
    newline="\n",
)

print(f"Generated: {OUTPUT}")
print(f"Household item conditions: {len(form_calls)}")