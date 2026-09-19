# Contrato local de la vista `published`

- Estado: `CANDIDATE_LOCAL_SHADOW`
- Cloud: `BLOCKED_BY_CLOUD_GATE`

`published` es la única superficie que una aplicación puede leer. Contiene exclusivamente
resultados agregados que pertenecen a un release `APPROVED`; nunca contiene microdatos,
identificadores personales, variables de diseño ni rutas a fuentes privadas.

## Reglas

1. `current_release` debe apuntar a un release `APPROVED` antes de exponerlo y la vista debe fijar
   literalmente la misma combinación `release_id + run_id` mediante las variables operativas
   `publishedReleaseId` y `publishedRunId`.
2. Cada fila conserva `release_id`, versión de fuente, estado y notas de calidad.
3. Una celda suprimida mantiene su etiqueta y estado, pero expone como NULL `estimate`,
   `standard_error`, `ci95_lower`, `ci95_upper`, `cv`, `n_unweighted` y
   `weighted_population`.
4. La supresión se materializa en la capa published candidata; no puede ser solo visual.
5. No se publican combinaciones ausentes del catálogo ni filas con `FAILED`.
6. La aplicación no abre CSV privados, Drive ni `survey_input`.
7. `suppress_flag` es el control principal de nulificación; el estado visual debe ser coherente,
   pero no sustituye al flag como barrera de seguridad.
8. La vista consulta una sola tabla física. No une `outputs` con `current_release`: BigQuery cobra
   un mínimo de 10 MiB por tabla consultada y esa unión haría imposible respetar el límite
   obligatorio de 10 MiB por consulta. El puntero y la definición fija de la vista se verifican
   como un par durante promoción y rollback.

## Proyección segura mínima

`release_id`, `source_version`, `indicator_id`, `indicator_name`, `disaggregation`, `category`,
campos estadísticos protegidos, flags, `quality_note`, `validation_status` y `created_at`.

La creación de una vista real en BigQuery permanece `BLOCKED_BY_CLOUD_GATE`.

## Origen de `outputs.indicator_estimates`

`outputs.indicator_estimates` se carga exclusivamente desde el extracto agregado V0 autorizado,
encadenado mediante SHA-256 al padre congelado y a los manifiestos aprobados. Nunca se deriva de
`analytical`, `cleaned`, `raw` ni `survey_input`.

La razón de autoridad es que V0 constituye la salida oficial congelada. La reproducción SQL de
`analytical` continúa en revisión de sintaxis fuente y su cobertura no equivale a los 516
indicadores. Por ello, `analytical` sirve únicamente para verificación de migración, y las
aserciones `*_v0_parity` comprueban la construcción exacta de variables fila por fila, no los
estimadores ponderados.

Todavía no existe en Dataform una comparación agregada de porcentaje, error estándar e intervalo
de confianza contra las tabulaciones V0 congeladas. Si `analytical` se usa como contraste, primero
debe existir esa aserción. Toda diferencia se registra en `known_discrepancies.md` y vuelve al
productor; nunca sustituye la cifra V0.

Cambiar este origen requiere una decisión supervisora explícita. No puede hacerse mediante
configuración, una variable de Dataform ni la interfaz.

La nulificación de campos protegidos es un control técnico local implementado. Para 3.1–3.6,
`CV > 15 %` produce una estimación visible, referencial y con nota; `base_unw < 30` produce una
estimación visible con alerta. Ninguna de estas señales activa `suppress_flag`. La publicación de
nuevas cifras y la política independiente de confidencialidad continúan sujetas a sus gates.

El fixture demo es 100 % sintético. El corte golden V0 es un agregado autorizado, no sintético y
sin microdatos. Ninguno equivale a datos institucionales publicados. BigQuery, DDL, Cloud Run y
los demás recursos cloud continúan `BLOCKED_BY_CLOUD_GATE`.
