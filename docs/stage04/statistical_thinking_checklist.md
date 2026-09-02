# Checklist de razonamiento estadístico — corte vertical 3.2

**Issue:** #44 — V0 y contratos  
**Rama:** `feat/stage04-v0-contracts`  
**Estado:** `DRAFT_LOCAL_ONLY — METHODOLOGICAL_REVIEW_REQUIRED`  
**Módulo:** 3.2 — Violencia en el hogar

## 1. Alcance y fuentes

Este checklist documenta dos filas reales de la baseline agregada V0 y un caso sintético de
interfaz para supresión. No cambia la V0 oficial, no autoriza publicación y no carga datos a
BigQuery.

Fuentes recuperables:

- CSV V0 lógico `tabulados_crs04_long_v0.csv`, SHA-256
  `919C3F39C7681E71596CBC904369FBE6CD0B85D02FC9DC4D0AF36DF7845EC8FC`;
- diccionario lógico `diccionario_indicadores.csv`, SHA-256
  `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C`;
- productor lógico `tabulados_crs04_v0.R`, SHA-256
  `259E75A52E9A8299F5C79A55583C2E964D323E30BEAA39E175EE0E552EC5F5CC`;
- sintaxis declarada por el diccionario: `03/08/08b_CRS03_CRS04_3.2*.sps`.

Los campos `pct`, `es`, `ci_low` y `ci_high` están expresados en puntos porcentuales
(escala 0–100). `cv` es una razón; por ejemplo, `0.03055` equivale aproximadamente a 3.055 %.
`n_unw` es el denominador no ponderado, no una población estimada.

## 2. Diseño muestral común

- Unidad visible: estimación agregada, nunca un registro individual.
- Estrato: `CCDD`.
- PSU: `ID`.
- Peso: `FACTOR_ALUMNOS`.
- Configuración: una etapa, `nest=TRUE`.
- Contrato validado: 25 estratos, 1,115 PSU y 1,090 grados de libertad.
- `ID_AULA` se conserva para auditoría y no se usa como segunda etapa.
- Missing: `SYSMIS/NULL` se trata según la sintaxis SPSS; R usa `na.rm` dentro del
  dominio aplicable.

## 3. Caso A — candidato publicable

### Identificación y pregunta

- Indicador: `VF_HOGAR`.
- Corte: `Nacional — Total`.
- Pregunta que responde: ¿cuál es la prevalencia ponderada del indicador materializado
  `VF_HOGAR` entre los casos válidos del diseño muestral?
- Interpretación sustantiva provisional: indicador de violencia física en el hogar del módulo
  3.2. La redacción pública exacta y el periodo de referencia deben confirmarse contra la
  sintaxis SPSS y el cuestionario; no se infieren solo a partir del nombre técnico.

### Numerador, denominador y estimación

- Numerador: registros válidos con `VF_HOGAR == 1`, ponderados por `FACTOR_ALUMNOS`.
- Denominador: casos válidos del diseño muestral según la sintaxis aprobada.
- Estimación: `16.7432981789 %`.
- Error estándar: `0.5115056857` puntos porcentuales.
- IC95 % Wald: `[15.7407654570 %, 17.7458309009 %]`.
- CV: `0.0305498762` (aprox. `3.055 %`).
- N no ponderado: `18,807`.

### Calidad e interpretación

- Clasificación de trabajo: `CANDIDATE_PUBLICABLE`.
- Razón: CV menor que el umbral provisional `0.15` y N mayor que `30`.
- Advertencia: los umbrales todavía requieren aprobación metodológica; esta clasificación no
  equivale a publicación institucional.
- Afirmación permitida: la estimación agregada V0 para este corte es aproximadamente 16.74 %,
  sujeta a la definición y al periodo de referencia aprobados.
- Afirmación no permitida: que 16.74 % de cada departamento, escuela o grupo individual tenga
  el mismo resultado, o que exista cambio causal o longitudinal.
- Riesgo de interpretación: confundir N no ponderado con población ponderada o presentar la
  etiqueta técnica `VF_HOGAR` sin su definición sustantiva aprobada.
- Texto breve propuesto: `Estimación nacional agregada. Consulte universo, periodo, IC95 % y
  estado de calidad antes de interpretarla.`

## 4. Caso B — candidato referencial por CV alto

### Identificación y pregunta

- Indicador: `VF_HOGAR_01`.
- Corte: `Departamento — LAMBAYEQUE`.
- Pregunta que responde: ¿cuál es la prevalencia ponderada del subindicador materializado
  `VF_HOGAR_01` en el corte departamental de Lambayeque, entre los casos válidos?
- Interpretación sustantiva provisional: la forma concreta representada por el sufijo `_01`
  debe recuperarse de la sintaxis/cuestionario antes de mostrar una etiqueta pública.

### Numerador, denominador y estimación

- Numerador: registros válidos con `VF_HOGAR_01 == 1`, ponderados por
  `FACTOR_ALUMNOS`, dentro del dominio departamental.
- Denominador: casos válidos del diseño muestral en Lambayeque.
- Estimación: `0.3595933827 %`.
- Error estándar: `0.2498258491` puntos porcentuales.
- IC95 % Wald V0: `[-0.1300562840 %, 0.8492430494 %]`.
- CV: `0.6947454018` (aprox. `69.475 %`).
- N no ponderado: `651`.

### Calidad e interpretación

- Clasificación de trabajo: `REFERENTIAL_PROVISIONAL`.
- Razón: CV muy superior al umbral provisional `0.15`; N no es bajo.
- El límite inferior negativo proviene del IC Wald V0 y no representa una prevalencia física
  negativa. La interfaz debe aplicar el contrato de presentación aprobado sin alterar la
  evidencia histórica.
- Afirmación permitida: el CSV V0 contiene una estimación muy imprecisa para este corte.
- Afirmación no permitida: ordenar departamentos, afirmar diferencias o comunicar `0.36 %`
  como una cifra precisa.
- Riesgo de interpretación: ocultar la gran incertidumbre por mostrar demasiados decimales o
  usar únicamente la estimación puntual.
- Texto breve propuesto: `Resultado referencial por alta imprecisión (CV elevado). No usar para
  comparaciones ni rankings.`

## 5. Caso C — demostración sintética de supresión

La baseline V0 revisada contiene 215 filas vinculadas a los cinco indicadores 3.2 presentes en
el CSV. Ninguna tiene `n_unw < 30`, ninguna trae un campo de estado de supresión y el umbral de
CV no es una regla de confidencialidad. Por ello no se etiqueta falsamente una fila real como
suprimida.

Para probar localmente el comportamiento de la interfaz se define un caso exclusivamente
sintético:

- ID: `DEMO_32_SUPPRESSED_CELL`.
- Módulo: `3.2`.
- Corte: `Departamento — DEMO`.
- Estimación histórica sintética: `2.0 %`.
- Error estándar sintético: `0.9` puntos porcentuales.
- IC95 % sintético: `[0.24 %, 3.76 %]`.
- CV sintético: `0.45`.
- N no ponderado sintético: `20`.
- Estado de presentación: `SUPPRESSED_DEMO`.
- Regla de prueba: la interfaz, tooltip, tabla y exportación no muestran estimación, error,
  intervalo, CV ni N; solo muestran una nota de supresión.
- Uso permitido: test de presentación y privacidad con datos inequívocamente sintéticos.
- Uso prohibido: comparación con V0, evidencia de una regla institucional o publicación como
  resultado ENARES.

Este caso debe reemplazarse por una regla y un ejemplo aprobados por supervisión antes de que
un estado `SUPPRESSED` forme parte del contrato productivo.

## 6. Desagregaciones y límites

Las dimensiones declaradas en el diccionario no autorizan cruces arbitrarios. El corte nacional
y el corte departamental anteriores se leen tal como existen en el CSV V0. Stage 04 no suma
prevalencias, no reconstruye denominadores desde microdatos y no interpreta ausencia como cero.

Antes de una etiqueta pública deben confirmarse:

1. redacción sustantiva y periodo de referencia de `VF_HOGAR` y `VF_HOGAR_01`;
2. correspondencia exacta de la categoría `_01` con cuestionario/sintaxis;
3. conjunto final de desagregaciones autorizadas;
4. fuente y aprobación de umbrales CV/N;
5. regla de supresión primaria y complementaria.

## 7. Recordatorio de gobernanza temporal

Se permite continuar únicamente con documentación, contratos, tests y fixtures sintéticos
locales. Antes de la primera carga BigQuery, creación de recursos, cambio IAM, despliegue o PR
que pretenda habilitarlos, se debe detener el trabajo y completar:

- aprobación independiente del inventario V0 en el issue #44;
- responsable y autorización de IAM/coste;
- decisión firmada `READY_FOR_STAGE04_SHADOW` en `PRE_STAGE04.md`.

