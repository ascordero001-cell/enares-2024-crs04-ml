# Discrepancias conocidas del corte vertical 3.2

**Estado al 2026-09-04:** No existen discrepancias abiertas para el corte vertical 3.2 a la
fecha de esta revisión.

El golden reproduce directamente la evidencia agregada V0 aprobada de
`VF_HOGAR / Nacional / Total`; no se recalculó desde microdatos y no se presentó una comparación
CSV–BigQuery inexistente.

## Registro

Cuando aparezca una diferencia se añadirá una fila sin modificar silenciosamente el golden ni
ampliar tolerancias.

| KD-ID | Fecha | Componente | Fuente A | Fuente B | Valor A | Valor B | Magnitud | Explicación | Impacto | Responsable | Estado | Evidencia | Decisión supervisora requerida |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | 2026-09-04 | Piloto 3.2 | CSV V0 por hash | Golden local | Coincide | Coincide | 0 | Sin diferencia observada | Ninguno | Ana Silvia Cordero Ricaldi | CLOSED_NO_DIFFERENCE | Test golden local | Aprobar o ajustar la tolerancia propuesta de `1e-9` |

La tolerancia absoluta `1e-9` está en estado
`PROPOSED_REQUIRES_SUPERVISORY_APPROVAL`. Solo cubre serialización de punto flotante y no puede
usarse para ocultar una discrepancia sustantiva.
