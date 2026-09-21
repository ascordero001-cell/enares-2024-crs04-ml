# Evidencia visual previa a la paridad con la maqueta

## Reproducción

- Base SHA: `7d6e6249f6b5576dc8056d433550437d85bf22e1`
- Rama de captura: `feat/stage04-mockup-visual-parity`
- Entry point: `app/streamlit_app.py`
- Comando: `python -m streamlit run app/streamlit_app.py --server.port 8510 --server.headless true`
- Fecha de inspección: 2026-09-20 UTC

La inspección se realizó contra el entrypoint real usado por CI, Docker y Cloud Run. No se usó `app/ui_redesign_app.py` como sustituto.

## Estados verificados

| Evidencia | Estado observado | Resultado de línea base |
|---|---|---|
| Resumen en escritorio | Cabecera básica, banner de alcance, golden 3.2 y estados didácticos | Reproducible; no equivalente a la maqueta |
| Módulo 3.2 | Fuente V0 autorizada, búsqueda, indicador, categoría y exportación | Reproducible; entrypoint funcional |
| Alerta de CV | Cifra visible con texto `Referencial — precisión limitada` | Regla visible; composición pendiente |
| Estado suprimido | Sin campos estadísticos protegidos, con aviso de confidencialidad | Fail-closed visible |
| Navegación estrecha 390 × 844 | Cabecera se corta en varias líneas y la navegación depende del rail de Streamlit | Brecha responsive confirmada |
| URL cloud vigente | `https://enares-stage04-shadow-bmg5ifoitq-uc.a.run.app` | Referencia anterior; no se modificó tráfico |

## Texto accesible observado

La captura de Resumen confirmó:

- `ENARES 2024 · DEMO/SHADOW`;
- `Vigilancia de violencia contra adolescentes`;
- release `enares2024-crs04-v0-shadow-001`;
- selección `VF_HOGAR · Nacional / Total`;
- estimación `16.74 %`, EE `0.5115`, CV `3.06 %`, N no ponderado `18,807`;
- exportación CSV y Excel de una fila;
- estados didácticos Candidato, Referencia y Suprimido;
- cobertura local 3.1–3.6;
- advertencia de no publicación y ausencia de búsqueda individual.

La captura del estado suprimido confirmó que la interfaz muestra `Los campos protegidos no llegan a la interfaz` y no expone estimación, error estándar, intervalo, CV ni N.

## Hallazgos

1. El entrypoint es reproducible y conserva el golden y las protecciones existentes.
2. La estructura actual no implementa el grid `270 px | centro | 272 px` de la maqueta.
3. Faltan la franja de seis módulos, el panel derecho contextual y la navegación horizontal completa.
4. En móvil, el título ocupa un ancho insuficiente y se fragmenta; el rediseño debe eliminar este defecto.
5. La evidencia se levantó sin modificar datos, contratos, IAM, credenciales, servicio o tráfico cloud.

Las capturas visuales originales fueron tomadas durante la inspección supervisada del navegador local. La matriz de brechas y el contrato visual contienen la transcripción verificable de sus estados; las capturas binarias definitivas se incorporarán junto con la comparación `before/after` en la etapa de implementación visual, para evitar tratar esta documentación como una aprobación del nuevo layout.
