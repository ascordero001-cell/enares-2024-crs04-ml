# Verificación del presupuesto cloud — 2026-09-17

**Proyecto:** `enares-2024-crs04`

**Estado:** `BUDGET_AND_NOTIFICATION_CONFIGURED; PRIVATE_RECEIPT_CONFIRMED`

**Gasto objetivo:** USD 0

**Techo máximo autorizado:** USD 20/mes

## Configuración aplicada

La cuenta de facturación opera en soles. Para conservar un techo igual o inferior a USD 20 se
configuró un presupuesto mensual de **PEN 67**, filtrado únicamente al proyecto Stage 04.

La conversión usa como referencia el tipo de cambio interbancario de venta del BCRP del
2026-09-16: **S/ 3.3667142857 por USD**. PEN 67 equivalen aproximadamente a USD 19.90 y, por
tanto, no exceden el techo aprobado.

| Umbral | Importe en PEN | Equivalencia aproximada |
|---|---:|---:|
| 5 % | S/ 3.35 | USD 1 |
| 25 % | S/ 16.75 | USD 5 |
| 50 % | S/ 33.50 | USD 10 |
| 100 % | S/ 67.00 | USD 19.90 |

Referencia oficial del tipo de cambio: [BCRP, serie diaria interbancaria de venta](https://estadisticas.bcrp.gob.pe/estadisticas/series/diarias/resultados/PD04638PD).

## Verificación redactada

- vínculo de facturación del proyecto: activo;
- Cloud Billing Budget API: habilitada;
- número de presupuestos Stage 04: uno;
- filtro de proyecto: una coincidencia, el proyecto exacto Stage 04;
- moneda: PEN;
- umbrales de gasto real: 5 %, 25 %, 50 % y 100 %;
- destinatarios IAM predeterminados: habilitados;
- canal específico de la supervisora: creado y vinculado al presupuesto;
- identificadores de billing, presupuesto y proyecto: conservados solo en el registro privado.

## Confirmación privada

Rita confirmó la recepción del canal y el funcionamiento efectivo de sus roles de lectura en la
[revisión aprobatoria del PR #116](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/116#pullrequestreview-5243890667).
El principal y el identificador del canal no se publican. La confirmación cierra este control, pero
no autoriza por sí sola crear recursos: esa misma revisión conserva ese punto dentro del gate del
paso 47.

Un presupuesto de Cloud Billing genera alertas, no un corte automático. La configuración busca
terminar con gasto USD 0; cualquier gasto inesperado activa la parada descrita en el runbook.
