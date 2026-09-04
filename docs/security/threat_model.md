# Modelo de amenazas local — Stage 04, corte 3.2

- Estado: `REVIEW_REQUIRED`
- Alcance: `LOCAL_SHADOW_ONLY`
- Datos del ejercicio: totalmente sintéticos
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

## Demostración sintética

La tabla de prueba usa `Total = 100`, `grupo A = 7` y `grupo B = 93`. Ninguna cifra representa
un territorio, grupo o resultado ENARES.

1. Supresión primaria: se oculta A, pero Total y B quedan visibles. Entonces A se reconstruye de
   forma única como `100 - 93 = 7`.
2. Supresión complementaria: también se oculta B. Con dos incógnitas y solo el total, A ya no se
   determina de forma única.
3. La capa published candidata reemplaza estimate, SE, IC95 %, CV y N por NULL para ambas celdas
   suprimidas. La interfaz no recibe el valor oculto.

Los umbrales `CV > 0.15` y `N < 30` permanecen
`PROVISIONAL_REQUIRES_METHODOLOGICAL_APPROVAL`. No son una regla institucional.
