# Acta de decisión supervisora — gate numérico D01–D12 — PR #60

**Revisora:** Rita Ricaldi
**Fecha:** 2026-09-13
**PR:** #60 · head `cff8faf3cdf56b4e4304426da6a7c3a69db61f69`
**Evidencia formal:** [Review changes → Approve](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/60#pullrequestreview-5191733879)
**Merge:** `0096842bcbc591d91ea689b2c1ac09ee60e8cbcf` · 2026-09-13T19:14:18Z
**CI de main:** [run 34777073136 — success](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/34777073136)
**Documentos evaluados:** `numeric_authorization_review_20260913.md`, `numeric_gate_decision_package.md`, `spss_numeric_gate_reconciliation.md`, `d09_cons_atencion_salud_domain_evidence.md`
**Estado resultante:** `NUMERIC_SCOPE_PARTIALLY_AUTHORIZED; PUBLICATION_NOT_AUTHORIZED`

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
| **D09** · 3.5 `CONS_ATENCION_SALUD` | AUTORIZADO — los 48 pares exactos | Los 22 pares originales más Departamento: las 26 categorías enumeradas en la adenda de 2026-09-14. | Dominio `CONS_ALGUNA = 1` ya aprobado y su equivalencia estructural R/V0 verificada. El dominio se muestra junto a la cifra. Las celdas departamentales con `base_unw < 30` o `CV > 15 %` siguen visibles con sus alertas; ninguna se suprime por precisión. |
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

### D01 — textos, agrupación y ampliación cerrada

- Ítems 1–7: «Porcentaje en que [tarea] la realiza principalmente una mujer del hogar».
- Ítems 8–10: «Porcentaje en que quien [ayuda con las tareas escolares / aconseja y escucha /
  juega con ella] es principalmente una mujer del hogar».
- Los dos bloques representan preguntas distintas y no se combinan en una figura de diez barras.
- Se autorizan además `tarea8_nadie`, `tarea9_nadie` y `tarea10_nadie`, sin desagregaciones nuevas,
  con el texto «Porcentaje de adolescentes con quienes nadie [ayuda con las tareas escolares /
  conversa y escucha / juega]» y el mismo denominador `n_tareas_validas_8_10` de la serie `_fem`.

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

### D09 — ampliación cerrada a 48 pares

La decisión supervisora del 2026-09-14 añade a los 22 pares previamente autorizados la dimensión
`Departamento` con estas 26 categorías: Amazonas, Apurímac, Arequipa, Ayacucho, Cajamarca,
Callao, Cusco, Huancavelica, Huánuco, Ica, Junín, La Libertad, Lambayeque, Lima Metropolitana,
Loreto, Madre de Dios, Moquegua, Pasco, Piura, Puno, Región Lima, San Martín, Tacna, Tumbes,
Ucayali y Áncash.

El alcance D09 queda cerrado en 48 pares. Por el dominio `CONS_ALGUNA = 1`, una celda
departamental puede tener simultáneamente `base_unw < 30` y `CV > 15 %`; en ese caso la
prevalencia sigue visible, referencial y con ambas notas. Estas alertas de precisión no activan
supresión.
