# Paquete de decisiones — gate numérico de Sprint 04.2

**Estado:** `QUALITY_RULES_APPROVED; NUMERIC_SCOPE_REVIEW_PENDING`
**Alcance:** preparación local desconectada; no autoriza cifras nuevas, exportación ni cloud
**Issues:** [#48](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/48) y [#49](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/49)
**Revisora requerida:** `ritaricaldi-cpu`
**Fecha del paquete:** `2026-09-13`

La conciliación directa posterior contra las sintaxis primarias entregadas está en
[spss_numeric_gate_reconciliation.md](spss_numeric_gate_reconciliation.md), con identificación
por hash en [spss_source_manifest.md](spss_source_manifest.md). La decisión independiente posterior
está registrada en [supervisory_decisions_20260913.md](supervisory_decisions_20260913.md). La fuente
histórica SPSS se conserva, pero la presentación Stage 04 aplica la decisión vigente de Rita.

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

## Decisiones transversales aprobadas

- En 3.1–3.6, `CV > 0.15` —o `CV > 15` cuando la unidad declarada sea porcentaje— conserva la
  prevalencia visible, la clasifica como referencial y añade la nota aprobada. La igualdad exacta
  al umbral no activa la alerta y un CV ausente permanece ausente.
- En 3.1–3.6, `base_unw < 30` conserva la prevalencia visible y añade la alerta de N pequeño.
  `target_unw` jamás sustituye el denominador. La igualdad exacta a 30 no activa la alerta.
- `cv_flag` y `n_flag` se derivan centralmente. Ninguno activa `suppress_flag`; la confidencialidad
  mantiene política y aprobación independientes. La tolerancia `1e-9` sigue pendiente.
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
| D09 | 3.5 `CONS_ATENCION_SALUD` (atención de salud por consecuencias) | 22 pares exactos del anexo; sin Departamento | `CONS_ALGUNA = 1`; numerador `CONS_ATENCION_SALUD = 1`; denominador de respuestas válidas dentro del dominio; N=`base_unw` condicionado | prevalence → prevalence | completos | Mantener en Consecuencias con dominio visible; no hereda autorización del centinela de Acumulación | equivalencia sintética y contraste estructural R/V0; alcance exacto continúa cerrado | Dominio aprobado; autorizar pares por separado. [Evidencia D09](d09_cons_atencion_salud_domain_evidence.md) |
| D10 | 3.6, cuatro indicadores separados en el anexo | Nacional / Total en cada indicador | Dominio, numerador y denominador específicos del anexo | prevalence → incomplete | estimate=0, SE=0, IC=0–0, target=0 y CV ausente; `base_unw` presente | Conservar cero y `CV=null`; estado candidato `ZERO_EVENT_CV_UNDEFINED_PENDING`; sin métricas | nulo conservado; cero no se convierte en ausencia ni CV=0 | Aprobar estado y presentación. [Conciliación 3.6](reconciliation_module_36.md) |
| D11 | 3.3 `C3P223_10_1`; 3.4 `Agresor_VS_12M__AG_01`; 3.6 `C3P213` | Solo Nacional / Total; ningún otro indicador incluido | Tres definiciones específicas del anexo; `C3P213 == 5`, no regla universal `== 1` | prevalence → prevalence | completos | No fabricar otras dimensiones; alcance cerrado a tres indicadores | pruebas de pares e indicador ajeno | Aprobar cada uno por separado. Informes 3.3, 3.4 y 3.6 |
| D12 | Familias con `Área y sexo` o `Lengua materna` | Posibles etiquetas UI `Área × sexo` e `Idioma del hogar` | Sin cambio estadístico; equivalencia solo de presentación | mismo tipo | según familia | Mantener etiqueta original o bloquear alias hasta revisión semántica | alcance exacto rechaza alias no autorizado | Aprobar o rechazar cada equivalencia. [Matriz de módulos](module_indicator_dimension_matrix.md) |

## Anexo A — alcance explícito contrastado

El anexo se contrastó en modo de solo lectura contra los objetos V0-TAB y V0-DIC identificados por
los hashes aprobados. No registra enlaces ni IDs internos de Drive, y no incorpora valores de
microdatos. Cada elemento `dimensión: categorías` representa únicamente los pares enumerados, no
un producto cartesiano ni una autorización vigente.

- **D01 / Componentes / Tareas del hogar:** Aconsejar y escuchar; Ayudar con tareas escolares;
  Cocinar; Compras mercado; Cuidar hermanas/os; Dar dinero/gastos; Jugar contigo; Lavar
  platos/utensilios; Lavar/planchar ropa; Limpieza.
- **D02 / VP_VF_VS_HOGAR:** Departamento: Cusco, Huancavelica. En ambos pares `estimate=0`,
  `SE=0`, `IC=0–0`, `target_unw=0`, `base_unw` presente y `CV` ausente. El denominador
  estadístico es casos válidos; `base_unw` es el origen separado de N no ponderado.
- **D03 / PV_condicional_con_VS / Condicional:** P(escuela | hogar), con VS; P(hogar | escuela),
  con VS.
- **D04 / Solap_VP_VF_E:** Condicional: P(VF | VP): de quienes sufren VP, % que además sufre VF;
  P(VP | VF): de quienes sufren VF, % que además sufre VP. Prevalencia (contexto): VF (física);
  VP (psicológica). Solo estas dos filas de contexto carecen de SE, IC y CV.
- **D05 / Solap_VP_VF_H:** los mismos cuatro pares y textos de D04 bajo su indicador propio. Solo
  las dos filas de Prevalencia (contexto) carecen de SE, IC y CV.
- **D06 / Solap_VS_12M:** 2×2: P(con contacto (301 o 302) | no física (303)): de no física
  (303), % con con contacto (301 o 302); P(no física (303) | con contacto (301 o 302)): de con
  contacto (301 o 302), % con no física (303). 3×3: P(agresión con contacto (302) | no física
  (303)); P(agresión con contacto (302) | violación (301)) [referencial]; P(no física (303) |
  agresión con contacto (302)); P(no física (303) | violación (301)) [referencial]; P(violación
  (301) | agresión con contacto (302)) [referencial]; P(violación (301) | no física (303))
  [referencial]. Cada etiqueta conserva el texto explicativo “de [denominador], % con
  [numerador]” registrado en la fuente.
- **D07 / Solap_VS_VIDA:** exactamente el mismo conjunto cerrado de dos pares 2×2 y seis pares
  dirigidos 3×3 descrito en D06, aplicado a vida y conservando las etiquetas completas del informe
  versionado; no hereda autorización de D06.
- **D08 / num_consecuencias_fisicas / Nacional:** Cinco consecuencias; Cuatro consecuencias; Dos
  consecuencias; Ninguna; Total; Tres consecuencias; Una consecuencia.
- **D09 / CONS_ATENCION_SALUD:** Discapacidad: 0, 1; Etnicidad: 1, 3, 5, 6, 9; Lengua materna:
  1, 3, 4; Nacional: Total; Sexo: 1, 2; Tipo de hogar: 1, 2, 3; Área: 1, 2; Área y sexo: Rural
  Hombre, Rural Mujer, Urbano Hombre, Urbano Mujer. Son 22 pares; Departamento está excluido.
- **D10 / cuatro solicitudes independientes:** `C3P242_10`: Nacional / Total, numerador
  `C3P242_10 == 1`, dominio y denominador `dom_institucion_escuela == 1`; `C3P242_5`: Nacional /
  Total, numerador `C3P242_5 == 1`, dominio y denominador `dom_institucion_escuela == 1`;
  `C4P258_7`: Nacional / Total, numerador `C4P258_7 == 1`, dominio y denominador
  `dom_institucion_vs == 1`; `ayuda_vs_car`: Nacional / Total, numerador `ayuda_vs_car == 1`,
  dominio y denominador `dom_busco_vs == 1`. En los cuatro, `base_unw` alimenta N; no es el texto
  de la condición del denominador.
- **D11 / tres solicitudes independientes:** `C3P223_10_1`: Nacional / Total, numerador
  `C3P223_10_1 == 1`, dominio y denominador `VP_ESCUELA == 1`; `Agresor_VS_12M__AG_01`:
  Nacional / Total, numerador `Agresor_VS_12M__AG_01 == 1`, dominio y denominador `VS_12M == 1`;
  `C3P213`: Nacional / Total, numerador `C3P213 == 5`, dominio y denominador
  `dom_no_recibio_hogar == 1`. Ninguna “demás salida” pertenece a D11.
- **D12a:** etiqueta original `Área y sexo`; alias UI propuesto `Área × sexo`; pendiente por cada
  indicador y sus categorías. **D12b:** etiqueta original `Lengua materna`; alias UI propuesto
  `Idioma del hogar`; pendiente por cada indicador y sus categorías. Ningún alias se registra como
  par permitido antes de la decisión.

## Anexo B — opciones, recomendación y registro de decisión

| Casos | Opciones para revisión | Recomendación preparatoria | quality_note propuesta | Estado / revisora / fecha / evidencia |
|---|---|---|---|---|
| D01, D03 | rechazar; aceptar como prevalencia con semántica especial; pedir rediseño | Validar primero significado/categorías; un `adapter_id` solo identifica trabajo futuro | `SPECIAL_SOURCE_TYPE_REQUIRES_APPROVED_ADAPTER` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| D04, D05 | excluir contexto; mostrar contexto no numérico; autorizar presentación parcial | Contexto no numérico, sin métricas, hasta decisión | `CONTEXT_ROW_MISSING_SE_CI_CV` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| D06, D07 | excluir; adaptar matriz completa; autorizar subconjunto explícito | Revisar matriz y categorías como una unidad; no reinterpretar pares | `SPECIAL_MATRIX_SEMANTICS_PENDING` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| D08 | excluir; adaptar distribución; tratar erróneamente como prevalencia | Adaptador de distribución y navegación Consecuencias | `SPECIAL_DISTRIBUTION_ADAPTER_PENDING` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| D02, D10 | excluir métricas; contexto no numérico; presentación parcial señalizada | Conservar cero y nulos; contexto no numérico hasta definir CV/calidad | `ZERO_EVENT_CV_UNDEFINED_PENDING` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| D09, D11 | rechazar; autorizar pares enumerados; autorizar subconjunto | D09 ya tiene dominio aprobado; decidir indicador por indicador y par por par | `EXACT_SCOPE_AUTHORIZATION_PENDING` | DOMAIN_APPROVED_SCOPE_PENDING / `ritaricaldi-cpu` / 2026-09-13 / revisión PR #60 |
| D12a, D12b | conservar original; aprobar alias; pedir validación de comprensión | La sintaxis respalda `Área × sexo` para `AREA BY SEXO` e `Idioma del hogar` para `idiomaHogar`; conservar también el código fuente en metadata | `SEMANTIC_ALIAS_SPSS_EVIDENCE_READY` | PENDING / `ritaricaldi-cpu` / — / conciliación SPSS |
| Transversal precisión | conservar valor y mostrar alertas aprobadas | CV alto referencial; N pequeño visible; N proviene de `base_unw`; sin supresión automática | notas aprobadas de CV/N | APPROVED / `ritaricaldi-cpu` / 2026-09-13 / revisión PR #60 |
| Transversal paridad | mantener; cambiar; retirar tolerancia absoluta `1e-9` | Limitarla a serialización del mismo indicador/celda/escala, nunca a diferencias sustantivas | `PARITY_TOLERANCE_PENDING` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |
| Transversal confidencialidad | definir supresión independientemente de precisión | No inferir `suppress_flag` desde CV/N; esperar política de confidencialidad | `CONFIDENTIALITY_POLICY_PENDING` | PENDING / `ritaricaldi-cpu` / — / revisión del PR |

Los indicadores ordinarios prevalence con campos completos pueden reutilizar las validaciones
transversales técnicas, pero siguen fuera de autorización numérica salvo que aparezcan en D09 o
D11 y se aprueben sus pares exactos. Distribution, special, incompletos, nuevas categorías y todo
el resto del catálogo permanecen fuera del próximo corte hasta una solicitud cerrada posterior.

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
| Un total con dos componentes ocultos | TESTED_SYNTHETIC_NO_UNIQUE_SOLUTION_FROM_ONE_EQUATION | mismo archivo; no representa una tabla cruzada |
| Mezcla de releases en un catálogo | TESTED_SYNTHETIC_REJECTED | `tests/test_stage04_module_coverage.py`; no demuestra protección contra reconstrucción entre publicaciones |
| Cruces con márgenes de filas/columnas, multitabla o multirelease | TEST_PENDING | Requiere escenarios y política de vínculo aprobados |
| AppTest: combinaciones pendientes/ausentes sin métricas | TESTED | `tests/test_stage04_ui_guards.py` |
| AppTest: demo sintético separado de V0 autorizado | TESTED | `tests/test_stage04_ui_guards.py` |
| CV menor/igual/mayor a 15 %, N=29/30/31 y alertas combinadas en 3.1–3.6 | TESTED_SYNTHETIC | `tests/test_stage04_candidate_adapter.py` |
| D09 condicionado a `CONS_ALGUNA = 1`, con válidos y ausencias | TESTED_SYNTHETIC_AND_V0_STRUCTURAL | mismo archivo y [evidencia D09](d09_cons_atencion_salud_domain_evidence.md) |

## Decisiones concretas solicitadas

1. Aprobar, ajustar o rechazar los adaptadores D01 y D03–D08, incluidos tipo y categorías.
2. Definir el tratamiento UI de D02, D04, D05 y D10 sin imputar estadísticas.
3. Aprobar o reemplazar la tolerancia `1e-9`; no forma parte de la decisión CV/N.
4. Definir la política independiente de confidencialidad, `suppress_flag` y precedencias.
5. Autorizar alcances exactos por indicador/dimensión/categorías; no por módulo implícito.
6. Resolver las equivalencias de etiquetas de D12.
7. Definir política contra reconstrucción multitabla y multirelease.

Las reglas de calidad están resueltas, pero `NUMERIC_DATA_GATE_OPEN` continúa para cifras nuevas.
Solo 3.2 / `VF_HOGAR` / Nacional / Total permanece como golden numérico local autorizado. La tabla
completa para la siguiente decisión está en
[numeric_authorization_review_20260913.md](numeric_authorization_review_20260913.md).
