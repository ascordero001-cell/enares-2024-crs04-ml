# C0 — preprueba sintética de navegación del catálogo

**Estado:** `C0_ARCHITECTURE_INSUFFICIENT; SUPERVISORY_REVIEW_REQUIRED`
**Alcance:** exclusivamente sintético; no conecta ni reproduce cifras V0
**Gate posterior:** PR B no comienza hasta clasificar formalmente el resultado C0

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

C2 repetirá este mismo recorrido manual con revisión de accesibilidad, evaluación heurística y
recorrido cognitivo. No requiere participantes independientes. AppTest comprueba únicamente que
la ruta funcional existe y no decide el umbral humano ni la clasificación de C0.

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

**Clasificación C0:** `ARCHITECTURE_INSUFFICIENT`.
