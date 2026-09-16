# C0 — preprueba sintética de navegación del catálogo

**Estado:** `C0_MANUAL_TRAVERSAL_PENDING; SUPERVISORY_REVIEW_REQUIRED`
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

Esta tabla debe completarse durante una ejecución humana desde la pantalla inicial. La persona
recibe solo el prompt correspondiente, no usa ayuda externa y confirma un indicador. No se deriva
ninguna clasificación hasta terminar las siete tareas.

| Tarea | Módulo / alcance | Inicio | Fin | Segundos | Seleccionado | Esperado | PASS/FAIL | Ayuda | Observaciones |
|---|---|---|---|---:|---|---|---|---|---|
| C0-01 | 3.1 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_31_031` | PENDIENTE | Ninguna | PENDIENTE |
| C0-02 | 3.2 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_32_032` | PENDIENTE | Ninguna | PENDIENTE |
| C0-03 | 3.3 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_33_033` | PENDIENTE | Ninguna | PENDIENTE |
| C0-04 | 3.4 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_34_034` | PENDIENTE | Ninguna | PENDIENTE |
| C0-05 | 3.5 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_35_035` | PENDIENTE | Ninguna | PENDIENTE |
| C0-06 | 3.6 / Nacional | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_36_036` | PENDIENTE | Ninguna | PENDIENTE |
| C0-07 | 3.2 / Departamento | PENDIENTE | PENDIENTE | — | PENDIENTE | `SYN_C0_32_086` | PENDIENTE | Ninguna | PENDIENTE |

**Clasificación C0:** `PENDIENTE_DE_RECORRIDO_MANUAL`.
