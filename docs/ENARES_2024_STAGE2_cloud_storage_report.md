# ENARES 2024 CRS04 - Stage 2 Cloud Storage Report

Fecha de ejecucion: 2026-06-18T02:01:10.875306+00:00

Google Cloud project_id: `enares-2024-crs04`

Cuenta operativa esperada: `anacordero.001@gmail.com`

## Decision

Stage 2 pass: `True`

## Validaciones automaticas

| Validacion | Resultado |
|---|---:|
| Rowcount .sav vs BigQuery | `True` |
| Schema / column count validation | `True` |
| Metadata preservation | `True` |
| BigQuery datasets created or verified | `True` |
| Source files found in Drive | `True` |

## Datasets BigQuery

| dataset_id                  | location   | status            |
|:----------------------------|:-----------|:------------------|
| enares2024_crs04_raw        | US         | created_or_exists |
| enares2024_crs04_cleaned    | US         | created_or_exists |
| enares2024_crs04_analytical | US         | created_or_exists |

## Archivos fuente CRS04

| chapter   | source_file         | target_table     | file_exists   |   file_size_bytes |
|:----------|:--------------------|:-----------------|:--------------|------------------:|
| CAP100    | 19_CRS04_CAP100.sav | raw_crs04_cap100 | True          |          15327888 |
| CAP200    | 20_CRS04_CAP200.sav | raw_crs04_cap200 | True          |          14731025 |
| CAP248    | 21_CRS04_CAP248.sav | raw_crs04_cap248 | True          |          16100226 |
| CAP300    | 22_CRS04_CAP300.sav | raw_crs04_cap300 | True          |           5707643 |

## Tablas raw cargadas

| source_file         | chapter   | target_table     |   sav_rows |   sav_columns |   bq_rows |   bq_columns |
|:--------------------|:----------|:-----------------|-----------:|--------------:|----------:|-------------:|
| 19_CRS04_CAP100.sav | CAP100    | raw_crs04_cap100 |      18807 |           147 |     18807 |          147 |
| 20_CRS04_CAP200.sav | CAP200    | raw_crs04_cap200 |      18807 |           523 |     18807 |          523 |
| 21_CRS04_CAP248.sav | CAP248    | raw_crs04_cap248 |      18807 |           578 |     18807 |          578 |
| 22_CRS04_CAP300.sav | CAP300    | raw_crs04_cap300 |      18807 |            51 |     18807 |           51 |

## Metadata preservada

| table_name                   |   row_count |   column_count |
|:-----------------------------|------------:|---------------:|
| metadata_crs04_variables     |        1299 |              6 |
| metadata_crs04_value_labels  |        3317 |              7 |
| metadata_crs04_missing_codes |           0 |              9 |
| metadata_crs04_source_files  |           4 |             21 |

## Outputs obligatorios usados

- `ENARES_2024_STAGE2_bigquery_dataset_registry.csv`
- `ENARES_2024_STAGE2_crs04_bigquery_table_mapping.csv`
- `ENARES_2024_STAGE2_source_file_check.csv`
- `ENARES_2024_STAGE2_raw_table_inventory.csv`
- `ENARES_2024_STAGE2_rowcount_validation.csv`
- `ENARES_2024_STAGE2_schema_validation.csv`
- `ENARES_2024_STAGE2_metadata_inventory.csv`

## Limite metodologico Stage 2

En Stage 2 no se hizo merge, no se recodificaron variables, no se crearon outcomes, no se construyeron variables derivadas, no se calcularon indicadores y no se interpreto ningun resultado estadistico.

La capa producida es raw, trazable, completa y auditable en BigQuery.

## Pendientes para Fase 03

- Validar llave de merge: `ID`, `COLEGIAL_ID`, `ID + COLEGIAL_ID` u otra llave documentada en metadata.
- Revisar duplicados, no matches y cardinalidad antes de crear `cleaned_crs04_merged_adolescents`.
- Si `ID`, `COLEGIAL_ID` u otra llave llega como `FLOAT64`, verificar que no existan decimales reales antes de convertir a `INT64`.
- Traducir y preservar el diseno muestral complejo: `CCDD` como estrato, `ID`/colegio como UPM, `ID_AULA`/seccion como USM y peso muestral oficial.
- Verificar variables con prefijo `C3` dentro de CRS04 como items comunes CRS03/CRS04 antes de usarlas en variables derivadas.

## Decision final

Decision Stage 2: `Aprobado`

