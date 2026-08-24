# Stage 03 Known Discrepancies — CRS04

## KD-001 — `VS_12M`, Nacional, Total

- Status: documented and methodologically resolved for V0.5 validation
- Scope: one of 3,014 comparison rows
- Candidate universe: all 18,807 adolescents

| Measure | Consolidated SPSS reference row | Validated R/V0.5 result |
|---|---:|---:|
| Percent | 100.0 | 19.168455 |
| Standard error | 0.0 | 0.628039 |
| CI low | 100.0 | 17.966095 |
| CI high | 100.0 | 20.431242 |
| CV | 0.0 | 0.032764 |
| Unweighted N | 3,429 | 18,807 |

### Classification

`UNIVERSE / DENOMINATOR — REFERENCE CONSOLIDATION CONFLICT`

The consolidated SPSS row restricts the analysis to positive cases and
therefore reports 100%. The canonical 3.4.1 syntax and the V0 tabulation use
the full adolescent denominator. The V0.5 candidate reproduces the canonical
rule and retains 3,429 positive cases over 18,807 adolescents.

### Gate treatment

This row is the single documented exception. The remaining 3,013 rows match
strictly and all 3,014 rows are validated. The exception must not be removed,
hidden by a larger tolerance or rewritten as a strict match.

### Evidence

- `docs/stage03/evidence/stage3_cloud_full_survey_comparison_20260823.csv`;
- `docs/stage03/evidence/stage3_cloud_full_survey_pass_20260823.md`;
- `docs/stage03/evidence/stage3_cloud_full_survey_closure_20260823.csv`.

## Open discrepancies

None. Any future difference requires a new entry and blocks promotion of the
affected component until reviewed.
