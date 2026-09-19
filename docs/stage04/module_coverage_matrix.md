# Matriz de cobertura Stage 04 — cuatro estados

- **Estado:** `AUTHENTICATED_SHADOW_APPROVED; SPRINT042_CLOSURE_REVIEW`
- **Alcance de ejecución actual:** `CONTROLLED_SHADOW`
- **GO de configuración:** `GO_FOR_STAGE7_CONTROLLED_SHADOW`
- **Ejecución cloud:** pasos 47–49 cerrados; paso 49 `PASS_SUPERVISOR` en PR #126
- **Publicación institucional y cutover:** `NOT_AUTHORIZED`

Esta matriz separa cuatro hechos que no son intercambiables: que exista trabajo local, que una
cifra esté autorizada, que haya sido ejecutada en cloud y que todavía permanezca pendiente. La
existencia de una fila en el padre V0 no concede autorización ni acredita ejecución cloud.

El detalle técnico por indicador y dimensión permanece en
[module_indicator_dimension_matrix.md](module_indicator_dimension_matrix.md). PR B conecta las
3014 filas en un único extracto integral, manifiesto y ledger de conciliación; los extractos
históricos de 52 filas se conservan como evidencia, pero la aplicación consume el integral. V0
continúa oficial y no se recalcula en Stage 04.

## Cobertura por módulo

La autorización supervisora del 2026-09-15 cubre las 3014 filas del padre V0. La tabla mantiene
separado lo decidido de lo efectivamente conectado.

| Módulo | Trabajo local actual | Decisión supervisora vigente | Cloud ejecutado | Autorizado, pendiente de conectar | Sin decisión supervisora |
|---|---|---|---|---:|---|
| 3.1 Roles y tareas en el hogar | 1170/1170 filas conectadas | 1170 filas V0 cubiertas | Sí; 1170 filas | 0 | Ninguna fila V0 |
| 3.2 Violencia en el hogar | 389/389 filas conectadas | 389 filas V0 autorizadas | Sí; 389 filas | 0 | Ninguna fila V0 |
| 3.3 Violencia en la escuela | 123/123 filas conectadas | 123 filas V0 autorizadas | Sí; 123 filas | 0 | Ninguna fila V0 |
| 3.4 Violencia sexual | 749/749 filas conectadas | 749 filas V0 autorizadas | Sí; 749 filas | 0 | Ninguna fila V0 |
| 3.5 Acumulación y consecuencias | 457/457 filas conectadas: 438 A, 4 C, 7 D y 8 E | 457 filas V0 cubiertas | Sí; 457 filas | 0 | Ninguna fila V0 |
| 3.6 Búsqueda de ayuda | 126/126 filas conectadas | 126 filas V0 autorizadas | Sí; 126 filas | 0 | Ninguna fila V0 |

## Totales por estado

| Estado | Resultado verificable |
|---|---:|
| Agregados conectados y reconciliados automáticamente | 3014 filas |
| Filas V0 con decisión supervisora | 3014 filas |
| Filas autorizadas todavía no conectadas | 0 filas |
| Agregados ejecutados y promovidos en cloud | 3014 filas |
| Servicio nuevo creado durante la promoción | 0 |

Las 3014 filas son `1170 + 389 + 123 + 749 + 457 + 126` para los módulos 3.1–3.6. La autorización
numérica no equivale a autorización de publicación. La carga, la materialización autenticada de
`published.v_dashboard_current`, la promoción y el rollback cloud fueron ejecutados. La URL
pública, la publicación institucional y el cutover continúan no autorizados.

## Evidencia y gates siguientes

- El repositorio verifica manifiesto, SHA-256 y registro V0 antes de derivar la procedencia
  institucional; el campo `synthetic=false` nunca se acepta desde el CSV o el llamador.
- `CV > 15 %` y `base_unw < 30` producen alertas visibles sin supresión. La granularidad nunca
  supera V0 y no se fabrican cruces.
- El proyecto, billing, alertas y roles supervisores fueron verificados privadamente. La Etapa 7
  comenzó solo después de la decisión separada del paso 47 exigida en la revisión del PR #116.
- La ejecución real protegió identidades, acceso autenticado y el límite de 10 MiB por consulta.
- El extracto integral, su manifiesto y el ledger verifican 3014/3014 filas y 516/516 indicadores.
- La evidencia de promoción autenticada fue aprobada sin reservas en el PR #126.

Sprint 04.2 permanece abierto únicamente hasta la decisión supervisora del paquete del paso 53.
La Etapa 7 y su revisión están cerradas; la URL sigue siendo autenticada y no constituye
publicación ni cutover.
