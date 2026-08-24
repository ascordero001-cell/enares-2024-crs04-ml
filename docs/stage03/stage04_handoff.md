# Stage 03 to Stage 04 Handoff — CRS04

- Candidate release: `stage03-v0.5-cloud-full`
- Current state: `AWAITING_STAGE04_ACCEPTANCE`
- Official publication state: V0 remains official

## Delivered contract

Stage 04 may consume
`enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5` only after the
closure-extension assertions pass. The table contains 18,807 rows and an
explicit 737-column projection:

- respondent key and design/context columns;
- `ID_AULA` for audit;
- 730 validated derived outputs covering blocks 3.1–3.6.

No Stage 04 process should reconstruct Stage 03 indicators from raw columns.

## Approved survey design

```r
svydesign(
  ids = ~ID,
  strata = ~CCDD,
  weights = ~FACTOR_ALUMNOS,
  nest = TRUE
)
```

This design reproduces the official CSPLAN: 25 strata, 1,115 PSUs and 1,090
degrees of freedom. `ID_AULA` is not a second-stage PSU in the validated
contract.

## Known exception

`VS_12M — Nacional — Total` follows the canonical full-population denominator
and is documented in `known_discrepancies.md`. It is not an unexplained error.

## Stage 04 acceptance checklist

- [ ] I reviewed `stage03_data_contract.md`;
- [ ] I confirmed that the closure-extension Dataform assertions passed;
- [ ] I understand that V0.5 is shadow and not a published estimate release;
- [ ] I will not upload respondent-level exports to GitHub;
- [ ] I accept the survey-input schema and validated design;
- [ ] I recorded my name, role, date and decision below.

## Acceptance record

- Reviewer: _pending_
- Role: _pending_
- Date: _pending_
- Decision: `PENDING`
- Notes: _pending_
