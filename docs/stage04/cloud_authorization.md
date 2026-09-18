# Registro de autorización cloud — Stage 04

**Decisión histórica:** Rita, 2026-09-13

**Actualización operativa más restrictiva:** Ana, 2026-09-17
**Estado:** `BILLING_LINK_VERIFIED; ZERO_BUDGET_HARD_STOP`
**Alcance vigente:** `LOCAL_SHADOW_ONLY`

| Campo | Estado verificable |
|---|---|
| Modelo de coste | Límite operativo estricto `USD 0` desde el 2026-09-17; no se ejecutan operaciones cloud |
| Propiedad y operación | Ana; propietaria del proyecto y titular de la cuenta de facturación |
| Supervisión | Rita; lectura de Cloud Run, Logging y Monitoring, sin propiedad ni administración de billing |
| Proyecto | `enares-2024-crs04`; existencia y coincidencia verificadas privadamente |
| Ubicaciones previstas | BigQuery `US`; Cloud Run `us-central1`; pendientes de verificación |
| Billing | Responsable: Ana; vínculo efectivo verificado privadamente, sin publicar identificadores |
| IAM | Ana aplica bindings; Rita recibe `roles/run.viewer`, `roles/logging.viewer` y `roles/monitoring.viewer`; sin claves JSON |
| Recursos permitidos actualmente | Ninguno; el diseño histórico de BigQuery, Artifact Registry y Cloud Run queda bloqueado |
| Recursos ejecutados por este PR | Ninguno |
| Datos autorizados | Catálogo V0 autorizado para implementación local; la conexión de cifras reales en cloud conserva el gate separado del paso 47 |
| Acceso | `viewer_01` a `viewer_04` solo con `roles/run.invoker`; Ana propietaria/operadora; Rita supervisora de lectura; principales exactos solo por canal privado |
| Parada | Política aprobada: Ana ejecuta y Rita supervisa; prueba efectiva solo después del GO |
| Decisión técnica | El GO histórico se conserva; su ejecución está bloqueada por el límite estricto `USD 0` |

Antes de cualquier primer despliegue deben existir una nueva autorización de presupuesto positivo,
identidades, roles, alertas acordes con esa autorización, `maximum_bytes_billed` en cada consulta, cuota diaria
personalizada de BigQuery, mínimo cero y máximo una instancia, limpieza de Artifact Registry,
acceso positivo y negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son
un tope automático; con `USD 0` no se despliega ni se crea ningún recurso.

Este PR no ejecuta `gcloud`, no crea cuentas, bindings, datasets, buckets, imágenes ni servicios.

La solicitud operativa de los pasos 40–41, con alcance mínimo, IAM propuesto, controles de coste,
rollback y campos bloqueantes, está en [cloud_go_request.md](cloud_go_request.md). El GO del
2026-09-14 queda como antecedente. La decisión operativa del 2026-09-17 impide iniciar el paso 43
mientras el límite estricto sea `USD 0`, aunque proyecto y vínculo ya estén verificados.

Véase [zero_budget_override_20260917.md](zero_budget_override_20260917.md).

Rita no administra la cuenta ni puede detener el gasto directamente. Sus controles son
`CODEOWNERS`, los gates de los pasos 47/53 y la visibilidad de ejecución y alertas. Antes de una
entrega institucional debe resolverse una titularidad institucional para proyecto y facturación.
