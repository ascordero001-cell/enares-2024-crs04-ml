# Mapa real de issues — Stage 04

**Repositorio:** `ascordero001-cell/enares-2024-crs04-ml`
**Estado:** `SHADOW/PREPARING`

| Tema local | Número GitHub real | URL | Tipo | Bloqueante |
|---|---:|---|---|---|
| Paraguas Stage 04 | #43 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43 | núcleo | sí |
| V0 y contratos | #44 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/44 | núcleo | sí |
| Automatización shadow | #45 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/45 | núcleo | sí |
| Auditoría, promoción y rollback | #46 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/46 | núcleo | sí |
| Looker opcional | #47 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/47 | núcleo opcional | no |
| App Streamlit y Cloud Run | #48 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/48 | núcleo | sí |
| Calidad, paridad y privacidad | #49 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/49 | núcleo | sí |
| Runbook y cutover | #50 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/50 | núcleo | sí |
| Documentación y cierre | #51 | https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/51 | núcleo | sí |
| Buckets | No creado | — | learning-lab | no |
| GKE | No creado | — | learning-lab | no |
| Airflow | No creado | — | learning-lab | no |
| Agent Engine | No creado | — | learning-lab | no |

Los números anteriores usados por las plantillas locales son referencias temáticas y no identificadores reales de GitHub. Los laboratorios opcionales se crearán únicamente si existe una decisión posterior documentada.

## Orden rector corregido

La plantilla local stage04_43.md declara como dependencia el «#42» en numeración local, que corresponde a «Automatizar ejecución por release y código en shadow» y en GitHub es el issue #45, hoy abierto. No debe confundirse con el PR #42 de GitHub, que actualizó el README y se fusionó el 2026-08-24.

Esa dependencia quedó superada por el reordenamiento del rector: la aplicación se valida primero en Sprint 04.2 mediante #46, #47 y #48, y la automatización #45 pertenece a Sprint 04.3, después de esa validación. Local 43 no está bloqueado por local 42, y no existe relación GitHub blocked by entre estos issues.
