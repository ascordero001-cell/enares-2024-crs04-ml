# ENARES 2024 CRS04 - Stage 2 Cloud Storage Workplan

Fecha: 2026-05-30T08:32:36.689105+00:00

## Objetivo

Cargar CRS04 raw a BigQuery y preservar metadata SPSS/PDF sin transformaciones analiticas.

## Alcance

Stage 2 incluye:
- Crear/verificar datasets `raw`, `cleaned` y `analytical`.
- Cargar los cuatro archivos `.sav` CRS04 como tablas raw.
- Validar conteos de filas.
- Validar conteos de columnas/schema.
- Preservar metadata SPSS como tablas separadas.
- Registrar archivos fuente y PDFs oficiales cuando esten disponibles.
- Generar reporte de cierre auditable.

Stage 2 no incluye:
- Merge.
- Recodificacion.
- Variables derivadas.
- Indicadores.
- Modelos.
- Interpretacion estadistica.
