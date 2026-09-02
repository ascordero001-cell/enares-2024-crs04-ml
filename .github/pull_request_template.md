## Objetivo

Describir el cambio y el issue que resuelve.

Closes #

## Estado

- [ ] `SHADOW/PREPARING`
- [ ] No presenta V0.5 como publicación oficial.
- [ ] No autoriza cutover ni gasto cloud.

## Cambios

-

## Validación

- [ ] `python -m pytest tests/test_naming.py -q`
- [ ] `python -m pytest -q`
- [ ] CI `Python tests` en verde.
- [ ] CI `Dataform compile` en verde.
- [ ] Diff completo revisado.

## Datos, seguridad y privacidad

- [ ] No contiene `.sav`, microdatos ni exports reales.
- [ ] No contiene credenciales, tokens o claves JSON.
- [ ] No contiene rutas personales.
- [ ] Los fixtures incluidos son sintéticos y están documentados.
- [ ] Los CSV/JSON permitidos tienen manifest y SHA-256 cuando corresponde.

## Revisión

- [ ] Revisora independiente asignada.
- [ ] Conversaciones resueltas.
- [ ] Evidencia y documentación actualizadas.

## Rollback

Describir cómo revertir este cambio sin modificar V0 ni perder el historial.
