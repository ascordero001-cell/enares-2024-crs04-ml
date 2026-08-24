# ADR-0004: Synthetic Public Tests and Aggregate Operational Lineage

- Date: 2026-08-23
- Status: Accepted

## Context

Public CI must exercise methodology without exposing ENARES respondent rows.
Approved outputs must also be traceable to data, code, execution and evidence.

## Decision

1. Test representative indicator semantics with small synthetic inputs and
   explicit expected results.
2. Keep respondent-level records outside GitHub.
3. Store only release-level metadata in `ops.pipeline_runs`.
4. Store only aggregate gate outcomes in `ops.validation_results`.
5. Link every ops result to `run_id`, `release_id`, Git commit and evidence.

## Consequences

- CI can run from a clean public clone.
- Passing Python tests does not replace BigQuery/Dataform assertions or
  methodological review.
- Ops tables can be audited without mixing logs into analytical data.
- A new approved run requires a new lineage record rather than overwriting
  the meaning of an earlier release.
