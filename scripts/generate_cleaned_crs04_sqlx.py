from pathlib import Path

from google.cloud import bigquery


PROJECT = "enares-2024-crs04"
RAW_DATASET = "enares2024_crs04_raw"
OUTPUT = Path(
    "dataform/definitions/cleaned/"
    "cleaned_crs04_merged_adolescents_v0_5.sqlx"
)

TABLES = [
    ("raw_crs04_cap100", "cap100"),
    ("raw_crs04_cap200", "cap200"),
    ("raw_crs04_cap248", "cap248"),
    ("raw_crs04_cap300", "cap300"),
]

KEYS = {"ID", "COLEGIAL_ID"}


def quote(name: str) -> str:
    return f"`{name.replace('`', '``')}`"


client = bigquery.Client(project=PROJECT, location="US")

schemas = {
    table_name: client.get_table(
        f"{PROJECT}.{RAW_DATASET}.{table_name}"
    ).schema
    for table_name, _ in TABLES
}

selected_names = set()
select_expressions = []
collision_sources = {}

for table_name, alias in TABLES:
    for field in schemas[table_name]:
        normalized_name = field.name.upper()

        if normalized_name in selected_names:
            collision_sources.setdefault(field.name, []).append(table_name)
            continue

        selected_names.add(normalized_name)

        if alias == "cap100" and normalized_name in KEYS:
            expression = (
                f"  CAST({alias}.{quote(field.name)} AS INT64) "
                f"AS {quote(field.name)}"
            )
        else:
            expression = (
                f"  {alias}.{quote(field.name)} AS {quote(field.name)}"
            )

        select_expressions.append(expression)

if len(select_expressions) != 1206:
    raise RuntimeError(
        f"Expected 1206 output columns, found {len(select_expressions)}"
    )

config = """config {
  type: "table",
  schema: dataform.projectConfig.vars.cleanedDataset,
  name: "cleaned_crs04_merged_adolescents_v0_5",
  description: "Stage 03 V0.5 shadow merge; CAP100 is canonical for shared columns.",
  tags: ["stage03", "cleaned", "shadow", "v0_5"],
  dependencies: [
    "raw_key_values",
    "raw_key_unique",
    "raw_match_cap100",
    "raw_rowcount"
  ]
}
"""

query = f"""
SELECT
{",\n".join(select_expressions)}
FROM ${{ref("raw_crs04_cap100")}} AS cap100
LEFT JOIN ${{ref("raw_crs04_cap200")}} AS cap200
  USING (`ID`, `COLEGIAL_ID`)
LEFT JOIN ${{ref("raw_crs04_cap248")}} AS cap248
  USING (`ID`, `COLEGIAL_ID`)
LEFT JOIN ${{ref("raw_crs04_cap300")}} AS cap300
  USING (`ID`, `COLEGIAL_ID`)
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(config + query, encoding="utf-8")

print(f"Generated: {OUTPUT}")
print(f"Output columns: {len(select_expressions)}")
print(f"Suppressed duplicate occurrences: {sum(map(len, collision_sources.values()))}")