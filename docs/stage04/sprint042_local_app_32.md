# Sprint 04.2-A — aplicación local segura para el módulo 3.2

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

La aplicación no abre `.sav`, microdatos, Drive, fuentes privadas de Stage 03 ni permite buscar
NNA individuales. `AuthorizedAggregateRepository` comprueba el manifiesto y el hash aprobado;
`DemoRepository` acepta únicamente filas marcadas como sintéticas.

## Evidencia visual segura

Las capturas no contienen rutas personales, tokens, credenciales ni observaciones individuales.

- Resumen nacional: [sprint042_summary.png](evidence/sprint042_summary.png)
- Módulo 3.2 con agregado V0: [sprint042_module32.png](evidence/sprint042_module32.png)
- Estados sintéticos, incluida la celda suprimida: [sprint042_suppressed.png](evidence/sprint042_suppressed.png)

La celda `SUPPRESSED_EXERCISE` no recibe estimate, error estándar, IC95 %, CV, N no ponderado ni
`weighted_population`. La exportación permanece deshabilitada.

## Verificación

```text
python -m pytest -q
160 passed

git diff --check
sin salida
```

Las pruebas cubren el inicio de Streamlit, inyección por `IndicatorRepository`, coincidencia de la
tarjeta 3.2 con el golden, presencia de estadísticos autorizados, nulificación de campos
protegidos, etiquetas diferenciadas, filtros sin datos, release SHADOW, exportación deshabilitada
y bloqueo explícito de `BigQueryRepository`.

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
- BigQuery, DDL, Cloud Run, IAM, buckets, facturación y despliegue siguen
  `BLOCKED_BY_CLOUD_GATE`.
