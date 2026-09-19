# Sprint 04.3 — auditoría de prerequisitos y afirmaciones de control

- Fecha: 2026-09-19
- Issue núcleo: #45
- Base auditada: `main` en `9d780c609b72155c8577cc07fc765ba3b4d82a65`
- Estado técnico: `PASS; NO_OPEN_SPRINT042_CONTROL_GAPS`
- Gate: `PENDING_SUPERVISORY_CONFIRMATION_0_3`

## Cierre del prerequisito 0.1

El Issue #46 quedó cerrado después de registrar la evidencia que faltaba:

- PR #126: ejecución real de `PROMOTE → ROLLBACK_TO_EMPTY → RE_PROMOTE`;
- PR #127: paquete de Sprint 04.2 aprobado por Rita;
- 3.014/3.014 filas, 516/516 indicadores y cinco gates `PASS`;
- configuración viva de IAM/ACL contrastada;
- CI posterior a los merges en `SUCCESS`.

El Issue #43 permanece abierto como paraguas y el Issue #45 permanece abierto para Sprint 04.3.

## Método de la auditoría 0.2

Se volvió a aplicar el criterio de la advertencia de cierre: para cada nombre de control se buscó
la ruta que realmente se ejecuta, su prueba negativa y, cuando corresponde, la comprobación de
configuración viva. Se revisaron los PR #119–#127 y la auditoría versionada en
`executable_control_claims_audit.md`; no se aceptó como protección una afirmación solo documental.

| Afirmación | Ruta ejecutable o estado vivo | Prueba negativa o contraste | Resultado |
|---|---|---|---|
| Diagnóstico de release completo | `scripts/release_diagnostic.py` | releases múltiples o inesperados fallan | `PASS` |
| Procedencia antes de `synthetic=false` | `AuthorizedAggregateRepository` | manifiesto, hash o registro inválido fallan | `PASS` |
| Reglas estadísticas compartidas | `quality_rules.py` | ambos adaptadores recorren la misma lógica | `PASS` |
| Granularidad limitada a V0 | `validate_estimates` → `assert_v0_granularity_boundary` | dimensiones y cruces no autorizados fallan | `PASS` |
| `[referencial]` derivado del flag | UI y exportación | marcador sin `cv_flag` falla | `PASS` |
| Reconciliación integral | ledger y suite parametrizada | faltantes, extras o diferencias fallan | `PASS` |
| Identidad reservada rechazada | aserción Dataform | `UNPROMOTED` y `__UNPROMOTED__` fallan | `PASS` |
| Cap de bytes obligatorio | `BigQueryRepository` y jobs reales | consulta sobre cap falla antes de ejecutarse | `PASS` |
| Vista autorizada sin lectura directa | IAM y ACL vivos | 0 roles de datos y 0 ACL directa en `outputs` | `PASS` |
| Acceso exclusivamente autenticado | IAM de Cloud Run | llamada anónima devuelve 403 | `PASS` |
| Cache aislada por release/run | `repository_cache.py` | snapshots no pueden sobrescribirse ni mezclarse | `PASS` |
| Rollback verificable | lifecycle, runbook y ejecución real | rollback a vacío y repromoción exacta | `PASS` |
| Residual WCAG acotado | `test:a11y-control` | conteo distinto de nueve falla | `PASS` |
| Tipos entre módulos | mypy con `follow_imports = normal` | CI comprueba `src`, `app` y `tests` | `PASS` |

## Hallazgos

No se encontró una afirmación activa de Sprint 04.2 sin ruta ejecutable, prueba negativa o
verificación viva. No queda una corrección de Sprint 04.2 pendiente antes de especificar la
automatización.

Sí existe un gate nuevo y propio de Sprint 04.3: un runner de GitHub no dispone de un canal
autorizado para recibir un agregado privado de una release futura. El repositorio no contiene el
CSV V0 real y no existen bucket, credencial ni mecanismo de descarga autorizados para este fin.
Esto no invalida Sprint 04.2, que ejecutó el flujo bajo supervisión; impide implementar una carga
automatizada futura hasta que Rita apruebe el contrato de entrada. No se creará ese canal por
inferencia.

## Decisión solicitada — 0.3

Se solicita a Rita confirmar:

1. que esta auditoría satisface 0.2 y no deja correcciones de Sprint 04.2 abiertas;
2. que la implementación de Etapa 2 permanece en `HOLD` hasta aprobar el canal de entrada;
3. que puede aprobarse la clasificación humano/automatizable de la especificación de Etapa 1.

Nada en esta auditoría autoriza acceso público, publicación, cutover, sustitución de V0, aumento
del techo de USD 20/mes ni del cap de 10 MiB.
