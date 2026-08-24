# Stage 03 Migration Decisions — CRS04

- Transition: V0 to V0.5 cloud shadow
- Technical release: `stage03-v0.5-cloud-full`
- Release commit: `3885fcd344d4d21a7311ca49e3d11f5c0509905f`

## Decisions

| ID | Decision | Reason | Status |
|---|---|---|---|
| MD-01 | Preserve V0 and tag it as `stage03-v0-baseline` | V0 is the functional and methodological oracle | Applied |
| MD-02 | Use `ID + COLEGIAL_ID` as the respondent key | Missing, decimal, duplicate and match checks passed | Applied |
| MD-03 | Use CAP100 as the `LEFT JOIN` base | Prevent loss of adolescents | Applied |
| MD-04 | Cast key values only after proving they are integral | Raw keys arrived as `FLOAT64` | Applied |
| MD-05 | Keep `cleaned` structural and create indicators only in `analytical` | Preserve layer responsibilities | Applied |
| MD-06 | Resolve the 31 shared-column collisions from CAP100 | Values were identical across all 18,807 matched rows | Applied |
| MD-07 | Treat SPSS syntax and frozen V0 contracts as the rule authority | Prevent silent changes to universes and denominators | Applied |
| MD-08 | Preserve `NULL`, skip, nonresponse and zero as distinct states | They have different methodological meanings | Applied |
| MD-09 | Map historical source names `3.7` to official block `3.6 búsqueda de ayuda` without renaming source files | Preserve traceability and official numbering | Applied |
| MD-10 | Use the validated one-stage survey design: `CCDD` strata, `ID` PSU and `FACTOR_ALUMNOS` weight | This reproduces the official CSPLAN with 25 strata, 1,115 PSUs and 1,090 df | Applied |
| MD-11 | Retain `ID_AULA` in the reporting contract for audit, but do not add it as a second PSU stage | A two-stage design is not supported by the validated SPSS parity evidence | Applied |
| MD-12 | Keep V0.5 in shadow after full parity | Publication and Stage 04 acceptance require a separate human decision | Active |

## GitHub issue-number reconciliation

The planning document refers to proposed Stage 03 Issues #12–#18 and #23.
Those numbers were already occupied by earlier repository work. The actual
Stage 03 umbrella issues are:

- #22 — Stage 03 validation and setup;
- #23 — core transformation;
- #24 — statistical validation and release.

PRs #25–#33 contain the implemented Stage 03 migration. Issues #22–#24 must
be closed against the final closure PR rather than closing unrelated historical
issues.
