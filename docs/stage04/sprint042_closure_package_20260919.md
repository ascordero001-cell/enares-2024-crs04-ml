# Sprint 04.2 — paquete de cierre supervisor

- Fecha: 2026-09-19
- Estado: `CLOSED; PASS_SUPERVISOR`
- Alcance: `CONTROLLED_SHADOW`
- V0: continúa oficial
- Publicación institucional, acceso público, cutover y sustitución de V0: `NOT_AUTHORIZED`

Este paquete presenta el cierre técnico del Sprint 04.2. No convierte el shadow en publicación,
no amplía IAM y no sustituye la decisión final de la revisora en el paso 53.

## Resultado técnico

| Control | Resultado |
|---|---|
| Catálogo local | 3.014/3.014 filas; 516/516 indicadores |
| Cobertura | módulos 3.1–3.6 completos |
| Promoción shadow | 3.014 filas / 516 indicadores |
| Gates operativos | 5/5 `PASS` |
| Ciclo operacional | `PROMOTE → ROLLBACK_TO_EMPTY → RE_PROMOTE` |
| BigQuery | consultas bajo `maximum_bytes_billed=10.485.760` |
| Cloud Run | autenticado; health 200; anónimo 403; mínimo 0; máximo 1 |
| Acceso a datos | vista autorizada; 0 ACL directa del runtime en `outputs` |
| Acceso público | 0 entradas `allUsers` / `allAuthenticatedUsers` |

La revisión formal del PR #126 aprobó sin reservas el paso 49. El merge
`8eaedce97ad6222ea20bb6af6ad27071e46feb02` quedó seguido por CI, App CI, Container CI,
Security CI y Quickstart CI en `SUCCESS`.

## Auditoría de afirmaciones de control

La pasada exigida antes del paso 53 contrastó el nombre de cada control con la ruta que se
ejecuta y con su prueba negativa. No se aceptó como control una afirmación exclusivamente
documental.

| Afirmación | Ruta o configuración ejecutada | Evidencia de fallo cerrado | Estado |
|---|---|---|---|
| El diagnóstico cubre el release completo | `scripts/release_diagnostic.py` | rechaza releases múltiples y release inesperado | `PASS` |
| `[referencial]` procede de `cv_flag` | UI y exportación llaman funciones derivadas del flag | verdadero/falso cubiertos; texto fuente no gobierna la alerta | `PASS` |
| La granularidad nunca supera V0 | `validate_estimates` llama `assert_v0_granularity_boundary` | dimensión, cruce y par matricial no autorizados se rechazan | `PASS` |
| `synthetic=false` deriva de procedencia | `AuthorizedAggregateRepository` verifica manifiesto, SHA-256 y registro | faltantes, duplicados y origen no autorizado se rechazan | `PASS` |
| El catálogo integral coincide con V0 | ledger de reconciliación y pruebas parametrizadas | 3.014/3.014, sin faltantes, extras ni diferencias | `PASS` |
| Un release reservado no puede promoverse | aserción Dataform `stage04_reserved_release_identity` | `UNPROMOTED` y `__UNPROMOTED__` producen filas de aserción | `PASS` |
| El límite de consulta se aplica al runtime | repositorio BigQuery y jobs reales | primera consulta real: 1.598.962 de 10.485.760 bytes | `PASS` |
| El runtime no lee `outputs` directamente | IAM del proyecto y ACL de datasets | 0 grant de datos del proyecto; 0 ACL directa en `outputs` | `PASS` |
| La app no queda pública | IAM de Cloud Run y prueba anónima | anónimo 403; 0 principals públicos | `PASS` |
| Promoción y rollback no mezclan snapshots | lifecycle, cache por release/run y ejecución real | rollback a vacío y repromoción exacta | `PASS` |
| El residual WCAG conocido no puede crecer silenciosamente | `test:a11y-control` en App CI | el conteo distinto de nueve falla | `PASS` |
| Mypy comprueba llamadas entre módulos Stage 04 | `follow_imports = normal` global | CI y prueba de configuración; excepción limitada a `scripts.*` | `PASS` |

La maquinaria de dominancia y supresión complementaria permanece explícitamente inactiva: V0 no
incluye señal de dominancia y la política vigente no suprime por recuento. No se presenta como
protección activa.

## Validación del paquete

- `python -m pytest -q`: 476 passed, 2 skipped, 0 failed;
- `python -m mypy src app tests`: sin errores en 84 archivos fuente;
- `dataform compile dataform`: 48 acciones compiladas;
- `git diff --check`: sin errores.

Los dos skips corresponden exclusivamente a rederivaciones que requieren la ubicación privada del
padre V0. La reconciliación integral 3.014/3.014 y los hashes ya están versionados; el paquete no
incorpora rutas privadas ni datos fuente.

## Paso 52 — URL y advertencia de estado

URL autenticada:

<https://enares-stage04-shadow-bmg5ifoitq-uc.a.run.app>

La URL exige identidad autorizada. No concede acceso público y no constituye publicación
institucional. El PR #127 la registró en README y en el propio paquete; el campo About del
repositorio contiene la URL y la advertencia de estado. El prerelease de ingeniería
[`stage04-sprint042-controlled-shadow`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/releases/tag/stage04-sprint042-controlled-shadow)
apunta al merge aprobado y repite esta misma advertencia.

## Evidencia principal

- [Matriz de cobertura](module_coverage_matrix.md)
- [Auditoría de controles ejecutables](executable_control_claims_audit.md)
- [Evaluación HCI y accesibilidad](hci_accessibility_corte2.md)
- [Conexión integral V0](pr_b_full_v0_connection.md)
- [Carga y reconciliación real](stage7_real_v0_load_evidence_20260918.md)
- [Promoción autenticada](stage7_authenticated_shadow_promotion_evidence_20260919.md)
- [Runbook de promoción y rollback](promotion_rollback_runbook.md)

## Decisión supervisora — paso 53

Rita aprobó el head `9dcb9e7` y el cierre del Sprint 04.2 bajo `CONTROLLED_SHADOW`. El PR #127 se
fusionó en `68f052ccdb2b6d67cb31ea66134a2885de1958bf`; las cinco workflows posteriores de `main`
terminaron en `SUCCESS`. La decisión no autoriza acceso público, publicación institucional,
cutover, sustitución de V0 ni un aumento del techo presupuestario. El Issue #43 permanece abierto
como paraguas de Stage 04.
