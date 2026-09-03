# Checklist de razonamiento estadístico — corte vertical 3.2

- **Estado:** `PUERTA_B_REVIEW_REQUESTED`
- **Alcance:** `LOCAL_SHADOW_ONLY`
- **Fuente:** `tabulados_crs04_long.csv` y `diccionario_indicadores.csv` V0 leídos directamente
  desde Drive privado y fijados por `docs/stage04/v0_drive_hash_manifest.md`
- **Indicador piloto:** `VF_HOGAR`, Nacional, Total

Los valores de V0 que aparecen aquí son evidencia agregada para revisión shadow; no constituyen
publicación institucional. No se consultaron microdatos ni se recalcularon estimaciones.

## 1. Indicador piloto nacional: `VF_HOGAR`

| Control | Evidencia y explicación |
|---|---|
| Pregunta de vigilancia | ¿Qué prevalencia estimada de adolescentes del alcance CRS04 experimenta violencia física en el hogar, conforme a la variable materializada y al contrato V0? |
| Población y periodo | Adolescentes de 12 a 17 años del alcance CRS04, ENARES 2024. |
| Universo operativo | Casos válidos del diseño muestral para `VF_HOGAR`; el diccionario no declara una variable de dominio adicional para esta fila. |
| Numerador | Casos con `VF_HOGAR == 1`. |
| Denominador | Casos válidos del diseño muestral. En la fila nacional V0, `base_unw = 18,807`. |
| `0/1/NULL` y saltos | `1` integra numerador y denominador; `0` integra solo el denominador; `NULL`/`SYSMIS` se excluye mediante `na.rm` dentro del dominio. El contrato no registra una regla de salto adicional para este indicador. |
| Diseño | Peso `FACTOR_ALUMNOS`, estrato `CCDD`, PSU `ID`, `nest = TRUE`; 25 estratos, 1,115 PSU, 1,090 grados de libertad. `ID_AULA` es solo de auditoría. |
| Estadística | Prevalencia en escala 0–100: `16.7432981789`; SE `0.5115056857`; IC95 % Wald `[15.7396510021, 17.7469453558]`; CV `0.0305498762`; N no ponderado reportado `18,807`; conteo no ponderado del numerador `3,134`. |
| Desagregaciones admisibles | Las registradas para `VF_HOGAR` en el diccionario: Nacional; Sexo; Área; Área y sexo; Lengua materna; Discapacidad; Etnicidad; Tipo de hogar; Departamento y dimensiones temáticas expresamente listadas. No se muestra una combinación ausente del contrato. |
| Afirmación permitida | “En la estimación nacional V0 de ENARES 2024, la prevalencia agregada de `VF_HOGAR` es 16.74 %, con IC95 % de 15.74 % a 17.75 %.” |
| Afirmación no permitida | No identifica personas, no prueba causalidad, no describe trayectorias longitudinales, no autoriza comparar universos distintos y no representa a edades fuera de CRS04. |
| Riesgo y texto para la aplicación | Riesgo: leer el porcentaje como conteo individual o como cifra exacta sin incertidumbre. Texto: “Estimación poblacional agregada; revisar IC95 %, CV, N, universo y denominador. Datos V0 en validación shadow.” |

### Explicación en lenguaje claro

El 16.74 % no significa que se haya contado a todas las personas de la población ni permite
buscar quién respondió. Es una estimación poblacional ponderada. El error estándar y el intervalo
describen su incertidumbre; el CV relaciona el error estándar con la estimación. El N mostrado es
no ponderado y no debe confundirse con población proyectada. La lectura solo es válida para el
universo y el periodo indicados.

## 2. Tres decisiones de visualización para la PUERTA B

No existe todavía una regla institucional aprobada de publicación o supresión. Para practicar el
razonamiento se aplica provisionalmente `CV > 0.15` como señal referencial y `N < 30` como señal
de supresión. Estas reglas son ejemplos técnicos pendientes de aprobación metodológica; no
cambian el estado de las filas V0.

### Caso A — candidato publicable

- Fila: `VF_HOGAR / Nacional / Total` (V0 agregada real).
- Estimate 16.7433; SE 0.5115; IC95 % [15.7397, 17.7469]; CV 0.03055; N 18,807.
- Decisión provisional: `PUBLISHABLE_CANDIDATE`, porque no activa los ejemplos técnicos de CV
  ni N.
- Presentación: valor, IC95 %, CV, N, universo, denominador y etiqueta SHADOW visibles.
- Límite: “candidato” no equivale a publicación institucional ni a reemplazo de V0.

### Caso B — referencial por CV alto

- Fila: `VF_HOGAR_01 / Departamento / Lambayeque` (V0 agregada real).
- Estimate 0.3596; SE 0.2498; IC95 % Wald [-0.1306, 0.8498]; CV 0.69475;
  N no ponderado del denominador 651; conteo no ponderado del numerador 2.
- Decisión provisional: `REFERENCE_HIGH_CV`, porque `0.69475 > 0.15`.
- Presentación: no destacar ni ordenar como ranking; acompañar con “estimación imprecisa” y toda
  la evidencia de incertidumbre. El límite inferior negativo es una consecuencia del IC Wald y
  no una prevalencia negativa observable.
- Límite: el conteo de numerador bajo refuerza la cautela, pero no se convierte aquí en una regla
  institucional de supresión.

### Caso C — celda suprimida de ejercicio

- Fila: ejemplo **totalmente sintético** del módulo 3.2; no procede del CSV V0 y no representa
  ningún territorio ni grupo real.
- Valores de prueba: estimate 12.0; SE 4.0; IC95 % [4.16, 19.84]; CV 0.3333; N 24.
- Decisión provisional: `SUPPRESSED_EXERCISE`, porque `N = 24 < 30` bajo la regla técnica de
  práctica. La interfaz mostraría “Suprimido” sin estimate, intervalo ni conteo.
- Propósito: demostrar el estado visual requerido sin atribuir una supresión inexistente a V0.
- Límite: no es evidencia empírica y no debe entrar en comparaciones, totales ni exports.

## 3. Reconstrucción conceptual del resultado

1. El diccionario fija variable, numerador, denominador, missing, método de IC y dimensiones.
2. El diseño Stage 03 aplica `ID`, `CCDD`, `FACTOR_ALUMNOS` y `nest = TRUE`.
3. El productor R calcula estimate, SE, IC95 %, CV y conteos y escribe el CSV integrado V0.
4. Stage 04 lee esa fila agregada por hash; no consulta microdatos ni recalcula el indicador.
5. La decisión visual depende de una regla de calidad separada. Por ahora las decisiones de los
   tres casos son didácticas y provisionales.

## 4. Autoevaluación y parada

- Puedo reconstruir el denominador del piloto: casos válidos no missing; N no ponderado 18,807.
- Puedo explicar el IC95 % como rango de incertidumbre del estimador, no como rango de valores
  individuales.
- Puedo distinguir N no ponderado, conteo del numerador y estimate ponderado.
- Puedo explicar que CV es `SE / estimate` en la misma escala.
- No puedo declarar una regla institucional de publicación o supresión sin aprobación.
- No avanzaré a contratos, golden, seguridad, interfaz ni réplica 3.1–3.6 hasta que supervisión
  revise esta PUERTA B.

## 5. Solicitud de revisión

Se solicita confirmar:

1. que `VF_HOGAR / Nacional / Total` es un piloto adecuado;
2. que universo, denominador y tratamiento de missing están interpretados correctamente;
3. que los casos A–C son suficientes para el ejercicio formativo;
4. qué regla institucional sustituirá, si corresponde, los umbrales provisionales.

