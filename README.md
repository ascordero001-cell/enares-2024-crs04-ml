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

Actualmente el repositorio se enfoca en **Stage 1 - Data Ingestion**.

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

Stage 1 se encuentra en desarrollo.

Pendiente o en revisión:

- creación/verificación de estructura en Google Drive;
- ingesta de módulos ENARES 2024;
- generación de manifest y logs;
- identificación de CRS04;
- extracción de metadata SPSS;
- reporte de cierre Stage 1;
- documentación de decisiones técnicas;
- revisión supervisora semanal.

---

# Author

**Ana Silvia Cordero Ricaldi**  
BSc Computer Science, University of Sussex

Supervised independent research apprenticeship.
