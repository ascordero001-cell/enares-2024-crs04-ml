# PUERTA 04.2-A — shell local 3.2 listo para revisión

- Alcance: `LOCAL_SHADOW_ONLY`
- Cloud: `NOT_AUTHORIZED`
- Presupuesto: `USD 0`
- Módulos implementados: resumen nacional y 3.2
- Módulos pendientes: 3.1 y 3.3–3.6
- Publicación y exportación: no autorizadas

## Ejecución local

```text
python -m streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

- Python: `3.14.7`
- Streamlit: `1.63.0`
- Acceso: exclusivamente local en `127.0.0.1`
- Datos: fixture demo 100 % sintético y un agregado V0 autorizado mediante la interfaz
  `IndicatorRepository`.

La PUERTA 04.2-A acredita únicamente el shell local de resumen nacional y módulo 3.2. No constituye
el cierre completo de Sprint 04.2.

La aplicación no abre `.sav`, microdatos, Drive, fuentes privadas de Stage 03 ni permite buscar
NNA individuales. `AuthorizedAggregateRepository` comprueba el manifiesto y el hash aprobado;
`DemoRepository` acepta únicamente filas marcadas como sintéticas.

## Barreras antes de la interfaz

Toda lectura pasa por `load_validated_estimates()`, que ejecuta `validate_estimates()` antes de
filtrar o construir cualquier tarjeta. `build_numeric_card()` y `build_suppressed_card()` vuelven a
validar la fila como defensa adicional. Se bloquean hash de fuente inválido, estado `FAILED`, escala
desconocida, estimate fuera de escala, SE/CV/N negativos, IC95 % incoherente y cualquier combinación
inconsistente entre `quality_status`, `suppress_flag` y campos estadísticos protegidos. Un catálogo
vacío conserva el significado “sin datos” y nunca fabrica resultados.

Los valores textuales procedentes de los repositorios se convierten en contenido inerte mediante
`html.escape(..., quote=True)`. La aplicación usa componentes nativos de Streamlit para títulos,
tarjetas, avisos y detalle; `unsafe_allow_html=True` queda limitado a CSS completamente estático.

`.streamlit/config.toml` fija `toolbarMode = "viewer"` para ocultar opciones de desarrollo y
despliegue, `disableDataExport = true` para retirar controles incorporados de exportación y
`showErrorDetails = "none"` para no exponer detalles internos. Estas defensas complementan, pero no
sustituyen, la validación estadística y la supresión previa a la UI. `EXPORT_ENABLED = False`
permanece como control explícito de la aplicación.

## Evidencia visual segura

Las capturas no contienen rutas personales, tokens, credenciales ni observaciones individuales.

- Resumen nacional: [sprint042_summary.png](evidence/sprint042_summary.png)
- Módulo 3.2 con agregado V0: [sprint042_module32.png](evidence/sprint042_module32.png)
- Estados sintéticos, incluida la celda suprimida: [sprint042_suppressed.png](evidence/sprint042_suppressed.png)
- Filtro sin datos, sin cifras fabricadas: [sprint042_no_data.png](evidence/sprint042_no_data.png)

La celda `SUPPRESSED_EXERCISE` no recibe estimate, error estándar, IC95 %, CV, N no ponderado ni
`weighted_population`. La exportación permanece deshabilitada.

## Verificación

```text
python -m pytest -q
resultado registrado en el comentario del SHA revisable

git diff --check
sin salida
```

Las pruebas AppTest cubren el comportamiento visible del resumen, módulo 3.2, golden, tres estados
demo, filtro sin datos, release SHADOW, controles locales, exportación deshabilitada, sentinel HTML
escapado y rechazo de resultados estadísticamente inválidos. Las pruebas negativas bloquean SE,
CV y N negativos, escala o estimate inválidos, IC95 % inconsistente, hash inválido, `FAILED` y
supresión incoherente. `BigQueryRepository` continúa bloqueado explícitamente.

## Aprendizaje

`SHADOW` significa que el artefacto puede evaluarse localmente sin convertirse en fuente oficial.
`APPROVED` implica que una revisión independiente aceptó un artefacto y un SHA concretos para el
alcance declarado. `PUBLISHED` sería una exposición institucional a consumidores y exige otro
gate: responsables, privacidad integral, rollback, presupuesto, IAM e infraestructura autorizada.
La aprobación local no implica publicación.

## Riesgos y decisiones pendientes

- Los umbrales `CV > 0.15`, `N < 30` y la tolerancia golden `1e-9` no son política institucional.
- Cruces multitabla/multirelease, enlace externo y pruebas de integración de logs, caché y exports
  permanecen pendientes.
- Los módulos 3.1 y 3.3–3.6, las nueve dimensiones completas, exportación, promoción y rollback
  permanecen pendientes fuera de esta puerta.
- BigQuery, DDL, Cloud Run, IAM, buckets, facturación y despliegue siguen
  `BLOCKED_BY_CLOUD_GATE`.
