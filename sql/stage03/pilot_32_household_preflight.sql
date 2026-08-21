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
        household_form(SEXO, C3P201_1, C3P203, C3P201A_1, C3P201E_1, C3P201C_1, C3P201D_1, C3P201F_1) = 1
      OR household_form(SEXO, C3P201_2, C3P203, C3P201A_2, C3P201E_2, C3P201C_2, C3P201D_2, C3P201F_2) = 1
      OR household_form(SEXO, C3P201_3, C3P203, C3P201A_3, C3P201E_3, C3P201C_3, C3P201D_3, C3P201F_3) = 1
      OR household_form(SEXO, C3P201_4, C3P203, C3P201A_4, C3P201E_4, C3P201C_4, C3P201D_4, C3P201F_4) = 1
      OR household_form(SEXO, C3P201_5, C3P203, C3P201A_5, C3P201E_5, C3P201C_5, C3P201D_5, C3P201F_5) = 1
      OR household_form(SEXO, C3P201_6, C3P203, C3P201A_6, C3P201E_6, C3P201C_6, C3P201D_6, C3P201F_6) = 1
      OR household_form(SEXO, C3P201_7, C3P203, C3P201A_7, C3P201E_7, C3P201C_7, C3P201D_7, C3P201F_7) = 1
      OR household_form(SEXO, C3P201_8, C3P203, C3P201A_8, C3P201E_8, C3P201C_8, C3P201D_8, C3P201F_8) = 1
      OR household_form(SEXO, C3P201_9, C3P203, C3P201A_9, C3P201E_9, C3P201C_9, C3P201D_9, C3P201F_9) = 1
      OR household_form(SEXO, C3P201_10, C3P203, C3P201A_10, C3P201E_10, C3P201C_10, C3P201D_10, C3P201F_10) = 1
      OR household_form(SEXO, C3P201_11, C3P203, C3P201A_11, C3P201E_11, C3P201C_11, C3P201D_11, C3P201F_11) = 1
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
