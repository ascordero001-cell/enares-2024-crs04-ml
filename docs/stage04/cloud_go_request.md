# Solicitud de autorización cloud y GO — pasos 40 y 41

**Fecha:** 2026-09-14 UTC

**Estado de esta solicitud:** `APPROVED_2026-09-14`

**Estado operativo vigente:** `GO_FOR_STAGE7_CONTROLLED_SHADOW; PRIVATE_VERIFICATION_COMPLETE; RESOURCE_CREATION_BLOCKED_BY_STEP47`

Esta solicitud no habilita por sí sola servicios, billing ni IAM. El GO permite iniciar la Etapa 7
controlada cuando presupuesto, alertas e IAM estén configurados en el orden aprobado. No autoriza
publicación institucional, cutover, sustitución de V0 ni nuevas cifras.

## 1. Evidencia previa del camino crítico

| Control | Evidencia | Resultado |
|---|---|---|
| Imagen construible | [Container CI corregido del PR #68](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/34906554621), fusionado en `main` mediante `3c7b4d3212d360e4dd940800c99f1f8b5ec2f1c2` | `SUCCESS` |
| Tamaño de imagen | Medido mediante `docker image inspect --format='{{.Size}}'` en el mismo run | `1,273,620,610 bytes` (aprox. 1.19 GiB) |
| Aplicación dentro del contenedor | Inicio y respuesta HTTP en el mismo run | `SUCCESS` |
| Streamlit fijado | Verificación dentro de la imagen | `1.63.0` |
| Health superficial | `/_stcore/health` dentro del contenedor | `200 / ok` |
| Diagnóstico profundo | Todas las filas autorizadas: release único, `source_version` único y ningún módulo 3.1–3.6 vacío | `SUCCESS` |
| Estado Docker | Healthcheck de la imagen | `healthy` |
| Regresión local | Suite con padre V0 privado | `405 passed; 0 failed` |

La ejecución se realizó en GitHub Actions porque el host local de desarrollo no dispone de Docker
ni Podman. No se presenta como evidencia local una ejecución que no ocurrió.

## 2. Alcance exacto solicitado para la Etapa 7

Tras un GO formal, y no antes, se solicita autorización para configurar y verificar:

- proyecto exacto `enares-2024-crs04`, después de confirmar que existe y pertenece a la cuenta
  de billing aprobada;
- un repositorio de Artifact Registry para una imagen candidata inmutable;
- un servicio Cloud Run autenticado en `us-central1`, con mínimo cero y máximo una instancia;
- datasets candidatos `outputs`, `published` y `ops` en BigQuery `US`;
- una cuenta de servicio de ejecución administrada por el proyecto;
- acceso de lectura de la aplicación exclusivamente a `published` y creación de jobs de consulta;
- logging operativo, health, prueba positiva/negativa de acceso y rollback de práctica.

No se solicita autorización para buckets, GKE, Airflow, Agent Engine/Platform, acceso público,
microdatos, `raw`, `cleaned`, `analytical`, `survey_input`, publicación ni cutover.

## 3. Capa gratuita, límites de consumo y parada

El techo máximo de contingencia es **USD 20 al mes** y el gasto objetivo es **USD 0**. Esto permite
asumir el riesgo controlado de configuración y pruebas sin convertir el techo en meta de consumo.
PR B conecta localmente las 3.014 filas autorizadas; ninguna ha sido cargada en cloud. El diseño
previsto mantiene seis personas
usuarias. Artifact Registry puede generar un cargo pequeño e inevitable de centavos cuando la
imagen almacenada exceda 0.5 GiB; la alerta de USD 1 señala un gasto anómalo que sí requiere
investigación.

Controles obligatorios antes de habilitar tráfico:

- toda consulta, sin excepción, debe enviar `maximum_bytes_billed`; el valor inicial propuesto es
  **10 MiB (10,485,760 bytes) por consulta** y una consulta que lo exceda debe fallar cerrada;
- BigQuery debe tener una cuota diaria personalizada de consulta en el proyecto de **1 GiB por
  día**, que limita el máximo teórico mensual muy por debajo del 1 TiB gratuito;
- Cloud Run debe conservar `min-instances=0` y `max-instances=1`;
- Artifact Registry debe conservar **una sola imagen viva**. Tras validar la nueva revisión y su
  ventana de rollback, se elimina la imagen anterior; el historial de digest y la revisión de
  Cloud Run permanecen en auditoría;
- alertas de gasto real y previsto en **USD 1, 5, 10 y 20**.

Las alertas no detienen consumo. A USD 1 se congelan nuevas pruebas y se investiga la salida de la
capa gratuita. A USD 5 se detienen tráfico y consultas candidatas. USD 10 exige revisión conjunta
de billing/IAM antes de cualquier reanudación. USD 20 es el techo de contingencia: todo Stage 04
cloud permanece detenido hasta una nueva autorización. No se añaden Pub/Sub ni funciones de
parada, porque serían recursos fuera del alcance mínimo.

Referencia oficial: [presupuestos y alertas de Cloud Billing](https://docs.cloud.google.com/billing/docs/how-to/budgets).

## 4. IAM mínimo propuesto

No se usarán roles básicos `Owner` o `Editor`. Los bindings se aplicarán solo después de registrar
en privado los principales exactos y obtener GO.

| Principal | Alcance mínimo propuesto | Estado |
|---|---|---|
| Desplegadora (Ana; principal exacto privado) | `roles/run.developer` sobre Cloud Run, `roles/artifactregistry.writer` sobre el repositorio y `roles/iam.serviceAccountUser` sobre la identidad de ejecución | `PENDING_GO` |
| Identidad de ejecución de la app | `roles/bigquery.jobUser` en el proyecto y `roles/bigquery.dataViewer` solo sobre `published` | `PENDING_CREATION_AND_GO` |
| Revisora (Rita; principal exacto privado) | `roles/run.viewer`, `roles/logging.viewer` y `roles/monitoring.viewer` sobre el proyecto; sin propiedad ni administración de billing | `APPROVED_FOR_STAGE7_CONFIGURATION` |
| Personas usuarias | Ana, Rita y las etiquetas privadas `viewer_01`–`viewer_04`; las seis reciben solo `roles/run.invoker` para invocación autenticada. Los principales exactos se mantienen en el registro privado | `COMPOSITION_APPROVED; PRINCIPALS_PRIVATE` |

Google documenta que el despliegue de un contenedor requiere permisos sobre Cloud Run, lectura de
la imagen y capacidad de actuar como la identidad del servicio; Artifact Registry permite limitar
escritura al repositorio. Para BigQuery, `jobUser` crea jobs en el proyecto y `dataViewer` puede
otorgarse en el dataset o vista autorizada.

Referencias oficiales:

- [roles para desplegar en Cloud Run](https://docs.cloud.google.com/run/docs/reference/iam/roles);
- [control de acceso de Artifact Registry](https://docs.cloud.google.com/artifact-registry/docs/access-control);
- [roles IAM de BigQuery](https://docs.cloud.google.com/bigquery/docs/access-control).

## 5. Datos, acceso y rollback

- Solo se conectará el conjunto agregado ya autorizado y fijado por sus manifiestos SHA-256.
- El contenedor no recalcula estimadores ni consulta microdatos.
- La aplicación no fabrica cortes más finos que V0 ni cruces ausentes de los tabulados oficiales.
- CV alto y N reducido permanecen visibles con sus notas; no activan supresión por recuento.
- El servicio empieza autenticado y sin acceso público.
- La prueba IAM debe demostrar acceso positivo de una identidad autorizada y rechazo de una no
  autorizada, además de ausencia de lectura sobre capas previas a `published`.
- Rollback conserva la imagen y revisión anterior, restaura el release aprobado anterior y vuelve
  a ejecutar health, diagnóstico y prueba de acceso. No borra el historial.

## 6. Campos que deben resolverse antes del GO

| Gate | Estado actual | Evidencia requerida |
|---|---|---|
| Responsable real de billing | `ASIGNADO: ANA` | Ana confirma que la cuenta y el medio de pago son propios |
| Responsable real de IAM | `ASIGNADO: ANA; REVISIÓN: RITA` | Ana aplica o revoca; Rita revisa antes de cada binding; ninguna clave JSON |
| Cuenta de billing | `LINK_VERIFIED_PRIVATE` | identificador y medio de pago permanecen fuera del repositorio |
| Proyecto | `VERIFIED_PRIVATE` | ID exacto confirmado; número y propiedad permanecen en el registro privado |
| Seis identidades | `COMPOSITION_APPROVED` | Ana, Rita y `viewer_01`–`viewer_04`; los principales exactos se verifican solo por canal privado |
| Roles exactos de Rita | `VERIFIED_PRIVATE` | `run.viewer`, `logging.viewer` y `monitoring.viewer`; presencia y acceso efectivo confirmados |
| Condición de parada | `CONFIGURED` | PEN 67; umbrales 5/25/50/100 %, equivalentes aproximados a USD 1/5/10/20 |
| GO de Etapa 7 | `GO_FOR_STAGE7_CONTROLLED_SHADOW` | Aprobado el 2026-09-14 en la [revisión formal del PR #69](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/69#pullrequestreview-5203865560) |

El vínculo, el proyecto, el presupuesto, sus cuatro umbrales, el canal y los tres roles de Rita ya
fueron configurados y verificados privadamente. Las identidades exactas nunca se incorporan al
repositorio. La revisión aprobatoria del PR #116 mantuvo la creación de recursos, consultas,
cargas y cifras reales sujeta a la decisión separada del paso 47.

## 7. Decisión registrada

Rita registró `GO_FOR_STAGE7_CONTROLLED_SHADOW` el 2026-09-14. El GO no inicia por sí solo la Etapa
7: primero deben configurarse presupuesto, alertas y roles de lectura. La aclaración del
2026-09-17 mantiene USD 20 como techo máximo y USD 0 como gasto objetivo. La titularidad de Ana
corrige la propuesta histórica de administración compartida sin borrar esa evidencia.

Incluso con `GO_FOR_STAGE7_CONTROLLED_SHADOW`, el estado de publicación seguirá siendo
`NOT_AUTHORIZED`. Cada creación, binding y despliegue deberá quedar registrado con fecha UTC,
actor, recurso, configuración, coste observado y rollback.
