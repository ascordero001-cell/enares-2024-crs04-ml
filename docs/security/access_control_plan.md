# Plan de control de acceso — Stage 04

- Estado: `PLAN_READY; EXECUTION_PENDING_PRIVATE_VERIFICATION`
- Alcance autorizado: `GO_FOR_STAGE7_CONTROLLED_SHADOW`
- Publicación institucional: `NOT_AUTHORIZED`
- Responsabilidades: Ana es propietaria, operadora y responsable de billing; Rita supervisa en
  modo de solo lectura antes de cada binding

No se ejecutará ninguna configuración hasta verificar por canal privado el proyecto y la cuenta de
billing. Este documento no contiene correos, principales exactos, identificadores de billing ni
credenciales.

## Mecanismo de autenticación

La aplicación se desplegará en Cloud Run con autenticación obligatoria y sin bindings para
`allUsers` ni `allAuthenticatedUsers`. El acceso se concederá mediante `roles/run.invoker` sobre el
servicio únicamente a las seis identidades aprobadas: Ana, Rita y las etiquetas privadas
`viewer_01`–`viewer_04`. Los principales exactos se conservan y verifican fuera del repositorio.

Todas las rutas de la aplicación, archivos estáticos y descargas deben quedar detrás del mismo
control. No se autoriza una URL pública alternativa, un bucket público ni un enlace de exportación
que eluda Cloud Run IAM.

## Roles mínimos

| Sujeto | Roles y alcance | Restricción |
|---|---|---|
| Seis personas usuarias | `roles/run.invoker` solo sobre el servicio | Sin acceso directo a BigQuery ni Artifact Registry |
| Ana, despliegue | `roles/run.developer` sobre Cloud Run, `roles/artifactregistry.writer` sobre el repositorio y `roles/iam.serviceAccountUser` sobre la identidad de ejecución | Aplica o revoca; cada binding es revisado por Rita |
| Identidad de ejecución | `roles/bigquery.jobUser` en el proyecto y `roles/bigquery.dataViewer` solo sobre `published` | Sin lectura de `raw`, `cleaned`, `analytical` ni `survey_input` |
| Rita, supervisión de solo lectura | `roles/run.viewer`, `roles/logging.viewer` y `roles/monitoring.viewer` sobre el proyecto | Sin permisos de modificación ni administración de billing |

No se usarán roles básicos `Owner` o `Editor`, claves JSON ni credenciales dentro del repositorio,
la imagen, variables de ejemplo, logs o capturas.

## Alta, baja y revocación

1. Ana confirma por canal privado el principal exacto; Rita revisa la evidencia sin asumir su administración.
2. Ana aplica el binding mínimo sobre el servicio y registra fecha UTC, actor, alcance y resultado.
3. Rita revisa el binding antes de la prueba de acceso.
4. Una baja elimina `run.invoker`; la verificación negativa debe demostrar que el acceso dejó de
   funcionar.
5. Una sustitución de las dos reservas se registra como baja y alta separadas, nunca reutilizando
   una identidad.

Ante un permiso inesperado, acceso anónimo, lectura fuera de `published` o descarga directa sin
autenticación, se detienen las pruebas, se revoca el binding afectado y se conserva evidencia para
rollback. Ningún resultado se publica durante esta verificación.

## Protección de canales

- UI, rutas directas, health detallado y descargas: autenticación obligatoria.
- Health superficial: no revela cifras, identidades, configuración ni procedencia privada.
- Exportación: solo datos ya autorizados y visibles; mismas alertas de CV/N y misma granularidad.
- Caché: clave por `release_id` y `run_id`; nunca mezcla releases.
- Logs y errores: taxonomía estable sin filas, cifras, tokens ni principales exactos.

La evidencia posterior al GO se captura con [access_verification.md](access_verification.md).
