# D06/D07: corrección versionada de etiquetas

Estado: **migración reproducible preparada; artefacto nuevo aún no emitido**.

La fuente privada aprobada es `ENARES_2024_PROJECT/04Outputs/tabulados_crs04_long.csv`,
fijada por SHA-256 `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`
en el [manifiesto V0](../stage04/v0_drive_hash_manifest.md). El productor
`ENARES_2024_PROJECT/03Scripts_R/tabulados.R` incorpora literalmente
`[referencial]` en cuatro categorías `3×3` de `Solap_VS_12M` y repite
esas mismas etiquetas en `Solap_VS_VIDA`. El CSV privado contiene ocho
marcadores de texto, pero solo cuatro de sus 16 filas D06/D07 tienen
`cv > 0.15`: cuatro en D06 y ninguna en D07. La columna `cv` está en escala
de proporción. Se contrastó el contenido de ambos objetos directamente en
Drive privado; no se usó una copia local como fuente de esta conclusión.

`scripts/migrate_stage03_vs_labels.py` prepara una **versión nueva** del CSV
agregado. Exige el SHA-256 congelado de entrada, 3.014 filas, ocho filas por
matriz, cuatro sufijos fuente por matriz y los conteos de CV anteriores.
Elimina únicamente esos ocho sufijos de `categoria`, conserva cada campo
numérico como texto exacto y rechaza sobrescribir una salida existente.
Imprime los hashes de entrada y salida para un nuevo manifiesto. Las pruebas
incluyen los límites `0.149999`, `0.15` y `0.150001`, paridad de campos,
rechazo de marcadores inesperados, hash incorrecto y destino existente.

Para completar el issue #101 falta:

1. Versionar el productor R en una copia nueva, retirando los cuatro sufijos
   literales de la sección D06/D07, sin sobrescribir el `tabulados.R` V0.
2. Ejecutar el productor versionado o la migración validada sobre el agregado
   privado aprobado; registrar hash, fecha, filas, conteos y paridad en un
   manifiesto nuevo. No subir el CSV al repositorio ni reemplazar V0.
3. Conciliar la salida con el diccionario y actualizar el consumo de Stage 04
   mediante su flujo normal de revisión. Verificar que interfaz y exportación
   derivan el marcador de `cv_flag`, sin segunda lógica de presentación.

Hasta completar esos pasos, V0 sigue congelado, Stage 04 utiliza su adaptador
vigente y el issue #101 permanece abierto. Esta preparación no autoriza
publicación, cutover ni nuevas cifras.
