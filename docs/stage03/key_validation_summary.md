# Stage 03 Key Validation Summary

Date: 2026-08-18  
Project: `enares-2024-crs04`  
Dataset: `enares2024_crs04_raw`  
Candidate key: `ID + COLEGIAL_ID`  
Technical result: `PASS`

## Schema

Both key columns are stored as `FLOAT64` and are nullable in the BigQuery
schema in all four raw tables.

No cast was performed before validating their actual values.

## Key-quality results

| Table | Rows | ID nulls | COLEGIAL_ID nulls | ID decimals | COLEGIAL_ID decimals | Duplicate groups | Excess rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| raw_crs04_cap100 | 18807 | 0 | 0 | 0 | 0 | 0 | 0 |
| raw_crs04_cap200 | 18807 | 0 | 0 | 0 | 0 | 0 | 0 |
| raw_crs04_cap248 | 18807 | 0 | 0 | 0 | 0 | 0 | 0 |
| raw_crs04_cap300 | 18807 | 0 | 0 | 0 | 0 | 0 | 0 |

## Match results against CAP100

| Module | CAP100 rows | Matched | CAP100 without module | Module without CAP100 |
|---|---:|---:|---:|---:|
| raw_crs04_cap200 | 18807 | 18807 | 0 | 0 |
| raw_crs04_cap248 | 18807 | 18807 | 0 | 0 |
| raw_crs04_cap300 | 18807 | 18807 | 0 | 0 |

## Decision

`ID + COLEGIAL_ID` is technically validated as a one-to-one merge key for
the current CRS04 raw release.

Because all observed values are integer-valued, conversion from `FLOAT64` to
`INT64` may be performed in the cleaned layer using an explicit cast. The raw
tables remain unchanged.

CAP100 remains the required base for the Stage 03 `LEFT JOIN`.

## Reproducible queries

- `sql/stage03/key_validation_summary.sql`
- `sql/stage03/merge_match_diagnostics.sql`

Methodological/supervisor approval remains separate from this technical PASS.