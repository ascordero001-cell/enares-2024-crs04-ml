# PR #154 — recorrido de accesibilidad de la entrada canónica

Verificación local: 2026-09-23 UTC. Entrada: `app/streamlit_app.py`, Streamlit 1.63.0. Comando: `npm run test:a11y` con `APP_URL` dirigido a la instancia local de esa entrada.

El control abre cada `?view=`, exige que el radio de la vista esté seleccionado, espera contenido propio de esa vista dentro del panel central y falla ante una excepción de Streamlit, un error inesperado de la aplicación, un error de página o una respuesta HTTP no satisfactoria. La leyenda prevista «Suprimido — ningún campo estadístico protegido llega a la vista» no se confunde con un error de ejecución.

| Vista solicitada | Selección y contenido | Errores de aplicación | Infracciones WCAG 2.2 AA accionables |
| --- | --- | ---: | ---: |
| Resumen nacional | PASS | 0 | 0 |
| Módulo 3.1 | PASS | 0 | 0 |
| Módulo 3.2 | PASS | 0 | 0 |
| Módulo 3.3 | PASS | 0 | 0 |
| Módulo 3.4 | PASS | 0 | 0 |
| Módulo 3.5 | PASS | 0 | 0 |
| Módulo 3.6 | PASS | 0 | 0 |
| Brechas | PASS | 0 | 0 |
| Calidad y notas | PASS | 0 | 0 |
| Estado del gate | PASS | 0 | 0 |
| Historial | PASS | 0 | 0 |

Resultado: `PASS: no actionable WCAG 2.2 AA violations; 0 known Streamlit sidebar occurrence(s) recorded`.

La referencia al SHA completo de este cambio y la CI del nuevo head se registran en el comentario de revisión del PR #154 después del push.
