# ENARES 2024 CRS04 ML Pipeline

Repositorio técnico del proyecto **ENARES 2024 CRS04 ML Pipeline**, desarrollado como parte de un **Independent Undergraduate Research Apprenticeship** en Data Engineering aplicado a microdatos oficiales de INEI.

El objetivo general del proyecto es construir una pipeline reproducible, trazable y auditable para procesar el **Cuestionario 4 de ENARES 2024**, correspondiente a adolescentes de 12 a 17 años.

---

# Project Scope

Este repositorio contiene código, notebooks, documentación técnica y evidencia de trabajo para las primeras etapas del pipeline:

- Stage 1: Data Ingestion
- Stage 2: Cloud Storage
- Stage 3: ETL & Pre-processing
- Stage 4: ML Modelling
- Stage 5: Evaluation & Validation

Stages 1 y 2 están aprobados. Stage 3 completó su validación técnica V0.5 en
modo shadow y espera el cierre operativo y la aceptación formal de Stage 04.

---

# Stage 1 - Data Ingestion

El objetivo de Stage 1 es construir una ingesta reproducible de los archivos originales de ENARES 2024 desde la fuente oficial de INEI hacia Google Drive.

Al cierre de Stage 1 debe poder demostrarse:

- de dónde salió cada archivo;
- qué formato de descarga fue seleccionado;
- cuándo fue descargado;
- dónde quedó guardado;
- cuál es su hash SHA-256;
- qué archivos fueron extraídos;
- qué módulo corresponde a CRS04;
- qué metadata SPSS fue preservada;
- si la ingesta puede reproducirse desde cero.

---

# Official Data Source

Fuente oficial:

<https://proyectos.inei.gob.pe/microdatos/>

Para este proyecto se utiliza siempre el paquete **SPSS ZIP** de cada módulo ENARES 2024.

El formato SPSS se selecciona porque los archivos `.sav` preservan metadata importante, incluyendo:

- variable labels;
- value labels;
- códigos originales;
- estructura de variables;
- documentación necesaria para interpretación reproducible.

CSV y Stata pueden estar disponibles en INEI, pero no se usan como fuente primaria en este proyecto.

---

# Repository Structure

```text
enares-2024-crs04-ml/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── notebooks/
│   └── 01_ingesta/
│
├── docs/
│   └── supervision_notes/
│
├── outputs/
│   └── logs/
│       └── README.md
│
├── sql/
├── src/
└── config/
```

---

# Notebooks - Stage 1

Los notebooks esperados para Stage 1 son:

```text
notebooks/01_ingesta/
├── 01_ENARES_2024_PROJECT_crear_estructura_drive.ipynb
├── 02_ENARES_2024_STAGE1_data_ingestion_inei.ipynb
├── 03_ENARES_2024_CRS04_identificar_modulo.ipynb
└── 04_ENARES_2024_STAGE1_reporte_cierre.ipynb
```

---

# Stage 1 Expected Outputs

Los outputs principales de Stage 1 se almacenan en Google Drive, no en GitHub.

Outputs esperados:

```text
05Resultados/logs/
├── ENARES_2024_PROJECT_drive_folder_ids.csv
├── ENARES_2024_STAGE1_catalogo_modulos.csv
├── ENARES_2024_CRS04_variables_stage1.csv
├── ENARES_2024_CRS04_value_labels_stage1.csv
├── ENARES_2024_CRS04_missing_codes_stage1.csv
└── ENARES_2024_CRS04_validacion_stage1.csv

01BasesDatosPrimarias/
├── ENARES_2024_STAGE1_manifest_YYYYMMDD_HHMMSS.json
└── ENARES_2024_STAGE1_log_ingesta_YYYYMMDD_HHMMSS.txt

04CuestionariosInformes/reportes/
├── ENARES_2024_CRS_identificacion_modulos.md
└── ENARES_2024_STAGE1_ingestion_report.md
```

---

# Data Governance

Este repositorio no contiene microdatos.

Por razones de trazabilidad, privacidad y control de versiones, GitHub solo contiene código y documentación. Los datos originales y outputs con identificadores privados permanecen en Google Drive.

No se debe subir a GitHub:

- archivos `.sav`;
- archivos `.zip`;
- archivos `.csv` con microdatos o IDs privados;
- archivos `.xlsx` con datos;
- credenciales;
- tokens;
- archivos `.env`;
- service accounts;
- outputs con información sensible;
- Google Drive file IDs no sanitizados.

---

# Required Python Packages

Las dependencias principales del proyecto son:

- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `requests`
- `tqdm`
- `pyreadstat`
- `pandas`

Estas dependencias están listadas en `requirements.txt`.

---

# Reproducibility Principle

La regla técnica del proyecto es:

> Código que no se puede reproducir, auditar y explicar no cuenta como producto técnico.

Cada etapa debe producir:

- código ejecutable;
- output verificable;
- log;
- manifest;
- documentación;
- decisión técnica;
- commit en GitHub;
- evidencia de revisión.

---

# Current Status

Stages 1 y 2 están aprobados. Stage 3 tiene un release técnico V0.5 validado
en shadow: `stage03-v0.5-cloud-full`.

Completado:

- baseline V0 preservada y etiquetada;
- raw sources, llave, cardinalidad y colisiones validadas;
- cleaned con 18,807 filas y 1,206 columnas;
- bloques analíticos 3.1–3.6 con 730 outputs derivados;
- analytical completo con 18,807 filas y 1,937 columnas;
- 516 indicadores y 3,014/3,014 filas estadísticas validadas;
- CI con `pytest` y compilación Dataform;
- PRs de migración revisados y merged.

Completado en el cierre operativo:

- reporting completo con 18,807 filas y 737 columnas explícitas;
- `ops.pipeline_runs` y `ops.validation_results`;
- assertions de calidad y paridad reporting en verde.

Pendiente antes de promoción:

- merge y CI del PR de cierre;
- aceptación metodológica y handoff formal a Stage 04;
- decisión separada de publicación o cutover.

Documentos de cierre:

- `docs/stage03/stage03_data_contract.md`;
- `docs/stage03/known_discrepancies.md`;
- `docs/stage03/stage3_closure_report.md`;
- `docs/stage03/stage04_handoff.md`.

---

# Stage 03 Local Setup

## Environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Google Cloud authentication

For a new computer or collaborator:

```powershell
gcloud init
gcloud auth application-default login
gcloud auth application-default set-quota-project enares-2024-crs04
```

No service-account keys or credential files should be stored in this repository.

## Tests

```powershell
python -m pytest -q
```

## V0.5 cloud validation

Run:

```text
notebooks/03_limpieza/00_ENARES_2024_STAGE03_cloud_config_pilot_v0_5.ipynb
```

using:

```text
Python (.venv ENARES CRS04)
```

The configuration pilot performs read-only checks for the required BigQuery
datasets and raw tables. The full shadow validation lives in
`03B_ENARES_2024_cloud_full_survey_validation_v0_5.ipynb`; its generated
respondent-level outputs remain in Drive and are not committed to GitHub.

## Version strategy

- V0: preserved baseline tagged `stage03-v0-baseline`.
- V0.5: modular configuration, tests and read-only cloud pilots.
- V1: approved Dataform/BigQuery pipeline promoted by component.

---

# Stage 03 Local Setup

## Environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

# Author

**Ana Silvia Cordero Ricaldi**  
BSc Computer Science, University of Sussex

Supervised independent research apprenticeship.
