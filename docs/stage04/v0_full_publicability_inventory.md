# Inventario integral de publicabilidad del padre V0

- **Fecha UTC del análisis:** `2026-09-15`
- **Estado:** `APPROVED_FOR_LOCAL_SHADOW_IMPLEMENTATION`
- **Fuente:** padre agregado V0 privado contrastado directamente en Drive
- **Filas evaluadas:** `3,014`
- **Indicadores distintos:** `516`
- **Indicadores íntegramente clase A:** `511`
- **SHA-256 del padre:** `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`
- **SHA-256 del diccionario:** `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C`

Este informe no contiene valores de estimación, errores estándar, intervalos ni conteos de
personas. No modifica extractos, manifiestos ni cifras. La decisión supervisora posterior quedó
registrada en la revisión del PR #91 y en la adenda del acta D01–D12.

## Criterio reproducido

Cada fila de clase A fue convertida al contrato `IndicatorEstimate` y pasó individualmente
por `validate_estimates`. `base_unw` alimenta exclusivamente `n_unweighted`. Los flags de CV y
N se derivaron con las reglas comunes. Un cero exacto con SE e IC iguales a cero y CV vacío
se acepta como CV aritméticamente indefinido. `CV > 15 %` y `base_unw < 30` permanecen en A
porque son alertas visibles y nunca reglas de supresión.

Las clases son exclusivas y se aplicaron en este orden de cierre: E (identidad/etiqueta
ambigua), C (contexto sin estadística inferencial completa), D (forma no prevalencia), B
(estadística incompleta) y A (publicable directa). La resolución contra el diccionario exige
que `indicator_id` exista exactamente, que la categoría no esté vacía y que no incorpore un
marcador de precisión escrito a mano.

## Totales por clase

| Clase | Filas | Interpretación |
|---|---:|---|
| A | 2995 | Autorizada para implementación local shadow bajo el contrato estadístico |
| B | 0 | Estadísticas incompletas |
| C | 4 | Contexto no apto como estimación completa |
| D | 7 | Requiere adaptador por forma estadística |
| E | 8 | Etiqueta o identidad ambigua |
| **Total** | **3014** | Padre V0 completo |

## Clase por módulo

| Módulo | A | B | C | D | E | Total |
|---|---:|---:|---:|---:|---:|---:|
| 3.1 | 1170 | 0 | 0 | 0 | 0 | 1170 |
| 3.2 | 389 | 0 | 0 | 0 | 0 | 389 |
| 3.3 | 123 | 0 | 0 | 0 | 0 | 123 |
| 3.4 | 749 | 0 | 0 | 0 | 0 | 749 |
| 3.5 | 438 | 0 | 4 | 7 | 8 | 457 |
| 3.6 | 126 | 0 | 0 | 0 | 0 | 126 |

## Clase por dimensión

| Dimensión V0 | A | B | C | D | E | Total |
|---|---:|---:|---:|---:|---:|---:|
| 2×2 | 4 | 0 | 0 | 0 | 0 | 4 |
| 3×3 | 4 | 0 | 0 | 0 | 8 | 12 |
| Condicional | 6 | 0 | 0 | 0 | 0 | 6 |
| Conductas de riesgo inducidas por adultos | 10 | 0 | 0 | 0 | 0 | 10 |
| Conductas de riesgo personales | 10 | 0 | 0 | 0 | 0 | 10 |
| Creencia: VS ocurre en sitios oscuros | 2 | 0 | 0 | 0 | 0 | 2 |
| Creencia: VS ocurre fuera de la casa | 2 | 0 | 0 | 0 | 0 | 2 |
| Creencia: VS solo afecta a NNA pobres | 2 | 0 | 0 | 0 | 0 | 2 |
| Creencia: VS solo la cometen personas locas | 2 | 0 | 0 | 0 | 0 | 2 |
| Departamento | 1294 | 0 | 0 | 0 | 0 | 1294 |
| Desempeño escolar: expulsión de colegio | 10 | 0 | 0 | 0 | 0 | 10 |
| Desempeño escolar: repitencia de año | 10 | 0 | 0 | 0 | 0 | 10 |
| Discapacidad | 106 | 0 | 0 | 0 | 0 | 106 |
| Etnicidad | 255 | 0 | 0 | 0 | 0 | 255 |
| Exposición a discusiones entre cuidadores | 8 | 0 | 0 | 0 | 0 | 8 |
| Exposición a violencia entre cuidadores | 2 | 0 | 0 | 0 | 0 | 2 |
| Justificación del castigo físico docente | 2 | 0 | 0 | 0 | 0 | 2 |
| Justificación del castigo físico parental | 2 | 0 | 0 | 0 | 0 | 2 |
| Lengua materna | 153 | 0 | 0 | 0 | 0 | 153 |
| Nacional | 509 | 0 | 0 | 7 | 0 | 516 |
| Normas sobre castigo físico | 4 | 0 | 0 | 0 | 0 | 4 |
| Normas sobre castigo físico docente | 4 | 0 | 0 | 0 | 0 | 4 |
| Normas sobre castigo físico parental | 4 | 0 | 0 | 0 | 0 | 4 |
| Participación en decisiones del hogar | 10 | 0 | 0 | 0 | 0 | 10 |
| Prevalencia (contexto) | 0 | 0 | 4 | 0 | 0 | 4 |
| Sexo | 103 | 0 | 0 | 0 | 0 | 103 |
| Tareas del hogar | 10 | 0 | 0 | 0 | 0 | 10 |
| Te piden o te han ordenado no ir al colegio para ayudar a tu mamá o papá u otra persona en la casa u otro lugar | 10 | 0 | 0 | 0 | 0 | 10 |
| Tipo de hogar | 153 | 0 | 0 | 0 | 0 | 153 |
| Área | 106 | 0 | 0 | 0 | 0 | 106 |
| Área y sexo | 198 | 0 | 0 | 0 | 0 | 198 |

## Lista completa de filas no A

| Clase | Módulo | indicator_id | Dimensión | Categoría | Motivo exacto |
|---|---|---|---|---|---|
| C | 3.5 | `Solap_VP_VF_E` | Prevalencia (contexto) | VF (física) | fila de contexto sin error estándar, intervalo de confianza ni CV; no es una estimación publicable directa |
| C | 3.5 | `Solap_VP_VF_E` | Prevalencia (contexto) | VP (psicológica) | fila de contexto sin error estándar, intervalo de confianza ni CV; no es una estimación publicable directa |
| C | 3.5 | `Solap_VP_VF_H` | Prevalencia (contexto) | VF (física) | fila de contexto sin error estándar, intervalo de confianza ni CV; no es una estimación publicable directa |
| C | 3.5 | `Solap_VP_VF_H` | Prevalencia (contexto) | VP (psicológica) | fila de contexto sin error estándar, intervalo de confianza ni CV; no es una estimación publicable directa |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Cinco consecuencias | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Cuatro consecuencias | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Dos consecuencias | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Ninguna | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Total | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Tres consecuencias | statistic_type=distribution requiere un adaptador explícito |
| D | 3.5 | `num_consecuencias_fisicas` | Nacional | Una consecuencia | statistic_type=distribution requiere un adaptador explícito |
| E | 3.5 | `Solap_VS_12M` | 3×3 | P(agresión con contacto (302) \| violación (301)): de violación (301), % con agresión con contacto (302) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_12M` | 3×3 | P(no física (303) \| violación (301)): de violación (301), % con no física (303) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_12M` | 3×3 | P(violación (301) \| agresión con contacto (302)): de agresión con contacto (302), % con violación (301) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_12M` | 3×3 | P(violación (301) \| no física (303)): de no física (303), % con violación (301) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_VIDA` | 3×3 | P(agresión con contacto (302) \| violación (301)): de violación (301), % con agresión con contacto (302) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_VIDA` | 3×3 | P(no física (303) \| violación (301)): de violación (301), % con no física (303) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_VIDA` | 3×3 | P(violación (301) \| agresión con contacto (302)): de agresión con contacto (302), % con violación (301) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |
| E | 3.5 | `Solap_VS_VIDA` | 3×3 | P(violación (301) \| no física (303)): de no física (303), % con violación (301) [referencial] | la categoría contiene [referencial]; el marcador debe derivarse de cv_flag |

## Resultado y decisión supervisora

Las 2995 filas A pasaron `validate_estimates`; las demás quedaron enumeradas sin imputación ni
transformación. La [revisión formal del PR #91](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/91#pullrequestreview-5215637752)
autorizó la clase A completa y fijó los tratamientos C, D y E para Sprint 04.2.

La implementación, el nuevo extracto, el manifiesto y la navegación continúan pendientes. La
Etapa 7 y cualquier recurso cloud conservan su gate propio. Esta decisión no autoriza publicación
institucional, cutover ni sustitución de V0.
