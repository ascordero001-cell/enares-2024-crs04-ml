# Política de confidencialidad de agregados — borrador operativo

- Fecha de inicio: 2026-09-14 UTC
- Estado: `PROPOSED_FOR_SUPERVISORY_APPROVAL; D06_D07_REAL_VALUES_BLOCKED`
- Alcance: `LOCAL_SHADOW_ONLY`
- Cloud: `NOT_AUTHORIZED`

Este documento presenta para aprobación supervisora la política del paso 16 y convierte el riesgo
de reconstrucción en controles verificables. No autoriza por sí solo cifras de D06/D07,
publicación, exportación institucional ni despliegue.

## 1. Entradas y parada segura

La decisión de confidencialidad es independiente de las alertas de precisión. `CV > 15 %` y
`base_unw < 30` mantienen la prevalencia visible y nunca activan `suppress_flag`.

Se propone marcar una celda con supresión primaria cuando ocurra al menos uno de estos casos:

1. el conteo no ponderado del evento sensible está entre 1 y 4;
2. su complemento dentro de la base válida está entre 1 y 4; o
3. el productor entrega una alerta de dominancia aprobada y trazable.

Un conteo de evento igual a cero permanece visible si no concurre otro riesgo, en coherencia con
D02/D10. Cinco o más casos no activan por sí solos la supresión. El umbral 5 es una regla propuesta
de control de divulgación, no un indicador de precisión: `CV > 15 %` y `base_unw < 30` continúan
visibles con alerta. Las razones quedan registradas mediante códigos reproducibles; no se permiten
supresiones ad hoc.

La decisión se deriva de conteos validados o de la alerta del productor. No se acepta desde la
interfaz ni se completa por defecto con `false`. Si D06/D07 no traen conteos válidos y una decisión
de dominancia válida, el release falla cerrado antes de `published`. El criterio anterior sigue
pendiente de aprobación explícita de `ritaricaldi-cpu`.

## 2. Supresión complementaria

Para cada ecuación aditiva —total, márgenes de fila y márgenes de columna— se registra su identidad
y sus términos. La selección complementaria usa un orden determinista documentado: primero la
celda publicable de menor `base_unw`, después `cell_id` ascendente como desempate. Cada elección
conserva `suppression_type=COMPLEMENTARY`, razón y vínculo con la primaria protegida.

Después de cada elección se analiza el sistema lineal combinado, no solo cada margen por separado.
Se añaden complementarias hasta que ninguna celda primaria sea resoluble de forma única. Si no se
puede lograr sin invalidar el producto, el release completo se bloquea. Ningún total, margen o
tabla queda exceptuado.

## 3. Protección entre tablas y releases

Todas las tablas del mismo release se analizan como un único sistema de ecuaciones usando una
identidad estable de celda basada en indicador, universo, dimensión, categoría y periodo. Una
tabla segura por separado puede ser insegura al combinarse con otra.

Antes de un release nuevo se repite el análisis contra todos los releases todavía accesibles. Una
celda estable visible en un release anterior no puede protegerse retroactivamente ocultándola en el
nuevo: el nuevo release se bloquea y requiere rediseño o retiro formal del producto anterior. Si la
combinación permite resolver otra celda protegida, se añaden complementarias o se retira la tabla.
Cambiar una etiqueta no crea una identidad distinta para evadir el control.

## 4. Precedencia y materialización

La confidencialidad prevalece sobre calidad y utilidad. Si concurren alerta CV, alerta N y
supresión, la salida es suprimida; las notas de precisión no justifican exponer el valor. Una única
frontera `published` nulifica `estimate`, error estándar, IC, CV, N y población ponderada, y de esa
misma salida segura se derivan UI, exportación, caché y log. Se conservan etiquetas, tipo y razón de
supresión para auditoría. La supresión exclusivamente visual está prohibida.

## 5. Evidencia necesaria para pasar a aprobación

- casos sintéticos con márgenes de fila y columna: implementados;
- dos tablas del mismo release que juntas reconstruyen una celda: implementado;
- dos releases que juntos reconstruyen una celda: implementado;
- imposibilidad de ocultar retroactivamente una celda antes visible: implementada;
- nulificación común antes de UI, export, caché y logs: implementada;
- derivación primaria independiente de CV/N y casos límite 0, 4 y 5: implementada;
- criterio primario, prioridad complementaria y riesgo residual: requieren aprobación supervisora.

## 6. Decisiones solicitadas

Se solicita a `ritaricaldi-cpu` aprobar o ajustar: (a) el rango primario 1–4 para evento y
complemento; (b) el tratamiento visible del cero; (c) la señal de dominancia emitida por el
productor; (d) el orden determinista de complementarias; y (e) el bloqueo combinado entre tablas y
releases. Una aprobación debe anteceder a la conexión de cifras reales de D06 o D07.

Hasta completar y aprobar esa evidencia, D06 y D07 permanecen sin cifras reales. El código y las
pruebas sintéticas pueden avanzar, pero no se conecta ni publica ningún agregado de esos casos.
