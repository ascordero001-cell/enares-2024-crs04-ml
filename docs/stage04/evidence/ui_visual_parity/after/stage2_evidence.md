# Stage 04 UI — evidencia sintética de la Etapa 2

Fecha de verificación: 2026-09-21

Base: `7106a6dd364525c991d072cd4537e45466edc9b3`

Corrección de selección efectiva: `2f8fdd187f245e213392497820958da5aa0bb4f8`.

Alcance: estructura visual con fixture sintético; sin conexión a V0 ni BigQuery.

## Capturas

- `desktop_summary.png`: viewport CSS 1360 × 900.
- `desktop_1920x1080.png`: viewport CSS 1920 × 1080.
- `tablet_summary.png`: viewport CSS 768 × 1024.
- `mobile_summary.png`: viewport CSS 390 × 844.

Las capturas se generaron desde `app/ui_redesign_synthetic_app.py`. No contienen
cifras V0 ni resultados institucionales.

## Verificación responsive

| Viewport | `clientWidth` | `scrollWidth` | Resultado |
|---|---:|---:|---|
| Escritorio | 1360 | 1360 | PASS |
| Escritorio amplio | 1920 | 1920 | PASS |
| Tablet | 768 | 768 | PASS |
| Móvil | 390 | 390 | PASS |

No se detectó scroll horizontal de página. En escritorio se conservó el grid de
tres columnas; en tablet y móvil los paneles se reorganizaron en una columna. Las
seis tarjetas se reorganizaron en tres y dos columnas, respectivamente.

## Controles aplicados

- Cabecera, banner, filtros, seis módulos, navegación, tabla, forest plot,
  alertas, ficha y exportación sintética presentes.
- Navegación implementada con control nativo accesible por teclado y estado de
  vista persistido en el parámetro `view` de la URL.
- Opciones de dimensión, indicador y categoría derivadas del fixture vigente.
- Una sola selección efectiva alimenta tabla, forest plot, alertas y ficha; la
  navegación por módulo sincroniza el filtro de módulo y conserva filtros
  compatibles.
- Una selección vacía presenta su estado vacío y no reutiliza una fila ajena
  como ficha activa.
- Combinaciones ausentes no se fabrican ni se convierten en cero.
- Campos estadísticos protegidos permanecen ausentes en el estado suprimido.
- Texto dinámico renderizado con componentes nativos; el HTML se limita a CSS
  estático controlado.
- Movimiento reducido cubierto por `prefers-reduced-motion`.
- Exportación deshabilitada en esta maqueta sintética.

## Estado del gate

La evidencia permite solicitar revisión de Gate 2. No autoriza conectar el
adaptador real, modificar `app/streamlit_app.py`, desplegar ni cambiar tráfico,
IAM o datos.
