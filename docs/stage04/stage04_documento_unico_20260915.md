# Stage 04 CRS04 — documento unico al 15 de septiembre de 2026

**Fecha:** 2026-09-15
**Fuente de autoridad:** decisiones de Rita Ricaldi, supervisora.
**Reemplaza a:** nada. Complementa el plan rector de 53 pasos, el acta D01-D12 del 2026-09-13 y
la adenda de esa misma fecha.

Este documento reune en un solo sitio tres cosas que hasta ahora estaban separadas: el estado
real de los 53 pasos, las decisiones tomadas el 15 de septiembre, y el trabajo que no existe en
la numeracion original. Sustituye a cualquier version parcial anterior de estas materias.

---

# PARTE 1. Donde esta el proyecto hoy

| Indicador | Valor |
|---|---|
| Pasos del plan cerrados | 44 de 53 |
| Filas del agregado V0 conectadas en la aplicacion | 3.014 de 3.014 |
| Recursos creados en Google Cloud | 0 |
| Consultas ejecutadas en Google Cloud | 0 |
| Gasto acumulado | USD 0 |

**Ana termino los pasos 1 a 42, incluido el paso 36, y no puede entrar al 43.** Tambien esta
cerrado el paso 50, que se adelanto.

Lo que separa el estado actual de la Etapa 7 es una sola cosa, y no ocurre en GitHub: que exista
el proyecto de Google Cloud vinculado a una cuenta de facturacion. Esta detallado en la seccion J.

---

# PARTE 2. Decisiones del 15 de septiembre

## A. Origen de `outputs.indicator_estimates`

`outputs.indicator_estimates` se carga **exclusivamente** desde el extracto agregado autorizado
de V0, encadenado por SHA-256 al archivo padre congelado. No se deriva, ni total ni parcialmente,
de `analytical`, `cleaned`, `raw` ni `survey_input`.

Fundamento:

1. La sintaxis fuente sigue en revision del INEI. `analytical` se computa desde ella; V0 es la
   salida congelada. Publicar desde `analytical` haria que las cifras cambiaran cuando cambie una
   sintaxis aun no aprobada, sin decision supervisora y sin que se note en pantalla.
2. Se romperia la cadena de procedencia: un extracto de V0 encadena a un SHA congelado y tiene
   rederivacion byte a byte; una tabla calculada depende del estado de `raw`, `cleaned`, la
   version de la sintaxis y la corrida.
3. Las aserciones `*_v0_parity` comparan registro por registro la derivacion en SQL contra la
   base analitica del SPSS. Validan la construccion de variables, no los estimadores ponderados.
4. La cobertura no esta demostrada: V0 tiene 516 indicadores; `analytical` tiene siete
   definiciones y tres pilotos.

`analytical` conserva su funcion de verificacion de la migracion. El contraste a nivel de
agregado no existe hoy en Dataform; si alguna vez se quiere usar como control cruzado, esa
asercion debe escribirse primero, y su resultado nunca sustituye la cifra de V0: una diferencia
se registra en `known_discrepancies.md` y vuelve al productor.

**Estado: incorporado** a `docs/contracts/published_view_contract.md`, PR #90, fusionado.

## B. Ampliacion del alcance numerico: clase A

Base: inventario integral del padre V0, PR #91.

- padre V0: `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`
- filas evaluadas: 3.014 · indicadores: 516 · indicadores integramente en clase A: 511

| Clase | Filas | Resultado |
|---|---:|---|
| A. Publicable directa | 2.995 | **autorizada** |
| B. Estadisticos incompletos | 0 | no aplica |
| C. Contexto no numerico | 4 | tratamiento en la seccion C |
| D. Requiere adaptador | 7 | tratamiento en la seccion C |
| E. Etiqueta ambigua | 8 | tratamiento en la seccion C |

**Queda autorizada la clase A completa**, como clase y no indicador por indicador, bajo las
reglas transversales ya decididas y que esta adenda no modifica:

- `CV > 15 %` conserva el valor, lo marca como referencial y muestra su nota. Nunca suprime.
- `base_unw < 30` conserva el valor y muestra su alerta. Nunca suprime.
- `N` procede exclusivamente de `base_unw`.
- Un cero exacto observado tiene CV indefinido por aritmetica y es salida valida.
- No existe umbral primario de supresion por recuento.
- La granularidad nunca supera la de V0 y no se fabrican cruces.

Un CV superior al 15 % o un `base_unw` inferior a 30 **no excluyen** de la clase A.

## C. Las 19 excepciones

| Clase | Filas | Indicadores | Tratamiento | Precedente |
|---|---:|---|---|---|
| C | 4 | `Solap_VP_VF_E`, `Solap_VP_VF_H` | Contexto no numerico: visibles, sin tarjeta, sin tabla numerica, sin exportacion | Filas de contexto de D04 y D05 |
| D | 7 | `num_consecuencias_fisicas` | Adaptador de distribucion, como total de distribucion y nunca como prevalencia | D08 |
| E | 8 | `Solap_VS_12M`, `Solap_VS_VIDA` | Ya autorizados y conectados; el marcador se deriva de `cv_flag`, no del texto de origen | D06 y D07, PR #67 |

**En conjunto, las 3.014 filas del padre V0 quedan cubiertas:** 2.995 como prevalencias
ordinarias, 7 como distribucion, 8 ya conectadas, y 4 como contexto visible sin metricas.
Ninguna fila del agregado queda fuera del producto.

## D. Discrepancia devuelta a produccion Stage 03

Las ocho filas de clase E salen marcadas porque el sufijo `[referencial]` viene escrito dentro de
la categoria **en el propio V0**. La correccion aplicada en Stage 04 es correcta y se conserva,
pero el origen es un defecto de V0: un marcador de presentacion no pertenece a una etiqueta de
identidad, y ya provoco un error detectado en el PR #67.

Registrado en `known_discrepancies.md` con indicador, dimension y las ocho categorias, y devuelto
al productor mediante el Issue #101 para correccion en la proxima version de V0. No se corrige en
Stage 04; el registro queda efectivo cuando se fusione el PR #100.

## E. Ubicacion e implementacion

**Sprint 04.2.** Diecinueve excepciones, quince de ellas patrones ya resueltos, quedan muy por
debajo del umbral que habria justificado aplazar al 04.3.

Patron de implementacion, el mismo de los PR #64 y #67: alcance en `authorized_scopes.py` (ruta
protegida), extracto nuevo con manifiesto encadenado al SHA del padre, prueba de rederivacion
byte a byte, y regresion completa.

**Condicion de cierre: navegacion.** Pasar de 52 filas a 2.995 cambia el problema, no solo el
volumen: Departamento aporta ella sola 1.294 filas y el catalogo son 516 indicadores en seis
modulos y nueve dimensiones. Si al conectar el catalogo completo no se puede encontrar un
indicador concreto sin recorrer la lista entera, **el paso se detiene y vuelve a revision
supervisora**, aunque las cifras sean correctas. Cobertura numerica no equivale a producto
utilizable.

## F. Lo que estas decisiones no autorizan

- Recursos cloud, ejecucion de la Etapa 7 ni gasto.
- Conectar cifras reales en la nube: sigue siendo el paso 47, decision separada.
- Publicacion institucional, cutover ni sustitucion de V0.
- Cortes mas finos que V0 ni cruces ausentes del agregado.
- Comparaciones entre departamentos, cohortes o rondas: el estadistico de la diferencia no esta
  en V0 y Stage 04 no lo calcula. Si se quiere, debe venir de produccion Stage 03.

## G. Efecto sobre decisiones anteriores

**Casos autorizados y no conectados.** D02, D03, D04, D05, D08 y D10 tenian decision desde el
2026-09-13 pero no estaban implementados. La ampliacion de la clase A los absorbe; no se conectan
por separado.

**Matriz de cobertura.** Su columna de pendientes mezclaba dos estados: lo que falta por conectar
y lo que falta por decidir. Debe separarlos.

**Cambio futuro conocido.** Etnicidad, Lengua materna y Tipo de hogar suman 561 filas de clase A
y son las que se veran afectadas cuando el INEI apruebe la reordenacion de categorias. Cuando
llegue ese V0 nuevo, la verificacion de paridad del release candidato debe contrastar
**etiquetas** y no solo codigos: una renumeracion deja intacto el codigo y cambia su significado.
Sin fecha.

## H. Verificaciones que no dependen de terceros

Tres pasos exigian personas ajenas al equipo. Esa exigencia procede de la practica estandar de
usabilidad y no corresponde a este proyecto: el equipo son dos personas y la aplicacion muestra
datos sobre violencia contra adolescentes. Los tres se reescriben conservando su proposito.
Ninguno se elimina. El texto nuevo esta en la Parte 3, pasos 36, 48 y 51.

**Riesgo residual registrado.** Estos metodos detectan incumplimientos de principios conocidos.
No detectan lo que descubre una persona que usa la aplicacion por primera vez con un problema
real delante. Esa cobertura no se obtiene y no se simula: queda anotada en la evidencia de los
pasos 36, 48 y 51.

## J. Titularidad y desbloqueo del gate cloud

### Quien es que

- **Ana es propietaria del proyecto de Google Cloud y titular de la cuenta de facturacion**, con
  su propio medio de pago. Construye, configura, opera y asume el riesgo economico.
- **Rita es supervisora.** No es propietaria del proyecto ni titular de la facturacion.

Esto corrige el paquete de GO del 2026-09-14, que describia administracion compartida.

**Dicho sin adornos:** la supervision de Rita no se ejerce mediante permisos de nube. Rita no
puede detener el gasto por si misma, porque la cuenta no es suya. Sus controles efectivos son:

1. **`CODEOWNERS` sobre las rutas metodologicas del repositorio.** Control tecnico real: el acta,
   los contratos, `authorized_scopes.py` y `quality_rules.py` no cambian sin su revision.
2. **Los gates de autorizacion**: paso 47 y paso 53.
3. **Visibilidad**: roles de lectura sobre el proyecto y alertas de gasto dirigidas a las dos.

El tope historico de USD 20 al mes queda conservado en las decisiones del 2026-09-13 y 2026-09-14.
La decision operativa posterior del 2026-09-17 fija un limite estricto de USD 0 y bloquea toda
ejecucion cloud. Los presupuestos de Cloud Billing son alertas, no topes automaticos.

### Secuencia de desbloqueo

| # | Accion | Quien |
|---|---|---|
| 1 | Confirmar la cuenta de facturacion activa, con medio de pago y medios de recuperacion | CERRADO privadamente por Ana |
| 2 | Comprobar si existe el proyecto `enares-2024-crs04`; anotar ID y numero solo en el registro privado | CERRADO privadamente por Ana |
| 3 | Vincular el proyecto a la cuenta de facturacion | CERRADO; vinculo verificado |
| 4 | Aplicar el limite operativo estricto USD 0 | CERRADO como condicion de parada; no crea alertas ni autoriza consumo |
| 5 | Conceder a Rita `roles/run.viewer`, `roles/logging.viewer` y `roles/monitoring.viewer` | NO EJECUTAR con limite USD 0 |
| 6 | Confirmar a Rita, por canal privado, ID y numero de proyecto, vinculo efectivo y recepcion de una alerta de prueba | BLOQUEADO por pasos 4 y 5 |

La verificacion de Rita consiste en recibir esa confirmacion y comprobar que sus roles funcionan.
No obstante, con limite estricto USD 0 el gate no se levanta y el paso 43 no puede iniciar.

### Composicion de los seis accesos

| Identificador | Nivel | Acceso |
|---|---|---|
| `viewer_01` a `viewer_04` | Consulta | Solo `roles/run.invoker`. Ningun otro permiso |
| Ana | Propiedad y operacion | Propietaria del proyecto y titular de la facturacion |
| Rita | Supervision | Los tres roles de lectura y las alertas |

Los identificadores `viewer_01` a `viewer_04` son etiquetas de registro. Los principales exactos,
la persona y su cargo se mantienen en el registro privado y nunca entran al repositorio.
Registrar el cargo permite que una sustitucion sea un cambio de una linea.

**Lo que sigue excluido sin excepcion:** la identidad de ejecucion de la aplicacion conserva
`roles/bigquery.jobUser` sobre el proyecto y `roles/bigquery.dataViewer` unicamente sobre
`published`. Nunca alcanza `raw`, `cleaned`, `analytical`, `outputs` ni `survey_input`, y nunca se
emiten claves JSON. Ese es el control que protege los datos y no depende de quien sea propietaria.

### Titularidad en la entrega institucional

Una cuenta de facturacion personal no es el soporte adecuado para una herramienta que va a
entregarse a una institucion. Antes de cualquier entrega debe resolverse quien asume la
facturacion y la propiedad del proyecto. Sin fecha ni solucion: queda registrado para que la
entrega no ocurra sin haberlo decidido.

---

# PARTE 3. Los 53 pasos, uno por uno

Estados: **CERRADO** · **PENDIENTE** · **BLOQUEADO** (espera el gate cloud) · **REESCRITO** (su
metodo cambia por la seccion H; el proposito se conserva).

## Etapa 0 — cerrar lo ya decidido

| # | Paso | Estado |
|---|---|---|
| 1 | PR #60 fusionado | CERRADO |
| 2 | Versionar el acta D01-D12 en `docs/stage04/` y enlazarla | CERRADO |
| 3 | Actualizar `numeric_gate_decision_package.md` y `cloud_blockers.md` | CERRADO |
| 4 | Corregir la dependencia caduca del issue local 43 | CERRADO |

## Etapa 1 — implementar el alcance autorizado

| # | Paso | Estado |
|---|---|---|
| 5 | D12a y D12b: los dos alias en tarjeta, tabla, grafico, tooltip, impresion y exportacion | CERRADO |
| 6 | D01: documentar que mide el sufijo `_fem` | CERRADO |
| 7 | D11: etiqueta exacta del valor 5 de `C3P213` | CERRADO |
| 8 | D02 y D10: consulta al productor sobre el origen de los ceros | CERRADO |
| 9 | Implementar los adaptadores autorizados con nombre y version | CERRADO |
| 10 | Separar el adaptador de pruebas sinteticas del institucional autorizado | CERRADO |
| 11 | Conectar D09 con sus 22 pares y el dominio visible | CERRADO |
| 12 | Contexto no numerico para D02, D10 y las filas de D04 y D05 | CERRADO |
| 13 | D06 y D07 con adaptador y pruebas | CERRADO |
| 14 | Regresion obligatoria en cada ampliacion | CERRADO |
| 15 | Cierre de etapa: suite verde, golden intacto, capturas | CERRADO |

## Etapa 2 — politica de confidencialidad

| # | Paso | Estado |
|---|---|---|
| 16 | Politica de confidencialidad entregada para decision | CERRADO. Resuelta sin umbral por recuento; el limite es la granularidad de V0 |

## Etapa 3 — infraestructura escrita y probada en local

| # | Paso | Estado |
|---|---|---|
| 17 | `ops/release_registry.sqlx` y `ops/current_release.sqlx` compilando | CERRADO |
| 18 | `published/v_dashboard_current.sqlx` con la proyeccion segura minima | CERRADO |
| 19 | Maquina de promocion y rollback con backend en memoria | CERRADO |
| 20 | Los cinco criterios de aceptacion sin tocar la nube | CERRADO |
| 21 | `promotion_rollback_runbook.md` | CERRADO |
| 22 | Contenedor construido, arrancado y demostrado | CERRADO |

## Etapa 4 — higiene de ingenieria y gobernanza

| # | Paso | Estado |
|---|---|---|
| 23 | `app-ci.yml` con ruff, mypy, pytest y build de imagen | CERRADO |
| 24 | Firmas tipadas compartidas y mypy en verde | CERRADO |
| 25 | Taxonomia `RepositoryError` con sus tres casos | CERRADO |
| 26 | Cache indexada por `release_id` y `run_id` | CERRADO |
| 27 | Dependabot y auditoria de dependencias | CERRADO |
| 28 | Gitleaks o equivalente bloqueando el merge | CERRADO |
| 29 | Proteccion de `main`: PR obligatorio y checks en verde | CERRADO |
| 30 | Templates de Issue y PR, y `CODEOWNERS` sobre las rutas metodologicas | CERRADO |
| 31 | ADR Repository | CERRADO |
| 32 | `threat_model.md` al dia | CERRADO |
| 33 | Logica productiva fuera de los notebooks | CERRADO |

## Etapa 5 — entregas de la adenda

| # | Paso | Estado |
|---|---|---|
| 34 | `LICENSE` propuesta y aprobada | CERRADO. Apache-2.0, titular Ana, `NOTICE` sin atribucion institucional |
| 35 | `CONTRIBUTING.md` | CERRADO |
| **36** | **REESCRITO** — ver texto abajo | CERRADO |
| 37 | `docs/security/access_control_plan.md` | CERRADO |
| 38 | `docs/security/access_verification.md` como plantilla con los cinco escenarios | CERRADO |
| 39 | Exportacion CSV y Excel con `test_export_formats.py` y `test_xlsx_package_privacy.py` | CERRADO |

### Paso 36 reescrito

**Decia:** verificar el quickstart desde un clon limpio por una persona distinta de Ana.

**Dice ahora:** un job de integracion continua que ejecuta el quickstart sobre un runner limpio.
Un runner de GitHub Actions es por definicion un clon nuevo, sin credenciales ni cuenta de
Google, de modo que la condicion documental se cumple mecanicamente.

**Requisito de calidad:** el job extrae los comandos de los bloques de codigo del propio
`docs/stage04/demo_local_quickstart.md`, no los reproduce en el workflow. Asi, el dia que la guia
y el repositorio se desincronicen, el PR falla. Esa desincronizacion es el fallo real de un
quickstart, y una verificacion humana unica tampoco lo habria cazado.

**Evidencia de cierre:** PR #103, merge
`042bffde5fda22012ac3fb37485372ded1f96016`, y ejecución del quickstart en `main`
[35042028920](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/35042028920),
con resultado `SUCCESS`.

**Riesgo residual:** el control prueba desde un checkout limpio que los comandos documentados se
ejecutan correctamente, pero no comprueba que una persona haya leido y comprendido la prosa.

El cierre documental de este paso no modifica ningun gate cloud ni autoriza crear recursos,
conectar cifras reales en cloud, publicar o hacer cutover.

## Etapa 6 — preparacion y autorizacion de la configuracion cloud

| # | Paso | Estado |
|---|---|---|
| 40 | `cloud_authorization.md` con los controles H1 | CERRADO. Su tabla de IAM queda corregida por la seccion J |
| 41 | Comprobar disponibilidad de `Spend cap budgets` y proponer importe | CERRADO |
| 42 | Revision GO/NO-GO del primer despliegue | CERRADO. `GO_FOR_STAGE7_CONTROLLED_SHADOW`, 2026-09-14 |

## Etapa 7 — configurar, verificar y solo entonces conectar

Los siete estan **BLOQUEADOS** por `ZERO_BUDGET_HARD_STOP`. El orden entre ellos no es negociable:
nada se configura o despliega mientras el limite operativo sea `USD 0`.

| # | Paso | Estado |
|---|---|---|
| 43 | Configuracion base, sin datos | BLOQUEADO por limite estricto USD 0 |
| 44 | Billing y limites en funcionamiento | VINCULO VERIFICADO; consumo BLOQUEADO por limite estricto USD 0 |
| 45 | Identidades y acceso, antes de desplegar nada | BLOQUEADO. La composicion esta en la seccion J |
| 46 | Verificacion con datos sinteticos; URL en estado DEMO | BLOQUEADO |
| 47 | **Autorizacion para conectar cifras reales — decision de Rita** | BLOQUEADO |
| **48** | **REESCRITO** — ver texto abajo | BLOQUEADO en su mitad cloud; la otra mitad se adelanta |
| 49 | Corrida de evidencia: promocion y rollback reales con paridad | BLOQUEADO |

### Paso 48 reescrito

**Decia:** prueba seis sesiones simultaneas con navegacion y filtros, midiendo consumo.

**Dice ahora:** la prueba se ejecuta con **sesiones automatizadas, no con seis personas**. Seis
contextos de navegador concurrentes con Playwright, que el repositorio ya incorpora desde el
PR #94, navegando y filtrando mientras se mide consumo, latencia y numero de instancias.

Las identidades empleadas en las pruebas de acceso de los pasos 38 y 46 siguen siendo ficticias,
como ya establecia el plan.

**Mitad adelantable:** el guion se escribe y se prueba contra la aplicacion local ahora. Solo la
medicion de consumo e instancias espera a que exista Cloud Run.

## Etapa 8 — cierre

| # | Paso | Estado |
|---|---|---|
| 50 | Matriz de cobertura 3.1-3.6 en cuatro estados | CERRADO |
| **51** | **REESCRITO** — ver texto abajo | CERRADO: accesibilidad manual, heuristicas y recorrido cognitivo completos |
| 52 | URL registrada en README, About, PR y Release, con su advertencia de estado | BLOQUEADO: necesita que exista una URL |
| 53 | **Paquete de cierre para revision final — decision de Rita** | PENDIENTE |

### Paso 51 reescrito

**Decia:** prueba automatica de WCAG 2.2 AA, revision manual, evaluacion heuristica y prueba con
tres a cinco personas sobre datos sinteticos.

**Dice ahora:** se conserva la auditoria automatica, ya entregada en el PR #94, y la prueba con
personas se sustituye por tres metodos que no requieren participantes externos:

1. **Revision manual de accesibilidad:** navegacion exclusivamente por teclado, lectura con
   lector de pantalla, comprobacion manual de contraste, y zoom al 200 % sin perder contenido ni
   funcion. La auditoria automatica no cubre ninguna de las cuatro.
2. **Evaluacion heuristica** contra las diez heuristicas de Nielsen, con hallazgos clasificados
   por severidad. Metodo de evaluador unico.
3. **Recorrido cognitivo** sobre los escenarios de `docs/hci/task_scenarios.md`: para cada paso de
   cada tarea, si la persona sabria que hacer, si veria el control y si entenderia el resultado.
   Metodo disenado para ejecutarse sin usuarios.

**Hacerlos despues de conectar la clase A, no antes.** Evaluar la navegacion de una aplicacion de
52 filas no dice nada sobre una de 3.014.

---

# PARTE 4. Trabajo fuera de los 53 pasos

El plan rector nunca contemplo estas cuatro cosas. No llevan numero y no renumeran nada.

| Trabajo | Que es | Donde | Estado |
|---|---|---|---|
| Contrato de origen de `outputs` | Edicion de contrato | `docs/contracts/published_view_contract.md` | HECHO, PR #90 |
| Versionar este documento | Registro de las decisiones | `docs/stage04/` | HECHO, PR #100 |
| Conectar el V0 integral | 2.995 filas mas las 19 excepciones | `authorized_extract.py`, `app/data/` | HECHO, PR #112; evidencia E fijada en PR #113 |
| Discrepancia del `[referencial]` | Registro y devolucion al productor | `known_discrepancies.md`, Issue #101 | HECHO, PR #100 |

---

# PARTE 5. Que hace Ana ahora, en orden

## Sin depender de nadie, desde ya

1. Mantener verde la auditoria automatica y la regresion integral mientras se resuelve el gate.

## Cuando quiera, en paralelo con lo anterior

2. **La secuencia de desbloqueo de la seccion J**, los seis puntos. En cuanto este el punto 6,
   Rita verifica y se levanta el gate.

## Solo con el gate levantado

3. Pasos **43 a 49**, en ese orden.

## Al final

4. Paso **52** y paso **53**.

---

# PARTE 6. Que vuelve a Rita

| Cuando | Que |
|---|---|
| Ahora | Aprobar el PR que versiona este documento |
| Ahora | Aprobar el PR de la clase A: toca `authorized_scopes.py` |
| Cuando Ana lo confirme | Verificar proyecto, vinculo de facturacion y sus propios roles de lectura |
| Si la navegacion no aguanta | Decidir sobre la condicion de parada del punto 2 |
| Paso 47 | Autorizar la conexion de cifras reales en la nube |
| Paso 53 | Decidir el cierre del sprint |

Cualquier PR que toque el acta, los contratos, `authorized_scopes.py`, `quality_rules.py`,
`cloud_authorization.md` o `cloud_blockers.md` le llega automaticamente por `CODEOWNERS`.

---

# PARTE 7. Advertencia de cierre

En dos dias se fusionaron 25 PR. La disciplina fue buena, pero en esa revision aparecieron cinco
defectos y **todos eran de la misma familia**: un control cuyo nombre prometia mas de lo que su
codigo comprobaba. El diagnostico de release que miraba una sola fila. El `[referencial]` metido
en la etiqueta. La senal de dominancia que no calculaba nada. El `follow_imports = skip` que
apagaba mypy entre modulos. El contador de residuales de accesibilidad que no se afirmaba.

Los cinco se corrigieron. Pero aparecieron revisando, no auditando, y no hay razon para suponer
que fueran los unicos.

**Antes del paquete de cierre del paso 53 se hara una pasada especifica sobre lo construido esos
dos dias, buscando ese patron.** Es una tarde de trabajo y es exactamente lo que un paquete de
cierre debe sostener.

---

Sprint 04.2 no se cierra por este documento, por un PR documental ni por CI en verde. Requiere el
paquete del paso 53 y revision supervisora.
