# Registro de autorización cloud — Stage 04

**Decisión:** Rita, 2026-09-13
**Estado:** `GO_FOR_STAGE7_CONTROLLED_SHADOW; PRIVATE_PROJECT_BILLING_VERIFICATION_PENDING`
**Alcance vigente:** `LOCAL_SHADOW_ONLY`

| Campo | Estado verificable |
|---|---|
| Modelo de coste | Operación prevista dentro de la capa gratuita; USD 20/mes es margen máximo de contingencia, no gasto objetivo |
| Propiedad y operación | Ana; propietaria del proyecto y titular de la cuenta de facturación |
| Supervisión | Rita; lectura de Cloud Run, Logging y Monitoring, sin propiedad ni administración de billing |
| Proyecto previsto | `enares-2024-crs04`; existencia y coincidencia pendientes de verificación |
| Ubicaciones previstas | BigQuery `US`; Cloud Run `us-central1`; pendientes de verificación |
| Billing | Responsable: Ana; cuenta y medio de pago propios, pendientes de confirmación privada |
| IAM | Ana aplica bindings; Rita recibe `roles/run.viewer`, `roles/logging.viewer` y `roles/monitoring.viewer`; sin claves JSON |
| Recursos permitidos tras GO | BigQuery candidato `outputs/published/ops`, Artifact Registry y Cloud Run Service |
| Recursos ejecutados por este PR | Ninguno |
| Datos autorizados | Catálogo V0 autorizado para implementación local; la conexión de cifras reales en cloud conserva el gate separado del paso 47 |
| Acceso | `viewer_01` a `viewer_04` solo con `roles/run.invoker`; Ana propietaria/operadora; Rita supervisora de lectura; principales exactos solo por canal privado |
| Parada | Política aprobada: Ana ejecuta y Rita supervisa; prueba efectiva solo después del GO |
| Decisión técnica | GO controlado concedido; ejecución bloqueada hasta verificar privadamente proyecto y billing |

Antes de cualquier primer despliegue deben verificarse la cuenta de billing, el proyecto,
identidades, roles, alertas USD 1/5/10/20, `maximum_bytes_billed` en cada consulta, cuota diaria
personalizada de BigQuery, mínimo cero y máximo una instancia, limpieza de Artifact Registry,
acceso positivo y negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son
un tope automático; los límites técnicos son obligatorios.

Este PR no ejecuta `gcloud`, no crea cuentas, bindings, datasets, buckets, imágenes ni servicios.

La solicitud operativa de los pasos 40–41, con alcance mínimo, IAM propuesto, controles de coste,
rollback y campos bloqueantes, está en [cloud_go_request.md](cloud_go_request.md). El GO del
2026-09-14 autoriza preparar la configuración, pero no permite iniciar el paso 43 hasta confirmar
privadamente cuenta de billing activa, proyecto exacto, vínculo, alertas y roles de lectura.

Rita no administra la cuenta ni puede detener el gasto directamente. Sus controles son
`CODEOWNERS`, los gates de los pasos 47/53 y la visibilidad de ejecución y alertas. Antes de una
entrega institucional debe resolverse una titularidad institucional para proyecto y facturación.
