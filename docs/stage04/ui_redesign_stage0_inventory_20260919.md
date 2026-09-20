# Rediseño UI — inventario de Etapa 0

- Commit base: `5660e6df23141b313b6f3281f5349668a709eeb4`
- PR base: #143 fusionado
- Datos e infraestructura: sin cambios
- Resultado: `READY_FOR_STAGE1_REVIEW`

## Superficie Streamlit existente

| Componente | Ruta ejecutable | Estado actual |
|---|---|---|
| Entrada principal | `app/streamlit_app.py::render` | una app multipágina controlada por navegación lateral |
| Navegación | `app.config.NAVIGATION` + `st.sidebar.radio` | Resumen, módulos 3.1–3.6, Metodología y Estado del release |
| Dimensión | `app.config.FUTURE_DIMENSIONS` + `st.sidebar.selectbox` | nueve dimensiones de presentación; combinaciones ausentes fallan cerradas |
| Fuente | `configured_repositories()` | local autorizado o shadow autenticado; modos desconocidos se rechazan |
| Lectura cloud | `BigQueryRepository` | tabla configurada como `published.v_dashboard_current`, release/run fijos y cap de bytes |
| Validación | `load_validated_estimates()` → `validate_estimates()` | toda fila se valida antes de filtrar o mostrar |
| Autorización | registro de módulos y `authorized_scopes.py` | la UI no crea cruces ni categorías |
| Calidad | `quality_rules.py` y flags persistidos | CV y N son alertas visibles; supresión es independiente |
| Tarjeta numérica | `_numeric_summary()` + `build_numeric_card()` | estimación, EE, CV, N e IC95 % |
| Estados sintéticos | `_validated_state_gallery()` | candidato, referencial y ejercicio suprimido |
| Resultados | selectores de indicador/categoría | no hay todavía `st.tabs`, `st.dataframe` ni forest plot |
| Exportación | `_download_cut()` | CSV/Excel agregado, gobernado por `EXPORT_ENABLED` |
| Seguridad HTML | `_styles()` y `escape_dynamic_text()` | HTML inseguro limitado a CSS estático; texto dinámico escapado |
| Pruebas UI | `tests/test_stage04_local_app.py`, `tests/test_stage04_ui_guards.py` | AppTest, golden, estados, errores genéricos y controles de seguridad |

## Flujo de datos que se reutiliza

```text
published.v_dashboard_current
  → BigQueryRepository(release_id, run_id, maximum_bytes_billed)
  → load_validated_estimates
  → validate_estimates + assert_v0_granularity_boundary
  → helpers puros de presentación
  → componentes Streamlit
```

En modo local, `AuthorizedAggregateRepository` sustituye únicamente el transporte y conserva las
mismas barreras de manifiesto, SHA-256, registro aprobado y validación. `DemoRepository` acepta
solo filas `synthetic=true`.

## Confirmación de infraestructura

El rediseño no necesita conexión, credencial, permiso IAM, dataset, bucket, servicio o deployment
nuevo. Reutilizará exactamente el runtime autenticado y las rutas existentes. Esta es la propuesta
de Ana para confirmación supervisora; no se realizará ninguna mutación cloud en este bloque.

