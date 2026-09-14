# Solicitud de autorización cloud y GO — pasos 40 y 41

**Fecha:** 2026-09-14 UTC

**Estado de esta solicitud:** `SUBMITTED_FOR_SUPERVISORY_DECISION`

**Estado operativo mientras no exista respuesta formal:** `NO_GO / CLOUD_NOT_AUTHORIZED`

Esta solicitud no habilita servicios, billing ni IAM. Su aprobación permitiría iniciar únicamente
la Etapa 7 controlada en shadow, con los recursos y límites enumerados aquí. No autoriza
publicación institucional, cutover, sustitución de V0 ni nuevas cifras.

## 1. Evidencia previa del camino crítico

| Control | Evidencia | Resultado |
|---|---|---|
| Imagen construible | [Container CI del PR #68](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/34904684299) | `SUCCESS` |
| Aplicación dentro del contenedor | Inicio y respuesta HTTP en el mismo run | `SUCCESS` |
| Streamlit fijado | Verificación dentro de la imagen | `1.63.0` |
| Health superficial | `/_stcore/health` dentro del contenedor | `200 / ok` |
| Diagnóstico profundo | Manifiestos, release y módulos 3.1–3.6 | `SUCCESS` |
| Estado Docker | Healthcheck de la imagen | `healthy` |
| Regresión local | Suite con padre V0 privado | `396 passed; 0 failed` |

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

## 3. Presupuesto y parada

- Tope aprobado: **USD 20 por mes para todo Stage 04**, no por servicio.
- Alertas requeridas: USD 5, 10, 15 y 20, para gasto real y previsto cuando la plataforma lo
  permita.
- Las alertas no se describen como un límite automático: Google Cloud advierte que un presupuesto
  basado solo en alertas no detiene el consumo.
- A USD 15: se congelan nuevas revisiones/despliegues y las administradoras revisan el gasto.
- A USD 20 o ante gasto anómalo: se detienen tráfico y consultas de la Etapa 7 hasta decisión
  conjunta; no se elimina evidencia ni releases previos.
- No se añaden Pub/Sub ni funciones automáticas de parada en este gate, porque serían recursos
  adicionales no incluidos en el alcance mínimo.

Referencia oficial: [presupuestos y alertas de Cloud Billing](https://docs.cloud.google.com/billing/docs/how-to/budgets).

## 4. IAM mínimo propuesto

No se usarán roles básicos `Owner` o `Editor`. Los bindings se aplicarán solo después de registrar
en privado los principales exactos y obtener GO.

| Principal | Alcance mínimo propuesto | Estado |
|---|---|---|
| Desplegadora (Ana; principal exacto privado) | `roles/run.developer` sobre Cloud Run, `roles/artifactregistry.writer` sobre el repositorio y `roles/iam.serviceAccountUser` sobre la identidad de ejecución | `PENDING_GO` |
| Identidad de ejecución de la app | `roles/bigquery.jobUser` en el proyecto y `roles/bigquery.dataViewer` solo sobre `published` | `PENDING_CREATION_AND_GO` |
| Revisora (Rita; principal exacto privado) | Visibilidad de servicio, logs, gasto y políticas necesaria para verificar; roles exactos sujetos a revisión antes del binding | `PENDING_SUPERVISORY_CONFIRMATION` |
| Seis personas usuarias | Solo invocación autenticada del servicio; lista y principales se mantienen fuera del repositorio | `PENDING_PRIVATE_LIST_AND_GO` |

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
| Responsable real de billing | `PENDIENTE / NO ASIGNADO` | confirmación privada del principal y capacidad de recuperación |
| Responsable real de IAM | `PENDIENTE / NO ASIGNADO` | confirmación privada del principal que aplicará/revocará bindings |
| Cuenta de billing | `PENDING` | identificador verificado en canal privado y vínculo con el proyecto |
| Proyecto | `PENDING_VERIFICATION` | ID/número y propiedad verificados |
| Seis identidades | `PENDING_PRIVATE_LIST` | lista privada, autenticación y procedimiento de revocación |
| Roles exactos de Rita | `PENDING_SUPERVISORY_CONFIRMATION` | decisión de mínimo privilegio |
| Condición de parada | `PROPOSED` | responsable ejecutor y prueba supervisada |
| GO de Etapa 7 | `PENDING` | revisión formal sobre este paquete |

Ana y Rita están designadas como administradoras del presupuesto y del proceso, pero esa
designación no se convierte aquí en una asignación inventada de responsabilidades de billing o
IAM. Esos dos campos bloquean el GO hasta su confirmación explícita.

## 7. Decisión solicitada a Rita

Registrar una de estas decisiones sobre el SHA revisado:

- `GO_FOR_STAGE7_CONTROLLED_SHADOW`, una vez completados todos los campos bloqueantes;
- `CHANGES_REQUIRED`, enumerando los ajustes;
- `NO_GO`, manteniendo el alcance local.

Incluso con `GO_FOR_STAGE7_CONTROLLED_SHADOW`, el estado de publicación seguirá siendo
`NOT_AUTHORIZED`. Cada creación, binding y despliegue deberá quedar registrado con fecha UTC,
actor, recurso, configuración, coste observado y rollback.
