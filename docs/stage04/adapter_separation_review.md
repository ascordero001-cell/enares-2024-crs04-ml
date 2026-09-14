# Revisión de separación — adaptadores sintético e institucional

Estado: `APPROVED_PR62; CONDITIONS_IMPLEMENTED_2026-09-14`

Alcance: adaptadores y pruebas locales; cero agregados nuevos conectados a la aplicación.

Tras la aprobación del PR #62, la transformación institucional quedó habilitada únicamente para
objetos emitidos por `AuthorizedAggregateRepository` con clasificación interna de procedencia.
Las reglas de CV, N, notas y `quality_status` viven en `quality_rules.py` y son llamadas por los
dos adaptadores. Esto no conecta D01–D12 a la aplicación ni amplía el alcance autorizado.

## Decisión de diseño propuesta

Los dos flujos no comparten una vía de entrada ni pueden cambiar de clasificación:

```text
fixture synthetic=true
  -> SyntheticCandidateAdapter
  -> validación de contratos con datos inventados
  -> pruebas locales únicamente

agregado institucional + manifiesto/hash/registro aprobados
  -> AuthorizedAggregateRepository deriva synthetic=false
  -> InstitutionalAuthorizedAggregateAdapter
  -> validación estadística pura compartida
  -> salida LOCAL SHADOW (sin conexión automática a la aplicación)
```

| Control | Adaptador sintético | Adaptador institucional |
|---|---|---|
| Identidad | `synthetic-candidate-v1` | `institutional-authorized-aggregate-v1` |
| Clasificación aceptada | `SYNTHETIC_TEST_ONLY` | `AUTHORIZED_INSTITUTIONAL_AGGREGATE` |
| Marca exigida | `synthetic=true` literal del fixture | derivada; nunca leída del CSV ni del llamador |
| Evidencia de procedencia | fixture versionado | manifiesto, hash y registro de aprobación |
| Estado de conexión | `LOCAL_TEST_ONLY` | `PROVENANCE_GATE_REQUIRED` |
| Acceso desde la aplicación | no | no |

## Invariantes demostradas

1. El adaptador sintético rechaza cualquier fila que no declare literalmente `synthetic=true`.
2. El adaptador institucional rechaza incluso una fila demo alterada manualmente a
   `synthetic=false`; exige el tipo interno emitido por el repositorio autorizado.
3. `AuthorizedAggregateRepository` deriva `synthetic=false` solo después de verificar nombre,
   SHA-256, clasificación de manifiesto, hash fuente y registro V0 aprobado.
4. Ambos adaptadores tienen nombres, versiones y clasificaciones diferentes.
5. `app/streamlit_app.py` no importa ni instancia el adaptador institucional.
6. No existe una operación que cambie `synthetic=false` a `synthetic=true`.

Pruebas: `tests/test_stage04_etapa1_boundaries.py`.

## Integración posterior a la aprobación

El adaptador institucional recibe exclusivamente objetos ya
verificados por `AuthorizedAggregateRepository`: CSV agregado, manifiesto coincidente, SHA-256,
`synthetic=false`, clasificación `AUTHORIZED_AGGREGATE_ONLY` y hash fuente presente en el registro
V0 aprobado. Después aplicará un adaptador estadístico con nombre y versión por caso D01–D11 y
volverá a ejecutar las validaciones de alcance antes de construir cualquier modelo de interfaz.

No se reutiliza el entrypoint `adapt_candidate_row`: esa función conserva la barrera de pruebas
sintéticas. Ambos entrypoints sí reutilizan la validación posterior a la frontera y
`derive_statistical_quality`, una función pura que no puede alterar la clasificación de origen.

## Decisión recibida

`ritaricaldi-cpu` aprobó en el PR #62:

1. la frontera de clasificación y procedencia;
2. la prohibición de reutilizar el entrypoint sintético;
3. el orden repositorio autorizado → adaptador institucional → validación de alcance → vista;
4. la extracción previa de reglas estadísticas puras compartidas.

Las condiciones 3 y 4 ya están implementadas y probadas. La aplicación continúa sin importar el
adaptador institucional. Cloud, publicación, exportación fuera del golden y cutover permanecen
bloqueados.
