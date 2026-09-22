# Integración del catálogo V0 en el rediseño

Fecha UTC: 2026-09-22

## Alcance

`app/ui_redesign_app.py` consume el repositorio autorizado ya existente y presenta
las 3,014 filas agregadas y los 516 indicadores del release vigente. La carga sigue
pasando por `load_validated_estimates`, la verificación de procedencia y las reglas
de granularidad. Esta integración no recalcula Stage 03, no construye cruces y no
modifica el archivo, el manifiesto, los hashes ni las claves del release.

La rama no cambia `app/streamlit_app.py`, los Dockerfiles, Cloud Run, IAM, BigQuery,
tráfico ni despliegue. La promoción del rediseño al entrypoint canónico continúa
sujeta a su PR y aprobación de despliegue específicos.

## Etiquetas comprensibles

La interfaz usa `src/enares/stage04/indicator_labels.py` como capa de presentación:

- el nombre comprensible es la información principal;
- `indicator_id` permanece visible como código secundario;
- el release conserva sin cambios sus campos `indicator_id` e `indicator_name`;
- los textos de preguntas e instituciones proceden de los diccionarios oficiales
  de variables CRS04;
- los nombres de indicadores derivados describen la semántica ya registrada en el
  diccionario Stage 03, sin alterar numeradores, denominadores ni universos.
- los grupos de personas agresoras se presentan por su significado documentado,
  nunca como un número de grupo;
- período, contexto y denominador distinguen indicadores que antes compartían
  texto;
- dentro de cada módulo no quedan nombres duplicados y el selector presenta
  `Nombre comprensible — indicator_id`.

Fuentes verificadas en Drive privado:

- `Diccionario de variables 20_CRS.04_CAP200.pdf`, id
  `19i-C6UCG3yafATOzOq0GH_UAl5K8wkuN`;
- `Diccionario de variables 21_CRS.04_CAP248.pdf`, id
  `1K1yEqd9xJO_SXL81oyS2zBSbLSkcDu1Z`;
- `Diccionario de variables 22_CRS.04_CAP300.pdf`, id
  `1v2Qu3aeQyMNZvnSQlYldR04N9Q-7_BqO`;
- `stage3_data_dictionary.md`, id
  `1YJsM3VFMhxovdHcwccxYD32r8L1RSftJ`;
- `diccionario_indicadores.xlsx`, id
  `1d6G9ccz4BjIEkzw7xb9NKyQMUiCCbLcT`.

No se versionan enlaces públicos, rutas personales, credenciales, microdatos ni
identificadores internos distintos de los ids de evidencia ya inventariados.

## Selección efectiva

El rediseño aplica una única selección a tabla, gráfico, alertas y ficha:

1. módulo;
2. una sola desagregación activa entre las ocho autorizadas;
3. estado de calidad;
4. indicador;
5. categoría.

Las opciones se derivan de filas verificadas. Una combinación ausente produce un
estado vacío. CV alto y N reducido continúan visibles con sus alertas; la interfaz
no transforma esos estados en supresión.

El filtro de módulo y la vista modular se sincronizan en ambos sentidos con el
título y el parámetro `view` de la URL. El forest plot se habilita solamente al
seleccionar un indicador y cada punto se identifica como `Indicador — categoría`;
por tanto, la vista inicial nunca superpone indicadores distintos bajo `Total`.

## Evidencia automática

- el fixture autorizado contiene exactamente 516 pares indicador-módulo;
- cada par obtiene un nombre principal no vacío, distinto del código, sin guiones
  bajos ni grupos numerados;
- los 516 nombres no tienen duplicados dentro de su módulo y el texto del selector
  conserva el código;
- las dos secuencias vista↔filtro mantienen alineados módulo, título y URL;
- el forest plot permanece oculto sin indicador y usa etiquetas inequívocas al
  activarse;
- la tabla muestra por separado `Indicador` y `Código`;
- una selección vacía no abre una ficha ajena;
- la tarjeta dorada de 3.2 conserva exactamente sus estadísticas aprobadas.
