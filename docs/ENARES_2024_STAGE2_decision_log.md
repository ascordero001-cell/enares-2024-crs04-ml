# ENARES 2024 CRS04 - Stage 2 Decision Log

Fecha: 2026-05-30T08:32:36.689105+00:00

## Decision 1

Stage 2 solo carga, preserva y valida la capa raw.

## Motivo

La separacion `raw` / `cleaned` / `analytical` evita mezclar almacenamiento, limpieza estructural y analisis.

## Decision 2

No se ejecuta merge en Stage 2.

## Motivo

La llave de merge debe investigarse y demostrarse con evidencia en Stage 3.

## Hipotesis pendientes para Stage 3

- `COLEGIAL_ID`
- `ID`
- `ID + COLEGIAL_ID`
- Otra llave identificadora documentada en metadata

## Nota tecnica

Si `ID`, `COLEGIAL_ID` u otra llave llega como `FLOAT64`, se debe verificar que no existan decimales reales antes de convertir a `INT64`.

SPSS requiere `SORT CASES` antes de `MATCH FILES`; BigQuery no requiere ordenar antes de un `JOIN` porque SQL une por valores de llave, no por posicion.
