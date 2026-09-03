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

## 3. Inventario V0 recuperado para revisión

El productor R y el CSV V0 son integrados y cubren transversalmente los módulos 3.1–3.6. La
ubicación se expresa como ruta lógica dentro de Drive privado; no se registran enlaces públicos,
identificadores de Drive ni rutas personales.

Metadatos y hashes de los objetos recuperables fueron contrastados el
`2026-09-03T00:31:07Z`. La responsable registrada es Ana Silvia Cordero Ricaldi y el respaldo
verificable es el historial de Drive. Esto deja el paquete listo para
**revisión independiente**, no aprobado.

### 3.1 Objetos V0 oficiales en Drive privado

| Cobertura/rol | Nombre lógico | Nombre real en Drive | Ubicación recuperable | Tamaño o filas | SHA-256 calculado sobre el objeto en Drive | Responsable/respaldo | Estado |
|---|---|---|---|---|---|---|---|
| 3.1–3.6 / productor R | `tabulados_crs04_v0.R` | `tabulados.R` | `ENARES_2024_PROJECT/03Scripts_R` | 19,864 bytes | `A45A73F40D728713A52800653991EBDBFF4E80A0D9A6A8318E8D7BD266597C1D` | Ana / historial de Drive | `PENDING_INDEPENDENT_REVIEW` |
| 3.1–3.6 / output agregado | `tabulados_crs04_long_v0.csv` | `tabulados_crs04_long.csv` | `ENARES_2024_PROJECT/04Outputs` | 576,919 bytes; 3,014 filas | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` | Ana / historial de Drive | `PENDING_INDEPENDENT_REVIEW` |
| 3.1–3.6 / diseño survey | `design_crs04.rds` | `design_crs04.rds` | `ENARES_2024_PROJECT/04Outputs` | 6,166,714 bytes; 25 estratos, 1,115 PSU y 1,090 gl | `C9C7D96F053BE17606C9BDCED365ECC5E0016FF0294958E378CC62C747F46965` | Ana / historial de Drive | `PENDING_INDEPENDENT_REVIEW` |
| 3.1–3.6 / diccionario | `diccionario_indicadores.csv` | `diccionario_indicadores.csv` | `ENARES_2024_PROJECT/04Outputs` | 354,668 bytes; 516 indicadores | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | Ana / historial de Drive | `PENDING_INDEPENDENT_REVIEW` |

Los objetos de Drive privado son la fuente autoritativa de este inventario. Los nombres con
sufijos de descarga y los hashes de copias locales anteriores no se usan para identificar ni
aprobar la baseline V0.

### 3.2 Conciliación de hashes y linaje

La conciliación se hizo sobre los bytes de cada objeto en Drive, no sobre copias locales. La
evidencia mínima reproducible, incluidas las fechas de modificación y la salida normalizada del
cálculo, está en [`docs/stage04/v0_drive_hash_manifest.md`](docs/stage04/v0_drive_hash_manifest.md).
Ningún cambio de hash se sustituyó silenciosamente.

| Artefacto | Versión | Nombre lógico | Nombre real en Drive | Ubicación lógica privada | Tamaño o filas | Hash registrado anteriormente | Hash observado actualmente en Drive | Motivo de la diferencia | Objeto declarado autoritativo | Evidencia | Estado | Responsable | Decisión de la revisora |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Productor R | V0 oficial | `tabulados_crs04_v0.R` | `tabulados.R` | `ENARES_2024_PROJECT/03Scripts_R` | 19,864 bytes | `259E75A52E9A8299F5C79A55583C2E964D323E30BEAA39E175EE0E552EC5F5CC` | `A45A73F40D728713A52800653991EBDBFF4E80A0D9A6A8318E8D7BD266597C1D` | El mismo objeto fue actualizado en Drive: el historial registra 68 revisiones y revisiones del 12–13 de agosto de 10,879 bytes; la revisión vigente del 20 de agosto tiene 19,864 bytes. | Revisión vigente del objeto raíz `03Scripts_R/tabulados.R` | Historial de Drive, tamaño, fecha, hash y enlace productor–salida del manifiesto | `EXPLAINED_VERSION_DIFFERENCE` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Output agregado | V0 oficial | `tabulados_crs04_long_v0.csv` | `tabulados_crs04_long.csv` | `ENARES_2024_PROJECT/04Outputs` | 576,919 bytes; 3,014 filas | 3,274 filas; `919C3F39C7681E71596CBC904369FBE6CD0B85D02FC9DC4D0AF36DF7845EC8FC` | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` | El nombre fue versionado en el mismo objeto de Drive (82 revisiones). El registro de 3,274 filas corresponde a una revisión/copia anterior; el objeto raíz vigente tiene 3,014 filas. No es V0.5: está en otra carpeta, tiene tamaño y hash distintos y su productor R apunta explícitamente a la carpeta shadow. | Revisión vigente del objeto raíz `04Outputs/tabulados_crs04_long.csv` | Historial de Drive; conteo sobre bytes actuales; hashes, tamaños, carpetas y enlaces productor–salida de ambas versiones | `EXPLAINED_VERSION_DIFFERENCE` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Diseño survey | V0 oficial | `design_crs04.rds` | `design_crs04.rds` | `ENARES_2024_PROJECT/04Outputs` | 6,166,714 bytes | `D65CEA98CCF595E1D2E88287FEDB523CD60B606FD2982AA25CFFF156BC7AF5A6` | `C9C7D96F053BE17606C9BDCED365ECC5E0016FF0294958E378CC62C747F46965` | El objeto V0 fue actualizado en Drive; su historial registra 58 revisiones y cambios de tamaño. | Revisión vigente del objeto raíz `04Outputs/design_crs04.rds` | Historial de Drive, tamaño, fecha y hash del manifiesto | `EXPLAINED_VERSION_DIFFERENCE` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Diccionario | V0 oficial | `diccionario_indicadores.csv` | `diccionario_indicadores.csv` | `ENARES_2024_PROJECT/04Outputs` | 354,668 bytes; 516 filas | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` | Sin diferencia. | Objeto raíz `04Outputs/diccionario_indicadores.csv` | Tamaño, fecha y hash del manifiesto | `MATCH` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Productor R | V0.5 shadow | `tabulados_crs04_v0_5.R` | `tabulados.R` | `ENARES_2024_PROJECT/03Scripts_R/shadow_full_v0_5` | 19,915 bytes | `B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6` | `B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6` | Sin diferencia. | Objeto `shadow_full_v0_5/tabulados.R` | Carpeta, tamaño, fecha, hash y enlace productor–salida del manifiesto | `MATCH` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Especificaciones | V0.5 shadow | `stage3_r_tabulation_specs.csv` | `stage3_r_tabulation_specs.csv` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 153,012 bytes; 516 filas | `AF312A53F19718B00E3307E02FC6C91B8720B7EEAC4139493529AAF81F368082` | `FE97A84167C356816C7E30C302F0138DA5468B9E05F1EF6AB24D58AAF556E076` | El objeto se amplió durante el armado shadow: el historial registra cuatro revisiones de 122,229, 128,337, 135,667 y 153,012 bytes; la última es la vigente. | Revisión final del objeto shadow `stage3_r_tabulation_specs.csv` | Historial de Drive, tamaño, fecha y hash del manifiesto | `EXPLAINED_VERSION_DIFFERENCE` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Output agregado | V0.5 shadow | `tabulados_crs04_long_v0_5.csv` | `tabulados_crs04_long.csv` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 576,797 bytes; 3,014 filas | `0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760` | `0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760` | Sin diferencia. Igual número de filas que V0 no implica igualdad: el tamaño y SHA-256 difieren. | Objeto shadow `04Outputs/shadow_full_v0_5/tabulados_crs04_long.csv` | Carpeta, tamaño, conteo y hash del manifiesto | `MATCH` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |
| Diseño survey | V0.5 shadow | `design_crs04.rds` | `design_crs04.rds` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 6,155,185 bytes | `D65CEA98CCF595E1D2E88287FEDB523CD60B606FD2982AA25CFFF156BC7AF5A6` | `26748A206E64020A2504969BD9A5C758CAF18D71B40E62A38575274755C54B11` | El hash anterior reutilizaba el registro de otro objeto V0. Drive contiene un objeto shadow separado, con una sola revisión, otro tamaño y otro hash. | Objeto separado `04Outputs/shadow_full_v0_5/design_crs04.rds` | Carpeta, revisión única, tamaño, fecha y hash del manifiesto | `WRONG_OBJECT_REPLACED` | Ana Silvia Cordero Ricaldi | `PENDIENTE — ritaricaldi-cpu` |

No quedan filas `UNRESOLVED` en la conciliación documental. Esto no constituye aprobación: la
revisora debe contrastar los objetos autoritativos y decidir cada fila. La V0 oficial es el
conjunto vigente en las carpetas raíz indicadas; V0.5 es un conjunto separado bajo
`shadow_full_v0_5` y no sustituye ni publica V0.

### 3.3 Sintaxis SPSS de contraste por módulos 3.1–3.6

Ubicación recuperable para todas las filas:
`ENARES_2024_PROJECT/02Codigos/CodigoSpss`. Responsable y respaldo: Ana / historial de Drive.
Estos archivos son sintaxis de referencia; no son microdatos y no se copian al repositorio.

| Módulo | Nombre lógico | Nombre real en Drive | Tamaño | SHA-256 |
|---|---|---|---:|---|
| 3.1 | `crs04_3_1_caracteristicas_percepciones.sps` | `07_CRS04_3.1_Caracteristicas_violencia_Percepciones_ver6.sps` | 85,420 bytes | `324247276F3478B76823E0C9BBF92987334E4A470CD23B46A6093301D4A07473` |
| 3.2 | `crs04_3_2_violencia_hogar.sps` | `08_CRS04_3.2 Violencia en el hogar_ver6.sps` | 113,379 bytes | `41B6EF03F8C39887D1E1B368A86455CB76B352C69289F843E283AE901AA71420` |
| 3.2 | `crs04_3_2_desagregados.sps` | `08b_CRS04_3.2.6_desagregados.sps` | 23,273 bytes | `FFDE8F8DDEBB36FA8EA0DC5AC650CEC8607D9F6EE9384EE22D8487912EBD5165` |
| 3.3 | `crs04_3_3_violencia_entorno_escolar.sps` | `09_CRS04_3.3 Violencia en el entorno escolar_ver4.sps` | 112,787 bytes | `8C20905424E8A21D6F61BFE89AF1AA6F9D31E3BE741C25E0ED88C771FBD8561E` |
| 3.3 | `crs04_3_3_desagregados_b.sps` | `09b_CRS04_3.3_8_desagregados.sps` | 22,763 bytes | `1C64AFF41A15DF8CDAFF021159649E796F9549FB5A6A1E3E165382868DF8C488` |
| 3.3 | `crs04_3_3_desagregados_c.sps` | `09c_CRS04_3.3_8_desagregados.sps` | 21,698 bytes | `B74D1BEE4B204C7B5FB4706AE95BA242457E9904947FF6F2E20F5FBFB7C4B305` |
| 3.4 | `crs04_3_4_violencia_sexual_12_17.sps` | `10_CRS04_3.4 Violencia sexual en adolescentes de 12 a 17 años_ver4.sps` | 79,191 bytes | `14468032D9A9FBC4E6D12AA6E7303542DDAC093A9A72377E4FF2FA65C2274009` |
| 3.4 | `crs04_3_4_desagregados.sps` | `10b_CRS04_3.4_5_desagregados.sps` | 20,259 bytes | `8B772D36320C3BBC707F5F60FCDFA22EB6D0F88F1CAEACF26818BA54631C5D99` |
| 3.5 | `crs04_3_5_acumulacion_violencias.sps` | `11_CRS04_3.5 Acumulación de violencias_ver4.sps` | 35,017 bytes | `CBB03211806E14BED95885F2DF86A0635BE364D9335DE476CF77AC1218C9E593` |
| 3.6 | `crs04_3_6_busqueda_ayuda_hogar_escuela.sps` | `12_CRS03_CRS04_3.6_BusquedaAyuda_Hogar_Escuela_ver5.sps` | 73,100 bytes | `D979283C1861F4F6D78EE539113A4FB9E00BC9663E41F71EFF683AAD1A8C8688` |
| 3.6 | `crs04_3_6_busqueda_ayuda_vs.sps` | `13_CRS04_3.6_BusquedaAyuda_VS_ver4.sps` | 32,393 bytes | `C84A96B75BDEC8403B50C4D71200E8D447BAFB22719D942BC3CCE02A74A8DD0D` |

## 4. Handoff V0.5 aceptado para shadow

V0.5 se registra separadamente y no reemplaza la V0 oficial.

| Rol | Nombre real en Drive | Nombre lógico | Evidencia de Drive | SHA-256 | Estado |
|---|---|---|---|---|---|
| Productor R | `tabulados.R` | `tabulados_crs04_v0_5.R` | 19,915 bytes | `B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6` | `ACCEPTED_SHADOW` |
| Especificaciones | `stage3_r_tabulation_specs.csv` | Mismo nombre | 153,012 bytes; 516 indicadores | `FE97A84167C356816C7E30C302F0138DA5468B9E05F1EF6AB24D58AAF556E076` | `ACCEPTED_SHADOW` |
| Output agregado | `tabulados_crs04_long.csv` | `tabulados_crs04_long_v0_5.csv` | 576,797 bytes; 3,014 filas | `0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760` | `ACCEPTED_SHADOW` |
| Diseño survey | `design_crs04.rds` | Mismo nombre | 6,155,185 bytes; 25 estratos, 1,115 PSU y 1,090 gl | `26748A206E64020A2504969BD9A5C758CAF18D71B40E62A38575274755C54B11` | `ACCEPTED_SHADOW` |
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
| Fecha UTC de actualización | 2026-09-03T00:31:07Z |
| Revisora | `ritaricaldi-cpu` |
| Issue | `#44` |
| Resultado | `READY_FOR_V0_INVENTORY_REVIEW` |
| Evidencia disponible | Nombres lógicos y reales, ubicación privada recuperable, tamaños/filas, hashes, responsable/respaldo y cobertura 3.1–3.6 registrados |
| Conciliación documental | Cero filas `UNRESOLVED`; diferencias explicadas y objetos autoritativos identificados |
| Contraste pendiente | Verificación y decisión independiente de la conciliación y de los objetos autoritativos de Drive |
| Aprobación | Pendiente; este documento no declara `READY_FOR_V0_INVENTORY` |

El resultado cambia a `READY_FOR_V0_INVENTORY` únicamente cuando todas las filas bloqueantes estén completas y revisadas.
