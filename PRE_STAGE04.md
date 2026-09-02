# PRE-STAGE04 — Puerta de preparación antes del documento principal

**Proyecto:** ENARES 2024 CRS04
**Repositorio objetivo:** [`ascordero001-cell/enares-2024-crs04-ml`](https://github.com/ascordero001-cell/enares-2024-crs04-ml)
**Propietaria de implementación:** Ana Silvia Cordero Ricaldi
**Fecha de verificación en vivo:** 2026-08-25
**Documento que habilita:** `CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md`

## 1. Propósito

Este archivo se ejecuta **una sola vez antes de comenzar el MD principal**. Su función es dejar
preparados identidad, repositorio, gates, numeración real de issues, revisión, archivos de inicio
y límites de seguridad. No contiene el trabajo analítico de Stage 04 y no sustituye sus sprints.

La salida de este pre-stage es una decisión `READY_FOR_STAGE04_SHADOW` o `NOT_READY`. `READY` solo
autoriza desarrollo controlado en shadow; no autoriza publicación institucional, reemplazo de V0,
cutover ni gasto cloud no aprobado.

## 2. Estado confirmado en GitHub

La gráfica del [perfil de Ana](https://github.com/ascordero001-cell?tab=overview&from=2026-08-01&to=2026-08-25)
es evidencia secundaria de actividad. Los gates se prueban con PR, CI, documentos firmados y
commits del repositorio.

| Control | Estado verificado | Evidencia |
|---|---|---|
| PR de gobernanza y handoff | **MERGED** el 2026-08-24 | [PR #41](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/41), merge `0e95c349a638f6fc0e80528255d42ff62f042f4c` |
| Estado Stage 03 | **PASS** | [`stage3_pass.md`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/blob/main/docs/stage03/stage3_pass.md) |
| Supervisión metodológica | **APPROVED** | [`stage03_supervisor_acceptance.md`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/blob/main/docs/stage03/stage03_supervisor_acceptance.md) |
| Handoff a Ana | **ACCEPTED_FOR_SHADOW_DEVELOPMENT** | [`stage04_handoff.md`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/blob/main/docs/stage03/stage04_handoff.md) |
| Cierre técnico | **TECHNICAL_PASS — SHADOW** | [`stage3_closure_report.md`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/blob/main/docs/stage03/stage3_closure_report.md) |
| Discrepancias abiertas | **NINGUNA**; KD-001 está resuelta y documentada | [`known_discrepancies.md`](https://github.com/ascordero001-cell/enares-2024-crs04-ml/blob/main/docs/stage03/known_discrepancies.md) |
| CI posterior al cierre | **SUCCESS** | [GitHub Actions run 32765383664](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/32765383664) |
| `main` revisado | `0a55a7192a381a0964d6a1fd7ceb32e7109e2e38`, merge de PR #42 | [commit](https://github.com/ascordero001-cell/enares-2024-crs04-ml/commit/0a55a7192a381a0964d6a1fd7ceb32e7109e2e38) |
| Estado de publicación | **REMAIN_SHADOW**; V0 continúa oficial | documentos anteriores |
| Protección de `main` | **CONFIGURADA**; PR, aprobación independiente, CI y conversaciones resueltas son obligatorios | protección verificada antes del PR #52 |
| Issues Stage 04 reales | **CREADOS Y MAPEADOS**; paraguas #43 y núcleo #44-#51 | `docs/stage04/issue_map.md` |
| PR de bootstrap Stage 04 | **REVISADO Y MERGED** | [PR #52](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/52), aprobación de `ritaricaldi-cpu`, merge `e381158e377f2d615e5b56cbc4ac8041a68df6ff` |
| CI posterior al merge del bootstrap | **SUCCESS** | [GitHub Actions run 33585101445](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/33585101445) |

### Contrato Stage 03 ya aceptado

- release candidato: `stage03-v0.5-cloud-full`;
- tabla autorizada para shadow:
  `enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5`;
- tamaño contractual: 18,807 filas y proyección explícita de 737 columnas;
- módulos derivados: 3.1-3.6;
- diseño: `ids=~ID`, `strata=~CCDD`, `weights=~FACTOR_ALUMNOS`, `nest=TRUE`;
- 25 estratos, 1,115 PSU y 1,090 grados de libertad;
- `ID_AULA` es auditoría, no segunda etapa del diseño;
- KD-001 `VS_12M — Nacional — Total` está metodológicamente resuelta;
- Stage 04 no reconstruye indicadores de Stage 03 ni presenta V0.5 como publicación oficial.

Ana no debe repetir ni reabrir Stage 03 salvo que el contrato cambie o aparezca nueva evidencia.

## 3. Condiciones de parada

No se inicia el MD principal si ocurre cualquiera de estas situaciones:

- la sesión de GitHub no corresponde a `ascordero001-cell`;
- se trabaja desde el fork `ritaricaldi-cpu` como si fuera el repositorio oficial;
- `main` local no coincide con `origin/main` o hay cambios locales sin identificar;
- falta el enlace o estado de alguno de los gates Stage 03 anteriores;
- se pretende usar un `release_id` distinto sin nuevo handoff;
- los números locales #41-#52 se tratan como números reales de GitHub sin crear los issues;
- no existe revisión independiente ni mecanismo manual documentado mientras `main` está sin
  protección;
- el PR de bootstrap incluye `.sav`, microdatos, credenciales, caches, rutas personales o datos
  reales presentados como fixtures;
- no se conocen las ubicaciones recuperables de los scripts R y CSV V0;
- una acción requiere facturación, IAM o publicación sin autorización supervisora.

Ante una parada, Ana prepara evidencia y solicita supervisión. No intenta resolverla reduciendo
tests, ampliando permisos o haciendo push directo a `main`.

## 4. Paso A — Confirmar cuenta y repositorio

Desde una copia local del repositorio oficial:

```bash
git remote -v
git status --short
git branch --show-current
```

Debe comprobarse:

- `origin` apunta a `ascordero001-cell/enares-2024-crs04-ml`;
- no se está trabajando desde el fork de la supervisora;
- cada archivo modificado es reconocido y pertenece al trabajo actual;
- no existen credenciales o datos fuera del alcance.

Si Ana usa GitHub CLI, puede comprobar la sesión con `gh auth status`. No se copian tokens o
salidas sensibles al issue.

## 5. Paso B — Sincronizar y congelar la línea base

```bash
git switch main
git pull --ff-only origin main
git status --short
git rev-parse HEAD
```

Resultado confirmado para este registro de cierre: `main` en
`e381158e377f2d615e5b56cbc4ac8041a68df6ff`, merge de PR #52, con CI posterior al merge en
verde. Si el SHA
cambió, se registra el nuevo SHA y se vuelve a verificar Stage 03; no se obliga al repositorio a
retroceder al SHA escrito aquí.

Crear una branch de preparación, no de producto:

```bash
git switch -c docs/stage04-bootstrap
```

## 6. Paso C — Establecer colaboración antes del código

### 6.1 Revisión humana

- Ana desarrolla y abre los PR.
- Rita u otra persona designada revisa metodología/gobernanza desde una cuenta distinta.
- La autora no usa su propia aprobación como evidencia independiente.
- Si la revisora necesita permisos, se concede solo el nivel mínimo necesario.

### 6.2 Proteger `main`

Configurar branch protection o ruleset con:

- pull request obligatorio;
- al menos una aprobación independiente;
- checks CI requeridos;
- conversaciones resueltas;
- sin force push ni eliminación de `main`.

Si el plan o permisos no permiten una regla, se documenta la limitación y se aplica revisión
manual obligatoria. `protected=false` no autoriza pushes directos.

## 7. Paso D — Resolver la numeración real de issues

GitHub comparte la misma secuencia numérica para issues y pull requests. En este repositorio
`#41` y `#42` ya son PR; por tanto, los archivos locales `stage04_41.md` a `stage04_52_learning_agent.md`
son **plantillas temáticas**, no números reservados.

Antes del primer PR de implementación:

1. crear el issue paraguas Stage 04;
2. crear los ocho issues núcleo usando las plantillas locales;
3. crear #49-#52 conceptuales solo si se desea conservar los laboratorios opcionales;
4. anotar los números que GitHub asigne realmente;
5. crear `docs/stage04/issue_map.md`;
6. actualizar referencias del documento principal, supervisión y evidencias con los números
   reales;
7. no abrir PR entre creaciones si se pretende conservar números consecutivos, aunque nunca se
   deben predecir antes de que GitHub los asigne.

Plantilla de mapeo:

| Tema local | Número GitHub real | URL | Tipo | Bloqueante |
|---|---:|---|---|---|
| Paraguas Stage 04 | | | núcleo | sí |
| V0 y contratos | | | núcleo | sí |
| Automatización shadow | | | núcleo | sí |
| Auditoría/promoción/rollback | | | núcleo | sí |
| Looker opcional | | | núcleo opcional | no |
| App Streamlit/Cloud Run | | | núcleo | sí |
| Calidad/paridad/privacidad | | | núcleo | sí |
| Runbook/cutover | | | núcleo | sí |
| Documentación/cierre | | | núcleo | sí |
| Buckets | | | learning-lab | no |
| GKE | | | learning-lab | no |
| Airflow | | | learning-lab | no |
| Agent Engine | | | learning-lab | no |

## 8. Paso E — Preparar el paquete Stage 04 para GitHub

El PR `docs/stage04-bootstrap` incorpora como mínimo:

- `PRE_STAGE04.md`;
- documento principal Stage 04;
- hoja arquitectónica;
- `NAMING_CONVENTIONS.md` en la raíz;
- `tests/test_naming.py`;
- registro V0 y plantillas de issues;
- mapa de issues con números reales;
- actualización acotada del README indicando `Stage 04: PREPARING/SHADOW`, nunca `APPROVED`.

Antes de `git add`, eliminar o excluir:

```text
.claude/
.pytest_cache/
__pycache__/
*.pyc
.env
credenciales o claves JSON
rutas personales C:\Users\...
microdatos, .sav y exports reales
```

No se hace `git add .` sin revisar primero `git status --short`.

### 8.1 Ajustar `.gitignore` sin abrir la puerta a datos reales

El `.gitignore` actual excluye globalmente `data/`, `*.csv` y `*.json`. Antes de versionar los
fixtures/golden Stage 04 debe incluir excepciones estrechas, por ejemplo:

```gitignore
!app/data/
!app/data/demo_*.csv
!app/data/demo_*.manifest.json
!tests/golden/
!tests/golden/**/
!tests/golden/**/*.json
```

Solo se fuerzan archivos demostrablemente sintéticos o agregados autorizados. Nunca se usa
`git add -f` para saltar el control sin revisión.

### 8.2 Rutas y nombres canónicos

Los documentos de trabajo dentro de `docs/stage04/` usan `snake_case`; los documentos normativos
de raíz usan `MAYUSCULAS_SNAKE.md`. Si se cambia un nombre al copiar el paquete local al repo, se
actualizan enlaces internos en el mismo PR. No se mantienen dos copias canónicas divergentes.

## 9. Paso F — Verificaciones locales del bootstrap

Desde la raíz del repositorio:

```bash
python -m pytest tests/test_naming.py -q
python -m pytest -q
```

Además:

- revisar el diff completo;
- comprobar enlaces relativos;
- buscar rutas personales, emails, tokens, claves y nombres de archivos sensibles;
- confirmar que todo CSV incluido tiene `synthetic=true` documentado y manifest SHA-256;
- confirmar que ningún `.xlsx` generado se versiona como evidencia sin contrato/autorización;
- confirmar que los MD no dicen que V0.5 está publicado.

## 10. Paso G — Abrir y aprobar el PR de bootstrap

El PR debe incluir:

- objetivo: preparar Stage 04, no implementarla;
- enlace al issue paraguas real;
- lista de archivos;
- salida de tests;
- estado `SHADOW/PREPARING`;
- declaración de ausencia de microdatos/secretos;
- revisión independiente;
- CI verde.

Después del merge:

```bash
git switch main
git pull --ff-only origin main
git status --short
```

No se empieza el PR de código desde una branch antigua anterior al bootstrap.

## 11. Paso H — Confirmar entradas sin mover datos todavía

Ana registra únicamente dónde están y cómo se recuperan:

- scripts R V0 de 3.1-3.6;
- CSV agregados V0 por módulo/desagregación;
- diccionario y sintaxis SPSS de referencia;
- hashes o mecanismo para calcularlos;
- acceso de lectura al contrato Stage 03 aceptado;
- propietario y respaldo de cada artefacto.

Los archivos reales no se copian a GitHub. Completar el inventario técnico, calcular hashes y
cargar candidatos pertenece al primer sprint del MD principal.

## 12. Paso I — Preparar seguridad, coste y supervisión

Antes de crear recursos cloud, registrar:

- proyecto y región GCP autorizados;
- cuenta que controla facturación y presupuesto máximo;
- persona que aprueba IAM y coste;
- cuenta de servicio prevista para la app read-only;
- regla de no usar claves JSON locales;
- datasets permitidos y prohibidos;
- mecanismo de parada y borrado/rollback de recursos candidatos.

### Registro cloud vigente

| Control | Valor registrado | Gate |
|---|---|---|
| Proyecto propuesto | `enares-2024-crs04` | documentado; no creado ni autorizado por este cierre |
| Ubicación BigQuery | `US` | propuesta documentada |
| Región operativa propuesta | `us-central1` | despliegue no autorizado |
| Presupuesto máximo autorizado | `USD 0` | bloquea toda creación o despliegue cloud |
| Responsable de facturación | `PENDIENTE/NO ASIGNADO` | **BLOQUEANTE** |
| Responsable IAM | `PENDIENTE/NO ASIGNADO` | **BLOQUEANTE** |
| Cuenta de servicio prevista | `sa-enares-app-reader@enares-2024-crs04.iam.gserviceaccount.com`; no creada | solo diseño |
| Estado cloud | `NOT_AUTHORIZED` | **BLOQUEANTE** |

Con presupuesto `USD 0` se pueden preparar código, tests, contratos y diseño local. No se crean
cuentas de servicio, bindings IAM, buckets, Cloud Run, GKE, Airflow, Agent Engine ni otros
recursos cloud. La ausencia de responsables reales de facturación e IAM mantiene la decisión
general en `NOT_READY` hasta que se registren o exista una alternativa formalmente aprobada.

No es necesario crear todavía `BigQueryRepository`, Docker, Cloud Run, app CI, supresión
complementaria, evaluación HCI, pruebas de carga o laboratorios #49-#52. Esos son entregables de
Stage 04, no condiciones previas para abrir el documento principal.

## 13. Definition of Ready — autorización para abrir el MD principal

- [x] PR #41 de Stage 03 fusionado.
- [x] Stage 03 `PASS` y supervisión `APPROVED`.
- [x] Handoff aceptado por Ana para desarrollo shadow.
- [x] CI del cierre en verde.
- [x] KD-001 resuelta y ninguna discrepancia abierta.
- [x] V0 continúa oficial y V0.5 permanece shadow.
- [x] Ana trabaja en el repositorio oficial y `main` está sincronizado.
- [x] Branch protection/ruleset funciona o la revisión manual alternativa está documentada.
- [x] Existe revisora independiente con acceso adecuado.
- [x] Issues Stage 04 fueron creados y `issue_map.md` contiene sus números/URLs reales.
- [x] El PR de bootstrap fue revisado, pasó CI y se fusionó.
- [x] `.gitignore` permite solo fixtures/golden sintéticos autorizados.
- [x] `pytest tests/test_naming.py -q` y la suite existente pasan desde el repo real.
- [x] No hay caches, credenciales, rutas personales, microdatos ni exports reales en el PR.
- [x] Se conocen las ubicaciones recuperables de scripts R, CSV V0, sintaxis SPSS y diccionario; sus hashes y metadatos quedan en revisión independiente.
- [ ] Proyecto, región, presupuesto y condiciones de parada están registrados; responsables IAM y facturación: `PENDIENTE/NO ASIGNADO` (**BLOQUEANTE**).
- [ ] Decisión `READY_FOR_STAGE04_SHADOW` firmada abajo.

Si una casilla pendiente no aplica, no se borra: se explica, se asigna responsable y se registra
la alternativa aprobada.

## 14. Registro de decisión

```text
Fecha UTC: 2026-09-02T19:17:00Z
Repositorio: ascordero001-cell/enares-2024-crs04-ml
main SHA: e381158e377f2d615e5b56cbc4ac8041a68df6ff
Stage 03 release: stage03-v0.5-cloud-full
Estado autorizado: SHADOW
Issue paraguas real: #43
PR bootstrap: #52
CI run: 33585101445
Revisora: ritaricaldi-cpu
Estado de versiones: V0 sigue siendo oficial; V0.5 continúa únicamente en shadow
Pendientes bloqueantes: aprobación independiente del inventario V0; responsable de facturación; responsable IAM; revisión y merge del PR de cierre
Decisión: NOT_READY
Firma o aprobación enlazada: aprobación del bootstrap en PR #52; aprobación final del PRE-STAGE 04 pendiente
```

## 15. Primer paso después de READY

Solo después de `READY_FOR_STAGE04_SHADOW`, Ana abre
`CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md` y comienza por:

1. `Paso 0 - Puerta de entrada Stage 03`;
2. Sprint 04.1;
3. issue real equivalente a “V0 y contratos”;
4. branch `feat/stage04-v0-contracts`;
5. corte vertical 3.2;
6. inventario y hashes antes de cualquier carga;
7. PR pequeño, CI y revisión antes de extender a 3.1-3.6.

No comienza por Looker, GKE, Airflow, Agent Engine ni despliegue público.
