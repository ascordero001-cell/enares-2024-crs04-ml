WITH candidate_keys AS (
  SELECT
    cap100.ID,
    cap100.COLEGIAL_ID
  FROM
    `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap100` AS cap100
  LEFT JOIN
    `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap200` AS cap200
    USING (ID, COLEGIAL_ID)
  LEFT JOIN
    `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap248` AS cap248
    USING (ID, COLEGIAL_ID)
  LEFT JOIN
    `enares-2024-crs04.enares2024_crs04_raw.raw_crs04_cap300` AS cap300
    USING (ID, COLEGIAL_ID)
),

duplicate_keys AS (
  SELECT ID, COLEGIAL_ID
  FROM candidate_keys
  GROUP BY ID, COLEGIAL_ID
  HAVING COUNT(*) > 1
)

SELECT
  (SELECT COUNT(*) FROM candidate_keys) AS candidate_rows,
  (
    SELECT COUNT(*)
    FROM candidate_keys
    WHERE ID IS NULL OR COLEGIAL_ID IS NULL
  ) AS null_key_rows,
  (SELECT COUNT(*) FROM duplicate_keys) AS duplicate_key_groups;