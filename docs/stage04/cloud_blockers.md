# Estado de autorización cloud

**Presupuesto máximo autorizado:** USD 20/mes; gasto objetivo USD 0.
**Propietaria y operadora designada:** Ana; titular de la cuenta de facturación.
**Supervisora:** Rita; roles de lectura y alertas, sin administración de billing.
**Estado operativo:** `GO_FOR_STAGE7_CONTROLLED_SHADOW; BUDGET_AND_IAM_CONFIGURED; PRIVATE_VERIFICATION_PENDING`.

El [acta supervisora D01–D12](acta_decision_d01_d12_20260913.md) confirma que el presupuesto no
autoriza conexión cloud, publicación ni cutover. Proyecto y vínculo de billing ya fueron
verificados privadamente; IAM y la lista de seis identidades continúan sin ejecutar ni verificar.

El margen de contingencia de USD 20/mes continúa vigente. La aclaración del 2026-09-17 fija USD 0
como objetivo de gasto, no como bloqueo absoluto. El vínculo de billing fue verificado
privadamente; no configura IAM ni modifica la autorización local del catálogo V0 completo.

La decisión vigente se registra en
[zero_spend_target_20260917.md](zero_spend_target_20260917.md). Como las alertas de Cloud Billing
no constituyen un tope automático, se mantienen los límites técnicos y la parada temprana.
Los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE` hasta completar verificación:

- comandos mutantes de `gcloud` y habilitación de APIs;
- creación o modificación de BigQuery y ejecución de DDL;
- buckets y Artifact Registry;
- Cloud Run, GKE, Airflow y Agent Platform;
- cuentas de servicio, configuración de alertas/límites y bindings IAM;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- despliegue, URL pública, publicación institucional o cutover.

Alcance vigente: `LOCAL_SHADOW_ONLY`; presupuesto, umbrales, canal y roles de lectura configurados,
ejecución cloud bloqueada hasta la verificación privada de Rita. No publicar, no hacer
cutover y no sustituir V0. Los contratos
describen destinos futuros, pero no crean recursos ni conceden autorización de publicación. Véase
[cloud_authorization.md](cloud_authorization.md) y
[cloud_budget_verification_20260917.md](cloud_budget_verification_20260917.md).
