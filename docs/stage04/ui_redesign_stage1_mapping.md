# Rediseño UI — mapeo de Etapa 1

Estado: `PROPOSED_FOR_SUPERVISORY_APPROVAL`.

## Maqueta → Streamlit

| Bloque funcional | Componente Streamlit | Fuente/contrato | Restricción |
|---|---|---|---|
| Encabezado y estado | `st.title`, `st.caption`, `st.warning` | release/run ya validados | siempre muestra shadow y no-publicación |
| Panel de filtros | `st.sidebar.selectbox` y, solo si la maqueta lo exige, `st.sidebar.multiselect` | opciones derivadas de filas autorizadas | ninguna lista paralela inventada |
| Navegación por módulos | `st.tabs` | módulos 3.1–3.6 del registro único | no cambia cobertura |
| Subvistas de un módulo | `st.tabs` internas | desagregaciones presentes y autorizadas | combinación ausente muestra pendiente/sin datos |
| Tabla de indicadores | `st.dataframe` | view models validados | texto inerte; estados visibles también como texto |
| Forest plot | librería ya instalada o componente nativo aprobado | estimación e IC95 % de la misma fila validada | no recalcula ni imputa intervalos ausentes |
| Detalle | `st.metric`, `st.info`, `st.caption` | helper `build_numeric_card` | CV, N y supresión no se mezclan |
| Exportación | `st.download_button` existente | `build_export_bundle` | decisión pendiente; no se cambia en Etapa 1 |

## Estados de celda

| Estado visible | Derivación ejecutable | Presentación propuesta |
|---|---|---|
| Publicable en shadow | fila validada, `suppress_flag=false`, sin alertas | valor e IC95 % visibles; etiqueta “Sin alerta” |
| Referencial por CV | `cv_flag=true` | valor visible; distintivo “Referencial”; nota de precisión |
| N reducido | `n_flag=true` | valor visible; distintivo “N reducido”; nota `<30` |
| CV + N | ambos flags verdaderos | valor visible; ambos distintivos y ambas notas |
| Contexto no numérico | `quality_status=CONTEXT_ONLY` | texto de contexto; sin tarjeta inferencial ni forest plot |
| Pendiente de autorización | combinación no incluida por el gate | mensaje explícito; nunca valor fabricado |
| Suprimido por confidencialidad | `suppress_flag=true` | estado textual sin ningún campo protegido |

La UI no deriva confidencialidad desde CV o N. El marcador `[referencial]` procede únicamente de
`cv_flag`; la alerta N procede únicamente de `n_flag`; la ocultación numérica procede únicamente
de `suppress_flag`.

## Origen de opciones de filtro

- Módulos: registro único `src/enares/stage04/modules.py`.
- Dimensiones y desagregaciones: intersección entre `authorized_dimensions` y las filas validadas
  del release/run actual.
- Indicadores: `indicator_id` presentes después de validación y dentro del módulo autorizado.
- Categorías: categorías presentes para la combinación módulo/indicador/desagregación elegida.
- Matrices D06/D07: solo los 16 pares autorizados, validados por cierre de matriz.

Una selección sin coincidencia produce “pendiente de autorización” o “sin datos autorizados”,
según corresponda. Nunca produce cero, una categoría genérica ni un cruce calculado por la UI.

## Accesibilidad y regresión previstas para Etapa 2

- Controles nativos con etiquetas programáticas y orden de foco lógico.
- Foco visible, contraste y tamaño de texto conforme al criterio ya documentado.
- Estado comunicado por texto y no solo por color.
- AppTest para módulos, pestañas, filtros, tabla, forest plot, combinaciones ausentes y estados.
- Prueba negativa que impida mostrar campos protegidos bajo `suppress_flag=true`.
- Prueba que impida marcar “referencial” sin `cv_flag=true` o “N reducido” sin `n_flag=true`.
- Ningún uso nuevo de HTML dinámico ni `unsafe_allow_html=True`.

## Gate solicitado

Antes de Etapa 2, Rita debe confirmar:

1. que esta representación de estados conserva las decisiones vigentes;
2. que el rediseño no requiere IAM, credenciales ni recursos nuevos;
3. si la exportación agregada segura vigente permanece habilitada o debe existir una nueva decisión
   formal para deshabilitarla; y
4. que la maqueta HTML será incorporada, o que esta especificación textual basta como referencia.
