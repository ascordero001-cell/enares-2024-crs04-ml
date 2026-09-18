# Evidencia de ejecución sintética de Etapa 7 — 2026-09-18

**Estado:** `TECHNICAL_PASS; SUPERVISORY_ACCESS_VERIFICATION_PENDING`

**Alcance:** Decisión A `SYNTHETIC_INFRA_ONLY`. La Decisión B para cifras V0 reales continúa
`BLOCKED`.

Los principales exactos, IDs internos, URL autenticada, digest completo y tokens permanecen en el
registro privado. Ninguna cifra V0 fue cargada, consultada o incorporada a la imagen.

## Registro de acciones

| Fecha UTC | Actor | Acción y recurso lógico | Resultado |
|---|---|---|---|
| 2026-09-18T04:08:24Z | Ana | Habilitar APIs aprobadas de Artifact Registry, Cloud Run e IAM | `SUCCESS` |
| 2026-09-18T04:09:03Z | Ana | Crear tres datasets `stage04_shadow` aislados en BigQuery `US` | `SUCCESS; 3/3 VACÍOS` |
| 2026-09-18T04:09:56Z | Ana | Crear identidad de ejecución y repositorio Docker inmutable | `SUCCESS; 0 LLAVES` |
| 2026-09-18T04:11:25Z | Ana | Aplicar `jobUser` y lectura limitada al `published` aislado | `SUCCESS` |
| 2026-09-18T04:12:01Z | Ana | Fijar cuota diaria de consultas BigQuery en 1 GiB | `SUCCESS` |
| 2026-09-18T04:23:08Z | Ana | Subir una imagen sintética verificada por digest | `SUCCESS; 1 IMAGEN` |
| 2026-09-18T04:24:51Z | Ana | Desplegar Cloud Run autenticado, min=0 y max=1 | `SUCCESS` |
| 2026-09-18T04:25:32Z | Ana | Conceder invocación a dos principales privados verificados | `SUCCESS; SIN ACCESO PÚBLICO` |
| 2026-09-18T04:26:03Z | Ana | Probar acceso anónimo y autenticado | `403 / 200; HEALTH OK` |
| 2026-09-18T04:26Z | Ana | Ejecutar seis contextos Playwright concurrentes | `6/6 PASS; 0 ERRORES` |
| 2026-09-18T04:27:51Z | Ana | Crear revisión de práctica y ejecutar rollback | `PASS; TRÁFICO RESTAURADO` |
| 2026-09-18T04:28:33Z | Ana | Consultar métricas, logs y escalado | `MAX 1 INSTANCIA; 0 ERRORES` |

## Separación de datos demostrada

- La imagen copia únicamente la navegación C0, el generador del catálogo sintético y el health.
- `app/data`, manifiestos V0, repositorios institucionales y adaptadores autorizados no existen en
  la imagen.
- El diagnóstico exige exactamente 516 localizadores, seis módulos y `synthetic=true` en todos.
- Los datasets aislados `outputs`, `published` y `ops` permanecen vacíos.
- Los datasets preexistentes permanecen intactos con sus conteos anteriores de 1 y 32 tablas; no
  se leyó contenido, no se modificó IAM y no se ejecutó ninguna acción sobre ellos.

## Controles y resultados

| Control | Resultado |
|---|---|
| Imagen inmutable | una imagen viva, desplegada por digest |
| Autenticación | solicitud anónima `403`; solicitud autorizada `200` |
| Escalado | mínimo 0 por defecto; máximo 1 configurado; máximo observado 1 |
| Concurrencia | seis contextos, seis respuestas `200`, cero errores de página |
| Health | `200 / ok` |
| Logs | cero entradas con severidad `ERROR` durante la ventana |
| Rollback | revisión de práctica saludable; tráfico restaurado al 100 % a la revisión previa |
| BigQuery | tres datasets vacíos; cuota diaria 1 GiB; cero consultas y cero cargas |
| Credenciales | identidad sin llaves; login efímero y archivos temporales eliminados |
| Coste | pendiente de latencia de facturación; ninguna alerta recibida durante la ejecución |

## Pendientes antes de declarar PASS supervisor

- Rita confirma privadamente que puede invocar la aplicación y consultar logs/métricas.
- Se completan o se retiran formalmente los cuatro principales de reserva antes del cierre de
  AC-01.
- Se prueba una identidad autenticada sin autorización y una revocación controlada.
- `maximum_bytes_billed=10,485,760` continúa como condición obligatoria antes de cualquier consulta;
  no se ejecutó porque la Decisión A no conecta BigQuery a la aplicación.

Este resultado no autoriza cifras reales, publicación institucional, cutover ni sustitución de V0.
