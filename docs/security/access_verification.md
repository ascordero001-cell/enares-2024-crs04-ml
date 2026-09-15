# Verificación efectiva de acceso — plantilla Stage 04

- Estado: `TEMPLATE_READY; NOT_EXECUTED`
- Release candidato: `<release_id>`
- Revisión de aplicación: `<container_digest / Cloud Run revision>`
- Fecha UTC: `<timestamp>`
- Ejecutora: Ana
- Revisora: Rita

Los principales, correos, tokens, IDs internos y capturas que los revelen se guardan únicamente en
el registro privado. En el repositorio se anotan roles, resultado, timestamp y referencias
redactadas.

## Precondiciones

- [ ] Proyecto y cuenta de billing confirmados privadamente con Rita.
- [ ] GO `GO_FOR_STAGE7_CONTROLLED_SHADOW` vigente.
- [ ] Servicio autenticado sin `allUsers` ni `allAuthenticatedUsers`.
- [ ] Revisión y digest de imagen registrados.
- [ ] Release único aprobado y diagnóstico profundo correcto.
- [ ] Plan de rollback listo.

## Cinco escenarios obligatorios

| ID | Escenario | Resultado esperado | Evidencia redactada | Resultado |
|---|---|---|---|---|
| AC-01 | Las seis identidades autorizadas ingresan | Cada principal obtiene acceso a la aplicación autenticada | timestamp, cargo, revisión y código de resultado; principal solo en registro privado | `PENDING` |
| AC-02 | Identidad autenticada no autorizada y solicitud anónima | Ambas reciben denegación y ninguna cifra o descarga | código de resultado y ruta probada, sin token ni correo | `PENDING` |
| AC-03 | Revocación de una identidad de prueba | Tras retirar `run.invoker`, el mismo principal pierde acceso | binding retirado, timestamp y prueba negativa | `PENDING` |
| AC-04 | Rutas y descargas directas | Ninguna ruta, archivo o exportación elude autenticación | lista de rutas probadas y resultados redactados | `PENDING` |
| AC-05 | Identidad de ejecución de la app | Lee `published`; falla al leer cualquier capa previa | consultas sintéticas/mínimas, bytes procesados y denegaciones | `PENDING` |

## Controles adicionales

- [ ] `maximum_bytes_billed=10,485,760` aplicado en toda consulta.
- [ ] Cuota personalizada BigQuery de 1 GiB/día verificada.
- [ ] Cloud Run conserva min=0, max=1 y acceso público deshabilitado.
- [ ] Rita conserva únicamente roles de visualización aprobados.
- [ ] No existen claves JSON ni secretos descargados.
- [ ] Logs y health no exponen cifras, principales ni configuración privada.
- [ ] Coste observado y previsión permanecen dentro de los escalones aprobados.

## Cierre de la verificación

- Decisión: `PASS | FAIL | BLOCKED`
- Hallazgos: `<resumen sin información privada>`
- Acción correctiva o rollback: `<referencia>`
- Evidencia privada: `<referencia no sensible al registro custodio>`
- Aprobación de Rita: `<enlace o referencia de revisión>`

Un `FAIL` o permiso inesperado detiene la Etapa 7. Un `PASS` valida el acceso controlled shadow,
pero no autoriza publicación institucional, cutover ni sustitución de V0.
