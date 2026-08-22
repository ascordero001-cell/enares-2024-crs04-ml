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
        school_form(C3P223_1, C3P225, C3P223A_1, C3P223C_1, C3P223E_1) = 1
      OR school_form(C3P223_2, C3P225, C3P223A_2, C3P223C_2, C3P223E_2) = 1
      OR school_form(C3P223_3, C3P225, C3P223A_3, C3P223C_3, C3P223E_3) = 1
      OR school_form(C3P223_4, C3P225, C3P223A_4, C3P223C_4, C3P223E_4) = 1
      OR school_form(C3P223_5, C3P225, C3P223A_5, C3P223C_5, C3P223E_5) = 1
      OR school_form(C3P223_6, C3P225, C3P223A_6, C3P223C_6, C3P223E_6) = 1
      OR school_form(C3P223_7, C3P225, C3P223A_7, C3P223C_7, C3P223E_7) = 1
      OR school_form(C3P223_8, C3P225, C3P223A_8, C3P223C_8, C3P223E_8) = 1
      OR school_form(C3P223_9, C3P225, C3P223A_9, C3P223C_9, C3P223E_9) = 1
      OR school_form(C3P223_10, C3P225, C3P223A_10, C3P223C_10, C3P223E_10) = 1
      OR school_form(C3P223_11, C3P225, C3P223A_11, C3P223C_11, C3P223E_11) = 1
      OR school_form(C3P223_12, C3P225, C3P223A_12, C3P223C_12, C3P223E_12) = 1
      OR school_form(C3P223_13, C3P225, C3P223A_13, C3P223C_13, C3P223E_13) = 1
      OR school_form(C3P223_14, C3P225, C3P223A_14, C3P223C_14, C3P223E_14) = 1
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
