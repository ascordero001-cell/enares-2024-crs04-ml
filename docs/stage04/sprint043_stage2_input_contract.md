# Sprint 04.3 — Etapa 2: contrato ejecutable de entrada

- Fecha: 2026-09-19
- Issue núcleo: #45
- Decisión supervisora: [Issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5738454716)
- Estado: `IMPLEMENTED_PREPARATION; BLOCKED_TRANSPORT`

## Decisión aplicada

Cada agregado futuro se autoriza manualmente por corrida. Antes de ejecutar, Ana verifica
procedencia, SHA-256 y manifiesto. Rita es la única revisora requerida del Environment que
proteja cualquier job que mute cloud y se debe activar `prevent self-review`.

No se autoriza bucket, dataset de tránsito, cuenta de servicio nueva, credencial permanente de
CI, descarga automática ni sincronización con Drive. La evidencia generada omite filas, rutas
privadas, principales, credenciales e identificadores de jobs.

## Límite comprobado de la plataforma

`workflow_dispatch` acepta texto, opciones, booleanos y environments; no acepta archivos. Por
ello, la decisión de «adjuntar el archivo al disparar» no puede materializarse directamente en un
runner hospedado por GitHub. El workflow no sustituye ese canal por artifacts previos, Releases,
URLs, secretos, commits, buckets ni Drive: exige que el agregado y su manifiesto ya estén en
`$RUNNER_TEMP/stage04-private-input` y falla cerrado cuando no están.

La preparación ejecutable queda lista, pero el workflow no puede pasar ese punto en un runner
hospedado hasta que se apruebe cómo materializar ambos archivos efímeros. Esta limitación no se
presenta como implementación completa del paso 4.

## Controles ejecutados

`prepare_stage04_shadow_run.py`:

1. valida release/run, hashes, URL de decisión y commit exacto;
2. rechaza identidades reservadas;
3. verifica SHA-256 del agregado y del manifiesto;
4. enlaza el manifiesto al padre V0 y a los conteos aprobados;
5. usa `AuthorizedAggregateRepository`, que deriva `synthetic=false` por procedencia;
6. usa `validate_estimates`, incluida la frontera de granularidad V0;
7. comprueba 3.014 filas, 516 indicadores, seis módulos y estado `APPROVED`;
8. genera únicamente evidencia JSON/Markdown redactada;
9. termina antes de carga, consulta, promoción, rollback, IAM, tráfico o publicación.

## Próximo gate

Rita debe aprobar un mecanismo técnicamente realizable para colocar el agregado y el manifiesto
en el directorio efímero de la corrida. Después se podrá añadir el job cloud bajo Environment
protegido, con Rita como única revisora y `prevent self-review`, conservando separados los gates
de carga y promoción.

La consulta de configuración realizada el 2026-09-19 no encontró un Environment existente en el
repositorio. Este PR no lo crea porque su único job termina antes de cualquier mutación cloud; el
Environment se configura y verifica antes de añadir el primer job que cargue o promueva datos.
