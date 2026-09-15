# Matriz de cobertura Stage 04 — cuatro estados

- **Estado:** `LOCAL_SCOPE_IMPLEMENTED; CLOUD_NOT_EXECUTED; SPRINT042_OPEN`
- **Alcance de ejecución actual:** `LOCAL_SHADOW_ONLY`
- **GO de configuración:** `GO_FOR_STAGE7_CONTROLLED_SHADOW`
- **Bloqueante de ejecución cloud:** verificación privada del proyecto y de la cuenta de billing
- **Publicación institucional y cutover:** `NOT_AUTHORIZED`

Esta matriz separa cuatro hechos que no son intercambiables: que exista trabajo local, que una
cifra esté autorizada, que haya sido ejecutada en cloud y que todavía permanezca pendiente. La
existencia de una fila en el padre V0 no concede autorización ni acredita ejecución cloud.

El detalle técnico por indicador y dimensión permanece en
[module_indicator_dimension_matrix.md](module_indicator_dimension_matrix.md). Los 52 agregados
conectados localmente se rederivan del padre V0 aprobado y se distribuyen en tres extractos con
manifiestos independientes. V0 continúa oficial y no se recalcula en Stage 04.

## Cobertura por módulo

La autorización supervisora del 2026-09-15 cubre las 3014 filas del padre V0. La tabla mantiene
separado lo decidido de lo efectivamente conectado.

| Módulo | Trabajo local actual | Decisión supervisora vigente | Cloud ejecutado | Autorizado, pendiente de conectar | Sin decisión supervisora |
|---|---|---|---|---:|---|
| 3.1 Roles y tareas en el hogar | 10 filas `_fem` conectadas en dos grupos de presentación | 1170 filas V0 cubiertas por D01 y la autorización de clase A | No; 0 filas | 1160 | Ninguna fila V0. Las tres candidatas `_nadie`, ausentes del padre, requieren nueva versión y adenda |
| 3.2 Violencia en el hogar | Golden `VF_HOGAR / Nacional / Total` conectado | 389 filas V0 autorizadas; D02 absorbido por la ampliación | No; 0 filas | 388 | Ninguna fila V0 |
| 3.3 Violencia en la escuela | `C3P223_10_1 / Nacional / Total` conectado | 123 filas V0 autorizadas; D11 incluido | No; 0 filas | 122 | Ninguna fila V0 |
| 3.4 Violencia sexual | `Agresor_VS_12M__AG_01 / Nacional / Total` conectado | 749 filas V0 autorizadas; D11 incluido | No; 0 filas | 748 | Ninguna fila V0 |
| 3.5 Acumulación y consecuencias | 38 filas conectadas: D09 y matrices D06/D07 | 457 filas V0 cubiertas: 438 A, 4 C, 7 D y 8 E | No; 0 filas | 419 | Ninguna fila V0 |
| 3.6 Búsqueda de ayuda | `C3P213 / Nacional / Total` conectado | 126 filas V0 autorizadas; D10/D11 absorbidos por la ampliación | No; 0 filas | 125 | Ninguna fila V0 |

## Totales por estado

| Estado | Resultado verificable |
|---|---:|
| Agregados conectados y probados localmente | 52 filas |
| Filas V0 con decisión supervisora | 3014 filas |
| Filas autorizadas todavía no conectadas | 2962 filas |
| Agregados ejecutados o cargados en cloud | 0 filas |
| Recursos cloud creados por este trabajo local | 0 |

Los 52 agregados son `10 + 1 + 1 + 1 + 38 + 1` para los módulos 3.1–3.6. La autorización
numérica no equivale a autorización de publicación. La URL pública, la materialización de
`published.v_dashboard_current`, la carga real, la promoción y el rollback cloud no se han
ejecutado.

## Evidencia y gates siguientes

- El repositorio verifica manifiesto, SHA-256 y registro V0 antes de derivar la procedencia
  institucional; el campo `synthetic=false` nunca se acepta desde el CSV o el llamador.
- `CV > 15 %` y `base_unw < 30` producen alertas visibles sin supresión. La granularidad nunca
  supera V0 y no se fabrican cruces.
- El GO vigente permite preparar la configuración controlada, pero la Etapa 7 no empieza hasta
  verificar en privado el proyecto y billing.
- La primera ejecución cloud debe proteger identidades y límites antes de desplegar el fixture
  sintético. Conectar cifras reales requiere la autorización separada del paso 47.
- El inventario integral y la adenda del 2026-09-15 autorizan el catálogo, pero no lo declaran
  conectado. El nuevo extracto, manifiesto, rederivación, pruebas y navegación siguen pendientes.

Sprint 04.2 permanece abierto. Esta actualización completa el registro local del paso 50, pero
no declara ejecutada la Etapa 7 ni satisface por sí sola el paquete de cierre del paso 53.
