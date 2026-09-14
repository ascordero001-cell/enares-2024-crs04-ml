# Registro de autorización cloud — Stage 04

**Decisión:** Rita, 2026-09-13
**Estado:** `BUDGET_AND_ADMINISTRATION_APPROVED; CLOUD_CONFIGURATION_PENDING`
**Alcance vigente:** `LOCAL_SHADOW_ONLY`

| Campo | Estado verificable |
|---|---|
| Presupuesto | Máximo USD 20/mes para el total de Stage 04, no por servicio |
| Administradoras | Ana y Rita; identidades exactas pendientes de registro privado |
| Proyecto previsto | `enares-2024-crs04`; existencia y coincidencia pendientes de verificación |
| Ubicaciones previstas | BigQuery `US`; Cloud Run `us-central1`; pendientes de verificación |
| Billing | `PENDING`; cuenta, responsable y recuperación no verificados |
| IAM | `PENDING`; roles mínimos y seis identidades no configurados ni probados |
| Recursos permitidos tras GO | BigQuery candidato `outputs/published/ops`, Artifact Registry y Cloud Run Service |
| Recursos ejecutados por este PR | Ninguno |
| Datos autorizados | Solo baseline/golden ya aprobados; nuevas cifras y pares pendientes |
| Acceso | Seis personas previstas; lista privada, autenticación y revocación pendientes |
| Parada | Ana ejecuta y Rita supervisa; procedimiento efectivo pendiente |
| Decisión técnica | `NO_GO_UNTIL_VERIFIED` |

Antes de cualquier primer despliegue deben verificarse billing, identidades, roles, alertas
USD 5/10/15/20, límites de consulta y cómputo, máximo una instancia inicial, acceso positivo y
negativo, seis sesiones, health y rollback. Las alertas de presupuesto no son un tope automático.

Este PR no ejecuta `gcloud`, no crea cuentas, bindings, datasets, buckets, imágenes ni servicios.

La solicitud operativa de los pasos 40–41, con alcance mínimo, IAM propuesto, controles de coste,
rollback y campos bloqueantes, está en [cloud_go_request.md](cloud_go_request.md). Mientras los
responsables reales de billing/IAM, la cuenta, el proyecto y las identidades no estén verificados,
la decisión continúa como `NO_GO / CLOUD_NOT_AUTHORIZED`.
