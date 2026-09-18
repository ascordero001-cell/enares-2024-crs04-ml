# Registro de autorización cloud — Stage 04

**Decisión histórica:** Rita, 2026-09-13

**Aclaración operativa:** Ana, 2026-09-17

**Estado:** `DECISION_B_LOAD_AND_RECONCILIATION_PASS; PROMOTION_BLOCKED`
**Alcance vigente:** `CONTROLLED_SHADOW; REAL_V0_IN_OUTPUTS_ONLY`

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
| Datos ejecutados | 3.014 filas V0 cargadas en `outputs` aislado y reconciliadas 3.014/3.014; `published` y `ops` vacíos |
| Acceso | Ana y Rita verificadas con invocación autenticada; cuatro reservas retiradas formalmente para este cierre; principales exactos solo por canal privado |
| Parada | Política aprobada: Ana ejecuta y Rita supervisa; prueba efectiva solo después del GO |
| Decisión técnica | Decisión B ejecutada hasta carga y reconciliación; promoción y conexión de Cloud Run no ejecutadas |

Antes de cualquier primer despliegue deben verificarse identidades, roles, alertas USD 1/5/10/20,
`maximum_bytes_billed` en cada consulta, cuota diaria
personalizada de BigQuery, mínimo cero y máximo una instancia, limpieza de Artifact Registry,
acceso positivo y negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son
un tope automático; el objetivo de gasto es USD 0 y el techo de contingencia es USD 20.

La ejecución B creó únicamente `outputs.indicator_estimates` dentro del dataset aislado ya
existente. No añadió cuentas, bindings, datasets, buckets, imágenes ni servicios.

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
a `published` y la conexión de Cloud Run permanecen separadas.

Véase [zero_spend_target_20260917.md](zero_spend_target_20260917.md).
La configuración redactada está en
[cloud_budget_verification_20260917.md](cloud_budget_verification_20260917.md).
La decisión siguiente se solicita en
[step47_cloud_execution_request.md](step47_cloud_execution_request.md).
La ejecución redactada se registra en
[stage7_synthetic_execution_evidence_20260918.md](stage7_synthetic_execution_evidence_20260918.md).
La primera carga real se registra en
[stage7_real_v0_load_evidence_20260918.md](stage7_real_v0_load_evidence_20260918.md).

Rita no administra la cuenta ni puede detener el gasto directamente. Sus controles son
`CODEOWNERS`, los gates de los pasos 47/53 y la visibilidad de ejecución y alertas. Antes de una
entrega institucional debe resolverse una titularidad institucional para proyecto y facturación.
