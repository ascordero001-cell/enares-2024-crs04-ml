WITH candidate AS (
  SELECT
    ID,
    COLEGIAL_ID,
    CASE
      WHEN C3P301_4 = 1 THEN 1
      WHEN C3P301_4 = 2 THEN 0
    END AS candidate_value
  FROM
    `enares-2024-crs04.enares2024_crs04_cleaned.cleaned_crs04_merged_adolescents_v0_5`
),

reference AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
    CAST(justifica_castigo_docente AS INT64) AS reference_value
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

  COUNTIF(candidate.candidate_value = 1) AS candidate_ones,
  COUNTIF(candidate.candidate_value = 0) AS candidate_zeros,
  COUNTIF(candidate.candidate_value IS NULL) AS candidate_nulls,

  COUNTIF(reference.reference_value = 1) AS reference_ones,
  COUNTIF(reference.reference_value = 0) AS reference_zeros,
  COUNTIF(reference.reference_value IS NULL) AS reference_nulls

FROM candidate
FULL OUTER JOIN reference
  USING (ID, COLEGIAL_ID);