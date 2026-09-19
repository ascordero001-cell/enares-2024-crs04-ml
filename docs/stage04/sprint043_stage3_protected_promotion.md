# Sprint 04.3 — promoción shadow protegida

- Fecha: 2026-09-19
- Issue núcleo: #45
- Estado: `IMPLEMENTED; NOT_EXECUTED`
- Alcance: pasos 10–11 después de una decisión humana del paso 9

## Decisión humana preservada

El workflow `stage04-shadow-promote.yml` no contiene una decisión de promoción. Solo puede
ejecutarse desde `main`, bajo el Environment `stage04-shadow-mutation`, y exige un JSON versionado
en `docs/stage04/decisions/` dentro de un commit ancestro del commit despachado. El contrato debe
coincidir exactamente con release, run, SHA-256 y corrida de reconciliación; debe estar aprobado
por `ritaricaldi-cpu`, negar acceso público y negar cutover.

La revisión y fusión de este código no crea ese JSON, no concede la decisión y no dispara el
workflow. La autorización `APPROVE_AUTHENTICATED_SHADOW_PROMOTION` continúa siendo exclusivamente
humana y trazable.

## Ejecución técnica automatizada

Después de recibir esa decisión, el job protegido:

1. vuelve a exigir 3.014 filas, 516 indicadores, el SHA-256 exacto, una sola entrada `APPROVED` y
   los cinco gates de reconciliación en `PASS`;
2. deja primero la vista publicada vacía, actualiza el puntero en una transacción idempotente y
   recrea la vista fijada literalmente al release/run aprobado;
3. comprueba paridad de identidad, hash y conteos, y registra un evento idempotente conservando el
   puntero anterior;
4. reutiliza la imagen actual fijada por digest para crear una revisión Cloud Run sin tráfico;
5. exige acceso anónimo `403`, health autenticado `200`, cero principals públicos, mínimo cero,
   máximo una instancia y concurrencia seis;
6. mueve el 100 % del tráfico únicamente después de validar la candidata y repite las
   comprobaciones sobre el servicio final;
7. guarda artifacts redactados durante siete días.

Todas las consultas BigQuery usan cache desactivada y el techo existente de 10 MiB. El flujo opera
solo sobre el snapshot ya reconciliado; no carga datos, no crea una release y no modifica IAM.

## Límites invariables

El resultado continúa siendo `CONTROLLED_SHADOW`: sin acceso público, publicación institucional,
cutover, sustitución de V0 ni aumento del techo mensual. Un contrato ausente o discordante, un gate
incompleto, una diferencia de paridad o una verificación de acceso fallida detiene el job.
