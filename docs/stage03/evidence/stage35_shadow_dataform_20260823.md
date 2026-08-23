# Stage 03 Section 3.5 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-23
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-35`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.5 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 8 |
| Derived columns | 40 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The eight blocks cover school locations and schedules, violence exercised by
students, school and household combinations, accumulation indices, physical
consequences, and health care following consequences.

The model consumes the validated section 3.2, 3.3, and 3.4 shadow tables
through the respondent key. It does not copy derived values from V0.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage35_v0_5`

Table creation: PASS

Job ID:

`dataform-19a3cc1d-8f6e-4ce4-b3cd-6114c9a9df02`

Bytes billed: 40.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage35_shadow_quality`

Job IDs:

- `dataform-f803d53f-1f67-49a9-b179-5b41a32cbd40`
- `dataform-019d95a0-aa22-44f4-bbb8-dd60e1d285e4`

The quality gate verifies row and key integrity, survey-design fields, binary
outputs, accumulation ranges of 0–4 and 0–5, and consequence counts of 0–6.
Methodological nulls remain permitted for consequence and health-care fields.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage35_shadow_v0_parity`

Job IDs:

- `dataform-d89f38b4-a5c4-42a9-814a-3c9cbcc4f094`
- `dataform-a1d69e76-03bc-4755-a92e-416423bd5c26`

The parity gate compares every one of the 40 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 8 blocks and 40 derived columns.
- Full Python test suite: 50 passed.
- Dataform graph: 34 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The section 3.5 Dataform shadow model reproduces the official V0 analytical
values exactly for all 40 derived columns and all 18,807 respondents.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
