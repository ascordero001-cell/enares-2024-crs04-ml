# Registro de autorización cloud — Stage 04

**Decisión:** Rita, 2026-09-13
**Estado:** `BUDGET_AND_ADMINISTRATION_APPROVED; CLOUD_CONFIGURATION_PENDING`
**Alcance vigente:** `LOCAL_SHADOW_ONLY`

| Campo | Estado verificable |
|---|---|
| Modelo de coste | Operación prevista dentro de la capa gratuita; USD 20/mes es margen máximo de contingencia, no gasto objetivo |
| Administradoras | Ana y Rita; identidades exactas pendientes de registro privado |
| Proyecto previsto | `enares-2024-crs04`; existencia y coincidencia pendientes de verificación |
| Ubicaciones previstas | BigQuery `US`; Cloud Run `us-central1`; pendientes de verificación |
| Billing | Responsable: Rita; cuenta y medio de pago propios, pendientes de verificación privada |
| IAM | Ana aplica bindings y Rita revisa cada uno; sin claves JSON; configuración aún no ejecutada |
| Recursos permitidos tras GO | BigQuery candidato `outputs/published/ops`, Artifact Registry y Cloud Run Service |
| Recursos ejecutados por este PR | Ninguno |
| Datos autorizados | Solo las 52 filas agregadas autorizadas y fijadas por manifiesto; no se autorizan cifras nuevas |
| Acceso | Seis personas: protección UNICEF, Dirección de Niñez del MIMP, Ana, Rita y dos reservas; principales exactos solo por canal privado |
| Parada | Política aprobada: Ana ejecuta y Rita supervisa; prueba efectiva solo después del GO |
| Decisión técnica | `NO_GO_UNTIL_VERIFIED` |

Antes de cualquier primer despliegue deben verificarse la cuenta de billing, el proyecto,
identidades, roles, alertas USD 1/5/10/20, `maximum_bytes_billed` en cada consulta, cuota diaria
personalizada de BigQuery, mínimo cero y máximo una instancia, limpieza de Artifact Registry,
acceso positivo y negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son
un tope automático; los límites técnicos son obligatorios.

Este PR no ejecuta `gcloud`, no crea cuentas, bindings, datasets, buckets, imágenes ni servicios.

La solicitud operativa de los pasos 40–41, con alcance mínimo, IAM propuesto, controles de coste,
rollback y campos bloqueantes, está en [cloud_go_request.md](cloud_go_request.md). Mientras los
cuenta de billing y el proyecto no estén verificados, la decisión continúa como
`NO_GO / CLOUD_NOT_AUTHORIZED`.
