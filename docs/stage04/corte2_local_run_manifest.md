# Manifiesto de ejecución local — Corte 2

- Run ID: `sprint042-corte2-local-coverage-001`
- Fecha UTC: `2026-09-10`
- Rama: `feat/stage04-sprint042-local-module-coverage`
- Base de rama: `10692b160bcc8a0998c2b4ea622c74c066b5a952`
- Alcance: `LOCAL_SHADOW_ONLY`
- Estado cloud: `NOT_AUTHORIZED`
- Presupuesto: `USD 0`
- Exportación: deshabilitada
- Publicación/cutover: no autorizados

## Fuentes contrastadas

| Artefacto lógico | SHA-256 aprobado | Uso en este run |
|---|---|---|
| tabulados_crs04_long.csv | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` | Conciliación agregada 3.1–3.6 |
| diccionario_indicadores.csv | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | Módulo, indicador, universo, denominador y tipo |

No se copiaron a Git los archivos fuente completos, IDs internos de Drive, rutas privadas ni
microdatos. La conciliación registra metadatos y conteos agregados verificables.

## Decisión fail-closed

El run prueba navegación, configuración, validación y ausencia de fabricación de cifras.
Solo el golden previamente aprobado de 3.2 conserva `AUTHORIZED_GOLDEN`. Las combinaciones
nuevas permanecen `PENDING_QUALITY_SUPPRESSION` y no producen tarjetas numéricas hasta que
exista aprobación independiente de su estado de calidad/supresión.

Este identificador pertenece a evidencia técnica local. No crea ni modifica
`ops.current_release`, un release institucional o una ejecución cloud.
