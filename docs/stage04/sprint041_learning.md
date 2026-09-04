# Aprendizajes del corte vertical local 3.2

`outputs`, `published` y `ops` resuelven problemas distintos. `outputs` conserva todo el historial
de resultados candidatos. `published` es la superficie segura que solo deja pasar agregados
aprobados y ya suprimidos. `ops` registra qué ocurrió, qué controles pasaron, qué release está
vigente y cómo volver al anterior.

Stage 04 no recalcula Stage 03 porque el diseño, universo y reglas ya fueron validados allí.
Recalcularlos introduciría otra definición metodológica. En su lugar, el `source_hash` demuestra
qué objeto agregado exacto se usó; si cambian sus bytes, cambia el hash y la revisión deja de
aplicar automáticamente.

Un golden test congela la respuesta esperada del piloto: números, textos, estados y linaje. No
demuestra por sí solo que la metodología sea correcta, pero detecta cambios inesperados. La
tolerancia propuesta de `1e-9` solo cubre serialización; aumentarla para hacer pasar una diferencia
ocultaría un problema en vez de explicarlo.

La supresión primaria oculta una celda pequeña. Si total y celdas vecinas siguen visibles, esa
celda puede recuperarse por resta. La supresión complementaria oculta otra pieza de la ecuación y
evita una solución única. El control debe vivir en `published`, no solo en la pantalla.

La aplicación nunca debe acceder a microdatos porque no necesita registros individuales para
mostrar vigilancia poblacional y porque aumentaría innecesariamente el riesgo de exposición. Una
promoción cambia `current_release` solo hacia un release aprobado. Un rollback restaura el puntero
aprobado anterior, sin borrar el historial ni esconder la corrida problemática.
