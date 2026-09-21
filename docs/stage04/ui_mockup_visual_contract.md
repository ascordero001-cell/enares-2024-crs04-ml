# Stage 04 — contrato visual y funcional de la maqueta

## Decisión de arquitectura

`app/streamlit_app.py` se mantiene como único entrypoint canónico para ejecución local, CI, `Dockerfile`, `Dockerfile.cloud` y Cloud Run. El diseño se implementará en componentes importables y reutilizables. `app/ui_redesign_app.py` quedará como wrapper de desarrollo o se retirará cuando deje de aportar valor; nunca será una segunda aplicación divergente.

El orden de precedencia es:

1. seguridad y privacidad vigentes;
2. contratos y actas aprobados;
3. agregados autorizados y sus metadatos;
4. comportamiento protegido por pruebas;
5. estructura visual de la maqueta;
6. textos y cifras ilustrativas de la maqueta.

## Tokens visuales

| Token | Valor | Uso |
|---|---|---|
| `paper` | `#F1F4F9` | fondo de página |
| `surface` | `#FFFFFF` | paneles y tarjetas |
| `surface-secondary` | `#EAEFF6` | superficies auxiliares |
| `border` | `#DBE3EE` | separadores y contornos |
| `ink` | `#16202E` | texto principal |
| `ink-soft` | `#4B5A72` | texto secundario |
| `brand` | `#22405F` | navegación y énfasis institucional |
| `brand-strong` | `#16293D` | títulos y foco fuerte |
| `accent` | `#0E7C6B` | selección activa |
| `success` | `#2F9E5C` | estado sin alerta |
| `warning` | `#9A6B08` | CV alto o N reducido |
| `information` | `#2E5EA8` | contexto informativo |
| `critical` | `#B23A2E` | error fail-closed o supresión |

Tipografía: Georgia o serif equivalente para títulos, Segoe UI o sans-serif del sistema para cuerpo y Consolas o monospace equivalente para cifras. Ninguna fuente remota es necesaria.

## Grid y responsive

- Ancho máximo de contenido: aproximadamente 1 360 px.
- Escritorio: `270 px | minmax(0, 1fr) | 272 px`, separación de 18 px.
- Los paneles laterales solo serán sticky cuando el viewport tenga espacio suficiente.
- Bajo 1 080 px, el contenido pasa a una columna y la navegación/filtros se presentan sin ocultar controles esenciales.
- No se permite scroll horizontal de página. Las tablas anchas usan scroll interno.
- Las seis tarjetas de módulos se reorganizan en seis, tres, dos o una columna según el ancho disponible.
- Viewports obligatorios de aceptación: 1 920 × 1 080, 1 360 × 900, 768 × 1 024 y 390 × 844.

## Áreas y componentes

| Área | Responsabilidad | Fuente de contenido |
|---|---|---|
| Cabecera | glifo `04`, eyebrow, título, subtítulo | textos controlados |
| Chip de release | `CONTROLLED_SHADOW`, autenticación, `release_id`, `run_id` | metadata validada |
| Banner | V0 oficial, no publicación y no cutover | configuración vigente |
| Panel izquierdo | filtros, cobertura y módulos 3.1–3.6 | filas autorizadas |
| Franja de módulos | seis tarjetas de panorama | resultados autorizados |
| Navegación horizontal | vistas funcionales y estado en URL | estado de sesión controlado |
| Área central | tabla, métricas, forest plot, ficha y estados vacíos | view models validados |
| Panel derecho | alertas, ficha activa, release y exportación | flags y metadata validados |
| Pie | alcance del shadow y límites de uso | textos controlados |

Los nombres internos orientativos son `_render_header`, `_render_release_chip`, `_render_scope_banner`, `_render_authorized_filters`, `_render_coverage_card`, `_render_module_navigation`, `_render_module_strip`, `_render_view_navigation`, `_render_results_table`, `_render_forest_plot`, `_render_alerts_panel`, `_render_indicator_sheet`, `_render_safe_export`, `_render_quality_legend` y `_render_release_history`. Pueden sustituirse por abstracciones equivalentes si conservan una sola fuente de verdad.

## Vistas requeridas

1. Resumen nacional.
2. Módulo 3.1.
3. Módulo 3.2.
4. Módulo 3.3.
5. Módulo 3.4.
6. Módulo 3.5.
7. Módulo 3.6.
8. Brechas.
9. Calidad y notas.
10. Estado del gate.
11. Historial.

El cambio de vista conserva el corte activo y los parámetros autorizados necesarios. La navegación debe ser operable con teclado y mostrar foco visible.

## Estados visuales

| Estado | Cifra | Tratamiento visible | Regla |
|---|---|---|---|
| Sin alerta | visible | estado verde y texto | flags de calidad falsos |
| CV alto | visible | `Referencial` y nota | `cv_flag=true` |
| N reducido | visible | alerta de N y nota | `n_flag=true`; N procede de `base_unw` |
| CV alto + N reducido | visible | ambas alertas | ambos flags verdaderos |
| Contexto no numérico | no aplica | explicación, sin inferencia | contrato del indicador |
| Suprimido | oculta | aviso sin campos protegidos | `suppress_flag=true` |
| Combinación ausente | no inventada | error fail-closed | ausencia en filas autorizadas |

Los estados nunca se derivan de texto escrito a mano. `cv_flag`, `n_flag` y `suppress_flag` permanecen independientes. CV alto y N reducido no suprimen. Una fila suprimida no expone estimación, error estándar, intervalo, CV ni N.

## Contrato de datos y seguridad

El flujo autorizado no cambia:

```text
configured_repositories()
  -> AuthorizedAggregateRepository o BigQueryRepository
  -> load_validated_estimates()
  -> validate_estimates()
  -> view models
  -> componentes Streamlit
```

- Los filtros y categorías se derivan exclusivamente de filas verificadas.
- La aplicación cloud lee `published.v_dashboard_current` y no consulta `outputs` ni microdatos.
- No se recalcula Stage 03 ni se fabrican cruces, categorías, ceros o estimaciones ausentes.
- La selección `3.2 / VF_HOGAR / Nacional / Total` conserva exactamente el golden aprobado.
- La exportación reproduce solo el corte agregado visible, incluye metadata de release/run y conserva las protecciones contra fórmulas.
- `unsafe_allow_html=True` se limita a CSS estático y estructura controlada. Todo texto dinámico usa componentes nativos o escape explícito.
- La maqueta HTML no se incrusta mediante `iframe` ni se ejecuta como sustituto de la aplicación.

## Criterios de aceptación del contrato

- CI, Docker y Cloud Run usan el mismo entrypoint.
- La composición es reconociblemente equivalente a la maqueta sin copiar sus cifras o JavaScript.
- Los seis módulos y las once vistas son navegables.
- El conteo reconciliado de 516 indicadores y 3 014 filas no cambia.
- El golden 3.2 no cambia.
- Alertas y supresión responden únicamente a los flags autorizados.
- No existe búsqueda individual ni exposición de campos protegidos.
- No existe contenido dinámico sin escapar.
- Los cuatro viewports pasan sin solapamiento ni scroll horizontal de página.
- La revisión local no modifica IAM, credenciales, datasets, buckets, identidades, servicio o tráfico cloud.

## Gate 1

Este documento congela la especificación propuesta. La conexión del nuevo layout con el adaptador real se realizará únicamente después de la aprobación supervisora de este contrato. Mientras el gate permanezca abierto, el trabajo siguiente se limita al layout con fixture sintético, pruebas y evidencia local.
