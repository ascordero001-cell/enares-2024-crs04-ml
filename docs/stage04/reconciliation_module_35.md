# Conciliación completa 3.5 — diccionario y agregado de Drive

Alcance: conciliación documental del catálogo completo; no implica autorización de publicación ni carga de cifras nuevas en la UI.
Fuente: diccionario_indicadores.csv y tabulados_crs04_long.csv leídos directamente de Drive privado.
N del denominador: base_unw. target_unw no se sustituye por N. Periodo: ENARES 2024.
Universo marco CRS04; el dominio y la regla del denominador indicados abajo restringen cada indicador.
Escala de la salida pct/es/IC: 0–100 (porcentaje/puntos porcentuales); CV se conserva como razón.
No se recalcularon estimaciones, no se completaron CV vacíos y no se inventaron flags.

Resultado global: 21 indicadores del diccionario, todos con salida; 457 filas agregadas.

| Indicador / etiqueta exacta | Módulo del diccionario | Numerador | Denominador | Dominio | Tipo del diccionario / salida | Dimensiones observadas | Filas | Resultado |
|---|---|---|---|---|---|---|---:|---|
| CONS_ATENCION_SALUD | 3.5 Consecuencias | CONS_ATENCION_SALUD == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 22 | MATCHED_METADATA |
| PV_VF_hogar_VP_escuela | 3.5 Acumulación de violencias | PV_VF_hogar_VP_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_VF_hogar_escuela | 3.5 Acumulación de violencias | PV_VF_hogar_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_VP_VF_hogar_escuela | 3.5 Acumulación de violencias | PV_VP_VF_hogar_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_VP_VF_hogar_escuela_VS | 3.5 Acumulación de violencias | PV_VP_VF_hogar_escuela_VS == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_VP_hogar_VF_escuela | 3.5 Acumulación de violencias | PV_VP_hogar_VF_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_VP_hogar_escuela | 3.5 Acumulación de violencias | PV_VP_hogar_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_condicional_con_VS | 3.5 Acumulación de violencias | special(PV_hogar_escuela1) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / prevalence | Condicional | 2 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED |
| PV_condicional_escuela_dado_hogar | 3.5 Acumulación de violencias | PV_hogar_escuela == 1 | VP_o_VF_HOGAR == 1 | VP_o_VF_HOGAR == 1 | prevalence / prevalence | Área; Discapacidad; Nacional; Sexo | 7 | MATCHED_METADATA |
| PV_condicional_escuela_sin_hogar | 3.5 Acumulación de violencias | VP_o_VF_E == 1 | VP_o_VF_HOGAR == 0 | VP_o_VF_HOGAR == 0 | prevalence / prevalence | Nacional | 1 | MATCHED_METADATA |
| PV_condicional_hogar_dado_escuela | 3.5 Acumulación de violencias | PV_hogar_escuela == 1 | VP_o_VF_E == 1 | VP_o_VF_E == 1 | prevalence / prevalence | Área; Discapacidad; Nacional; Sexo | 7 | MATCHED_METADATA |
| PV_condicional_hogar_sin_escuela | 3.5 Acumulación de violencias | VP_o_VF_HOGAR == 1 | VP_o_VF_E == 0 | VP_o_VF_E == 0 | prevalence / prevalence | Nacional | 1 | MATCHED_METADATA |
| PV_hogar_escuela | 3.5 Acumulación de violencias | PV_hogar_escuela == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| PV_hogar_escuela1 | 3.5 Acumulación de violencias | PV_hogar_escuela1 == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Área; Área y sexo; Departamento; Discapacidad; Etnicidad; Lengua materna; Nacional; Sexo; Tipo de hogar | 48 | MATCHED_METADATA |
| Solap_VP_VF_E | 3.5 Acumulación de violencias | special(VP_VF_E) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / prevalence | Condicional; Prevalencia (contexto) | 4 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED; INCOMPLETE_STATISTICS |
| Solap_VP_VF_E__Coexistencia | 3.5 Acumulación de violencias | Solap_VP_VF_E__Coexistencia == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Nacional | 1 | MATCHED_METADATA |
| Solap_VP_VF_H | 3.5 Acumulación de violencias | special(VP_VF_HOGAR) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / prevalence | Condicional; Prevalencia (contexto) | 4 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED; INCOMPLETE_STATISTICS |
| Solap_VP_VF_H__Coexistencia | 3.5 Acumulación de violencias | Solap_VP_VF_H__Coexistencia == 1 | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | prevalence / prevalence | Nacional | 1 | MATCHED_METADATA |
| Solap_VS_12M | 3.5 Acumulación de violencias | special(VS_ICVAC_301) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / prevalence | 2×2; 3×3 | 8 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED |
| Solap_VS_VIDA | 3.5 Acumulación de violencias | special(VS_ICVAC_301_VIDA) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / prevalence | 2×2; 3×3 | 8 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED |
| num_consecuencias_fisicas | 3.5 Consecuencias | special(CONS_NUM_CONSECUENCIAS) | casos válidos del diseño muestral | Sin dominio adicional declarado; aplicar denominador | special / distribution | Nacional | 7 | MATCHED_METADATA; TYPE_ADAPTER_REQUIRED |

## Interpretación y límites

MATCHED_METADATA significa correspondencia del identificador, definición y presencia de salida; no significa APPROVED.
Las dimensiones de esta tabla son las existentes en la salida, incluidas dimensiones temáticas ajenas a las nueve globales.
La declaración de dimensiones del diccionario usa también nombres de variables; su catálogo de etiquetas y categorías debe conservarse en el adaptador.
Las reglas de missing se heredan del diccionario: SYSMIS/NULL según sintaxis SPSS y na.rm dentro del dominio en R.
El agregado no contiene release_id/run_id ni estados de calidad/supresión; no se atribuyen retroactivamente.
Una futura adaptación debe crear su propia ejecución local y conservar la baseline y el golden aprobados.

- El prefijo 3.5 contiene dos bloques distintos en el diccionario: Acumulación de violencias y Consecuencias. La navegación solicitada corresponde a Acumulación; CONS_ATENCION_SALUD y num_consecuencias_fisicas no se incorporan automáticamente a esa tarjeta.
- PV_condicional_con_VS, Solap_VP_VF_E, Solap_VP_VF_H, Solap_VS_12M y Solap_VS_VIDA están declarados special pero salen como prevalence; num_consecuencias_fisicas está declarado special y sale como distribution. Requieren adaptador explícito.
- Solap_VP_VF_E y Solap_VP_VF_H tienen dos filas de contexto cada uno sin es, IC ni cv. No se completan con cero ni se muestran como estimaciones completas.
