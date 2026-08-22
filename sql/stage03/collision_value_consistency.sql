DECLARE common_columns ARRAY<STRING>;
DECLARE common_struct_expression STRING;

SET common_columns = (
  SELECT ARRAY_AGG(column_name ORDER BY column_name)
  FROM (
    SELECT column_name
    FROM `enares-2024-crs04.enares2024_crs04_raw.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name IN (
      'raw_crs04_cap100',
      'raw_crs04_cap200',
      'raw_crs04_cap248',
      'raw_crs04_cap300'
    )
    GROUP BY column_name
    HAVING COUNT(DISTINCT table_name) = 4
  )
  WHERE column_name NOT IN ('ID', 'COLEGIAL_ID')
);

SET common_struct_expression = (
  SELECT STRING_AGG(
    FORMAT('`%s`', column_name),
    ', '
    ORDER BY column_name
  )
  FROM UNNEST(common_columns) AS column_name
);

EXECUTE IMMEDIATE FORMAT("""
WITH
base AS (
  SELECT
    ID,
    COLEGIAL_ID,
    TO_JSON_STRING(STRUCT(%s)) AS common_values
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap100`
),

cap200 AS (
  SELECT
    ID,
    COLEGIAL_ID,
    TO_JSON_STRING(STRUCT(%s)) AS common_values
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap200`
),

cap248 AS (
  SELECT
    ID,
    COLEGIAL_ID,
    TO_JSON_STRING(STRUCT(%s)) AS common_values
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap248`
),

cap300 AS (
  SELECT
    ID,
    COLEGIAL_ID,
    TO_JSON_STRING(STRUCT(%s)) AS common_values
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap300`
)

SELECT
  'raw_crs04_cap200' AS module_name,
  COUNT(*) AS matched_rows,
  COUNTIF(
    base.common_values IS DISTINCT FROM cap200.common_values
  ) AS rows_with_differences
FROM base
JOIN cap200 USING (ID, COLEGIAL_ID)

UNION ALL

SELECT
  'raw_crs04_cap248',
  COUNT(*),
  COUNTIF(
    base.common_values IS DISTINCT FROM cap248.common_values
  )
FROM base
JOIN cap248 USING (ID, COLEGIAL_ID)

UNION ALL

SELECT
  'raw_crs04_cap300',
  COUNT(*),
  COUNTIF(
    base.common_values IS DISTINCT FROM cap300.common_values
  )
FROM base
JOIN cap300 USING (ID, COLEGIAL_ID)

ORDER BY module_name
""",
  common_struct_expression,
  common_struct_expression,
  common_struct_expression,
  common_struct_expression
);