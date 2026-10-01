# Ajuste visual y de etiquetas de #149

Fecha: 2026-10-01. Alcance: presentación del release V0 aprobado en la aplicación privada.

La revisión funcional de la candidata #167 reemplaza **solo** los anchos fijos de la
maqueta original. En pantallas de al menos 1080 px la grilla usa rieles de hasta
210/220 px y una columna central de al menos 55 % del contenedor; el ancho máximo
del contenedor pasa a 1600 px. Las seis tarjetas permanecen en una fila. Bajo
1080 px la página vuelve a una columna para no recortar contenido.

`display_taxonomy.py` es la única correspondencia versionada para nombres y
categorías de desagregaciones. Filtros, tabla, gráfico, ficha, alertas y exportación
usan estas funciones; el repositorio conserva los códigos originales. La exportación
mantiene `source_category` y `source_dimension` intactos y escribe la etiqueta
humana en `category` y `dimension`. Las categorías ausentes en V0 no se ofrecen.
Una categoría estándar nueva sin etiqueta bloquea la vista, no se muestra como
código. Las categorías binarias de otros cortes se presentan como No/Sí.

La carga de BigQuery se valida y fija una sola vez por proceso para la combinación
de tabla, `release_id`, `run_id` y hashes de los manifiestos aprobados. La caché
solo funciona en `AUTHENTICATED_SHADOW`; el modo local sigue validando cada lectura
para que las pruebas negativas detecten cambios de procedencia. No se omite la
verificación inicial ni se mezclan releases. Cada nueva identidad de release o
manifiesto produce una entrada independiente.

El gráfico no mezcla desagregaciones: presenta un bloque por corte, con categorías
ordenadas por estimación y nombres completos (26 departamentos en 3.2.1). Al elegir
un corte se conserva el bloque completo y se destaca la categoría elegida. La
línea nacional discontinua utiliza la cifra V0 preexistente; no recalcula nada.
Los temas mixtos muestran universo y N sin ponderar por contexto, sin expresiones
de sintaxis SPSS. Nacional es el estado inicial donde existe una fila nacional;
`Volver a Nacional` limpia los filtros.

Controles: suite Python completa, ruff, mypy, WCAG 2.2 AA y navegador a
1366×768, 1536×864 y 1920×1080. El navegador mide cada transición tarjeta→tema
y verifica etiquetas de filtros, 26 nombres departamentales completos y el retorno
a Nacional. Las capturas de revisión se generan fuera del control de versiones en
`artifacts/ui-parity/`; cualquier distribución de capturas de la aplicación privada
debe usar un canal privado, no una publicación abierta.

No cambian: CSV V0, hashes, valores, IC95%, CV, N, flags, catálogo de 80 temas,
permisos, IAM, facturación ni alcance institucional. El servicio permanece privado
y la revisión anterior se conserva para rollback.
