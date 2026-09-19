# Runbook local de promoción y rollback

**Estado:** `LOCAL_SHADOW_TESTED`

**Cloud:** `NOT_AUTHORIZED`

Este runbook prueba el contrato operativo sin crear tablas ni cambiar V0. La ejecución real de
Dataform, BigQuery o Cloud Run continúa bloqueada hasta el GO.

## Estados y gates

1. Registrar una combinación nueva `release_id + run_id` en `PENDING`.
2. Registrar una sola vez los controles bloqueantes `technical`, `v0_parity`, `privacy` y
   `release_consistency`.
3. Un fallo cambia la corrida a `FAILED` y es terminal.
4. Solo cuando todos los controles pasan, la corrida cambia a `PASSED`.
5. Una referencia de revisión independiente cambia `PASSED` a `APPROVED`.
6. Solo `APPROVED` puede convertirse en el puntero visible.

`PASSED` no equivale a aprobación y nunca se promueve. El registro y los resultados de validación
son append-only: una corrección produce un `run_id` nuevo.

## Ensayo local

```powershell
python -m pytest tests/test_stage04_promotion_rollback.py -q
dataform compile dataform
```

Los cinco criterios obligatorios son:

- no registrar éxito antes de completar validaciones;
- no sobrescribir el histórico;
- seleccionar únicamente una corrida `APPROVED`;
- cambiar el puntero y restaurar la vista anterior durante rollback;
- no modificar la identidad ni el estado oficial de V0.

## Promoción controlada futura

1. Confirmar GO cloud, actor, motivo, release, run, commit y digest.
2. Confirmar que los cuatro controles y la aprobación pertenecen al mismo release/run.
3. Leer y conservar el puntero actual.
4. Dejar temporalmente la vista en estado vacío (fail closed).
5. Actualizar el singleton de `ops.current_release` en una operación controlada.
6. Volver a crear `published.v_dashboard_current` fijando literalmente el mismo release/run con
   `publishedReleaseId` y `publishedRunId`, sin unir la tabla operativa.
7. Verificar que puntero y vista coinciden y que la vista contiene únicamente el release/run
   seleccionado.
8. Ejecutar health, diagnóstico de release y comparación V0 con tolerancia aprobada.
9. Registrar evento, timestamp y evidencia. No borrar la versión anterior.

La vista consulta una sola tabla física para que cada consulta pueda conservar
`maximum_bytes_billed=10,485,760`. Una unión con `ops.current_release` exige al menos 20 MiB por
los mínimos de facturación de BigQuery y debe fallar el preflight.

## Rollback futuro

1. Detener promoción adicional y registrar el síntoma.
2. Identificar el puntero aprobado inmediatamente anterior.
3. Dejar temporalmente la vista vacía, restaurar `ops.current_release` y volver a crear la vista
   con la combinación aprobada anterior; no reescribir outputs ni borrar historial.
4. Verificar la coincidencia puntero/vista, health, release, acceso y cifras centinela.
5. Registrar actor, motivo y timestamp y abrir el issue correctivo.

Si no existe un puntero anterior aprobado, si las validaciones están incompletas o si la vista
mezcla releases, el procedimiento falla cerrado y requiere intervención. Un ensayo local exitoso
no autoriza la operación cloud.

## Excepción de bootstrap para la primera promoción shadow autenticada

La primera promoción del dataset aislado no tiene un release institucional anterior que pueda
inventarse como destino. En ese único caso, la prueba de rollback restaura el checkpoint previo
real: `current_release` vacío y `published.v_dashboard_current` fijada a los valores fail-closed
`__UNPROMOTED__`, con cero filas. Debe conservar
`outputs` y el registro append-only, anotar el evento `ROLLBACK_TO_EMPTY`, demostrar cero filas
visibles y volver a promover exactamente el mismo release `APPROVED` antes de cerrar la ventana.

Esta excepción no permite crear un release ficticio ni se aplica desde la segunda promoción. Una
vez que exista un puntero aprobado anterior, todo rollback debe restaurarlo y la ausencia de ese
destino vuelve a ser un fallo cerrado.
