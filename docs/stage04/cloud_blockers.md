# Estado de autorización cloud

**Presupuesto autorizado:** máximo USD 20/mes para todo Stage 04.
**Administradoras designadas:** Ana y Rita.
**Estado operativo:** `CLOUD_CONFIGURATION_PENDING`; no existe GO técnico ni primer despliegue verificado.

La autorización presupuestaria sustituye el estado histórico USD 0, que se conserva en commits y
evidencia anteriores. No configura billing, IAM ni recursos y no equivale a autorización de datos.
Los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE` hasta completar verificación:

- ejecución de `gcloud` y habilitación de APIs;
- creación o modificación de BigQuery y ejecución de DDL;
- buckets y Artifact Registry;
- Cloud Run, GKE, Airflow y Agent Platform;
- IAM, cuentas de servicio, vinculación de billing y configuración de alertas/límites;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- despliegue, URL pública, publicación institucional o cutover.

Alcance vigente: `LOCAL_SHADOW_ONLY`; presupuesto y administración `APPROVED`, configuración y
despliegue `PENDING_VERIFICATION`. Los contratos describen destinos futuros, pero no crean recursos
ni conceden autorización de publicación. Véase [cloud_authorization.md](cloud_authorization.md).
