# Tabla para autorización de nuevas cifras — D01–D12

**Estado:** `SUPERVISORY_DECISION_REQUIRED`
**Resuelto:** reglas CV/N, origen de N y dominio D09.
**No resuelto:** pares numéricos, estadísticas incompletas, confidencialidad y tolerancia.

La tabla no contiene prevalencias ni incorpora nuevos agregados. Las categorías proceden del V0
congelado y la conciliación SPSS del PR #60.

| Caso e indicador | Población / denominador | Desagregaciones y categorías exactas | Estadísticas ausentes | Confidencialidad | Recomendación | Estado |
|---|---|---|---|---|---|---|
| D01 · 3.1 `Componentes` | CRS04 válido; casos válidos de cada tarea | Tareas del hogar: Aconsejar y escuchar; Ayudar con tareas escolares; Cocinar; Compras mercado; Cuidar hermanas/os; Dar dinero/gastos; Jugar contigo; Lavar platos/utensilios; Lavar/planchar ropa; Limpieza | Ninguna observada | Política independiente pendiente; no inferir por CV/N | Aprobar tipo special→prevalence y adaptador nombrado antes de cifras | PENDING |
| D02 · 3.4 `VP_VF_VS_HOGAR` | CRS04 válido; casos válidos | Departamento: Cusco; Huancavelica | CV ausente; preservar NULL, no imputar cero | No publicar hasta decidir celda incompleta y confidencialidad | Mantener como contexto no numérico o excluir | PENDING |
| D03 · 3.5 `PV_condicional_con_VS` | CRS04 válido; denominador explícito de cada condicional | Condicional: P(escuela \| hogar), con VS; P(hogar \| escuela), con VS | Ninguna observada | Política independiente pendiente | Aprobar adaptador de prevalencia condicional sin comparar silenciosamente CRS03/CRS04 | PENDING |
| D04 · 3.5 `Solap_VP_VF_E` | Denominador dirigido VP o VF según la fila | Condicional: P(VF \| VP); P(VP \| VF). Contexto: VF (física); VP (psicológica) | Dos filas de contexto sin SE, IC ni CV | Contexto no puede revelar métricas ausentes; política independiente pendiente | Autorizar condicionales completas y contexto no numérico por separado | PENDING |
| D05 · 3.5 `Solap_VP_VF_H` | Igual estructura dirigida, aplicada al hogar | Condicional: P(VF \| VP); P(VP \| VF). Contexto: VF (física); VP (psicológica) | Dos filas de contexto sin SE, IC ni CV | Igual que D04 | Usar adaptador propio; no intercambiar hogar y escuela | PENDING |
| D06 · 3.5 `Solap_VS_12M` | Universo VS 12 meses; denominador indicado por cada probabilidad condicional | 2×2: P(contacto 301/302 \| no física 303); P(no física 303 \| contacto 301/302). 3×3: P(302\|303); P(302\|301); P(303\|302); P(303\|301); P(301\|302); P(301\|303) | Ninguna observada | Evaluar conjunto completo y reconstrucción entre pares | Aprobar matriz dirigida como unidad o un subconjunto enumerado | PENDING |
| D07 · 3.5 `Solap_VS_VIDA` | Universo VS alguna vez; denominador indicado por cada condicional | Los mismos ocho pares dirigidos de D06, aplicados a vida | Ninguna observada | No heredar autorización de D06; evaluar reconstrucción | Aprobar matriz de vida por separado | PENDING |
| D08 · 3.5 `num_consecuencias_fisicas` | CRS04 válido; casos válidos del bloque de consecuencias | Nacional: Ninguna; Una consecuencia; Dos consecuencias; Tres consecuencias; Cuatro consecuencias; Cinco consecuencias; Total | Ninguna observada | Política independiente pendiente | Aprobar como distribución y ubicar en Consecuencias | PENDING |
| D09 · 3.5 `CONS_ATENCION_SALUD` | `CONS_ALGUNA=1`; respuestas válidas; N=`base_unw` condicionado | Discapacidad: 0,1; Etnicidad: 1,3,5,6,9; Lengua materna: 1,3,4; Nacional: Total; Sexo: 1,2; Tipo de hogar: 1,2,3; Área: 1,2; Área y sexo: Rural Hombre, Rural Mujer, Urbano Hombre, Urbano Mujer | Ninguna observada | Departamento excluido; política independiente pendiente | Dominio ya aprobado; autorizar los 22 pares exactos o subconjunto | DOMAIN_RESOLVED_SCOPE_PENDING |
| D10 · 3.6 `C3P242_10`, `C3P242_5`, `C4P258_7`, `ayuda_vs_car` | Respectivamente `dom_institucion_escuela=1`, `dom_institucion_escuela=1`, `dom_institucion_vs=1`, `dom_busco_vs=1`; respuestas válidas | Nacional: Total para cada indicador | CV ausente en los ceros observados; conservar cero y CV=NULL | No presentar como completo sin decisión; política independiente pendiente | Contexto no numérico hasta aprobar estado de cero con CV indefinido | PENDING |
| D11 · 3.3 `C3P223_10_1`; 3.4 `Agresor_VS_12M__AG_01`; 3.6 `C3P213` | `VP_ESCUELA=1`; `VS_12M=1`; `dom_no_recibio_hogar=1`. Numeradores 1, 1 y 5 respectivamente | Nacional: Total, únicamente para cada indicador | Ninguna observada | No generalizar a otros indicadores o pares | Decidir cada indicador individualmente | PENDING |
| D12 · alias de dimensión | Hereda exactamente el denominador del indicador fuente | `Área y sexo`→`Área × sexo`; `Lengua materna`→`Idioma del hogar`; categorías sin cambios | Hereda ausencias de la familia | Alias no amplía pares ni permite combinaciones nuevas | Aprobar alias conservando nombre/código fuente en metadata | PENDING |

## Decisiones solicitadas a Rita

1. Autorizar, reducir o rechazar los pares exactos de D01–D12.
2. Elegir exclusión o contexto no numérico para D02, D04, D05 y D10.
3. Aprobar los adaptadores special/distribution y los alias D12.
4. Definir la política de confidencialidad y reconstrucción antes de cualquier publicación.
5. Aprobar o reemplazar la tolerancia técnica de paridad `1e-9`.
