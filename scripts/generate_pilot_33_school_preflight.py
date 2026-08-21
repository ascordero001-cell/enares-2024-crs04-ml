from pathlib import Path


OUTPUT = Path(
    "sql/stage03/pilot_33_school_preflight.sql"
)

form_calls = []

for index in range(1, 15):
    form_calls.append(
        "school_form("
        f"C3P223_{index}, C3P225, "
        f"C3P223A_{index}, C3P223C_{index}, "
        f"C3P223E_{index}"
        ") = 1"
    )

any_form = "\n      OR ".join(form_calls)

query = f"""
CREATE TEMP FUNCTION school_form(
  p_item FLOAT64,
  p_gateway FLOAT64,
  p_confirmation_a FLOAT64,
  p_confirmation_c FLOAT64,
  p_confirmation_e FLOAT64
)
RETURNS INT64
AS (
  CASE
    WHEN
      p_item = 1
      AND p_gateway = 1
      AND (
        p_confirmation_a = 1
        OR p_confirmation_c = 1
        OR p_confirmation_e = 1
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
    CAST(VP_ESCUELA AS INT64) AS reference_value
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

  COUNTIF(candidate.candidate_value = 1)
    AS candidate_positive_count,

  COUNTIF(candidate.candidate_value = 0)
    AS candidate_zero_count,

  COUNTIF(candidate.candidate_value IS NULL)
    AS candidate_null_count,

  COUNTIF(reference.reference_value = 1)
    AS reference_positive_count,

  COUNTIF(reference.reference_value = 0)
    AS reference_zero_count,

  COUNTIF(reference.reference_value IS NULL)
    AS reference_null_count

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
print(f"School item conditions: {len(form_calls)}")