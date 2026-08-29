# CRS04 STAGE04 — REGISTRO DE VERSIÓN 0

**Proyecto:** ENARES 2024 CRS04
**Estado:** `DRAFT/SHADOW`
**Propietaria:** Ana Silvia Cordero Ricaldi
**Issue relacionado:** [#44](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/44)

## 1. Propósito

Este registro identifica los scripts R, CSV agregados, sintaxis SPSS, diccionario y resultados que constituyen la baseline V0.

Los artefactos reales no se copian a GitHub. Las ubicaciones registradas deben ser recuperables y no deben contener rutas personales, credenciales ni enlaces públicos no autorizados.

## 2. Contrato de la baseline

- V0 continúa siendo la versión oficial.
- V0.5 permanece en shadow.
- Stage 04 no reconstruye indicadores de Stage 03.
- Cada candidato debe conservar `source_sha256`.
- Ningún artefacto se promueve sin paridad, calidad, privacidad y aprobación supervisora.

## 3. Inventario de módulos

| Módulo | Script R V0 | CSV agregado V0 | Ubicación recuperable | Propietario/respaldo | SHA-256 | Estado |
|---|---|---|---|---|---|---|
| 3.1 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| 3.2 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| 3.3 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| 3.4 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| 3.5 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| 3.6 | Pendiente | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |

## 4. Artefactos metodológicos

| Artefacto | Nombre o identificador | Ubicación recuperable | Propietario/respaldo | SHA-256 | Estado |
|---|---|---|---|---|---|
| Diccionario de variables | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| Sintaxis SPSS de referencia | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |
| Contrato Stage 03 | `stage03-v0.5-cloud-full` | `docs/stage03/` | Repositorio oficial | Git commit | Disponible |
| Tabla shadow autorizada | `enares2024_crs04_outputs.reporting_crs04_survey_input_v0_5` | BigQuery autorizado | Supervisión / Ana | Pendiente | Disponible bajo control |
| Resultados de referencia | Pendiente | Pendiente | Ana / pendiente | Pendiente | Bloqueante |

## 5. Método de hash

Los hashes se calculan sin modificar los archivos:

`Get-FileHash -Algorithm SHA256 -LiteralPath <archivo>`

Solo se registra el hash hexadecimal, el nombre lógico del archivo y una ubicación institucional o recuperable. No se registran rutas `C:\Users\...`.

## 6. Condiciones de parada

No se inicia la carga V0 si:

- falta un módulo;
- no existe ubicación recuperable;
- el hash no fue calculado;
- el artefacto no tiene propietario y respaldo;
- el CSV contiene microdatos o identificadores individuales;
- existe discrepancia entre el inventario y el contrato de Stage 03.

## 7. Aprobación del inventario

| Control | Valor |
|---|---|
| Fecha UTC | Pendiente |
| Revisora | `ritaricaldi-cpu` |
| Issue | `#44` |
| Resultado | `NOT_READY` |
| Evidencia o aprobación | Pendiente |

El resultado cambia a `READY_FOR_V0_INVENTORY` únicamente cuando todas las filas bloqueantes estén completas y revisadas.
