# Política de confidencialidad de agregados

- Fecha de decisión: 2026-09-14 UTC
- Estado: `APPROVED; NO_PRIMARY_SUPPRESSION_ACTIVE`
- Alcance: `LOCAL_SHADOW_ONLY`
- Cloud: `NOT_AUTHORIZED`
- Revisión supervisora: aprobación de `ritaricaldi-cpu` en el PR #66

Esta política protege la confidencialidad manteniendo exactamente la granularidad de los tabulados
oficiales V0. No define un umbral por recuento y no autoriza publicación institucional, cutover ni
despliegue.

## 1. Regla vigente: límite de granularidad

La base ENARES es anónima y el agregado V0 no presenta cortes por distrito, escuela o conglomerado.
Por ello, el recuento de una celda no constituye aquí un criterio de supresión. No existe regla
1–4, ni para la aplicación ni para sus exportaciones.

La aplicación:

1. no muestra ningún corte más fino que el contenido en V0;
2. no fabrica cruces ausentes de los tabulados oficiales; y
3. conserva las cifras de V0 sin recalcularlas, redefinirlas o suprimirlas selectivamente.

`CV > 15 %` y `base_unw < 30` mantienen la prevalencia visible con sus alertas. Nunca activan
`suppress_flag`. Una cifra oficial con evento igual a cero también permanece visible y conserva el
CV ausente cuando corresponda.

## 2. Maquinaria de supresión inactiva

No existe supresión primaria activa en el alcance actual. Tampoco existe hoy un campo, cálculo o
señal de dominancia en V0; por tanto, la dominancia no se presenta como regla aplicable.

Se conserva la maquinaria de supresión complementaria y verificación de márgenes, multitabla y
multirelease, con sus pruebas sintéticas, pero permanece inactiva mientras no exista una supresión
primaria. Solo se reabrirá este gate si se propone y autoriza expresamente:

- un corte más fino que departamento; o
- un cruce que no exista en los tabulados oficiales V0.

Una propuesta así requerirá antes de conectarse una nueva política supervisada, señal primaria
explícita, análisis de riesgo y evidencia de no reconstrucción. No puede activarse desde la interfaz
ni mediante valores escritos manualmente por quien llama.

## 3. Márgenes, tablas y releases

La maquinaria inactiva conserva una identidad estable de celda basada en indicador, universo,
dimensión, categoría y periodo. Si llegara a activarse, todas las ecuaciones y tablas se evaluarían
como un único sistema y las complementarias se seleccionarían de forma determinista. Un release se
bloquearía si una primaria pudiera reconstruirse o no existiera un plan seguro.

Todo lo que haya sido publicado se considera permanentemente expuesto, aunque el release deje de
estar accesible. Una celda estable visible en cualquier release anterior no puede protegerse de
forma retroactiva ocultándola después. Retirar acceso no equivale a despublicar.

## 4. Precedencia y materialización de la maquinaria inactiva

Si un gate futuro activara supresión primaria, la confidencialidad prevalecería sobre calidad y
utilidad. Una única frontera `published` nulificaría `estimate`, error estándar, IC, CV, N y
población ponderada antes de UI, exportación, caché o log. Se conservarían etiquetas, tipo y razón
de supresión para auditoría. La supresión exclusivamente visual seguiría prohibida.

Esta precedencia no suprime hoy ninguna cifra V0: no existe señal primaria activa.

## 5. Evidencia automatizada conservada

Las veinte pruebas específicas cubren:

- el límite de dimensiones y cruces de V0;
- la activación exclusivamente ante una futura ampliación autorizada;
- márgenes aditivos y selección complementaria determinista;
- reconstrucción combinada entre tablas;
- reconstrucción combinada entre releases;
- imposibilidad de ocultar retroactivamente una celda ya publicada; y
- nulificación común antes de UI, export, caché y logs.

Estas pruebas mantienen preparado el control futuro sin alterar ninguna cifra oficial actual.

## 6. D06 y D07

La aprobación supervisora retira el bloqueo que dependía de esta política. D06 y D07 pueden
conectarse con sus cifras reales mediante un PR posterior, conservando por separado sus universos,
adaptadores, matrices completas, evidencia V0 y regresión. Esta autorización no permite crear
cruces nuevos ni ampliar la granularidad existente.
