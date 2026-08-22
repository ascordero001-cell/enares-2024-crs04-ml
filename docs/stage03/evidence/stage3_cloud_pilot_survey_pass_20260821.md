# Stage 03 cloud pilot — complex-survey validation

Resultado: PASS

Fecha UTC: 2026-08-21T21:49:42.365083+00:00

## Scope

Shadow validation of three migrated CRS04 indicators:

- `justifica_castigo_docente`
- `VP_HOGAR`
- `VP_ESCUELA`

The official V0 analytical data and outputs were not overwritten.

## Hybrid validation input

- Rows: 18,807
- Columns: 1,937
- Matched composite keys: 18,807/18,807
- V0-only rows: 0
- V0.5-only rows: 0
- Replaced columns: 3
- Export SHA-256: `3d3952513dfddd732236eede956f95b4392fbfb40041e9528e25753ef0a15ea9`

All non-migrated analytical, domain and disaggregation columns remained from V0.
Only the three indicator columns were replaced with values from:

`enares-2024-crs04.enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5`

## Complex-survey design

- Rows: 18,807
- Strata: 25
- PSUs: 1,115
- Design degrees of freedom: 1,090
- PSU: `ID`
- Stratum: `CCDD`
- Weight: `FACTOR_ALUMNOS`
- Lonely PSU option: `remove`

## Pilot comparison

- Expected aggregate rows: 160
- Compared rows: 160
- Strictly equal rows: 160
- Validated rows: 160
- Documented exceptions affecting pilot: 0
- Statistical differences: 0

Breakdown:

- `VP_HOGAR`: 64/64
- `VP_ESCUELA`: 48/48
- `justifica_castigo_docente`: 48/48

Statistics compared:

- Weighted percentage
- Standard error
- Confidence interval lower bound
- Confidence interval upper bound
- Coefficient of variation
- Unweighted count

## Full-regression context

The complete 516-indicator regression produced 3,014 validated rows.
There were 3,013 strict matches and one previously documented SPSS-reference
exception for `VS_12M — Nacional`. That exception is unrelated to the three
migrated pilot indicators. There were zero unvalidated statistical rows.

The copied full-closure notebook reported `artifacts_complete=False` because
the isolated shadow folder intentionally does not duplicate all upstream V0
documentation artifacts. This does not alter the pilot statistical result.

## Artifact hashes

- Hybrid analytical export: `3d3952513dfddd732236eede956f95b4392fbfb40041e9528e25753ef0a15ea9`
- Pilot V0 reference: `5b3a5eb44b34e32072e1da9fc5eb5d52498831a06fa0501e72e239b352ecb3f4`
- Pilot comparison: `147d405fb50ac6bbcb7873c467a18b0e4edc8fd79f66269bad4a4890bdbf2c95`
- Shadow R tabulation output: `15b845da4a886fdcf54a96d8b8471b6f6be618ae18b43024488c6bd6b23d0bb4`
- Shadow survey design: `c9c7d96f053be17606c9bdced365ecc5e0016ff0294958e378cc62c747f46965`

## Decision

The three-indicator complex-survey shadow pilot passes the methodological gate.

This PASS authorizes continued shadow migration work. It does not promote V0.5
to production and does not modify the official V0 baseline.
