# Sprint 04.3 — paquete de cierre de automatización shadow

- Fecha: 2026-09-19
- Issue núcleo: [#45](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/45)
- Estado propuesto: `CLOSED; PASS_SUPERVISOR`
- Alcance: `CONTROLLED_SHADOW`
- V0: continúa oficial
- Publicación institucional, acceso público, cutover y sustitución de V0: `NOT_AUTHORIZED`

Este paquete documenta el cierre del Sprint 04.3 conforme a la
[decisión supervisora](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/45#issuecomment-5746144880).
El cierre confirma la automatización de la reconciliación de solo lectura y de la promoción
controlada. No convierte el shadow en una publicación institucional ni amplía el alcance cloud.

## Resultado del sprint

| Bloque | Resultado | Estado |
|---|---|---|
| Pasos 1–4 | decisiones humanas, configuración y entrada privada por corrida | `GOVERNED` |
| Pasos 5–8 | carga idempotente, reconciliación, cinco gates y evidencia redactada | `AUTOMATED; VERIFIED` |
| Pasos 9–11 | autorización humana separada, promoción y verificación del runtime | `AUTOMATED_AFTER_APPROVAL; VERIFIED` |
| Paso 12 | rollback de práctica automatizado | `DEFERRED` |
| Respaldo del paso 12 | `PROMOTE → ROLLBACK_TO_EMPTY → RE_PROMOTE` manual | `PROVEN; OPERATIONAL_BACKUP` |
| Pasos 13–14 | repromoción manual probada y aceptación supervisora | `PROVEN / HUMAN_DECISION` |

No se requiere otra automatización para declarar cerrado este sprint. El paso 12 queda registrado
como trabajo futuro explícito, no como una capacidad automatizada ni como una brecha oculta.

## Evidencia automatizada — pasos 5 a 8

La corrida de reconciliación de solo lectura
[`35421445001`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35421445001)
verificó el snapshot ya autorizado sin promover, cambiar IAM ni mover tráfico:

- 3.014/3.014 filas y 516/516 indicadores;
- release `enares2024-crs04-v0-shadow-001` y run `pr-b-full-v0-authorized-20260916`;
- identidad, manifiesto y hashes autorizados;
- cinco gates técnicos;
- evidencia redactada sin microdatos, credenciales ni identificadores sensibles.

## Evidencia automatizada — pasos 9 a 11

La corrida protegida
[`35475887689`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35475887689)
ejecutó la promoción completa después de la aprobación humana del deployment:

- carga/persistencia reconciliada: 3.014 filas y 516 indicadores;
- paridad de hash: `true`;
- gates de validación: 5/5;
- puntero y vista publicada del shadow actualizados de forma atómica e idempotente;
- Cloud Run con imagen fijada por digest, mínimo 0, máximo 1 y concurrencia 6;
- health autenticado: HTTP 200 y cuerpo `ok`;
- acceso anónimo: HTTP 403;
- principals públicos: 0;
- publicación institucional: `false`;
- cutover: `false`;
- residuos del inbox privado al finalizar: 0.

Los artefactos redactados de la corrida (`bigquery.json`, `runtime.json` y
`workflow-outcome.json`) registran esos resultados sin incluir el agregado privado.

## Rollback de práctica diferido

El workflow automatizado no ejecuta todavía el paso 12. Mientras permanezca diferido, el respaldo
operativo es el mecanismo manual probado en el
[PR #126](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/126):

```text
PROMOTE → ROLLBACK_TO_EMPTY → RE_PROMOTE
```

Ese ejercicio demostró rollback a vacío y restauración exacta del snapshot aprobado, sin
recalcular cifras ni mezclar releases o runs. Automatizarlo en el futuro requerirá conservar la
autorización humana del paso 12 y producir evidencia equivalente; su postergación no autoriza a
omitir el procedimiento manual si un rollback operativo fuera necesario.

## Controles y límites que permanecen vigentes

- V0 continúa como versión oficial; V0.5 y la aplicación permanecen en shadow.
- El servicio exige autenticación y no tiene `allUsers` ni `allAuthenticatedUsers`.
- La aplicación consume solo `published.v_dashboard_current` y no consulta microdatos.
- El cap por consulta continúa en 10 MiB y el objetivo de gasto continúa en USD 0 dentro del
  techo autorizado de USD 20/mes.
- No se autoriza acceso público, publicación institucional, cutover ni sustitución de V0.
- Una futura automatización de rollback o ampliación del alcance requiere un cambio revisado y
  las autorizaciones humanas correspondientes.

## Trazabilidad principal

- [Especificación del pipeline](sprint043_pipeline_specification.md)
- [Contrato de entrada privada](sprint043_stage2_input_contract.md)
- [Gate de reconciliación](sprint043_stage3_reconciliation_gate.md)
- [Promoción protegida](sprint043_stage3_protected_promotion.md)
- [Runbook de promoción y rollback](promotion_rollback_runbook.md)
- [PR #126 — ejercicio manual de promoción y rollback](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/126)
- [PR #142 — corrección final previa a la corrida exitosa](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/142)
- [Decisión supervisora de cierre](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/45#issuecomment-5746144880)

## Decisión de cierre

Rita verificó la promoción automatizada de punta a punta y autorizó cerrar el Sprint 04.3 con el
rollback automatizado diferido. El Issue #45 se cerrará cuando este paquete quede revisado y
fusionado en `main`; el Issue #43 permanece abierto como paraguas de Stage 04.
