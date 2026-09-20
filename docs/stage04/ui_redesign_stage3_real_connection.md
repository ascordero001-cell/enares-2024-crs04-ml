# Rediseño UI — Etapa 3, conexión autorizada

- Issue: #144
- Alcance: conexión del layout aprobado al adaptador existente
- Estado: `APPROVED_AND_MERGED`
- PR: #147
- Head aprobado: `a9c71e1c3403f74d476b0a929797cd66d7345c2d`
- Merge SHA: `322fc46784d5e3f4928f62b4d2aa21e52dc2781b`

## Ruta ejecutable

`app/ui_redesign_app.py` obtiene el repositorio mediante `configured_repositories()`. En local usa
`AuthorizedAggregateRepository`; en shadow autenticado conserva `BigQueryRepository` sobre la
tabla `published.v_dashboard_current` ya configurada. No existe una consulta, credencial o ruta de
lectura nueva.

`app/views/ui_redesign_real.py` carga 3.1–3.6 mediante `load_validated_estimates`, rechaza cualquier
fila que no haya sido clasificada por la verificación de procedencia y deriva módulo, dimensión,
indicador, categoría y estados exclusivamente de esas filas.

## Paridad golden

La selección inicial es `3.2 / VF_HOGAR / Nacional / Total`. La tarjeta usa directamente
`build_numeric_card`, el adaptador vigente, y se compara campo por campo con
`tests/golden/stage04_32_national/expected_card_view_model.json`.

La prueba AppTest confirma además los cuatro valores visibles:

- estimación: `16.74 %`;
- error estándar: `EE 0.5115`;
- CV: `0.03055`;
- N no ponderado: `18,807`.

## Límites conservados

- No se recalcula Stage 03.
- No se fabrica una combinación ausente.
- CV y N permanecen visibles como señales independientes.
- Un estado suprimido o de contexto nunca entrega estadísticas a tabla, tarjeta o forest plot.
- Sin cambios en IAM, autenticación, workflows, Cloud Run, recursos o exportación.
- V0 continúa oficial; publicación, acceso público y cutover siguen `NOT_AUTHORIZED`.
