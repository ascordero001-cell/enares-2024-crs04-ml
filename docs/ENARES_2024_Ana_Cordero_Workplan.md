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
| Workplan | Stage 1 scope, role, schedule, review plan, evaluation criteria and final outputs. | `docs/ENARES_2024_Ana_Cordero_Workplan.md` | Submitted for review |
| Source registry | Official INEI source, ENARES 2024 survey metadata, selected SPSS ZIP package, module range and alternative formats not selected. | `docs/ENARES_2024_STAGE1_source_registry.md` | Submitted for review |
| Work log | Independent work record with task, output, time, issues, next step and review status. | `docs/ENARES_2024_STAGE1_work_log.md` | Submitted for review |
| Decision log | Data engineering decisions for reproducible ingestion, provenance, integrity and metadata preservation. | `docs/ENARES_2024_STAGE1_decision_log.md` | Submitted for review |
| Supervision note | Week 01 supervision evidence, submitted products, revision needs, comments, technical issues and next week tasks. | `docs/supervision_notes/week_01_supervision_review.md` | Submitted for review |

## Review schedule

| Review point | Expected date | Purpose | Evidence |
|---|---:|---|---|
| Week 01 documentation review | 2026-05-16 | Confirm Stage 1 documentation, selected source package, apprenticeship evidence and supervisor pending items. | Workplan, source registry, work log, decision log and supervision note |
| Week 01 technical review | 2026-05-23 | Confirm ingestion reproducibility, manifest/log/catalogue outputs, CRS04 identification and SPSS metadata extraction. | Notebooks, manifest, logs, catalogue, CRS04 metadata outputs |

## Evaluation criteria

| Criterion | Standard |
|---|---|
| Reproducibility | The work must show how ENARES 2024 files can be ingested again from the official INEI source. |
| Data provenance | Each selected module must be traceable to the official INEI Microdatos portal, download format, package type and timestamp. |
| Integrity checks | SHA-256 checks, file sizes, preserved ZIP files and extracted raw files must be documented in Stage 1 outputs. |
| Metadata preservation | SPSS `.sav` metadata, including variable labels, value labels and missing codes where available, must be preserved and extracted. |
| Documentation | Workplan, source registry, work log, decision log and supervision note must be complete, dated and auditable. |
| Professional boundaries | No BigQuery, cleaning, recoding, merges, statistical analysis, graphics or ML models in Stage 1. |
| Data safety | Microdata, ZIPs, `.sav` files, credentials and private Drive IDs must not be uploaded to GitHub. |

## Final outputs

| Output | Expected form |
|---|---|
| Apprenticeship evidence bundle | Five required Markdown files under `docs/`. |
| Stage 1 source registry | Official INEI source, SPSS ZIP selection, module range `976-Modulo1941` to `976-Modulo1962`, and alternative formats not selected. |
| Stage 1 supervision evidence | Work log, decision log and week 01 supervision review note. |
| Handoff to technical ingestion | Documentation ready to support Colab notebooks, Google Drive storage, manifests, logs and CRS04 metadata validation. |
