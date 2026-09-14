# Contrato local de `indicator_estimates`

- Estado: `CANDIDATE_LOCAL_SHADOW`
- Cloud: `BLOCKED_BY_CLOUD_GATE`
- Escritura: histórica e inmutable por `release_id` y `run_id`
- Prohibición: no se permite `WRITE_TRUNCATE` sobre releases aprobados

Este contrato describe resultados poblacionales agregados. No admite microdatos ni identificadores
de personas. Los ejemplos son seguros y no constituyen nombres de recursos reales.

## Clasificación de entradas locales

- `demo_indicator_estimates.csv` es un fixture 100 % sintético, didáctico y sin uso institucional.
- `v0_authorized_indicator_estimates.csv` contiene exclusivamente un corte agregado V0 autorizado,
  no sintético, sin microdatos y ligado a su manifiesto y al inventario aprobado en el PR #53.
- En el flujo institucional, `synthetic=false` no es un dato aceptado del CSV ni de quien llama.
  `AuthorizedAggregateRepository` lo deriva únicamente después de verificar el nombre y SHA-256
  del agregado contra el manifiesto, la clasificación del manifiesto y la presencia del hash de
  origen en el registro V0 aprobado. El adaptador institucional exige esa clasificación interna.
- Ninguna de estas entradas constituye datos institucionales publicados; publicación y cutover
  permanecen no autorizados.
- BigQuery, DDL, Cloud Run y todo recurso cloud permanecen `BLOCKED_BY_CLOUD_GATE`.

| Campo | Tipo | Obligatorio | Significado | Ejemplo seguro | Validación | Procedencia |
|---|---|---:|---|---|---|---|
| `release_id` | STRING | Sí | Identifica el release candidato | `enares2024-crs04-v0-shadow-001` | No vacío; inmutable | Registro shadow local |
| `run_id` | STRING | Sí | Identifica una ejecución | `sprint041-local-golden` | Único dentro del release | Ejecución local |
| `source_version` | STRING | Sí | Versión lógica de la fuente | `v0_official_drive_baseline` | Catálogo versionado | Manifiesto V0 |
| `source_hash` | STRING(64) | Sí | SHA-256 de la fuente agregada | `15B845...D0BB4` | Hexadecimal de 64 caracteres | Manifiesto V0 aprobado |
| `git_commit_sha` | STRING(40) | Sí | Código que produjo o incorporó la fila | `0000000000000000000000000000000000000000` | Hexadecimal de 40 caracteres | Git |
| `container_image_digest` | STRING | Condicional | Imagen de una futura corrida | `BLOCKED_BY_CLOUD_GATE` | Digest válido o marcador bloqueado | Pipeline futuro |
| `dataform_release` | STRING | Condicional | Release Dataform asociado | `BLOCKED_BY_CLOUD_GATE` | Release conocido o marcador bloqueado | Pipeline futuro |
| `engine_version` | STRING | Sí | Motor que originó el resultado | `v0_csv` | Valor del catálogo | Ingesta agregada local |
| `scale` | ENUM | Sí | Escala de los campos estadísticos | `0_100` | `0_1` o `0_100` | Manifiesto y fuente agregada |
| `indicator_id` | STRING | Sí | Identificador estable del indicador | `VF_HOGAR` | Existe en diccionario | Diccionario V0 |
| `indicator_name` | STRING | Sí | Etiqueta aprobada | `VF_HOGAR` | Coincidencia exacta | Diccionario V0 |
| `disaggregation` | STRING | Sí | Dimensión de la fila | `Nacional` | Combinación autorizada | CSV y diccionario V0 |
| `category` | STRING | Sí | Categoría dentro de la dimensión | `Total` | No vacía | CSV V0 |
| `estimate` | FLOAT64 | Condicional | Estimación agregada | `16.7432981789` | Dentro de la escala; NULL si suprimida | CSV V0 |
| `standard_error` | FLOAT64 | Condicional | Error estándar | `0.5115056857` | Mayor o igual que cero; NULL si suprimida | CSV V0 |
| `ci95_lower` | FLOAT64 | Condicional | Límite inferior IC95 % | `15.7396510021` | Menor o igual al estimate; NULL si suprimida | CSV V0 |
| `ci95_upper` | FLOAT64 | Condicional | Límite superior IC95 % | `17.7469453558` | Mayor o igual al estimate; NULL si suprimida | CSV V0 |
| `cv` | FLOAT64 | Condicional | Coeficiente de variación | `0.0305498762` | Mayor o igual que cero; NULL si suprimida | CSV V0 |
| `n_unweighted` | INT64 | Condicional | N no ponderado del denominador | `18807` | Entero mayor o igual que cero; NULL si suprimida | CSV V0 |
| `weighted_population` | FLOAT64 | Condicional | Población ponderada cuando la fuente la entrega | `NULL` | Mayor o igual que cero; NULL permitido en V0 legado | Fuente agregada |
| `cv_flag` | BOOL | Sí | Señal de revisión por CV | `false` | Coherente con regla versionada | Validador de calidad |
| `n_flag` | BOOL | Sí | Señal de revisión por N | `false` | Coherente con regla versionada | Validador de calidad |
| `suppress_flag` | BOOL | Sí | Control principal de no exposición | `false` | Si true, estimate, SE, IC95, CV, N y weighted_population son NULL | Control de privacidad |
| `quality_note` | STRING | Sí | Explicación de calidad | `Estimación referencial por precisión reducida` | No vacía cuando hay alerta | Validador y ADR |
| `validation_status` | ENUM | Sí | Estado de validación | `PENDING` | `PENDING`, `PASSED`, `FAILED` o `APPROVED` | Ops local |
| `created_at` | TIMESTAMP | Sí | Fecha UTC de creación | `2026-09-04T00:00:00Z` | ISO-8601 UTC | Ejecución local |

## Llave e invariantes

Para el adaptador V0 del Corte 2, `n_unweighted` procede exclusivamente de `base_unw`:
cuenta los casos no ponderados del denominador. `target_unw` cuenta los casos de la
categoría analizada y `n_unw` legado no se usa como sustituto. Si falta `base_unw`,
la adaptación falla; no se infiere N. Correspondencia aclarada explícitamente por la
usuaria y contrastada con las columnas del agregado de Drive. Esta correspondencia
fue aprobada como fuente de N no ponderado. No autoriza por sí sola supresión: la
confidencialidad conserva un gate independiente.

La llave candidata es `release_id + run_id + indicator_id + disaggregation + category`.
No puede haber duplicados. Un release aprobado nunca se sobrescribe: una corrección crea otro
`run_id` o release y conserva el registro anterior. El piloto usa `engine_version = v0_csv`,
`validation_status = PENDING` y un `release_id` explícitamente shadow.

## Decisiones metodológicas vigentes

La decisión supervisora del 2026-09-13 aplica a los módulos 3.1–3.6. `CV > 0.15` —o `CV > 15`
si la unidad declarada es porcentaje— conserva la prevalencia visible, la marca referencial y
añade la nota aprobada. `base_unw < 30` conserva la prevalencia visible y añade la alerta aprobada.
La igualdad exacta no activa flags y un estadístico ausente permanece ausente. `cv_flag` y
`n_flag` nunca activan `suppress_flag`; cualquier supresión requiere la política independiente de
confidencialidad. La tolerancia golden `1e-9` continúa siendo un control técnico, no una regla de
calidad ni confidencialidad.

Un cero exacto observado con `base_unw` presente, error estándar 0 e intervalo [0, 0] es una
salida completa aunque `cv` sea `null`: el CV es el cociente 0/0 y por tanto indefinido. Se
clasifica como `EXACT_ZERO_CV_UNDEFINED`, conserva la estimación cero y recibe una nota explícita.
No se confunde con una fila incompleta por otra causa. Esta regla contractual no levanta por sí
sola los gates D02/D10 ni autoriza su presentación numérica.

La validación genérica no exige que cada catálogo reproduzca los tres estados didácticos. La
cobertura simultánea de `PUBLISHABLE_CANDIDATE`, `REFERENCE_HIGH_CV` y
`SUPPRESSED_EXERCISE` pertenece exclusivamente al fixture demo.
