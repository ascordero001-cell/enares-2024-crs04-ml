# Stage 04 — revisión de frontera de notebooks

**Fecha:** 2026-09-15 UTC

**Estado:** VERIFIED

Los 19 notebooks versionados pertenecen a Stages 01–03 y se conservan como material histórico y
explicativo. Ninguno forma parte del runtime de Stage 04: la aplicación no los importa, la lógica
productiva vive en `src/`, `app/`, configuración, SQLX y tests, y el contenedor no instala Jupyter.

La revisión encontró 120 celdas con outputs guardados y 142 bloques de metadata de ejecución. Se
eliminaron mecánicamente outputs, contadores de ejecución y las claves `execution`,
`executionInfo` y `outputId`, sin modificar el contenido de las celdas. Esto retira, entre otros,
metadatos personales generados por Colab y evita conservar vistas accidentales de datos.

La suite inspecciona todos los `.ipynb` y falla si reaparece un output, un contador de ejecución o
metadata de ejecución. Los notebooks no autorizan acceso a Drive, BigQuery ni cloud; ejecutar un
notebook histórico sigue sujeto al gate y a las credenciales privadas correspondientes.
