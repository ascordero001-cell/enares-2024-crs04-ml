WITH all_rows AS (
  SELECT
    'raw_crs04_cap100' AS table_name,
    ID,
    COLEGIAL_ID
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap100`

  UNION ALL

  SELECT
    'raw_crs04_cap200',
    ID,
    COLEGIAL_ID
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap200`

  UNION ALL

  SELECT
    'raw_crs04_cap248',
    ID,
    COLEGIAL_ID
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap248`

  UNION ALL

  SELECT
    'raw_crs04_cap300',
    ID,
    COLEGIAL_ID
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap300`
),

row_metrics AS (
  SELECT
    table_name,
    COUNT(*) AS row_count,
    COUNTIF(ID IS NULL) AS id_nulls,
    COUNTIF(COLEGIAL_ID IS NULL) AS colegial_id_nulls,
    COUNTIF(ID != TRUNC(ID)) AS id_decimal_values,
    COUNTIF(COLEGIAL_ID != TRUNC(COLEGIAL_ID))
      AS colegial_id_decimal_values
  FROM all_rows
  GROUP BY table_name
),

duplicate_metrics AS (
  SELECT
    table_name,
    COUNTIF(key_count > 1) AS duplicate_key_groups,
    COALESCE(
      SUM(IF(key_count > 1, key_count - 1, 0)),
      0
    ) AS duplicate_excess_rows
  FROM (
    SELECT
      table_name,
      ID,
      COLEGIAL_ID,
      COUNT(*) AS key_count
    FROM all_rows
    WHERE ID IS NOT NULL
      AND COLEGIAL_ID IS NOT NULL
    GROUP BY table_name, ID, COLEGIAL_ID
  )
  GROUP BY table_name
)

SELECT
  row_metrics.*,
  duplicate_metrics.duplicate_key_groups,
  duplicate_metrics.duplicate_excess_rows
FROM row_metrics
JOIN duplicate_metrics USING (table_name)
ORDER BY table_name