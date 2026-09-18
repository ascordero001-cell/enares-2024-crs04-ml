# Paso 51 — evaluación manual del catálogo V0 completo

Estado: `PARTIAL_COMPLETE; EXACT_200_PERCENT_ZOOM_PENDING`.
Fecha UTC: 2026-09-17.
Base evaluada: `main` en `45ad227792c4312281908c09c405b90ceb900a60`.
Release local: `enares2024-crs04-v0-shadow-001`.
Entorno: aplicación local en `127.0.0.1`; cloud continúa `NOT_AUTHORIZED`.

## Alcance y método

La evaluación se ejecutó después de fusionar la conexión integral del V0 (PR #112) y su prueba
explícita de las ocho filas de clase E (PR #113). Se revisó la interfaz con el agregado completo de
3.014 filas: 2.995 de clase A y las 19 excepciones C/D/E autorizadas.

Se usaron tres métodos:

1. revisión manual de navegación por teclado, foco, texto, estados y contraste visual;
2. evaluación de las diez heurísticas de Nielsen;
3. recorrido cognitivo de los cinco escenarios de `task_scenarios.md`.

La inspección del árbol de accesibilidad confirma nombres, roles y estados. El 2026-09-17 se añadió
una prueba real con Narrador de Windows: `Tab` anunció los controles de descarga y el modo de examen
leyó el contenido estático. El control exacto de zoom al 200 % todavía no quedó demostrado por el
navegador de prueba; por ello el paso 51 no se declara cerrado.

## Revisión manual de accesibilidad

| Control | Evidencia | Resultado |
| --- | --- | --- |
| Teclado exclusivo | `Tab` movió el foco desde la navegación al selector `Dimensión` y al menú; las radios y comboboxes exponen nombre, valor y estado | PASS |
| Nombres y roles | Navegación como radios; `Dimensión`, `Buscar indicador`, `Indicador` y `Categoría` con nombre accesible; descargas como botones `Descargar CSV` y `Descargar Excel` | PASS |
| Estados no dependientes del color | `Referencial — precisión limitada`, nota de CV, N no ponderado, `PUBLISHED: NOT_AUTHORIZED` y mensajes `sin datos` aparecen como texto | PASS |
| Contraste manual | Texto principal, sidebar, controles y alertas se distinguen en la revisión visual; la CI conserva Axe WCAG 2.2 AA | PASS con respaldo automatizado |
| Reflujo/zoom exacto al 200 % | El reflujo equivalente a media anchura (640 × 384 desde 1280 × 768) conservó el contenido sin solapamientos; el navegador de prueba no expuso una escala de zoom exacta verificable | REFLOW PASS; EXACT ZOOM PENDING |
| Lector de pantalla real | Narrador de Windows anunció los controles con `Tab`; con modo de examen activo leyó título, contenido y resultados | PASS |

Hallazgo residual conocido: Streamlit 1.63.0 añade `aria-expanded` al elemento raíz del sidebar
con un rol que no admite ese atributo. La excepción automática sigue limitada a esa combinación
exacta y se mantiene como S2/`DEFER` hasta actualizar Streamlit.

Narrador anuncia además «hay un vínculo» al alcanzar el enlace automático que Streamlit agrega a
los encabezados. El encabezado y el contenido siguen siendo legibles y el vínculo no bloquea la
navegación. Se registra como S1/`DEFER` hasta revisar una actualización de Streamlit.

## Evaluación heurística

| Heurística de Nielsen | Evidencia del catálogo completo | Resultado |
| --- | --- | --- |
| Visibilidad del estado del sistema | Release, estado SHADOW, calidad, dimensión, universo y bloqueo cloud son visibles | S0 |
| Correspondencia con el mundo real | Etiquetas institucionales, módulo, denominador, CV y N no ponderado conservan el lenguaje aprobado | S0 |
| Control y libertad del usuario | La persona puede cambiar módulo, dimensión, indicador y categoría sin alterar datos | S0 |
| Consistencia y estándares | Controles nativos y estructura repetida en 3.1–3.6; el marcador referencial sale del flag | S0 |
| Prevención de errores | `3.6 + Departamento` termina en `sin datos autorizados` y no fabrica un cruce | S0 |
| Reconocimiento antes que recuerdo | Búsqueda, lista filtrada, contexto y estado permanecen visibles durante la selección | S0 |
| Flexibilidad y eficiencia de uso | La búsqueda por términos reduce un catálogo de cientos de indicadores sin exigir conocer un ID | S0 |
| Diseño estético y minimalista | Solo se muestran el corte agregado, su contexto y sus dos exportaciones | S0 |
| Reconocer, diagnosticar y recuperarse de errores | Los estados ausentes son explícitos y no exponen rutas ni contenido privado | S0 |
| Ayuda y documentación | Metodología y estado del release explican reglas, límites y autorización | S0 |

No se observó ningún S3/S4. El residual de semántica del sidebar permanece S2/`DEFER` y los dos
controles manuales pendientes no se convierten artificialmente en evidencia.

## Recorrido cognitivo

| Escenario | ¿Sabría qué hacer? | ¿Encontraría el control? | ¿Entendería el resultado? | Resultado |
| --- | --- | --- | --- | --- |
| 1. Prevalencia nacional del módulo 3.4 | Sí: elegir 3.4, Nacional y buscar `VS_12M` | Sí: navegación, dimensión, búsqueda e indicador tienen etiquetas | Sí: tarjeta muestra 19.17 %, IC95 %, CV, N, universo y denominador | PASS |
| 2. Interpretar una estimación referencial | Sí: abrir 3.6 / `C3P213` | Sí: el único indicador autorizado aparece en el selector | Sí: `[referencial]`, CV 0.29583, N 99 y la nota de precisión son coherentes | PASS |
| 3. Cambiar desagregación sin inventar combinaciones | Sí: usar `Dimensión` | Sí: el selector permanece en el sidebar | Sí: `Departamento: sin datos autorizados para 3.6. No se fabrican resultados.` | PASS |
| 4. Descargar solo el agregado visible | Sí: usar CSV o Excel junto a la tarjeta | Sí: ambos botones tienen nombre accesible | Sí: la interfaz declara `1 fila(s)` y `mismo corte en CSV y Excel` | PASS |
| 5. Ver universo, denominador, metodología y release | Sí: leer la tarjeta y abrir Metodología / Estado del release | Sí: ambas vistas están en la navegación principal | Sí: distingue V0 agregado, SHADOW, PUBLISHED no autorizado y cloud bloqueado | PASS |

## Decisión y pendientes

La navegación funcional del catálogo completo, las diez heurísticas y los cinco recorridos quedan
ejecutados sin S3/S4. El paso 51 permanece `PARTIAL_COMPLETE` hasta completar y registrar el zoom
verificable al 200 % sin pérdida de contenido o función.

La ausencia de una persona nueva continúa como riesgo residual explícito. Esta evaluación no
autoriza cloud, publicación institucional ni sustitución de V0.
