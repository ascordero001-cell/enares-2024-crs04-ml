# Objetivo de gasto cero con techo de contingencia — 2026-09-17

**Decisora y responsable económica:** Ana

**Techo máximo autorizado:** `USD 20/mes` para todo Stage 04

**Gasto objetivo:** `USD 0`

**Estado cloud:** `GO_FOR_STAGE7_CONTROLLED_SHADOW; BILLING_LINK_VERIFIED`

## Decisión

El techo máximo autorizado continúa siendo USD 20 mensuales. Este importe es un límite de
contingencia para la configuración y las pruebas controladas; no es una meta de consumo ni una
autorización para gastar sin control. El resultado económico buscado es terminar con gasto
efectivo de USD 0 mediante capa gratuita, límites técnicos y detención temprana.

El proyecto exacto `enares-2024-crs04` existe y su vínculo de facturación fue verificado de forma
privada. No se publican el número de proyecto, el identificador de la cuenta de facturación, el
medio de pago, correos ni principales IAM.

## Controles obligatorios

- presupuesto mensual de USD 20 con alertas equivalentes a USD 1, 5, 10 y 20;
- `maximum_bytes_billed=10,485,760` en cada consulta;
- cuota diaria personalizada de BigQuery de 1 GiB;
- Cloud Run con mínimo cero y máximo una instancia;
- una sola imagen viva en Artifact Registry después de la ventana de rollback;
- servicio autenticado y sin acceso público;
- ningún dato real en cloud antes del gate separado del paso 47;
- parada inmediata ante cualquier gasto no esperado.

Los presupuestos de Cloud Billing son alertas y no topes automáticos. El riesgo económico existe,
pero el objetivo operativo continúa siendo USD 0 y el techo absoluto de contingencia es USD 20.

## Alcance que permanece prohibido

No se autoriza publicación institucional, cutover, sustitución de V0, microdatos, búsquedas
individuales, cortes más finos que V0 ni cruces ausentes de los tabulados oficiales.
