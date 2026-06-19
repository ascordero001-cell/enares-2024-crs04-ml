# ENARES 2024 Stage 1 Work Log

| Date       | Task                                                                                                        | Output                                                                                                                                                                                                                                                                                                                                                                                                          | Time spent | Issues                                                                                                                                                                                                                                                                    | Next step                                                                                                                | Review status            |
| ---------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| 2026-05-15 | **Sprint Inicial:** Inicialización del repositorio y arquitectura del entorno local en VS Code.             | Repositorio creado en GitHub, configuración de límites estrictos en `.gitignore` y definición de dependencias en `requirements.txt`.                                                                                                                                                                                                                                                                            |  1.5 hours | Ninguno. Se bloquearon correctamente los binarios `.sav` y `.zip` para evitar fugas de datos.                                                                                                                                                                             | Construir los notebooks base de ingesta.                                                                                 | **Completed & Pushed**   |
| 2026-05-16 | Diseño y ejecución del Notebook 01 para la automatización de la estructura de carpetas en la nube.          | `01_PROJECT_crear_estructura_drive.ipynb` ejecutado. Carpeta raíz y subcarpetas mapeadas y verificadas sin duplicados.                                                                                                                                                                                                                                                                                          |  1.0 hours | Ninguno. La API v3 de Drive respondió correctamente mapeando los IDs únicos de los directorios.                                                                                                                                                                           | Iniciar el pipeline de descarga masiva.                                                                                  | **Completed & Verified** |
| 2026-05-18 | Desarrollo y pruebas del bucle de ingesta masiva (Notebook 02) desde el portal oficial del INEI.            | `02_STAGE1_data_ingestion_inei.ipynb` configurado con lógicas de retry y backoff para los 22 módulos esperados.                                                                                                                                                                                                                                                                                                 |  2.0 hours | Google Drive API/FUSE lanzó un error de conexión (`Errno 103`) al intentar extraer archivos `.sav` pesados en secuencia directa a la nube.                                                                                                                                | Implementar buffers locales en `/content/` para estabilizar el flujo.                                                    | **Completed & Verified** |
| 2026-05-19 | Optimización del script de ingesta (Hotfix) y cálculo masivo de firmas criptográficas.                      | Manifest JSON actualizado a v2.0; hashes SHA-256 calculados para cada ZIP y archivo extraído en Drive.                                                                                                                                                                                                                                                                                                          |  1.5 hours | Errores de sintaxis al escapar caracteres de barras invertidas (`\\`) en las consultas automatizadas de la API de Drive.                                                                                                                                                  | Corregir los strings literales del helper y proceder al análisis de metadatos de SPSS.                                   | **Completed & Pushed**   |
| 2026-05-21 | Desarrollo del Notebook 03 para la extracción profunda de metadatos SPSS mediante `pyreadstat`.             | `03_CRS04_identificar_modulo.ipynb` completado. Extracción exitosa de etiquetas de variables, value labels y missing codes para CRS04.                                                                                                                                                                                                                                                                          |  1.5 hours | Mapear las heurísticas (`possible_`) para variables de diseño complejo requirió refinar expresiones regulares sobre las etiquetas de las columnas.                                                                                                                        | Generar las tablas CSV de validación de Stage 1.                                                                         | **Completed & Verified** |
| 2026-05-22 | Redacción de la documentación obligatoria del Apprenticeship y auditoría de la canalización.                | Finalización de los archivos Markdown en `docs/` (Workplan, Source Registry, Decision Log y Supervision Note).                                                                                                                                                                                                                                                                                                  |  1.0 hours | Alinear los formatos y nombres de columnas estrictos exigidos por la rúbrica del proyecto.                                                                                                                                                                                | Realizar la revisión de cumplimiento final y preparar la entrega.                                                        | **Completed & Pushed**   |
| 2026-05-23 | **Cierre de Stage 1:** Control de calidad de entregables, reubicación de logs y despliegue del Notebook 04. | `04_STAGE1_reporte_cierre.ipynb` ejecutado. El archivo `log_ingesta.txt` fue movido de `05Resultados` a `01BasesDatosPrimarias` para cumplir la rúbrica.                                                                                                                                                                                                                                                        |  1.0 hours | Se detectó que la ruta del log violaba la especificación del checklist de entrega. Se corrigieron los parámetros de `LOG_DIR` a `RAW_DIR`.                                                                                                                                | Push final a GitHub y handoff listo para Stage 2 (Cloud Storage).                                                        | **Completed & Pushed**   |
| 2026-06-19 | **Sprint 1 Refactorization & Closure Activities**                                                           | Se implementó GitHub Actions CI (`.github/workflows/ci.yml`), se limpiaron y fijaron versiones exactas en `requirements.txt`, se corrigió la generación idempotente del manifest, se eliminaron duplicados del catálogo, se fortaleció el notebook de perfilamiento con evidencia de reproducibilidad (SHA-256, timestamps UTC y limpieza de memoria), y se versionó el reporte Stage 1 dentro del repositorio. |  2.0 hours | Se detectó que el manifest y el catálogo crecían al reejecutar el notebook debido a operaciones de append no idempotentes. También se verificó que las métricas de recursos provenían de una ejecución con artefactos en caché y no de una descarga completamente limpia. | Cerrar Sprint 1 e iniciar Stage 2, validando claves de unión, estructura analítica y preparación de datos para modelado. | **Completed & Pushed**   |

---

# Sprint 1 Learning Notes

## What did I build this sprint, and what evidence proves it ran?

Durante Sprint 1 construí una canalización reproducible de ingesta para ENARES 2024 utilizando los paquetes oficiales SPSS ZIP publicados por el INEI. El flujo automatiza la descarga, extracción, catalogación, validación de integridad, identificación de módulos CRS04, exportación de metadatos SPSS y generación de reportes de evidencia.

La ejecución está respaldada por los siguientes artefactos:

* Manifest JSON con trazabilidad por módulo.
* Log de ingesta.
* Catálogo de archivos procesados.
* Validaciones CRS04.
* Resultados de aserciones programáticas.
* Métricas de recursos.
* Reportes HTML de perfilamiento.
* Reporte final de Stage 1.
* Evidencia de ejecución en GitHub y Google Drive.

## The manifest doubled — what did I learn?

Aprendí el concepto de **idempotencia**. El notebook de ingesta agregaba registros al manifest cada vez que era ejecutado, incluso cuando los módulos ya habían sido procesados anteriormente. Como consecuencia, una segunda ejecución producía 44 registros para 22 módulos.

La solución no fue únicamente eliminar los duplicados existentes, sino corregir la causa raíz: impedir que un módulo ya registrado vuelva a agregarse al manifest. A partir de esta corrección, el resultado final permanece estable independientemente del número de veces que se ejecute el notebook.

Esta experiencia reforzó la importancia de diseñar procesos reproducibles y seguros frente a reejecuciones accidentales.

## Why does pinning versions matter for reproducibility?

La reproducibilidad no depende únicamente del código; también depende del entorno donde se ejecuta.

Si una dependencia cambia de versión, una ejecución futura podría producir resultados distintos, lanzar advertencias nuevas o incluso fallar. Por ese motivo se limpiaron las dependencias duplicadas y se fijaron versiones exactas en `requirements.txt`.

Entre ellas:

* pandas==2.2.2
* pyreadstat==1.3.5
* psutil==5.9.5
* requests==2.32.4
* tqdm==4.67.3
* ydata-profiling==4.18.4
* google-api-python-client==2.197.0
* google-auth==2.47.0
* google-auth-httplib2==0.4.0
* google-auth-oauthlib==1.4.0
* pydata-google-auth==1.9.1

La fijación explícita de versiones permite reconstruir el entorno de ejecución de manera consistente en el futuro.

## Were the resource metrics a fair measurement?

Las métricas de recursos registradas durante Stage 1 corresponden a una ejecución donde parte de los archivos ya se encontraban descargados y extraídos previamente.

Por tanto, representan correctamente el comportamiento del pipeline en condiciones de reutilización de caché, pero no constituyen una medición exacta del costo de una ingesta completamente limpia.

Para obtener una medición más representativa del proceso real se debería:

1. Eliminar todos los ZIP descargados.
2. Eliminar directorios de extracción.
3. Limpiar artefactos intermedios.
4. Ejecutar nuevamente la descarga desde cero.
5. Medir todo el ciclo descarga → extracción → catalogación → validación.

Las métricas actuales siguen siendo útiles como evidencia operacional, pero deben interpretarse como una medición de ejecución con caché y no como un benchmark de cold start.

---

# Sprint 1 Closure Summary

## Technical Deliverables Completed

* Estructura oficial de Google Drive creada y validada.
* Descarga automatizada de los 22 módulos ENARES 2024.
* Preservación de paquetes oficiales SPSS ZIP.
* Cálculo de hashes SHA-256 para trazabilidad.
* Exportación de metadatos SPSS mediante pyreadstat.
* Identificación documentada de CRS01–CRS04.
* Validación estructural de CRS04.
* Generación de catálogo de archivos.
* Generación de manifest de procedencia.
* Generación de logs de ejecución.
* Instrumentación de métricas de recursos.
* Perfilamiento descriptivo con ydata-profiling.
* Dockerfile preparado para portabilidad.
* GitHub Actions configurado para integración continua.
* Dependencias fijadas para reproducibilidad.
* Reporte final de Stage 1 versionado en el repositorio.

## Validation Results

* Modules processed: 22/22.
* Failed modules: 0.
* Manifest records: 22.
* Catalogue records: 66 (22 archivos SAV y 44 archivos PDF).
* CRS04 modules validated:

  * 976-Modulo1959
  * 976-Modulo1960
  * 976-Modulo1961
  * 976-Modulo1962
* CRS04 row count validated: 18,807 observaciones por módulo.
* CRS04 assertions: PASS.
* Resource profiling: PASS.
* Metadata export: PASS.
* Provenance documentation: PASS.

## Supervisor Closure Requirements Addressed

* CI workflow implemented.
* Manifest duplication resolved through idempotent guards.
* Catalogue duplication resolved.
* Dependency versions pinned.
* Stage 1 report committed to repository.
* Engineering review comments addressed.

---

**Sprint 1 Status:**  **Closed and ready for Stage 2.**
