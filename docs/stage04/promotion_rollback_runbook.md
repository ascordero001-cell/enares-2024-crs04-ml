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
4. Actualizar el singleton de `ops.current_release` en una operación controlada.
5. Verificar que `published.v_dashboard_current` contiene únicamente el release/run seleccionado.
6. Ejecutar health, diagnóstico de release y comparación V0 con tolerancia aprobada.
7. Registrar evento, timestamp y evidencia. No borrar la versión anterior.

## Rollback futuro

1. Detener promoción adicional y registrar el síntoma.
2. Identificar el puntero aprobado inmediatamente anterior.
3. Cambiar únicamente `ops.current_release`; no reescribir outputs ni borrar historial.
4. Verificar vista, health, release, acceso y cifras centinela.
5. Registrar actor, motivo y timestamp y abrir el issue correctivo.

Si no existe un puntero anterior aprobado, si las validaciones están incompletas o si la vista
mezcla releases, el procedimiento falla cerrado y requiere intervención. Un ensayo local exitoso
no autoriza la operación cloud.
