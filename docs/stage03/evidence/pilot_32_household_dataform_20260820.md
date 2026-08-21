# Stage 03 Analytical Pilot 3.2 — Household Violence

- Result: PASS
- Date: 2026-08-20
- Status: SHADOW
- Engine: `v1_dataform`
- Implementation commit: `6e22a5676ed5a70333b43cacefc24c127ffd7819`
- Location: US

## Scope

Pilot indicator:

`VP_HOGAR`

Gateway variable:

`C3P203`

Source items:

`C3P201_1` through `C3P201_11`

The implementation also evaluates the corresponding perpetrator and
confirmation fields:

- `C3P201A_*`
- `C3P201E_*`
- `C3P201C_*`
- `C3P201D_*`
- `C3P201F_*`

## SPSS semantic rule

Each form becomes one only when:

1. `SEXO` is 1 or 2;
2. the corresponding `C3P201_*` item is 1;
3. gateway `C3P203` is 1; and
4. the perpetrator value is directly valid or satisfies its applicable
   confirmation fields.

Each form otherwise becomes zero. `VP_HOGAR` becomes one when any of
the eleven forms is one and zero otherwise.

This is an explicit SPSS rule where closed, missing or nonmatching
conditions become zero rather than remaining `NULL`.

## Preflight comparison

| Metric | Result |
|---|---:|
| Matched rows | 18,807 |
| Reference-only rows | 0 |
| Candidate-only rows | 0 |
| Rows with differences | 0 |
| Positive | 5,269 |
| Zero | 13,538 |
| NULL | 0 |

## Candidate table

`enares-2024-crs04.enares2024_crs04_analytical.analytical_crs04_pilot_32_household_v0_5`

Creation job:

`dataform-1bda73a0-a5c3-4e74-9fd1-106845f95ac4`

## Dataform assertions

Quality assertion: PASS

`dataform-8f78a33c-0cf9-4872-aca9-3b617304077f`

Exact V0 parity assertion: PASS

`dataform-1d19a576-dcd8-4cbb-941e-e439f446eece`

## V0–V0.5 point-estimate comparison

| Metric | V0 | V0.5 |
|---|---:|---:|
| Rows | 18,807 | 18,807 |
| Positive | 5,269 | 5,269 |
| Zero | 13,538 | 13,538 |
| NULL | 0 | 0 |
| Unweighted percent | 28.016164 | 28.016164 |
| Weighted point estimate | 28.481212 | 28.481212 |
| Row-level differences | 0 | 0 |

## Synthetic tests

`pytest` result: 18 passed.

Synthetic cases cover:

- direct perpetrator codes;
- confirmation requirements for nonstandard codes;
- closed gateways;
- invalid or missing sex;
- missing and nonmatching item values;
- aggregation across exactly eleven forms.

## Conclusion

The Dataform pilot reproduces the V0 `VP_HOGAR` indicator exactly at
row level and reproduces its weighted and unweighted point estimates.

This PASS does not yet cover complex-survey standard errors or
confidence intervals. Those remain pending for the survey-input/R
validation stage.

The candidate remains SHADOW and does not replace the official V0
analytical table.