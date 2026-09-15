# Estado de autorización cloud

**Presupuesto autorizado:** máximo USD 20/mes para todo Stage 04.
**Propietaria y operadora designada:** Ana; titular de la cuenta de facturación.
**Supervisora:** Rita; roles de lectura y alertas, sin administración de billing.
**Estado operativo:** `GO_FOR_STAGE7_CONTROLLED_SHADOW; PRIVATE_PROJECT_BILLING_VERIFICATION_PENDING`.

El [acta supervisora D01–D12](acta_decision_d01_d12_20260913.md) confirma que el presupuesto no
autoriza conexión cloud, publicación ni cutover. Billing, IAM y la lista de seis identidades
continúan sin verificar.

La autorización presupuestaria sustituye el estado histórico USD 0, que se conserva en commits y
evidencia anteriores. No configura billing, IAM ni recursos. La autorización local del catálogo
V0 tampoco equivale al gate separado del paso 47 para cifras reales en cloud.
Los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE` hasta completar verificación:

- ejecución de `gcloud` y habilitación de APIs;
- creación o modificación de BigQuery y ejecución de DDL;
- buckets y Artifact Registry;
- Cloud Run, GKE, Airflow y Agent Platform;
- cuentas de servicio, vinculación de billing y configuración de alertas/límites antes de la
  verificación privada; los bindings se aplican únicamente en el orden de la Etapa 7;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- despliegue, URL pública, publicación institucional o cutover.

Alcance vigente: `LOCAL_SHADOW_ONLY`; presupuesto y GO controlado `APPROVED`, ejecución
`BLOCKED_PENDING_PRIVATE_VERIFICATION`. Los contratos describen destinos futuros, pero no crean
recursos ni conceden autorización de publicación. Véase [cloud_authorization.md](cloud_authorization.md).
