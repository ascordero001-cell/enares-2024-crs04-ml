# Matriz de cobertura — Corte 2

Estado: CORTE2_ENGINEERING_CHECKPOINT_APPROVED_MERGED; NUMERIC_DATA_GATE_OPEN.
Alcance: LOCAL_SHADOW_ONLY.

Detalle verificable por indicador y dimensión:
[module_indicator_dimension_matrix.md](module_indicator_dimension_matrix.md).

Las nueve dimensiones están configuradas. La existencia de filas en Drive no equivale a
conciliación de calidad, supresión y significado del indicador para su presentación.
Tampoco equivale a autorización: una dimensión puede figurar en `available_dimensions`, pero
solo `authorized_dimensions` habilita el agregado no sintético después de validar indicador,
disponibilidad y autorización. La UI repite el gate antes de consultar el repositorio.

| Módulo | Centinela examinado en Drive | Dimensiones observadas para ese centinela | Datos habilitados en UI | Evidencia automatizada |
|---|---|---|---|---|
| 3.1 Mitos sobre el castigo | justifica_castigo_parental; justifica_castigo_docente | Nueve por indicador | Pendiente: estados de calidad/supresión | AppTest: navegación y sin datos |
| 3.2 Violencia en el hogar | VF_HOGAR | Nueve | Solo Nacional / Total del golden aprobado | Golden y AppTest |
| 3.3 Violencia en la escuela | C3P223_10_1 | Nacional | Pendiente: contrato de calidad y N | AppTest: navegación y sin datos |
| 3.4 Violencia sexual | Agresor_VS_12M__AG_01 | Nacional | Pendiente: contrato de calidad y N | AppTest: navegación y sin datos |
| 3.5 Acumulación de violencia | Catálogo completo: 21 IDs, incluidos 19 de acumulación y 2 de consecuencias | Nueve globales y dimensiones temáticas según indicador | Pendiente: estados de calidad/supresión y adaptadores special | Conciliación completa de Drive + AppTest sin datos |
| 3.6 Búsqueda de ayuda | Catálogo completo: 126 IDs | Nacional | Pendiente: estados de calidad/supresión; cuatro CV vacíos | Conciliación completa de Drive + AppTest sin datos |

Los seis módulos ya tienen conciliación documental completa en Drive. Esto no equivale a
habilitar los 516 indicadores en la interfaz. Los estados candidato, referencial y suprimido
siguen ejercitándose con el fixture sintético aprobado de 3.2.
No se adoptó una nueva regla institucional de CV, N o supresión.
