# ADR-005: Calidad y supresión complementaria

- Fecha: 2026-09-04
- Estado: `PROPOSED_REQUIRES_METHODOLOGICAL_APPROVAL`
- Propietario metodológico: `PENDIENTE/NO_ASIGNADO`

## Origen

El documento rector exige diferenciar resultados candidatos publicables, referenciales y
suprimidos. `CV > 0.15` y `N < 30` fueron autorizados únicamente como ejemplos didácticos en la
PUERTA B del PR #54.

## Decisión propuesta

Aplicar las reglas solo en fixtures y pruebas locales, con origen y versión visibles. Una celda
primaria suprimida activa análisis de reconstrucción y, cuando un total o margen la revela,
supresión complementaria. Published elimina estimate, error estándar, intervalo, CV y N antes de
que la aplicación o un export reciban la fila.

## Alternativas

- Mostrar todo con advertencias: rechazada por riesgo de reconstrucción.
- Suprimir solo visualmente: rechazada porque logs, API o exports conservarían valores.
- Suprimir totales en vez de una segunda celda: posible, pero reduce utilidad y requiere revisión.
- Métodos formales de control de divulgación: evaluar antes de una regla institucional.

## Efectos y riesgos

La supresión complementaria reduce inferencia directa, pero puede ocultar más información. El
riesgo residual incluye ataques multitabla, multirelease y enlace con fuentes externas.

## Condición de aprobación institucional

Asignar propietario metodológico, aprobar umbrales y precedencias, probar cruces y releases,
definir excepciones y registrar aprobación supervisora. Hasta entonces todo estado es provisional
y `LOCAL_SHADOW_ONLY`.
