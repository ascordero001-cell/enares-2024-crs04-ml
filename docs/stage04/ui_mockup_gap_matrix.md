# Stage 04 — matriz de brechas de paridad visual

## Línea base

- Base SHA: `7d6e6249f6b5576dc8056d433550437d85bf22e1`
- Rama: `feat/stage04-mockup-visual-parity`
- Entry point efectivo de CI, Docker y Cloud Run: `app/streamlit_app.py`
- Rediseño conectado pero no desplegado: `app/ui_redesign_app.py`
- Referencia visual: `docs/stage04/references/MAQUETA_APP_VIGILANCIA_CRS04.html`
- Alcance: `CONTROLLED_SHADOW`

## Diagnóstico

La lógica autorizada, la validación, los 516 indicadores y las 3 014 filas agregadas ya existen. La brecha es que el rediseño aprobado vive en un entrypoint separado, mientras CI, `Dockerfile`, `Dockerfile.cloud` y Cloud Run siguen ejecutando la interfaz anterior. La implementación debe conservar `app/streamlit_app.py` como entrypoint canónico e integrar allí componentes visuales reutilizables, sin duplicar acceso a datos ni reglas estadísticas.

| Elemento de la maqueta | Estado actual | Brecha | Archivo responsable | Solución propuesta | Prueba |
|---|---|---|---|---|---|
| Cabecera institucional con glifo `04` | Título y advertencia básicos | Falta jerarquía equivalente y estado del release | `app/streamlit_app.py` | Componente de cabecera con CSS estático y textos de runtime vigentes | AppTest + captura desktop |
| Chip de release y autenticación | Información distribuida | Falta agrupación visible del release/run y shadow autenticado | `app/streamlit_app.py` | Derivar chip de metadata del repositorio configurado | AppTest sin valores hardcodeados |
| Banner de alcance | Existe advertencia funcional | No sigue la composición de la maqueta | `app/streamlit_app.py` | Banner controlado con `CONTROLLED_SHADOW`, V0 oficial y no publicación | AppTest de textos vigentes |
| Grid 270 px / centro / 272 px | Layout principal diferente | No hay dos rails equivalentes | nuevo módulo visual + CSS estático | Grid responsive, una columna bajo 1080 px | Capturas 1360, 768 y 390 px |
| Ocho filtros visibles | Implementado en `ui_redesign_app.py` por PR #150 | No está en el entrypoint canónico | `app/ui_redesign_app.py`, `app/streamlit_app.py` | Mover/reutilizar el componente sin duplicar lógica | AppTest: ocho controles y un solo corte activo |
| Etiquetas de categorías | Varias categorías conservan códigos autorizados | Falta aplicar etiquetas aprobadas donde existan | view models vigentes | Usar metadata aprobada; conservar códigos si no existe etiqueta | Prueba de pares dimensión/categoría |
| Cobertura V0 | No existe como tarjeta equivalente | Falta resumen 516/3 014/3.1–3.6 | componente visual | Derivar conteos de filas verificadas, no de la maqueta | Prueba de conteos reconciliados |
| Navegación lateral de módulos | Selector de módulo | Falta navegación reconocible 3.1–3.6 | entrypoint canónico | Controles Streamlit accesibles con estado persistente | AppTest + teclado |
| Seis tarjetas superiores | Ausentes | Falta panorama por módulo | componente visual | Construir desde resultados autorizados y estados reales | AppTest sin cifras sintéticas |
| Navegación horizontal | Tabs funcionales parciales | Faltan Resumen, Brechas, Calidad, Gate e Historial | entrypoint canónico | Vistas nativas con estado persistente | AppTest de navegación |
| Tabla central | Existe tabla funcional | Falta presentación equivalente y scroll interno | vista de tabla | Reutilizar registros seguros con estilos controlados | AppTest de campos y captura móvil |
| Forest plot | Existe Vega-Lite | Requiere encaje visual y responsive | vista de forest plot | Mantener datos e intervalos sin recalcular | Golden + AppTest |
| Estados de calidad | Funcionales en pestaña separada | Falta integración de badges y leyenda | view models + componentes | Derivar exclusivamente de flags y `quality_status` | Pruebas CV/N/supresión |
| Panel derecho de alertas | Ausente | Falta resumen contextual | componente visual | Alertas desde flags/notas reales | AppTest sin alertas ficticias |
| Ficha del indicador | Existe detalle parcial | Falta panel equivalente | componente visual | Mostrar universo, denominador, release y procedencia ya validados | AppTest de metadata |
| Exportación segura | Existe en la app anterior | No está integrada al rediseño | helper de exportación vigente | Reutilizar exportación del corte visible, sin duplicarla | Pruebas CSV/XLSX y fórmulas |
| Historial del release | No hay vista equivalente | Falta representación del estado real | repositorio/configuración | Mostrar únicamente metadata disponible y verificada | AppTest de release/run |
| Responsive | Streamlit adapta componentes, sin evidencia completa | Falta verificación contra cuatro viewports | CSS + componentes | Breakpoints sin scroll horizontal de página | Capturas 1920/1360/768/390 |
| Accesibilidad | CI WCAG existente | Falta evidencia específica de la nueva composición | componentes + CSS | Foco visible, teclado, texto además de color, movimiento reducido | WCAG CI + recorrido manual |
| Tema visual | Estilo Streamlit básico | Falta paleta, tipografía y superficies rectoras | CSS estático controlado | Tokens derivados de la maqueta, sin HTML dinámico inseguro | Revisión de CSS + captura |
| Entrypoint único | Dos aplicaciones divergentes | Riesgo de probar una UI y desplegar otra | `app/streamlit_app.py`, Dockerfiles y workflows | Integrar el diseño en `streamlit_app.py`; dejar el otro como wrapper o retirarlo | Prueba de entrypoint CI/contenedor |

## Restricciones de implementación

- No cambiar datos, hashes, contratos estadísticos ni el alcance D01–D12.
- No copiar cifras, estados ni JavaScript sintético desde la maqueta.
- No consultar microdatos ni crear cruces ausentes.
- No usar `iframe` ni sustituir la aplicación por HTML estático.
- No cambiar IAM, credenciales, datasets, buckets, identidades, servicio Cloud Run o tráfico en este bloque.
- Toda mutación cloud queda detrás del environment protegido y de la aprobación supervisora específica.
