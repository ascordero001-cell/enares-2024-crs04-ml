# Sprint 04.3 — Etapa 2: contrato ejecutable de entrada

- Fecha: 2026-09-19
- Issue núcleo: #45
- Decisión supervisora: [Issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43#issuecomment-5738454716)
- Estado: `IMPLEMENTED_PREPARATION; SELF_HOSTED_TRANSPORT_CONFIGURED`

## Decisión aplicada

Cada agregado futuro se autoriza manualmente por corrida. Antes de ejecutar, Ana verifica
procedencia, SHA-256 y manifiesto. Rita es la única revisora requerida del Environment que
proteja cualquier job que mute cloud y se debe activar `prevent self-review`.

No se autoriza bucket, dataset de tránsito, cuenta de servicio nueva, credencial permanente de
CI, descarga automática ni sincronización con Drive. La evidencia generada omite filas, rutas
privadas, principales, credenciales e identificadores de jobs.

## Límite comprobado de la plataforma

`workflow_dispatch` acepta texto, opciones, booleanos y environments; no acepta archivos. Rita
resolvió este límite en la revisión del PR #130 autorizando exclusivamente un runner autoalojado
en la máquina de Ana. El workflow requiere las etiquetas `self-hosted`, `Windows`, `X64` y
`stage04-private-input`; ya no puede caer en un runner hospedado por GitHub.

GitHub vacía `RUNNER_TEMP` al inicio y al final de cada job. Por eso, una copia colocada allí antes
del disparo se perdería. El runner usa un inbox local privado y un hook de inicio: después de la
limpieza automática, el hook valida que existan `aggregate.csv` y `manifest.json`, conserva para
el CSV el nombre seguro declarado en el manifiesto y copia ambos a
`RUNNER_TEMP/stage04-private-input`. Un hook de finalización elimina las copias del inbox y del
directorio temporal. Los hooks auditables están en `scripts/runner_hooks/`.

No se usa artifact previo, Release, URL, secreto, bucket, commit de datos ni sincronización con
Drive. El archivo privado permanece en la máquina autoalojada y solo la evidencia redactada puede
subirse como artifact.

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

El runner de repositorio `enares-stage04-local` quedó registrado con la etiqueta exclusiva y el
Environment `stage04-shadow-mutation` quedó configurado para `main`, con Rita como única revisora
requerida y `prevent self-review` activo. El workflow de este PR todavía termina antes de toda
mutación cloud y por eso no consume el Environment.

El próximo gate es una corrida supervisada de preparación con una copia del agregado autorizado.
Solo después de revisar su evidencia se añadirá un job separado de carga/reconciliación que use el
Environment protegido. Promoción y rollback conservarán decisiones humanas distintas.
