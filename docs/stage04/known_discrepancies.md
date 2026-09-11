# Discrepancias conocidas del corte vertical 3.2

**Estado al 2026-09-04:** No existen discrepancias abiertas para el corte vertical 3.2 a la
fecha de esta revisión.

El golden reproduce directamente la evidencia agregada V0 aprobada de
`VF_HOGAR / Nacional / Total`; no se recalculó desde microdatos y no se presentó una comparación
CSV–BigQuery inexistente.

La entrada golden reside en `v0_authorized_indicator_estimates.csv`: es un agregado autorizado,
no sintético, sin microdatos y ligado a su manifiesto y al inventario V0 aprobado. Está físicamente
separada de `demo_indicator_estimates.csv`, fixture 100 % sintético que conserva únicamente los
tres estados didácticos. Ninguno de los dos archivos constituye una publicación institucional.
BigQuery, DDL, Cloud Run y todo recurso cloud permanecen `BLOCKED_BY_CLOUD_GATE`.

## Registro

Cuando aparezca una diferencia se añadirá una fila sin modificar silenciosamente el golden ni
ampliar tolerancias.

| KD-ID | Fecha | Componente | Fuente A | Fuente B | Valor A | Valor B | Magnitud | Explicación | Impacto | Responsable | Estado | Evidencia | Decisión supervisora requerida |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | 2026-09-04 | Piloto 3.2 | CSV V0 por hash | Golden local | Coincide | Coincide | 0 | Sin diferencia observada | Ninguno | Ana Silvia Cordero Ricaldi | CLOSED_NO_DIFFERENCE | Test golden local | Aprobar o ajustar la tolerancia propuesta de `1e-9` |

La tolerancia absoluta `1e-9` está en estado
`PROPOSED_REQUIRES_SUPERVISORY_APPROVAL`. Solo cubre serialización de punto flotante y no puede
usarse para ocultar una discrepancia sustantiva.

La reconstrucción aditiva simple tiene prueba automatizada. Los cruces multitabla o multirelease y
el enlace externo permanecen `TEST_PENDIENTE`; logs, errores, caché y exports permanecen
`PRUEBA_DE_INTEGRACIÓN_PENDIENTE`. Los umbrales `CV > 0.15`, `N < 30`, la tolerancia `1e-9` y el
owner metodológico siguen pendientes de aprobación formal y no son política institucional.

## Corte 2 — discrepancias detectadas antes de publicación

| ID | Comparación | Clasificación | Efecto | Tratamiento | Revisor | Estado |
|---|---|---|---|---|---|---|
| KD-C2-01 | Flags de la adaptación frente a campos existentes en V0 | Calidad no conciliada | Bloquea nuevas cifras | Retirada adaptación con flags false por defecto; conservar golden | PENDIENTE | OPEN |
| KD-C2-02 | Centinelas 3.1/3.5 frente a títulos mitos/acumulación | Correspondencia temática contrastada en Drive | Selección resuelta; calidad/supresión pendientes | 3.1: justifica_castigo_parental/docente; 3.5: PV_hogar_escuela; evidencia en indicator_reconciliation_corte2.md | Revisión formal pendiente | RESOLVED_MAPPING |
| KD-C2-03 | n_unw frente a target_unw/base_unw en dominios condicionados | N del denominador aclarada | Correspondencia resuelta; otros gates siguen abiertos | n_unweighted toma exclusivamente base_unw; aclaración explícita de la usuaria, contraste en Drive y tests sintéticos | Revisión formal del corte pendiente | RESOLVED_MAPPING |
| KD-C2-04 | Tipo special del diccionario frente a prevalence/distribution en seis salidas 3.5 | Contrato especial | Bloquea adaptación genérica | Exigir adaptador explícito; no tratar como prevalencia binaria ordinaria | PENDIENTE | OPEN |
| KD-C2-05 | Cuatro filas de contexto de Solap_VP_VF_E / Solap_VP_VF_H sin SE, IC ni CV | Estadísticas incompletas | No pueden mostrarse como estimaciones completas | Conservar vacíos y excluir de tarjetas hasta decisión de calidad | PENDIENTE | OPEN |
| KD-C2-06 | C3P242_10, C3P242_5, C4P258_7 y ayuda_vs_car con estimación/target 0 y CV vacío | CV no definido para cero eventos | Requiere estado visual explícito | Conservar CV vacío; no sustituir por cero ni aprobar publicación por defecto | PENDIENTE | OPEN |
