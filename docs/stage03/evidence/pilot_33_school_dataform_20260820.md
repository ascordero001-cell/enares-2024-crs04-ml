# Stage 03 Analytical Pilot 3.3 — School Violence

- Result: PASS
- Date: 2026-08-20
- Status: SHADOW
- Engine: `v1_dataform`
- Implementation commit: `9c0dcd73282b43b62e1c46cededbbc5f781a0bf8`
- Location: US

## Scope

Pilot indicator:

`VP_ESCUELA`

Gateway variable:

`C3P225`

Source items:

`C3P223_1` through `C3P223_14`

Each item also evaluates its corresponding confirmation fields:

- `C3P223A_*`
- `C3P223C_*`
- `C3P223E_*`

## SPSS semantic rule

Each form becomes one only when:

1. the corresponding `C3P223_*` item is 1;
2. gateway `C3P225` is 1; and
3. at least one corresponding confirmation field is 1.

Each form otherwise becomes zero. `VP_ESCUELA` becomes one when any
of the fourteen forms is one and zero otherwise.

Under this SPSS rule, closed, missing and nonmatching cases become zero.

## Preflight comparison

| Metric | Result |
|---|---:|
| Matched rows | 18,807 |
| Reference-only rows | 0 |
| Candidate-only rows | 0 |
| Rows with differences | 0 |
| Positive | 7,522 |
| Zero | 11,285 |
| NULL | 0 |

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_33_school_v0_5`

Creation job:

`dataform-10fff1ed-d00c-4fb9-b77c-0bf8cedf2e43`

## Dataform assertions

Quality assertion: PASS

`dataform-8ea2177c-3f66-4d4f-a457-31bfaab5f425`

Exact V0 parity assertion: PASS

`dataform-4d5960fb-b20d-43f2-bd0f-2008129d8b2d`

## V0–V0.5 point-estimate comparison

| Metric | V0 | V0.5 |
|---|---:|---:|
| Rows | 18,807 | 18,807 |
| Positive | 7,522 | 7,522 |
| Zero | 11,285 | 11,285 |
| NULL | 0 | 0 |
| Unweighted percent | 39.995746 | 39.995746 |
| Weighted point estimate | 40.207641 | 40.207641 |
| Row-level differences | 0 | 0 |

## Synthetic tests

Complete `pytest` result: 26 passed.

School-rule tests cover:

- confirmation through fields A, C and E;
- closed or missing item values;
- closed or missing gateway values;
- missing and nonmatching confirmation values;
- aggregation across exactly fourteen forms.

## Conclusion

The Dataform pilot reproduces the V0 `VP_ESCUELA` indicator exactly at
row level and reproduces its weighted and unweighted point estimates.

This PASS does not yet cover complex-survey standard errors or
confidence intervals. Those remain pending for the survey-input/R
validation stage.

The candidate remains SHADOW and does not replace the official V0
analytical table.