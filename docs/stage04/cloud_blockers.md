# Componentes cloud bloqueados

Todos los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE`:

- ejecución de `gcloud` y habilitación de APIs;
- creación o modificación de BigQuery y ejecución de DDL;
- buckets y Artifact Registry;
- Cloud Run, GKE, Airflow y Agent Platform;
- IAM, cuentas de servicio, billing y presupuestos;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- despliegue, URL pública, publicación institucional o cutover.

Alcance vigente: `LOCAL_SHADOW_ONLY`, Cloud `NOT_AUTHORIZED`, presupuesto USD 0. Los archivos de
contrato describen destinos futuros, pero no crean recursos ni conceden autorización.
