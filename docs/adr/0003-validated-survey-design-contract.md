# ADR-0003: Validated CRS04 Survey Design Contract

- Date: 2026-08-23
- Status: Accepted for V0.5 shadow

## Context

The planning document proposed `ID + ID_AULA` as a design subject to
validation. The official CSPLAN evidence and the complete SPSS–R regression
identify a one-stage design.

## Decision

Use `CCDD` as stratum, `ID` as PSU and `FACTOR_ALUMNOS` as weight. Retain
`ID_AULA` only as a non-null audit field. Use `nest=TRUE` and the validated
lonely-PSU treatment in the R validation implementation.

## Evidence

- 18,807 rows;
- 25 strata;
- 1,115 PSUs;
- 1,090 design degrees of freedom;
- 3,014/3,014 statistical rows validated.

## Consequences

Adding `ID_AULA` as a second PSU stage would be a methodological change and
requires new SPSS evidence, regression and supervisor approval.
