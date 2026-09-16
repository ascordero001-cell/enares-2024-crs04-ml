# C0 — preprueba sintética de navegación del catálogo

**Estado:** `C0_PROVISIONAL_ARCHITECTURE_SUFFICIENT; SUPERVISORY_REVIEW_REQUIRED`
**Alcance:** exclusivamente sintético; no conecta ni reproduce cifras V0
**Gate posterior:** PR B no comienza hasta clasificar formalmente el resultado C0

## Fixture único

El fixture determinístico compartido por aplicación, script y pruebas contiene exactamente 516
indicadores: 86 por cada módulo 3.1–3.6. Las etiquetas sintéticas reproducen longitud, prefijos
repetidos, paréntesis anidados y variantes casi duplicadas. Cada módulo incluye 85 entradas
nacionales y una departamental. Los nombres de departamento, estimaciones, N, CV y registros
individuales no aparecen.

## Protocolo congelado para C0 y C2

C0 y C2 usan las mismas siete tareas, el mismo inicio, el mismo final y el mismo límite:

- **Inicio:** la persona o AppTest recibe solo el texto de la tarea y abre la pantalla inicial del
  prototipo funcional Streamlit.
- **Ruta permitida:** seleccionar módulo, seleccionar dimensión, escribir términos en la búsqueda
  visible y seleccionar el resultado.
- **Ayuda permitida:** solo el texto de la tarea; no se entrega el `indicator_id` ni se permite ayuda
  externa.
- **Final:** el `indicator_id` objetivo aparece como único resultado seleccionado en pantalla.
- **Umbral previo:** máximo 90 segundos por tarea.
- **Fallo:** objetivo incorrecto, más de un resultado sin resolver, excepción o tiempo mayor a 90
  segundos.

C2 repetirá este protocolo con revisión manual de accesibilidad, evaluación heurística y recorrido
cognitivo. No requiere participantes independientes. El tiempo automatizado de AppTest en C0
demuestra que la ruta funcional completa existe; no se presenta como tiempo humano.

Resultados posibles:

1. `ARCHITECTURE_SUFFICIENT`: las siete tareas completan la ruta y cumplen el umbral.
2. `BOUNDED_IMPROVEMENTS_FOR_C3`: completan la ruta, pero se documentan mejoras acotadas.
3. `ARCHITECTURE_INSUFFICIENT`: alguna tarea falla; vuelve a supervisión.

## Tareas congeladas

| Tarea | Alcance | Consulta visible | Objetivo |
|---|---|---|---|
| C0-01 | 3.1 / Nacional | `corresponsabilidad repetido 031` | `SYN_C0_31_031` |
| C0-02 | 3.2 / Nacional | `hogar repetido 032 12 meses` | `SYN_C0_32_032` |
| C0-03 | 3.3 / Nacional | `escuela repetido 033` | `SYN_C0_33_033` |
| C0-04 | 3.4 / Nacional | `sexual repetido 034 12 meses` | `SYN_C0_34_034` |
| C0-05 | 3.5 / Nacional | `solapamiento repetido 035` | `SYN_C0_35_035` |
| C0-06 | 3.6 / Nacional | `barreras acceso repetido 036` | `SYN_C0_36_036` |
| C0-07 | 3.2 / Departamento | `hogar repetido 086 12 meses` | `SYN_C0_32_086` |

## Ejecución reproducible

```powershell
python scripts/run_stage04_c0_navigation.py
python -m pytest tests/test_stage04_c0_navigation.py -q
```

El benchmark aislado del filtro puede conservarse como evidencia complementaria, pero no decide el
gate. La decisión se basa en las siete rutas completas de Streamlit y requiere nueva revisión
supervisora. Este documento no autoriza PR B, cloud, publicación ni cutover por sí solo.

## Reejecución local

Ejecución del 2026-09-15 con AppTest sobre el prototipo Streamlit y el fixture de 516 entradas:

| Tarea | Tiempo de ruta (s) | Umbral (s) | Resultado |
|---|---:|---:|---|
| C0-01 | 0,223 | 90 | PASS |
| C0-02 | 0,101 | 90 | PASS |
| C0-03 | 0,104 | 90 | PASS |
| C0-04 | 0,104 | 90 | PASS |
| C0-05 | 0,103 | 90 | PASS |
| C0-06 | 0,105 | 90 | PASS |
| C0-07 | 0,098 | 90 | PASS |

Resultado provisional: `ARCHITECTURE_SUFFICIENT` (7/7). Los tiempos corresponden a automatización
funcional de la ruta Streamlit; C2 conservará el umbral y la secuencia al realizar la revisión
manual de accesibilidad, la evaluación heurística y el recorrido cognitivo.
