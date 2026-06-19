# ENARES 2024 - Stage 1 Ingestion Report

## Account and Objective
- **Account Used:** anacordero.001@gmail.com
- **Objective:** Reproducible ingestion of ENARES 2024 CRS04 dataset from INEI SPSS ZIP source, ensuring traceability, metadata preservation, and initial module identification.
- **Scope Notice:** Stage 1 documents ingestion and preservation only. No statistical analysis, data cleaning, recoding, merging, modeling, or BigQuery transfers have been performed at this stage.

## GitHub Repository
- **Repository:** https://github.com/ascordero001-cell/enares-2024-crs04-ml
- **Linked Issue:** Issue #7 - Write Stage 1 report
- **Linked Notebook:** `notebooks/01_ingesta/04_ENARES_2024_STAGE1_reporte_cierre.ipynb`
- **Linked Commit:** pending

## Official Data Source & Format
- **Source:** https://proyectos.inei.gob.pe/microdatos/
- **Raw Package:** Data downloaded as exact SPSS ZIP packages from INEI.
- **Format:** ZIP files preserved intact; `.sav` files are the confirmed raw analytical source. CSV/Stata formats were NOT used as primary sources to ensure metadata integrity.

## Drive Structure
- **Total Registered Folders:** 19
- **Main Subfolders Present:** True (01BasesDatosPrimarias, 04CuestionariosInformes, 05Resultados, 99Codigos)
- **Project Root Path:** `/content/drive/MyDrive/ENARES_2024_PROJECT`

## Required Inputs Verification
| Input | Status | Size (Bytes) | Path |
|---|---|---|---|
| Manifest JSON | FOUND | 66510 | `/content/drive/MyDrive/ENARES_2024_PROJECT/01BasesDatosPrimarias/ENARES_2024_STAGE1_manifest_20260619_175509.json` |
| Log TXT | FOUND | 901 | `/content/drive/MyDrive/ENARES_2024_PROJECT/01BasesDatosPrimarias/ENARES_2024_STAGE1_log_ingesta_20260525_232957.txt` |
| Catalogue CSV | FOUND | 12485 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_STAGE1_catalogo_modulos.csv` |
| CRS04 Variables CSV | FOUND | 315388 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_CRS04_variables_stage1.csv` |
| CRS04 Values CSV | FOUND | 562770 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_CRS04_value_labels_stage1.csv` |
| CRS04 Validation CSV | FOUND | 2580 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_CRS04_validacion_stage1.csv` |
| CRS04 Missing CSV | FOUND | 1 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_CRS04_missing_codes_stage1.csv` |
| CRS Ident Report | FOUND | 4038 | `/content/drive/MyDrive/ENARES_2024_PROJECT/04CuestionariosInformes/reportes/ENARES_2024_CRS_identificacion_modulos.md` |
| Drive Folder IDs | FOUND | 2375 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_PROJECT_drive_folder_ids.csv` |
| Resource Metrics JSON | FOUND | 327 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_STAGE1_resource_metrics.json` |
| Assertion Results CSV | FOUND | 252 | `/content/drive/MyDrive/ENARES_2024_PROJECT/05Resultados/logs/ENARES_2024_STAGE1_assertion_results.csv` |

## Modules Processed
- **Expected Modules (Total):** 22 (Range: 976-Modulo1941 to 976-Modulo1962)
- **Processed Modules:** 22
- **Failed Modules:** 0

## Integrity Checks
- **ZIPs:** Downloaded and verified via SHA-256.
- **.sav Files:** Extracted and mapped in the catalogue.
- **PDFs:** Questionnaire and dictionary PDFs identified in catalogue.
- **Drive IDs:** Generated and stored securely.
- **Missing Codes:** Reviewed. If the missing codes output is empty, no SPSS user-missing metadata was exported/detected in the `.sav` headers.

## Manifest
- **File Used:** `ENARES_2024_STAGE1_manifest_20260619_175509.json`
- **Total Records:** 22
- **Confirmation:** `selected_download_format = SPSS` and `official_selected_package_type = SPSS ZIP`.
- **Integrity:** SHA-256 checksums documented for all downloaded packages.

## Log
- **File Used:** `ENARES_2024_STAGE1_log_ingesta_20260525_232957.txt`
- **Lines Processed:** 44
- **Inferred Date:** 2026-05-25 23:31:17
- **Errors/Failures Detected:** 0

## Catalogue
- **File Used:** `ENARES_2024_STAGE1_catalogo_modulos.csv`
- **Total Files Tracked:** 66
- **Extensions Found:**
  - `pdf`: 44 files
  - `sav`: 22 files

## CRS01-CRS04 Identification
Based on the separate identification report (`ENARES_2024_CRS_identificacion_modulos.md`), CRS01, CRS02, CRS03, and CRS04 were successfully identified. CRS04 specifically corresponds to:
- `976-Modulo1959`
- `976-Modulo1960`
- `976-Modulo1961`
- `976-Modulo1962`
This was confirmed using evidence from filename patterns, SPSS metadata, variable labels, and questionnaire dimensions.

## CRS04 Initial Validation
**Total CRS04 raw rows across four files: 75228**
> **Note:** Rows are summed across CAP100, CAP200, CAP248, and CAP300. This is **not** yet the merged adolescent-level analytical sample.

| Module | SAV File | Rows | Columns |
|---|---|---|---|
| 976-Modulo1959 | Unknown | 18807 | 147 |
| 976-Modulo1960 | Unknown | 18807 | 523 |
| 976-Modulo1961 | Unknown | 18807 | 578 |
| 976-Modulo1962 | Unknown | 18807 | 51 |

## Key CRS04 Candidate Variables Detected
- **Age & Sex:** Present in demographics.
- **Disability:** Candidates `C4P130_1` to `C4P130_6`.
- **Sample Weight:** `FACTOR_ALUMNOS`.
- **Strata:** `STRATA`.
- **Cluster/UPM:** `CCDD` (Department) and explicit school/ID identifiers to be verified in Stage 2.

## Performance Metrics
- Step profiled: stage1_inei_download_extract_hash
- Elapsed seconds: 68.34
- Memory start MB: 392.89
- Memory end MB: 392.89
- Memory delta MB: 0.0
- CPU start %: 15.5
- CPU end %: 17.8
- Interpretation: Stage 1 ingestion is I/O-bound and reproducible under documented resource constraints.

- CRS04 file count assertion: PASS
- CRS04 expected rows assertion: PASS
- CRS04 readable columns assertion: PASS
- CRS04 filename rule assertion: PASS
- CRS04 distinct modules assertion: PASS

## Issues Found
- No critical ingestion failures detected in manifest.
- No failed modules detected.
- Missing codes file was reviewed; if empty, no SPSS user-missing metadata were exported or detected.
- CRS04 row count is reported as raw rows across four files, not as a merged analytical sample.

## Pending Questions for Supervisor
1. Confirmation of CRS04 module boundaries (1959-1962).
2. Confirmation of interpretation regarding the CRS04 row sum vs. the final merged adolescent sample.
3. Confirmation of sample design variables: Weight (`FACTOR_ALUMNOS`), Strata (`STRATA`), and Cluster/UPM.
4. Validation of derived disability variable definition candidates (`C4P130_1`–`C4P130_6`).
5. Confirmation that Stage 2 must thoroughly validate merge keys before any joins occur.

## Output Summary
- **Report Generated At:** 2026-06-19 18:14:04
- **Report Path:** `/content/drive/MyDrive/ENARES_2024_PROJECT/04CuestionariosInformes/reportes/ENARES_2024_STAGE1_ingestion_report.md`
- **Inputs Read Successfully:** 11
- **Inputs Missing:** 0

## Stage 1 Refactorization Sprint Addendum

Durante el sprint de refactorización de Stage 1 se fortaleció la evidencia computacional del pipeline. La ingesta INEI fue instrumentada con medición de recursos mediante psutil, la identificación CRS04 incorporó aserciones programáticas de integridad estructural, el reporte de cierre integró métricas de rendimiento y resultados de validación ejecutable, y se agregó un notebook EDA con ydata-profiling para perfilamiento descriptivo crudo. Además, se prepararon artefactos de portabilidad e integración continua mediante Dockerfile y GitHub Actions.

Estos cambios no modifican el alcance metodológico de Stage 1: no limpian, no recodifican, no fusionan tablas, no crean indicadores y no realizan inferencia; documentan reproducibilidad, trazabilidad y control técnico del proceso de ingesta.

- **Stage 1 Status:** **Ready for Supervisor Review**
