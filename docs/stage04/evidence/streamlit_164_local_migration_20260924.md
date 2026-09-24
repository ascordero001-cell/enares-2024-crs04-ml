# Streamlit 1.64.0 — validación local del entrypoint canónico

Fecha UTC: 2026-09-24. Alcance: migración de dependencia y controles; sin despliegue ni cambio de tráfico.

## Contrato actualizado

- `requirements.txt` y `requirements-runtime.txt` fijan `streamlit==1.64.0`.
- Los tres builds (local, sintético y cloud autenticado), el quickstart y las pruebas conservan aserciones explícitas de versión.
- La política de residual de accesibilidad exige exactamente cero ocurrencias en el entrypoint canónico; no exime infracciones por versión.
- La evidencia histórica tomada con 1.63.0 permanece intacta.

## Reproducción local

Se instaló Streamlit 1.64.0 en Python 3.12 y se levantó `app/streamlit_app.py` en `127.0.0.1:8515` para las pruebas de navegador. El health respondió `ok`.

| Control | Resultado |
| --- | --- |
| `python -m pytest -q` | 529 passed, 2 skipped, 0 failed |
| `ruff check src app tests` | PASS |
| `mypy --config-file mypy.ini src app tests` | PASS, 102 archivos |
| `node scripts/test_accessibility_residual_policy.mjs` | PASS; cero residual permitido |
| `npm run test:a11y` | 11/11 vistas seleccionadas y cargadas, sin errores de aplicación, cero infracciones WCAG 2.2 AA accionables, cero residuales del sidebar |
| `npm run test:six-sessions` | PASS; seis contextos independientes, HTTP 200, p95 8419 ms, pared 8541 ms |

Las 11 vistas verificadas fueron: Resumen nacional; módulos 3.1, 3.2, 3.3, 3.4, 3.5 y 3.6; Brechas; Calidad y notas; Estado del gate; Historial. La verificación selecciona cada vista por URL, espera el contenido específico y rechaza excepciones de Streamlit y errores de navegador. La prueba de seis sesiones abrió Resumen nacional, 3.1, 3.2, 3.5, Brechas y Estado del gate simultáneamente.

## Límites y siguiente gate

La validación de imagen Docker y el quickstart de runner limpio deben confirmarse en GitHub Actions sobre el nuevo head. Esta prueba local no demuestra consumo de Cloud Run ni autoriza desplegar la versión 1.64.0. Si se solicita una prueba cloud posterior, la candidata deberá ser privada, autenticada y mantenerse a 0 % de tráfico hasta un GO separado. La revisión vigente de Cloud Run no cambia por este PR.
