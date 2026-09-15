# Stage 04 — propuesta de licencia

**Estado:** PENDING_SUPERVISORY_DECISION

**Fecha:** 2026-09-15 UTC

Este documento presenta una propuesta para revisión. No incorpora una licencia al repositorio ni
otorga derechos sobre datos o materiales de terceros.

## Recomendación

Adoptar **Apache License 2.0** (`Apache-2.0`) exclusivamente para el software original del
repositorio y la documentación técnica original cuya titularidad permita licenciarla. Es una
licencia permisiva que exige conservar avisos, incluye una concesión expresa de patentes y excluye
garantías y uso de marcas.

Si se aprueba, un PR posterior incorporará el texto oficial sin modificaciones en `LICENSE` y un
`NOTICE` con el alcance y las exclusiones. No se añadirá el archivo antes de resolver las
decisiones indicadas abajo.

## Alcance propuesto

Incluido, sujeto a confirmar titularidad:

- código original en `src/`, `app/` y `scripts/`;
- definiciones originales en `dataform/` y `sql/`;
- pruebas y fixtures completamente sintéticos;
- documentación técnica original creada para este repositorio.

Excluido expresamente:

- microdatos y agregados ENARES, diccionarios, tabulados, instrumentos y demás materiales del
  INEI, incluso si alguna evidencia autorizada se encuentra versionada;
- documentos, contenidos, logotipos y marcas de UNICEF o de otras instituciones;
- nombres, emblemas y marcas de INEI, UNICEF y terceros;
- dependencias y componentes de terceros, que conservan sus propias licencias;
- cualquier material cuya titularidad o permiso de redistribución no esté confirmado.

La disponibilidad pública de un archivo no se interpretará como autorización para relicenciarlo.

## Atribución propuesta

El futuro `NOTICE` identificaría el proyecto como “ENARES 2024 CRS04 — software Stage 04” y
declararía que Apache-2.0 cubre únicamente el software y material original enumerado. También
repetiría las exclusiones de datos, instrumentos, contenidos institucionales y marcas.

No se propone todavía un nombre para la línea de copyright: el titular legal no debe inferirse del
usuario de GitHub ni de la autoría de commits.

## Decisiones requeridas

1. Aprobar o rechazar `Apache-2.0`.
2. Confirmar el nombre exacto del titular que debe figurar en el aviso de copyright.
3. Confirmar el alcance de documentación original que puede quedar incluida.
4. Confirmar si existe alguna atribución de terceros adicional que deba entrar en `NOTICE`.

Hasta resolver los cuatro puntos, el repositorio continúa sin un `LICENSE` incorporado.

## Referencias normativas

- Texto oficial: <https://www.apache.org/licenses/LICENSE-2.0.txt>
- Guía oficial de aplicación: <https://www.apache.org/legal/apply-license>
