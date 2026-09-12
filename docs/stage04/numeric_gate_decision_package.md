# Paquete de decisiones — gate numérico de Sprint 04.2

**Estado:** `PROPOSED_FOR_SUPERVISORY_REVIEW`  
**Alcance:** preparación local desconectada; no autoriza cifras nuevas, exportación ni cloud  
**Issues:** [#48](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/48) y [#49](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/49)  
**Revisora requerida:** `ritaricaldi-cpu`  
**Fecha del paquete:** `2026-09-12`

## Fuentes congeladas

| Clave | Fuente y versión | SHA-256 aprobado | Uso |
|---|---|---|---|
| V0-TAB | `tabulados_crs04_long.csv`, V0 oficial | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` | Estadísticas agregadas; 3014 filas |
| V0-DIC | `diccionario_indicadores.csv`, V0 oficial | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | Definición; 516 indicadores |

La baseline y su aprobación están en [v0_drive_hash_manifest.md](v0_drive_hash_manifest.md). No se
recalcularon resultados de Stage 03 ni se modificaron CSV o manifests. Para todas las familias,
`estimate`, `SE` e `IC95 %` usan la escala 0–100; `CV` se conserva como proporción. `N no
ponderado` procede exclusivamente de `base_unw`; `target_unw` se conserva separado y jamás lo
sustituye.

## Propuestas transversales

- `CV > 0.15`, `N < 30` y tolerancia absoluta `1e-9` permanecen propuestas, no política.
- Ningún flag se rellena con `false` por defecto. Hasta una decisión explícita: `cv_flag = null`,
  `n_flag = null`, `suppress_flag = null` y `quality_status =
  PENDING_METHODOLOGICAL_DECISION`.
- La autorización debe enumerar `indicator_id`, dimensión y categorías o una regla de alcance
  inequívoca. Un centinela no autoriza el módulo.
- Una estadística ausente permanece `null`. Una salida incompleta se muestra solo como contexto,
  sin tarjeta, tabla numérica ni exportación.
- `Área × sexo` de UI solo podría mapear a `Área y sexo` de V0, e `Idioma del hogar` a `Lengua
  materna`, después de aprobación semántica explícita. Mientras tanto quedan bloqueadas.

## Tabla de decisiones por familia y excepción

Las fuentes de todas las filas son `V0-TAB + V0-DIC`. “Campos” enumera la expectativa del contrato;
la evidencia puntual está enlazada en la última columna.

| Caso | Módulo e indicator_id | Alcance: dimensión/categoría | Universo, dominio, numerador y denominador | Tipo diccionario → salida | Campos | Propuesta de calidad y UI | Pruebas preparadas | Decisión requerida y evidencia |
|---|---|---|---|---|---|---|---|---|
| D01 | 3.1 `Componentes` | `Tareas del hogar`; 10 categorías observadas | CRS04 válido; sin dominio adicional; `special(tarea1_fem)` / casos válidos | special → prevalence | completos por fila | Adaptador `components-special-prevalence-v1`; mantener bloqueado y sin métricas hasta validar semántica de categorías | acepta adaptador nombrado; rechaza discrepancia sin adaptador | Aprobar tipo, categorías y adaptador. [Conciliación 3.1](reconciliation_module_31.md) |
| D02 | 3.4 `VP_VF_VS_HOGAR` | Departamento / Cusco y Huancavelica | CRS04 válido; sin dominio adicional; indicador == 1 / casos válidos | prevalence → prevalence | `CV` ausente; demás presentes | Conservar `CV=null`; estado incompleto; mostrar contexto sin métrica | conserva ausencias; rechaza salida completa con campos nulos | Decidir si se excluye o admite presentación parcial. [Conciliación 3.4](reconciliation_module_34.md) |
| D03 | 3.5 `PV_condicional_con_VS` | Condicional; 2 categorías | CRS04 válido; sin dominio adicional; `special(PV_hogar_escuela1)` / casos válidos | special → prevalence | completos | Adaptador específico; bloqueado hasta aprobar interpretación | discrepancia exige adaptador nombrado | Aprobar adaptador/alcance. [Conciliación 3.5](reconciliation_module_35.md) |
| D04 | 3.5 `Solap_VP_VF_E` | Condicional y Prevalencia (contexto); 4 filas | CRS04 válido; sin dominio adicional; `special(VP_VF_E)` / casos válidos | special → prevalence/incomplete | 2 filas de contexto sin SE/IC/CV | Separar contexto de estimación completa; contexto no numérico | conserva nulos y evita métricas | Aprobar taxonomía y tratamiento de contexto. [Conciliación 3.5](reconciliation_module_35.md) |
| D05 | 3.5 `Solap_VP_VF_H` | Condicional y Prevalencia (contexto); 4 filas | CRS04 válido; sin dominio adicional; `special(VP_VF_HOGAR)` / casos válidos | special → prevalence/incomplete | 2 filas de contexto sin SE/IC/CV | Igual a D04, con adaptador propio | conserva nulos y evita métricas | Aprobar taxonomía y tratamiento de contexto. [Conciliación 3.5](reconciliation_module_35.md) |
| D06 | 3.5 `Solap_VS_12M` | 2×2 y 3×3; 8 categorías | CRS04 válido; sin dominio adicional; `special(VS_ICVAC_301)` / casos válidos | special → prevalence | completos | Adaptador matricial propio; no reinterpretar celdas | discrepancia exige adaptador nombrado | Aprobar semántica de celdas/alcance. [Conciliación 3.5](reconciliation_module_35.md) |
| D07 | 3.5 `Solap_VS_VIDA` | 2×2 y 3×3; 8 categorías | CRS04 válido; sin dominio adicional; `special(VS_ICVAC_301_VIDA)` / casos válidos | special → prevalence | completos | Adaptador matricial propio; no reinterpretar celdas | discrepancia exige adaptador nombrado | Aprobar semántica de celdas/alcance. [Conciliación 3.5](reconciliation_module_35.md) |
| D08 | 3.5 `num_consecuencias_fisicas` | Nacional; 7 categorías | CRS04 válido; sin dominio adicional; `special(CONS_NUM_CONSECUENCIAS)` / casos válidos | special → distribution | completos | Adaptador de distribución; ubicar en Consecuencias, no Acumulación | tipo completo separado y adaptador requerido | Aprobar categorías y navegación. [Conciliación 3.5](reconciliation_module_35.md) |
| D09 | 3.5 `CONS_ATENCION_SALUD` | Dimensiones observadas; categorías catalogadas | CRS04 válido; sin dominio adicional; indicador == 1 / casos válidos | prevalence → prevalence | completos | Mantener en Consecuencias; no hereda autorización del centinela de Acumulación | alcance exacto rechaza dimensión/categoría ajena | Aprobar alcance separado. [Conciliación 3.5](reconciliation_module_35.md) |
| D10 | 3.6 `C3P242_10`, `C3P242_5`, `C4P258_7`, `ayuda_vs_car` | Nacional; categoría original de cada fila | Dominios institucionales respectivos; indicador == 1 / `base_unw` del dominio | prevalence → incomplete | estimate=0, target=0, CV ausente; SE/IC según fuente | Conservar cero y `CV=null`; estado explícito `ZERO_EVENT_CV_UNDEFINED_PENDING`; sin tarjeta hasta decisión | nulo conservado; cero no se convierte en ausencia ni CV=0 | Aprobar estado y presentación. [Conciliación 3.6](reconciliation_module_36.md) |
| D11 | 3.3 `C3P223_10_1`, 3.4 `Agresor_VS_12M__AG_01`, 3.6 `C3P213` y demás salidas solo nacionales | Exclusivamente Nacional/categorías originales | Universo y dominio propios del diccionario; `base_unw` como denominador no ponderado | prevalence → prevalence | completos salvo excepciones registradas | No fabricar Sexo, Área, Departamento u otra dimensión | rechaza dimensión y categoría fuera de alcance | Aprobar individualmente cada indicador/categoría. Informes 3.3, 3.4 y 3.6 |
| D12 | Familias con `Área y sexo` o `Lengua materna` | Posibles etiquetas UI `Área × sexo` e `Idioma del hogar` | Sin cambio estadístico; equivalencia solo de presentación | mismo tipo | según familia | Mantener etiqueta original o bloquear alias hasta revisión semántica | alcance exacto rechaza alias no autorizado | Aprobar o rechazar cada equivalencia. [Matriz de módulos](module_indicator_dimension_matrix.md) |

## Cobertura de pruebas preparatorias

| Escenario | Estado | Evidencia |
|---|---|---|
| N solo desde `base_unw`; sin fallback a `target_unw` | TESTED_SYNTHETIC | `tests/test_stage04_candidate_adapter.py` |
| Ausencias sin imputación y sin métrica | TESTED_SYNTHETIC | mismo archivo |
| prevalence/distribution/special/incomplete y rechazos | TESTED_SYNTHETIC | mismo archivo |
| Escala, SE, IC, CV y N | TESTED_SYNTHETIC | mismo archivo |
| Alcance por indicador/dimensión/categoría | TESTED_SYNTHETIC | mismo archivo |
| Golden 3.2 y vínculo SHA | TESTED_BASELINE | mismo archivo y pruebas golden existentes |
| Nulificación de todos los campos protegidos | TESTED_SYNTHETIC | mismo archivo y `tests/test_stage04_ui_guards.py` |
| Total/margen con una celda oculta | TESTED_SYNTHETIC_REJECTED | mismo archivo |
| Cruce con dos celdas ocultas | TESTED_SYNTHETIC_NO_UNIQUE_RECONSTRUCTION | mismo archivo |
| Mezcla de releases | TESTED_SYNTHETIC_REJECTED | `tests/test_stage04_module_coverage.py` |
| Reconstrucción multitabla o multirelease | TEST_PENDING | Requiere política de vínculo aprobada |
| AppTest: combinaciones pendientes/ausentes sin métricas | TESTED | `tests/test_stage04_ui_guards.py` |
| AppTest: demo sintético separado de V0 autorizado | TESTED | `tests/test_stage04_ui_guards.py` |

## Decisiones concretas solicitadas

1. Aprobar, ajustar o rechazar los adaptadores D01 y D03–D08, incluidos tipo y categorías.
2. Definir el tratamiento UI de D02, D04, D05 y D10 sin imputar estadísticas.
3. Aprobar o reemplazar las propuestas `CV > 0.15`, `N < 30` y `1e-9`, indicando unidad de CV.
4. Definir `cv_flag`, `n_flag`, `suppress_flag`, `quality_status` y `quality_note` por familia.
5. Autorizar alcances exactos por indicador/dimensión/categorías; no por módulo implícito.
6. Resolver las equivalencias de etiquetas de D12.
7. Definir política contra reconstrucción multitabla y multirelease.

Hasta esas decisiones, `NUMERIC_DATA_GATE_OPEN`; solo 3.2 / `VF_HOGAR` / Nacional / Total continúa
como golden numérico local autorizado.
