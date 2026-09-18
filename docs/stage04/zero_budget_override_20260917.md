# Decisión operativa de presupuesto cero — 2026-09-17

**Decisora y responsable económica:** Ana

**Presupuesto operativo vigente:** `USD 0` estricto

**Estado cloud:** `BILLING_LINK_VERIFIED; ZERO_BUDGET_HARD_STOP`

**Alcance:** verificación y documentación; sin ejecución cloud

## Decisión

Desde el 2026-09-17, el límite operativo autorizado para Stage 04 es `USD 0`. Esta decisión más
restrictiva deja sin efecto operativo el margen histórico de contingencia de USD 20/mes mientras
no exista una nueva autorización explícita. Las actas y revisiones históricas se conservan sin
reescritura para mantener la trazabilidad.

El proyecto exacto `enares-2024-crs04` existe y su vínculo de facturación fue verificado de forma
privada. No se publican el número de proyecto, el identificador de la cuenta de facturación, el
medio de pago, correos ni principales IAM.

## Efecto obligatorio

Un presupuesto de Cloud Billing es una alerta y no un límite automático de gasto. Por ello, el
límite estricto `USD 0` se aplica como condición de parada previa a cualquier operación:

- no se habilitan APIs adicionales;
- no se crean ni modifican recursos cloud;
- no se construyen ni publican imágenes en cloud;
- no se despliega Cloud Run;
- no se crean datasets, tablas, buckets, repositorios ni cuentas de servicio;
- no se cargan cifras reales ni fixtures sintéticos;
- no se ejecutan consultas o pruebas que puedan generar consumo;
- no se modifican bindings IAM como parte de una secuencia de despliegue bloqueada.

Los pasos 43–49 de la Etapa 7 permanecen bloqueados por `ZERO_BUDGET_HARD_STOP`. El vínculo de
facturación, por sí solo, no levanta el gate ni autoriza gasto, despliegue, publicación, cutover o
sustitución de V0.

## Condición para reabrir el carril cloud

Se requiere una decisión nueva y explícita que autorice un importe positivo, restablezca los
controles de coste y alertas, complete IAM y confirme el orden de ejecución. Hasta entonces solo
continúan el trabajo local, las pruebas sin consumo cloud, la documentación y la revisión del
paquete de cierre.
