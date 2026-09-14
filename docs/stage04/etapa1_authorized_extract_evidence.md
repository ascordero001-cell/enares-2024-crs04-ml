# Evidencia del extracto autorizado de la Etapa 1

Fecha UTC: 2026-09-14

## Procedencia y alcance

- Fuente aprobada: `tabulados_crs04_long.csv`.
- SHA-256 de la fuente: `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`.
- Extracto: `app/data/v0_authorized_etapa1_indicator_estimates.csv`.
- SHA-256 del extracto: `208bc654029e40ce5271519939258b59d69bd3dfd0c1c5b537d8ec4cebeb7332`.
- Filas: 35, distribuidas en D01 (10), D09 (22) y D11 (3).
- D12 no agrega filas: aplica los alias aprobados `Área × sexo` e `Idioma del hogar`.
- Quedan fuera de este corte las tres series «nadie», D06 y D07.

El archivo padre se verificó contra el manifiesto V0 aprobado antes de construir el
extracto. El manifiesto del extracto conserva el SHA-256 del padre y el SHA-256
propio; `AuthorizedAggregateRepository` valida ambos antes de habilitar la lectura.

## Controles reproducidos

- La rederivación desde el agregado padre produce el mismo CSV byte por byte.
- Los 22 pares de D09 coinciden exactamente con el alcance aprobado.
- Trece celdas de D09 superan CV de 15 % y permanecen visibles como referenciales.
- Ninguna fila se suprime por CV alto o N no ponderado bajo.
- No se modificó el golden autorizado de 3.2.
- El extracto contiene únicamente estadísticas agregadas; no contiene microdatos,
  identificadores individuales, rutas personales, enlaces de Drive ni credenciales.

## Estado operativo

- Alcance: `LOCAL_SHADOW_ONLY`.
- Cloud: `NOT_AUTHORIZED`.
- Publicación institucional, exportación y cutover: no autorizados.

## Verificación de conexión local — 2026-09-14 UTC

- D01 se presenta en dos tablas estáticas: ítems 1–7 sobre ejecución de tareas e
  ítems 8–10 sobre acompañamiento. No aparece control de descarga en estas tablas.
- D09 muestra el dominio `CONS_ALGUNA = 1` junto a la cifra. Se comprobó una celda
  con CV 20,70 % visible como «Referencial — precisión limitada», sin supresión.
- D12 muestra `Idioma del hogar` y la categoría codificada `3` como
  `Quechua/Aymara`; los nombres fuente permanecen en la trazabilidad, no en la interfaz.
- D11 se presenta uno por uno. `C3P213` muestra el texto aprobado «No recibió ayuda
  porque no supieron cómo ayudarle» y su dominio `dom_no_recibio_hogar = 1`.
- El control principal de exportación permanece deshabilitado y no se habilitó ningún
  repositorio cloud.
