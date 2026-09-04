# Contrato local de la vista `published`

- Estado: `CANDIDATE_LOCAL_SHADOW`
- Cloud: `BLOCKED_BY_CLOUD_GATE`

`published` es la única superficie que una aplicación puede leer. Contiene exclusivamente
resultados agregados que pertenecen a un release `APPROVED`; nunca contiene microdatos,
identificadores personales, variables de diseño ni rutas a fuentes privadas.

## Reglas

1. `current_release` debe apuntar a un release `APPROVED` antes de exponerlo.
2. Cada fila conserva `release_id`, versión de fuente, estado y notas de calidad.
3. Una celda suprimida mantiene su etiqueta y estado, pero expone como NULL `estimate`,
   `standard_error`, `ci95_lower`, `ci95_upper`, `cv`, `n_unweighted` y
   `weighted_population`.
4. La supresión se materializa en la capa published candidata; no puede ser solo visual.
5. No se publican combinaciones ausentes del catálogo ni filas con `FAILED`.
6. La aplicación no abre CSV privados, Drive ni `survey_input`.

## Proyección segura mínima

`release_id`, `source_version`, `indicator_id`, `indicator_name`, `disaggregation`, `category`,
campos estadísticos protegidos, flags, `quality_note`, `validation_status` y `created_at`.

La creación de una vista real en BigQuery permanece `BLOCKED_BY_CLOUD_GATE`.
