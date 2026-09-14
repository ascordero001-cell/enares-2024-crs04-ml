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
| — | 2026-09-04 | Piloto 3.2 | CSV V0 por hash | Golden local | Coincide | Coincide | 0 | Sin diferencia observada | Ninguno | Ana Silvia Cordero Ricaldi | CLOSED_NO_DIFFERENCE | Test golden local | Resuelta — `1e-9` aprobada el 2026-09-13, alcance restringido |

La tolerancia absoluta `1e-9` está aprobada desde el 2026-09-13 (revisión del PR #60, sección 2.5),
en estado `APPROVED_SERIALIZATION_SCOPE_ONLY`. Solo cubre serialización de punto flotante del mismo
indicador, celda y escala, y no puede usarse para ocultar una discrepancia sustantiva ni para
comparar magnitudes distintas.

La reconstrucción aditiva simple tiene prueba automatizada. Los cruces multitabla y multirelease,
la exposición histórica y la frontera común de UI, export, caché y logs tienen pruebas sintéticas
automatizadas. La política fue aprobada sin umbral de recuento: estos controles quedan inactivos
mientras no se autorice granularidad más fina que departamento o un cruce ausente de V0. La
decisión del 2026-09-13 resolvió `CV > 0.15` y `base_unw < 30` como alertas visibles sin supresión
automática, aprobó la tolerancia `1e-9` con alcance restringido y fijó los alcances numéricos
D01–D12 en el acta de decisión. La política de confidencialidad quedó aprobada el 2026-09-14 sin
umbral de recuento. Lo que continúa abierto es la conexión de cifras reales de D06 y D07, que va
en un PR posterior.

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

## Seguimiento de Etapa 1

La tabla anterior conserva el estado histórico previo al acta D01–D12. El estado rector vigente
es el siguiente:

| Caso | Evidencia nueva | Estado vigente |
|---|---|---|
| D01 | Semántica de `tarea1_fem`–`tarea10_fem` contrastada contra la sintaxis CRS04 y registrada en [etapa1_source_semantics.md](etapa1_source_semantics.md) | SOURCE_SEMANTICS_VERIFIED; ADAPTER_REVIEW_PENDING |
| D02 | Ceros observados y significado conjuntivo confirmados en [Issue #24](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/24#issuecomment-5657767214) | RESOLVED; AUTHORIZED_VISIBLE_ZERO_CV_UNDEFINED |
| D10 | Ceros observados y linaje del bloque CRS04 resueltos en [Issue #24](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/24#issuecomment-5657767214) | RESOLVED; AUTHORIZED_VISIBLE_ZERO_CV_UNDEFINED |
| D11 | Valor 5 y etiqueta exacta de `C3P213` contrastados contra la sintaxis y registrados en [etapa1_source_semantics.md](etapa1_source_semantics.md) | SOURCE_SEMANTICS_VERIFIED; ADAPTER_REVIEW_PENDING |
| D12 | Alias aprobados centralizados para seis superficies, conservando nombre y código fuente en metadata | UI_ALIAS_CONTRACT_IMPLEMENTED |

### Respuesta de producción y verificaciones del 2026-09-14 UTC

- **D02:** producción confirmó ceros observados de `VP_VF_VS_HOGAR` en Cusco y Huancavelica.
  Significan que no concurren las tres violencias; una o dos formas siguen contándose en sus
  indicadores propios. Se corrige el módulo de 3.4 a **3.2**. Estado:
  `RESOLVED; AUTHORIZED_VISIBLE_ZERO_CV_UNDEFINED`.
- **D10:** producción confirmó que los cuatro ceros son observados en dominios condicionados y
  que no existe conversión general de ausencia a cero. El CV nulo es 0/0 para un cero exacto.
  El linaje está resuelto: la base de 9 a 11 años no está disponible en el entorno de trabajo,
  por lo que el bloque CRS03 emparejado no produjo filas; `C3P242_5` y `C3P242_10` provienen del
  bloque CRS04 de la línea 2416. Estado:
  `RESOLVED; AUTHORIZED_VISIBLE_ZERO_CV_UNDEFINED`.
- **D01 / `predominio_femenino_tareas`:** la sintaxis
  `07_CRS04_3.1_Caracteristicas_violencia_Percepciones_ver6.sps`, líneas 1730–1762, confirma que
  la categoría 0 reúne predominio masculino, empate y ausencia de ambos, y que el denominador de
  las proporciones reúne los diez ítems. La etiqueta V0 «tareas del hogar» no se modifica en
  Stage 04. Estado: `PRODUCER_REVIEW_REQUIRED`; indicador fuera del alcance D01.

## Correcciones técnicas R01–R05 del PR #59

| Revisión | Corrección | Estado técnico | Límite conservado |
|---|---|---|---|
| R01 | Catálogos runtime de tipo, escala y unidad CV; adaptador solo como identificador candidato | RESOLVED_ENGINEERING | No concede autorización ni acredita implementación futura |
| R02 | NaN, infinitos, texto y booleanos rechazados; `None` solo donde incomplete lo permite | RESOLVED_ENGINEERING | No imputa IC/CV ni crea regla metodológica |
| R03 | Alcance como pares exactos dimensión/categoría | RESOLVED_ENGINEERING | No modifica `authorized_dimensions` ni activa cifras |
| R04 | D01–D12 y anexos de alcance/opciones precisados desde baseline por hash | RESOLVED_DOCUMENTED | Todas las decisiones indicadas siguen PENDING |
| R05 | Ejemplo renombrado como un total con dos componentes ocultos | RESOLVED_DOCUMENTED | Márgenes múltiples, multitabla y multirelease están probados sintéticamente; política pendiente de aprobación |

## Etapa 2 — control de confidencialidad propuesto

El código de esta etapa detecta reconstrucción única usando todas las ecuaciones disponibles,
impide decisiones contradictorias para una misma celda dentro del release, bloquea la supresión
retroactiva de una celda históricamente visible y materializa una única salida segura para todos los
canales. La política aprobada elimina el umbral de recuento y mantiene esa maquinaria inactiva bajo
la granularidad V0. D06 y D07 quedan `REAL_VALUES_AUTHORIZED_FOR_SEPARATE_CONNECTION_PR`, sin
cruces nuevos ni mayor granularidad.
