# Evidencia de conexión D06 y D07

- Fecha: 2026-09-14 UTC
- Estado: `IMPLEMENTED; SUPERVISORY_REVIEW_PENDING`
- Fuente: agregado V0 aprobado por SHA-256
- Alcance: `LOCAL_SHADOW_ONLY`
- Cloud: `NOT_AUTHORIZED`

La conexión contiene exactamente dos matrices independientes de ocho filas: `Solap_VS_12M`
(D06) y `Solap_VS_VIDA` (D07). Cada una conserva los dos pares dirigidos 2×2 y los seis pares
dirigidos 3×3 enumerados en el acta D01–D12. No se crearon dimensiones, categorías ni cruces.

`n_unweighted` procede exclusivamente de `base_unw`. Las cuatro celdas con `CV > 15 %` permanecen
visibles como referenciales; ninguna fila se suprime. El repositorio deriva `synthetic=false` tras
verificar manifiesto, hash y registro V0: el CSV no puede conferir esa identidad.

La validación ejecutable recibe los cruces reales:

- 2×2: `VS_301_OR_302 × VS_303`;
- 3×3: `VS_301 × VS_302 × VS_303`.

Ambos deben pertenecer al conjunto de cruces V0 y cada par dimensión/categoría debe coincidir con
el alcance cerrado. La aplicación obliga a elegir primero la matriz D06/D07 y después una de sus
categorías; nunca combina filas de universos distintos.

El extracto puede rederivarse byte por byte desde el agregado privado aprobado. El repositorio no
incluye microdatos, rutas personales, IDs de Drive, enlaces públicos ni credenciales.

## Artefacto conectado

- Archivo: `v0_authorized_d06_d07_indicator_estimates.csv`
- Filas: 16 agregadas
- SHA-256: `1359e725b21877cac649ab24f196c0f6f727ebd264264489acd7a35fd7aca42c`
- Padre V0 SHA-256: `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`
- D06: 8 filas; D07: 8 filas
- CV > 15 %: 4 filas visibles y referenciales
- Supresión: 0 filas
