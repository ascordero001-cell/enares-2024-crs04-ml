# Conciliación directa de SPSS para D01–D12

**Estado:** `SPSS_EVIDENCE_PRESERVED; SUPERVISORY_PRESENTATION_RULES_APPROVED`
**Alcance:** preparación local desconectada; no habilita cifras ni cambia la aplicación
**Manifiesto:** [spss_source_manifest.md](spss_source_manifest.md)
**Revisora requerida:** `ritaricaldi-cpu`

> **EVIDENCIA HISTÓRICA / NO NORMATIVA.** Los estados y gates de solicitud que siguen documentan
> la conciliación previa. El estado vigente es la autorización de las 3.014 filas V0 para
> implementación local shadow del 2026-09-15; cloud y publicación continúan separados.

Esta conciliación contrasta el paquete D01–D12 con las sintaxis CRS04 entregadas y con el
diccionario y los agregados V0 congelados. Las referencias `Lx–Ly` son líneas del archivo lógico
identificado por SHA-256 en el manifiesto; no son rutas locales.

## Decisión supervisora posterior — 2026-09-13

La revisión de Rita en el PR #60 resolvió la capa de presentación sin reescribir la evidencia
histórica: en 3.1–3.6, CV > 15 % es visible, referencial y lleva nota; `base_unw < 30` es visible y
lleva alerta; ninguno implica supresión. Por ello, las instrucciones SPSS históricas que dicen
“suprimir por imprecisión” se mantienen citadas como antecedente, pero no gobiernan la interfaz
Stage 04. La confidencialidad continúa como decisión separada.

También quedó aprobado que D09 usa `CONS_ALGUNA = 1`. La evidencia de su equivalencia estructural
con el productor R y V0 se registra en
[d09_cons_atencion_salud_domain_evidence.md](d09_cons_atencion_salud_domain_evidence.md).

## Hallazgos transversales

- Las estimaciones se ejecutan con el plan complejo CRS04 y solicitan `SE`, `CV`, `COUNT` e
  `IC95 %`. El `COUNT` es el recuento muestral no ponderado; en el contrato Stage 04 continúa
  representado exclusivamente por `base_unw`.
- Las sintaxis de desagregación 3.2, 3.3 y 3.4 indican explícitamente que una estimación con
  `CV > 15 %` debe suprimirse por imprecisión. La sintaxis 3.5 usa tanto “referencial” como
  “suprimir/atender” según el bloque. Por eso el motivo de precisión debe conservarse y no
  confundirse con una supresión de confidencialidad.
- No se encontró una regla SPSS `N < 30`. Ese umbral no puede activarse por fidelidad a estas
  sintaxis.
- SPSS no define tolerancia de paridad `1e-9`, protección multitabla/multirelease ni una política
  institucional de confidencialidad. Esos controles siguen pendientes y separados.
- Los valores `SYSMIS` se excluyen cuando la sintaxis lo ordena; cuando un bloque recodifica
  expresamente `SYSMIS=0`, el cero forma parte de esa definición y no es una imputación posterior.

## Resultado por decisión

| Caso | Evidencia SPSS directa | Conciliación resultante | Estado |
|---|---|---|---|
| D01 | 3.1, L1641–1660 construye `tarea1_fem`–`tarea10_fem`; L1663–1673 fija sus etiquetas; L2399–2405 las tabula con diseño complejo | El adaptador `components-special-prevalence-v1` puede representar las diez categorías exactas sin cambiar su semántica | `READY_FOR_SUPERVISORY_DECISION` |
| D02 | 3.2, L2214–2223 define `VP_VF_VS_HOGAR` y recodifica expresamente `SYSMIS=0`; los bloques posteriores solicitan CV y COUNT | Cero se conserva. Un CV ausente en una celda observada permanece nulo; SPSS no autoriza inventarlo | `READY_FOR_SUPERVISORY_DECISION` |
| D03 | 3.5, L452–479 define las condicionales; L487–568 las estima directamente con subpoblaciones y diseño complejo | `PV_condicional_con_VS` debe ser un adaptador de prevalencia condicional; la variante con VS es secundaria y no comparable con CRS03 | `READY_FOR_SUPERVISORY_DECISION` |
| D04 | 3.3, bloque adicional de solapamiento VP × VF en escuela; usa `ROWPCT`/`COLPCT`, SE, CV, IC y COUNT | `Solap_VP_VF_E` conserva condicionales y filas de contexto como roles distintos; no se completan estadísticas ausentes | `READY_FOR_SUPERVISORY_DECISION` |
| D05 | 3.2, bloque adicional de solapamiento VP × VF en hogar; usa el mismo diseño de tabla | `Solap_VP_VF_H` aplica la misma separación de roles sin intercambiar hogar y escuela | `READY_FOR_SUPERVISORY_DECISION` |
| D06 | 3.4, L1877–1918 restringe a `VS_12M=1` y tabula 2×2/3×3 mediante `ROWPCT`/`COLPCT` | `Solap_VS_12M` requiere adaptador matricial dirigido; no admite reinterpretar pares como categorías independientes | `READY_FOR_SUPERVISORY_DECISION` |
| D07 | 3.4, L1920–1961 repite el diseño bajo universo `VS_VIDA=1` | `Solap_VS_VIDA` no hereda autorización de D06 y debe conservar su universo propio | `READY_FOR_SUPERVISORY_DECISION` |
| D08 | 3.5, L638–683 define consecuencias; L726–738 cuenta códigos afirmativos; L940–959 tabula la distribución | `num_consecuencias_fisicas` se mapea a `CONS_NUM_CONSECUENCIAS` como distribución 0–6, no como prevalencia | `READY_FOR_SUPERVISORY_DECISION` |
| D09 | 3.5, L663–675 y L748–762 restringe `CONS_ATENCION_SALUD` a `CONS_ALGUNA=1` | El denominador especializado queda confirmado; los pares de presentación siguen siendo el alcance cerrado del paquete | `READY_FOR_SUPERVISORY_DECISION` |
| D10 | 3.6 solicita SE, CV, IC y COUNT para los cuatro indicadores; el V0 observado contiene cero con CV indefinido | Cero y `base_unw` se conservan, CV permanece nulo y la fila no se presenta como completa | `READY_FOR_SUPERVISORY_DECISION` |
| D11 | 3.3 contiene `C3P223_10_1`; 3.4 contiene `Agresor_VS_12M__AG_01`; 3.6 contiene `C3P213` y sus dominios respectivos | Cada indicador se autoriza individualmente; no se generaliza la regla de numerador ni el módulo | `READY_FOR_SUPERVISORY_DECISION` |
| D12 | SPSS usa `/SUBPOP TABLE = AREA BY SEXO`; las sintaxis de desagregación llaman `Idioma del hogar` a `idiomaHogar` | Se consideran fieles las etiquetas UI `Área × sexo` e `Idioma del hogar`, manteniendo en metadata `AREA BY SEXO` e `idiomaHogar` | `READY_FOR_SUPERVISORY_DECISION` |

## Política vigente y separación de fuentes

1. `cv_flag = true` cuando el CV sea mayor que el umbral correspondiente a su unidad declarada.
2. `quality_status = REFERENCE_HIGH_CV` y la nota aprobada; la prevalencia permanece visible.
3. `n_flag = true` cuando `base_unw < 30`; la prevalencia permanece visible con nota.
4. La regla N no se atribuye a SPSS: proviene de la decisión supervisora del 2026-09-13.
5. Un CV ausente permanece ausente y la fila conserva estado incompleto.
6. `suppress_flag` de confidencialidad permanece pendiente hasta una política independiente.
7. La tolerancia `1e-9` continúa limitada a una propuesta técnica de paridad y no se atribuye a
   SPSS.

## Parada de supervisión

La aprobación resuelve CV/N y el dominio D09, pero no autoriza cifras nuevas ni los alcances
D01–D12. Hasta que la revisora enumere cada indicador/dimensión/categoría aprobado:

- `NUMERIC_DATA_GATE_OPEN`;
- solo 3.2 / `VF_HOGAR` / Nacional / Total permanece autorizado;
- el adaptador candidato continúa desconectado;
- no se modifican `authorized_dimensions`, la aplicación, el golden ni los agregados V0;
- el margen histórico de USD 20/mes queda conservado como antecedente, pero el límite operativo
  vigente desde el 2026-09-17 es USD 0 y bloquea toda configuración cloud.
