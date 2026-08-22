# Stage 03 Section 3.1 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-21
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-31`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.1 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 10 |
| Derived columns | 71 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The ten ordered blocks cover factors and disaggregations, risk indicators,
attitude components and aggregates, rights recognition, household-task
components and aggregates, and myth components and aggregates.

The already validated pilot indicator `justifica_castigo_docente` is included
inside this complete section migration.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage31_v0_5`

Table creation: PASS

Job ID:

`dataform-feb279b0-f299-47fe-8be6-649e7f8cbdcf`

Bytes billed: 10.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage31_shadow_quality`

Job IDs:

- `dataform-d0322ff5-4a5f-4443-88e5-f5370b92857a`
- `dataform-b773e554-0d4f-4fbf-a147-8e51330f16a7`

The quality gate verifies the expected 18,807 rows, non-null and unique
respondent keys, and valid survey-design fields.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage31_shadow_v0_parity`

Job IDs:

- `dataform-3467c08c-aa31-40b4-8cb7-4dc3e10aff64`
- `dataform-f3bfbcec-d865-47c6-8fe7-84f6c3954bec`

The parity gate compares every one of the 71 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 10 blocks and 71 derived columns.
- Full Python test suite: 30 passed.
- Dataform graph: 22 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The section 3.1 Dataform shadow model reproduces the official V0 analytical
values exactly for all 71 derived columns and all 18,807 respondents.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
