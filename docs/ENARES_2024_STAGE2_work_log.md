# ENARES 2024 CRS04 - Stage 2 Work Log

Fecha: 2026-05-30T08:32:36.689105+00:00

## Trabajo realizado

- Notebook 1: se crearon/verificaron datasets BigQuery.
- Notebook 2: se cargaron cuatro tablas raw CRS04.
- Notebook 3: se preservo metadata SPSS en tablas BigQuery.
- Notebook 4: se genero reporte de cierre Stage 2.

## Evidencia principal

Los outputs estan en `05Resultados/logs`.

## Resultado

Stage 2 aprobado segun `ENARES_2024_STAGE2_cloud_storage_report.md`.

## Tablas raw verificadas

- `raw_crs04_cap100`: 18,807 filas.
- `raw_crs04_cap200`: 18,807 filas.
- `raw_crs04_cap248`: 18,807 filas.
- `raw_crs04_cap300`: 18,807 filas.

## Incidencias

- Los archivos `.sav` estaban dentro de subcarpetas; se ajusto el notebook para buscarlos de forma recursiva.
