# Estado de autorización cloud

**Presupuesto operativo vigente:** `USD 0` estricto desde el 2026-09-17.
**Propietaria y operadora designada:** Ana; titular de la cuenta de facturación.
**Supervisora:** Rita; roles de lectura y alertas, sin administración de billing.
**Estado operativo:** `BILLING_LINK_VERIFIED; ZERO_BUDGET_HARD_STOP`.

El [acta supervisora D01–D12](acta_decision_d01_d12_20260913.md) confirma que el presupuesto no
autoriza conexión cloud, publicación ni cutover. Proyecto y vínculo de billing ya fueron
verificados privadamente; IAM y la lista de seis identidades continúan sin ejecutar ni verificar.

El margen histórico de contingencia de USD 20/mes se conserva en el acta y las revisiones que lo
aprobaron, pero queda sin efecto operativo por la decisión más restrictiva del 2026-09-17. El
vínculo de billing fue verificado privadamente; no configura IAM, no autoriza recursos y no
modifica la autorización local del catálogo V0 completo.

La decisión vigente se registra en
[zero_budget_override_20260917.md](zero_budget_override_20260917.md). Como las alertas de Cloud
Billing no constituyen un tope automático, no se ejecuta ningún paso cloud con límite estricto
`USD 0`.
Los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE` hasta completar verificación:

- comandos mutantes de `gcloud` y habilitación de APIs;
- creación o modificación de BigQuery y ejecución de DDL;
- buckets y Artifact Registry;
- Cloud Run, GKE, Airflow y Agent Platform;
- cuentas de servicio, configuración de alertas/límites y bindings IAM;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- despliegue, URL pública, publicación institucional o cutover.

Alcance vigente: `LOCAL_SHADOW_ONLY`; ejecución cloud `BLOCKED_BY_ZERO_BUDGET`. No publicar, no
hacer cutover y no sustituir V0. Los contratos describen destinos futuros, pero no crean recursos
ni conceden autorización de publicación. Véase [cloud_authorization.md](cloud_authorization.md).
