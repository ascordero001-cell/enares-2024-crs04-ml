# Week 01 Supervision Review - ENARES 2024 CRS04 ML Pipeline

| Field | Entry |
|---|---|
| Project | ENARES 2024 CRS04 ML Pipeline |
| Researcher | Ana Cordero |
| Role | Computer Science Lead - Data Engineering |
| Project type | Independent Undergraduate Research Apprenticeship |
| Week | Week 01 |
| Stage | Stage 1 - Data Ingestion |
| Review date | 2026-05-16 |
| Supervisor | Pending supervisor confirmation |
| Stage 1 status | Documentation evidence submitted for review; technical ingestion execution pending notebook run |

## Submitted products

| Product | Location | Status |
|---|---|---|
| Workplan | `docs/ENARES_2024_Ana_Cordero_Workplan.md` | Submitted |
| Source registry | `docs/ENARES_2024_STAGE1_source_registry.md` | Submitted |
| Work log | `docs/ENARES_2024_STAGE1_work_log.md` | Submitted |
| Decision log | `docs/ENARES_2024_STAGE1_decision_log.md` | Submitted |
| Week 01 supervision note | `docs/supervision_notes/week_01_supervision_review.md` | Submitted |

## Accepted products

Pending supervisor review.

## Products requiring revision

| Product | Revision needed | Owner | Status |
|---|---|---|---|
| Workplan | Add confirmed supervisor name and confirm weekly hours if different from 6-8 hours. | Ana Cordero / Supervisor | Pending |
| Source registry | Validate every selected SPSS ZIP URL during notebook execution and update if INEI redirects or changes paths. | Ana Cordero | Pending |
| Work log | Add supervisor review status after feedback. | Ana Cordero | Pending |
| Decision log | Mark decisions as accepted or revised after review. | Supervisor / Ana Cordero | Pending |

## Supervisor comments

Pending supervisor comments.

## Technical issues

| Issue | Impact | Proposed action |
|---|---|---|
| This Section 6 task creates documentation only; it does not authenticate Google Drive or run Colab notebooks. | Manifest, SHA-256 values, Drive IDs and CRS04 row/column evidence are not produced in these docs. | Complete notebooks separately in Google Colab using `anacordero.001@gmail.com`. |
| Supervisor name was not provided in the brief. | Review ownership cannot be finalized yet. | Add supervisor name after confirmation. |
| INEI module URLs must be tested during ingestion. | Source registry records expected SPSS ZIP URLs, but runtime validation is still required. | Notebook 2 should verify download status, retry failures and write manifest/log outputs. |

## Next week tasks

| Task | Expected output |
|---|---|
| Run Drive structure notebook in Google Colab using `anacordero.001@gmail.com`. | `ENARES_2024_PROJECT_drive_folder_ids.csv` stored in Drive logs. |
| Run INEI SPSS ZIP ingestion notebook for modules `976-Modulo1941` to `976-Modulo1962`. | Preserved ZIPs, extracted `.sav` and PDFs, manifest JSON, ingestion TXT log and module catalogue CSV. |
| Compute SHA-256 for ZIPs and extracted files. | Integrity fields completed in manifest and catalogue. |
| Identify CRS01, CRS02, CRS03 and CRS04 using file names, labels, dimensions and documentation. | CRS identification report and CRS04 validation CSV. |
| Extract CRS04 SPSS metadata with `pyreadstat`. | Variable labels, value labels and missing code outputs. |
| Update supervision evidence after review. | Accepted products, comments, revised decisions and next actions documented. |

## Stage 1 status

The Section 6 apprenticeship evidence files are prepared and submitted for review. The documentation aligns Stage 1 with reproducible data ingestion from the official INEI Microdatos portal, selected SPSS ZIP packages, module range `976-Modulo1941` to `976-Modulo1962`, preservation of `.sav` metadata, and the rule that CSV/Stata are not primary sources. Technical execution in Colab and Google Drive remains the next step.
