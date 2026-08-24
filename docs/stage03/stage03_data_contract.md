# Stage 03 Data Contract — CRS04 V0.5

- Release: `stage03-v0.5-cloud-full`
- Status: technically validated shadow; not the published official version
- Project/location: `enares-2024-crs04` / `US`

## Layer contracts

| Layer | Object | Rows | Columns | Contract |
|---|---|---:|---:|---|
| raw | four `raw_crs04_cap*` tables | 18,807 each | source-defined | immutable Stage 02 inputs |
| cleaned | `cleaned_crs04_merged_adolescents_v0_5` | 18,807 | 1,206 | structural merge; no indicators |
| analytical | `analytical_crs04_full_v0_5` | 18,807 | 1,937 | cleaned + `ID_AULA` + 730 derived outputs |
| reporting | `reporting_crs04_survey_input_v0_5` | 18,807 | 737 | explicit design/context projection + 730 derived outputs |
| ops | `pipeline_runs` | one row per registered run | 11 | release/code/execution lineage |
| ops | `validation_results` | one row per gate | 6 | aggregate validation outcomes only |

## Keys and joins

- Respondent key: `ID + COLEGIAL_ID`.
- CAP100 is the base of every structural `LEFT JOIN`.
- The key is non-null and unique in every raw module.
- Cast from `FLOAT64` to `INT64` is allowed because the preflight found zero
  decimal values.

## Survey design

| Role | Column | Validated property |
|---|---|---|
| Stratum | `CCDD` | 25 distinct strata |
| PSU | `ID` | 1,115 distinct PSUs |
| Weight | `FACTOR_ALUMNOS` | non-null and positive |
| Audit classroom ID | `ID_AULA` | non-null; not used as a second PSU stage |

The validated design has 1,090 design degrees of freedom. `SEXO` and `AREA`
are retained as base disaggregations. The other approved dimensions are part
of the 730 derived outputs.

## Indicator contract

- 516 statistical specifications.
- Blocks 3.1–3.6 are represented by 730 derived analytical columns.
- Expected binary domains are `0/1/NULL` unless a contract explicitly defines
  a count, mean, category or continuous result.
- A valid skip becomes zero only when the SPSS rule and indicator universe
  explicitly require it.
- No reporting projection may use `SELECT *`.

## Security boundary

Respondent-level tables remain in BigQuery/Drive. Git contains SQLX, code,
contracts and authorized aggregate comparisons only. `ops` contains no
respondent rows.
