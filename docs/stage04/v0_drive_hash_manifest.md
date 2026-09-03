# Manifiesto privado de evidencia de hashes V0 y V0.5

**Fecha UTC de contraste:** `2026-09-03T00:31:07Z`
**Fuente autoritativa:** objetos y revisiones de Drive privado
**Estado:** `PENDING_INDEPENDENT_REVIEW`
**Responsable:** Ana Silvia Cordero Ricaldi
**Revisora:** `ritaricaldi-cpu` — decisión pendiente

Este manifiesto contiene solo metadatos y hashes. No contiene archivos `.sav`, microdatos,
credenciales, identificadores de Drive, enlaces públicos, rutas personales ni registros de NNA.
Los bytes se leyeron directamente de Drive en modo de solo lectura y se calcularon con SHA-256
sin modificar los objetos.

## Objetos contrastados

| Versión declarada | Nombre lógico | Nombre real | Carpeta lógica privada | Tamaño / filas | Modificación UTC | SHA-256 |
|---|---|---|---|---|---|---|
| V0 oficial | `tabulados_crs04_v0.R` | `tabulados.R` | `ENARES_2024_PROJECT/03Scripts_R` | 19,864 bytes | `2026-08-20T19:20:35.064Z` | `A45A73F40D728713A52800653991EBDBFF4E80A0D9A6A8318E8D7BD266597C1D` |
| V0 oficial | `tabulados_crs04_long_v0.csv` | `tabulados_crs04_long.csv` | `ENARES_2024_PROJECT/04Outputs` | 576,919 bytes; 3,014 filas de datos | `2026-08-20T20:04:04.089Z` | `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4` |
| V0 oficial | `design_crs04.rds` | `design_crs04.rds` | `ENARES_2024_PROJECT/04Outputs` | 6,166,714 bytes | `2026-08-20T19:22:04.749Z` | `C9C7D96F053BE17606C9BDCED365ECC5E0016FF0294958E378CC62C747F46965` |
| V0 oficial | `diccionario_indicadores.csv` | `diccionario_indicadores.csv` | `ENARES_2024_PROJECT/04Outputs` | 354,668 bytes; 516 filas | `2026-08-20T19:20:30.171Z` | `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C` |
| V0.5 shadow | `tabulados_crs04_v0_5.R` | `tabulados.R` | `ENARES_2024_PROJECT/03Scripts_R/shadow_full_v0_5` | 19,915 bytes | `2026-08-23T23:34:37.094Z` | `B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6` |
| V0.5 shadow | `stage3_r_tabulation_specs.csv` | `stage3_r_tabulation_specs.csv` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 153,012 bytes; 516 filas | `2026-08-24T00:27:41.857Z` | `FE97A84167C356816C7E30C302F0138DA5468B9E05F1EF6AB24D58AAF556E076` |
| V0.5 shadow | `tabulados_crs04_long_v0_5.csv` | `tabulados_crs04_long.csv` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 576,797 bytes; 3,014 filas de datos | `2026-08-24T00:44:17.512Z` | `0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760` |
| V0.5 shadow | `design_crs04.rds` | `design_crs04.rds` | `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` | 6,155,185 bytes | `2026-08-23T23:36:52.788Z` | `26748A206E64020A2504969BD9A5C758CAF18D71B40E62A38575274755C54B11` |

## Salida normalizada del cálculo SHA-256

La salida siguiente es equivalente a `Get-FileHash -Algorithm SHA256`; las rutas se normalizaron
a la ubicación lógica privada para no revelar rutas personales ni identificadores internos.

```text
SHA256 A45A73F40D728713A52800653991EBDBFF4E80A0D9A6A8318E8D7BD266597C1D ENARES_2024_PROJECT/03Scripts_R/tabulados.R
SHA256 15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4 ENARES_2024_PROJECT/04Outputs/tabulados_crs04_long.csv
SHA256 C9C7D96F053BE17606C9BDCED365ECC5E0016FF0294958E378CC62C747F46965 ENARES_2024_PROJECT/04Outputs/design_crs04.rds
SHA256 F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C ENARES_2024_PROJECT/04Outputs/diccionario_indicadores.csv
SHA256 B41233026096CCB9F6457604A9BEDFEB21743874E2902046AC94099A5A870AC6 ENARES_2024_PROJECT/03Scripts_R/shadow_full_v0_5/tabulados.R
SHA256 FE97A84167C356816C7E30C302F0138DA5468B9E05F1EF6AB24D58AAF556E076 ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5/stage3_r_tabulation_specs.csv
SHA256 0977FA7D2C68BE7B1A1E37DF8D5A131D8551A1251D61D2CC28DC2D932BAEF760 ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5/tabulados_crs04_long.csv
SHA256 26748A206E64020A2504969BD9A5C758CAF18D71B40E62A38575274755C54B11 ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5/design_crs04.rds
```

## Evidencia productor–salida y separación de versiones

- El productor V0 lee el diseño y las especificaciones desde la raíz lógica
  `ENARES_2024_PROJECT/04Outputs` y escribe `tabulados_crs04_long.csv` en esa misma raíz.
- El productor V0.5 lee diseño y especificaciones desde
  `ENARES_2024_PROJECT/04Outputs/shadow_full_v0_5` y escribe su CSV en esa carpeta shadow.
- Los dos CSV vigentes tienen 3,014 filas, pero no son iguales: sus tamaños son 576,919 y
  576,797 bytes y sus SHA-256 son distintos. La ubicación y el productor también son distintos.
- El historial del CSV V0 raíz contiene 82 revisiones. El registro previo de 3,274 filas y hash
  `919C3F39C7681E71596CBC904369FBE6CD0B85D02FC9DC4D0AF36DF7845EC8FC` corresponde a una
  revisión o copia anterior, no al objeto V0.5 shadow.
- El diseño V0 raíz y el diseño V0.5 shadow son objetos distintos: difieren en carpeta, tamaño,
  historial y SHA-256. El diseño shadow tiene una sola revisión registrada.

La cobertura funcional declarada de los productores integrados y sus salidas es 3.1–3.6. La
aceptación de esta evidencia y el cambio a `READY_FOR_V0_INVENTORY` requieren aprobación explícita
de `ritaricaldi-cpu`.
