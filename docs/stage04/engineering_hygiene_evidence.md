# Evidencia de higiene de ingeniería — Stage 04

- Fecha UTC: 2026-09-15
- Alcance: pasos 23–26
- Implementación revisada: PR #74, aprobado sobre `41715dc20fc56304c62a63953421dbe17bac4034`
- Estado: `APPROVED_AND_MERGED`

## Numeración correcta

El paso 22 corresponde al contenedor ejecutable y quedó cerrado antes de este bloque. El PR #74
cerró los pasos 23–26: App CI, firmas tipadas, taxonomía `RepositoryError` y caché inmutable por
`release_id + run_id`. Gitleaks corresponde al paso 28; no es el requisito de revisión del PR #74.

## Alcance real de mypy

La primera ejecución con `follow_imports = normal` encontró 22 errores, todos dentro de
generadores históricos de Stage 03 alcanzados indirectamente desde los tests. No encontró errores
en `repository`, `validation`, `view_model` ni en otros módulos de Stage 04.

El estado definitivo conserva `follow_imports = normal` globalmente, por lo que mypy comprueba los
tipos que cruzan entre `src`, `app` y `tests`. Solo `scripts.*` mantiene `follow_imports = skip` de
forma explícita y documentada. En consecuencia, un resultado `CLEAN` no afirma que los generadores
legados de Stage 03 estén tipados; registra únicamente el alcance configurado en `mypy.ini`.

Este ajuste no cambia cifras, hashes V0, reglas estadísticas, runtime ni estado cloud.
