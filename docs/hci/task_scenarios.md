# Escenarios de tareas HCI — Sprint 04.2

Estado: `READY_FOR_INDEPENDENT_SYNTHETIC_TEST`.
Fecha: 2026-09-15.

Estos escenarios evalúan la comprensión y el uso de la interfaz sin conectar nuevas cifras ni
recursos cloud. La prueba formativa se ejecutará únicamente con una instancia y datos sintéticos.
No se solicitarán nombres de NNA, búsquedas individuales ni información sensible a las personas
participantes.

## Criterios comunes

- La persona completa la tarea sin acceder a una dimensión o cruce no autorizado.
- La interpretación distingue cifra, universo, denominador, calidad y release.
- Una combinación no disponible termina en un mensaje `sin datos`; la interfaz nunca fabrica el
  resultado.
- Solo se descarga el corte agregado visible y autorizado.
- Se registran tiempo, errores, dudas y resultado, pero no datos personales innecesarios.

## Tarea 1 — Encontrar la prevalencia nacional de 3.4

- **Persona usuaria:** analista de política pública que consulta ENARES.
- **Necesidad:** encontrar la prevalencia nacional disponible del módulo 3.4 y reconocer a qué
  encuesta corresponde.
- **Pasos previstos:** abrir `Módulo 3.4`; mantener `Nacional`; leer el indicador, la categoría y
  la identificación de CRS04 que presenta la vista.
- **Resultado esperado:** identifica la cifra mostrada como un agregado de ENARES 2024 CRS04 y no
  como un resultado individual, distrital o de otra cohorte.
- **Errores previsibles:** confundir CRS04 con CRS03; buscar un corte departamental inexistente;
  interpretar el porcentaje sin leer el universo.
- **Riesgo de interpretación:** atribuir el resultado a toda la población cuando la pregunta tiene
  un universo específico.
- **Criterio de éxito:** localiza la vista y explica correctamente encuesta, módulo, dimensión y
  universo sin ayuda de la persona facilitadora.

## Tarea 2 — Interpretar una estimación referencial

- **Persona usuaria:** especialista que prepara una nota técnica.
- **Necesidad:** determinar si una cifra visible requiere cautela por precisión estadística.
- **Pasos previstos:** localizar una fila marcada `Referencial`; revisar el marcador, la nota de
  calidad, `CV` y `N no ponderado`.
- **Resultado esperado:** explica que `CV > 15 %` genera una alerta visible pero no supresión, y
  que `N no ponderado` procede de `base_unw`; una base menor que 30 también alerta sin ocultar la
  prevalencia.
- **Errores previsibles:** leer `N` como población expandida; asumir que `Referencial` significa
  dato inválido; esperar una celda suprimida.
- **Riesgo de interpretación:** omitir la nota de precisión al comunicar la cifra.
- **Criterio de éxito:** reconoce el estado y formula una interpretación con cautela, sin afirmar
  que la cifra fue suprimida o recalculada por Stage 04.

## Tarea 3 — Cambiar la desagregación sin crear combinaciones inválidas

- **Persona usuaria:** analista que compara los cortes autorizados de un módulo.
- **Necesidad:** cambiar la dimensión y reconocer cuándo un corte no existe en V0.
- **Pasos previstos:** elegir un módulo; abrir el selector `Dimensión`; seleccionar una opción
  disponible; observar la vista o el mensaje fail-closed.
- **Resultado esperado:** solo consulta pares dimensión/categoría existentes en el alcance
  autorizado; ante una combinación ausente entiende el mensaje `sin datos`.
- **Errores previsibles:** interpretar el listado de dimensiones futuras como autorización;
  intentar combinar categorías de dos dimensiones; asumir que `sin datos` equivale a cero.
- **Riesgo de interpretación:** presentar una combinación no publicada como si fuera un resultado
  oficial.
- **Criterio de éxito:** cambia de dimensión sin obtener un cruce cartesiano inventado y explica
  que `sin datos` no representa el valor cero.

## Tarea 4 — Descargar solamente el corte agregado visible

- **Persona usuaria:** analista que necesita reutilizar una tabla en un informe.
- **Necesidad:** exportar a CSV o Excel exactamente el corte agregado mostrado.
- **Pasos previstos:** llegar a una vista con resultados; verificar módulo, dimensión y filtros;
  usar `Descargar CSV` o `Descargar Excel`; comparar el archivo con la tabla visible.
- **Resultado esperado:** el archivo contiene el corte visible, sus metadatos de calidad y ninguna
  fila individual, ruta privada, credencial o localizador interno.
- **Errores previsibles:** esperar una descarga de toda la base; confundir el archivo con
  microdatos; no comprobar el filtro activo.
- **Riesgo de interpretación:** reutilizar el archivo fuera de contexto o sin sus notas de CV y N.
- **Criterio de éxito:** confirma que el contenido corresponde al filtro visible, conserva las
  notas y no incluye más granularidad que V0.

## Tarea 5 — Verificar universo, denominador, metodología y release

- **Persona usuaria:** revisora institucional que contrasta la trazabilidad de una cifra.
- **Necesidad:** decidir si cuenta con el contexto mínimo para citar un resultado.
- **Pasos previstos:** leer universo y denominador de una estimación; abrir `Metodología`; abrir
  `Estado del release`; relacionar las reglas mostradas con el identificador del release.
- **Resultado esperado:** identifica el universo, el denominador, las reglas de CV/N, la ausencia
  de supresión por recuento, el límite de granularidad y el release único activo.
- **Errores previsibles:** confundir denominador con población ponderada; omitir el release;
  interpretar `LOCAL SHADOW ONLY` como publicación institucional.
- **Riesgo de interpretación:** citar el resultado como publicado o desplegado oficialmente.
- **Criterio de éxito:** explica los cinco elementos y reconoce que el entorno sigue siendo local,
  sin autorización de publicación ni cutover.

## Registro mínimo por sesión

Por cada tarea se registra: `COMPLETED`, `COMPLETED_WITH_HELP` o `NOT_COMPLETED`; tiempo aproximado;
errores observados; dudas expresadas; severidad del hallazgo y decisión `FIX`, `DEFER` o `REJECT`.
Las notas se anonimizan y no incluyen respuestas de encuesta ni otros datos sensibles.
