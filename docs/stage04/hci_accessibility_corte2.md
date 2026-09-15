# Evidencia HCI y accesibilidad — Corte 2

Estado: `LOCAL_MANUAL_REVIEW_COMPLETE; AUTOMATED_WCAG22_AA_IMPLEMENTED; INDEPENDENT_REVIEW_PENDING`.
Fecha de ejecución y renovación: 2026-09-11.

## Controles implementados

- La navegación, dimensión, categoría y fuente usan controles nativos de Streamlit con etiquetas.
- Los estados incluyen texto explícito (`Candidato`, `Referencial`, `Suprimido`) y no dependen
  únicamente del color.
- Los campos dinámicos del repositorio se convierten en texto inerte antes de presentarse.
- Los errores visibles son genéricos y no incluyen rutas, secretos ni contenido de archivos.
- Una combinación ausente o no autorizada comunica `sin datos` y que no se fabrican resultados.
- El selector de dimensión conserva texto oscuro sobre fondo claro mediante selectores CSS
  acotados; su valor cerrado, opciones abiertas y foco son visibles sin recolorear todo el sidebar.
- `Exportar` permanece inequívocamente deshabilitado y `Cloud: NOT_AUTHORIZED` sigue visible.

## Revisión manual local ejecutada

Se recorrió la aplicación en viewports de 1280 × 900 y 390 × 844. La revisión local verificó:

1. navegación con `Tab` y flechas, con foco visible en los controles;
2. etiquetas accesibles en navegación, dimensión y exportación deshabilitada;
3. estados expresados por texto, sin depender únicamente del color;
4. lectura del valor seleccionado `Nacional`, de las nueve opciones abiertas y del foco visible
   después de acotar el CSS del selector;
5. lectura de texto, métricas y mensajes fail-closed sin superposición en ancho reducido;
6. vistas de resumen, cada módulo, estados candidato/referencial/suprimido y combinaciones sin
   datos.

El tema final usa fondo `rgb(245, 247, 244)` y texto principal `rgb(23, 37, 31)`; los avisos
conservan texto y semántica visibles. Esta comprobación es evidencia operativa local, no una
certificación WCAG ni una auditoría formal con lector de pantalla.

## Evidencia visual

- [Resumen](evidence/sprint042_corte2_summary.png)
- [Módulo 3.1](evidence/sprint042_corte2_module31.png)
- [Módulo 3.2](evidence/sprint042_corte2_module32.png)
- [Módulo 3.3](evidence/sprint042_corte2_module33.png)
- [Módulo 3.4](evidence/sprint042_corte2_module34.png)
- [Módulo 3.5](evidence/sprint042_corte2_module35.png)
- [Módulo 3.6 — Búsqueda de ayuda](evidence/sprint042_corte2_module36.png)
- [Estados de presentación](evidence/sprint042_corte2_states.png)
- [Selector de dimensión abierto en escritorio](evidence/sprint042_corte2_dimension_open.png)
- [Vista estrecha con selector cerrado](evidence/sprint042_corte2_narrow.png)
- [Vista estrecha con selector abierto](evidence/sprint042_corte2_narrow_open.png)
- [Resumen y métricas en vista estrecha](evidence/sprint042_corte2_narrow_summary.png)

## Gate pendiente

La CI ejecuta Axe sobre las nueve vistas de navegación con las etiquetas WCAG 2 A/AA, 2.1 A/AA
y 2.2 AA. El job falla si encuentra una infracción automática nueva. La primera ejecución detectó
y corrigió el contraste de captions, encabezados tabulares, números en bloques de código y alertas
de éxito.

Permanece un único residual generado por Streamlit 1.63.0: el elemento raíz del sidebar recibe
`aria-expanded=true` aunque ese atributo no está permitido para su rol. La prueba admite solo esa
combinación exacta de regla, selector y atributo; no desactiva la regla para otros elementos. El
residual se revisará al actualizar Streamlit y no se declara corregido. Esta comprobación
complementa, pero no reemplaza, la revisión manual ni las pruebas con tecnologías de asistencia y
personas.

La aprobación general del checkpoint de ingeniería no acredita una sesión independiente de
teclado, lector de pantalla o prueba con personas usuarias. La comprensión de etiquetas por una
persona distinta de la autora continúa pendiente. Hasta entonces no se declara cerrado Sprint
04.2.
