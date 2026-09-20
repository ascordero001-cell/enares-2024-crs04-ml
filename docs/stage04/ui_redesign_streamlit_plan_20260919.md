# Stage 04 — rediseño de UI en Streamlit

- Fecha: 2026-09-19
- Issue núcleo: [#144](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/144)
- Precondición: Sprint 04.3 cerrado mediante PR #143
- Estado: `STAGE1_SPECIFICATION_READY_FOR_SUPERVISORY_REVIEW`
- Alcance: `CONTROLLED_SHADOW`

## Decisión de arquitectura

La maqueta se traducirá a componentes de la aplicación Streamlit existente. No se reconstruirá la
aplicación en otro stack: se conservan el repositorio de agregados, la validación, la autenticación
y el despliegue ya revisados.

El rediseño cambia únicamente la presentación. No autoriza indicadores, dimensiones o categorías
fuera del acta D01–D12 y no duplica reglas de `authorized_scopes.py` ni `quality_rules.py`.

## Etapas y gates

| Etapa | Alcance | Gate de salida |
|---|---|---|
| 0 | commit base, inventario de componentes y confirmación de infraestructura | confirmación de reutilización sin IAM/credenciales/recursos nuevos |
| 1 | mapeo visual, estados, filtros y exportación | aprobación supervisora de la especificación |
| 2 | estructura/layout con datos 100 % sintéticos y AppTest | aprobación supervisora antes de conectar datos reales |
| 3 | reutilización del adaptador real y prueba de paridad golden | paridad y ausencia de cambios cloud verificadas |
| 4 | suite, evidencia ejecutable y cierre | decisión supervisora final |

La Etapa 2 no comienza hasta incorporar o identificar la maqueta
`ui_redesign_mockup_v1.html` y aprobar la especificación de la Etapa 1. La Etapa 3 permanece
bloqueada hasta la aprobación explícita de la estructura sintética.

## Límites permanentes

- Sin ampliación de D01–D12.
- Sin consultas directas a `outputs`; el runtime conserva `published.v_dashboard_current`.
- Sin lógica estadística o de autorización nueva en la UI.
- Sin cambios IAM, credenciales, conexión o infraestructura.
- Sin acceso público, publicación institucional, cutover o sustitución de V0.
- CV alto y N reducido permanecen visibles como alertas; nunca causan supresión.
- `suppress_flag`, `cv_flag` y `n_flag` se representan como señales independientes.

## Dependencia visual pendiente

La referencia `ui_redesign_mockup_v1.html` no está versionada en el repositorio ni fue encontrada
junto al documento rector recibido. No se inventará su estructura visual. El mapeo de Etapa 1
define componentes y contratos; la implementación pixel/estructura de Etapa 2 espera esa maqueta
o una confirmación explícita de que la especificación textual es suficiente.

## Discrepancia que requiere decisión

El documento de entrada describe el panel CSV/Excel como construido pero deshabilitado. El estado
vigente de `main`, aprobado durante Sprint 04.2, tiene `EXPORT_ENABLED = True` y pruebas que exigen
exportación agregada segura. Esta especificación no revierte esa decisión. Rita debe confirmar si
el rediseño conserva la exportación agregada habilitada o si existe una nueva decisión que la
deshabilita. Hasta entonces, la Etapa 2 no modifica el control.
