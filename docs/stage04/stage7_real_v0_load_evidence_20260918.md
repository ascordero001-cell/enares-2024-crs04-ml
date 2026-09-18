# Evidencia de carga V0 real — Decisión B — 2026-09-18

**Estado:** `LOAD_AND_RECONCILIATION_PASS; PROMOTION_NOT_EXECUTED`

**Autorización:** `APPROVE_B_REAL_V0_CLOUD_EXECUTION`, revisión formal del PR #120 y
[confirmación en el Issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5736519265).

Los identificadores de jobs, principales exactos y enlaces privados permanecen en BigQuery Job
History y en el registro custodio. No se versionan tokens, correos ni IDs internos.

## Preflight

- SHA-256 del extracto coincidió con el manifiesto aprobado.
- Filas: `3.014/3.014`; indicadores: `516/516`.
- Un solo `release_id` y un solo `run_id`.
- `synthetic=false` en todas las filas.
- Los tres datasets aislados estaban vacíos y la tabla destino no existía.

## Carga

| Fecha UTC | Destino lógico | Resultado |
|---|---|---|
| 2026-09-18T22:43:10.996Z | `stage04_shadow_outputs.indicator_estimates` | `DONE; 3.014 FILAS; 1.601.976 BYTES` |

Solo se creó esa tabla. Los datasets aislados `published` y `ops` permanecieron vacíos. Los
datasets preexistentes conservaron sus conteos anteriores de una y 32 tablas y no fueron
modificados.

## Primera consulta real de reconciliación

| Control | Resultado |
|---|---|
| Fecha UTC | `2026-09-18T22:43:47.827Z` |
| Estado | `DONE / SUCCESS` |
| `maximum_bytes_billed` | `10.485.760` |
| Bytes procesados | `105.020` |
| Total | 3.014 filas / 516 indicadores |
| 3.1 | 1.170 filas / 100 indicadores |
| 3.2 | 389 / 28 |
| 3.3 | 123 / 29 |
| 3.4 | 749 / 212 |
| 3.5 | 457 / 21 |
| 3.6 | 126 / 126 |
| `synthetic=true` | 0 |
| Estado distinto de `APPROVED` | 0 |
| `suppress_flag=true` | 0 |

## Paridad completa

Se compararon los 31 campos de las 3.014 filas con el CSV autorizado. Resultado:

- `3.014/3.014 MATCH`;
- cero faltantes y cero extras;
- cero diferencias con tolerancia numérica `1e-9`;
- todas las consultas con bytes procesados aplicaron el cap de 10 MiB;
- bytes totales de reconciliación: `3.308.972`, por debajo de la cuota diaria de 1 GiB.

Una comprobación intermedia detectó diferencias de codificación de salida y conversión del
timestamp en el cliente local. Se aplicó la condición de parada, se diagnosticó sin mutar cloud y
la comparación se repitió preservando Windows-1252 y normalizando el timestamp ISO. No fue una
discrepancia de datos. Una consulta sintácticamente inválida procesó cero bytes y no mutó datos.

## Límite del checkpoint

No se creó ninguna vista o tabla en `published`, no se escribió `ops`, no se conectó
`BigQueryRepository` y Cloud Run continúa sirviendo únicamente el fixture sintético. No hubo
acceso público, publicación, cutover ni sustitución de V0. La promoción requiere un paso posterior
con revisión de esta evidencia.
