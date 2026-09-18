# Solicitud de decisión — paso 47 y ejecución controlada de Etapa 7

**Fecha:** 2026-09-18 UTC

**Estado:** `DECISION_B_LOAD_AND_RECONCILIATION_PASS; PROMOTION_NOT_EXECUTED`

## Antecedentes verificados

- `GO_FOR_STAGE7_CONTROLLED_SHADOW` continúa vigente.
- El proyecto y su vínculo de facturación fueron verificados privadamente.
- El presupuesto de PEN 67, sus cuatro umbrales y el canal supervisor están configurados.
- Rita confirmó privadamente recepción del canal y acceso efectivo con `run.viewer`,
  `logging.viewer` y `monitoring.viewer` en la revisión aprobatoria del PR #116.
- Las 3.014 filas V0 fueron cargadas en `outputs` aislado y reconciliadas 3.014/3.014.
- Antes de la decisión no existían recursos de Stage 04 ni consultas cloud. La Decisión A fue
  aprobada posteriormente y se ejecutó con recursos aislados y sin cifras reales.

## Decisión solicitada A — infraestructura sintética

Autorizar, en este orden y sin cifras reales:

1. habilitar exclusivamente las APIs necesarias para Artifact Registry, Cloud Run, BigQuery,
   Logging y Monitoring;
2. crear una identidad de ejecución sin claves JSON;
3. crear un repositorio Artifact Registry en `us-central1` y mantener una sola imagen viva;
4. crear los datasets vacíos `outputs`, `published` y `ops` en BigQuery `US`;
5. aplicar `maximum_bytes_billed=10,485,760`, cuota diaria de consulta de 1 GiB y acceso mínimo;
6. desplegar el fixture sintético en Cloud Run autenticado, con mínimo cero y máximo una instancia;
7. ejecutar health, diagnóstico, acceso positivo/negativo, seis sesiones y rollback de práctica.

Esta decisión no incluye datos V0 reales, acceso público, buckets, GKE, Airflow, Agent Engine,
publicación institucional, cutover ni sustitución de V0.

## Decisión solicitada B — cifras reales agregadas

Mantener bloqueada hasta que la decisión A termine con evidencia `PASS`. Después de ese resultado,
Rita decidirá por separado si autoriza cargar exclusivamente las 3.014 filas agregadas V0 fijadas
por manifiesto y SHA-256. No se cargarán microdatos ni se fabricarán cortes o cruces nuevos.

## Condiciones de parada

- Cualquier permiso inesperado, acceso anónimo, error de procedencia o discrepancia detiene la
  ejecución.
- La primera alerta de gasto congela nuevas pruebas y exige investigación.
- El gasto objetivo continúa siendo USD 0; USD 20/mes es techo de contingencia, no meta.
- Cada acción debe registrarse con fecha UTC, actor, recurso, resultado, coste observado y rollback.

## Decisión registrada

- `APPROVE_A_SYNTHETIC_INFRA_ONLY`: aprobada y ejecutada.
- `ISOLATE_STAGE04_DATASETS`: aprobada; los datasets preexistentes permanecieron intactos.
- La decisión supervisora del 2026-09-18 resolvió `VF_ESCUELA`, la política universal de alertas
  sin supresión y el antiguo HOLD de D06/D07. Ya no existe un bloqueante metodológico de
  confidencialidad para B.
- `APPROVE_B_REAL_V0_CLOUD_EXECUTION`: aprobada en el PR #120 y ejecutada hasta carga y
  reconciliación.
- La promoción a `published`, escritura en `ops` y conexión real de Cloud Run no fueron ejecutadas.
