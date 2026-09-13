# Manifiesto de sintaxis SPSS contrastada para Stage 04

**Estado:** `HASHED_READ_ONLY_INPUT`
**Fecha de contraste:** `2026-09-13`
**Alcance:** sintaxis CRS04 de los módulos 3.1–3.6; no contiene bases ni microdatos

Los archivos se recibieron como insumos externos de solo lectura. No se incorporan al
repositorio y no se registran rutas locales. Este manifiesto permite identificar exactamente la
evidencia usada para conciliar el gate numérico sin confundirla con los agregados V0 oficiales.

| Módulo | Archivo lógico | Bytes | Líneas | SHA-256 |
|---|---|---:|---:|---|
| 3.1 | `07_CRS04_3.1_Caracteristicas_violencia_Percepciones_ver6.sps` | 85420 | 2414 | `324247276F3478B76823E0C9BBF92987334E4A470CD23B46A6093301D4A07473` |
| 3.2 | `08_CRS04_3.2 Violencia en el hogar_ver6.sps` | 113379 | 2893 | `41B6EF03F8C39887D1E1B368A86455CB76B352C69289F843E283AE901AA71420` |
| 3.2 | `08b_CRS04_3.2.6_desagregados.sps` | 23273 | 380 | `FFDE8F8DDEBB36FA8EA0DC5AC650CEC8607D9F6EE9384EE22D8487912EBD5165` |
| 3.3 | `09_CRS04_3.3 Violencia en el entorno escolar_ver4.sps` | 112787 | 2895 | `8C20905424E8A21D6F61BFE89AF1AA6F9D31E3BE741C25E0ED88C771FBD8561E` |
| 3.3 | `09b_CRS04_3.3_8_desagregados.sps` | 22763 | 374 | `1C64AFF41A15DF8CDAFF021159649E796F9549FB5A6A1E3E165382868DF8C488` |
| 3.3 | `09c_CRS04_3.3_8_desagregados.sps` | 21698 | 351 | `B74D1BEE4B204C7B5FB4706AE95BA242457E9904947FF6F2E20F5FBFB7C4B305` |
| 3.4 | `10_CRS04_3.4 Violencia sexual en adolescentes de 12 a 17 años_ver4.sps` | 79191 | 1968 | `14468032D9A9FBC4E6D12AA6E7303542DDAC093A9A72377E4FF2FA65C2274009` |
| 3.4 | `10b_CRS04_3.4_5_desagregados.sps` | 20259 | 330 | `8B772D36320C3BBC707F5F60FCDFA22EB6D0F88F1CAEACF26818BA54631C5D99` |
| 3.5 | `11_CRS04_3.5 Acumulación de violencias_ver4.sps` | 35017 | 965 | `CBB03211806E14BED95885F2DF86A0635BE364D9335DE476CF77AC1218C9E593` |
| 3.6 | `12_CRS03_CRS04_3.6_BusquedaAyuda_Hogar_Escuela_ver5.sps` | 73100 | 2442 | `D979283C1861F4F6D78EE539113A4FB9E00BC9663E41F71EFF683AAD1A8C8688` |
| 3.6 | `13_CRS04_3.6_BusquedaAyuda_VS_ver4.sps` | 32393 | 1128 | `C84A96B75BDEC8403B50C4D71200E8D447BAFB22719D942BC3CCE02A74A8DD0D` |

Las sintaxis exclusivas de CRS03 y la ficha de riesgo 9–11 no forman parte de la autoridad para
habilitar cifras CRS04. El archivo 12 se incluye porque declara expresamente alcance compartido
CRS03/CRS04 y contiene el bloque CRS04 de búsqueda de ayuda.

No se copiaron rutas `FILE HANDLE`, credenciales, datos, resultados individuales ni archivos
`.sav`. La evidencia derivada se limita a reglas, nombres de variables, universos, comandos de
diseño complejo y referencias de línea verificables en estos archivos identificados por hash.
