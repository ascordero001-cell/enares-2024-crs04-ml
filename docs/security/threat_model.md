# Modelo de amenazas local — Stage 04, corte 3.2

- Estado: `REVIEW_REQUIRED`
- Alcance: `LOCAL_SHADOW_ONLY`
- Entradas locales: fixture demo 100 % sintético y corte golden V0 agregado autorizado, separados
- Cloud: `NOT_AUTHORIZED`

## Amenazas y controles

| Elemento | Evaluación |
|---|---|
| Activo protegido | Confidencialidad de NNA y de celdas agregadas que puedan revelar grupos pequeños |
| Posible atacante | Persona con acceso a una pantalla, export o log que intenta deducir una celda oculta |
| Vía de exposición | Totales y márgenes visibles, cruces repetidos, exports, mensajes de error, caché o logs |
| Reconstrucción por totales | Si `Total = A + B`, ocultar solo A permite calcular `A = Total - B` |
| Inferencia mediante cruces | Distintas tablas compatibles pueden formar ecuaciones adicionales sobre la misma celda |
| Enlace externo | Categorías demasiado específicas podrían combinarse con fuentes externas |
| Logs, errores, caché y exports | Pueden filtrar valores anteriores a la supresión si el control es solo visual |
| Control preventivo | Aplicar supresión primaria y complementaria en published; eliminar estimate, IC, CV y N antes de cualquier consumidor |
| Control de detección | Test de reconstrucción, revisión de schema, auditoría de exports y registro de release |
| Riesgo residual | Más de un cruce o release podría permitir inferencia aun con una tabla aislada protegida |
| Decisión pendiente | Aprobar propietario, regla institucional, umbrales y análisis multitabla/multirelease |

El agregado golden V0 no contiene observaciones individuales y se valida contra un manifiesto
separado. No es una publicación institucional. BigQuery, DDL, Cloud Run y cualquier otro recurso
cloud continúan `BLOCKED_BY_CLOUD_GATE`.

## Estado de verificación

| Riesgo o control | Estado de evidencia |
|---|---|
| Reconstrucción aditiva simple `Total = A + B` | `TEST_AUTOMATIZADO` |
| Cruces entre tablas o múltiples releases | `RIESGO_DOCUMENTADO_TEST_PENDIENTE` |
| Enlace con fuentes externas | `RIESGO_DOCUMENTADO_TEST_PENDIENTE` |
| Logs, errores, caché y exports | `CONTROLES_ESPECIFICADOS_PRUEBA_DE_INTEGRACION_PENDIENTE` |

Solo la reconstrucción aditiva simple y la nulificación de campos en la proyección local cuentan
como pruebas automatizadas en este subbloque. Los demás elementos son riesgos o controles
documentados y no se presentan como verificados experimentalmente.

## Demostración sintética

La tabla de prueba usa `Total = 100`, `grupo A = 7` y `grupo B = 93`. Ninguna cifra representa
un territorio, grupo o resultado ENARES.

1. Supresión primaria: se oculta A, pero Total y B quedan visibles. Entonces A se reconstruye de
   forma única como `100 - 93 = 7`.
2. Supresión complementaria: también se oculta B. Con dos incógnitas y solo el total, A ya no se
   determina de forma única.
3. La capa published candidata reemplaza estimate, SE, IC95 %, CV y N por NULL para ambas celdas
   suprimidas. La interfaz no recibe el valor oculto.

Desde la decisión supervisora del 2026-09-13, `CV > 15 %` y `base_unw < 30` son alertas de
calidad visibles para 3.1–3.6. No activan `suppress_flag` ni sustituyen los controles de
confidencialidad descritos aquí.
