# Conciliación temática de indicadores — Corte 2

Fuente de autoridad: lectura del diccionario y agregado en Drive privado, junto con
la hoja arquitectónica y metodología ver6 del paquete rector. No se abrieron microdatos.
Estado: correspondencia temática contrastada y checkpoint de ingeniería aprobado mediante
[PR #57](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/57); decisiones de
calidad/supresión del gate numérico pendientes.

## Selección

| Módulo de navegación | Indicador exacto | Clasificación del diccionario | Numerador | Denominador | Filas observadas |
|---|---|---|---|---|---:|
| 3.1 Mitos sobre el castigo | justifica_castigo_parental | 3.1 Características y percepciones | justifica_castigo_parental == 1 | casos válidos del diseño muestral | 48 |
| 3.1 Mitos sobre el castigo | justifica_castigo_docente | 3.1 Características y percepciones | justifica_castigo_docente == 1 | casos válidos del diseño muestral | 48 |
| 3.5 Acumulación de violencia | PV_hogar_escuela | 3.5 Acumulación de violencias | PV_hogar_escuela == 1 | casos válidos del diseño muestral | 48 |

Son prevalencias ya calculadas en V0; el diccionario declara categoría objetivo 1.
No se suman prevalencias ni se reconstruye la variable compuesta.
La selección es un corte temático, no cobertura exhaustiva de cada módulo.

La hoja arquitectónica y ver6 llaman al módulo 3.1 «Características, percepciones y normas».
Se conserva el título de navegación solicitado en el correo, pero los indicadores activos
deben identificarse explícitamente como justificación del castigo parental/docente.
Los indicadores mito_fuera_casa, mito_locas, mito_pobreza y mito_sitios_oscuros también
pertenecen a 3.1, pero describen creencias sobre violencia sexual; no deben relabelarse
como mitos sobre castigo. AG_VF_09 no se utiliza como sustituto de esos indicadores.

CONS_ATENCION_SALUD pertenece al bloque de consecuencias: se sustituye por
PV_hogar_escuela para la selección de acumulación. El diccionario también contiene
otras intersecciones PV y solapamientos; no se declaran todos implementados.

## Dimensiones y N

Los tres indicadores seleccionados tienen Nacional, Sexo, Área, Área y sexo,
Lengua materna, Discapacidad, Etnicidad, Tipo de hogar y Departamento.
La configuración usa Área × sexo e Idioma del hogar como etiquetas, conservando
la correspondencia con los nombres fuente Área y sexo y Lengua materna.

N del denominador se toma de base_unw, según la aclaración explícita de la usuaria.
En Nacional / Total: parental base_unw=18353 y target_unw=8548; docente
base_unw=18627 y target_unw=1161; PV_hogar_escuela base_unw=18807 y target_unw=3938.
Estos conteos documentan la conciliación; no habilitan nuevas tarjetas en la UI.

## Trazabilidad y gate restante

- Diccionario: diccionario_indicadores.csv; hash de la baseline contrastada:
  F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C.
- Agregado: tabulados_crs04_long.csv; hash de la baseline contrastada:
  15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4.
- Referencias rectoras: CRS04_STAGE04_HOJA_ARQUITECTONICA_APP_VIGILANCIA.md y
  CRS04_Stage04_CORREGIDO_ver6_NUEVA_METODOLOGIA.md, consultadas en Drive.

La conciliación temática queda resuelta técnicamente. Permanece separado el gate de
estados de calidad/supresión: no se asignan flags false ni aprobación por defecto.
La UI conserva sin datos hasta incorporar un contrato completo para las nuevas filas.
Cloud NOT_AUTHORIZED; exportación deshabilitada; golden 3.2 intacto.
