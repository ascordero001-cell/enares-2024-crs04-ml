# ENARES 2024 CRS04 ML Pipeline - Ana Cordero Workplan

## Project overview

| Field | Entry |
|---|---|
| Project title | ENARES 2024 CRS04 ML Pipeline - Stage 1 Data Ingestion |
| Role | Computer Science Lead - Data Engineering |
| Project type | Independent Undergraduate Research Apprenticeship; reproducible data engineering contribution, not a formal internship |
| Supervisor | Pending supervisor confirmation |
| Stage | Stage 1 - Data Ingestion |
| Start date | 2026-05-16 |
| End date | 2026-05-23 |
| Weekly hours expected | 6-8 hours |

## Deliverables

| Deliverable | Description | Evidence file or location | Review status |
|---|---|---|---|
| Workplan | Stage 1 scope, role, schedule, review plan, evaluation criteria and final outputs. | `docs/ENARES_2024_Ana_Cordero_Workplan.md` | **Accepted** |
| Source registry | Official INEI source, ENARES 2024 survey metadata, selected SPSS ZIP package, module range and alternative formats not selected. | `docs/ENARES_2024_STAGE1_source_registry.md` | **Accepted** |
| Work log | Independent work record with task, output, time, issues, next step and review status. | `docs/ENARES_2024_STAGE1_work_log.md` | **Updated** (Week 01 hours logged and completed) |
| Decision log | Data engineering decisions for reproducible ingestion, provenance, integrity and metadata preservation. | `docs/ENARES_2024_STAGE1_decision_log.md` | **Updated** (Format choice finalized and approved) |
| Supervision note | Week 01 supervision evidence, submitted products, revision needs, comments, technical issues and next week tasks. | `docs/supervision_notes/week_01_supervision_review.md` | **Completed** (Stage 1 pipeline executed, outputs validated) |

## Review schedule

| Review point | Expected date | Purpose | Evidence | Status |
|---|---:|---|---|---|
| Week 01 documentation review | 2026-05-16 | Confirm Stage 1 documentation, selected source package, apprenticeship evidence and supervisor pending items. | Workplan, source registry, work log, decision log and supervision note | **Completed & Passed** |
| Week 01 technical review | 2026-05-23 | Confirm ingestion reproducibility, manifest/log/catalogue outputs, CRS04 identification and SPSS metadata extraction. | Notebooks, manifest, logs, catalogue, CRS04 metadata outputs | **Completed & Passed** |

## Evaluation criteria

| Criterion | Standard | Status |
|---|---|---|
| Reproducibility | The work must show how ENARES 2024 files can be ingested again from the official INEI source. | **Verified.** Pipeline successfully re-executed via Google Colab natively from the INEI portal. |
| Data provenance | Each selected module must be traceable to the official INEI Microdatos portal, download format, package type and timestamp. | **Verified.** Audit records mapped inside JSON manifest and CSV catalogue. |
| Integrity checks | SHA-256 checks, file sizes, preserved ZIP files and extracted raw files must be documented in Stage 1 outputs. | **Verified.** Cryptographic signatures generated for all 22 official packages and individual `.sav`/PDF extractions. |
| Metadata preservation | SPSS `.sav` metadata, including variable labels, value labels and missing codes where available, must be preserved and extracted. | **Verified.** Processed through `pyreadstat` without loss of categorical mappings. |
| Documentation | Workplan, source registry, work log, decision log and supervision note must be complete, dated and auditable. | **Verified.** Complete documentation trace versioned safely inside the private GitHub repository. |
| Professional boundaries | No BigQuery, cleaning, recoding, merges, statistical analysis, graphics or ML models in Stage 1. | **Verified.** Strictly isolated to ingestion, integrity checks, and raw metadata extraction. |
| Data safety | Microdata, ZIPs, `.sav` files, credentials and private Drive IDs must not be uploaded to GitHub. | **Verified.** Explicit rules added to `.gitignore`. Microdata isolated completely inside Google Drive. |

## Final outputs

| Output | Expected form | Location / Status |
|---|---|---|
| Apprenticeship evidence bundle | Five required Markdown files under `docs/`. | `docs/` folder updated with full logs. |
| Stage 1 source registry | Official INEI source, SPSS ZIP selection, module range `976-Modulo1941` to `976-Modulo1962`, and alternative formats not selected. | `docs/ENARES_2024_STAGE1_source_registry.md` finalized. |
| Stage 1 supervision evidence | Work log, decision log and week 01 supervision review note. | Synced and pushed to the private GitHub repository. |
| Handoff to technical ingestion | Documentation ready to support Colab notebooks, Google Drive storage, manifests, logs and CRS04 metadata validation. | **Complete.** All 4 operational notebooks fully executed and saved inside Google Drive `99Codigos/01_ingesta/`. |