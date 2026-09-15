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

| Módulo | Trabajo local | Alcance numérico autorizado | Cloud ejecutado | Pendiente |
|---|---|---|---|---|
| 3.1 Roles y tareas en el hogar | 10 filas de la serie `_fem` de `Componentes`; dos grupos de presentación para ítems 1–7 y 8–10; exportación del mismo corte | D01: 10 filas `_fem` conectadas | No; 0 filas cargadas o publicadas | Las tres filas `_nadie` se retiraron porque no existen en el agregado V0; cualquier corte posterior exige nueva versión y adenda supervisora |
| 3.2 Violencia en el hogar | Golden `VF_HOGAR / Nacional / Total` conectado y probado | 1 fila del golden V0 | No; 0 filas cargadas o publicadas | Resto del catálogo 3.2 sujeto a decisión posterior |
| 3.3 Violencia en la escuela | `C3P223_10_1 / Nacional / Total` conectado y probado | D11: 1 fila V0 | No; 0 filas cargadas o publicadas | Resto del catálogo 3.3 sujeto a decisión posterior |
| 3.4 Violencia sexual | `Agresor_VS_12M__AG_01 / Nacional / Total` conectado y probado | D11: 1 fila V0 | No; 0 filas cargadas o publicadas | Resto del catálogo 3.4 sujeto a decisión posterior |
| 3.5 Acumulación y consecuencias | D09 con 22 pares; D06 y D07 con dos matrices completas de 8 filas cada una | 38 filas: 22 de `CONS_ATENCION_SALUD`, 8 de `Solap_VS_12M` y 8 de `Solap_VS_VIDA` | No; 0 filas cargadas o publicadas | Formas de contexto y distribución, y cualquier ampliación, requieren tratamiento/adenda específica |
| 3.6 Búsqueda de ayuda | `C3P213 / Nacional / Total` conectado y probado | D11: 1 fila V0 | No; 0 filas cargadas o publicadas | Resto del catálogo 3.6 sujeto a decisión posterior |

## Totales por estado

| Estado | Resultado verificable |
|---|---:|
| Agregados conectados y probados localmente | 52 filas |
| Agregados con autorización numérica dentro de ese corte local | 52 filas |
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
- El inventario integral del padre V0 y cualquier adenda de ampliación son gates separados; no
  alteran automáticamente esta matriz.

Sprint 04.2 permanece abierto. Esta actualización completa el registro local del paso 50, pero
no declara ejecutada la Etapa 7 ni satisface por sí sola el paquete de cierre del paso 53.
