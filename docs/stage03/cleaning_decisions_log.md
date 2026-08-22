# Stage 03 Cleaning Decisions — CRS04

## Controlled merge

- Base table: `raw_crs04_cap100`
- Join type: `LEFT JOIN`
- Composite key: `ID + COLEGIAL_ID`
- Expected universe: 18,807 adolescents
- Output columns: 1,206
- Candidate table: `cleaned_crs04_merged_adolescents_v0_5`
- Status: SHADOW

## Key decision

The raw and V0 keys use `FLOAT64`. Validation demonstrated:

- zero null key values;
- zero decimal key values;
- zero duplicate key groups;
- complete matching across CAP100, CAP200, CAP248 and CAP300.

Therefore, V0.5 normalizes `ID` and `COLEGIAL_ID` to `INT64`.
No other column type is intentionally changed.

## Collision decision

Thirty-one columns occur in all four modules. Comparison across all
18,807 matched rows found zero value differences.

CAP100 is therefore the canonical source for shared administrative,
geographical and survey-design columns. The 93 duplicate occurrences
in CAP200, CAP248 and CAP300 are excluded explicitly.

## Semantic boundaries

- No analytical indicators are created in `cleaned`.
- No blanket conversion of `NULL` to zero is performed.
- The V0 table is not overwritten or renamed.
- The V0.5 table remains shadow-only until reviewed and approved.