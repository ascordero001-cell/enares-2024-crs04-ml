# Contrato de exportación agregada — Stage 04

- Estado: `CANDIDATE_LOCAL_SHADOW`
- Fuente permitida: agregado V0 con procedencia verificada
- Publicación institucional y cutover: `NOT_AUTHORIZED`
- Cloud: `BLOCKED_BY_CLOUD_GATE`

## Alcance

La descarga reproduce exclusivamente el corte agregado que la aplicación muestra. No consulta
microdatos, Drive, `survey_input` ni una API distinta; no recalcula estimadores y no fabrica
desagregaciones o cruces ausentes de V0. Un fixture sintético no puede pasar la barrera de
exportación institucional.

CSV y Excel contienen la misma tabla semántica y las mismas filas, en el mismo orden. Cada fila
conserva el módulo, indicador, dimensión y categoría visible, identificadores fuente para
trazabilidad, estimación, error estándar, IC95 %, CV, `base_unw`, flags, nota de calidad,
universo, denominador y lineage del release. `N` se exporta con el nombre `base_unw`: es el
conteo real no ponderado del denominador, no una población expandida.

## Estadísticas ausentes y calidad

- Una estadística ausente se representa como celda vacía; nunca se imputa con cero.
- `CV > 0.15` y `base_unw < 30` permanecen visibles con sus flags y notas; no suprimen.
- La categoría visible deriva el marcador `[referencial]` de `cv_flag`; el texto fuente se
  conserva por separado y no codifica manualmente el estado de precisión.
- La política vigente no contiene umbral primario por recuento. La maquinaria de nulificación
  permanece disponible e inactiva mientras no exista una supresión primaria autorizada.
- Las filas de contexto no numérico no se presentan como métricas y no se exportan.

## Controles de archivo

1. Todo texto que empieza por `=`, `+`, `-` o `@` se escribe como literal con prefijo de
   apóstrofo en ambos formatos. Los números negativos genuinos conservan tipo y valor.
2. El XLSX es un paquete OOXML mínimo, determinista y sin fórmulas, propiedades de autor,
   timestamps variables, relaciones externas, hipervínculos, comentarios, notas, objetos
   incrustados, macros, hojas ocultas ni filas/columnas ocultas.
3. Rutas personales, URI `file:///` y enlaces de Drive se rechazan antes de producir una
   descarga.
4. El nombre descargado se normaliza a caracteres seguros y no incorpora valores de datos.
5. `.streamlit/config.toml` mantiene `disableDataExport = true`: bloquea la exportación genérica
   incorporada de componentes y obliga a usar únicamente este camino validado.

## Pruebas exigibles

- `tests/test_export_formats.py` vuelve a leer CSV y la hoja OOXML y exige igualdad de la tabla.
- `tests/test_xlsx_package_privacy.py` inspecciona el ZIP interno y bloquea metadata, fórmulas,
  relaciones externas y localizadores privados.
- Las pruebas de interfaz confirman que una descarga solo aparece para agregados V0 verificados,
  nunca para el demo sintético ni para una combinación sin datos.

Esta capacidad es una descarga técnica en `LOCAL_SHADOW_ONLY`. No convierte el prototipo en una
publicación institucional, no cambia el estado oficial de V0 y no autoriza nuevas cifras.
