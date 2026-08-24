# Stage 03 Opening Checklist — CRS04

- Verification date: 2026-08-18
- Project: `enares-2024-crs04`
- Location: `US`
- Status: `PASS`

## Prerequisites

| Check | Evidence | Result |
|---|---|---|
| Stage 02 closed and documented | `docs/ENARES_2024_STAGE2_cloud_storage_report.md` | PASS |
| Four CRS04 raw tables exist | Dataform raw sources and BigQuery inventory | PASS |
| Every raw table has 18,807 rows | `raw_rowcount` assertion | PASS |
| SPSS metadata and V0 contracts are available | `docs/stage03/contracts/v0/` | PASS |
| Cloud project and datasets confirmed | `configs/project.example.yaml` | PASS |
| Local ADC authentication works | cloud configuration pilot | PASS |
| No credential is stored in Git | `.gitignore`, `.env.example` and CI review | PASS |

## Raw inventory

The approved inputs are:

- `enares2024_crs04_raw.raw_crs04_cap100`;
- `enares2024_crs04_raw.raw_crs04_cap200`;
- `enares2024_crs04_raw.raw_crs04_cap248`;
- `enares2024_crs04_raw.raw_crs04_cap300`.

Each table contains 18,807 records. `ID + COLEGIAL_ID` has no missing
values, decimal values or duplicate groups. Every non-CAP100 module matches
CAP100 on all 18,807 keys.

## Gate decision

Stage 03 was authorized to proceed in shadow mode. This checklist did not
authorize publication, replacement of V0 or a Stage 04 cutover.
