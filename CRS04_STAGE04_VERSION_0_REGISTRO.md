# CRS04 STAGE04 — REGISTRO DE VERSIÓN 0

**Proyecto:** ENARES 2024 CRS04
**Estado:** `READY_FOR_V0_INVENTORY_REVIEW`
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

## 3. Inventario V0 recuperado

El productor R y el CSV V0 son integrados y cubren transversalmente los módulos 3.1–3.6.

| Módulos | Productor R V0 | Output CSV V0 | Ubicación recuperable | Propietaria/respaldo | Estado |
|---|---|---|---|---|---|
| 3.1–3.6 | `tabulados_crs04_v0.R` | `tabulados_crs04_long_v0.csv` | Drive privado — `ENARES_2024_PROJECT/04Outputs` | Ana / historial de Drive y copia local verificada | `RECOVERED_REFERENCE` |

### Hashes V0

| Artefacto recuperado | Nombre lógico | Evidencia | SHA-256 |
|---|---|---|---|
| `tabulados (4).R` | `tabulados_crs04_v0.R` | Script integrado; 10,879 bytes | `259E75A52E9A8299F5C79A55583C2E964D323E30BEAA39E175EE0E552EC5F5CC` |
| `tabulados_crs04_long (5).csv` | `tabulados_crs04_long_v0.csv` | 3,274 filas; copia `(4)` idéntica | `919C3F39C7681E71596CBC904369FBE6CD0B85D02FC9DC4D0AF36DF7845EC8FC` |
| `design_crs04.rds` | `design_crs04.rds` | Diseño survey recuperado | `D65CEA98CCF595E1D2E88287FEDB523CD60B606FD2982AA25CFFF156BC7AF5A6` |
| `diccionario_indicadores (1).csv` | `diccionario_indicadores.csv` | 516 indicadores | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` |

## 4. Handoff V0.5 aceptado para shadow

V0.5 se registra separadamente y no reemplaza la V0 oficial.

| Rol | Archivo recuperado | Nombre lógico | Evidencia | SHA-256 | Estado |
|---|---|---|---|---|---|
| Productor R | `tabulados (5).R` | `tabulados_crs04_v0_5.R` | Productor del output aceptado | `B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6` | `ACCEPTED_SHADOW` |
| Especificaciones | `stage3_r_tabulation_specs.csv` | Mismo nombre | 516 indicadores | `AF312A53F19718B00E3307E02FC6C91B8720B7EEAC4139493529AAF81F368082` | `ACCEPTED_SHADOW` |
| Output agregado | `tabulados_crs04_long (7).csv` | `tabulados_crs04_long_v0_5.csv` | 3,014 filas | `0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760` | `ACCEPTED_SHADOW` |
| Diseño survey | `design_crs04.rds` | Mismo nombre | 25 estratos, 1,115 PSU y 1,090 gl | `D65CEA98CCF595E1D2E88287FEDB523CD60B606FD2982AA25CFFF156BC7AF5A6` | `ACCEPTED_SHADOW` |
| Tabla Stage 03 | `reporting_crs04_survey_input_v0_5` | BigQuery autorizado | 18,807 filas y 737 columnas | Contrato Stage 03 | `ACCEPTED_SHADOW` |

Ubicación recuperable: Drive privado —
`ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5`.

### Inputs restringidos

| Input | SHA-256 | Estado |
|---|---|---|
| `19_CRS04_CAP100.sav` | `0296F855F1795BF855E7ADC80FA3A2560F4FAEA3C153516050D59C7B19EBD7B8` | `RESTRICTED_AVAILABLE` |
| `20_CRS04_CAP200.sav` | `A6D22F0C4FA5DC0659107BF9CE13C689B16FC77274E168B07D6C74CAB329CE11` | `RESTRICTED_AVAILABLE` |
| `21_CRS04_CAP248.sav` | `9230FB4A7A8DE9B537E9300EAF535B5BCF4A49463E271ED01CE536C1DF823D6E` | `RESTRICTED_AVAILABLE` |
| `22_CRS04_CAP300.sav` | `BF03CDB816F0E6649B75A9524D87BA3FF33C5445F1E5A8327A4E93A2E5D9E4E3` | `RESTRICTED_AVAILABLE` |

Los inputs restringidos no se copian a GitHub ni se usan como fixtures.

### Diccionario y evidencia

| Artefacto | SHA-256 o evidencia | Estado |
|---|---|---|
| `Diccionario de variables 19_CRS.04_CAP100.pdf` | `6A0799B126CB140C372FD824CC57288B40FAAD6F4191BE5CCE6334EE346D014B` | `AVAILABLE` |
| `diccionario_indicadores.csv` | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | `AVAILABLE` |
| Release `stage03-v0.5-cloud-full` | PR #41, CI y contrato Stage 03 | `ACCEPTED_SHADOW` |

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
| Fecha UTC | 2026-08-29 |
| Revisora | `ritaricaldi-cpu` |
| Issue | `#44` |
| Resultado | `READY_FOR_V0_INVENTORY_REVIEW` |
| Evidencia o aprobación | Hashes, ubicaciones, inputs y outputs registrados; aprobación independiente pendiente |

El resultado cambia a `READY_FOR_V0_INVENTORY` únicamente cuando todas las filas bloqueantes estén completas y revisadas.
