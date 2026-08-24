# Stage 03 Closure Reporting/Ops Dataform Evidence

- Execution date: 2026-08-23/24 UTC
- Project/location: `enares-2024-crs04` / `US`
- Result: `PASS`

## Local reproducibility gates

- Python tests: 91 passed.
- Python compileall: passed.
- Dataform compile: 44 actions.
- Compiled datasets: 14.
- Compiled assertions: 30.

## Materialized tables

| Object | Result | Job ID | Bytes billed |
|---|---|---|---:|
| `enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5` | created | `dataform-2dcbab17-0f14-457d-b1d3-28576148f23d` | 101 MiB |
| `enares2024_crs04_ops.pipeline_runs` | created | `dataform-5c78f7f2-773c-4f86-aaf7-c9675eb15ab7` | 0 B |
| `enares2024_crs04_ops.validation_results` | created | `dataform-590b0035-28fa-4606-b48b-7121deecb4da` | 0 B |

Independent BigQuery metadata inspection confirmed:

- reporting rows: 18,807;
- reporting columns: 737;
- pipeline run rows: 1;
- validation-result rows: 5;
- validation results with `PASS` or `PASS_CON_EXCEPCION_DOCUMENTADA`: 5.

## Assertions

| Assertion | Result | Job IDs | Bytes billed |
|---|---|---|---:|
| `survey_input_full_quality` | PASS | `dataform-f4399c93-f45b-43d8-983f-8bdc06d81c86`, `dataform-3b943092-3427-4910-905a-f0589d0c4ae1` | 20 MiB |
| `survey_input_full_v0_parity` | PASS | `dataform-f8dba382-e8bc-4d09-998f-d22c241f005f`, `dataform-c7966f8f-b9d4-4b45-ab6b-8b5629bb9a47` | 201 MiB |

## Traceability note

The first operational materialization verified table shape and content. The
ops models now require `runId` and `gitCommitSha` runtime variables. After the
closure commit is created, `pipeline_runs` and `validation_results` must be
rerun with that commit SHA before the closure PR is merged.

No V0 table was modified. V0.5 remains `shadow`.
