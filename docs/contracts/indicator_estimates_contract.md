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
| `quality_note` | STRING | Sí | Explicación de calidad | `Umbrales provisionales` | No vacía | Validador y ADR |
| `validation_status` | ENUM | Sí | Estado de validación | `PENDING` | `PENDING`, `PASSED`, `FAILED` o `APPROVED` | Ops local |
| `created_at` | TIMESTAMP | Sí | Fecha UTC de creación | `2026-09-04T00:00:00Z` | ISO-8601 UTC | Ejecución local |

## Llave e invariantes

La llave candidata es `release_id + run_id + indicator_id + disaggregation + category`.
No puede haber duplicados. Un release aprobado nunca se sobrescribe: una corrección crea otro
`run_id` o release y conserva el registro anterior. El piloto usa `engine_version = v0_csv`,
`validation_status = PENDING` y un `release_id` explícitamente shadow.

## Decisiones metodológicas vigentes

Los flags existen técnicamente y viajan con cada resultado, pero su regla institucional no está
aprobada. `CV > 0.15`, `N < 30` y la tolerancia golden `1e-9` son propuestas didácticas o técnicas
pendientes de supervisión. El ADR-005 identifica responsables pendientes y evidencia requerida;
ningún test local puede convertirlas en política institucional.

La validación genérica no exige que cada catálogo reproduzca los tres estados didácticos. La
cobertura simultánea de `PUBLISHABLE_CANDIDATE`, `REFERENCE_HIGH_CV` y
`SUPPRESSED_EXERCISE` pertenece exclusivamente al fixture demo.
