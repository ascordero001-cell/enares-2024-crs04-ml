# Sprint 04.3 — gate de reconciliación cloud existente

- Fecha: 2026-09-19
- Issue núcleo: #45
- Estado: `IMPLEMENTED; NOT_EXECUTED`
- Modo único: `RECONCILE_EXISTING`

## Environment aplicado al job específico

El workflow manual `stage04-shadow-reconcile.yml` contiene un único job con acceso cloud,
`reconcile-existing`, y ese mismo job declara explícitamente:

```yaml
environment:
  name: stage04-shadow-mutation
```

El Environment está configurado externamente con Rita como única revisora requerida,
`prevent_self_review=true` y política de rama limitada a `main`. El workflow añade además una
condición ejecutable `github.ref == 'refs/heads/main'`. Por tanto, el runner y los hooks no reciben
el trabajo ni la copia privada hasta que GitHub registre la aprobación del deployment.

## Alcance ejecutable

La primera corrida automatizada solo puede:

1. recibir la copia local por los hooks ya aprobados;
2. volver a validar hashes, manifiesto, registro V0, 3.014 filas y 516 indicadores;
3. consultar la tabla existente con parámetros, cache desactivada y 10 MiB máximos por consulta;
4. comparar los 31 campos con tolerancia `1e-9` solo para valores flotantes;
5. exigir los cinco gates `PASS` y los bytes previamente observados;
6. subir exclusivamente evidencia redactada.

No existe una llamada de carga. Tampoco ejecuta promoción, rollback, IAM, tráfico, publicación,
cutover ni creación de recursos. Cualquier diferencia de contenido, conteo, cache, cap o bytes
produce `HOLD` y salida distinta de cero. El artifact se intenta subir incluso en `HOLD` para que
Rita pueda revisar la causa sin exponer filas, rutas, principals o identificadores de jobs.

## Condición para ejecutar

Fusionar este código no inicia el workflow. Después del merge todavía se requieren, en orden:

1. copia privada colocada manualmente en el inbox local aprobado;
2. dispatch desde `main` con el contrato inmutable ya aprobado;
3. aprobación de Rita mediante **Review deployments → Approve and deploy**.

Hasta completar esas tres condiciones el estado continúa `NOT_EXECUTED`.
