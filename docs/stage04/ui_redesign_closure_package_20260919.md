# Stage 04 — paquete de cierre del rediseño UI Streamlit

- Fecha UTC: 2026-09-20
- Issue: [#144](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/144)
- Estado solicitado: `PASS_SUPERVISOR`
- Alcance: `CONTROLLED_SHADOW`

## Trazabilidad por etapa

| Etapa | Evidencia | Decisión |
|---|---|---|
| 0–1 | [PR #145](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/145), merge `a65945dff855d3af21db0314f2a30c5150dc1bcf` | especificación y arquitectura aprobadas |
| 2 | [PR #146](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/146), head `ec42155cf38aafb6a10d0d1b33571c26366585fe`, merge `9eab462ae71699b196f89beb0e950d2c008daef1` | estructura sintética aprobada |
| 3 | [PR #147](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/147), head `a9c71e1c3403f74d476b0a929797cd66d7345c2d`, merge `322fc46784d5e3f4928f62b4d2aa21e52dc2781b` | conexión real y paridad golden aprobadas |

## Evidencia ejecutable final

La revisión del PR #147 verificó `516 passed, 2 skipped`, Ruff y mypy limpios, y doce checks en
verde. Después del merge, `main` volvió a ejecutar satisfactoriamente:

- [CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044749);
- [App CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044740);
- [Container CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044741);
- [Authenticated shadow cloud image](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044736);
- [Security CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044778);
- [Documented quickstart CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35484044785).

La prueba `tests/test_stage04_ui_redesign_real.py` demuestra que la tarjeta mostrada para
`3.2 / VF_HOGAR / Nacional / Total` coincide campo por campo con el golden existente. Los valores
visibles siguen siendo 16.74 %, EE 0.5115, CV 0.03055 y N no ponderado 18,807. No son cifras nuevas
ni fueron recalculadas por la interfaz.

## Controles conservados

- La lectura real reutiliza `configured_repositories()` y los repositorios existentes.
- Las opciones de filtro proceden únicamente de filas autorizadas y validadas.
- Las combinaciones ausentes no producen ceros ni valores fabricados.
- CV, N y supresión permanecen independientes.
- No hubo cambios en IAM, credenciales, workflows, Cloud Run, recursos o exportación.
- No existe búsqueda individual ni exposición de microdatos.
- V0 continúa oficial; acceso público, publicación institucional, cutover y sustitución de V0
  permanecen `NOT_AUTHORIZED`.

## Decisión solicitada

Se solicita confirmar `PASS_SUPERVISOR` para el bloque de rediseño y cerrar únicamente el Issue
#144. El Issue paraguas #43 permanece abierto y el resultado continúa limitado a
`CONTROLLED_SHADOW`.
