from google.cloud import bigquery


PROJECT = "enares-2024-crs04"
DATASET = "enares2024_crs04_cleaned"
V0_NAME = "cleaned_crs04_merged_adolescents"
V05_NAME = "cleaned_crs04_merged_adolescents_v0_5"

client = bigquery.Client(project=PROJECT, location="US")

v0 = client.get_table(f"{PROJECT}.{DATASET}.{V0_NAME}")
v05 = client.get_table(f"{PROJECT}.{DATASET}.{V05_NAME}")

v0_fields = {field.name: field.field_type for field in v0.schema}
v05_fields = {field.name: field.field_type for field in v05.schema}

if list(v0_fields) != list(v05_fields):
    raise RuntimeError("V0 and V0.5 column names/order do not match")

type_differences = {
    name: (v0_fields[name], v05_fields[name])
    for name in v0_fields
    if v0_fields[name] != v05_fields[name]
}

expected_type_differences = {
    "ID": ("FLOAT", "INTEGER"),
    "COLEGIAL_ID": ("FLOAT", "INTEGER"),
}

if type_differences != expected_type_differences:
    raise RuntimeError(
        f"Unexpected schema differences: {type_differences}"
    )

def quote(name: str) -> str:
    return f"`{name.replace('`', '``')}`"


v0_struct = []
v05_struct = []

for name in v0_fields:
    if name in {"ID", "COLEGIAL_ID"}:
        v0_struct.append(
            f"CAST(v0.{quote(name)} AS INT64) AS {quote(name)}"
        )
    else:
        v0_struct.append(f"v0.{quote(name)} AS {quote(name)}")

    v05_struct.append(f"v05.{quote(name)} AS {quote(name)}")

query = f"""
WITH
v0_normalized AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
    FARM_FINGERPRINT(
      TO_JSON_STRING(STRUCT({", ".join(v0_struct)}))
    ) AS row_hash
  FROM `{PROJECT}.{DATASET}.{V0_NAME}` AS v0
),
v05_normalized AS (
  SELECT
    ID,
    COLEGIAL_ID,
    FARM_FINGERPRINT(
      TO_JSON_STRING(STRUCT({", ".join(v05_struct)}))
    ) AS row_hash
  FROM `{PROJECT}.{DATASET}.{V05_NAME}` AS v05
)
SELECT
  COUNTIF(
    v0_normalized.ID IS NOT NULL
    AND v05_normalized.ID IS NOT NULL
  ) AS matched_rows,
  COUNTIF(v05_normalized.ID IS NULL) AS v0_only_rows,
  COUNTIF(v0_normalized.ID IS NULL) AS v0_5_only_rows,
  COUNTIF(
    v0_normalized.ID IS NOT NULL
    AND v05_normalized.ID IS NOT NULL
    AND v0_normalized.row_hash IS DISTINCT FROM v05_normalized.row_hash
  ) AS rows_with_value_differences
FROM v0_normalized
FULL OUTER JOIN v05_normalized
  USING (ID, COLEGIAL_ID)
"""

result = dict(next(iter(client.query(query).result())))

print(f"V0 rows: {v0.num_rows}")
print(f"V0.5 rows: {v05.num_rows}")
print(f"V0 columns: {len(v0.schema)}")
print(f"V0.5 columns: {len(v05.schema)}")
print(f"Expected type differences: {type_differences}")
print(result)