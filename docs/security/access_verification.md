# Verificación efectiva de acceso — plantilla Stage 04

- Estado: `CLOSED; PASS_SUPERVISOR`
- Release candidato: `stage04-synthetic-shadow-20260918`
- Revisión de aplicación: registrada por digest y revisión en el registro privado
- Fecha UTC: `2026-09-18T04:26:03Z`
- Ejecutora: Ana
- Revisora: Rita

Los principales, correos, tokens, IDs internos y capturas que los revelen se guardan únicamente en
el registro privado. En el repositorio se anotan roles, resultado, timestamp y referencias
redactadas.

## Precondiciones

- [x] Ana confirma proyecto, cuenta de billing, vínculo y medio de pago; Rita revisa privadamente
      la evidencia.
- [x] GO `GO_FOR_STAGE7_CONTROLLED_SHADOW` vigente.
- [x] Servicio autenticado sin `allUsers` ni `allAuthenticatedUsers`.
- [x] Revisión y digest de imagen registrados privadamente.
- [x] Imagen única sintética y diagnóstico de 516 localizadores correcto.
- [x] Rollback de práctica ejecutado y tráfico restaurado a la revisión anterior.

## Cinco escenarios obligatorios

| ID | Escenario | Resultado esperado | Evidencia redactada | Resultado |
|---|---|---|---|---|
| AC-01 | Identidades autorizadas vigentes ingresan | Cada principal configurado obtiene acceso a la aplicación autenticada | Ana y Rita `PASS`; cuatro reservas retiradas formalmente para este cierre | `PASS` |
| AC-02 | Identidad autenticada no autorizada y solicitud anónima | Ambas reciben denegación y ninguna cifra o descarga | solicitud anónima `403`; identidad real no autorizada diferida | `PASS_CURRENT_SCOPE` |
| AC-03 | Revocación de una identidad de prueba | Tras retirar `run.invoker`, el mismo principal pierde acceso | diferida hasta disponer de una identidad real de prueba | `DEFERRED_NON_BLOCKING` |
| AC-04 | Rutas y descargas directas | Ninguna ruta, archivo o exportación elude autenticación | raíz y health autenticados `200`; payload institucional ausente de la imagen | `PASS_SYNTHETIC_SCOPE` |
| AC-05 | Identidad de ejecución de la app | Lee `published`; falla al leer cualquier capa previa | consultas sintéticas/mínimas, bytes procesados y denegaciones | `PENDING` |

## Controles adicionales

- [ ] `maximum_bytes_billed=10,485,760` aplicado en toda consulta.
- [x] Cuota personalizada BigQuery de 1 GiB/día verificada.
- [x] Cloud Run conserva min=0, max=1 y acceso público deshabilitado.
- [x] Rita conserva los tres roles de visualización y `run.invoker` sobre el servicio.
- [x] No existen claves JSON ni secretos descargados.
- [x] Logs y health no exponen cifras, principales ni configuración privada.
- [ ] Coste observado y previsión permanecen dentro de los escalones aprobados.

## Cierre de la verificación

- Decisión: `PASS_SUPERVISOR; DECISION_A_CLOSED`
- Hallazgos: seis sesiones automatizadas `PASS`; acceso público denegado; Ana y Rita verificadas; cero errores de aplicación
- Acción correctiva o rollback: rollback de práctica `PASS`; tráfico restaurado a la revisión previa
- Evidencia privada: `<referencia no sensible al registro custodio>`
- Aprobación de Rita: revisión formal del PR #119

Un `FAIL` o permiso inesperado detiene la Etapa 7. Un `PASS` valida el acceso controlled shadow,
pero no autoriza publicación institucional, cutover ni sustitución de V0.
