# ENARES 2024 Stage 1 Source Registry

## Registry

| Field | Entry |
|---|---|
| official_microdata_portal | https://proyectos.inei.gob.pe/microdatos/ |
| survey_name | Encuesta Nacional sobre Relaciones Sociales (ENARES) |
| year | 2024 |
| access_date | 2026-05-16 |
| selected_download_format | SPSS |
| selected_package_type | SPSS ZIP |
| download_urls | Official portal: https://proyectos.inei.gob.pe/microdatos/; consultation page: https://proyectos.inei.gob.pe/microdatos/Consulta_por_Encuesta.asp; selected SPSS ZIP module URL pattern: `https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo####.zip`; selected module URLs listed below. |
| module_range | 22 ENARES 2024 modules: `976-Modulo1941` through `976-Modulo1962`. |
| alternative_formats_available | CSV ZIP and Stata ZIP. |
| notes | SPSS ZIP is selected because the extracted `.sav` files preserve variable labels, value labels and coding metadata required for reproducible interpretation. CSV and Stata are available in the INEI portal but are not selected as the primary source format for this pipeline. Any CSV created later must be declared as a derived or intermediate pipeline output generated from `.sav`, not as an official primary source. |

## Selected SPSS ZIP URLs

| Module | Selected SPSS ZIP source URL |
|---|---|
| 976-Modulo1941 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1941.zip |
| 976-Modulo1942 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1942.zip |
| 976-Modulo1943 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1943.zip |
| 976-Modulo1944 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1944.zip |
| 976-Modulo1945 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1945.zip |
| 976-Modulo1946 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1946.zip |
| 976-Modulo1947 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1947.zip |
| 976-Modulo1948 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1948.zip |
| 976-Modulo1949 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1949.zip |
| 976-Modulo1950 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1950.zip |
| 976-Modulo1951 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1951.zip |
| 976-Modulo1952 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1952.zip |
| 976-Modulo1953 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1953.zip |
| 976-Modulo1954 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1954.zip |
| 976-Modulo1955 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1955.zip |
| 976-Modulo1956 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1956.zip |
| 976-Modulo1957 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1957.zip |
| 976-Modulo1958 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1958.zip |
| 976-Modulo1959 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1959.zip |
| 976-Modulo1960 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1960.zip |
| 976-Modulo1961 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1961.zip |
| 976-Modulo1962 | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/SPSS/976-Modulo1962.zip |

## Source validation notes

| Check | Result | Evidence |
|---|---|---|
| Official institution | Source is the INEI Microdatos portal. | `official_microdata_portal` |
| Survey-year match | Survey recorded as ENARES 2024. | INEI Microdatos source selection |
| Selected format | SPSS selected for all 22 modules. | Stage 1 operating rule |
| Selected package | SPSS ZIP selected as the official package. | Stage 1 operating rule |
| Alternative formats | CSV ZIP and Stata ZIP are available but not selected. | Stage 1 source rule |
| Metadata rationale | SPSS `.sav` preserves labels and coding metadata needed for reproducible interpretation. | Stage 1 methodology |
