# Stage 03 Full Analytical Shadow Parity

- Result: PASS
- Date: 2026-08-23
- Status: SHADOW
- Engine: `v1_dataform`
- Branch: `test/stage03-cloud-full-validation`
- Location: US

## Scope

This checkpoint consolidates the cleaned shadow and all six migrated SPSS
methodology sections into one complete analytical candidate.

| Component | Columns |
|---|---:|
| Cleaned V0.5 | 1,206 |
| Structural `ID_AULA` | 1 |
| SPSS-derived sections 3.1–3.6 | 730 |
| **Full analytical candidate** | **1,937** |

All column names are unique. No cleaned column collides with a migrated
derived column.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_full_v0_5`

Table creation: PASS

Job ID:

`dataform-1a44f70c-c102-45d6-b5f6-893ccf4bab5d`

Bytes billed: 147.00 MiB.

## Dataform assertions

Full quality assertion: PASS

`enares2024_crs04_ops.stage03_full_shadow_quality`

Job IDs:

- `dataform-4ffc0c8c-e2e9-4c4a-83fc-2f9b3be9e507`
- `dataform-036e6087-0d62-43bd-9421-ddd9ef638a62`

The quality gate verifies:

- 18,807 rows;
- non-null respondent keys;
- no duplicate respondent-key groups;
- non-null `ID_AULA`; and
- exactly 1,937 physical table columns.

Full V0 parity assertion: PASS

`enares2024_crs04_ops.stage03_full_shadow_v0_parity`

Job IDs:

- `dataform-c33257d2-6e75-479f-a2c7-f8d491bd9685`
- `dataform-f77f501a-d3b9-45dd-bf21-850cb81e0a75`

Bytes billed by the comparison query: 290.00 MiB.

The parity gate normalizes the two intentional respondent-key type changes
from FLOAT to INTEGER and then compares the complete 1,937-column row as a
null-sensitive JSON structure. It returned zero violating rows.

## Local reproducibility gates

- Consolidation generator: PASS.
- Cleaned columns: 1,206/1,206.
- Derived columns: 730/730.
- Full columns: 1,937/1,937.
- Full Python test suite: 59 passed.
- Dataform graph: 40 actions compiled successfully.
- Python syntax compilation: PASS.
- Git whitespace validation: PASS.

## Conclusion

The consolidated Stage 03 V0.5 shadow is exactly equal to the official V0
analytical table for all 18,807 respondents and all 1,937 columns, after the
two approved key-type normalizations.

This checkpoint proves analytical row parity. Complex-survey tabulation
parity for all 516 specifications and 3,014 validated output rows is the next
closure gate.

The candidate remains SHADOW and does not replace the official V0 table.
