SELECT
  column_name,
  COUNT(DISTINCT table_name) AS table_count,
  ARRAY_AGG(
    DISTINCT table_name
    ORDER BY table_name
  ) AS tables
FROM `enares-2024-crs04.enares2024_crs04_raw.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN (
  'raw_crs04_cap100',
  'raw_crs04_cap200',
  'raw_crs04_cap248',
  'raw_crs04_cap300'
)
GROUP BY column_name
HAVING COUNT(DISTINCT table_name) > 1
ORDER BY table_count DESC, column_name