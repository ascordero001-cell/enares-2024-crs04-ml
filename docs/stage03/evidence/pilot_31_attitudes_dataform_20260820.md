# Stage 03 Analytical Pilot 3.1 — Attitudes

- Result: PASS
- Date: 2026-08-20
- Status: SHADOW
- Engine: `v1_dataform`
- Implementation commit: `24e237ff6f31427af9ab00e735feb2108f5e56aa`
- Location: US

## Scope

Pilot indicator:

`justifica_castigo_docente`

Source variable:

`C3P301_4`

SPSS rule:

```sql
CASE
  WHEN C3P301_4 = 1 THEN 1
  WHEN C3P301_4 = 2 THEN 0
END
```

Missing and unexpected source values remain `NULL`.

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_31_attitudes_v0_5`

Creation job:

`dataform-56246cae-f79b-4daa-84a9-6683e7fc4726`

## Dataform assertions

Quality assertion: PASS

`dataform-b1439a00-d59c-400d-83d5-cce3946173c3`

Exact V0 parity assertion: PASS

`dataform-1ace97b7-821f-4679-97e8-530989010772`

## V0–V0.5 comparison

| Metric | V0 | V0.5 |
|---|---:|---:|
| Rows | 18,807 | 18,807 |
| Positive | 1,161 | 1,161 |
| Zero | 17,466 | 17,466 |
| NULL | 180 | 180 |
| Unweighted percent | 6.232888 | 6.232888 |
| Weighted point estimate | 4.522469 | 4.522469 |
| Row-level differences | 0 | 0 |

## Conclusion

The Dataform pilot reproduces the V0 materialized indicator exactly,
including its `1/0/NULL` distribution and weighted point estimate.

This PASS covers row-level materialization and point estimates only.
Complex-survey standard errors and confidence intervals remain pending
for the survey-input/R validation stage.

The candidate remains SHADOW and does not replace the V0 analytical
table.