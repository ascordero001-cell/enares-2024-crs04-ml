# Preflight de coste de la vista autenticada — 2026-09-18

## Resultado

`BLOCKED_BEFORE_PROMOTION`

La imagen cloud aprobada fue construida en `main`, inspeccionada y cargada en el Artifact
Registry existente. Antes de mover `ops.current_release`, el preflight creó las tablas operativas
vacías y compiló la vista aprobada en el PR #124. No se desplegó una revisión ni se expusieron
filas en `published`.

La consulta mínima a la vista original fue rechazada con
`maximum_bytes_billed=10,485,760`: el plan necesita 20 MiB porque lee dos tablas físicas,
`outputs.indicator_estimates` y `ops.current_release`. BigQuery aplica un mínimo de 10 MiB por
tabla consultada. Aumentar el límite contradiría el control de coste aprobado.

## Corrección fail-closed

La vista fija el `release_id + run_id` aprobado mediante variables de despliegue y lee una sola
tabla física. Los valores por defecto son `__UNPROMOTED__`, por lo que una compilación sin
parámetros muestra cero filas. Promoción y rollback verifican como un par:

1. el singleton auditable en `ops.current_release`;
2. la combinación literal de la vista;
3. la identidad de todas las filas visibles;
4. el límite de 10 MiB en cada consulta.

La transición deja primero la vista vacía. Si cualquier paso falla, la aplicación no ve una
mezcla de releases. `outputs` y los registros append-only no se reescriben.

## Estado conservado

- `outputs`: 3.014 filas y 516 indicadores, sin cambios;
- `current_release`: vacío;
- filas visibles en `published`: cero por construcción;
- Cloud Run: continúa en la revisión sintética autenticada anterior;
- acceso público, publicación institucional y cutover: no autorizados.
