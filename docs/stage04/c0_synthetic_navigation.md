# C0 — preprueba sintética de navegación del catálogo

**Estado:** `ARCHITECTURE_SUFFICIENT; SUPERVISORY_REVIEW_REQUIRED`
**Alcance:** exclusivamente sintético; no conecta ni reproduce cifras V0
**Gate posterior:** C3 precede a C2; PR B no comienza hasta aprobar el nuevo recorrido

## Fixture único

El fixture determinístico compartido por aplicación, script y pruebas contiene exactamente 516
indicadores: 86 por cada módulo 3.1–3.6. Las etiquetas sintéticas reproducen longitud, prefijos
repetidos, paréntesis anidados y variantes casi duplicadas. Cada módulo incluye 80 entradas
nacionales y seis departamentales. Los nombres de departamento, estimaciones, N, CV y registros
individuales no aparecen.

## Protocolo congelado para C0 y C2

C0 y C2 usan las mismas siete tareas, el mismo inicio, el mismo final y el mismo límite:

- **Inicio:** la persona o AppTest recibe solo el texto de la tarea y abre la pantalla inicial del
  prototipo funcional Streamlit.
- **Ruta permitida:** seleccionar módulo, seleccionar dimensión, escribir términos en la búsqueda
  visible, revisar varios candidatos plausibles, seleccionar uno y pulsar **Confirmar indicador**.
- **Ayuda permitida:** solo el texto de la tarea; no se entrega el `indicator_id` ni se permite ayuda
  externa.
- **Final:** el `indicator_id` objetivo aparece solo después de la confirmación explícita.
- **Umbral previo:** máximo 90 segundos por tarea.
- **Fallo:** objetivo incorrecto, más de un resultado sin resolver, excepción o tiempo mayor a 90
  segundos.

C2 aplicará este mismo protocolo manual con objetivos no utilizados previamente, revisión de
accesibilidad, evaluación heurística y recorrido cognitivo. No requiere participantes
independientes. AppTest comprueba únicamente que la ruta funcional existe y no decide el umbral
humano ni la clasificación de C0.

Resultados posibles:

1. `ARCHITECTURE_SUFFICIENT`: las siete tareas completan la ruta y cumplen el umbral.
2. `BOUNDED_IMPROVEMENTS_FOR_C3`: completan la ruta, pero se documentan mejoras acotadas.
3. `ARCHITECTURE_INSUFFICIENT`: alguna tarea falla; vuelve a supervisión.

## Tareas congeladas

La persona que realiza el recorrido recibe únicamente el prompt. La consulta técnica y el ID
esperado permanecen separados en el fixture de regresión y no forman parte de la ayuda humana.

| Tarea | Prompt humano definitivo |
|---|---|
| C0-01 | En el módulo 3.1 y alcance nacional, localiza el indicador sobre corresponsabilidad cotidiana en adolescentes de 12 a 17 años, alguna vez, para el ámbito urbano. |
| C0-02 | En el módulo 3.2 y alcance nacional, localiza el indicador sobre corresponsabilidad cotidiana en adolescentes de 12 a 17 años durante los últimos 12 meses, para el ámbito rural. |
| C0-03 | En el módulo 3.3 y alcance nacional, localiza el indicador sobre apoyo y acompañamiento entre estudiantes que buscaron ayuda, alguna vez, para el total del ámbito observado. |
| C0-04 | En el módulo 3.4 y alcance nacional, localiza el indicador sobre apoyo y acompañamiento entre estudiantes que buscaron ayuda durante los últimos 12 meses, para el ámbito urbano. |
| C0-05 | En el módulo 3.5 y alcance nacional, localiza el indicador sobre respuesta institucional entre estudiantes que buscaron ayuda, alguna vez, para el ámbito rural. |
| C0-06 | En el módulo 3.6 y alcance nacional, localiza el indicador sobre respuesta institucional entre estudiantes que buscaron ayuda durante los últimos 12 meses, para el total del ámbito observado. |
| C0-07 | En el módulo 3.2 y alcance departamental, localiza el indicador sobre barreras para pedir ayuda en comunidad educativa entrevistada durante los últimos 12 meses, para el ámbito rural. |

## Ejecución reproducible

```powershell
python scripts/run_stage04_c0_navigation.py
python -m pytest tests/test_stage04_c0_navigation.py -q
```

La regresión de AppTest abre la aplicación, comprueba los controles, obtiene varios candidatos,
selecciona explícitamente el objetivo, pulsa la confirmación y verifica que el ID esté oculto antes
de confirmar y visible después. Su duración es rendimiento técnico complementario y no se compara
con el umbral humano. Este documento no autoriza PR B, cloud, publicación ni cutover por sí solo.

## Regresión funcional AppTest

Ejecución del 2026-09-15 con AppTest sobre el prototipo Streamlit y el fixture de 516 entradas:

| Tarea | Tiempo AppTest (s) | Resultado funcional |
|---|---:|---|
| C0-01 | 0,322 | PASS |
| C0-02 | 0,203 | PASS |
| C0-03 | 0,203 | PASS |
| C0-04 | 0,204 | PASS |
| C0-05 | 0,205 | PASS |
| C0-06 | 0,211 | PASS |
| C0-07 | 0,192 | PASS |

## Recorrido manual cronometrado C0

Ejecución realizada por Ana el 2026-09-16 UTC desde la pantalla inicial. Ana recibió únicamente
cada prompt, no consultó el ID esperado, la consulta técnica ni el fixture y no utilizó ayuda
externa. El tiempo se midió conservadoramente desde la entrega del prompt hasta la recepción del
resultado confirmado; por ello incluye el tiempo de copiar y enviar el resultado y constituye una
cota superior del tiempo de navegación.

| Tarea | Módulo / alcance | Inicio | Fin | Segundos | Seleccionado | Esperado | PASS/FAIL | Ayuda | Observaciones |
|---|---|---|---|---:|---|---|---|---|---|
| C0-01 | 3.1 / Nacional | 02:18:15 | 02:19:50 | 94,8 | `SYN_C0_31_017` | `SYN_C0_31_031` | FAIL | Ninguna | Selección incorrecta y tiempo mayor a 90 s. |
| C0-02 | 3.2 / Nacional | 02:21:35 | 02:23:04 | 89,2 | `SYN_C0_32_032` | `SYN_C0_32_032` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C0-03 | 3.3 / Nacional | 02:23:04 | 02:24:09 | 65,2 | `SYN_C0_33_033` | `SYN_C0_33_033` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C0-04 | 3.4 / Nacional | 02:24:09 | 02:24:57 | 48,3 | `SYN_C0_34_034` | `SYN_C0_34_034` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C0-05 | 3.5 / Nacional | 02:24:57 | 02:27:37 | 159,5 | `SYN_C0_35_035` | `SYN_C0_35_035` | FAIL | Ninguna | Objetivo correcto; tiempo mayor a 90 s. |
| C0-06 | 3.6 / Nacional | 02:27:37 | 02:29:27 | 109,7 | `SYN_C0_36_036` | `SYN_C0_36_036` | FAIL | Ninguna | Objetivo correcto; tiempo mayor a 90 s. |
| C0-07 | 3.2 / Departamento | 02:29:27 | 02:30:09 | 42,2 | `SYN_C0_32_086` | `SYN_C0_32_086` | PASS | Ninguna | Objetivo correcto dentro del límite. |

Resultado: cuatro tareas PASS y tres FAIL. C0-01 seleccionó un indicador incorrecto; además,
C0-01, C0-05 y C0-06 excedieron el límite conservador de 90 segundos. Una tarea incorrecta basta
para aplicar la salida congelada de retorno a supervisión.

**Clasificación aplicada al primer recorrido:** `ARCHITECTURE_INSUFFICIENT`.

## Dictamen supervisor y análisis causal

Rita [reclasificó el resultado](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/102#issuecomment-5691319296)
el 2026-09-16 como `BOUNDED_IMPROVEMENTS_FOR_C3`. La evidencia original no cambia: 4/7 PASS, con selección
incorrecta en C0-01 y dos tareas correctas pero lentas. El dictamen concluyó que las dificultades
eran acotadas y ordenó ejecutar C3 antes de C2. PR B permanece detenido.

El análisis de C0-01 separa las tres hipótesis solicitadas:

- **Candidatos demasiado parecidos: confirmado.** «Corresponsabilidad» aparecía en el título
  general del módulo 3.1 y por ello coincidía con filas cuyo tema diferenciador era otro. La
  búsqueda incluía texto ya representado por el selector de módulo.
- **Falta de contexto antes de confirmar: confirmado.** El selector presentaba una etiqueta larga
  en una sola línea. Población, periodo y ámbito no tenían controles separados, y el resumen de
  confirmación aparecía solo después de revelar el ID.
- **Prompt humano: no confirmado como causa.** El prompt contenía tema, población, periodo y
  ámbito suficientes para distinguir el objetivo. El problema estaba en cómo la interfaz usaba y
  presentaba esos datos.

Las mejoras acotadas de C3 son:

1. la búsqueda libre vuelve a operar sobre la etiqueta completa visible;
2. las coincidencias en tema, población, periodo y ámbito se ordenan antes que las coincidencias
   que proceden únicamente del texto genérico del módulo;
3. tema, población, periodo y ámbito aparecen como refinadores opcionales;
4. los resultados omiten el prefijo repetido del módulo y muestran los cuatro atributos en orden
   estable;
5. antes de confirmar se presenta un resumen semántico, mientras el `indicator_id` continúa
   oculto;
6. la regresión exige múltiples candidatos tras la búsqueda amplia y exactamente uno después de
   aplicar los refinadores.

## Segundo recorrido posterior a C3

Los siete objetivos originales están quemados y no se reutilizan. El segundo recorrido usa siete
objetivos distintos —uno por módulo y uno departamental— y conserva el protocolo de 90 segundos,
sin ayuda externa y desde la pantalla inicial. Los IDs y consultas técnicas permanecen separados
de estos prompts humanos.

| Tarea | Prompt humano nuevo |
|---|---|
| C3-01 | En el módulo 3.1 y alcance nacional, localiza el indicador sobre experiencias reportadas en adolescentes de 12 a 17 años durante los últimos 12 meses, para el total del ámbito observado. |
| C3-02 | En el módulo 3.2 y alcance nacional, localiza el indicador sobre experiencias reportadas en adolescentes de 12 a 17 años, alguna vez, para el ámbito rural. |
| C3-03 | En el módulo 3.3 y alcance nacional, localiza el indicador sobre consecuencias percibidas entre estudiantes que buscaron ayuda durante los últimos 12 meses, para el ámbito rural. |
| C3-04 | En el módulo 3.4 y alcance nacional, localiza el indicador sobre redes de confianza entre estudiantes que no buscaron ayuda, alguna vez, para el total del ámbito observado. |
| C3-05 | En el módulo 3.5 y alcance nacional, localiza el indicador sobre respuesta institucional en hogares con persona adulta de referencia durante los últimos 12 meses, para el ámbito rural. |
| C3-06 | En el módulo 3.6 y alcance nacional, localiza el indicador sobre consecuencias percibidas en hogares con persona adulta de referencia, alguna vez, para el total del ámbito observado. |
| C3-07 | En el módulo 3.4 y alcance departamental, localiza el indicador sobre respuesta institucional en comunidad educativa entrevistada, alguna vez, para el ámbito rural. |

### Corrección supervisora del 2026-09-16

La primera C3-01 quedó anulada porque utilizó la población de 9 a 11 años, exclusiva de CRS03 y
fuera de la autoridad CRS04. El fixture sustituyó esa población y C3-01 quedó redefinida sobre un
objetivo 3.1 nuevo y no usado.

C3-05 fue un fallo real de navegación. El código informado pertenecía a 3.4. Como
`filter_catalog` aplica el módulo antes de construir candidatos, una fila 3.4 no puede aparecer
bajo el selector 3.5: el error fue no cambiar el selector de módulo antes de confirmar, no una
fuga de resultados entre módulos. La repetición conserva el mismo objetivo y prompt.

En la repetición autorizada, la persona llegó al módulo, enfoque, periodo y ámbito correctos, pero
eligió la población «adolescentes de 12 a 17 años» en lugar de «hogares con persona adulta de
referencia». Este segundo fallo, ahora dentro del módulo correcto, confirma que el problema no se
limita al selector de módulo y requiere revisión supervisora de la arquitectura de selección.

La evidencia previa se preserva:

| Tarea | Resultado previo | Tratamiento |
|---|---|---|
| C3-01 | 52,6 s; `SYN_C0_31_012`; PASS técnico | ANULADO por objetivo fuera de la autoridad CRS04. |
| C3-05 | 43,2 s; `SYN_C0_34_068`; FAIL | Fallo de selección; repetición autorizada con el mismo objetivo. |

La tabla combinada conserva los cinco primeros intentos válidos e incorpora las dos repeticiones
autorizadas. El tiempo se mide desde la entrega de cada prompt por chat hasta la recepción del
código confirmado e incluye su copia y envío.

| Tarea | Inicio UTC | Fin UTC | Segundos | Seleccionado | Esperado | PASS/FAIL | Ayuda | Observaciones |
|---|---|---|---:|---|---|---|---|---|
| C3-01 | 19:04:38 | 19:05:03 | 25,0 | `SYN_C0_31_024` | `SYN_C0_31_024` | PASS | Ninguna | Objetivo nuevo correcto dentro del límite. |
| C3-02 | 03:44:20 | 03:45:27 | 67,2 | `SYN_C0_32_023` | `SYN_C0_32_023` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C3-03 | 03:45:32 | 03:46:32 | 59,3 | `SYN_C0_33_044` | `SYN_C0_33_044` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C3-04 | 03:46:39 | 03:47:40 | 61,5 | `SYN_C0_34_057` | `SYN_C0_34_057` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C3-05 | 19:06:38 | 19:07:17 | 38,9 | `SYN_C0_35_020` | `SYN_C0_35_068` | FAIL | Ninguna | Módulo, enfoque, periodo y ámbito correctos; población incorrecta: adolescentes de 12 a 17 años en vez de hogares con persona adulta de referencia. |
| C3-06 | 03:48:37 | 03:49:26 | 49,5 | `SYN_C0_36_075` | `SYN_C0_36_075` | PASS | Ninguna | Objetivo correcto dentro del límite. |
| C3-07 | 03:49:32 | 03:50:17 | 45,7 | `SYN_C0_34_083` | `SYN_C0_34_083` | PASS | Ninguna | Objetivo correcto dentro del límite. |

**Resultado combinado:** 6/7 tareas PASS; las siete finalizaron dentro de 90 segundos y sin ayuda.

**Salida C3:** `ARCHITECTURE_INSUFFICIENT`. De acuerdo con la clasificación predefinida, el fallo
de C3-05 devuelve el flujo a supervisión. C2 y PR B continúan detenidos hasta recibir una decisión
supervisora explícita.

## Corrección acotada posterior a la aprobación del PR #108

La revisión supervisora del 2026-09-16 aprobó el registro técnico, mantuvo la clasificación
`ARCHITECTURE_INSUFFICIENT` y autorizó una corrección específica antes de repetir únicamente
C3-05:

1. el orden de candidatos usa evidencia ponderada de la consulta en tema, población, ámbito,
   periodo y categoría; los empates conservan el orden canónico y nunca se resuelven ordenando
   alfabéticamente la población;
2. Tema, Población, Periodo y Ámbito se estrechan progresivamente, por lo que cada elección elimina
   valores incompatibles de los refinadores siguientes.

### Tercera ejecución autorizada de C3-05

| Inicio UTC | Fin UTC | Segundos | Seleccionado | Esperado | PASS/FAIL | Ayuda | Observaciones |
|---|---|---:|---|---|---|---|---|
| 19:48:37 | 20:29:01 | 2424,7 | `SYN_C0_35_068` | `SYN_C0_35_068` | ANULADO | Ninguna | Objetivo correcto; el cronómetro midió una ausencia y no una navegación continua. |

La decisión supervisora del 2026-09-16 anuló esta medición: no se clasifica como PASS ni FAIL. La
ruta corregida permitió confirmar el objetivo exacto, pero el tiempo no representa el uso de la
interfaz. La evidencia combinada permanece en 6/7 hasta una medición continua.

### Cuarta ejecución autorizada de C3-05

El inicio técnico de las 20:40:50 UTC se anuló antes de navegar porque la pestaña del prototipo se
cerró. Tras reabrir `8504` en la pantalla inicial se inició una medición nueva y continua:

| Inicio UTC | Fin UTC | Segundos | Seleccionado | Esperado | PASS/FAIL | Ayuda | Observaciones |
|---|---|---:|---|---|---|---|---|
| 20:41:41 | 20:42:23 | 41,8 | `SYN_C0_35_068` | `SYN_C0_35_068` | PASS | Ninguna | Objetivo exacto confirmado dentro del límite de 90 segundos. |

Al sustituir únicamente la medición fallida de C3-05 por el recorrido limpio posterior a la
corrección, la evidencia combinada queda en **7/7 PASS**. Los cinco primeros intentos válidos,
C3-01 corregida y C3-05 corregida cumplen el umbral y no utilizaron ayuda externa.

**Salida C3:** `ARCHITECTURE_SUFFICIENT; SUPERVISORY_REVIEW_REQUIRED`. C2 y PR B permanecen
detenidos hasta que esta evidencia sea revisada y el PR de registro quede aprobado y fusionado.
