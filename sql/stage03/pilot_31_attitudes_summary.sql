WITH versions AS (
  SELECT
    "V0" AS version,
    CAST(justifica_castigo_docente AS FLOAT64) AS indicator_value,
    CAST(FACTOR_ALUMNOS AS FLOAT64) AS weight
  FROM
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_adolescents`

  UNION ALL

  SELECT
    "V0.5" AS version,
    CAST(justifica_castigo_docente AS FLOAT64) AS indicator_value,
    CAST(FACTOR_ALUMNOS AS FLOAT64) AS weight
  FROM
    `enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_31_attitudes_v0_5`
)

SELECT
  version,
  COUNT(*) AS row_count,
  COUNTIF(indicator_value = 1) AS positive_count,
  COUNTIF(indicator_value = 0) AS zero_count,
  COUNTIF(indicator_value IS NULL) AS null_count,
  ROUND(
    100 * AVG(indicator_value),
    6
  ) AS unweighted_percent,

  ROUND(
    100 * SAFE_DIVIDE(
      SUM(IF(
        indicator_value IS NULL,
        NULL,
        weight * indicator_value
      )),
      SUM(IF(
        indicator_value IS NULL,
        NULL,
        weight
      ))
    ),
    6
  ) AS weighted_percent

FROM versions
GROUP BY version
ORDER BY version;