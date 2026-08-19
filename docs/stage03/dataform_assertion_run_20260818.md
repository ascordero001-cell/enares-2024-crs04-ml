# Stage 03 Dataform Assertion Run

Date: 2026-08-18  
Project: `enares-2024-crs04`  
Location: `US`  
Dataform CLI: `3.0.64`  
Authentication: Application Default Credentials  
Result: `PASS`

## Assertions

| Assertion | Result |
|---|---|
| `raw_key_unique` | PASS |
| `raw_key_values` | PASS |
| `raw_match_cap100` | PASS |
| `raw_rowcount` | PASS |

## Interpretation

The current CRS04 raw release contains 18,807 rows in each module.
`ID + COLEGIAL_ID` is complete, integer-valued, unique within each table and
fully matched between CAP100 and CAP200/CAP248/CAP300.

The assertions created validation views in
`enares2024_crs04_ops`. No raw table was modified.

## Execution identity

Git commit: `PASTE_GIT_COMMIT_HERE`

Dataform reported successful BigQuery job execution with approximately 40 MiB
processed for each key/match assertion and no assertion violations.