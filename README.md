# ENARES 2024 CRS04 — Reproducible Cloud Pipeline and Population Surveillance

[![CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/workflows/ci.yml)

Pipeline reproducible, trazable y auditable para procesar el Cuestionario 4 de
ENARES 2024, correspondiente a adolescentes de 12 a 17 años, y preparar una
aplicación de vigilancia poblacional de la violencia contra niñas, niños y
adolescentes.

El proyecto forma parte de un **Independent Undergraduate Research
Apprenticeship** en Data Engineering aplicado a microdatos oficiales del INEI.

> **Estado de publicación:** V0 continúa siendo la versión oficial. La versión
> `stage03-v0.5-cloud-full` completó sus gates técnicos, de reproducibilidad,
> supervisión metodológica y handoff a Stage 04, pero permanece en
> `SHADOW — NOT PUBLISHED`.

## Estado del proyecto

| Stage | Alcance | Estado |
|---|---|---|
| Stage 01 | Ingesta y preservación de fuentes oficiales | ✅ Aprobado |
| Stage 02 | Almacenamiento y validación inicial en BigQuery | ✅ Aprobado |
| Stage 03 | Limpieza, indicadores 3.1–3.6, diseño muestral y migración cloud | ✅ `PASS` en shadow |
| Stage 04 | Aplicación cloud de vigilancia poblacional y publicación agregada controlada | `PREPARING/SHADOW` — bootstrap en revisión |
| Stage 05 | Evaluación, monitoreo y decisiones posteriores de publicación | ⏳ Pendiente |

## Principios

- La V0 se conserva; la migración no borra el trabajo previo.
- SPSS y los contratos V0 congelados son la referencia metodológica.
- Cada componente candidato se valida antes de cualquier promoción.
- `0`, `NULL`, salto válido y no respuesta conservan significados distintos.
- El bloque oficial **3.6 corresponde a búsqueda de ayuda**; los nombres
  históricos 3.7 se preservan únicamente para trazabilidad.
- Stage 04 consume resultados aprobados de Stage 03 y no recalcula indicadores.
- GitHub contiene código, contratos y evidencia agregada; no contiene
  microdatos ni credenciales.

## Arquitectura

```text
INEI / fuentes SPSS oficiales
  -> Stage 01: ingesta, manifiestos y hashes
  -> Stage 02: BigQuery raw
  -> Stage 03: cleaned
  -> Stage 03: analytical 3.1–3.6
  -> reporting_crs04_survey_input_v0_5
  -> validaciones Dataform + regresión SPSS–R
  -> decisión humana y release shadow
  -> Stage 04: resultados agregados
  -> staging_dashboard_base
  -> validación
  -> staging_dashboard_indicators
  -> validación
  -> published.v_dashboard_current
  -> aplicación Streamlit / Cloud Run
```

La futura aplicación consulta únicamente datos agregados, validados y
publicados. No consulta `raw`, `cleaned`, `analytical` ni microdatos de
respondentes.

## Resultados de Stage 03

La migración cloud de Stage 03 cerró con:

- baseline V0 preservada mediante el tag `stage03-v0-baseline`;
- release técnico `stage03-v0.5-cloud-full`;
- 18,807 registros en la base integrada;
- 1,206 columnas en la capa cleaned;
- bloques analíticos 3.1–3.6 y 730 outputs derivados;
- 1,937 columnas en la tabla analytical completa;
- 516 indicadores y 3,014 filas estadísticas validadas;
- 3,013/3,014 comparaciones SPSS–R con paridad estricta;
- una excepción metodológica documentada: `VS_12M — Nacional — Total`;
- contrato reporting de 18,807 filas y 737 columnas explícitas;
- tablas operativas `pipeline_runs` y `validation_results`;
- CI con `pytest` y compilación Dataform;
- aprobación metodológica independiente mediante PR #40;
- handoff, decisión `REMAIN_SHADOW` y cierre mediante PR #41.

La excepción `VS_12M` utiliza el denominador poblacional completo de 18,807
adolescentes, de acuerdo con la regla canónica documentada. No se ocultó ni se
absorbió mediante una tolerancia mayor.

## Diseño muestral validado

El contrato validado para R survey es:

```r
svydesign(
  ids = ~ID,
  strata = ~CCDD,
  weights = ~FACTOR_ALUMNOS,
  nest = TRUE
)
```

El diseño reproduce 25 estratos, 1,115 PSU y 1,090 grados de libertad.
`ID_AULA` se conserva para auditoría, pero no se utiliza como segunda etapa del
diseño validado.

## Módulos analíticos

| Bloque | Contenido |
|---|---|
| 3.1 | Características, percepciones y normas |
| 3.2 | Violencia psicológica y física en el hogar |
| 3.3 | Violencia psicológica y física en la escuela |
| 3.4 | Violencia sexual |
| 3.5 | Polivictimización y acumulación de violencias |
| 3.6 | Búsqueda y recepción de ayuda |

## Estructura del repositorio

```text
enares-2024-crs04-ml/
├── .github/workflows/       # Integración continua
├── configs/                 # Configuración, indicadores y skip logic
├── dataform/
│   └── definitions/
│       ├── sources/         # Fuentes raw y referencias V0
│       ├── cleaned/         # Integración estructural
│       ├── analytical/      # Bloques 3.1–3.6 y tabla completa
│       ├── assertions/      # Calidad, dominio y paridad
│       ├── reporting/       # Contrato de entrega a Stage 04
│       └── ops/             # Linaje y resultados de validación
├── docs/
│   ├── adr/                 # Architecture Decision Records
│   └── stage03/             # Contratos, evidencia y cierre
├── notebooks/
│   ├── 01_ingesta/
│   ├── 02_bigquery/
│   └── 03_limpieza/
├── scripts/                 # Generadores y utilidades reproducibles
├── src/enares/              # Código Python modular
├── tests/unit/              # Pruebas con datos sintéticos
├── .env.example
├── CONTRIBUTING.md
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

## Fuente oficial

Los microdatos y documentos fuente proceden del portal oficial de microdatos
del INEI:

<https://proyectos.inei.gob.pe/microdatos/>

El formato SPSS se conserva como fuente primaria porque mantiene etiquetas de
variables, etiquetas de valores, códigos y metadatos necesarios para la
interpretación reproducible.

## Instalación local

### Requisitos

- Git;
- Python 3.12;
- Google Cloud CLI;
- Node.js para compilar Dataform;
- acceso autorizado al proyecto cloud cuando corresponda.

### Clonar y crear el entorno

```powershell
git clone https://github.com/ascordero001-cell/enares-2024-crs04-ml.git
cd enares-2024-crs04-ml
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### Configuración segura

Use `.env.example` y `configs/project.example.yaml` como plantillas. No guarde
secretos ni rutas personales en archivos versionados.

Para autenticación local:

```powershell
gcloud init
gcloud auth application-default login
gcloud auth application-default set-quota-project enares-2024-crs04
```

Cloud Run debe utilizar una cuenta de servicio con mínimo privilegio; no se
versionan llaves de cuentas de servicio.

## Validación reproducible

### Pruebas Python

```powershell
python -m pytest -q
```

### Compilación Dataform

```powershell
npm install --global @dataform/cli@3.0.64
dataform compile dataform
```

El workflow `.github/workflows/ci.yml` ejecuta en un runner limpio:

- verificación de sintaxis Python;
- lint de notebooks como control informativo;
- pruebas `pytest` bloqueantes;
- compilación Dataform bloqueante.

Este flujo se denomina **CI**. No se presenta como CI/CD mientras no exista un
despliegue automático formalmente aprobado.

## Documentación de cierre

- [Stage 03 PASS](docs/stage03/stage3_pass.md)
- [Reporte de cierre](docs/stage03/stage3_closure_report.md)
- [Contrato de datos](docs/stage03/stage03_data_contract.md)
- [Aceptación supervisora](docs/stage03/stage03_supervisor_acceptance.md)
- [Handoff a Stage 04](docs/stage03/stage04_handoff.md)
- [Discrepancias conocidas](docs/stage03/known_discrepancies.md)
- [Decisiones de migración](docs/stage03/migration_decisions.md)
- [ADRs](docs/adr/)
- [Guía de contribución](CONTRIBUTING.md)

## Versionado y promoción

| Versión | Significado | Estado |
|---|---|---|
| V0 | Implementación histórica y versión oficial | Oficial |
| V0.5 | Migración cloud validada por componentes | `SHADOW — NOT PUBLISHED` |
| V1 | Eventual versión promovida tras una decisión futura de cutover | No aprobada |

Un `PASS` técnico o metodológico no equivale a autorización institucional de
publicación. La promoción requiere una decisión separada y registrada.

## Stage 04 — siguiente etapa

**Estado actual:** `PREPARING/SHADOW`. La preparación documental esta en curso y no autoriza publicación, cutover ni gasto cloud.

Documentos de inicio:

- [Puerta PRE-STAGE04](PRE_STAGE04.md)
- [Documento rector Stage 04](CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md)
- [Hoja arquitectonica](CRS04_STAGE04_HOJA_ARQUITECTONICA_APP_VIGILANCIA.md)
- [Convenciones de nombres](NAMING_CONVENTIONS.md)
- [Registro V0](CRS04_STAGE04_VERSION_0_REGISTRO.md)
- [Mapa real de issues](docs/stage04/issue_map.md)
- [Issue paraguas #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43)

Stage 04 construirá progresivamente una aplicación de vigilancia poblacional
con:

- navegación por módulos 3.1–3.6;
- desagregaciones autorizadas;
- estimaciones, IC95 %, CV y N no ponderado;
- reglas de calidad y supresión;
- comparación app–BigQuery–V0;
- Streamlit desplegado en Cloud Run;
- datos sintéticos o agregados shadow durante el desarrollo;
- publicación únicamente desde una vista agregada validada.

Kubernetes, Airflow, Agent Platform y Looker Studio son laboratorios u opciones
posteriores. No son requisitos para el MVP y pueden concluir como
`APRENDIDO Y EVALUADO, PERO NO ADOPTADO`.

## Gobernanza de datos

No subir a GitHub:

- archivos `.sav`, `.zip`, `.xlsx` o exports con microdatos;
- identificadores personales o filas de respondentes;
- credenciales, tokens, archivos `.env` o llaves privadas;
- service-account keys;
- outputs confidenciales;
- rutas personales o identificadores de Drive no sanitizados.

Los datos originales y outputs restringidos permanecen en ubicaciones cloud
autorizadas. El repositorio público contiene únicamente código, documentación,
contratos, pruebas sintéticas y evidencia agregada.

## Contribución

El flujo esperado es:

```text
Issue -> rama -> commits pequeños -> pull request -> CI -> revisión -> merge
```

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) antes de proponer cambios. Las
modificaciones metodológicas requieren revisión independiente y una ADR cuando
cambian universos, denominadores, recodes, diseño muestral o reglas de
publicación.

## Autora

**Ana Silvia Cordero Ricaldi**
BSc Computer Science and Artificial Intelligence, University of Sussex
Independent undergraduate research apprenticeship

Supervisión metodológica independiente registrada en la evidencia de cierre de
Stage 03.

## Alcance y descargo

Este repositorio es un proyecto técnico y formativo. La versión V0.5 y la futura
aplicación Stage 04 no constituyen por sí mismas una publicación oficial del
INEI, UNICEF u otra institución. Cualquier uso institucional requiere revisión,
autorización y gobernanza adicionales.
