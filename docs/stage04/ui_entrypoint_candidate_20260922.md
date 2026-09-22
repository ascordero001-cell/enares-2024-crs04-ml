# Stage 04 — evidencia de integración de la entrada canónica

Fecha de preparación: 2026-09-22

Base de trabajo: `65c43631ecb62640fd4a67a8b4ee3fd3f14972c9`

Estado: candidato local; sin despliegue ni cambio de tráfico

## Alcance

- `app/streamlit_app.py` conserva la ruta de entrada canónica y delega la presentación al rediseño aprobado.
- La selección del repositorio está centralizada en `app/repositories.py`; no existe una segunda carga paralela de V0.
- La exportación CSV/XLSX reutiliza el contrato vigente mediante `app/views/export_controls.py`.
- El catálogo mantiene los ocho cortes estándar y ofrece las demás desagregaciones únicamente cuando ya existen en V0. Esto conserva las matrices 2×2/3×3 y la evidencia D01 sin fabricar cruces.
- D01 continúa dividido entre tareas del hogar (ítems 1–7) y acompañamiento (ítems 8–10), sin una figura conjunta.
- `render_legacy()` permanece temporalmente como punto de comparación local; no es la entrada ejecutada por el contenedor.

## Evidencia visual reproducible

- Escritorio, 1440 × 1000: `docs/stage04/evidence/ui-entrypoint-desktop.png`.
- Móvil, 390 × 844: `docs/stage04/evidence/ui-entrypoint-mobile.png`.
- Captura reproducible: `APP_URL=<url-local> node scripts/capture_ui_entrypoint_evidence.mjs`.

Ambas capturas se generaron contra `app/streamlit_app.py`, verificando respuesta HTTP correcta, ausencia de errores de página y presencia del catálogo de 516 indicadores.

## Verificaciones locales

- `ruff`: limpio.
- `mypy`: limpio en los cuatro módulos de integración.
- `git diff --check`: sin salida.
- `pytest`: 529 aprobadas, 2 omitidas porque el padre V0 privado no está disponible en CI; 0 fallos.
- Revisión de alcance: sin microdatos, archivos `.sav`, credenciales, enlaces de Drive ni rutas personales nuevos.

## Rollback

Este cambio no modifica recursos cloud ni tráfico. Para una futura verificación de despliegue:

1. crear una revisión nueva sin mover tráfico;
2. ejecutar health, diagnóstico del release y pruebas visuales sobre la URL de la revisión;
3. mantener identificada la revisión previa que sirve tráfico;
4. ante cualquier fallo, dejar la candidata en 0 % y devolver 100 % del tráfico a la revisión previa;
5. no promover ni retirar la revisión previa hasta la aprobación supervisora.

El merge del código tampoco autoriza despliegue, publicación ni cutover.
