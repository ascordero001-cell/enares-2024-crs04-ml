# Sprint 04.3 — especificación base del pipeline shadow

- Fecha: 2026-09-19
- Issue núcleo: #45
- Estado: `CLASSIFICATION_APPROVED; STAGE2_PREPARATION_IN_PROGRESS`
- Principio: automatizar ejecución técnica; nunca automatizar autorización

## Contrato de entrada propuesto

Cada corrida identifica de forma inmutable:

- `release_id` y `run_id` no reservados;
- SHA-256 del padre V0 aprobado;
- SHA-256 y manifiesto del extracto agregado;
- conteos esperados de filas e indicadores;
- commit, digest de imagen y versión Dataform;
- decisión supervisora aplicable y commit exacto que la contiene.

El valor `synthetic=false` no forma parte de la entrada confiable: lo deriva exclusivamente
`AuthorizedAggregateRepository` después de verificar la procedencia.

## Flujo manual convertido uno a uno

| Orden | Paso observado en PR #119–#127 | Clasificación propuesta | Comportamiento automatizado |
|---:|---|---|---|
| 1 | Confirmar alcance, presupuesto y autorización | Exclusivamente humano | validar que existe un registro `APPROVE_*` aplicable; sin él, `HOLD` |
| 2 | Verificar recursos aislados e IAM | Automatizable, solo lectura | comprobar proyecto, datasets, identidad, ACL, ausencia de principals públicos y escala 0–1 |
| 3 | Verificar manifiesto, SHA-256 y registro V0 | Automatizable | llamar las rutas de procedencia existentes; cualquier diferencia falla cerrada |
| 4 | Resolver el agregado privado de entrada | Exclusivamente humano hasta decisión | seleccionar un canal previamente aprobado; nunca descargar por una ruta inventada |
| 5 | Cargar `outputs.indicator_estimates` | Automatizable después de autorización | carga idempotente por release/run; existente idéntico se acepta, distinto se rechaza |
| 6 | Reconciliar 31 campos y cobertura | Automatizable | 3.014/3.014, sin faltantes, extras ni diferencias; tolerancia 1e-9 solo para serialización |
| 7 | Ejecutar gates técnicos | Automatizable | `technical`, `v0_parity`, `privacy`, `release_consistency`, `query_cost_cap` |
| 8 | Generar evidencia previa | Automatizable | artefacto Markdown/JSON redactado, con bytes y resultados, sin principal ni job ID públicos |
| 9 | Autorizar promoción autenticada | Exclusivamente humano | exigir decisión trazable distinta de la autorización de carga |
| 10 | Promover vista y revisión de Cloud Run | Automatizable después de autorización | fijar literalmente release/run aprobado y mantener acceso autenticado |
| 11 | Verificar health, acceso y paridad | Automatizable | health 200 autenticado, anónimo 403, una release/run y cifras centinela |
| 12 | Autorizar y ejecutar rollback de ensayo | Humano + automatizable | decisión humana; ejecución técnica y evidencia automáticas |
| 13 | Re-promover exactamente el snapshot aprobado | Automatizable después de autorización | restaurar mismo release/run, sin recalcular ni mezclar cache |
| 14 | Aceptar el cierre | Exclusivamente humano | Rita revisa evidencia y decide `PASS` o `HOLD` |

## Fronteras ejecutables obligatorias

El pipeline debe importar o invocar las rutas existentes, sin copiar su lógica:

- `AuthorizedAggregateRepository` para procedencia y derivación de `synthetic=false`;
- `validate_estimates` y `assert_v0_granularity_boundary` para el contrato de filas;
- `quality_rules.py` para CV, N y notas;
- `BigQueryRepository` para consulta parametrizada y `maximum_bytes_billed`;
- lifecycle/cache existentes para promoción, rollback y aislamiento por release/run;
- aserciones Dataform, incluida `stage04_reserved_release_identity`.

Una implementación que reescriba estas reglas dentro de YAML, SQL ad hoc o scripts de shell no
satisface la especificación.

## Separación propuesta de workflows

### A. Preparación y reconciliación

Workflow manual y auditable que, después de verificar la autorización de carga:

1. valida entradas y configuración viva;
2. verifica procedencia;
3. carga de forma idempotente;
4. reconcilia bajo cap de bytes;
5. ejecuta los cinco gates;
6. genera evidencia;
7. termina siempre antes de promoción.

### B. Promoción/rollback

Workflow separado, protegido por una segunda decisión explícita. Nunca se invoca automáticamente
al terminar A. Acepta únicamente el release/run y los hashes aprobados por A; cualquier cambio
exige una nueva decisión.

## Registro de decisión propuesto

Se recomienda combinar:

1. un archivo de decisión versionado y revisado por Rita, con acción, release/run, hashes,
   alcance, fecha y commit; y
2. un GitHub Environment protegido para el job que muta cloud.

Un label, comentario libre o variable booleana por sí solos no son evidencia suficiente porque
pueden modificarse sin quedar ligados de manera inmutable al contenido ejecutado.

## Regresión del punto 2.4

La primera corrida automatizada usa el release/run ya aprobado en PR #126 en modo
`RECONCILE_EXISTING`. Debe producir:

- snapshot existente idéntico; ninguna fila duplicada ni sobrescrita;
- 3.014/3.014 filas y 516/516 indicadores;
- mismos hashes, release/run y cinco gates `PASS`;
- mismos bytes procesados con cache desactivada, cap de 10 MiB y mismo comportamiento fail-closed;
- cero promoción, rollback, IAM o cambio de tráfico durante esta corrida.

La regresión desactiva cache para hacer comparable el resultado. Una diferencia de bytes es una
condición `HOLD`: se diagnostica y documenta antes de continuar, aunque las cifras coincidan.

## Gate antes de Etapa 2

Rita aprobó la clasificación y autorizó iniciar la implementación mediante los comentarios del
[Issue #43 sobre el canal](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5738403514)
y el [Environment protegido](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5738454716).
La decisión estableció subida manual por corrida y a Rita como única revisora requerida, con
`prevent self-review`. Continúa prohibido crear un transporte alternativo por inferencia.

Las decisiones cubren:

- clasificación de esta tabla;
- registro de decisión trazable y Environment protegido;
- entrada manual, exclusivamente por corrida;
- inicio de la implementación de Etapa 2.

La API de `workflow_dispatch` no ofrece un input de tipo archivo. Rita resolvió el transporte en
la [revisión del PR #130](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/130):
un runner autoalojado exclusivo recibe una copia local por corrida. Como GitHub vacía
`RUNNER_TEMP` al inicio del job, un hook posterior a esa limpieza mueve la copia desde un inbox
local restringido y un hook final elimina ambas copias. No se utilizan artifacts previos,
Releases, URLs, secretos, commits, buckets o Drive como reemplazo no autorizado.

La preparación continúa fail-closed si falta cualquiera de los dos archivos. La regresión
`RECONCILE_EXISTING` y toda mutación cloud permanecen separadas y todavía no se ejecutan.

El alcance permanece `CONTROLLED_SHADOW`: sin acceso público, publicación institucional, cutover,
sustitución de V0 ni aumento de presupuesto o del cap de consulta.
