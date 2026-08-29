# NAMING CONVENTIONS

## Documentos normativos de raíz

Usar `MAYUSCULAS_SNAKE.md`.

Ejemplos:

- `PRE_STAGE04.md`
- `NAMING_CONVENTIONS.md`
- `CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md`

`README.md` y `CONTRIBUTING.md` conservan sus nombres convencionales.

## Documentos de trabajo

Dentro de `docs/stage04/`, usar `snake_case.md`.

Ejemplos:

- `issue_map.md`
- `architecture.md`
- `v0_registry.md`

## Código Python

- módulos y funciones: `snake_case`;
- clases: `PascalCase`;
- constantes: `MAYUSCULAS_SNAKE`;
- pruebas: `test_<componente>.py`.

## Restricciones

No usar espacios, sufijos de descarga como `(1)`, rutas personales, credenciales ni nombres que revelen microdatos. Si un archivo cambia de nombre, sus enlaces internos deben actualizarse en el mismo PR.
