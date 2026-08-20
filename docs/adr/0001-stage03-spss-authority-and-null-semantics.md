# ADR-0001: SPSS Authority and NULL Semantics in Stage 03

- Date: 2026-08-20
- Status: Proposed — applied in shadow pending methodological approval
- Scope: ENARES 2024 CRS04 Stage 03

## Context

Stage 03 is migrating from validated notebooks and SPSS syntax to
versioned Dataform, SQL and Python components.

The migration must reproduce the validated V0 results without silently
changing indicator universes, denominators, skip logic or missing-value
semantics.

The validated V0 contains 516 indicator contracts and achieved complete
SPSS–R equality across 3,014 comparison rows.

## Decision

1. The canonical SPSS syntax remains the authority for indicator logic.
2. Frozen V0 contracts provide a reviewable representation of that logic.
3. `cleaned` handles structure, keys, joins, types and collisions only.
4. Analytical indicators are created only in `analytical`.
5. `NULL`, valid skip, non-response, not applicable and numeric zero are
   not treated as equivalent states.
6. A source `NULL` may become zero only when the applicable SPSS rule,
   gateway and indicator universe explicitly require that recode.
7. Each migrated indicator must declare its source variable, numerator,
   denominator or domain, dimensions, missing-value rule and calculation
   method.
8. A component remains SHADOW until its V0 comparison and methodological
   review pass.

## Consequences

- Blanket `COALESCE(column, 0)` transformations are prohibited.
- Differences must be investigated rather than hidden by changing
  tolerances or denominator rules.
- Dataform assertions validate technical contracts but do not constitute
  methodological approval.
- Unmigrated indicator blocks continue using V0 and are not represented
  as V1.
- Promotion requires reproducible evidence tied to a Git commit and run.

## Alternatives rejected

### Treat all missing values as zero

Rejected because it changes denominators and can alter prevalence
estimates.

### Use the generated dictionary as the sole authority

Rejected because dictionaries describe the implementation but do not
override canonical SPSS syntax.

### Replace all 516 indicators simultaneously

Rejected because block-by-block shadow migration provides clearer
regression evidence and safer review.

## Evidence

- `docs/stage03/contracts/v0/`
- `configs/indicators_crs04.yaml`
- `configs/skip_logic_crs04.yaml`
- `docs/stage03/evidence/v0_validation_pass.md`
- `docs/stage03/evidence/cleaned_v0_v0_5_validation_20260819.md`