# ADR-0006: Stage 04 repository boundaries

- Date: 2026-09-15
- Status: Accepted

## Context

The Stage 04 application needs one read-only interface while its sources have different trust
levels. A synthetic teaching fixture, a manifest-bound extract of V0 and a future BigQuery view
must not become interchangeable merely because all three contain aggregate-shaped rows. The
restricted `survey_input` layer is respondent-level input and must never be an application source.

## Decision

1. `IndicatorRepository.list_estimates(module_id)` is the shared typed, read-only contract. It
   returns `IndicatorEstimate` objects or one of the safe `RepositoryError` subclasses.
2. `DemoRepository` accepts only rows whose input declares `synthetic=true`. It rejects sensitive
   columns and cannot produce a provenance-verified institutional estimate.
3. `AuthorizedAggregateRepository` verifies the extract digest, manifest classification, parent
   V0 SHA-256 and presence of that parent in the approved registry. `synthetic=false` is derived
   only after those checks; callers cannot set or promote it.
4. `BigQueryRepository` will implement the same interface only against the minimum projection of
   `published.v_dashboard_current`. Until the cloud gate is executed it fails closed as
   unavailable. It must not query `raw`, `cleaned`, `analytical`, `outputs` or `survey_input`.
5. The application may compose trusted aggregate repositories, but it does not import or execute
   notebooks and cannot convert demo rows into institutional rows.
6. Statistical validation and the approved granularity boundary run after retrieval and before a
   row reaches a card, chart, table or export. Cache identity includes both `release_id` and
   `run_id`.

## Consequences

- A common UI does not erase provenance differences between sources.
- A future cloud adapter can replace the local aggregate transport without changing statistical
  semantics or opening respondent-level access.
- Repository failures expose stable generic messages while preserving detailed diagnostics only
  in controlled internal handling.
- Adding a new source requires implementing the shared contract and proving the same fail-closed
  boundaries with tests.
