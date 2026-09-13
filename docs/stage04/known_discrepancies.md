# Discrepancias conocidas del corte vertical 3.2

## Actualización 2026-09-13 — dominio D09

El V0 deja vacíos `domain_variable/domain_value` de `CONS_ATENCION_SALUD`, mientras la decisión
vigente exige `CONS_ALGUNA = 1`. El contraste de Drive no encontró una diferencia estructural de
dominio: en los 22 pares, `base_unw(CONS_ATENCION_SALUD)` coincide con
`target_unw(CONS_ALGUNA)`. La equivalencia se explica porque la variable queda `NULL` fuera del
dominio y R usa respuestas válidas. Estado: `STRUCTURAL_EQUIVALENCE_VERIFIED`; se recomienda
versionar metadata explícita en el próximo productor, sin sobrescribir V0. Los pares y cifras
continúan pendientes de autorización. Véase
[d09_cons_atencion_salud_domain_evidence.md](d09_cons_atencion_salud_domain_evidence.md).

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
`PRUEBA_DE_INTEGRACIÓN_PENDIENTE`. La decisión del 2026-09-13 resolvió `CV > 0.15` y
`base_unw < 30` como alertas visibles sin supresión automática. La tolerancia `1e-9`, la política
de confidencialidad y los alcances numéricos continúan pendientes de aprobación formal.

## Corte 2 — discrepancias detectadas antes de publicación

| ID | Comparación | Clasificación | Efecto | Tratamiento | Revisor | Estado |
|---|---|---|---|---|---|---|
| KD-C2-01 | Flags de la adaptación frente a campos existentes en V0 | Calidad conciliada | No autoriza nuevas cifras | El adaptador deriva CV/N con umbrales aprobados y nunca deriva `suppress_flag` | `ritaricaldi-cpu`, revisión PR #60 | RESOLVED_APPROVED_2026_09_13 |
| KD-C2-02 | Centinelas 3.1/3.5 frente a títulos mitos/acumulación | Correspondencia temática contrastada | Selección resuelta; calidad/supresión pendientes | 3.1: justifica_castigo_parental/docente; 3.5: PV_hogar_escuela; [evidencia](indicator_reconciliation_corte2.md) | Checkpoint de ingeniería aprobado en PR #57 | RESOLVED_DOCUMENTED |
| KD-C2-03 | n_unw frente a target_unw/base_unw en dominios condicionados | N del denominador aprobada | Correspondencia resuelta; otros gates siguen abiertos | `n_unweighted` toma exclusivamente `base_unw`; contrato y pruebas rechazan fallback | `ritaricaldi-cpu`, revisión PR #60 | RESOLVED_APPROVED_2026_09_13 |
| KD-C2-04 | Tipo special del diccionario frente a prevalence/distribution en seis salidas 3.5 | Contrato especial | Bloquea adaptación genérica | Exigir seis adaptadores específicos; [D03–D08](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |
| KD-C2-05 | Cuatro filas de contexto de Solap_VP_VF_E / Solap_VP_VF_H sin SE, IC ni CV | Estadísticas incompletas | No pueden mostrarse como estimaciones completas | Conservar vacíos y excluir de métricas; [D04–D05](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |
| KD-C2-06 | C3P242_10, C3P242_5, C4P258_7 y ayuda_vs_car con estimación/target 0 y CV vacío | CV no definido para cero eventos | Requiere estado visual explícito | Conservar `CV=null`, sin sustituir por cero; [D10](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |
| KD-C2-07 | Disponibilidad observada frente a autorización explícita por dimensión | La presencia en V0 no acredita calidad/supresión | Impide que una fila disponible llegue sin gate | Validación central/UI exigen alcance autorizado; solo 3.2/Nacional está habilitado | Checkpoint de ingeniería aprobado en PR #57 | RESOLVED_ENGINEERING |
| KD-C2-08 | `Componentes` special frente a prevalence | Contrato especial 3.1 | Bloquea adaptación genérica | Adaptador propuesto en [D01](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |
| KD-C2-09 | `VP_VF_VS_HOGAR`, Cusco/Huancavelica, con CV vacío | Estadística incompleta 3.4 | Presentación completa bloqueada | Conservar vacío; propuesta [D02](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |
| KD-C2-10 | `Área × sexo`/`Área y sexo` e `Idioma del hogar`/`Lengua materna` | Equivalencia de etiqueta no aprobada | Alias UI bloqueado | Mantener nombre original hasta decisión; [D12](numeric_gate_decision_package.md) | `ritaricaldi-cpu` | METHODOLOGICAL_DECISION_PENDING |

## Correcciones técnicas R01–R05 del PR #59

| Revisión | Corrección | Estado técnico | Límite conservado |
|---|---|---|---|
| R01 | Catálogos runtime de tipo, escala y unidad CV; adaptador solo como identificador candidato | RESOLVED_ENGINEERING | No concede autorización ni acredita implementación futura |
| R02 | NaN, infinitos, texto y booleanos rechazados; `None` solo donde incomplete lo permite | RESOLVED_ENGINEERING | No imputa IC/CV ni crea regla metodológica |
| R03 | Alcance como pares exactos dimensión/categoría | RESOLVED_ENGINEERING | No modifica `authorized_dimensions` ni activa cifras |
| R04 | D01–D12 y anexos de alcance/opciones precisados desde baseline por hash | RESOLVED_DOCUMENTED | Todas las decisiones indicadas siguen PENDING |
| R05 | Ejemplo renombrado como un total con dos componentes ocultos | RESOLVED_DOCUMENTED | Cruces con márgenes múltiples, multitabla y multirelease siguen TEST_PENDING |
