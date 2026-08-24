# ADR-0002: BigQuery and Dataform for Controlled Stage 03 Processing

- Date: 2026-08-23
- Status: Accepted for V0.5 shadow

## Context

Stage 03 requires repeatable structural joins, 730 derived outputs, dependency
ordering and executable quality gates over four raw modules of 18,807 rows.

## Decision

Use BigQuery for controlled processing and Dataform for dependency management,
SQLX models and blocking assertions. Keep notebooks for explanation and
statistical validation, not as the sole production transformation engine.

## Consequences

- Raw, cleaned, analytical, outputs and ops remain separate datasets.
- Stable transformations are versioned as SQLX.
- Assertions return zero rows on success and block promotion on violations.
- Dataform compilation is a mandatory CI gate.
- V0 remains available until a candidate has parity evidence and approval.

## Alternatives rejected

- A notebook-only rewrite lacks a reliable dependency graph and clean-run gate.
- Kubernetes and Airflow add operational complexity not justified by this
  batch size and are non-blocking learning laboratories.
