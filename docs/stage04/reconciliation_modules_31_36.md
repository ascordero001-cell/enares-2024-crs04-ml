# Conciliación del catálogo completo 3.1–3.6

Lectura directa del diccionario y de los agregados en Drive privado. No se usaron
microdatos ni copias locales como autoridad. Un indicador centinela no acredita
cobertura completa de un módulo; los seis informes registran el catálogo íntegro.

| Módulo | Indicadores | Filas agregadas | Informe por indicador |
|---|---:|---:|---|
| 3.1 | 100 | 1170 | [Registro completo 3.1](reconciliation_module_31.md) |
| 3.2 | 28 | 389 | [Registro completo 3.2](reconciliation_module_32.md) |
| 3.3 | 29 | 123 | [Registro completo 3.3](reconciliation_module_33.md) |
| 3.4 | 212 | 749 | [Registro completo 3.4](reconciliation_module_34.md) |
| 3.5 | 21 | 457 | [Registro completo 3.5](reconciliation_module_35.md) |
| 3.6 | 126 | 126 | [Registro completo 3.6](reconciliation_module_36.md) |
| Total | 516 | 3014 | Todos los IDs tienen definición y salida |

Cada registro conserva etiqueta exacta, numerador, denominador, dominio, tipo
estadístico, dimensiones observadas, conteo de filas y resultado de conciliación.
N del denominador corresponde exclusivamente a base_unw; target_unw es el conteo
del objetivo y no lo sustituye.

## Excepciones concretas

- 3.1, Componentes: el diccionario declara special y la salida prevalence.
- 3.4, VP_VF_VS_HOGAR: CV vacío en Departamento / Cusco y Huancavelica.
- 3.5 contiene Acumulación de violencias y Consecuencias; la navegación 3.5 no
  incorpora automáticamente los dos indicadores de Consecuencias.
- Seis salidas 3.5 requieren adaptador explícito por diferencia entre special y
  prevalence/distribution. Dos filas de contexto de Solap_VP_VF_E y otras dos de
  Solap_VP_VF_H carecen de SE, IC y CV.
- 3.6 solo tiene salida Nacional. C3P242_10, C3P242_5, C4P258_7 y ayuda_vs_car
  tienen estimación y target_unw iguales a cero, con CV vacío.
- No se observaron claves dimensión/categoría duplicadas, estimaciones fuera de
  0–100, estadísticas negativas ni IC que excluyan la estimación en los campos
  presentes de 3.5 y 3.6.

## Alcance del resultado

La pertenencia a módulo, las definiciones y la presencia de salida quedaron
conciliadas para los 516 indicadores. Esto no habilita automáticamente las cifras
en Streamlit: siguen pendientes los estados autorizados de calidad/supresión, los
adaptadores especiales, el nuevo run_id local y la revisión formal del Corte 2.

Fuentes: diccionario_indicadores.csv y tabulados_crs04_long.csv. Sus hashes de la
baseline contrastada están en v0_drive_hash_manifest.md. Los archivos de Drive no
fueron modificados. Golden 3.2 intacto; LOCAL_SHADOW_ONLY; Cloud NOT_AUTHORIZED;
presupuesto USD 0; exportación deshabilitada.
