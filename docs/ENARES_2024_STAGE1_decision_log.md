# ENARES 2024 Stage 1 Decision Log

| Date | Decision | Reason | Alternatives considered | Reviewed by | Status |
|---|---|---|---|---|---|
| 2026-05-16 | Use the INEI Microdatos portal as the official source for ENARES 2024. | Stage 1 must be traceable to the official public microdata source. | Third-party mirrors, unofficial downloads, previously downloaded local copies. | Pending supervisor review | Proposed |
| 2026-05-16 | Select SPSS as the official download format for all ENARES 2024 modules. | SPSS `.sav` files preserve variable labels, value labels and coding metadata needed for reproducible interpretation. | CSV ZIP and Stata ZIP. | Pending supervisor review | Proposed |
| 2026-05-16 | Use SPSS ZIP as the official selected package type. | INEI distributes the selected raw files as module ZIP packages; preserving the ZIP keeps the original source package intact. | Extracted-only storage, Stata ZIP, CSV ZIP. | Pending supervisor review | Proposed |
| 2026-05-16 | Treat extracted `.sav` files as the primary raw data files. | `.sav` is the required raw analytical source for later metadata extraction with `pyreadstat`. | CSV as primary raw source; Stata `.dta` as primary raw source. | Pending supervisor review | Proposed |
| 2026-05-16 | Record the module range as `976-Modulo1941` through `976-Modulo1962`. | The Stage 1 brief defines 22 expected ENARES 2024 modules in this range. | Download all visible ENARES modules without a fixed expected range. | Pending supervisor review | Proposed |
| 2026-05-16 | Do not use CSV or Stata as the primary source in Stage 1. | The pipeline standard requires SPSS ZIP and `.sav` metadata preservation. | CSV for easier notebook loading; Stata for partial metadata support. | Pending supervisor review | Proposed |
| 2026-05-16 | Keep GitHub limited to code and documentation only. | Microdata, ZIPs, `.sav`, credentials and private IDs must remain outside version control. | Commit raw files to GitHub; commit unsanitized Drive manifests. | Pending supervisor review | Proposed |
| 2026-05-16 | Keep Week 1 boundaries limited to ingestion evidence, provenance, integrity and metadata preparation. | Stage 1 excludes BigQuery, cleaning, recoding, merges, analysis, graphics and ML. | Start BigQuery or analysis early. | Pending supervisor review | Proposed |
