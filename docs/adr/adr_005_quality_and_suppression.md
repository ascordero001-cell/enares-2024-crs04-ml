# ADR-005: Calidad y supresión complementaria

- Fecha inicial: 2026-09-04
- Última decisión: 2026-09-13
- Estado: `QUALITY_ALERTS_APPROVED; CONFIDENTIALITY_POLICY_PENDING`
- Autoridad de alertas: Rita Ricaldi, revisión del PR #60
- Propietario institucional de confidencialidad: `PENDIENTE/NO_ASIGNADO`

## Origen

El documento rector exige diferenciar resultados candidatos publicables, referenciales y
suprimidos. La PUERTA B los introdujo como ejercicios; la decisión supervisora del 2026-09-13
aprobó CV/N como alertas visibles y descartó su uso automático como supresión.

## Decisión vigente

En 3.1–3.6, CV > 15 % conserva la prevalencia, la marca referencial y añade la nota aprobada.
`base_unw < 30` conserva la prevalencia y añade la alerta de N pequeño. En ambos casos se conservan
los estadísticos disponibles y ninguna señal activa `suppress_flag`. CV=15 % y N=30 no activan
alertas; ausencias no se imputan.

Una celda suprimida por una política independiente activa análisis de reconstrucción y, cuando un
total o margen la revela, supresión complementaria. Published elimina estimate, error estándar,
intervalo, CV y N antes de que la aplicación o un export reciban esa fila.

Las entradas se mantienen separadas por clasificación: el demo es 100 % sintético; el golden usa
un único agregado V0 autorizado, no sintético y sin microdatos, ligado a su propio manifiesto. Los
datos institucionales publicados no están autorizados. BigQuery, DDL, Cloud Run y demás recursos
cloud permanecen `BLOCKED_BY_CLOUD_GATE`.

## Estado de decisiones

| Decisión | Estado | Responsable de aprobar | Evidencia requerida |
|---|---|---|---|
| Nulificar campos protegidos en una celda suprimida dentro de published candidata | `TECHNICAL_CONTROL_IMPLEMENTED_LOCAL` | Revisión técnica del PR | Tests de supresión y contrato |
| Usar `suppress_flag` como control principal de nulificación | `TECHNICAL_CONTROL_IMPLEMENTED_LOCAL` | Revisión técnica del PR | Tests de estado/flag y campos protegidos |
| Usar `CV > 15 %` como señal referencial visible | `APPROVED_2026_09_13` | Rita Ricaldi | Casos límite y seis módulos |
| Usar `base_unw < 30` como alerta visible, sin supresión | `APPROVED_2026_09_13` | Rita Ricaldi | N=29/30/31 y seis módulos |
| Tolerancia golden absoluta `1e-9` | `PROPOSED_REQUIRES_SUPERVISORY_APPROVAL` | Supervisión metodológica | Comparación de serialización y sensibilidad |
| Regla institucional de calidad y supresión | `NOT_APPROVED_PENDING_SUPERVISION` | Institución y propietario metodológico aún no asignado | Política formal, pruebas multitabla/multirelease y aprobación registrada |

La decisión aprobada se limita a calidad/presentación. No aprueba cifras, tolerancia ni política
de confidencialidad y no autoriza publicación institucional.

## Alternativas

- Mostrar alertas CV/N sin ocultar la prevalencia: adoptada para calidad; no sustituye el control
  independiente de confidencialidad.
- Suprimir solo visualmente: rechazada porque logs, API o exports conservarían valores.
- Suprimir totales en vez de una segunda celda: posible, pero reduce utilidad y requiere revisión.
- Métodos formales de control de divulgación: evaluar antes de una regla institucional.

## Efectos y riesgos

La supresión complementaria reduce inferencia directa, pero puede ocultar más información. El
riesgo residual incluye ataques multitabla, multirelease y enlace con fuentes externas.

## Condición de aprobación institucional

Asignar propietario institucional de confidencialidad, aprobar precedencias de supresión, probar
cruces y releases, definir excepciones y registrar riesgo residual. Hasta entonces cifras nuevas,
publicación y cutover continúan bloqueados y el alcance es `LOCAL_SHADOW_ONLY`.
