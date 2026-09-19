# Registro de autorización cloud — Stage 04

**Decisión histórica:** Rita, 2026-09-13

**Aclaración operativa:** Ana, 2026-09-17

**Estado:** `AUTHENTICATED_SHADOW_PROMOTION_EXECUTED_PASS`
**Alcance vigente:** `CONTROLLED_SHADOW; REAL_V0_IN_PUBLISHED`

| Campo | Estado verificable |
|---|---|
| Modelo de coste | Presupuesto PEN 67, equivalente conservador inferior a USD 20; gasto objetivo USD 0 |
| Propiedad y operación | Ana; propietaria del proyecto y titular de la cuenta de facturación |
| Supervisión | Rita; lectura de Cloud Run, Logging y Monitoring, sin propiedad ni administración de billing |
| Proyecto | `enares-2024-crs04`; existencia y coincidencia verificadas privadamente |
| Ubicaciones verificadas | BigQuery `US`; Cloud Run y Artifact Registry `us-central1` |
| Billing | Responsable: Ana; vínculo efectivo verificado privadamente, sin publicar identificadores |
| IAM | Los tres roles de lectura de Rita fueron aplicados; presencia y acceso efectivo confirmados privadamente |
| Recursos ejecutados bajo Decisión A | Tres datasets aislados y vacíos, identidad sin llaves, repositorio Docker inmutable y Cloud Run autenticado |
| Datos ejecutados | 3.014 filas V0 cargadas, reconciliadas, promovidas y verificadas en `published`; registro y gates en `ops` |
| Acceso | Ana y Rita verificadas con invocación autenticada; cuatro reservas retiradas formalmente para este cierre; principales exactos solo por canal privado |
| Parada | Política aprobada: Ana ejecuta y Rita supervisa; prueba efectiva solo después del GO |
| Decisión técnica | Promoción, rollback al checkpoint vacío, re-promoción y conexión autenticada ejecutadas en PASS |

Antes de cualquier primer despliegue deben verificarse identidades, roles, alertas USD 1/5/10/20,
`maximum_bytes_billed` en cada consulta, cuota diaria
personalizada de BigQuery, mínimo cero y máximo una instancia, limpieza de Artifact Registry,
acceso positivo y negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son
un tope automático; el objetivo de gasto es USD 0 y el techo de contingencia es USD 20.

La ejecución B utilizó los tres datasets aislados existentes. No añadió cuentas, bindings IAM de
principals, datasets, buckets ni servicios. `published.v_dashboard_current` fue registrada como
authorized view sobre `outputs`, sin conceder lectura directa de `outputs` al runtime.

La solicitud operativa de los pasos 40–41, con alcance mínimo, IAM propuesto, controles de coste,
rollback y campos bloqueantes, está en [cloud_go_request.md](cloud_go_request.md). El GO del
2026-09-14 continúa vigente. Proyecto, vínculo, presupuesto, umbrales, canal y bindings ya están
configurados. Rita confirmó privadamente recepción y acceso efectivo en la
[revisión del PR #116](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/116#pullrequestreview-5243890667).
La Decisión A fue aprobada en el PR #117 y la variante aislada de datasets fue aprobada en el
[Issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5724979721).
El paso 43 fue ejecutado sin datos reales. La decisión supervisora del 2026-09-18 resolvió
`VF_ESCUELA`, las alertas universales sin supresión y el HOLD de D06/D07. Rita autorizó la
Decisión B en el PR #120; las 3.014 filas fueron cargadas y reconciliadas en `outputs`. La promoción
a `published` y la conexión autenticada de Cloud Run fueron autorizadas después en los PR #123,
#124 y #125, y ejecutadas en PASS el 2026-09-19.

Véase [zero_spend_target_20260917.md](zero_spend_target_20260917.md).
La configuración redactada está en
[cloud_budget_verification_20260917.md](cloud_budget_verification_20260917.md).
La decisión y su ejecución se registran en
[step47_cloud_execution_request.md](step47_cloud_execution_request.md).
La ejecución redactada se registra en
[stage7_synthetic_execution_evidence_20260918.md](stage7_synthetic_execution_evidence_20260918.md).
La primera carga real se registra en
[stage7_real_v0_load_evidence_20260918.md](stage7_real_v0_load_evidence_20260918.md).
La promoción autenticada, rollback y primera consulta real se registran en
[stage7_authenticated_shadow_promotion_evidence_20260919.md](stage7_authenticated_shadow_promotion_evidence_20260919.md).

Rita no administra la cuenta ni puede detener el gasto directamente. Sus controles son
`CODEOWNERS`, los gates de los pasos 47/53 y la visibilidad de ejecución y alertas. Antes de una
entrega institucional debe resolverse una titularidad institucional para proyecto y facturación.
