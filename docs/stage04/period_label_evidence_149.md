# #149 · Evidencia de períodos de referencia visibles

Las etiquetas se asignan por fila de `report_topic_map.csv`, sin modificar el CSV V0, sus estimaciones ni el catálogo de 80 títulos. `No aplica` queda exclusivamente en las percepciones 3.1. En una ficha con `Período no precisado`, la interfaz advierte que la fuente no establece un plazo único.

| Temas o serie | Etiqueta | Evidencia de fuente y criterio |
|---|---|---|
| 3.2.1–4, 3.2.10–16, 3.2.17–18 | Últimos 12 meses | Informe CRS04, sección 3.2; sintaxis `08_CRS04_3.2 Violencia en el hogar_ver6.sps`. Las caracterizaciones 17–18 heredan el período de `VP_HOGAR` y `VF_HOGAR`. |
| 3.2.7–8 | Período no precisado | La sintaxis 3.2, comentarios sobre C3P121, dice que no siempre es posible precisar su período; 3.2.7 combina esa privación con desprotección familiar. No se extrapola el plazo del otro componente. |
| 3.3.1–4, 3.3.7–16, 3.3.19–20 | Últimos 12 meses | Informe CRS04, sección 3.3; sintaxis `09_CRS04_3.3 Violencia en el entorno escolar_ver4.sps`. Las caracterizaciones 19–20 heredan el período de `VP_EJERCIDA` y `VF_EJERCIDA`. |
| 3.5.1–9 | Últimos 12 meses | Sintaxis `11_CRS04_3.5 Acumulación de violencias_ver4.sps`: series de acumulación y solapamiento basadas en violencia reciente. |
| 3.5.10–12 | Período no precisado | En la sección 3.5.4 de la misma sintaxis, `VF_HOGAR` y `VF_ESCUELA` son de los últimos 12 meses, pero C3P243 pregunta por consecuencias de golpes o maltrato en hogar/CAR o colegio sin precisar el plazo de la consecuencia. No se presenta como si C3P243 tuviera una ventana explícita de 12 meses. |
| 3.6.1–10, excepto DEMUNA | Últimos 12 meses | Sintaxis `13_CRS04_3.6_BusquedaAyuda_VS_ver4.sps`: filtro principal `VS_12M = 1` (bloque 0); C4P257 pregunta explícitamente por los últimos 12 meses (bloque 10). Las etiquetas describen la población analítica, no una nueva estimación. |
| `uso_demuna` en 3.6.10 | Alguna vez en la vida | C3P247, bloque 12 de la sintaxis 3.6: «Alguna vez, ¿has ido a una DEMUNA?». |
| `conoce_demuna` en 3.6.10 | Período no precisado | C3P246, bloque 12: «¿Conoces o has escuchado de la DEMUNA?»; no expresa ventana temporal. |

Se conservan las asignaciones ya existentes de 3.2.5–6, 3.3.5–6 y 3.4.1–9, incluidos sus períodos mixtos. Los temas 3.2.9, 3.3.17 y 3.3.18 carecen de filas V0. La etiqueta corta entre paréntesis se añade únicamente en la presentación; la ficha mantiene el valor completo.
