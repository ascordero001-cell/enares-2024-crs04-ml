# Solicitud de decisión — paso 47 y ejecución controlada de Etapa 7

**Fecha:** 2026-09-18 UTC

**Estado:** `PENDING_SUPERVISORY_DECISION`

## Antecedentes verificados

- `GO_FOR_STAGE7_CONTROLLED_SHADOW` continúa vigente.
- El proyecto y su vínculo de facturación fueron verificados privadamente.
- El presupuesto de PEN 67, sus cuatro umbrales y el canal supervisor están configurados.
- Rita confirmó privadamente recepción del canal y acceso efectivo con `run.viewer`,
  `logging.viewer` y `monitoring.viewer` en la revisión aprobatoria del PR #116.
- Las 3.014 filas V0 están conectadas y verificadas localmente; no se han cargado en cloud.
- Recursos creados, consultas ejecutadas y gasto acumulado antes de esta decisión: cero.

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

## Decisión requerida

- `APPROVE_A_SYNTHETIC_INFRA_ONLY`: permite pasos 43–46 sin cifras reales.
- `NO_GO`: no se crea ningún recurso.
- La decisión B permanece siempre separada y requiere una aprobación posterior explícita.
