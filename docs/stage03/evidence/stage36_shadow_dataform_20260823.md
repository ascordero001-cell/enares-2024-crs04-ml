# Stage 03 Section 3.6 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-23
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-36`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.6 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 4 |
| Derived columns | 94 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The four blocks cover household and school help-seeking components, derived
help gaps, sexual-violence help-seeking components, institutional support,
DEMUNA awareness and use, and sexual-violence help gaps.

The model consumes validated section 3.2, 3.3, and 3.4 shadow indicators
through the respondent key. It does not copy derived values from V0.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage36_v0_5`

Table creation: PASS

Job ID:

`dataform-b8c9447d-1e0a-439c-b6c0-754b6ef102e6`

Bytes billed: 40.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage36_shadow_quality`

Job IDs:

- `dataform-ce837ac5-e05e-4816-b88a-a02227715898`
- `dataform-27fe7bd4-23fa-4898-8fea-28ade5a727e0`

The quality gate verifies row and key integrity, survey-design fields, and
binary 0/1 domains for all defined output values. Methodological nulls outside
victim and help-seeking domains remain permitted.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage36_shadow_v0_parity`

Job IDs:

- `dataform-033371f5-84ed-4350-8616-e031db631dc9`
- `dataform-c964c01a-5f39-4d38-9d6e-97adb4bd0a88`

The parity gate compares every one of the 94 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 4 blocks and 94 derived columns.
- Full Python test suite: 55 passed.
- Dataform graph: 37 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Complete methodology coverage

The six migrated section batches now account for every SPSS-derived column
materialized by the authority notebook:

| Section | Derived columns |
|---|---:|
| 3.1 | 71 |
| 3.2 | 50 |
| 3.3 | 51 |
| 3.4 | 424 |
| 3.5 | 40 |
| 3.6 | 94 |
| **Total** | **730** |

## Conclusion

The section 3.6 Dataform shadow model reproduces the official V0 analytical
values exactly for all 94 derived columns and all 18,807 respondents. Together,
sections 3.1–3.6 cover all 730 SPSS-materialized columns.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
