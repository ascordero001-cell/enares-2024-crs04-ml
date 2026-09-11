# Conciliación del catálogo completo 3.1–3.4

Este corte intermedio se conserva como trazabilidad. La conciliación vigente de
los seis módulos está en [reconciliation_modules_31_36.md](reconciliation_modules_31_36.md).

Lectura directa del diccionario y de los agregados en Drive privado. No se usaron
microdatos ni copias locales como autoridad. Esta revisión amplía la selección
parcial previa: un indicador centinela no acredita cobertura completa de un módulo.

| Módulo | Indicadores | Filas agregadas | Informe por indicador |
|---|---:|---:|---|
| 3.1 | 100 | 1170 | [Registro completo 3.1](reconciliation_module_31.md) |
| 3.2 | 28 | 389 | [Registro completo 3.2](reconciliation_module_32.md) |
| 3.3 | 29 | 123 | [Registro completo 3.3](reconciliation_module_33.md) |
| 3.4 | 212 | 749 | [Registro completo 3.4](reconciliation_module_34.md) |
| Total | 369 | 2431 | Todos los IDs tienen definición y salida |

Cada registro conserva etiqueta exacta, numerador, denominador, dominio, tipo
estadístico, dimensiones observadas, conteo de filas y resultado de la conciliación.
N del denominador corresponde a base_unw. No se usa target_unw como sustituto.

## Excepciones concretas

- 3.1, Componentes: el diccionario declara special y la salida prevalence;
  tiene diez filas en Tareas del hogar. Requiere adaptar el contrato especial,
  no tratarlo automáticamente como una prevalencia binaria ordinaria.
- 3.4, VP_VF_VS_HOGAR: CV vacío en Departamento / Cusco y Departamento /
  Huancavelica. No se sustituye por cero. Estas filas no cumplen el contrato
  actual de estadísticas completas y deben quedar fuera de tarjetas numéricas.
- No se observaron claves dimensión/categoría duplicadas por indicador ni
  estimaciones fuera de 0–100, SE/CV/N negativos o IC que excluyan la estimación
  en los campos presentes examinados.

## Qué queda y qué no queda conciliado

La pertenencia a módulo, las definiciones y la presencia de salida se conciliaron
para todos los indicadores 3.1–3.4. Las nueve dimensiones globales no deben
confundirse con todas las dimensiones temáticas del catálogo. Los informes
conservan las dimensiones realmente observadas por indicador.

No se acredita todavía un adaptador completo ni se habilitan 369 indicadores en
Streamlit. Siguen pendientes los estados de calidad/supresión autorizados, el
tratamiento del contrato especial y los CV ausentes. Esta revisión no asigna
APPROVED ni inventa release_id/run_id para el CSV legado.

Fuentes: diccionario_indicadores.csv y tabulados_crs04_long.csv. Sus hashes de la
baseline previamente contrastada están en v0_drive_hash_manifest.md. Los archivos
de Drive no fueron modificados. Golden 3.2 intacto; LOCAL_SHADOW_ONLY;
Cloud NOT_AUTHORIZED; presupuesto USD 0; exportación deshabilitada.
