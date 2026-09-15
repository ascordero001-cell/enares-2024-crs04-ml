# Evaluación de usabilidad — Sprint 04.2

Estado: `HEURISTIC_REVIEW_COMPLETE; INDEPENDENT_SYNTHETIC_TEST_PENDING`.
Fecha de corte: 2026-09-15.

## Alcance y evidencia disponible

Esta evaluación reúne la revisión heurística de la interfaz local, las pruebas funcionales con
AppTest y el control automatizado WCAG 2.2 AA descrito en
[`hci_accessibility_corte2.md`](../stage04/hci_accessibility_corte2.md). No acredita todavía una
prueba independiente con personas usuarias ni una auditoría formal con lector de pantalla.

La prueba formativa pendiente se realizará con 3 a 5 personas de perfil institucional y una demo
reproducible que use únicamente datos sintéticos. No se conectarán nuevas cifras reales, cloud ni
microdatos para ejecutarla.

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

## Prueba formativa independiente

Estado de participantes: `PENDING_INDEPENDENT_PARTICIPANTS`.

Se usarán los cinco escenarios de [`task_scenarios.md`](task_scenarios.md). Antes de iniciar cada
sesión se comprobará que la instancia sea sintética, local y sin acceso a fuentes privadas. La
persona facilitadora no dirigirá el recorrido salvo que la participante pida ayuda; esa ayuda se
registrará.

| Sesión | Perfil | T1 | T2 | T3 | T4 | T5 | Hallazgos / decisión |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Pendiente | — | — | — | — | — | Pendiente |
| 2 | Pendiente | — | — | — | — | — | Pendiente |
| 3 | Pendiente | — | — | — | — | — | Pendiente |
| 4 (opcional) | Pendiente | — | — | — | — | — | Pendiente |
| 5 (opcional) | Pendiente | — | — | — | — | — | Pendiente |

Para cada celda de tarea se anotará resultado, tiempo aproximado, errores y dudas. Los hallazgos se
clasificarán por severidad y terminarán en `FIX`, `DEFER` o `REJECT`. No se completarán las filas
por anticipado ni se atribuirán resultados a participantes inexistentes.

## Condición de cierre

El checkpoint HCI no se declara cerrado hasta ejecutar y documentar al menos tres sesiones
independientes, revisar los hallazgos y resolver cualquier S3/S4. Un hallazgo S2 solo puede quedar
en `DEFER` con causa, responsable de seguimiento y condición explícita de reevaluación.
