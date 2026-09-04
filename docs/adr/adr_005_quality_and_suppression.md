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

## Estado de decisiones

| Decisión | Estado | Responsable de aprobar | Evidencia requerida |
|---|---|---|---|
| Nulificar campos protegidos en una celda suprimida dentro de published candidata | `TECHNICAL_CONTROL_IMPLEMENTED_LOCAL` | Revisión técnica del PR | Tests de supresión y contrato |
| Usar `CV > 0.15` como señal referencial | `DIDACTIC_PROPOSAL` | Propietario metodológico `PENDIENTE/NO_ASIGNADO` y supervisión | Criterio institucional documentado y casos límite |
| Usar `N < 30` como señal de supresión | `DIDACTIC_PROPOSAL` | Propietario metodológico `PENDIENTE/NO_ASIGNADO` y supervisión | Evaluación de divulgación, utilidad y cruces |
| Tolerancia golden absoluta `1e-9` | `PROPOSED_REQUIRES_SUPERVISORY_APPROVAL` | Supervisión metodológica | Comparación de serialización y sensibilidad |
| Regla institucional de calidad y supresión | `NOT_APPROVED_PENDING_SUPERVISION` | Institución y propietario metodológico aún no asignado | Política formal, pruebas multitabla/multirelease y aprobación registrada |

La implementación técnica local no convierte una propuesta didáctica en decisión institucional.
No existe autoaprobación de umbrales, tolerancia ni propietario.

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
