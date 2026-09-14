# Revisión de separación — adaptadores sintético e institucional

Estado: `SUPERVISORY_REVIEW_REQUIRED_BEFORE_FIRST_AGGREGATE`

Alcance: esqueletos y pruebas locales; cero agregados nuevos conectados.

## Decisión de diseño propuesta

Los dos flujos no comparten una vía de entrada ni pueden cambiar de clasificación:

```text
fixture synthetic=true
  -> SyntheticCandidateAdapter
  -> validación de contratos con datos inventados
  -> pruebas locales únicamente

agregado institutional synthetic=false + manifiesto aprobado
  -> InstitutionalAuthorizedAggregateAdapter
  -> [DETENIDO: revisión supervisora]
  -> validación institucional propia
  -> repositorio de agregados autorizados
```

| Control | Adaptador sintético | Adaptador institucional |
|---|---|---|
| Identidad | `synthetic-candidate-v1` | `institutional-authorized-aggregate-v1` |
| Clasificación aceptada | `SYNTHETIC_TEST_ONLY` | `AUTHORIZED_INSTITUTIONAL_AGGREGATE` |
| Marca exigida | `synthetic=true` | `synthetic=false` |
| Evidencia de procedencia | fixture versionado | manifiesto, hash y registro de aprobación |
| Estado de conexión | `LOCAL_TEST_ONLY` | `REVIEW_REQUIRED_BEFORE_FIRST_AGGREGATE` |
| Acceso desde la aplicación | no | no |

## Invariantes demostradas

1. El adaptador sintético rechaza cualquier fila que no declare literalmente `synthetic=true`.
2. El adaptador institucional rechaza filas sintéticas o sin clasificación explícita.
3. Aunque reciba una fila con `synthetic=false`, el esqueleto institucional lanza
   `AdapterSeparationReviewRequired` y no transforma la fila.
4. Ambos adaptadores tienen nombres, versiones y clasificaciones diferentes.
5. `app/streamlit_app.py` no importa ni instancia el adaptador institucional.
6. No existe una operación que cambie `synthetic=false` a `synthetic=true`.

Pruebas: `tests/test_stage04_etapa1_boundaries.py`.

## Integración propuesta después de aprobación

Si la separación es aprobada, el adaptador institucional recibirá exclusivamente objetos ya
verificados por `AuthorizedAggregateRepository`: CSV agregado, manifiesto coincidente, SHA-256,
`synthetic=false`, clasificación `AUTHORIZED_AGGREGATE_ONLY` y hash fuente presente en el registro
V0 aprobado. Después aplicará un adaptador estadístico con nombre y versión por caso D01–D11 y
volverá a ejecutar las validaciones de alcance antes de construir cualquier modelo de interfaz.

No se propone reutilizar `adapt_candidate_row` en el flujo institucional porque esa función es la
barrera de pruebas sintéticas. Las reglas estadísticas compartidas se extraerían después de esta
revisión como funciones puras que no puedan alterar la clasificación de origen.

## Decisión solicitada

Se solicita a `ritaricaldi-cpu` aprobar o corregir:

1. la frontera de clasificación y procedencia;
2. la prohibición de reutilizar el entrypoint sintético;
3. el orden repositorio autorizado → adaptador institucional → validación de alcance → vista;
4. la extracción posterior de reglas estadísticas puras compartidas.

Hasta esa decisión no se implementa la transformación institucional ni se conecta el primer
agregado. Cloud, publicación, exportación fuera del golden y cutover permanecen bloqueados.
