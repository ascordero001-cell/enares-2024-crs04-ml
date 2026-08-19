WITH base AS (
  SELECT ID, COLEGIAL_ID
  FROM `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap100`
),

module_names AS (
  SELECT 'raw_crs04_cap200' AS module_name
  UNION ALL
  SELECT 'raw_crs04_cap248'
  UNION ALL
  SELECT 'raw_crs04_cap300'
),

module_keys AS (
  SELECT
    'raw_crs04_cap200' AS module_name,
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

base_to_module AS (
  SELECT
    module_names.module_name,
    COUNT(*) AS cap100_rows,
    COUNTIF(module_keys.ID IS NOT NULL) AS matched_rows,
    COUNTIF(module_keys.ID IS NULL) AS cap100_without_module
  FROM module_names
  CROSS JOIN base
  LEFT JOIN module_keys
    ON module_keys.module_name = module_names.module_name
   AND module_keys.ID = base.ID
   AND module_keys.COLEGIAL_ID = base.COLEGIAL_ID
  GROUP BY module_names.module_name
),

module_to_base AS (
  SELECT
    module_keys.module_name,
    COUNTIF(base.ID IS NULL) AS module_without_cap100
  FROM module_keys
  LEFT JOIN base
    ON base.ID = module_keys.ID
   AND base.COLEGIAL_ID = module_keys.COLEGIAL_ID
  GROUP BY module_keys.module_name
)

SELECT
  base_to_module.*,
  module_to_base.module_without_cap100
FROM base_to_module
JOIN module_to_base USING (module_name)
ORDER BY module_name