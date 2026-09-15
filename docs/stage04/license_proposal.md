# Stage 04 — propuesta de licencia

**Estado:** `APPROVED_AND_APPLIED`

**Fecha:** 2026-09-15 UTC

La decisión fue aprobada por `ritaricaldi-cpu` sobre el SHA
`c4b28161523e3ee52a44343ecadd5b26e2ad5042` en la
[revisión formal del PR #87](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/87#pullrequestreview-5205393361).
La licencia no otorga derechos sobre datos o materiales de terceros.

## Recomendación

Se adopta **Apache License 2.0** (`Apache-2.0`) exclusivamente para el software original del
repositorio y la documentación técnica original cuya titularidad permita licenciarla. Es una
licencia permisiva que exige conservar avisos, incluye una concesión expresa de patentes y excluye
garantías y uso de marcas.

Este mismo PR incorpora el texto oficial sin modificaciones en `LICENSE` y un `NOTICE` con el
alcance, el titular y las exclusiones aprobadas.

## Alcance aprobado

Incluido:

- código original en `src/`, `app/` y `scripts/`;
- definiciones originales en `dataform/` y `sql/`;
- pruebas y fixtures completamente sintéticos;
- documentación técnica original creada para este repositorio, incluidos contratos, actas de
  decisión y registros supervisores, runbooks, matrices de cobertura y evidencia de ingeniería.

Excluido expresamente:

- microdatos y agregados ENARES, diccionarios, tabulados, instrumentos y demás materiales del
  INEI, incluso si alguna evidencia autorizada se encuentra versionada;
- documentos, contenidos, logotipos y marcas de cualquier institución tercera;
- nombres, emblemas y marcas del INEI y de terceros;
- dependencias y componentes de terceros, que conservan sus propias licencias;
- cualquier material cuya titularidad o permiso de redistribución no esté confirmado.

La disponibilidad pública de un archivo no se interpretará como autorización para relicenciarlo.

## Atribución aprobada

El `NOTICE` identifica el proyecto como “ENARES 2024 CRS04 — software Stage 04” y declara que
Apache-2.0 cubre únicamente el software y material original enumerado. También repite las
exclusiones de datos, instrumentos, contenidos institucionales y marcas.

La línea aprobada es: `Copyright 2026 Ana Silvia Cordero Ricaldi`.

## Decisiones resueltas

1. `Apache-2.0`: aprobada.
2. Titular: `Ana Silvia Cordero Ricaldi`.
3. Documentación original: incluida con el alcance descrito arriba; cualquier documento mixto o
   cercano a materiales de terceros permanece excluido hasta consulta específica.
4. Atribuciones institucionales adicionales: ninguna. Las dependencias conservan sus licencias;
   solo se añadirá un aviso futuro si una dependencia lo exige expresamente.

La cita de fuente se definirá en una decisión posterior y no forma parte del `NOTICE` actual.

## Referencias normativas

- Texto oficial: <https://www.apache.org/licenses/LICENSE-2.0.txt>
- Guía oficial de aplicación: <https://www.apache.org/legal/apply-license>
