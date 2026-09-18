# Estado de autorización cloud

**Presupuesto máximo autorizado:** USD 20/mes; gasto objetivo USD 0.
**Propietaria y operadora designada:** Ana; titular de la cuenta de facturación.
**Supervisora:** Rita; roles de lectura y alertas, sin administración de billing.
**Estado operativo:** `DECISION_A_CLOSED_PASS; DECISION_B_READY_FOR_EXPLICIT_EXECUTION_GO`.

El [acta supervisora D01–D12](acta_decision_d01_d12_20260913.md) confirma que el presupuesto no
autoriza conexión cloud, publicación ni cutover. Proyecto y vínculo de billing ya fueron
verificados privadamente. Rita confirmó recepción del canal y funcionamiento efectivo de sus tres
roles de lectura. El servicio sintético existe y concede invocación únicamente a dos principales
verificados; los cuatro principales de reserva continúan pendientes y se conservan fuera del
repositorio.

El margen de contingencia de USD 20/mes continúa vigente. La aclaración del 2026-09-17 fija USD 0
como objetivo de gasto, no como bloqueo absoluto. El vínculo de billing fue verificado
privadamente; no configura IAM ni modifica la autorización local del catálogo V0 completo.

La decisión vigente se registra en
[zero_spend_target_20260917.md](zero_spend_target_20260917.md). Como las alertas de Cloud Billing
no constituyen un tope automático, se mantienen los límites técnicos y la parada temprana.
Los elementos siguientes permanecen `BLOCKED_BY_CLOUD_GATE`:

- tablas, vistas, cargas, consultas o DDL con cifras V0 reales;
- una segunda imagen viva o recursos fuera del conjunto mínimo aprobado;
- buckets, GKE, Airflow y Agent Platform;
- acceso anónimo o bindings adicionales sin principal privado verificado;
- autenticación de `BigQueryRepository`;
- carga CSV–BigQuery y cualquier afirmación de paridad cloud;
- URL pública, publicación institucional o cutover.

La decisión supervisora del 2026-09-18 resolvió `VF_ESCUELA`, confirmó alertas CV/N universales
sin supresión y retiró el HOLD de D06/D07. La confidencialidad ya no bloquea la Decisión B. Aun
así, no se ejecutan cargas ni consultas reales hasta recibir el GO explícito de ejecución de B.

Alcance vigente: `CONTROLLED_SHADOW; SYNTHETIC_ONLY`. La Decisión A permitió la infraestructura
aislada y el fixture sintético; la Decisión B para cifras reales no está aprobada. No publicar, no
hacer cutover y no sustituir V0. Los contratos
describen destinos futuros, pero no crean recursos ni conceden autorización de publicación. Véase
[cloud_authorization.md](cloud_authorization.md) y
[cloud_budget_verification_20260917.md](cloud_budget_verification_20260917.md).
