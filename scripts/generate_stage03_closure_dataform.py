"""Generate the final Stage 03 survey contract and operational lineage tables."""

from __future__ import annotations

from pathlib import Path

try:
    from scripts.generate_stage03_full_validation_dataform import derived_columns
except ModuleNotFoundError:
    from generate_stage03_full_validation_dataform import derived_columns


REPORTING_OUTPUT = Path(
    "dataform/definitions/reporting/reporting_crs04_survey_input_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/survey_input_full_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/survey_input_full_v0_parity.sqlx"
)
PIPELINE_RUNS_OUTPUT = Path("dataform/definitions/ops/pipeline_runs.sqlx")
VALIDATION_RESULTS_OUTPUT = Path(
    "dataform/definitions/ops/validation_results.sqlx"
)

EXPECTED_ROWS = 18_807
EXPECTED_SURVEY_COLUMNS = 737
RELEASE_ID = "stage03-v0.5-cloud-full"
ANALYTICAL_RELEASE_GIT_COMMIT_SHA = (
    "3885fcd344d4d21a7311ca49e3d11f5c0509905f"
)
SOURCE_HASH = "c9fb351f5dc1b09d7776dc8dedd65ad7471e4fc1fba5d2648daf58f4eba03d33"
EVIDENCE_BUNDLE_HASH = (
    "c9923719962cf2cdd172db33770bc4a1f56ee5305d15acb42a99417661edfda9"
)

SURVEY_CONTEXT_COLUMNS = [
    "ID",
    "COLEGIAL_ID",
    "CCDD",
    "ID_AULA",
    "FACTOR_ALUMNOS",
    "SEXO",
    "AREA",
]


def survey_columns() -> list[str]:
    columns = SURVEY_CONTEXT_COLUMNS + derived_columns()
    if len(columns) != EXPECTED_SURVEY_COLUMNS:
        raise ValueError(
            f"Expected {EXPECTED_SURVEY_COLUMNS} survey columns, found {len(columns)}"
        )
    if len(columns) != len(set(columns)):
        raise ValueError("Survey contract contains duplicate columns")
    return columns


def projection(alias: str) -> str:
    return ",\n".join(f"  {alias}.`{column}`" for column in survey_columns())


def render_reporting_model() -> str:
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.outputsDataset,
  name: "reporting_crs04_survey_input_v0_5",
  description: "Complete Stage 03 V0.5 survey input contract: design, approved disaggregations and 730 derived outputs.",
  tags: ["stage03", "reporting", "survey_input", "full", "shadow"]
}}

SELECT
{projection("analytical")}
FROM ${{ref("analytical_crs04_full_v0_5")}} AS analytical
'''


def render_quality_assertion() -> str:
    return f'''config {{
  type: "assertion",
  schema: dataform.projectConfig.vars.opsDataset,
  tags: ["stage03", "reporting", "survey_input", "full", "quality"]
}}

WITH
candidate AS (
  SELECT * FROM ${{ref("reporting_crs04_survey_input_v0_5")}}
),
duplicate_keys AS (
  SELECT ID, COLEGIAL_ID FROM candidate
  GROUP BY ID, COLEGIAL_ID HAVING COUNT(*) > 1
),
schema_count AS (
  SELECT COUNT(*) AS column_count
  FROM `enares-2024-crs04.enares2024_crs04_outputs.INFORMATION_SCHEMA.COLUMNS`
  WHERE table_name = "reporting_crs04_survey_input_v0_5"
),
checks AS (
  SELECT "row_count" AS check_name, ABS(COUNT(*) - {EXPECTED_ROWS}) AS violation_count
  FROM candidate HAVING COUNT(*) != {EXPECTED_ROWS}
  UNION ALL
  SELECT "null_keys", COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0
  UNION ALL
  SELECT "duplicate_key_groups", COUNT(*) FROM duplicate_keys HAVING COUNT(*) > 0
  UNION ALL
  SELECT "invalid_design", COUNTIF(
    CCDD IS NULL OR ID IS NULL OR ID_AULA IS NULL
    OR FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0)
  FROM candidate HAVING COUNTIF(
    CCDD IS NULL OR ID IS NULL OR ID_AULA IS NULL
    OR FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0) > 0
  UNION ALL
  SELECT "schema_column_count", ABS(column_count - {EXPECTED_SURVEY_COLUMNS})
  FROM schema_count WHERE column_count != {EXPECTED_SURVEY_COLUMNS}
)
SELECT * FROM checks
'''


def render_parity_assertion() -> str:
    reference_projection = projection("reference_source")
    return f'''config {{
  type: "assertion",
  schema: dataform.projectConfig.vars.opsDataset,
  tags: ["stage03", "reporting", "survey_input", "full", "parity"]
}}

WITH
reference AS (
  SELECT
{reference_projection}
  FROM ${{ref("analytical_crs04_full_v0_5")}} AS reference_source
),
candidate AS (
  SELECT * FROM ${{ref("reporting_crs04_survey_input_v0_5")}}
),
differences AS (
  (SELECT * FROM reference EXCEPT DISTINCT SELECT * FROM candidate)
  UNION ALL
  (SELECT * FROM candidate EXCEPT DISTINCT SELECT * FROM reference)
)
SELECT * FROM differences
'''


def render_pipeline_runs() -> str:
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.opsDataset,
  name: "pipeline_runs",
  description: "Stage 03 release-to-code lineage. Operational metadata only; no microdata.",
  tags: ["stage03", "ops", "lineage", "release"]
}}

SELECT
  "${{dataform.projectConfig.vars.runId}}" AS run_id,
  "{RELEASE_ID}" AS release_id,
  "{SOURCE_HASH}" AS source_hash,
  "${{dataform.projectConfig.vars.gitCommitSha}}" AS git_commit_sha,
  "{ANALYTICAL_RELEASE_GIT_COMMIT_SHA}" AS analytical_release_git_commit_sha,
  "3.0.64" AS dataform_release,
  TIMESTAMP("2026-08-23T23:33:18.972083Z") AS execution_started_at,
  TIMESTAMP("2026-08-24T02:19:33Z") AS execution_finished_at,
  "PASS_CON_EXCEPCION_DOCUMENTADA" AS validation_status,
  "shadow" AS promotion_status,
  "{EVIDENCE_BUNDLE_HASH}" AS evidence_bundle_sha256
'''


def render_validation_results() -> str:
    rows = [
        (
            "raw_key_integrity",
            "PASS",
            "0 duplicate groups; 0 decimal keys; 0 unmatched rows",
            "docs/stage03/key_validation_summary.md",
        ),
        (
            "cleaned_v0_v0_5_parity",
            "PASS",
            "18807 rows; 1206 columns; 0 value differences",
            "docs/stage03/evidence/cleaned_v0_v0_5_validation_20260819.md",
        ),
        (
            "analytical_full_row_parity",
            "PASS",
            "18807 rows; 1937 columns; 0 value differences",
            "docs/stage03/evidence/stage03_full_row_parity_20260823.md",
        ),
        (
            "complex_survey_full_parity",
            "PASS_CON_EXCEPCION_DOCUMENTADA",
            "3014 validated; 3013 strict; 1 documented VS_12M exception",
            "docs/stage03/evidence/stage3_cloud_full_survey_pass_20260823.md",
        ),
        (
            "github_actions_ci",
            "PASS",
            "Python tests and Dataform compile gates green",
            "docs/stage03/evidence/ci_run_73_20260820.md",
        ),
    ]
    selects = []
    for validation_name, status, observed_result, evidence_path in rows:
        selects.append(
            "SELECT\n"
            '  "${dataform.projectConfig.vars.runId}" AS run_id,\n'
            f'  "{RELEASE_ID}" AS release_id,\n'
            f'  "{validation_name}" AS validation_name,\n'
            f'  "{status}" AS validation_status,\n'
            f'  "{observed_result}" AS observed_result,\n'
            f'  "{evidence_path}" AS evidence_path'
        )
    return '''config {
  type: "table",
  schema: dataform.projectConfig.vars.opsDataset,
  name: "validation_results",
  description: "Stage 03 aggregate validation registry. Contains no respondent records.",
  tags: ["stage03", "ops", "validation", "release"]
}

''' + "\nUNION ALL\n".join(selects) + "\n"


def write_outputs() -> None:
    outputs = {
        REPORTING_OUTPUT: render_reporting_model(),
        QUALITY_OUTPUT: render_quality_assertion(),
        PARITY_OUTPUT: render_parity_assertion(),
        PIPELINE_RUNS_OUTPUT: render_pipeline_runs(),
        VALIDATION_RESULTS_OUTPUT: render_validation_results(),
    }
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Generated: {path}")
    print(f"Survey columns: {len(survey_columns())}")


if __name__ == "__main__":
    write_outputs()
