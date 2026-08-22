# Stage 03 Section 3.3 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-21
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-33`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.3 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 3 |
| Derived columns | 51 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The three ordered blocks cover 24 school-violence forms, nine principal
prevalence and ICVAC indicators, and eighteen aggressor groups.

The previously validated `VP_ESCUELA` pilot is included inside this complete
section migration.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage33_v0_5`

Table creation: PASS

Job ID:

`dataform-57e5b1ca-f7a2-452a-9f63-6663d5f305cc`

Bytes billed: 10.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage33_shadow_quality`

Job IDs:

- `dataform-e9e6942a-9a8a-4806-b2d3-9e0629c26aa7`
- `dataform-a4e43555-c265-4e22-87e2-74ab9ccee259`

The quality gate verifies the expected 18,807 rows, non-null and unique
respondent keys, valid survey-design fields, and binary non-null values for
all 51 outputs.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage33_shadow_v0_parity`

Job IDs:

- `dataform-76c11f37-da80-4562-94ea-9159e42fe95c`
- `dataform-29368ba6-4a09-4626-9b53-e530915b48bb`

The parity gate compares every one of the 51 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 3 blocks and 51 derived columns.
- Full Python test suite: 40 passed.
- Dataform graph: 28 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The section 3.3 Dataform shadow model reproduces the official V0 analytical
values exactly for all 51 derived columns and all 18,807 respondents.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
