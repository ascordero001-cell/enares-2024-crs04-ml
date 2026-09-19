# Auditoría de afirmaciones de control ejecutables

- Fecha inicial: 2026-09-15
- Última ampliación: 2026-09-19
- Alcance: controles transversales de Stage 04
- Estado: `PASS`
- Cloud: `CONTROLLED_SHADOW`; acceso público, publicación y cutover `NOT_AUTHORIZED`

La auditoría contrasta lo que los documentos y PR afirman con las rutas que realmente ejecutan la
aplicación y CI. No modifica cifras, hashes, reglas estadísticas, granularidad ni alcance cloud.

| Control histórico | Ruta ejecutable | Prueba negativa o cierre | Resultado |
| --- | --- | --- | --- |
| Diagnóstico de release sobre el catálogo completo | `scripts/release_diagnostic.py` reúne todos los `release_id` de los extractos autorizados | `test_release_diagnostic_fails_closed_on_multiple_authorized_release_ids` y `test_all_authorized_extracts_share_the_golden_release_id` | Conectado |
| Marcador `[referencial]` derivado de `cv_flag` | UI: `precision_category_label`; exportación: `_export_category` | `test_reference_marker_is_derived_exclusively_from_cv_flag` cubre verdadero y falso | Conectado |
| Dominancia | La política declara que V0 no contiene campo, cálculo ni señal de dominancia | La maquinaria no se presenta como regla activa y requiere un nuevo gate para activarse | Inactivo explícitamente |
| Tipos entre módulos | `mypy.ini` usa `follow_imports = normal` globalmente | `test_stage04_engineering_hygiene.py`; el `skip` queda limitado y explicado para `scripts.*` heredados | Conectado |
| Residual de accesibilidad | El job WCAG audita nueve vistas y reconoce solo la firma exacta de Streamlit 1.63.0 | El contador ahora debe ser exactamente 9; pruebas negativas con 8 y 10 rompen el control | Corregido en esta rama |
| Límite de granularidad V0 | `validate_estimates` llama `assert_v0_granularity_boundary` para cada fila antes de UI/exportación | Pruebas con dimensión, cruce y par matricial no autorizados | Conectado |
| Procedencia institucional | `AuthorizedAggregateRepository` deriva `synthetic=false` después de verificar manifiesto, SHA-256 y registro | Faltantes, duplicados y orígenes no autorizados fallan cerrados | Conectado |
| Identidad reservada | Aserción Dataform `stage04_reserved_release_identity` | `UNPROMOTED` y `__UNPROMOTED__` no pueden presentarse como release/run real | Conectado |
| Límite de consulta | El repositorio BigQuery fija `maximum_bytes_billed`; la vista publicada usa una sola tabla | Consulta real observada por debajo de 10 MiB; el preflight más costoso falla antes de ejecutarse | Conectado |
| Privilegio mínimo | Runtime con `bigquery.jobUser`, `READER` en `published` y vista autorizada | 0 roles de datos a nivel proyecto, 0 ACL directa en `outputs`, 0 principals públicos | Conectado |
| Promoción y rollback | Lifecycle, cache por release/run y runbook ejecutado | `PROMOTE → ROLLBACK_TO_EMPTY → RE_PROMOTE` sin mezcla de snapshots | Conectado |

## Corrección realizada

El job WCAG contaba el residual conocido del sidebar, pero no afirmaba su cardinalidad. Eso permitía
que el mismo defecto apareciera en más nodos o que se dejaran de auditar vistas sin romper CI. La
política queda aislada en una función pura: solo acepta exactamente nueve ocurrencias, una por cada
vista congelada. La excepción está ligada expresamente a Streamlit 1.63.0 y debe revisarse antes de
cambiar esa versión.

## Resultado

Después de la ampliación posterior a la promoción, ninguna afirmación auditada depende únicamente
de texto o registro manual: o bien se ejecuta y falla de forma cerrada, o bien está declarada
explícitamente inactiva sin presentarse como protección vigente. La configuración IAM/ACL fue
contrastada contra el servicio y los datasets vivos; los identificadores del principal permanecen
redactados del repositorio público.
