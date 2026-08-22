# Stage 03 Cleaned V0–V0.5 Validation

- Result: PASS
- Date: 2026-08-19
- Location: US
- Engine: `v1_dataform`
- Status: SHADOW
- Git commit: `06eaf77dfd9ddfc22e9429839889cc075a0e6b30`
- Dataform version: `3.0.64`

## Candidate creation

Table:

`enares-2024-crs04.enares2024_crs04_cleaned.cleaned_crs04_merged_adolescents_v0_5`

Creation job:

`dataform-f8a1d53c-9f36-4128-a24c-41f75960e783`

Bytes billed: 47 MiB.

## Dataform assertions

All six assertions passed:

- `raw_key_unique`
- `raw_key_values`
- `raw_match_cap100`
- `raw_rowcount`
- `cleaned_shadow_key_integrity`
- `cleaned_shadow_rowcount`

Cleaned assertion jobs:

- Key integrity: `dataform-cae115ad-9a1c-484a-8a10-3712b6d8e5fc`
- Row count: `dataform-e546c333-219a-4d3f-b5ff-d1b50a083010`

## V0–V0.5 regression

| Check | Result |
|---|---:|
| V0 rows | 18,807 |
| V0.5 rows | 18,807 |
| V0 columns | 1,206 |
| V0.5 columns | 1,206 |
| Matched rows | 18,807 |
| V0-only rows | 0 |
| V0.5-only rows | 0 |
| Rows with value differences | 0 |

The only schema differences are approved:

- `ID`: `FLOAT` → `INTEGER`
- `COLEGIAL_ID`: `FLOAT` → `INTEGER`

## Conclusion

V0.5 reproduces every V0 cleaned value after normalization of the two
validated key columns. The V0 table remained unchanged. The candidate
passes the technical shadow gate but is not yet promoted.