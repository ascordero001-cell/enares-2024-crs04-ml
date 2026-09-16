# C0 — preprueba sintética de navegación del catálogo

**Estado:** `C0_PROVISIONAL_ARCHITECTURE_SUFFICIENT; SUPERVISORY_REVIEW_REQUIRED`  
**Alcance:** exclusivamente sintético; no conecta ni reproduce cifras V0  
**Gate posterior:** PR B no comienza hasta clasificar formalmente el resultado C0

## Criterio congelado para C0 y C2

Las siete tareas siguen la misma ruta: seleccionar módulo, seleccionar dimensión y buscar por
palabras distintivas. Una tarea pasa cuando devuelve exactamente un indicador, sin recorrer una
lista completa. Se registra el tiempo por tarea. C0 mide tiempo de resolución del filtro en máquina;
C2 deberá medir además tiempo humano extremo a extremo con participantes independientes. El tiempo
de máquina no se presenta como evidencia de usabilidad humana.

Resultados posibles:

1. `ARCHITECTURE_SUFFICIENT`: las siete tareas resuelven un objetivo único; puede comenzar PR B.
2. `BOUNDED_IMPROVEMENTS_FOR_C3`: resuelven, pero se documentan mejoras acotadas posteriores.
3. `ARCHITECTURE_INSUFFICIENT`: alguna tarea no resuelve de forma única; vuelve a supervisión.

## Tareas congeladas

| Tarea | Alcance | Patrón sintético reproducido |
|---|---|---|
| C0-01 | 3.1 / Nacional | etiqueta con prefijo temático y paréntesis |
| C0-02 | 3.2 / Nacional | prefijo repetido y periodo entre paréntesis |
| C0-03 | 3.3 / Nacional | prefijo paralelo al módulo 3.2 |
| C0-04 | 3.4 / Nacional | etiqueta larga y periodo |
| C0-05 | 3.5 / Nacional | categorías cercanas y paréntesis |
| C0-06 | 3.6 / Nacional | etiqueta larga con actor entre paréntesis |
| C0-07 | 3.2 / Departamento | mismo indicador con alcance departamental sintético |

Los identificadores comienzan con `SYN_C0_`; no contienen estimaciones, N, CV, nombres de personas,
departamentos reales ni registros individuales.

## Ejecución reproducible

```powershell
python scripts/run_stage04_c0_navigation.py
python -m pytest tests/test_stage04_c0_navigation.py -q
```

La decisión C0 se registrará con la salida medida del runner y la revisión del PR. Este documento no
autoriza PR B, cloud, publicación ni cutover por sí solo.

## Resultado local reproducido

Ejecución del 2026-09-15 en Python 3.12; cada tiempo es la mediana de 1.000 resoluciones del filtro:

| Tarea | Tiempo mediano (ms) | Resultado |
|---|---:|---|
| C0-01 | 0,0048 | PASS — objetivo único |
| C0-02 | 0,0072 | PASS — objetivo único |
| C0-03 | 0,0080 | PASS — objetivo único |
| C0-04 | 0,0066 | PASS — objetivo único |
| C0-05 | 0,0064 | PASS — objetivo único |
| C0-06 | 0,0074 | PASS — objetivo único |
| C0-07 | 0,0084 | PASS — objetivo único |

Resultado provisional: `ARCHITECTURE_SUFFICIENT`. La búsqueda por tokens tolera mayúsculas y
acentos, y el orden módulo → dimensión → búsqueda evita recorrer la lista completa. Este resultado
requiere revisión supervisora y no sustituye las mediciones humanas de C2.
