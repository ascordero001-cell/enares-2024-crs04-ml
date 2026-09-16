# PR B — conexión integral V0 local shadow

- **Estado técnico automatizado:** `3014/3014 PASS`
- **Estado manual:** `PENDING_6_MODULE_TRAVERSALS`
- **Alcance:** `LOCAL_SHADOW_ONLY`
- **Cloud, publicación y cutover:** `NOT_EXECUTED / NOT_AUTHORIZED`

## Procedencia y artefactos

La construcción lee directamente de Drive privado el padre agregado V0 oficial y el diccionario
aprobado. No utiliza microdatos, archivos SAV, credenciales, identificadores internos de Drive,
enlaces públicos ni rutas personales.

| Artefacto | Filas | SHA-256 |
|---|---:|---|
| Padre `tabulados_crs04_long.csv` | 3014 | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` |
| `diccionario_indicadores.csv` | 516 | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` |

El extracto integral conserva las cifras del padre, usa `base_unw` como `n_unweighted` y deriva
`synthetic=false` exclusivamente después de que `AuthorizedAggregateRepository` valida archivo,
manifiesto, SHA del padre y registro V0 aprobado. El ledger contiene solo claves agregadas y un
SHA-256 por fila; permite contrastar las 3014 filas sin versionar otra copia del padre.

## Tratamientos cerrados

- 2995 filas A: tarjeta/exportación agregada según contrato, con alertas visibles de CV y N.
- 4 filas C: contexto visible, sin tarjeta, tabla numérica ni exportación; no se imputan SE, IC o CV.
- 7 filas D: distribución `num_consecuencias_fisicas`; `Total` no se presenta como prevalencia.
- 8 filas E: se elimina el texto manual `[referencial]`; la interfaz lo deriva de `cv_flag`.

## Recorrido manual representativo pendiente

Ana ejecutará un recorrido real por módulo. No hay umbral de 90 segundos.

| Módulo | Inicio UTC | Fin UTC | Segundos | Indicador/dimensión/categoría | Resultado | Observaciones |
|---|---|---|---:|---|---|---|
| 3.1 | 2026-09-16T22:42:25Z | 2026-09-16T23:51:21Z | 4136 | `AG_VF_09` / Nacional / Total | PASS | Tarjeta completa, IC, CV y `N=base_unw` visibles; ventana conservadora desde el arranque de la app, incluye tiempo inactivo porque el inicio manual exacto no fue capturado. |
| 3.2 | 2026-09-16T23:51:48Z | 2026-09-16T23:52:54Z | 67 | `VF_HOGAR` / Nacional / Total | PASS | Tarjeta completa: estimación 16.74 %, EE 0.5115, CV 0.03055, `N=base_unw` 18,807 e IC95 % 15.74 %–17.75 %; sin alerta ni error visible. |
| 3.3 | 2026-09-16T23:53:13Z | 2026-09-16T23:54:15Z | 62 | `C3P223_10_1` / Nacional / Total | PASS | Tarjeta completa: estimación 11.49 %, EE 0.6444, CV 0.05607, `N=base_unw` 7,522 e IC95 % 10.29 %–12.82 %; sin alerta ni error visible. |
| 3.4 | PENDIENTE | PENDIENTE | — | PENDIENTE | PENDIENTE | — |
| 3.5 | PENDIENTE | PENDIENTE | — | PENDIENTE | PENDIENTE | — |
| 3.6 | PENDIENTE | PENDIENTE | — | PENDIENTE | PENDIENTE | — |

PR B no se declara cerrado hasta completar esta tabla. Ningún resultado de este PR habilita una
carga cloud, publicación institucional, cutover ni sustitución de V0.
