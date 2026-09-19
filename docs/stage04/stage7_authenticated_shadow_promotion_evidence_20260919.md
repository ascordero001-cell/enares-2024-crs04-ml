# Evidencia de promoción shadow autenticada — 2026-09-19

## Resultado

`EXECUTED_PASS; PENDING_SUPERVISORY_REVIEW`

La ejecución reutilizó exclusivamente el servicio Cloud Run autenticado y el repositorio
Artifact Registry existentes. No creó servicios, identidades, datasets, buckets ni bindings IAM
de principals. No habilitó acceso público, publicación institucional ni cutover.

Autorizaciones y correcciones aplicadas:

- promoción real autorizada en la revisión del PR #123;
- runtime autenticado aprobado en el PR #124;
- corrección del límite de 10 MiB aprobada en el PR #125.

## BigQuery y promoción

- Origen aislado: 3.014 filas, 516 indicadores, una release, una corrida y un SHA-256.
- Filas no aprobadas: 0; filas suprimidas: 0.
- Registro: una release `APPROVED` y cinco gates `PASS` (`technical`, `v0_parity`, `privacy`,
  `release_consistency` y `query_cost_cap`).
- `__UNPROMOTED__` fue rechazado explícitamente como identidad real y queda protegido por una
  aserción Dataform durable.
- `published.v_dashboard_current` quedó autorizada sobre `outputs` como vista; la identidad de
  ejecución no recibió acceso directo a `outputs`.
- La lista ACL existente se conservó y no contiene acceso público.

Secuencia observada:

1. vista fail-closed con 0 filas;
2. `PROMOTE`: 3.014 filas y 516 indicadores visibles;
3. `ROLLBACK_TO_EMPTY`: puntero y vista en 0;
4. `RE_PROMOTE`: restauración exacta de las 3.014 filas y 516 indicadores;
5. paridad por módulo y SHA-256 preservado.

Todas las consultas de verificación se ejecutaron con
`maximum_bytes_billed=10,485,760`. La vista de una sola tabla pasó ese límite; no se aumentó el
guardrail.

## Cloud Run y acceso

- Imagen: artefacto inspeccionado del merge de PR #124, desplegado por digest.
- Servicio: el existente `enares-stage04-shadow`; no se creó otro.
- Despliegue inicial: revisión etiquetada con 0 % de tráfico.
- Escala: mínimo 0, máximo 1 instancia; concurrencia 6.
- Health autenticado: HTTP 200.
- Acceso anónimo: HTTP 403.
- Principals públicos `allUsers` / `allAuthenticatedUsers`: ausentes antes y después.
- Sesión Playwright autenticada: Streamlit renderizado, WebSocket abierto y contenido real sin
  error seguro de repositorio.
- Tráfico: promoción real 100 % → rollback sintético 100 % → restauración real 100 %.

## Primera consulta real a través de la aplicación

| Campo | Evidencia |
|---|---|
| Fecha UTC | 2026-09-19T00:26:12Z |
| Superficie | `published.v_dashboard_current` |
| Estado | `DONE`, sin error |
| Bytes procesados | 1.598.962 |
| Límite del job | 10.485.760 bytes |
| Cache | no utilizada |
| Job ID y principal | verificados y redactados del repositorio público |

La consulta anterior fue generada por una sesión de navegador contra la revisión real
autenticada. Una consulta previa falló cerrada por falta de autorización de la vista subyacente,
procesó 0 bytes y no recibió tráfico. Se corrigió mediante authorized view, sin conceder lectura
directa de `outputs` a la identidad del runtime.

## Estado final y límites

- `published`: release real aprobada, 3.014 filas / 516 indicadores.
- `ops`: registro, cinco gates y tres eventos append-only.
- Cloud Run: revisión real autenticada al 100 %, mínimo 0 y máximo 1.
- Presupuesto máximo: USD 20/mes; gasto objetivo: USD 0.
- Evidencia de uso: bytes procesados y ausencia de aumento del cap; el coste facturado definitivo
  no se infiere antes del reporte de facturación.
- V0 continúa oficial; la aplicación permanece shadow.
- Acceso público, publicación institucional, cutover y sustitución de V0: no autorizados.

Esta evidencia satisface técnicamente el paso 49. El cierre del sprint continúa pendiente del
paquete y la revisión supervisora del paso 53.
