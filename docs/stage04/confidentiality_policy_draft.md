# Política de confidencialidad de agregados — borrador operativo

- Fecha de inicio: 2026-09-14 UTC
- Estado: `DRAFT_IMPLEMENTATION_STARTED; PRIMARY_CRITERION_PENDING_APPROVAL`
- Alcance: `LOCAL_SHADOW_ONLY`
- Cloud: `NOT_AUTHORIZED`

Este documento inicia el paso 16 y convierte el riesgo de reconstrucción en controles verificables.
No autoriza cifras de D06/D07, publicación, exportación institucional ni un umbral primario nuevo.

## 1. Entradas y parada segura

La decisión de confidencialidad es independiente de las alertas de precisión. `CV > 15 %` y
`base_unw < 30` mantienen la prevalencia visible y nunca activan `suppress_flag`.

La marca de supresión primaria debe provenir de un proceso institucional aprobado y auditable;
no se deriva de CV/N, no se acepta de la interfaz y no se completa por defecto con `false`. Si una
fila sujeta a control no trae una decisión válida, el release falla cerrado antes de `published`.
El criterio institucional que origina esa marca permanece pendiente de aprobación explícita.

## 2. Supresión complementaria

Para cada ecuación aditiva —total, márgenes de fila y márgenes de columna— una única celda oculta
es reconstruible. Antes de emitir el release deben quedar al menos dos incógnitas en cada ecuación
que contenga una celda primaria. La selección complementaria será determinista, registrada y
procurará minimizar pérdida de información sin revelar la celda primaria. Ningún total o margen
queda exceptuado de este análisis.

## 3. Protección entre tablas y releases

Todas las tablas del mismo release se analizan como un único sistema de ecuaciones usando una
identidad estable de celda basada en indicador, universo, dimensión, categoría y periodo. Una
tabla segura por separado puede ser insegura al combinarse con otra.

Antes de un release nuevo se repite el análisis contra todos los releases todavía accesibles. Si
la combinación permite resolver una celda protegida, el release se bloquea hasta añadir supresión
complementaria, retirar una tabla o retirar formalmente una versión anterior. Cambiar una etiqueta
no crea una identidad distinta para evadir el control.

## 4. Precedencia y materialización

La confidencialidad prevalece sobre calidad y utilidad. Si concurren alerta CV, alerta N y
supresión, la salida es suprimida; las notas de precisión no justifican exponer el valor. La capa
`published` nulifica estimate, error estándar, IC, CV, N y población ponderada antes de UI,
exportación, caché o log. La supresión exclusivamente visual está prohibida.

## 5. Evidencia necesaria para pasar a aprobación

- casos sintéticos con márgenes de fila y columna;
- dos tablas del mismo release que juntas reconstruyen una celda;
- dos releases que juntos reconstruyen una celda;
- prueba de nulificación antes de UI, export, caché y logs;
- registro de decisiones primarias y complementarias reproducible;
- criterio primario, excepciones y riesgo residual aprobados.

Hasta completar y aprobar esa evidencia, D06 y D07 permanecen sin cifras reales. El código y las
pruebas sintéticas pueden avanzar, pero no se conecta ni publica ningún agregado de esos casos.
