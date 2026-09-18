# Acta de decisión supervisora — gate numérico D01–D12 — PR #60

**Revisora:** Rita Ricaldi
**Fecha:** 2026-09-13
**PR:** #60 · head `cff8faf3cdf56b4e4304426da6a7c3a69db61f69`
**Evidencia formal:** [Review changes → Approve](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/60#pullrequestreview-5191733879)
**Merge:** `0096842bcbc591d91ea689b2c1ac09ee60e8cbcf` · 2026-09-13T19:14:18Z
**CI de main:** [run 34777073136 — success](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/34777073136)
**Documentos evaluados:** `numeric_authorization_review_20260913.md`, `numeric_gate_decision_package.md`, `spss_numeric_gate_reconciliation.md`, `d09_cons_atencion_salud_domain_evidence.md`
**Estado resultante:** `NUMERIC_SCOPE_PARTIALLY_AUTHORIZED; PUBLICATION_NOT_AUTHORIZED`
**Estado vigente tras adenda del 2026-09-15:** `FULL_V0_NUMERIC_SCOPE_AUTHORIZED_FOR_LOCAL_SHADOW; IMPLEMENTATION_PENDING; PUBLICATION_NOT_AUTHORIZED`

> Las secciones 1–3 conservan el estado histórico decidido el 2026-09-13. Sus gates parciales
> fueron sustituidos por la adenda del 2026-09-15 indicada arriba y no son el estado operativo actual.

Esta acta responde a las decisiones solicitadas en el paquete del gate numérico. No autoriza
publicación, cutover, conexión cloud ni ampliación de presupuesto. No modifica V0, sus hashes,
las sintaxis SPSS ni el golden aprobado.

## 0. Sobre el PR #60

El PR quedó aprobado como entrega documental y fue fusionado con CI verde. El diff se limitó a
documentación, contratos, adaptador candidato y pruebas, sin `.sps`, `.sav`, microdatos ni
credenciales.

Fusionarlo no cierra el Sprint 04.2 ni el gate numérico. Ambos siguen abiertos y se rigen por
esta acta.

## 1. Decisiones por caso

Leyenda de estado: **AUTORIZADO** (puede implementarse y conectarse dentro del alcance escrito) ·
**AUTORIZADO CONDICIONADO** (implementable; la conexión de cifras exige cumplir la condición) ·
**CONTEXTO NO NUMÉRICO** (visible sin métricas, sin tarjeta, sin tabla numérica y sin exportación) ·
**DIFERIDO** (no se implementa ni se conecta en este corte).

| Caso | Decisión | Alcance autorizado | Condición de cumplimiento |
|---|---|---|---|
| **D01** · 3.1 `Componentes` | AUTORIZADO CONDICIONADO | Adaptador `components-special-prevalence-v1`; las 10 categorías enumeradas de `Tareas del hogar` | Antes de conectar cifras, Ana documenta qué mide el sufijo `_fem` en `tarea1_fem`–`tarea10_fem`: universo, sujeto de la tarea y persona de referencia. Si el universo no es el declarado en la etiqueta, la etiqueta se corrige antes de publicar, no después. |
| **D02** · 3.2 `VP_VF_VS_HOGAR` | AUTORIZADO | Departamento: Cusco, Huancavelica | Los ceros observados significan que no concurren las tres violencias. Se muestran como `0 %`, con `base_unw` presente, `CV` indefinido por aritmética y la etiqueta conjuntiva aprobada. |
| **D03** · 3.5 `PV_condicional_con_VS` | AUTORIZADO | Adaptador de prevalencia condicional; las 2 categorías: P(escuela \| hogar) con VS; P(hogar \| escuela) con VS | La etiqueta conserva el denominador explícito. Queda prohibido comparar o presentar junto a CRS.03 sin una decisión separada. |
| **D04** · 3.5 `Solap_VP_VF_E` | AUTORIZADO para las 2 condicionales · CONTEXTO NO NUMÉRICO para las 2 filas de contexto | Condicionales P(VF \| VP) y P(VP \| VF) con su texto “de [denominador], % con [numerador]” | Las filas de contexto VF (física) y VP (psicológica) carecen de SE, IC y CV: se muestran sin métrica y no se exportan. No se completan ni se imputan. |
| **D05** · 3.5 `Solap_VP_VF_H` | Igual que D04, con adaptador propio | Mismos 4 pares aplicados al hogar | Prohibido intercambiar o reutilizar el adaptador de escuela. La cobertura se demuestra por separado. |
| **D06** · 3.5 `Solap_VS_12M` | AUTORIZADO CONDICIONADO — estructura sí, cifras no | Matriz dirigida completa como unidad: 2 pares 2×2 y 6 pares dirigidos 3×3 | El adaptador y las pruebas pueden construirse ahora con datos sintéticos. **La conexión de cifras reales queda suspendida hasta que exista la política de confidencialidad del punto 2.4.** Una matriz dirigida sobre violencia sexual con celdas pequeñas es el caso de reconstrucción de mayor riesgo del catálogo; no se abre antes que la política. |
| **D07** · 3.5 `Solap_VS_VIDA` | Igual que D06, autorizado por separado | Mismo conjunto cerrado aplicado a vida | No hereda nada de D06. Universo, adaptador, pruebas y evidencia propios. Misma suspensión de cifras. |
| **D08** · 3.5 `num_consecuencias_fisicas` | AUTORIZADO | Adaptador de distribución; 7 categorías: Ninguna, Una, Dos, Tres, Cuatro, Cinco consecuencias, Total | Se ubica en **Consecuencias**, no en Acumulación. La fila `Total` se presenta como total de la distribución, nunca como una prevalencia. |
| **D09** · 3.5 `CONS_ATENCION_SALUD` | AUTORIZADO — los 22 pares exactos | Discapacidad 0,1 · Etnicidad 1,3,5,6,9 · Idioma del hogar 1,3,4 · Nacional Total · Sexo 1,2 · Tipo de hogar 1,2,3 · Área 1,2 · Área × sexo (Rural Hombre, Rural Mujer, Urbano Hombre, Urbano Mujer). Departamento excluido. | Dominio `CONS_ALGUNA = 1` aprobado y equivalencia estructural R/V0 verificada. El dominio se muestra junto a la cifra. Las 13 celdas con `CV > 15 %` siguen visibles y referenciales; la precisión no activa supresión. Las etiquetas de código constan en la adenda. |
| **D10** · 3.6 `C3P242_10`, `C3P242_5`, `C4P258_7`, `ayuda_vs_car` | AUTORIZADO | Nacional / Total en cada indicador | Los cuatro ceros son observados. Se publican con `base_unw` presente y `CV` indefinido por aritmética. El linaje de `C3P242_5` y `C3P242_10` está resuelto en Issue #24. |
| **D11** · 3.3 `C3P223_10_1` · 3.4 `Agresor_VS_12M__AG_01` · 3.6 `C3P213` | AUTORIZADO CONDICIONADO, uno por uno | Solo Nacional / Total en cada indicador | `C3P213` usa numerador `== 5`, no la regla binaria `== 1`. Antes de conectarlo, Ana registra la etiqueta exacta del valor 5 y el texto del indicador que se mostrará. Ningún otro indicador de esos módulos queda incluido. |
| **D12a** · alias `Área y sexo` → `Área × sexo` | AUTORIZADO | Todas las familias que ya usan la dimensión | Cambio tipográfico sobre el mismo constructo. `AREA BY SEXO` y el nombre V0 `Área y sexo` se conservan en metadata. No amplía pares ni habilita combinaciones nuevas. |
| **D12b** · alias `Lengua materna` → `Idioma del hogar` | AUTORIZADO | Todas las familias que ya usan la dimensión | La variable de origen es `idiomaHogar` y la pregunta CRS04 capta el idioma hablado en el hogar, no la lengua materna de la persona: la etiqueta correcta para la interfaz y los anexos es **Idioma del hogar**. El nombre V0 `Lengua materna` y el código fuente `idiomaHogar` se conservan en metadata para trazabilidad. El alias no amplía pares ni habilita combinaciones nuevas. Ana actualiza la etiqueta de forma consistente en tarjeta, tabla, gráfico, tooltip, impresión y exportación; no quedan las dos denominaciones conviviendo. |

## 2. Decisiones transversales

### 2.1 Alcance numérico autorizado

Queda autorizado exactamente lo listado en la columna “Alcance autorizado” de la sección 1,
más el golden vigente 3.2 / `VF_HOGAR` / Nacional / Total. Todo lo demás del catálogo —516
indicadores del diccionario V0— permanece fuera. Ningún módulo queda autorizado de forma
implícita. Un indicador autorizado no autoriza sus vecinos, y una dimensión autorizada en un
caso no se extiende a otro.

### 2.2 Tratamiento de estadísticas ausentes

Una estadística ausente permanece `null`. No se imputa cero, no se imputa la media, no se declara
precisión adecuada por ausencia de CV. Una fila incompleta se muestra como contexto sin métrica,
sin tarjeta, sin tabla numérica y sin exportación. Un cero legítimo con `base_unw` presente no es
una ausencia y se conserva como cero; distinguir ambos casos en la UI es requisito.

### 2.3 Adaptadores y tipos

Aprobados: `special → prevalence` para D01, D03, D04, D05, D06 y D07;
`special → distribution` para D08; `prevalence → prevalence` para D09 y D11. Cada adaptador se
identifica con nombre y versión, tiene pruebas sintéticas propias y rechaza filas no marcadas como
sintéticas. Un `adapter_id` registrado no equivale a alcance autorizado.

Aclaración posterior, 2026-09-13: esa comprobación pertenece al adaptador de pruebas sintéticas y debe conservarse ahí. Los agregados autorizados son datos institucionales reales y no pasan por esa barrera: usan un adaptador institucional con nombre, versión y pruebas propias. Bajo ninguna circunstancia se marca un dato real como sintético para superar la comprobación. La separación entre ambos adaptadores se presenta para revisión antes de conectar el primer agregado.

### 2.4 Confidencialidad — política pendiente, con plazo

`suppress_flag` no se deriva de `cv_flag` ni de `n_flag`, en ningún sentido, ni por defecto a
`false`. Se mantiene la separación.

El borrador de política de confidencialidad debe cubrir: criterio de celda primaria; supresión
complementaria sobre márgenes de filas y columnas; protección entre tablas del mismo release;
protección entre releases; y precedencia explícita cuando concurran motivo de precisión y motivo
de confidencialidad. Hasta su aprobación:

- no se conectan cifras reales de D06 ni D07;
- no se habilita exportación CSV/Excel de ningún corte fuera del golden;
- el resto del alcance de la sección 1 puede conectarse en SHADOW restringido, sin publicación.

### 2.5 Tolerancia de paridad `1e-9`

**Aprobada con alcance restringido.** Se aplica únicamente a la comparación técnica del mismo
indicador, misma celda y misma escala entre `v0_csv` y la carga candidata: diferencias de
serialización y redondeo de punto flotante. No absorbe cambios de denominador, universo o escala
ni concilia cifras de definiciones distintas. Cualquier diferencia superior a `1e-9` es una
discrepancia bloqueante, se registra en `known_discrepancies.md` y vuelve al productor. No se
ajusta la tolerancia para que un test pase.

## 3. Lo que sigue bloqueado

- `NUMERIC_DATA_GATE_OPEN` para todo lo no enumerado en la sección 1.
- Cifras reales de D06 y D07 hasta aprobar la política de 2.4.
- Publicación, exportación fuera del golden, promoción y cutover.
- Configuración cloud y primer despliegue: `PENDING_VERIFICATION`. El presupuesto de USD 20/mes
  está autorizado; la configuración, el billing, IAM y la lista de seis identidades no lo están.
- Cierre del Sprint 04.2: requiere su matriz de cobertura completa, prueba de rollback y acta
  go/no-go propia. Esta acta no lo cierra.
- Golden existentes: no se reescriben para hacer pasar CI.

## 4. Entregables del siguiente PR de implementación

1. Implementación del alcance autorizado con datos sintéticos y pruebas por adaptador.
2. D01: documentación del sufijo `_fem` y del universo real.
3. D02 y D10: consulta al productor Stage 03 sobre el origen de los ceros, registrada en
   `known_discrepancies.md`.
4. D11: etiqueta exacta del valor `5` de `C3P213`.
5. Borrador de la política de confidencialidad (2.4).
6. `docs/stage04/demo_local_quickstart.md`, verificado desde un clon limpio por alguien distinto
   de Ana.
7. Propuesta de `LICENSE` para aprobación, con sus atribuciones.
8. `docs/security/access_control_plan.md` y `docs/security/access_verification.md`.
9. Actualización del paquete numérico y los bloqueos cloud sin borrar evidencia histórica.

Decisiones tomadas sobre la evidencia del head `cff8faf3`. Si alguna cifra, etiqueta o dominio
cambia respecto de esa evidencia, la autorización correspondiente caduca y vuelve a revisión.

## 5. Adenda supervisora de Etapa 1 — 2026-09-14 UTC

La [revisión formal del PR #62](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/62#pullrequestreview-5192999425)
aprobó la separación de adaptadores. Antes de conectar el primer
agregado, las reglas de CV, N, notas y `quality_status` deben ser funciones puras compartidas por
ambos caminos, y `synthetic=false` debe ser derivado por `AuthorizedAggregateRepository` desde la
procedencia verificada; nunca se acepta de quien llama ni se fija manualmente.

### D01 — textos y agrupación cerrada

- Ítems 1–7: «Porcentaje en que [tarea] la realiza principalmente una mujer del hogar».
- Ítems 8–10: «Porcentaje en que quien [ayuda con las tareas escolares / aconseja y escucha /
  juega con ella] es principalmente una mujer del hogar».
- Los dos bloques representan preguntas distintas y no se combinan en una figura de diez barras.

`predominio_femenino_tareas` permanece fuera de D01. La sintaxis CRS04 confirma que su categoría
0 agrupa predominio masculino, empate y ausencia de ambos, y que la proporción usa los diez ítems
aunque la etiqueta V0 diga «tareas del hogar». Se conserva la etiqueta V0 sin reescribirla y la
discrepancia vuelve al productor.

### Corrección D02 y resolución D10

D02 pertenece a 3.2, no a 3.4. Sus dos ceros son observados: significan que no concurren las tres
violencias, y quien sufrió una o dos sigue contado en sus indicadores propios. Los cuatro ceros de
D10 también son observados.

El linaje de D10 queda resuelto: la base de 9 a 11 años no está disponible en el entorno de
trabajo, así que el bloque CRS03 emparejado no pudo producir ninguna fila. Las filas de
`C3P242_5` y `C3P242_10` provienen del bloque CRS04 de la línea 2416.

D02 y D10 salen de `NON_NUMERIC_CONTEXT` y se publican con su valor visible y CV indefinido por
aritmética. La etiqueta de D02 hace explícita la conjunción: «Porcentaje que sufrió violencia
psicológica, física y sexual en el hogar, las tres simultáneamente».

### Retiro de ampliaciones sin respaldo en V0 — 2026-09-14 UTC

- **D09 Departamento:** se retira la ampliación de 26 categorías. El agregado aprobado contiene
  exactamente 22 filas de `CONS_ATENCION_SALUD` y ninguna dimensión `Departamento`. Esa apertura
  no fue tabulada porque el dominio condicionado dejaba muy pocos casos por celda. D09 queda
  cerrado a los 22 pares existentes y no se reabre la baseline.
- **D01 «nadie»:** se retiran `tarea8_nadie`, `tarea9_nadie` y `tarea10_nadie` de este corte porque
  no existen en el agregado. Quedan registradas como candidatas para un corte posterior que cree
  una versión nueva; Stage 04 no las calcula ni modifica V0.

Etiquetas aprobadas para D09:

| Dimensión | Código | Etiqueta |
|---|---:|---|
| Idioma del hogar | 1 | Castellano |
| Idioma del hogar | 3 | Quechua/Aymara |
| Idioma del hogar | 4 | Otra lengua nativa |
| Etnicidad | 1 | Indígena andino |
| Etnicidad | 3 | Indígena amazónico/nativo |
| Etnicidad | 5 | Afrodescendiente |
| Etnicidad | 6 | No indígena ni afrodescendiente |
| Etnicidad | 9 | No sabe |
| Tipo de hogar | 1 | Biparental |
| Tipo de hogar | 2 | Monoparental |
| Tipo de hogar | 3 | Sin figuras parentales |
| Discapacidad | 0 | No |
| Discapacidad | 1 | Sí |

Trece de las 22 celdas D09 tienen `CV > 15 %`: se muestran visibles, referenciales y con nota.
La alerta de precisión no activa `suppress_flag`.

## 6. Adenda supervisora — catálogo V0 completo — 2026-09-15 UTC

La [revisión formal del PR #91](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/91#pullrequestreview-5215637752)
aprobó el inventario integral del padre V0 y autorizó la clase A como clase. Esta adenda amplía
el alcance numérico local, pero no modifica V0, no autoriza cloud y no autoriza publicación.

| Clase | Filas | Decisión vigente |
|---|---:|---|
| A | 2995 | Autorizadas para conexión `LOCAL_SHADOW_ONLY` bajo las reglas transversales aprobadas |
| B | 0 | No aplica |
| C | 4 | Contexto no numérico: visible, sin tarjeta, tabla numérica ni exportación |
| D | 7 | Distribución `num_consecuencias_fisicas`; adaptador D08, total nunca presentado como prevalencia |
| E | 8 | D06/D07 ya conectadas; `[referencial]` se deriva de `cv_flag` y la discrepancia vuelve a Stage 03 |
| **Total** | **3014** | Catálogo V0 cubierto por una decisión explícita |

Las 2995 filas A conservan el valor con `CV > 15 %` o `base_unw < 30` y muestran la alerta
correspondiente sin supresión. `N` procede exclusivamente de `base_unw`; un cero exacto con CV
indefinido por aritmética es válido; no se supera la granularidad de V0 ni se fabrican cruces.

La implementación requiere un nuevo extracto y manifiesto encadenados al SHA-256 del padre,
rederivación byte a byte, regresión completa y actualización de `authorized_scopes.py`. Si la
navegación no permite localizar un indicador entre los 516 sin recorrer una lista completa, el
trabajo se detiene y vuelve a revisión supervisora.

Continúan separados y bloqueados: recursos y gasto cloud, conexión de cifras reales en cloud
(paso 47), publicación institucional, cutover y sustitución de V0.

## 7. Adenda supervisora — resolución VF_ESCUELA y D06/D07 — 2026-09-18 UTC

La [decisión del Issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5735315006)
prevalece sobre los HOLD históricos de esta acta:

- `VF_ESCUELA` usa diez ítems; la discrepancia «10 frente a 7» queda resuelta y no bloquea el
  indicador.
- D06 y D07 quedan autorizados con cifras reales como matrices fijas de V0. `CV > 15 %` y
  `base_unw < 30` producen alertas visibles, nunca supresión.
- La regla de confidencialidad es el límite de granularidad de V0: no se crean cortes ni cruces
  ausentes del catálogo aprobado.
- Ana y Rita son la autoridad final del proyecto independiente; no existe un gate de aprobación
  institucional externa para esta publicación.

Esta adenda elimina el bloqueante metodológico de confidencialidad para la Decisión B. La carga o
consulta cloud continúa esperando una autorización de ejecución explícita y separada; publicación
y cutover permanecen fuera de alcance.
