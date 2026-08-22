# Stage 03 Section 3.2 Cloud Shadow Batch

- Result: PASS
- Date: 2026-08-21
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `feat/stage03-cloud-batch-32`
- Location: US

## Scope

This batch migrates the complete ordered SPSS-authority transformation for
Stage 03 section 3.2 into a Dataform shadow model.

| Metric | Result |
|---|---:|
| SPSS transformation blocks | 6 |
| Derived columns | 50 |
| Candidate rows | 18,807 |
| Row-level differences against V0 | 0 |

The six ordered blocks cover 18 household-violence forms, four principal
prevalence indicators, four household combinations, one published overlap
alias, seven ICVAC groups, and sixteen aggressor groups.

The previously validated `VP_HOGAR` pilot is included inside this complete
section migration.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_stage32_v0_5`

Table creation: PASS

Job ID:

`dataform-af984e32-87cb-4901-abbf-189dcb93eae5`

Bytes billed: 10.00 MiB.

## Dataform assertions

Quality assertion: PASS

`enares2024_crs04_ops.stage32_shadow_quality`

Job IDs:

- `dataform-ebe8c89b-b7e7-4443-9849-9e5387c2241d`
- `dataform-82dfb3f4-b907-4b6e-bcc9-7b21588629b7`

The quality gate verifies the expected 18,807 rows, non-null and unique
respondent keys, valid survey-design fields, and binary non-null values for
all 50 outputs.

Exact V0 parity assertion: PASS

`enares2024_crs04_ops.stage32_shadow_v0_parity`

Job IDs:

- `dataform-a82dc8ab-9d9a-4e9e-b568-376e780d6462`
- `dataform-fe5b46bd-4465-4f32-a1e3-46720aa38878`

The parity gate compares every one of the 50 derived columns using the
respondent key and null-safe equality. The assertion returned zero violating
rows.

## Local reproducibility gates

- Generator output: 6 blocks and 50 derived columns.
- Full Python test suite: 35 passed.
- Dataform graph: 25 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The section 3.2 Dataform shadow model reproduces the official V0 analytical
values exactly for all 50 derived columns and all 18,807 respondents.

The candidate remains SHADOW. It does not replace or modify the official V0
analytical table.
