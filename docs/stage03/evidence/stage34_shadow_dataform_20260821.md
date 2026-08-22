# Stage 03 Section 3.4 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-21
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-34`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.4 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 7 |
| Derived columns | 424 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The seven ordered blocks cover 80 sexual-violence form and context columns,
six principal indicators, 78 ICVAC and CP groups, two contact indicators,
18 aggressor groups, three women-domain indicators, and 237 published aliases.

Published household and school aggressor aliases consume the validated
section 3.2 and 3.3 shadow tables through the respondent key. They do not copy
derived values from the official V0 table.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage34_v0_5`

Table creation: PASS

Job ID:

`dataform-8c174cda-4c83-4615-8608-23aeaf6c1917`

Bytes billed: 30.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage34_shadow_quality`

Job IDs:

- `dataform-9e86101c-2bcb-4a62-bb28-706b7a6c4813`
- `dataform-20227e7f-a74c-4186-9bf4-1e8f9cf5f1dd`

The quality gate verifies the expected 18,807 rows, non-null and unique
respondent keys, valid survey-design fields, and binary non-null values for
all 424 outputs.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage34_shadow_v0_parity`

Job IDs:

- `dataform-57e49905-53bc-4a89-a0c2-48fa583baed8`
- `dataform-580ab7cd-c723-491b-b967-05ad22396b81`

The parity gate compares every one of the 424 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 7 blocks and 424 derived columns.
- Full Python test suite: 45 passed.
- Dataform graph: 31 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The section 3.4 Dataform shadow model reproduces the official V0 analytical
values exactly for all 424 derived columns and all 18,807 respondents.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
