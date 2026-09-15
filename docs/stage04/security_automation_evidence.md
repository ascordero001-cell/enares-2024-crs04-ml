# Stage 04 — automatización de seguridad (pasos 27–28)

**Estado:** IMPLEMENTED_PENDING_CI

## Paso 27 — dependencias

Dependabot revisa semanalmente dos ecosistemas independientes: dependencias Python declaradas en
la raíz y versiones de GitHub Actions. Los PR automáticos quedan limitados a cinco por ecosistema
para mantener una cola revisable.

`Security CI` ejecuta `pip-audit` sobre `requirements.txt` y `requirements-dev.txt`. El job falla
ante vulnerabilidades conocidas; no corrige versiones automáticamente ni autoriza un merge.

La primera ejecución local detectó `PYSEC-2026-2275` en `requests==2.32.4`. La dependencia se
actualizó a la versión corregida `2.33.0`; la auditoría posterior no encontró vulnerabilidades
conocidas.

## Paso 28 — secretos

`Security CI` ejecuta Gitleaks sobre el historial completo en cada PR, cada push a `main`, una vez
por semana y bajo ejecución manual. Los comentarios automáticos están desactivados para no copiar
hallazgos sensibles a una conversación del PR. Un hallazgo bloquea el job y debe tratarse fuera de
los logs públicos: revocación o rotación primero y saneamiento del historial solo mediante un plan
aprobado.

## Límites

Estos controles no habilitan cloud, IAM, facturación ni despliegues. No sustituyen revisión humana,
análisis de amenazas ni las reglas de protección de ramas. Cloud continúa `NOT_AUTHORIZED` y el
presupuesto autorizado continúa en USD 0.
