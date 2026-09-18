# Evaluación de usabilidad — Sprint 04.2

Estado: `FULL_CATALOG_HEURISTICS_AND_COGNITIVE_WALKTHROUGH_COMPLETE; ACCESSIBILITY_PARTIAL`.
Fecha de corte: 2026-09-17.

## Alcance y evidencia disponible

Esta evaluación reúne la revisión heurística inicial de la interfaz local, las pruebas funcionales
con AppTest y el control automatizado WCAG 2.2 AA descrito en
[`hci_accessibility_corte2.md`](../stage04/hci_accessibility_corte2.md). La decisión supervisora del
2026-09-15 sustituye la prueba con participantes externos por revisión manual de accesibilidad,
evaluación heurística y recorrido cognitivo. La repetición sobre las 3.014 filas conectadas está
registrada en [`full_catalog_step51_evaluation.md`](full_catalog_step51_evaluation.md).

## Escala de severidad

| Nivel | Definición | Tratamiento |
| --- | --- | --- |
| S0 | Sin problema observable | Sin acción |
| S1 | Fricción menor; no altera la interpretación ni bloquea la tarea | `DEFER` admisible |
| S2 | Puede causar error recuperable o duda relevante | `FIX` antes del cierre, salvo dependencia externa documentada |
| S3 | Bloquea una tarea o puede producir una interpretación incorrecta | `FIX` obligatorio |
| S4 | Expone información, rompe el alcance autorizado o produce un resultado falso | `REJECT` y detención |

## Revisión heurística

| Heurística | Evidencia revisada | Resultado | Severidad / decisión |
| --- | --- | --- | --- |
| Visibilidad del estado | Encabezado de release, alcance local, estados de calidad y mensajes `sin datos` | Conforme | S0 |
| Correspondencia con el lenguaje institucional | Módulos 3.1–3.6, universo, denominador, `N no ponderado` y notas de precisión | Conforme | S0 |
| Control y libertad | Navegación y selectores nativos; una selección no autorizada falla cerrada | Conforme | S0 |
| Consistencia | Marcador `Referencial` derivado de `cv_flag`; etiquetas y descargas siguen el corte visible | Conforme | S0 |
| Prevención de errores | Validación de release, alcance, dimensión/categoría y granularidad antes de mostrar filas | Conforme | S0 |
| Reconocimiento antes que recuerdo | Navegación, opciones, metodología y estado del release permanecen visibles | Conforme | S0 |
| Diseño minimalista | Presentación de agregados sin microdatos, búsquedas individuales ni controles cloud | Conforme | S0 |
| Recuperación ante errores | Mensajes genéricos no revelan rutas, secretos o contenido privado | Conforme | S0 |
| Ayuda y documentación | La interfaz explica CV, N, universo, denominador, granularidad y release | Conforme | S0 |
| Semántica del sidebar | Streamlit 1.63.0 añade `aria-expanded` al elemento raíz con un rol que no admite el atributo | Residual externo acotado por la prueba | S2 / `DEFER` hasta actualización de Streamlit; revalidar |

El `DEFER` anterior no desactiva una familia completa de controles: la CI admite únicamente la
combinación exacta de regla, selector y atributo documentada. Cualquier otra infracción automática
hace fallar el job.

## Reevaluación sobre el catálogo completo

1. **Revisión manual de accesibilidad:** teclado, nombres/roles, estados textuales, contraste y
   lectura real con Narrador quedaron revisados. Falta el zoom verificable al 200 %.
2. **Evaluación heurística:** las diez heurísticas quedaron repetidas sin S3/S4.
3. **Recorrido cognitivo:** los cinco escenarios de [`task_scenarios.md`](task_scenarios.md)
   quedaron recorridos con resultado PASS.

La falta de observación por una persona nueva se conserva como riesgo residual: estos métodos
detectan incumplimientos conocidos, pero no sustituyen el descubrimiento de problemas por usuarios
reales.

## Condición de cierre

El checkpoint HCI no se declara cerrado hasta conectar el catálogo autorizado, ejecutar y
documentar los tres métodos, y resolver cualquier S3/S4. Un hallazgo S2 solo puede quedar en
`DEFER` con causa, responsable de seguimiento y condición explícita de reevaluación.
