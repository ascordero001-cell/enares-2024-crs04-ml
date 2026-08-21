WITH
survey_input AS (
  SELECT
    attitudes.ID,
    attitudes.COLEGIAL_ID,
    attitudes.FACTOR_ALUMNOS,
    attitudes.CCDD,
    attitudes.SEXO,
    attitudes.AREA,
    attitudes.justifica_castigo_docente,
    household.VP_HOGAR,
    school.VP_ESCUELA

  FROM
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_31_attitudes_v0_5`
    AS attitudes

  LEFT JOIN
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_32_household_v0_5`
    AS household
    USING (ID, COLEGIAL_ID)

  LEFT JOIN
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_33_school_v0_5`
    AS school
    USING (ID, COLEGIAL_ID)
),

duplicate_keys AS (
  SELECT ID, COLEGIAL_ID
  FROM survey_input
  GROUP BY ID, COLEGIAL_ID
  HAVING COUNT(*) > 1
)

SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT ID) AS distinct_psu_count,
  COUNT(DISTINCT CCDD) AS distinct_stratum_count,

  COUNTIF(
    ID IS NULL OR COLEGIAL_ID IS NULL
  ) AS null_key_count,

  (SELECT COUNT(*) FROM duplicate_keys)
    AS duplicate_key_group_count,

  COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
  ) AS invalid_weight_count,

  COUNTIF(
    CCDD IS NULL OR TRIM(CCDD) = ""
  ) AS invalid_stratum_count,

  COUNTIF(
    justifica_castigo_docente IS NULL
  ) AS attitudes_null_count,

  COUNTIF(
    VP_HOGAR IS NULL
  ) AS household_null_count,

  COUNTIF(
    VP_ESCUELA IS NULL
  ) AS school_null_count,

  COUNTIF(
    justifica_castigo_docente NOT IN (0, 1)
  ) AS invalid_attitudes_domain_count,

  COUNTIF(
    VP_HOGAR NOT IN (0, 1)
  ) AS invalid_household_domain_count,

  COUNTIF(
    VP_ESCUELA NOT IN (0, 1)
  ) AS invalid_school_domain_count

FROM survey_input;