# Stage 03 Survey-Input Pilot — Dataform Evidence

- Result: PASS
- Date: 2026-08-20
- Status: SHADOW
- Engine: `v1_dataform`
- Implementation commit: `741eb72c118107bad267373824361cff0f1f0a05`
- Location: US

## Candidate table

`enares-2024-crs04.enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5`

Creation job:

`dataform-9a81b5a6-7cd7-4e4b-a808-77382abfa72b`

Bytes billed: 30 MiB.

## Explicit columns

Design and identity fields:

- `ID`
- `COLEGIAL_ID`
- `FACTOR_ALUMNOS`
- `CCDD`
- `SEXO`
- `AREA`

Approved pilot indicators:

- `justifica_castigo_docente`
- `VP_HOGAR`
- `VP_ESCUELA`

## Structural validation

| Check | Result |
|---|---:|
| Rows | 18,807 |
| Distinct PSUs | 1,115 |
| Distinct strata | 25 |
| Null keys | 0 |
| Duplicate key groups | 0 |
| Invalid or missing weights | 0 |
| Invalid or missing strata | 0 |
| Attitudes NULL values | 180 |
| Household NULL values | 0 |
| School NULL values | 0 |
| Invalid indicator values | 0 |

The 180 attitude NULL values are expected and reproduce V0 semantics.

## Dataform assertions

Survey-input quality assertion: PASS

`dataform-19f343b2-50d1-4b80-9f9a-e5dd6556d4f7`

Full V0 parity assertion: PASS

`dataform-72227b0c-db1e-4279-8ce8-48c705ece7da`

All upstream raw, cleaned and analytical assertions also passed.

## Conclusion

The survey-input shadow preserves the approved universe, design fields,
weights and three pilot indicators exactly.

This PASS establishes technical readiness for complex-survey validation.
It does not yet approve standard errors, confidence intervals or final
publication.

The candidate remains SHADOW and does not replace an official V0
reporting table.